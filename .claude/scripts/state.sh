#!/usr/bin/env bash
# Durable run state so any session can resume any task after /clear, a crash, or a day off.
#   state.sh new <slug> "<goal>"      — start a run, becomes CURRENT
#   state.sh current                  — print the current run id (or empty)
#   state.sh use <run-id>             — switch CURRENT
#   state.sh log <event> "<detail>"   — append to progress.jsonl
#   state.sh phase <name> <status>    — set phase status (pending|active|done|blocked)
#   state.sh decide "<decision>" "<why>"
#   state.sh show [run-id]            — full resume briefing
#   state.sh list                     — all runs, newest first
#   state.sh close [run-id]           — mark complete
#   state.sh gc [--force]             — drop closed runs older than 30 days
#
# CURRENT is shared by every session on this machine. When more than one session is running,
# export STUDIO_RUN=<run-id> so this session's writes cannot land in another session's run.

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

CURRENT_PTR="$STATE_DIR/CURRENT"
mkdir -p "$STATE_DIR"

now() { date -u '+%Y-%m-%dT%H:%M:%SZ'; }
run_path() { echo "$STATE_DIR/$1"; }

# Resolution order: an explicit id, then $STUDIO_RUN, then the CURRENT file.
#
# CURRENT is one pointer shared by every session on this machine. Two Claude sessions working at
# once therefore write into each other's runs — observed on 2026-09-20, where one session's `close`
# landed on another's live run and a third session's `landed` event appeared in a fourth's log.
# $STUDIO_RUN is the fix: a session that exports it is bound to its own run and cannot be diverted
# by whatever another session does to CURRENT. Leaving it unset preserves the old behaviour exactly.
resolve() {
  local id="${1:-}"
  [[ -n "$id" ]] || id="${STUDIO_RUN:-}"
  if [[ -z "$id" ]]; then
    id="$(cat "$CURRENT_PTR" 2>/dev/null || true)"
    [[ -n "$id" ]] && warn_shared_pointer "$id"
  fi
  [[ -n "$id" ]] || die "no run id given and no CURRENT run set (state.sh new <slug> \"<goal>\")"
  [[ -d "$(run_path "$id")" ]] || die "no such run: $id"
  echo "$id"
}

# Only once per process, and only when another run has been touched more recently than this one —
# which is the signal that a second session is live. A warning on every call would be noise.
warn_shared_pointer() {
  [[ -n "${_SHARED_PTR_WARNED:-}" ]] && return 0
  _SHARED_PTR_WARNED=1
  local id="$1" newest
  newest="$(ls -t "$STATE_DIR"/*/progress.jsonl 2>/dev/null | head -1)"
  [[ -n "$newest" ]] || return 0
  newest="$(basename "$(dirname "$newest")")"
  [[ "$newest" == "$id" ]] && return 0
  printf '\033[33m!\033[0m resolved %s from the shared CURRENT pointer, but %s was written more recently.\n' \
    "$id" "$newest" >&2
  printf '  another session may be live. bind this one: export STUDIO_RUN=%s\n' "$id" >&2
}

cmd_new() {
  local slug="${1:?slug}" goal="${2:?goal}"
  local id="$(date '+%Y%m%d-%H%M')-${slug}"
  local d; d="$(run_path "$id")"
  [[ -d "$d" ]] && die "run already exists: $id"
  mkdir -p "$d"

  cat > "$d/run.md" <<EOF
# Run: $id

- **Goal:** $goal
- **Started:** $(now)
- **Status:** active
- **Repos:** (not yet determined)
- **Worktree:** (none)
- **Branch:** (none)

## Phases

| # | Phase | Status | Notes |
|---|-------|--------|-------|
| 1 | scope | active | |

## Decisions

_(append-only — never rewrite an earlier decision, add a superseding one)_

## Open questions

_(none yet)_

## Verified facts

_(only claims backed by a file:line read or real command output; everything else is ASSUMPTION)_
EOF

  : > "$d/progress.jsonl"
  echo "$id" > "$CURRENT_PTR"
  printf '{"ts":"%s","event":"run_created","detail":%s}\n' "$(now)" "$(printf '%s' "$goal" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" >> "$d/progress.jsonl"
  ok "run $id created (now CURRENT)"
  printf '  bind this session to it, so a concurrent session cannot divert your writes:\n' >&2
  printf '    export STUDIO_RUN=%s\n' "$id" >&2
  echo "$id"
}

