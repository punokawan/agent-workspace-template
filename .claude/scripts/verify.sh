#!/usr/bin/env bash
# Ground-truth verification. Runs REAL toolchain checks and prints REAL output.
# Nothing here is inferred — every PASS/FAIL is an actual exit code.
#
#   verify.sh [target ...] [--quick|--full]
#     target: <project>/<repo> | <repo> | <project> | all
#             wt:<project>/<repo>/<slug>   — verify inside a worktree
#             (default: every repo with uncommitted changes, across all projects)
#     --quick (default): static analysis only — safe to run in parallel across worktrees
#     --full            : adds tests/builds. NOT parallel-safe (shared build cache).
#
# This script knows no stacks and no repos. What to run comes from the stack preset
# named by each repo's manifest entry (templates/stacks/<stack>.json), so adding a
# language means adding a preset, never editing this file.
#
# Every check runs with STUDIO_VERIFY_SCRATCH set to a sanitised per-target id
# (<repo> for a checkout, <repo>_<slug> for a worktree) for naming scratch resources.
# Complete output stays in a temporary log; a compact durable result is written under
# .claude/verify-results/. Timeout defaults: 45m total, 15m without output.

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
set +e +u   # report failures rather than aborting; empty arrays are normal here

export PATH="$ROOT/.claude/shims:$PATH"   # flutter/dart at the .fvmrc version: see shims/_pinned
MODE="quick"
SPECS=""       # newline-separated target specs
WT_SPECS=""    # newline-separated "project<TAB>repo<TAB>dir" for worktree targets

