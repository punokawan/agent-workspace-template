#!/usr/bin/env bash
# Isolated worktrees so new work never disturbs your main checkouts.
# Every worktree shares build caches (see storage-management) — ~180 MB, not ~9.7 GB.
#
#   wt.sh start <target> <type>/<slug> [--from <ref>]   (default base: the integration branch)
#   wt.sh list
#   wt.sh cd <target> <slug>        — print the path (use: cd "$(wt.sh cd ...)")
#   wt.sh drop <target> <slug> [--force]
#   wt.sh prune                     — enforce the LRU cap
#   wt.sh push <target> <slug>      — rebase on the integration branch + push
#   wt.sh land <target> <slug> [--keep] — ff-merge into the integration branch, then retire the
#                                    worktree (archive local-only files, drop, delete the branch)
#   wt.sh sweep [--apply]           — retire every clean, landed, idle worktree (dry run by default)
#   wt.sh sync-config <target> <slug> — re-copy untracked local config into an existing worktree
#
# <target> is <project>/<repo>, or a bare <repo> when a project is active.
# Worktrees live at .wt/<project>/<repo>/<slug> so two projects never collide.

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
STORAGE="$SCRIPTS/storage.sh"

VALID_TYPES="feat fix refactor chore hotfix release docs perf test"

slug_of() { echo "${1##*/}"; }

