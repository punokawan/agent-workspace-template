---
description: Write a complete product PRD for a new feature in any project. Delegates to the product-manager agent for structure, QA agent for acceptance criteria quality, and UX agent for screen and flow requirements. Saves the result to projects/<project>/planning/features/.
argument-hint: <feature-name> [one-line description]  e.g. "spending-alerts When budget overspends, notify user with actionable alert"
---

## Harness (applies before anything below)

1. **No worktree needed.** This command writes to `projects/<project>/planning/` or
   `projects/<project>/docs/`, which are not git repositories. Never touch repo source here.
2. **Load** `verification`. Anything asserted about the codebase needs a `path:line`; anything not
   grounded is written `ASSUMPTION:` or `unverified`. Do not describe code you have not read.
3. **Record:** `bash .claude/scripts/state.sh log write-prd "<file written>"`,
   and `state.sh decide` for any choice a future session could not re-derive.

---

# Write PRD

You are creating a new product requirement document for the target project.

## Input
`$ARGUMENTS`

---

## Step 1 — Parse & clarify

Extract from `$ARGUMENTS`:
- **Project**: `<project>` if given; otherwise the active project (`project.sh list`, `*`). Confirm it.
- **Feature name**: kebab-case (e.g., `spending-alerts`, `member-invites`)
- **Description**: one-line summary of the feature idea

If `$ARGUMENTS` is empty or vague, ask:
> What feature do you want to document? Give me a name and a one-line description of what it does for the user.

Do NOT proceed to Step 2 until you have a project, a feature name, and a clear purpose.

---

## Step 2 — Context check

Load the `planning` skill and `projects/<project>/**/.claude/skills/<project>-planning/SKILL.md` if it exists. Then check
`projects/<project>/planning/`:
1. Does `features/` already have a file for this feature? If yes, ask: "A PRD already exists at `{file}`. Do you want to extend it or write a new one?"
2. Does the feature overlap with any existing PRDs? List related plans it should coordinate with.
3. Does it depend on anything in `improvements/`?

Show the user a summary:
```
Project:   {project}
Feature:   {name}
Overlaps:  {list or "none"}
Depends:   {list or "none"}
File:      projects/{project}/planning/features/{kebab-name}.md
```

Ask: `Proceed?`

---

## Step 3 — Write the PRD using the product-manager agent

Delegate to the `product-manager` agent with:
- The project, feature name, and description
- Any overlap/dependency context from Step 2
- Instruction to follow the project's PRD structure (overlay `references/prd-structure.md` if present, else `planning/templates/prd-template.md`) with valid frontmatter (`status: draft`)
- Instruction to be specific on: non-goals, acceptance criteria, data model, success metrics, and any section the overlay marks mandatory

---

## Step 4 — UX review pass

Delegate to the `ux-designer` agent with the PRD draft and the project. Ask it to review the UX and
screen sections for missing states, missing interaction rules, inconsistency with the project's design
system, and screens underspecified for an engineer. Merge its additions before proceeding.

---

## Step 5 — QA review pass

Delegate to the `qa-reviewer` agent with the merged draft and the project. Ask it to review the
acceptance criteria for untestable wording, missing edge cases (delete safety, limits, math correctness,
concurrency or sync), and missing states. Merge its additions before proceeding.

---

## Step 6 — Save the PRD

Write the final merged PRD to `projects/{project}/planning/features/{kebab-name}.md`. Do not truncate
any section. Then run `bash .claude/scripts/plan.sh index`.

---

## Step 7 — Score the PRD (only if the project has a rubric)

If the project overlay defines a scoring rubric, ask: `Score this PRD now? (yes / no)`.
If yes: run `/score-plan projects/{project}/planning/features/{kebab-name}.md`, then apply any
score-index update the overlay describes. If the project has no rubric, skip this step and say so.

---

## Rules throughout

- Every section of the project's PRD structure is required — do not skip any
- Acceptance criteria must be independently testable — reject any "works correctly" language
- Apply every mandatory rule in the project overlay (e.g. sync or data-model fields)
- Do not add the feature to a roadmap sequence the overlay keeps unless the overlay's conditions are met
