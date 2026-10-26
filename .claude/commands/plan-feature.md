---
description: Generate a complete engineering implementation plan for a feature with an approved PRD in any project. Produces a layered, ordered implementation plan with every file to create or change. Use before starting implementation to align on approach.
argument-hint: <path-to-prd or feature-name>  e.g. "projects/example/planning/features/labels.md" or "labels"
---

## Harness (applies before anything below)

1. **No worktree needed.** This command writes to `projects/<project>/planning/` or
   `projects/<project>/docs/`, which are not git repositories. Never touch repo source here.
2. **Load** `verification`. Anything asserted about the codebase needs a `path:line`; anything not
   grounded is written `ASSUMPTION:` or `unverified`. Do not describe code you have not read.
3. **Record:** `bash .claude/scripts/state.sh log plan-feature "<file written>"`,
   and `state.sh decide` for any choice a future session could not re-derive.

---

# Plan Feature Implementation

You are creating an engineering implementation plan for a feature that has an approved PRD.

## Input
`$ARGUMENTS`

---

## Step 1 — Find and read the PRD

If `$ARGUMENTS` is a file path: read it; the project is its `projects/<project>/` segment.
If it is a feature name: find it in `projects/<project>/planning/features/` of the active project.
If empty: ask which feature to plan.

Also read `projects/<project>/AGENTS.md`, related plans, and
`projects/<project>/**/.claude/skills/<project>-planning/SKILL.md` with its implementation reference if they exist.

Verify the PRD has a data model, acceptance criteria, and an implementation order (plus any section
the overlay requires). If any are missing, say: "This PRD is missing {sections}. Run `/review-prd`
first to complete it before planning implementation."

---

## Step 2 — Read the codebase for context

Resolve the repos with `bash .claude/scripts/project.sh show <project>`. In each repo the PRD touches,
read the nearest existing feature end to end, plus any files the overlay lists as required context.
This gives the planner the actual current state, not a generalization.

---

## Step 3 — Generate the plan using the implementation-planner agent

Delegate to the `implementation-planner` agent with the project, the PRD, and the context from Step 2.
Ask for a complete phased plan (the overlay's phase list if one exists) listing every file to create or
modify.

---

## Step 4 — Architecture check

Before showing the plan, verify:
- No layer violations in the proposed file locations
- Every path cited as existing actually exists
- Backend endpoints are planned before app or web code that calls them
- Every check the overlay lists (for example sync layers, soft delete, required entity fields)

Flag any violations with ❌.

---

## Step 5 — Show the plan

Present the plan in full: files to create (full paths), files to modify (paths + what changes), DI
registrations, code generation steps. Save it as the PRD's tech doc
(`projects/<project>/planning/features/tech/<name>-tech.md`) if the project uses tech docs.

---

## Step 6 — Offer to start implementation

Ask: `Start implementation now? (yes / start from phase N / no)`

If yes: `/wt-start` per repo, then implement phase by phase with the platform engineers; run
`/arch-review` after the domain and data phases and `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --quick`
after each phase. Do not proceed until the current phase's acceptance criteria are met.

---

## Rules

- The plan must be complete before implementation starts — no "we'll figure it out as we go"
- Every phase must have testable completion criteria
- If the PRD's implementation order conflicts with the layer order, follow the layers and note the discrepancy
