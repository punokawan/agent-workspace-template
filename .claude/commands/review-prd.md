---
description: Run a multi-role review of an existing PRD in any project. Checks product completeness (PM agent), UX quality (UX agent), and acceptance criteria testability (QA agent). Produces a single consolidated review report with prioritized gaps.
argument-hint: <path-to-prd>  e.g. "projects/example/planning/features/labels.md"
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
4. **Record:** `bash .claude/scripts/state.sh log review-prd "<n findings, top severity>"`.

---

# Review PRD

You are running a comprehensive review of an existing product PRD using three specialist agents.

## Input
`$ARGUMENTS`

---

## Step 1 — Read the PRD

If `$ARGUMENTS` is a file path: read it; the project is the `projects/<project>/` segment.
If it is a feature name: find it in `projects/<project>/planning/features/` of the active project.
If empty: ask which PRD to review.

Load `projects/<project>/**/.claude/skills/<project>-planning/SKILL.md` if it exists — its `references/prd-structure.md`
defines the section list and gate the agents check against.

---

## Step 2 — PM review (product-manager agent)

Delegate with the PRD and project. Review for: missing sections, weak non-goals, untestable criteria,
score-affecting gaps, open questions answered in the body but left open in the table.

Output: ❌ MISSING, ⚠️ WEAK, ✅ SOLID findings.

---

## Step 3 — UX review (ux-designer agent)

Delegate with the PRD and project. Review the UX and screen sections for missing loading/empty/error
(and project-specific) states, missing interaction rules, inconsistency with the project's design
system, and underspecified screens.

Output: ❌ MISSING, ⚠️ INCONSISTENT, ✅ SOLID findings.

---

## Step 4 — QA review (qa-reviewer agent)

Delegate with the PRD and project. Review the acceptance criteria for untestable wording (rewrite
inline), missing edge cases (delete safety, limits, math correctness, multi-device or concurrency,
sync if the project syncs), and missing state coverage.

Output: gap summary, rewritten criteria, additions list.

---

## Step 5 — Consolidate and prioritize

Merge all three review outputs into one report:

```
PRD Review: {Feature Name}
File: projects/<project>/planning/features/{filename}.md
Date: {date}

─── BLOCKING ISSUES ─────────────────────────────
Issues that must be resolved before implementation:
  1. {issue — source: PM/UX/QA}
  2. ...

─── QUALITY GAPS ────────────────────────────────
Issues that should be fixed to improve the PRD quality:
  1. {issue — source: PM/UX/QA}
  2. ...

─── ACCEPTANCE CRITERIA REWRITES ────────────────
{original → improved, from QA review}

─── ADDITIONS NEEDED ────────────────────────────
UX sections: {additions from UX review}
Acceptance criteria: {additions from QA review}
Edge cases: {additions}

─── ALREADY SOLID ───────────────────────────────
{things that are well-defined across all three reviews}

─── VERDICT ─────────────────────────────────────
Ready for implementation: Yes / No / Conditional
Blocking issues count: N
Recommended next action: {apply fixes / score it / implement}
```

---

## Step 6 — Offer to apply fixes

Ask: `Apply the blocking fixes to the PRD now? (yes / no)`

If yes:
- Apply ❌ BLOCKING fixes using the Edit tool
- Rewrite untestable acceptance criteria in-place
- Add missing sections where content was specified in the review

Do not apply ⚠️ quality gaps automatically — list them for the user to decide.

---

## Rules

- All three agents must complete their review before consolidating
- Blocking = the PRD would cause implementation errors or data correctness risk if not fixed
- Quality gap = makes the PRD weaker or harder to implement, but not blocking
- Do not rewrite sections without showing the user what changed
