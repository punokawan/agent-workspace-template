#!/usr/bin/env bash
# Consistency audit for the whole studio AI toolkit + the docs agents rely on.
# Catches the drift that turns into hallucination: stale rosters, dead paths,
# renamed agents, broken scripts, docs that describe code that no longer exists.
#
#   audit.sh            — run every check, exit 1 if any fail
#   audit.sh --quiet    — only report failures

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
set +e +u

QUIET=""; [[ "${1:-}" == "--quiet" ]] && QUIET=1
FAIL=0
pass() { [[ -n "$QUIET" ]] || printf '  \033[32mPASS\033[0m  %s\n' "$1"; }
fail() { printf '  \033[31mFAIL\033[0m  %s\n' "$1"; FAIL=1; }
note() { [[ -n "$QUIET" ]] || printf '        %s\n' "$1"; }

echo "STUDIO TOOLKIT AUDIT — $(date '+%Y-%m-%d %H:%M')"
echo "==========================================================="

# 1 — roster freshness
if bash "$ROOT/.claude/scripts/roster.sh" --check >/dev/null 2>&1; then
  pass "AGENTS.md roster is current"
else
  fail "AGENTS.md is stale — run: bash .claude/scripts/roster.sh"
fi

# 2 — every script parses
n=0; bad=0
for s in "$ROOT/.claude/scripts"/*.sh; do
  n=$((n+1)); bash -n "$s" 2>/dev/null || { fail "syntax error: ${s#$ROOT/}"; bad=1; }
done
(( bad == 0 )) && pass "$n scripts parse"

# 3 — frontmatter on every agent / skill / command
bad=0; n=0
for f in "$ROOT/.claude/agents"/*.md "$ROOT/.claude/skills"/*/SKILL.md; do
  n=$((n+1))
  grep -q '^name:' "$f" && grep -q '^description:' "$f" || { fail "missing name/description: ${f#$ROOT/}"; bad=1; }
  [[ "$(basename "$f")" == "SKILL.md" ]] && continue
  grep -qE '^model: *(opus|sonnet|haiku)$' "$f" && grep -qE '^effort: *(low|medium|high|xhigh|max)$' "$f" \
    || { fail "agent missing model/effort tier: ${f#$ROOT/}"; bad=1; }
  fm="$(sed -n 's/^name: *//p' "$f" | head -1)"
  [[ "$fm" == "$(basename "$f" .md)" ]] || { fail "name/filename mismatch: ${f#$ROOT/} (name: $fm)"; bad=1; }
done
for f in "$ROOT/.claude/commands"/*.md; do
  n=$((n+1)); grep -q '^description:' "$f" || { fail "missing description: ${f#$ROOT/}"; bad=1; }
done
(( bad == 0 )) && pass "$n agent/skill/command files have valid frontmatter"

# 4 — no references to agents that no longer exist
bad=0
for a in $(grep -rhoE '\b(senior|mobile|backend|frontend)-[a-z-]+\b' "$ROOT/.claude" "$ROOT/AGENTS.md" 2>/dev/null | sort -u); do
  [[ -f "$ROOT/.claude/agents/$a.md" ]] && continue
  case "$a" in senior-*|mobile-reviewer|backend-reviewer|frontend-reviewer|mobile-test-engineer|frontend-test-engineer)
    fail "reference to nonexistent agent: $a"; bad=1 ;;
  esac
done
(( bad == 0 )) && pass "no dangling agent references"

# 5 — every script path referenced actually exists
bad=0
for p in $(grep -rhoIE '\.claude/scripts/[a-z_]+\.(sh|py)' "$ROOT/.claude" "$ROOT/AGENTS.md" 2>/dev/null | sort -u); do
  [[ -f "$ROOT/$p" ]] || { fail "referenced script missing: $p"; bad=1; }
done
(( bad == 0 )) && pass "all referenced scripts exist"

# 6 — every skill a guide, command, agent or skill names ("the `x` skill") exists
bad=0
for s in $(grep -rhoE '`[a-z][a-z0-9-]+` skill' "$ROOT/.claude" "$ROOT/AGENTS.md" "$ROOT/templates" 2>/dev/null \
             | sed -E 's/`([^`]+)` skill/\1/' | sort -u); do
  [[ -d "$ROOT/.claude/skills/$s" ]] && continue
  compgen -G "$PROJECTS_DIR/*/.claude/skills/$s" >/dev/null && continue
  compgen -G "$PROJECTS_DIR/*/*/.claude/skills/$s" >/dev/null && continue
  fail "a skill is named but does not exist: $s"; bad=1