cmd_log() {
  local ev="${1:?event}" detail="${2:-}" id; id="$(resolve "${3:-}")"
  printf '{"ts":"%s","event":%s,"detail":%s}\n' "$(now)" \
    "$(printf '%s' "$ev" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
    "$(printf '%s' "$detail" | python3 -c 'import json,sys;print(json.dumps(sys.stdin.read()))')" \
    >> "$(run_path "$id")/progress.jsonl"
  ok "logged: $ev"
}

cmd_phase() {
  local name="${1:?phase}" status="${2:?status}" id; id="$(resolve "${3:-}")"
  local f; f="$(run_path "$id")/run.md"
  local icon
  case "$status" in
    pending) icon="⬜ pending" ;; active) icon="🔵 active" ;;
    done)    icon="✅ done"    ;; blocked) icon="🔴 blocked" ;;
    *) die "status must be pending|active|done|blocked" ;;
  esac
  if grep -q "^| .* | $name |" "$f"; then
    python3 - "$f" "$name" "$icon" <<'PY'
import re,sys
f,name,icon=sys.argv[1],sys.argv[2],sys.argv[3]
out=[]
for l in open(f):
    c=l.split('|')
    if len(c)>4 and c[2].strip()==name:
        c[3]=f' {icon} '
        l='|'.join(c)
    out.append(l)
open(f,'w').writelines(out)
PY
  else
    local n; n=$(grep -c '^| [0-9]' "$f" || echo 0)
    python3 - "$f" "$((n+1))" "$name" "$icon" <<'PY'
import sys
f,n,name,icon=sys.argv[1:5]
lines=open(f).read().split('\n')
idx=max(i for i,l in enumerate(lines) if l.startswith('| '))
lines.insert(idx+1,f'| {n} | {name} | {icon} | |')
open(f,'w').write('\n'.join(lines))
PY
  fi
  cmd_log "phase:$name" "$status" "$id" >/dev/null
  ok "phase $name -> $status"
}

cmd_decide() {
  local what="${1:?decision}" why="${2:-}" id; id="$(resolve "${3:-}")"
  local f; f="$(run_path "$id")/run.md"
  python3 - "$f" "$(date '+%Y-%m-%d %H:%M')" "$what" "$why" <<'PY'
import sys
f,ts,what,why=sys.argv[1:5]
t=open(f).read()
entry=f"\n- **{ts}** — {what}\n  - **Why:** {why}\n" if why else f"\n- **{ts}** — {what}\n"
t=t.replace("_(append-only — never rewrite an earlier decision, add a superseding one)_",
            "_(append-only — never rewrite an earlier decision, add a superseding one)_\n"+entry,1)
open(f,'w').write(t)
PY
  cmd_log "decision" "$what" "$id" >/dev/null
  ok "recorded decision"
}

cmd_bind() {  # bind a worktree/branch/repos to a run
  local key="${1:?key: repos|worktree|branch}" val="${2:?value}" id; id="$(resolve "${3:-}")"
  local f label; f="$(run_path "$id")/run.md"
  case "$key" in
    repos) label="Repos" ;; worktree) label="Worktree" ;; branch) label="Branch" ;;
    *) die "key must be repos|worktree|branch" ;;
  esac
  python3 - "$f" "$label" "$val" <<'PYB'
import sys
f,label,val=sys.argv[1:4]
out=[]
for l in open(f):
    if l.startswith(f"- **{label}:**"):
        l=f"- **{label}:** {val}\n"
    out.append(l)
open(f,'w').writelines(out)
PYB
  cmd_log "bind:$key" "$val" "$id" >/dev/null
  ok "$label = $val"
}

cmd_show() {
  local id; id="$(resolve "${1:-}")"
  local d; d="$(run_path "$id")"
  echo "=============================================================="
  echo "RESUME BRIEFING — $id"
  echo "=============================================================="
  cat "$d/run.md"
  echo
  echo "--- Last 25 events -------------------------------------------"
  tail -25 "$d/progress.jsonl" 2>/dev/null | python3 "$(dirname "${BASH_SOURCE[0]}")/_fmt_events.py"
  [[ -f "$d/handoff.md" ]]      && { echo; echo "--- Pending handoff ---"; cat "$d/handoff.md"; }
  if [[ -f "$d/verification.md" ]]; then
    echo; echo "--- Last verification (verdict + summary; full text in the run dir) ---"
    sed -E $'s/\033\\[[0-9;]*m//g' "$d/verification.md" \
      | grep -E '^(  (PASS|FAIL|SKIP)  |passed=|VERDICT|VERIFICATION —)' | head -20
  fi
  echo
  echo "--- Live git state -------------------------------------------"
  local wt; wt=$(grep -m1 '^- \*\*Worktree:\*\*' "$d/run.md" | sed 's/.*\*\* //')
  if [[ -n "$wt" && "$wt" != "(none)" && -d "$wt" ]]; then
    git -C "$wt" status --short 2>&1 | head -20
    echo "  branch: $(git -C "$wt" rev-parse --abbrev-ref HEAD 2>/dev/null)"
  else
    echo "  (no worktree bound to this run)"
  fi
}

