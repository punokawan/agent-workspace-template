#!/usr/bin/env bash
# Shared constants + helpers for the studio agentic toolkit.
# Sourced by storage.sh, wt.sh, verify.sh, state.sh, changelog.sh, pr.sh, plan.sh, audit.sh.
#
# Nothing here knows the name of any project or repo. Everything comes from
# projects/<name>/project.json via _project.py — add a project by writing a
# manifest, never by editing this file.

set -euo pipefail

# Derived from this file's location (.claude/scripts/lib.sh -> workspace root), so the
# toolkit works from any checkout path. Override with STUDIO_ROOT if ever needed.
ROOT="${STUDIO_ROOT:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)}"
SCRIPTS="$ROOT/.claude/scripts"
WT_DIR="$ROOT/.wt"
CACHE_DIR="$ROOT/.cache"
STATE_DIR="$ROOT/.claude/agentic-state"
PROJECTS_DIR="$ROOT/projects"
TEMPLATES_DIR="$ROOT/templates"

# Max concurrent worktrees before LRU pruning kicks in.
WT_CAP="${STUDIO_WT_CAP:-10}"
# How recently a clean worktree must have been touched to be considered in use
# by someone else, and therefore not an LRU victim.
WT_IDLE_SECS="${STUDIO_WT_IDLE_SECS:-5400}"

die()  { printf '\033[31merror:\033[0m %s\n' "$*" >&2; exit 1; }
info() { printf '\033[36m▸\033[0m %s\n' "$*"; }
ok()   { printf '\033[32m✓\033[0m %s\n' "$*"; }
warn() { printf '\033[33m!\033[0m %s\n' "$*"; }

human() { # bytes -> human
  awk -v b="$1" 'BEGIN{
    split("B KB MB GB TB",u," ");i=1
    while(b>=1024&&i<5){b/=1024;i++}
    printf (i==1?"%.0f%s":"%.1f%s"),b,u[i]
  }'
}

free_bytes() { df -k /Users | awk 'NR==2{print $4*1024}'; }

# ---------------------------------------------------------------- registry

# Thin wrapper so no caller has to know where the registry lives.
proj() { STUDIO_ROOT="$ROOT" python3 "$SCRIPTS/_project.py" "$@"; }

# The project a bare repo id resolves against. Empty when several exist and none is set.
active_project() { proj active 2>/dev/null || true; }

all_projects() { proj list 2>/dev/null | awk '{print $2}'; }

# resolve_targets <spec...> -> lines of: project<TAB>repo<TAB>reldir<TAB>stack<TAB>integration
# Specs: all | <project> | <project>/all | <project>/<repo> | <repo>
resolve_targets() { proj resolve "$@"; }

# Absolute path to a checkout.
repo_dir() { echo "$ROOT/$(proj resolve "${1:?project}/${2:?repo}" | cut -f3)"; }

# Worktree + cache locations are <project>/<repo>/... so two projects never collide.
wt_root()    { echo "$WT_DIR/${1:?project}/${2:?repo}"; }
wt_path()    { echo "$WT_DIR/${1:?project}/${2:?repo}/${3:?slug}"; }
cache_path() { echo "$CACHE_DIR/${1:?project}/${2:?repo}/${3:?name}"; }

# Integration branch for a repo. The manifest declares it; git is consulted only when
# the declared branch has no remote ref, so a stale manifest degrades instead of lying.
# `main` is production and is NEVER a base for new work.
base_branch() {
  local p="${1:?project}" r="${2:?repo}" d b
  b="$(proj field "$p" "$r" integration 2>/dev/null || true)"
  d="$ROOT/$(proj resolve "$p/$r" 2>/dev/null | cut -f3)"
  [[ -n "$b" ]] || b="dev"
  [[ -d "$d/.git" || -f "$d/.git" ]] || { echo "$b"; return; }
  if git -C "$d" rev-parse --verify --quiet "refs/remotes/origin/$b" >/dev/null 2>&1; then
    echo "$b"; return
  fi
  for cand in dev development main; do
    if git -C "$d" rev-parse --verify --quiet "refs/remotes/origin/$cand" >/dev/null 2>&1; then
      echo "$cand"; return
    fi
  done
  echo "$b"
}

