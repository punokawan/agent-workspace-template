#!/usr/bin/env bash
# Keep a Changelog (keepachangelog.com/1.1.0) generation from conventional commits.
#
#   changelog.sh init <target>
#   changelog.sh add <target> <slug>        — fold a worktree branch's commits into [Unreleased]
#   changelog.sh add-range <target> <range> — e.g. v1.1.0..HEAD, run in the main checkout
#   changelog.sh release <target> <version> — cut [Unreleased] into a dated version section
#   changelog.sh preview <target> <range>   — print entries without writing
#
# <target> is <project>/<repo>, or a bare <repo> when a project is active.

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

# conventional type -> Keep a Changelog section
section_for() {
  case "$1" in
    feat)                  echo "Added" ;;
    fix|hotfix)            echo "Fixed" ;;
    perf|refactor|style)   echo "Changed" ;;
    chore|config|build|ci) echo "Maintenance" ;;
    docs)                  echo "Documentation" ;;
    revert)                echo "Removed" ;;
    *)                     echo "" ;;   # unknown/non-conventional -> skipped
  esac
}
SECTIONS=("Added" "Changed" "Fixed" "Removed" "Documentation" "Maintenance")

# Resolve CHANGELOG.md. $2 (optional) is the directory the entries came from — when that is
# a worktree, the changelog is written THERE, never in the user's checkout.
# Call split_target first; this reads $REPO_DIR.
cl_path() {
  local dir="${1:-}"
  if [[ -n "$dir" && "$dir" == "$WT_DIR"/* ]]; then echo "$dir/CHANGELOG.md"
  else echo "$REPO_DIR/CHANGELOG.md"; fi
}

cmd_init() {
  split_target "${1:?target}"
  local f; f="${CL_TARGET:-$(cl_path)}"
  [[ -f "$f" ]] && { warn "already exists: $f"; return 0; }
  cat > "$f" <<'EOF'
# Changelog

All notable changes to this project are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Entries are generated from conventional commit subjects — write commit subjects as
user-facing documentation. See `.claude/skills/git-workflow/SKILL.md`.

## [Unreleased]

EOF
  ok "created $f"
}

# Emit "Section<TAB>entry" lines for a commit range in a given directory.
collect() {
  local dir="$1" range="$2"
  git -C "$dir" log --reverse --no-merges --pretty='%s' "$range" 2>/dev/null | while IFS= read -r s; do
    local re='^([a-z]+)(\(([^)]+)\))?!?: (.+)$'
    [[ "$s" =~ $re ]] || continue
    local type="${BASH_REMATCH[1]}" scope="${BASH_REMATCH[3]}" desc="${BASH_REMATCH[4]}"
    local sec; sec="$(section_for "$type")"
    [[ -z "$sec" ]] && continue
    if [[ -n "$scope" ]]; then printf '%s\t**%s:** %s\n' "$sec" "$scope" "$desc"
    else                       printf '%s\t%s\n' "$sec" "$desc"; fi
  done
}

write_entries() {   # <dir> <range>   (split_target already called)
  local dir="$1" range="$2"
  local f; f="$(cl_path "$dir")"
  if [[ ! -f "$f" ]]; then
    # seed a worktree changelog from the checkout's, so history is preserved
    if [[ -f "$REPO_DIR/CHANGELOG.md" ]]; then cp "$REPO_DIR/CHANGELOG.md" "$f"
    else CL_TARGET="$f" cmd_init "$PROJECT/$REPO"; fi
  fi

  local tmp; tmp="$(mktemp)"; collect "$dir" "$range" > "$tmp"
  if [[ ! -s "$tmp" ]]; then warn "no conventional commits in $range"; rm -f "$tmp"; return 0; fi

  python3 - "$f" "$tmp" "${SECTIONS[*]}" <<'PY'
import sys
f, tmp, order = sys.argv[1], sys.argv[2], sys.argv[3].split()
lines = open(f).read().split("\n")

new = {}
for l in open(tmp):
    if "\t" not in l: continue
    sec, entry = l.rstrip("\n").split("\t", 1)
    new.setdefault(sec, []).append(entry)

# locate [Unreleased] and the next version heading
try:
    start = next(i for i, l in enumerate(lines) if l.startswith("## [Unreleased]"))
except StopIteration:
    lines.insert(0, "## [Unreleased]"); lines.insert(1, ""); start = 0
end = next((i for i in range(start + 1, len(lines)) if lines[i].startswith("## [")), len(lines))

block = lines[start + 1:end]
# Entries keep their wrapped continuation lines; hand-written sections survive a fold.
existing, cur = {}, None
for l in block:
    if l.startswith("### "):
        cur = l[4:].strip(); existing.setdefault(cur, [])
    elif cur and l.strip().startswith("- "):
        existing[cur].append([l.strip()[2:]])
    elif cur and existing[cur] and l.startswith((" ", "\t")) and l.strip():
        existing[cur][-1].append(l.rstrip())

for sec, entries in new.items():
    have = {e[0] for e in existing.setdefault(sec, [])}
    for e in entries:
        if e not in have:
            existing[sec].append([e])

out = [""]
for sec in order + [s for s in existing if s not in order]:
    if existing.get(sec):
        out.append(f"### {sec}")
        out.append("")
        for e in existing[sec]:
            out.append(f"- {e[0]}")
            out += e[1:]
        out.append("")

open(f, "w").write("\n".join(lines[:start + 1] + out + lines[end:]))
n = sum(len(v) for v in new.values())
print(f"folded {n} entr{'y' if n==1 else 'ies'} into [Unreleased]")
PY
  rm -f "$tmp"
  ok "updated $f"
}

cmd_add() {
  split_target "${1:?target}"
  local slug="${2:?slug}"
  local wt; wt="$(wt_path "$PROJECT" "$REPO" "$slug")"
  [[ -d "$wt" ]] || die "no worktree: $wt"
  write_entries "$wt" "$(base_ref "$PROJECT" "$REPO")..HEAD"
}

cmd_add_range() {
  split_target "${1:?target}"
  write_entries "$REPO_DIR" "${2:?range}"
}

cmd_preview() {
  split_target "${1:?target}"
  local range="${2:?range}" dir="$REPO_DIR"
  # A bare slug in the range position means "that worktree's branch".
  if [[ -d "$(wt_path "$PROJECT" "$REPO" "$range")" ]]; then
    dir="$(wt_path "$PROJECT" "$REPO" "$range")"; range="$(base_ref "$PROJECT" "$REPO")..HEAD"
  fi
  collect "$dir" "$range" | awk -F'\t' '{ if ($1!=p) { print ""; print "### " $1; p=$1 } print "- " $2 }'
}

cmd_release() {
  split_target "${1:?target}"
  local ver="${2:?version}"
  [[ "$ver" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] || die "version must be semver x.y.z"
  local f; f="$(cl_path)"; [[ -f "$f" ]] || die "no CHANGELOG.md in $PROJECT/$REPO"
  grep -q "^## \[$ver\]" "$f" && die "version $ver already in changelog"

  python3 - "$f" "$ver" "$(date '+%Y-%m-%d')" <<'PY'
import sys
f, ver, today = sys.argv[1:4]
lines = open(f).read().split("\n")
s = next(i for i, l in enumerate(lines) if l.startswith("## [Unreleased]"))
e = next((i for i in range(s + 1, len(lines)) if lines[i].startswith("## [")), len(lines))
raw = [l for l in lines[s + 1:e] if l.strip()]
if not raw:
    sys.exit("nothing under [Unreleased] to release")
body = []
for l in raw:                       # restore the blank line after each section heading
    body.append(l)
    if l.startswith("### "):
        body.append("")
out = lines[:s + 1] + ["", f"## [{ver}] - {today}", ""] + body + [""] + lines[e:]
open(f, "w").write("\n".join(out))
print(f"cut {len(body)} lines into [{ver}] - {today}")
PY
  ok "released $ver in $f"
}

case "${1:-preview}" in
  init) shift; cmd_init "$@" ;;        add) shift; cmd_add "$@" ;;
  add-range) shift; cmd_add_range "$@" ;; release) shift; cmd_release "$@" ;;
  preview) shift; cmd_preview "$@" ;;
  *) die "usage: changelog.sh {init|add|add-range|release|preview}" ;;
esac