cmd_list() {
  printf '%-34s %-10s %s\n' "RUN ID" "STATUS" "GOAL"
  local cur; cur="$(cat "$CURRENT_PTR" 2>/dev/null || true)"
  for d in $(ls -1t "$STATE_DIR" 2>/dev/null); do
    [[ -d "$STATE_DIR/$d" ]] || continue
    local st goal mark
    st=$(grep -m1 '^- \*\*Status:\*\*' "$STATE_DIR/$d/run.md" 2>/dev/null | sed 's/.*\*\* //')
    goal=$(grep -m1 '^- \*\*Goal:\*\*' "$STATE_DIR/$d/run.md" 2>/dev/null | sed 's/.*\*\* //' | cut -c1-58)
    mark=""; [[ "$d" == "$cur" ]] && mark=" ←CURRENT"
    printf '%-34s %-10s %s%s\n' "$d" "${st:-?}" "$goal" "$mark"
  done
}

cmd_use()   { local id; id="$(resolve "$1")"; echo "$id" > "$CURRENT_PTR"; ok "CURRENT = $id"; }
cmd_current(){ cat "$CURRENT_PTR" 2>/dev/null || true; }

cmd_close() {
  # Closing the wrong run is the one mistake here that destroys someone else's work rather than
  # just cluttering it, so an implicit close is refused whenever a second session looks live.
  # Naming the run is always allowed; so is binding this session with $STUDIO_RUN.
  if [[ -z "${1:-}" && -z "${STUDIO_RUN:-}" ]]; then
    local ptr newest
    ptr="$(cat "$CURRENT_PTR" 2>/dev/null || true)"
    newest="$(ls -t "$STATE_DIR"/*/progress.jsonl 2>/dev/null | head -1)"
    [[ -n "$newest" ]] && newest="$(basename "$(dirname "$newest")")"
    if [[ -n "$ptr" && -n "$newest" && "$ptr" != "$newest" ]]; then
      die "refusing to close $ptr from the shared CURRENT pointer — $newest was written more
     recently, so another session is probably live and CURRENT may not be yours.
     name it explicitly:  state.sh close $ptr
     or bind this session: export STUDIO_RUN=$ptr"
    fi
  fi
  local id; id="$(resolve "${1:-}")"
  sed -i.bak 's/^- \*\*Status:\*\* active/- **Status:** complete/' "$(run_path "$id")/run.md" \
    && rm -f "$(run_path "$id")/run.md.bak"   # -i.bak: the one form GNU and BSD sed both accept
  cmd_log "run_closed" "" "$id" >/dev/null
  [[ "$(cmd_current)" == "$id" ]] && : > "$CURRENT_PTR"
  ok "run $id closed — $(grep -m1 '^- \*\*Goal:\*\*' "$(run_path "$id")/run.md" | sed 's/^- \*\*Goal:\*\* //')"
}

cmd_gc() {
  local force="${1:-}" n=0
  while IFS= read -r d; do
    grep -q '^- \*\*Status:\*\* complete' "$d/run.md" 2>/dev/null || continue
    [[ -n "$(find "$d" -maxdepth 0 -mtime +30 2>/dev/null)" ]] || continue
    n=$((n+1)); echo "  $(basename "$d")"
    [[ "$force" == "--force" ]] && rm -rf "$d"
  done < <(find "$STATE_DIR" -mindepth 1 -maxdepth 1 -type d 2>/dev/null)
  (( n == 0 )) && { ok "nothing to gc"; return; }
  [[ "$force" == "--force" ]] && ok "removed $n closed runs" || warn "$n closed runs >30d (re-run with --force)"
}

case "${1:-show}" in
  new) shift; cmd_new "$@" ;;      log) shift; cmd_log "$@" ;;
  phase) shift; cmd_phase "$@" ;;  decide) shift; cmd_decide "$@" ;;
  bind) shift; cmd_bind "$@" ;;
  show) shift; cmd_show "${1:-}" ;; list) cmd_list ;;
  use) shift; cmd_use "$@" ;;      current) cmd_current ;;
  close) shift; cmd_close "${1:-}" ;; gc) shift; cmd_gc "${1:-}" ;;
  *) die "usage: state.sh {new|bind|log|phase|decide|show|list|use|current|close|gc}" ;;
esac