# The ref new work is cut from, and the ref a finished branch rebases onto.
# Prefers the LOCAL integration branch whenever it already contains
# origin's tip: work lands on the local branch, so cutting from origin/<base>
# while local is ahead by unpushed commits produces a branch that can never
# fast-forward. Falls back to origin/<base> when local is behind or absent.
base_ref() {
  local p="${1:?project}" r="${2:?repo}" b d
  b="$(base_branch "$p" "$r")"
  d="$ROOT/$(proj resolve "$p/$r" 2>/dev/null | cut -f3)"
  [[ -d "$d/.git" || -f "$d/.git" ]] || { echo "origin/$b"; return; }
  git -C "$d" rev-parse --verify --quiet "refs/heads/$b" >/dev/null 2>&1 || { echo "origin/$b"; return; }
  if git -C "$d" rev-parse --verify --quiet "refs/remotes/origin/$b" >/dev/null 2>&1; then
    git -C "$d" merge-base --is-ancestor "origin/$b" "$b" 2>/dev/null || { echo "origin/$b"; return; }
  fi
  echo "$b"
}

# Does <project>/<repo> exist in the registry?
is_repo() { proj resolve "${1:?project}/${2:?repo}" >/dev/null 2>&1; }

is_project() { local p="${1:?}"; [[ -f "$PROJECTS_DIR/$p/project.json" ]]; }

# Split a "project/repo" or bare spec into PROJECT and REPO globals.
# Fails loudly rather than guessing when a bare repo id has no active project.
split_target() {
  local line spec="${1:?target}"
  line="$(proj resolve "$spec")" || die "cannot resolve target: $spec"
  line="$(head -1 <<<"$line")"
  PROJECT="$(cut -f1 <<<"$line")"
  REPO="$(cut -f2 <<<"$line")"
  REPO_DIR="$ROOT/$(cut -f3 <<<"$line")"
  STACK="$(cut -f4 <<<"$line")"

  # A fully qualified target must resolve to itself. Nothing should be able to turn
  # <project>/<repo> into a different repo — but `wt.sh start` once
  # produced a worktree of another project's repo, cut from the wrong repository and placed under the
  # right path, and the root cause was never reproduced. The resolver is correct in isolation,
  # so the failure is either a race on the shared active-project pointer or an extra line
  # reaching `head -1`. This assertion does not explain it; it makes it loud at the point of
  # resolution rather than three steps later, where the symptom was an unrelated cache error.
  if [[ "$spec" == */* ]]; then
    local want_p="${spec%%/*}" want_r="${spec##*/}"
    if [[ "$want_r" != "all" && ( "$PROJECT" != "$want_p" || "$REPO" != "$want_r" ) ]]; then
      die "target '$spec' resolved to '$PROJECT/$REPO' — refusing to act on the wrong repository"
    fi
  fi
}

# Project-level directories (planning, docs) resolved from the manifest.
planning_dir() {
  local p="${1:-$(active_project)}" d
  [[ -n "$p" ]] || return 1
  d="$(proj meta "$p" planning 2>/dev/null || true)"
  [[ -n "$d" ]] && echo "$PROJECTS_DIR/$p/$d"
}

docs_dir() {
  local p="${1:-$(active_project)}" d
  [[ -n "$p" ]] || return 1
  d="$(proj meta "$p" docs 2>/dev/null | python3 -c 'import json,sys
try: print(json.load(sys.stdin).get("dir",""))
except Exception: print("")' || true)"
  [[ -n "$d" ]] && echo "$PROJECTS_DIR/$p/$d"
}
