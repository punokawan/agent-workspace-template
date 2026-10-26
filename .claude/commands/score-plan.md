---
description: Score a product PRD or engineering improvement with its project's own scoring rubric (named in the <project>-planning overlay). Produces the rubric's scores with full justification, then updates the project's score index if it keeps one.
argument-hint: <path-to-plan>  e.g. "projects/example/planning/features/labels.md"
---

## Harness (applies before anything below)

1. **Read-only.** This command analyses; it does not change code. Report findings — do not fix
   unless the user asks. Silent fixes hide regressions.
2. **Load** `verification`. Every finding is Grade **A** (a command's real output + exit code) or
   Grade **B** (a `path:line` you actually read). Anything else is **C — inferred** (show your
   inputs) or `ASSUMPTION:`. Never invent a file, symbol, line number, or severity.
3. **Ground static findings in a real run** where the toolchain can answer:
   `bash .claude/scripts/verify.sh <project>/<repo> --quick`
   Distinguish what the tool found from what you concluded.
4. **Record:** `bash .claude/scripts/state.sh log score-plan "<n findings, top severity>"`.

---

# Score Plan

You are scoring a product or engineering plan using the target project's scoring rubric.

## Input
`$ARGUMENTS`

---

## Step 1 — Identify the plan and project

If `$ARGUMENTS` is a file path: confirm it exists and read it; the project is its `projects/<project>/` segment.
If it is empty or a feature name: search `projects/<project>/planning/features/` and `.../improvements/`
of the active project. If ambiguous, list matches and ask which one.

---

## Step 2 — Find the rubric

Read `projects/<project>/**/.claude/skills/<project>-planning/SKILL.md` and its scoring reference (for example
`references/scoring.md`), then the rubric file it names — completely. The rubric is the authority.

**No overlay or no rubric → stop.** Tell the user this project has no scoring system; do not invent one.

---

## Step 3 — Score using the plan-scorer agent

Delegate to the `plan-scorer` agent with the project, the plan, the rubric, and the existing scores
for calibration (the overlay names the score index and any legacy calibration file).

---

## Step 4 — Validate the score

Re-check every formula in the rubric against the sub-scores. Flag any score that is suspiciously high
or low without clear justification. Correct math errors before proceeding.

---

## Step 5 — Update the score index

If the overlay keeps a score index, update it exactly as the overlay describes (rank, status, source,
clusters, dated summary). Never create a separate score file.

---

## Step 6 — Report

Show the user:
1. The complete score block
2. The tier and recommended action
3. Where the plan ranks relative to existing plans
4. What would most improve the score (top 2 actions)

---

## Rules

- Do not adjust scores upward for enthusiasm or seniority of the request
- Do not skip dimensions — all sub-scores must be filled and justified
- Do not score a plan you have not fully read
- If the plan has missing sections, note which and how they affect the score