for a in "$@"; do
  case "$a" in
    --quick) MODE=quick ;;
    --full)  MODE=full ;;
    wt:*)    spec="${a#wt:}"
             wproj="${spec%%/*}"; rest="${spec#*/}"
             wrepo="${rest%%/*}"; wslug="${rest#*/}"
             [[ "$rest" == */* ]] || die "worktree target must be wt:<project>/<repo>/<slug>: $a"
             WT_SPECS="$WT_SPECS$wproj	$wrepo	$WT_DIR/$wproj/$wrepo/$wslug
" ;;
    *)       SPECS="$SPECS$a
" ;;
  esac
done

RESOLVED=""
if [[ -n "$SPECS" ]]; then
  RESOLVED="$(proj resolve $(printf '%s' "$SPECS" | grep -v '^$' | tr '\n' ' '))" || exit 2
fi

# Auto-detect: verify only repos with uncommitted changes, anywhere in the workspace.
if [[ -z "$RESOLVED" && -z "$WT_SPECS" ]]; then
  ALL="$(proj resolve all)"
  DIRTY=""
  while IFS='	' read -r p r reldir stack integ; do
    [[ -n "$p" ]] || continue
    d="$ROOT/$reldir"
    [[ -e "$d/.git" ]] || continue
    if [[ -n "$(git -C "$d" status --porcelain 2>/dev/null)" ]]; then
      DIRTY="$DIRTY$p	$r	$reldir	$stack	$integ
"
    fi
  done <<< "$ALL"
  if [[ -n "$DIRTY" ]]; then RESOLVED="$DIRTY"; else RESOLVED="$ALL"; fi
fi

LOG="$(mktemp "${TMPDIR:-/tmp}/studio-verify.XXXXXX")"
RESULT_DIR="$ROOT/.claude/verify-results"
mkdir -p "$RESULT_DIR"
RESULT="$RESULT_DIR/$(date '+%Y%m%d-%H%M%S')-$$.txt"
TIMEOUT_SECONDS="${STUDIO_VERIFY_TIMEOUT_SECONDS:-2700}"
STALL_SECONDS="${STUDIO_VERIFY_STALL_SECONDS:-900}"
FAILED=(); PASSED=(); SKIPPED=()

run_check() {
  local name="$1" dir="$2"; shift 2
  printf '\n\033[1m── %s\033[0m\n' "$name"
  local check_log rc started elapsed
  check_log="$(mktemp "${TMPDIR:-/tmp}/studio-check.XXXXXX")"
  started="$(date +%s)"
  (cd "$dir" && python3 "$ROOT/.claude/scripts/_run_check.py" "$check_log" "$TIMEOUT_SECONDS" "$STALL_SECONDS" "$@")
  rc=$?
  elapsed=$(( $(date +%s) - started ))
  # Only failure-focused output reaches the agent; the complete output stays in $LOG.
  if (( rc != 0 )); then
    grep -E -i '(^|[^a-z])(fail(ed|ure|ing)?|error|panic|fatal|expected|actual|timeout|timed out)([^a-z]|$)' "$check_log" | tail -20
    tail -8 "$check_log"
  fi
  { echo "===== $name (exit $rc, ${elapsed}s) ====="; echo "\$ $*"; cat "$check_log"; } >> "$LOG"
  rm -f "$check_log"
  printf '%s\texit=%d\tduration=%ss\n' "$name" "$rc" "$elapsed" >> "$RESULT"
  if (( rc == 0 )); then PASSED+=("$name"); printf '\033[32m  PASS\033[0m (exit 0)\n'
  else FAILED+=("$name (exit $rc)"); printf '\033[31m  FAIL\033[0m (exit %d)\n' "$rc"; fi
}

# Lowercase [a-z0-9_] only, so a check can splice it into an identifier without quoting.
scratch_id() { printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | tr -c 'a-z0-9_' '_' | cut -c1-40; }

# Run every check the manifest declares for one checkout.
verify_dir() {
  local project="$1" repo="$2" dir="$3" label="$4" scratch="$5"
  if [[ ! -d "$dir" ]]; then SKIPPED+=("$label (no dir)"); return; fi
  local lock="${TMPDIR:-/tmp}/studio-verify-${scratch}-${MODE}.lock" owner
  if ! mkdir "$lock" 2>/dev/null; then
    owner="$(cat "$lock/pid" 2>/dev/null)"
    if [[ -n "$owner" ]] && kill -0 "$owner" 2>/dev/null; then
      FAILED+=("$label (verification already running as pid $owner)")
      printf '\n\033[31m  FAIL\033[0m %s verification already running as pid %s\n' "$label" "$owner"
      return
    fi
    rm -rf "$lock"
    mkdir "$lock" || { FAILED+=("$label (cannot acquire verification lock)"); return; }
  fi
  echo "$$" > "$lock/pid"
  # Per-target id for scratch resources (databases, ports) so concurrent gates never share one.
  export STUDIO_VERIFY_SCRATCH="$scratch"
  printf '\n\033[1m### %s  (%s)\033[0m\n' "$label" "${dir/#$ROOT\//}"
  local line name skipmsg
  while IFS= read -r -u 3 line; do
    [[ -n "$line" ]] || continue
    name="$(printf '%s' "$line" | python3 -c 'import json,sys;print(json.load(sys.stdin)["name"])')"
    skipmsg="$(printf '%s' "$line" | python3 -c 'import json,sys;print(json.load(sys.stdin).get("skip",""))')"
    if [[ -n "$skipmsg" ]]; then
      SKIPPED+=("$label: $name ($skipmsg)")
      continue
    fi
    # NUL-delimited argv so arguments containing spaces survive intact (bash 3.2: no mapfile).
    local cmd=() arg
    while IFS= read -r -d '' arg; do cmd+=("$arg"); done < <(
      printf '%s' "$line" | python3 -c 'import json,sys
for a in json.load(sys.stdin)["cmd"]: sys.stdout.write(a+"\0")')
    run_check "$label: $name" "$dir" "${cmd[@]}"
  done 3< <(CHECK_DIR="$dir" proj checks "$project" "$repo" "$MODE")
  rm -rf "$lock"
}

echo "VERIFICATION — mode=$MODE  root=$ROOT"

if [[ -n "$RESOLVED" ]]; then
  echo "targets: $(printf '%s' "$RESOLVED" | grep -v '^$' | awk -F'\t' '{printf "%s/%s ", $1, $2}')"
fi
[[ -n "$WT_SPECS" ]] && echo "worktrees: $(printf '%s' "$WT_SPECS" | grep -v '^$' | awk -F'\t' '{printf "%s ", $3}')"

while IFS='	' read -r p r reldir stack integ; do
  [[ -n "$p" ]] || continue
  verify_dir "$p" "$r" "$ROOT/$reldir" "$p/$r" "$(scratch_id "$r")"
done <<< "$RESOLVED"

while IFS='	' read -r p r dir; do
  [[ -n "$p" ]] || continue
  verify_dir "$p" "$r" "$dir" "$p/$r@$(basename "$dir")" "$(scratch_id "${r}_$(basename "$dir")")"
done <<< "$WT_SPECS"

echo
echo "=============================================================="
echo "VERIFICATION RESULT"
echo "=============================================================="
for p in "${PASSED[@]}";  do printf '  \033[32mPASS\033[0m  %s\n' "$p"; done
for s in "${SKIPPED[@]}"; do printf '  \033[33mSKIP\033[0m  %s\n' "$s"; done
for f in "${FAILED[@]}";  do printf '  \033[31mFAIL\033[0m  %s\n' "$f"; done
echo
printf 'passed=%d failed=%d skipped=%d\n' "${#PASSED[@]}" "${#FAILED[@]}" "${#SKIPPED[@]}"
echo "full log: $LOG"
echo "result summary: $RESULT"

{
  printf 'mode=%s\npassed=%d\nfailed=%d\nskipped=%d\n' "$MODE" "${#PASSED[@]}" "${#FAILED[@]}" "${#SKIPPED[@]}"
  printf 'verdict=%s\n' "$([[ ${#FAILED[@]} -gt 0 ]] && echo FAILED || ([[ ${#PASSED[@]} -eq 0 ]] && echo NO_EVIDENCE || echo PASSED))"
} >> "$RESULT"

if (( ${#FAILED[@]} > 0 )); then
  echo "VERDICT: FAILED — do not report this work as done."
  exit 1
fi
if (( ${#PASSED[@]} == 0 )); then
  echo "VERDICT: NO EVIDENCE — nothing ran; you may not claim verification."
  exit 2
fi
echo "VERDICT: PASSED"
