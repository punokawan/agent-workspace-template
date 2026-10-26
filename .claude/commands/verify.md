---
description: Run real toolchain verification (format, analyze/vet/typecheck, lint, tests) across any project's repos and report the actual exit codes — the mandatory gate before any work is called done
allowed-tools: Bash, Read, Grep, Skill
---

Verify: $ARGUMENTS

`$ARGUMENTS` may name targets (`<project>/<repo>` such as `example/app`,
`wt:<project>/<repo>/<slug>`, or `all`) and a
mode (`--quick`, `--full`). Empty → auto-detect repos with uncommitted changes, `--quick`.

## Procedure

1. Load the `verification` skill.
2. If `--full` is requested, first confirm no other build is running — the build cache is shared:
   ```bash
   pgrep -fl 'flutter build|next build|go test' || echo "clear"
   ```
3. Run it:
   ```bash
   bash .claude/scripts/verify.sh $ARGUMENTS
   ```
4. For every FAIL, determine whether it is **yours** or **pre-existing**:
   ```bash
   git -C <repo> stash list; git -C <repo> diff --name-only
   ```
   A failure in a file absent from your diff is pre-existing. Label it `[PRE-EXISTING]`.
   Grep the full log path the script prints for the complete output — the console shows only
   the last 25 lines per check.
5. Record the result in run state:
   ```bash
   bash .claude/scripts/state.sh log verify "<verdict + counts>"
   ```
   and write the summary to `<run-dir>/verification.md`.

## Report — this exact shape

```
VERIFICATION  <targets> --<mode>
  PASS  <check>
  FAIL  <check> (exit N) — <first real error line>   [YOURS|PRE-EXISTING]
VERDICT: PASSED | FAILED | NO EVIDENCE
```

Then one line: whether the work under review may be called done.

## Rules

- Quote the script's real output. Never paraphrase a failure into something milder.
- Exit 1 → the work is **not** done, regardless of how complete the code looks.
- Exit 2 → say "no evidence"; do not claim verification.
- Do not fix failures unless asked — report them. Fixing silently hides regressions.
