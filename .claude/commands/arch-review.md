---
description: Independent code review for a project's Flutter code — layer violations, SOLID principles, testability, and naming. Runs mobile-reviewer on staged/changed files or a specified path.
argument-hint: [<project>/app] [path or feature name]  e.g. "lib/domain/entities/tag" or leave empty to check git diff
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
4. **Record:** `bash .claude/scripts/state.sh log arch-review "<n findings, top severity>"`.

---

# Architecture Review

Scope: `$ARGUMENTS`

## Step 0 — Target

`$ARGUMENTS` may start with a `<project>/app` target (e.g. `example/app`). If it does not, use the
active project (marked `*` in `bash .claude/scripts/project.sh list`) and its `flutter` repo from
`bash .claude/scripts/project.sh show <project>`; if it has none, stop and say so. Then read
`projects/<project>/AGENTS.md`, `projects/<project>/app/AGENTS.md` if present, and — only if they
exist — `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and `projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md`.
Review paths below are examples; use the project's layout.


## Step 1 — Determine scope

**If `$ARGUMENTS` is provided:**
- If it looks like a path (`lib/...`): review all `.dart` files under that path
- If it looks like a feature name (e.g., `tag`, `order`): review every file of that feature across
  domain, data, and presentation. For example:
  - `lib/domain/entities/{feature}/`
  - `lib/domain/repositories/local/{feature}_repository.dart`
  - `lib/domain/usecases/{feature}/`
  - `lib/data/models/response/{feature}/`
  - `lib/data/models/db/{feature}/`
  - `lib/data/mappers/{feature}_mapper.dart`
  - `lib/data/datasources/local/{feature}_local_datasource.dart`
  - `lib/data/repositories/local/{feature}_repository.dart`
  - `lib/presentations/blocs/{feature}/`
  - `lib/presentations/screens/{feature}s/`

**If `$ARGUMENTS` is empty:**
Run `git diff --name-only HEAD` to find changed Dart files. Review those.
If no git changes, ask: "Which feature or path should I review?"

## Step 2 — Load skills and review

Load these skills:
- `.claude/skills/clean-architecture/SKILL.md`
- `.claude/skills/solid-principles/SKILL.md`
- `.claude/skills/code-review/SKILL.md`

Then load selectively based on what files are in scope:
- `.claude/skills/flutter-ui-patterns/SKILL.md` — if screens or widgets are in scope
- `.claude/skills/dart-style/SKILL.md` — if naming is in question
- `.claude/skills/tdd/SKILL.md` — if test files are in scope

## Step 3 — Use mobile-reviewer agent

Use `.claude/agents/mobile-reviewer.md` to perform the review.

Pass: the `<project>/app` target, the list of files, and the scope context (feature name / path / git diff).

## Step 4 — Present findings

Present the review report. For each Critical or High finding, include the exact fix.

After the report, ask: `Fix critical violations automatically? (yes / no)`

If yes: apply fixes with the Edit tool, one file at a time.