done
(( bad == 0 )) && pass "every named skill exists"

# 7 — paths claimed in each project's AGENTS.md exist
bad=0
while IFS='\t' read -r pj rp reldir stack integ; do
  [[ -n "$pj" ]] || continue
  doc="$PROJECTS_DIR/$pj/AGENTS.md"; [[ -f "$doc" ]] || continue
  # Only audit each project's AGENTS.md once, on its first repo row.
  [[ "$pj" == "${last_pj:-}" ]] && continue
  last_pj="$pj"
  while IFS= read -r p; do
    [[ -z "$p" ]] && continue
    # skip placeholders, globs, URLs, and Go/npm module paths
    case "$p" in
      *"<"*|*"*"*|http*|*.com/*|*.org/*|*.dev/*|@*) continue ;;
    esac
    # skip deliberate counter-examples ("never do X", "would break", ❌)
    if grep -F -- "$p" "$doc" | grep -qiE 'never|do not|don.t|instead of|would break|❌|wrong|anti-pattern'; then
      continue
    fi
    hit=0
    # direct under the project, then under each of its repos and their source roots
    [[ -e "$PROJECTS_DIR/$pj/$p" || -e "$ROOT/$p" ]] && hit=1
    if (( ! hit )); then
      while IFS='\t' read -r _ r2 rel2 _ _; do
        [[ -n "$r2" ]] || continue
        [[ -e "$ROOT/$rel2/$p" ]] && { hit=1; break; }
        while IFS= read -r sr; do
          [[ -n "$sr" ]] || continue
          [[ -e "$ROOT/$rel2/$sr/$p" ]] && { hit=1; break 2; }
        done < <(proj field "$pj" "$r2" source_roots)
      done < <(proj resolve "$pj")
    fi
    (( hit )) && continue
    find "$PROJECTS_DIR/$pj" -path "*/$p" -not -path '*/node_modules/*' -print -quit 2>/dev/null | grep -q . && continue
    fail "$pj/AGENTS.md claims a path that does not exist: $p"; bad=1
  done < <(grep -oE '`[A-Za-z0-9_.-]+/[A-Za-z0-9_./-]+`' "$doc" | tr -d '`' | sort -u)
done < <(proj resolve all)
(( bad == 0 )) && pass "all paths claimed in project AGENTS.md files exist"

# 8 — no secrets committed into the toolkit
bad=0
if grep -rlEi '(api[_-]?token|secret|password|private[_-]key)[\"'"'"']?\s*[:=]\s*[\"'"'"'][A-Za-z0-9/_+=-]{16,}' \
     "$ROOT/.claude" 2>/dev/null | grep -q .; then
  fail "possible hardcoded credential under .claude/ — inspect and rotate"; bad=1
fi
(( bad == 0 )) && pass "no hardcoded credentials under .claude/"

# 9 — worktrees are cache-linked and disk is within budget
# NOTE: capture first. `... | grep -q` makes grep exit on the first match, which
# SIGPIPEs storage.sh; with pipefail (set by lib.sh) that reads as a failed pipeline
# even though the check passed. Never pipe a long producer into `grep -q` here.
storage_out="$(bash "$SCRIPTS/storage.sh" doctor 2>&1)"
if grep -q '✓' <<<"$storage_out" && ! grep -q '^!' <<<"$storage_out"; then
  pass "worktrees share caches; disk within budget"
else
  fail "storage doctor reported a problem — run: /disk-report"
  printf '%s\n' "$storage_out" | sed -n '3,8p' | sed 's/^/        /'
fi

# 9b — no landed worktree left behind (clean, fully on its integration branch, idle)
sweep_out="$(bash "$SCRIPTS/wt.sh" sweep 2>&1 || true)"
landed="$(grep -c '^  retire ' <<<"$sweep_out" || true)"
if (( landed > 0 )); then
  fail "$landed landed worktree(s) still on disk — retire them: wt.sh sweep --apply"
  grep '^  retire ' <<<"$sweep_out" | sed 's/^  retire /        /'
else
  pass "no landed worktrees left on disk"
