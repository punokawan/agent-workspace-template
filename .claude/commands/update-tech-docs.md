---
description: Update a project's technical reference documentation for a specific feature after code changes. Reads the current implementation and rewrites projects/<project>/docs/<feature>/technical-reference.md.
argument-hint: [<project>] <feature-name>  e.g. "example subscription" | "auth"
---

## Harness (applies before anything below)

1. **No worktree needed.** This command writes to `projects/<project>/planning/` or
   `projects/<project>/docs/`, which are not git repositories. Never touch repo source here.
2. **Load** `verification`. Anything asserted about the codebase needs a `path:line`; anything not
   grounded is written `ASSUMPTION:` or `unverified`. Do not describe code you have not read.
3. **Record:** `bash .claude/scripts/state.sh log update-tech-docs "<file written>"`,
   and `state.sh decide` for any choice a future session could not re-derive.

---

# Update Technical Reference

You are updating the engineering documentation for a specific feature.

## Input

Feature: `$ARGUMENTS` (project = first word if it names a project, else the active project)

---

## Step 1 — Map feature to doc file and code paths

Read `projects/<project>/**/.claude/skills/<project>-docs/SKILL.md` if it exists — its feature table gives the doc file and the
backend and app paths. Without one: the doc is `projects/<project>/docs/<feature>/technical-reference.md`
and the sources are found by grepping each repo from `project.sh show <project>` for the feature's
entity, handlers, and BLoCs. If the doc does not exist, say so and offer `/write-docs new:`.

---

## Step 2 — Read current doc and source files

1. Read the existing doc
2. Read ALL relevant source files for the feature
3. Identify what has changed or is now inaccurate

---

## Step 3 — Update the doc

Rewrite only the sections that are out of date. Keep unchanged sections intact.

Rules for updates:
- **Data Models**: Update field names, types, or descriptions if entities changed
- **API Endpoints**: Add/remove/update endpoints, request/response shapes
- **BLoC Events/States**: Reflect any new events, removed events, renamed states
- **Business Rules**: Add new rules, remove obsolete ones, correct inaccurate statements
- **Flows**: Update step-by-step sequences if the code path changed
- **Accuracy over brevity**: Be specific — include exact field names, type signatures, status strings
- **Never remove sections** unless the feature they describe was deleted from code
- **Add "Last updated" timestamp** at the top of the file

---

## Step 4 — Save and verify

Write the updated doc, then run `python3 .claude/scripts/_docs.py` (every cited code path must exist).

Report a summary of what changed in the doc and what code triggered the change.
