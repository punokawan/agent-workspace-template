---
description: Scaffold a complete Clean Architecture feature in a project's Flutter app — entity, models, mapper, datasource, repository, use cases, BLoCs, and screen. Runs senior-mobile-engineer with the project's own conventions.
argument-hint: <feature_name> [field:Type field:Type ...]  e.g. "tag name:String color:String"
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <repo> <type>/<slug>` first. Never edit a checkout under
   `projects/<project>/<repo>/` directly — those are the user's working checkouts.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log new-feature "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# New Feature

You are scaffolding a new feature in a project's Flutter app. This command generates every layer of
Clean Architecture in the correct order, matching that app's existing features exactly.

## Input
Feature requested: `$ARGUMENTS`

---

## Step 1 — Parse & clarify

Extract from `$ARGUMENTS`:
- **Target**: `<project>/<repo>` — the Flutter repo (`project.sh show <project>`, stack `flutter`)
- **Feature name**: snake_case (e.g., `tag`, `savings_plan`)
- **Fields**: remaining `field:Type` pairs

If the feature name is missing, ask:
> What is the feature name (snake_case)? What fields does the entity need (name:Type)?

If fields are missing, ask for them as `fieldName:DartType`.

Do NOT proceed until you have a target, a feature name, and at least one field.

---

## Step 2 — Read the conventions

Read `projects/<project>/AGENTS.md`, `projects/<project>/<repo>/AGENTS.md` if present,
`projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` if it exists, and
`projects/<project>/**/.claude/skills/<project>-planning/references/scaffold-and-sync.md` if it exists (exact file list, DI
and route snippets, codegen command for that app). Then read one complete existing feature in the app.

---

## Step 3 — Confirm plan

Show the user the files to generate (domain entity, repository interface, use cases; response model,
DB model if the app persists locally, mapper, datasource, repository implementation; BLoCs; screen),
the DI and route registrations needed, and the codegen command. Paths and names must mirror the
existing feature you read.

Ask: `Proceed with generation? (yes / adjust fields first)`

---

## Step 4 — Delegate to senior-mobile-engineer

Pass the target, worktree path, feature name (PascalCase and snake_case), complete field list with Dart
types, the reference feature you read, and the overlay snippets. The agent writes every file completely
inside the worktree — no `// TODO` or `// ...` shortcuts — and registers DI and routes.

---

## Step 5 — Code generation

Run the app's codegen command (from the overlay or the repo `Makefile`/`AGENTS.md`), then
`bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --quick`.

---

## Step 6 — Architecture check

Run `/arch-review` (the `mobile-reviewer` agent) on the new files. Report findings.

---

## Rules throughout
- Imports use the app's own package name (`package:<app_package>/...`), read from `pubspec.yaml`
- No placeholder comments (`// TODO`, `// ...`) in output — complete code only
- Follow the naming conventions of the project's `AGENTS.md` and app overlay exactly