validate_branch() {
  local b="$1" t="${1%%/*}"
  [[ "$b" == */* ]] || die "branch must be <type>/<slug>, e.g. feat/wallet-archiving"
  grep -qw "$t" <<<"$VALID_TYPES" || die "type '$t' invalid. use one of: $VALID_TYPES"
  local s; s="$(slug_of "$b")"
  [[ "$s" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "slug must be kebab-case: '$s'"
  (( ${#b} <= 40 )) || die "branch name >40 chars: $b"
}

# .wt/<project>/<repo>/<slug> — three levels below .wt
# Only directories git still recognises as worktrees count against the cap. A
# dropped tree can leave an empty shell behind, and counting those blocks new
# work for no reason.
live_wt() {
  [[ -d "$WT_DIR" ]] || return 0  # no .wt yet: under pipefail the failing find would abort start
  find "$WT_DIR" -mindepth 3 -maxdepth 3 -type d 2>/dev/null | while read -r d; do
    if [[ -e "$d/.git" ]]; then echo "$d"; fi
  done
}
count_wt() { live_wt | wc -l | tr -d ' '; }
each_wt()  { find "$WT_DIR" -mindepth 3 -maxdepth 3 -type d 2>/dev/null | sort; }

# Decompose .wt/<project>/<repo>/<slug> back into its parts.
wt_parts() { # sets WPROJ WREPO WSLUG
  local rel="${1#"$WT_DIR"/}"
  WPROJ="${rel%%/*}"; rel="${rel#*/}"
  WREPO="${rel%%/*}"; WSLUG="${rel#*/}"
}

# Copy the untracked local files a worktree needs to build. The list comes from the stack
# preset (local_config), so a new stack declares its own without touching this script.
#
# Entries may be GLOBS. That matters: some generated output is gitignored and therefore
# absent from a fresh checkout, so a worktree that looks fine reports phantom analyzer
# errors and its tests fail to load. For Flutter that is the envied output under
# lib/config/environment/data/*.g.dart — 2 files, derived from the .env files copied
# alongside them. Copying is deliberate: regenerating them means a full build_runner run,
# and "never run two full builds at once" is a standing constraint here.
#
# These files can hold secrets. They are gitignored in the repo, so a worktree cannot
# commit them — same posture as .env and google-services.json.
copy_local_config() { # <project> <repo> <src-dir> <dest-dir>
  local project="$1" repo="$2" src="$3" dest="$4" cfg f rel n=0
  while IFS= read -r cfg; do
    [[ -n "$cfg" ]] || continue
    shopt -s nullglob
    for f in "$src"/$cfg; do
      rel="${f#"$src"/}"
      [[ -e "$dest/$rel" ]] && continue
      mkdir -p "$(dirname "$dest/$rel")"
      cp -R "$f" "$dest/$rel" 2>/dev/null && { ok "copied local config: $rel"; n=$((n+1)); }
    done
    shopt -u nullglob
  done < <(proj field "$project" "$repo" local_config)
  (( n == 0 )) && info "no local config to copy"
  return 0
}

# Re-run that copy for an existing worktree — recovers one created before a stack preset
# gained an entry, without dropping and re-cutting the branch.
# .wt/<project>/ sits outside projects/<project>/, so the project guide and skills would not
# load in a worktree. Link them in for Claude Code and Codex; .wt/ is gitignored.
link_project_context() { # <project>
  local p="$1" src="../../projects/$1" d
  [[ -f "$PROJECTS_DIR/$p/AGENTS.md" ]] && printf '@%s/AGENTS.md\n' "$src" > "$WT_DIR/$p/CLAUDE.md"
  for d in .claude .agents; do
    [[ -e "$PROJECTS_DIR/$p/$d" && ! -e "$WT_DIR/$p/$d" ]] && ln -s "$src/$d" "$WT_DIR/$p/$d"
  done
  return 0
}

# Once a project's last worktree is gone, remove its links and the empty folders.
unlink_project_context() { # <project>
  local dir="$WT_DIR/$1"
  [[ -d "$dir" ]] || return 0
  find "$dir" -mindepth 2 -maxdepth 2 -type d | grep -q . && return 0
  rm -f "$dir/CLAUDE.md" "$dir/.claude" "$dir/.agents"
  find "$dir" -type d -empty -delete
  return 0
}

cmd_sync_config() {
  split_target "${1:?target}"
  local slug="${2:?slug}" wt
  wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  [[ -d "$wt" ]] || die "no worktree: $wt"
  copy_local_config "$PROJECT" "$REPO" "$REPO_DIR" "$wt"
}

# LRU-prune until a slot is free.
#
# IT SAVES AND RESTORES split_target's GLOBALS, and that is not defensive tidying — it is the
# fix for a bug that twice cut a worktree from the wrong repository. cmd_prune drops another
# project's worktree by calling cmd_drop, cmd_drop calls split_target, and split_target writes
# PROJECT/REPO/REPO_DIR/STACK. A caller that resolved its own target BEFORE calling this got
# those globals silently replaced with whichever worktree happened to be least recently used,
# and then ran `git -C "$REPO_DIR" worktree add` against it: that once produced a
# worktree of one project's repo under another project's path, more than once.
#
# The assertion inside split_target could not catch it. Every call resolved correctly; the
# clobber happened afterwards, between the resolution and the use.
cmd_prune() {
  local saved_project="${PROJECT:-}" saved_repo="${REPO:-}"
  local saved_dir="${REPO_DIR:-}" saved_stack="${STACK:-}"
  local n; n="$(count_wt)"
  while (( n >= WT_CAP )); do
    local oldest
    oldest="$(live_wt | while read -r d; do echo "$(mtime "$d") $d"; done \
              | sort -n | head -1 | cut -d' ' -f2-)"
    [[ -n "$oldest" ]] || break
    wt_parts "$oldest"
    if [[ -n "$(git -C "$oldest" status --porcelain 2>/dev/null)" ]]; then
      die "LRU target $WPROJ/$WREPO/$WSLUG has uncommitted changes. Commit it, or run: wt.sh drop $WPROJ/$WREPO $WSLUG --force"
    fi
    # A clean tree is not an idle one. An agent that has only been reading, or
    # that is between edits, leaves no porcelain output, and concurrent sessions
    # share this cap — so recency is the only signal that someone is still in
    # there. Refuse rather than delete another session's working tree.
    local age=$(( $(date +%s) - $(mtime "$oldest") ))
    if (( age < WT_IDLE_SECS )); then
      die "cap $WT_CAP reached, and the LRU target $WPROJ/$WREPO/$WSLUG was used $(( age / 60 ))m ago — it may be in use by another session.
  Free a slot yourself:   wt.sh drop <project>/<repo> <slug>
  Or raise the cap:       STUDIO_WT_CAP=$(( WT_CAP + 1 )) wt.sh start ..."
    fi
    warn "cap $WT_CAP reached — LRU-pruning $WPROJ/$WREPO/$WSLUG (clean, last used $(fmt_mtime "$oldest"))"
    cmd_drop "$WPROJ/$WREPO" "$WSLUG" --force
    n="$(count_wt)"
  done

  PROJECT="$saved_project" REPO="$saved_repo" REPO_DIR="$saved_dir" STACK="$saved_stack"
}

cmd_start() {
  local target="${1:?<project>/<repo>}" branch="${2:?<type>/<slug>}"; shift 2
  split_target "$target"
  validate_branch "$branch"
  local from; from="$(base_ref "$PROJECT" "$REPO")"
  [[ "${1:-}" == "--from" ]] && from="${2:?ref}"

  local slug wt; slug="$(slug_of "$branch")"
  wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  [[ -d "$wt" ]] && die "worktree already exists: $wt"

  info "pre-flight: disk"
  bash "$STORAGE" report | sed -n '1,5p'
  local free; free=$(free_bytes)
  (( free < 8*1024*1024*1024 )) && die "only $(human "$free") free — run /disk-prune before starting new work"

  cmd_prune

  # Belt and braces for the clobber above: if anything between the resolution and here has
  # moved the target, say so rather than cutting a branch from the wrong repository.
  [[ "$REPO_DIR" == "$ROOT/$(proj resolve "$target" | head -1 | cut -f3)" ]] \
    || die "target '$target' moved to '$REPO_DIR' after pre-flight — refusing to cut a worktree from the wrong repository"

  info "fetching $PROJECT/$REPO"
  git -C "$REPO_DIR" fetch origin --prune --quiet || die "fetch failed"
  git -C "$REPO_DIR" rev-parse --verify "$from" >/dev/null 2>&1 || die "no such ref: $from"

  mkdir -p "$(dirname "$wt")"
  link_project_context "$PROJECT"
  if git -C "$REPO_DIR" show-ref --verify --quiet "refs/heads/$branch"; then
    info "branch $branch exists — checking it out"
    git -C "$REPO_DIR" worktree add "$wt" "$branch" || die "worktree add failed"
  else
    git -C "$REPO_DIR" worktree add -b "$branch" "$wt" "$from" || die "worktree add failed"
  fi

  # A worktree must belong to the repo we resolved. Concurrent sessions share
  # the active-project pointer, and a mismatch here means the new tree was cut
  # from a DIFFERENT repository — silent cross-project corruption. Fail loudly
  # and remove it rather than linking caches into the wrong repo.
  local wt_common expected_common
  wt_common="$(git -C "$wt" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
  expected_common="$(git -C "$REPO_DIR" rev-parse --path-format=absolute --git-common-dir 2>/dev/null || true)"
  if [[ -z "$wt_common" || "$wt_common" != "$expected_common" ]]; then
    git -C "$REPO_DIR" worktree remove --force "$wt" 2>/dev/null || rm -rf "$wt"
    die "worktree at $wt belongs to $wt_common, expected $expected_common — resolution raced with another session; retry"
  fi

  info "linking shared build caches"
  bash "$STORAGE" link "$PROJECT" "$REPO" "$slug"

  info "copying untracked local config"
  copy_local_config "$PROJECT" "$REPO" "$REPO_DIR" "$wt"

  ok "worktree ready: $wt"
  echo "  target : $PROJECT/$REPO"
  echo "  branch : $branch  (from $from)"
  echo "  size   : $(du -sh "$wt" 2>/dev/null | cut -f1)"
  echo "  slots  : $(count_wt)/$WT_CAP"
  echo "  cd $wt"
}

cmd_list() {
  printf '%-26s %-26s %-8s %s\n' "PROJECT/REPO" "BRANCH" "SIZE" "STATUS"
  local n=0
  while IFS= read -r d; do
    [[ -n "$d" ]] || continue
    n=$((n+1))
    wt_parts "$d"
    local br dirty ahead
    br="$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null)"
    dirty="clean"; [[ -n "$(git -C "$d" status --porcelain 2>/dev/null)" ]] && \
      dirty="dirty($(git -C "$d" status --porcelain | wc -l | tr -d ' '))"
    ahead="$(git -C "$d" rev-list --count "$(base_ref "$WPROJ" "$WREPO")..HEAD" 2>/dev/null || echo '?')"
    printf '%-26s %-26s %-8s %s, +%s commits\n' "$WPROJ/$WREPO" "$br" \
      "$(du -sh "$d" 2>/dev/null | cut -f1)" "$dirty" "$ahead"
  done < <(each_wt)
  (( n == 0 )) && echo "(no worktrees)"
  printf '\n%s/%s slots used\n' "$n" "$WT_CAP"
}

cmd_cd() {
  split_target "${1:?target}"
  local p; p="$(wt_path "$PROJECT" "$REPO" "${2:?slug}")"
  [[ -d "$p" ]] || die "no worktree: $p"
  echo "$p"
}

cmd_drop() {
  split_target "${1:?target}"
  local slug="${2:?slug}" force="${3:-}"
  local wt; wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  [[ -d "$wt" ]] || die "no worktree: $wt"
  if [[ -n "$(git -C "$wt" status --porcelain 2>/dev/null)" && "$force" != "--force" ]]; then
    git -C "$wt" status --short
    die "uncommitted changes in $PROJECT/$REPO/$slug — commit them, or re-run with --force to discard"
  fi
  local br; br="$(git -C "$wt" rev-parse --abbrev-ref HEAD 2>/dev/null)"
  git -C "$REPO_DIR" worktree remove --force "$wt" || die "worktree remove failed"
  git -C "$REPO_DIR" worktree prune
  unlink_project_context "$PROJECT"
  if [[ -n "${WT_RETIRING:-}" ]]; then ok "removed worktree $PROJECT/$REPO/$slug"
  else ok "removed worktree $PROJECT/$REPO/$slug (branch $br kept — delete with: git -C $REPO_DIR branch -d $br)"; fi
}

# ---- retiring landed worktrees -------------------------------------------------------
# A worktree whose branch is fully on the local integration branch holds nothing git does
# not already have, except gitignored local files (run ledgers, review diffs, an edited
# .env). Those are archived first, so retiring a worktree never loses anything.
WT_ARCHIVE_DIR="$CACHE_DIR/wt-archive"
WT_ARCHIVE_MAX_KB=$(( ${STUDIO_WT_ARCHIVE_MAX_MB:-200} * 1024 ))

# Is <wt>'s HEAD contained in the local integration branch (origin's when there is no local)?
wt_is_landed() { # <wt> <repo_dir> <base>
  local into="refs/heads/$3"
  git -C "$2" rev-parse --verify --quiet "$into" >/dev/null || into="refs/remotes/origin/$3"
  git -C "$2" merge-base --is-ancestor "$(git -C "$1" rev-parse HEAD)" "$into" 2>/dev/null
}

# Gitignored paths worth keeping. Skipped: node_modules, cache symlinks, the stack's build
# output (prune_dirs, e.g. .next, build), *.tsbuildinfo, and local config copies identical to
# the main checkout's. One path per line.
wt_local_only() { # <wt> <repo_dir> <project> <repo>
  local p build
  build="$(proj field "$3" "$4" prune_dirs 2>/dev/null || true)"
  git -C "$1" status --ignored --porcelain=v1 2>/dev/null | sed -n 's/^!! //p' | while IFS= read -r p; do
    p="${p%/}"
    [[ -L "$1/$p" ]] && continue
    case "/$p/" in */node_modules/*) continue ;; esac
    case "$p" in *.tsbuildinfo) continue ;; esac
    if [[ -n "$build" ]] && grep -qxF "${p%%/*}" <<<"$build"; then continue; fi
    if [[ -f "$1/$p" && -f "$2/$p" ]] && cmp -s "$1/$p" "$2/$p"; then continue; fi
    echo "$p"
  done
}

# A file touched inside the idle window means a session may still be in there. Clean is not idle.
# Prints the first such path (find -quit: no `| head`, which SIGPIPEs under pipefail).
wt_recent_change() { # <wt>
  local mins=$(( (WT_IDLE_SECS + 59) / 60 )) gd hit
  hit="$(find "$1" \( -name node_modules -o -name .git \) -prune -o -type f -mmin "-$mins" -print -quit 2>/dev/null || true)"
  if [[ -z "$hit" ]]; then
    gd="$(git -C "$1" rev-parse --absolute-git-dir 2>/dev/null || true)"
    [[ -n "$gd" ]] && hit="$(find "$gd" -maxdepth 1 -type f -mmin "-$mins" -print -quit 2>/dev/null || true)"
  fi
  echo "$hit"
}

# Archive local-only files, remove the worktree, delete its (verified-landed) local branch.
retire_wt() { # <project> <repo> <slug>
  local wt repo_dir base br files kb archive=""
  wt="$(wt_path "$1" "$2" "$3")"; repo_dir="$(repo_dir "$1" "$2")"; base="$(base_branch "$1" "$2")"
  br="$(git -C "$wt" rev-parse --abbrev-ref HEAD)"
  [[ -z "$(git -C "$wt" status --porcelain)" ]] || die "$1/$2/$3 has uncommitted changes — not retiring it"
  wt_is_landed "$wt" "$repo_dir" "$base" || die "$1/$2/$3 ($br) is not fully on $base — not retiring it"
  files="$(wt_local_only "$wt" "$repo_dir" "$1" "$2")"
  if [[ -n "$files" ]]; then
    kb="$(cd "$wt" && printf '%s\n' "$files" | tr '\n' '\0' | xargs -0 du -sk 2>/dev/null | awk '{s+=$1} END {print s+0}')"
    (( kb <= WT_ARCHIVE_MAX_KB )) || die "$1/$2/$3 holds ${kb} KB of local-only files (cap $(( WT_ARCHIVE_MAX_KB / 1024 )) MB) — back them up, then wt.sh drop"
    archive="$WT_ARCHIVE_DIR/$1/$2/$3-$(date +%Y%m%d-%H%M%S).tar.gz"
    mkdir -p "$(dirname "$archive")"
    printf '%s\n' "$files" | tar -czf "$archive" -C "$wt" -T - || die "archiving local files of $1/$2/$3 failed — nothing removed"
    info "archived local-only files → ${archive#"$ROOT"/}"
  fi
  local tip; tip="$(git -C "$wt" rev-parse HEAD)"
  WT_RETIRING=1 cmd_drop "$1/$2" "$3"
  # Landed was verified above, so this is `branch -d` semantics against the integration branch
  # (plain -d would compare against whatever the main checkout has checked out).
  if [[ "$br" != "HEAD" && "$br" != "$base" && "$br" != "main" ]] \
     && git -C "$repo_dir" update-ref -d "refs/heads/$br" "$tip" 2>/dev/null; then
    ok "deleted local branch $br (fully on $base)"
  fi
  if git -C "$repo_dir" rev-parse --verify --quiet "refs/remotes/origin/$br" >/dev/null; then
    warn "remote branch origin/$br still exists — deleting it is outward-facing, ask first:"
    echo "    git -C ${repo_dir#"$ROOT"/} push origin --delete $br"
  fi
}

# Every worktree that is clean, fully landed and idle. Dry run unless --apply.
cmd_sweep() {
  local apply="${1:-}" found=0 kept=0 d br base repo_dir reason here files
  [[ -z "$apply" || "$apply" == "--apply" ]] || die "usage: wt.sh sweep [--apply]"
  here="$(git rev-parse --show-toplevel 2>/dev/null || true)"
  while IFS= read -r d; do
    [[ -n "$d" ]] || continue
    wt_parts "$d"
    is_repo "$WPROJ" "$WREPO" || continue
    repo_dir="$(repo_dir "$WPROJ" "$WREPO")"; base="$(base_branch "$WPROJ" "$WREPO")"
    br="$(git -C "$d" rev-parse --abbrev-ref HEAD 2>/dev/null)"
    reason=""
    if [[ "$d" == "$here" ]]; then reason="this session's own worktree"
    elif [[ -n "$(git -C "$d" status --porcelain 2>/dev/null)" ]]; then reason="uncommitted changes"
    elif ! wt_is_landed "$d" "$repo_dir" "$base"; then
      reason="$(git -C "$repo_dir" rev-list --count "$base..$(git -C "$d" rev-parse HEAD)" 2>/dev/null || echo '?') commit(s) not on $base"
    elif [[ -n "$(wt_recent_change "$d")" ]]; then reason="changed in the last $(( WT_IDLE_SECS / 60 )) min — may be in use"
    fi
    if [[ -n "$reason" ]]; then
      kept=$((kept+1)); printf '  keep   %-40s %s\n' "$WPROJ/$WREPO/$WSLUG" "$reason"; continue
    fi
    found=$((found+1))
    printf '  retire %-40s %s, %s, landed on %s\n' "$WPROJ/$WREPO/$WSLUG" "$br" "$(du -sh "$d" 2>/dev/null | cut -f1)" "$base"
    files="$(wt_local_only "$d" "$repo_dir" "$WPROJ" "$WREPO")"
    [[ -z "$files" ]] || printf '%s\n' "$files" | sed -n '1,6s/^/           keep in archive: /p'
    if [[ "$apply" == "--apply" ]]; then ( retire_wt "$WPROJ" "$WREPO" "$WSLUG" ) || warn "skipped $WPROJ/$WREPO/$WSLUG"; fi
  done < <(live_wt | sort)
  echo
  if (( found == 0 )); then ok "nothing to retire ($kept kept)"
  elif [[ "$apply" == "--apply" ]]; then ok "retired $found worktree(s), $kept kept — $(count_wt)/$WT_CAP slots used"
  else info "$found worktree(s) can be retired, $kept kept. Dry run — re-run with: wt.sh sweep --apply"
  fi
}

cmd_push() {
  split_target "${1:?target}"
  local slug="${2:?slug}"
  local wt; wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  [[ -d "$wt" ]] || die "no worktree: $wt"
  local br; br="$(git -C "$wt" rev-parse --abbrev-ref HEAD)"
  [[ -z "$(git -C "$wt" status --porcelain)" ]] || { git -C "$wt" status --short; die "commit your changes first"; }

  local base; base="$(base_ref "$PROJECT" "$REPO")"
  info "rebasing $br onto $base"
  git -C "$wt" fetch origin --quiet
  git -C "$wt" rebase "$base" || die "rebase conflicts — resolve in $wt, then re-run"

  info "pushing $br"
  git -C "$wt" push -u origin "$br" || die "push failed"

  echo
  echo "=== READY TO LAND (branch $br, $PROJECT/$REPO -> $base) ==="
  echo "--- commits ---"
  git -C "$wt" log --reverse --pretty='  %s' "$base..HEAD"
  echo "--- files ---"
  git -C "$wt" diff --stat "$base..HEAD" | tail -30
  echo "--- remote ---"
  git -C "$wt" remote get-url origin
}

# Fast-forward the integration branch onto this worktree's branch, then delete the branch.
# No PR: feature work lands directly on the integration branch. `main` is never touched here.
cmd_land() {
  split_target "${1:?target}"
  local slug="${2:?slug}"
  local wt; wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  [[ -d "$wt" ]] || die "no worktree: $wt"
  local br base; br="$(git -C "$wt" rev-parse --abbrev-ref HEAD)"
  base="$(base_branch "$PROJECT" "$REPO")"
  [[ "$br" == "main" || "$br" == "$base" ]] && die "refusing to land '$br' — that is a long-lived branch"
  [[ -z "$(git -C "$wt" status --porcelain)" ]] || { git -C "$wt" status --short; die "commit your changes first"; }

  git -C "$wt" fetch origin --quiet
  # Rebase onto whatever this branch will actually fast-forward INTO. Local
  # <base> can carry commits origin has not seen; rebasing onto origin/<base>
  # then refuses the ff-merge below.
  local onto; onto="$(base_ref "$PROJECT" "$REPO")"
  git -C "$wt" rebase "$onto" || die "rebase conflicts — resolve in $wt, then re-run"

  local n; n="$(git -C "$wt" rev-list --count "$onto..HEAD")"
  (( n > 0 )) || { warn "$br has no commits above $onto — nothing to land"; return 0; }
  info "landing $n commit(s) from $br onto $base"

  [[ -z "$(git -C "$REPO_DIR" status --porcelain)" ]] || die "$PROJECT/$REPO checkout is dirty — cannot land into $base"
  local prev; prev="$(git -C "$REPO_DIR" rev-parse --abbrev-ref HEAD)"
  git -C "$REPO_DIR" checkout "$base" --quiet || die "cannot checkout $base in $PROJECT/$REPO"
  git -C "$REPO_DIR" merge --ff-only "$br" || { git -C "$REPO_DIR" checkout "$prev" --quiet; die "not a fast-forward — re-run the rebase"; }
  ok "$base fast-forwarded to $(git -C "$REPO_DIR" rev-parse --short HEAD)"

  # Landed work leaves nothing in the worktree git lacks: retire it now (local-only files are
  # archived first) so slots and disk come back. --keep holds it, e.g. for a follow-up fix.
  local project="$PROJECT" repo="$REPO" repo_dir="$REPO_DIR"
  if [[ "${3:-}" == "--keep" ]]; then
    info "worktree kept (--keep) — retire it later with: wt.sh sweep --apply"
  else
    retire_wt "$project" "$repo" "$slug"
  fi

  warn "push is outward-facing — run this yourself when ready:"
  echo "    git -C $repo_dir push origin $base"
}

case "${1:-list}" in
  start) shift; cmd_start "$@" ;;   list) cmd_list ;;
  cd)    shift; cmd_cd "$@" ;;      drop) shift; cmd_drop "$@" ;;
  prune) cmd_prune ;;               push) shift; cmd_push "$@" ;;
  land)  shift; cmd_land "$@" ;;    sweep) shift; cmd_sweep "$@" ;;
  sync-config) shift; cmd_sync_config "$@" ;;
  *) die "usage: wt.sh {start|list|cd|drop|prune|push|land|sweep|sync-config}" ;;
esac