fi

# 10 — stale open runs
open=$(grep -l '^- \*\*Status:\*\* active' "$STATE_DIR"/*/run.md 2>/dev/null | wc -l | tr -d ' ')
if (( open > 3 )); then
  fail "$open runs still marked active — close finished ones (state.sh close) to avoid duplicate work"
else
  pass "$open active run(s)"
fi

# 11 — planning index freshness
if bash "$ROOT/.claude/scripts/plan.sh" index --check >/dev/null 2>&1; then
  pass "planning INDEX.md is current"
else
  fail "planning/INDEX.md is stale — run: bash .claude/scripts/plan.sh index"
fi

# 12 — planning status drift (a plan marked unbuilt whose code actually exists)
if bash "$ROOT/.claude/scripts/plan.sh" audit >/dev/null 2>&1; then
  pass "plan statuses match the codebase"
else
  fail "planning status drift — run: bash .claude/scripts/plan.sh audit"
fi

# 13 — docs cite code paths that actually exist
if python3 "$ROOT/.claude/scripts/_docs.py" --quiet >/dev/null 2>&1; then
  pass "docs cite only real code paths"
else
  fail "docs cite dead code paths — run: python3 .claude/scripts/_docs.py"
fi

# 14 — every project manifest resolves against what is on disk
if bash "$SCRIPTS/project.sh" check >/dev/null 2>&1; then
  pass "project manifests match the checkouts on disk ($(proj list | wc -l | tr -d ' ') project(s))"
else
  fail "project manifest drift — run: bash .claude/scripts/project.sh check"
fi

# 15 — one guide per directory, and Codex sees the same skills as Claude
bad=0
for d in "$ROOT" "$PROJECTS_DIR"/*/ "$PROJECTS_DIR"/*/*/; do
  d="${d%/}"; rel="${d#"$ROOT"/}"
  if [[ -f "$d/AGENTS.md" && -f "$d/CLAUDE.md" ]] && ! grep -qx '@AGENTS.md' "$d/CLAUDE.md"; then
    fail "$rel/CLAUDE.md does not import AGENTS.md"; bad=1
  fi
  if [[ -d "$d/.claude/skills" && ! -L "$d/.agents/skills" ]]; then
    fail "$rel/.agents/skills must be a link to ../.claude/skills, so skills live in one place"; bad=1
  fi
done
(( bad == 0 )) && pass "CLAUDE.md files import AGENTS.md; skills are linked for Codex"

# 17 — each guide's rules block matches templates/rules and the project's profile
if bash "$SCRIPTS/rules.sh" check >/dev/null 2>&1; then
  pass "rules blocks match each project's profile"
else
  fail "rules blocks are stale — run: bash .claude/scripts/rules.sh sync"
fi

# 18 — Codex stops reading guides at 32 KiB: root + project + the largest repo guide must fit
over=0
for pj in "$PROJECTS_DIR"/*/; do
  [[ -f "$pj/AGENTS.md" ]] || continue
  big=0; for g in "$pj"*/AGENTS.md; do [[ -f "$g" ]] && (( $(wc -c < "$g") > big )) && big=$(wc -c < "$g"); done
  total=$(( $(wc -c < "$ROOT/AGENTS.md") + $(wc -c < "$pj/AGENTS.md") + big ))
  (( total > 32768 )) && { fail "${pj#"$ROOT"/} guides total $total bytes — over Codex's 32 KiB; trim the project or repo guide, or use a lighter profile"; over=1; }
done
(( over == 0 )) && pass "every project's guides fit Codex's 32 KiB"

# 19 — the toolkit's own tests (rules rendering) pass
if python3 -m unittest discover -s "$SCRIPTS/tests" >/dev/null 2>&1; then
  pass "toolkit tests pass"
else
  fail "toolkit tests fail — run: python3 -m unittest discover -s .claude/scripts/tests"
fi

# 16 — facts a project declares as identical across its repos really are
if python3 "$ROOT/.claude/scripts/_parity.py" --quiet >/dev/null 2>&1; then
  pass "cross-repo parity groups agree"
else
  fail "cross-repo parity drift — run: python3 .claude/scripts/_parity.py"
fi

echo
if (( FAIL )); then echo "VERDICT: DRIFT DETECTED"; exit 1; fi
echo "VERDICT: CONSISTENT"
