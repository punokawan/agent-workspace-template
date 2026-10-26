#!/usr/bin/env bash
# Generate a PR description grounded in real commits, a real diff, and a real
# verification run — then open the PR if `gh` is available.
#
#   pr.sh body <target> <slug> [verification-file]  — write the PR body, print path
#   pr.sh open <target> <slug> [--draft]            — push, then create the PR via gh
#   pr.sh preview <target> <slug>                   — print the body to stdout
#
# <target> is <project>/<repo>, or a bare <repo> when a project is active.
# Feature work does NOT use pull requests (see AGENTS.md) — this is for the exceptions.

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"


TYPE_LABEL() {
  case "$1" in
    feat) echo "Features" ;;        fix) echo "Fixes" ;;
    perf) echo "Performance" ;;     refactor) echo "Refactoring" ;;
    docs) echo "Documentation" ;;   test) echo "Tests" ;;
    chore|config|style) echo "Maintenance" ;;
    *) echo "Other" ;;
  esac
}

build_body() {
  split_target "$1"
  local repo="$PROJECT/$REPO" slug="$2" vfile="${3:-}"
  local wt; wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  [[ -d "$wt" ]] || die "no worktree: $wt"
  local br; br="$(git -C "$wt" rev-parse --abbrev-ref HEAD)"
  local range; range="$(base_ref "$PROJECT" "$REPO")..HEAD"

  local n; n="$(git -C "$wt" rev-list --count $range 2>/dev/null || echo 0)"
  (( n > 0 )) || die "no commits on $br above $(base_ref "$PROJECT" "$REPO")"

  echo "## Summary"
  echo
  # Lead with the highest-signal commit subject, de-prefixed.
  git -C "$wt" log --reverse --pretty='%s' $range | head -1 | sed -E 's/^[a-z]+(\([^)]*\))?: //' \
    | awk '{ printf "%s%s\n", toupper(substr($0,1,1)), substr($0,2) }'
  echo
  echo "Branch \`$br\` → \`main\` in \`$repo\`, $n commit(s)."
  echo

  echo "## Changes"
  echo
  local seen=""
  for t in feat fix perf refactor docs test chore config style; do
    local lines; lines="$(git -C "$wt" log --reverse --pretty='%s' $range | grep -E "^${t}(\(|:)" || true)"
    [[ -z "$lines" ]] && continue
    local lbl; lbl="$(TYPE_LABEL "$t")"
    grep -q "^$lbl\$" <<<"$seen" || { echo "### $lbl"; echo; seen="$seen"$'\n'"$lbl"; }
    while IFS= read -r l; do
      [[ -z "$l" ]] && continue
      echo "- ${l#*: }$(sed -nE 's/^[a-z]+\(([^)]*)\).*/  _(\1)_/p' <<<"$l")"
      :
    done <<<"$lines"
    echo
  done

  echo "## Files changed"
  echo
  echo '```'
  git -C "$wt" diff --stat $range | tail -40
  echo '```'
  echo

  echo "## Verification"
  echo
  if [[ -n "$vfile" && -f "$vfile" ]]; then
    echo '```'
    cat "$vfile"
    echo '```'
  else
    echo "> \`unverified\` — no verification record supplied."
    echo "> Run \`bash .claude/scripts/verify.sh wt:$repo/$slug --full\` and regenerate."
  fi
  echo

  echo "## Risk"
  echo
  local touched; touched="$(git -C "$wt" diff --name-only $range)"
  echo "- **Blast radius:** $(wc -l <<<"$touched" | tr -d ' ') file(s) in \`$repo\`"
  grep -qE 'migration|\.sql$'           <<<"$touched" && echo "- ⚠️ **Database migration** — review rollback path before merge"
  grep -qE 'workflow|\.github/'         <<<"$touched" && echo "- ⚠️ **CI/CD change** — affects the delivery pipeline"
  grep -qE 'injector|routes?\.|main\.'  <<<"$touched" && echo "- ⚠️ **Wiring/entry-point change** — affects app startup or routing"
  grep -qE 'middleware'                 <<<"$touched" && echo "- 🔴 **Middleware change** — runs on *every* request; a regression here affects all endpoints"
  grep -qE 'auth|identity|jwt|password|token' <<<"$touched" && echo "- 🔴 **Auth/identity change** — review the failure mode when the check does not pass"
  grep -qE 'subscription|purchase|voucher|wallet|transaction' <<<"$touched" && echo "- ⚠️ **Money-handling code** — verify amounts, currency, and idempotency"
  grep -qE '\.arb$'                     <<<"$touched" && echo "- ℹ️ Localization strings changed — all 10 locales must stay in sync"
  grep -qE 'pubspec|go\.mod|package\.json' <<<"$touched" && echo "- ⚠️ **Dependency change** — verify lockfile and licence implications"
  echo

  echo "## Checklist"
  echo
  echo "- [ ] Rebased on \`main\`, no merge commits"
  echo "- [ ] \`verify.sh\` exits 0 for this repo"
  echo "- [ ] No secrets, tokens, or customer PII in the diff"
  echo "- [ ] CHANGELOG.md updated"
  echo "- [ ] Branch deleted after merge"
}

cmd_body() {
  split_target "${1:?target}"
  local slug="${2:?slug}" vfile="${3:-}"
  local out; out="$(wt_path "$PROJECT" "$REPO" "$slug")/.pr-body.md"
  build_body "$PROJECT/$REPO" "$slug" "$vfile" > "$out"
  ok "PR body written: $out"
  echo "$out"
}

cmd_preview() { build_body "${1:?target}" "${2:?slug}" "${3:-}"; }

cmd_open() {
  split_target "${1:?target}"
  local repo="$PROJECT/$REPO" slug="${2:?slug}"; shift 2
  local draft=""; [[ "${1:-}" == "--draft" ]] && draft="--draft"
  local wt; wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  local br; br="$(git -C "$wt" rev-parse --abbrev-ref HEAD)"
  local body="$wt/.pr-body.md"
  [[ -f "$body" ]] || die "run 'pr.sh body $repo $slug <verification-file>' first"

  local title; title="$(git -C "$wt" log --reverse --pretty='%s' "$(base_ref "$PROJECT" "$REPO")..HEAD" | head -1)"

  if ! command -v gh >/dev/null 2>&1; then
    warn "gh CLI not installed — cannot open the PR automatically."
    echo
    echo "Install:  brew install gh && gh auth login"
    echo "Or open manually:"
    echo "  $(git -C "$wt" remote get-url origin | sed -E 's#git@github.com:#https://github.com/#; s#\.git$##')/compare/main...$br?expand=1"
    echo "  title: $title"
    echo "  body : $body"
    return 3
  fi

  git -C "$wt" push -u origin "$br" --quiet || die "push failed"
  (cd "$wt" && gh pr create --base main --head "$br" --title "$title" --body-file "$body" $draft) \
    || die "gh pr create failed"
  ok "PR opened"
}

case "${1:-preview}" in
  body) shift; cmd_body "$@" ;;  open) shift; cmd_open "$@" ;;
  preview) shift; cmd_preview "$@" ;;
  *) die "usage: pr.sh {body|open|preview} <target> <slug> [verification-file|--draft]" ;;
esac
