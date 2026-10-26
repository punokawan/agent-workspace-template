---
description: Flutter performance audit for a project's app — widget rebuild waste, list rendering, main-thread heavy work, local-DB query patterns, and memory leaks. Pass a feature or path to scope, or leave empty to audit the whole presentation layer.
argument-hint: [<project>/app] [feature name or path]  e.g. "example/app transaction" or "lib/presentations/screens/wallets" or leave empty
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
4. **Record:** `bash .claude/scripts/state.sh log audit-performance "<n findings, top severity>"`.

---

# Performance Audit

Scope: `$ARGUMENTS`

## Target

`$ARGUMENTS` may start with a `<project>/app` target (e.g. `example/app`). If it does not, use the
active project (marked `*` in `bash .claude/scripts/project.sh list`) and its `flutter` repo from
`bash .claude/scripts/project.sh show <project>`; if it has none, stop and say so. Then read
`projects/<project>/AGENTS.md`, `projects/<project>/app/AGENTS.md` if present, and — only if they
exist — `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and `projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md`.

## What this does

1. Audits `BlocBuilder` rebuild scope — identifies unnecessary full-tree rebuilds
2. Finds missing `const` on static widgets
3. Checks list rendering — `ListView(children:[])` vs builder, missing `itemExtent`
4. Finds heavy synchronous work on the main thread that should use `compute()`
5. Identifies in-memory filtering that should be native local-DB queries
6. Checks for missing `RepaintBoundary` around expensive subtrees (fl_chart)
7. Finds chart data construction inside `build()` methods
8. Audits `dispose()` completeness — unclosed controllers, subscriptions
9. Checks for unclosed local-DB queries

## Agent

Use `.claude/agents/performance-auditor.md`.

Pass:
- The `<project>/app` target and the scope from `$ARGUMENTS`
- Instruction to load `.claude/skills/flutter-performance/SKILL.md` first

## After the audit

If fixable findings exist, ask: `Apply fixes automatically? (yes / no / high-impact only)`

High-impact fixes to apply first: BlocBuilder rebuilds, `compute()` for heavy work, local-DB query replacements.
After fixes: run the repo's analyze command (`fvm flutter analyze` where FVM is used) and hand off to `mobile-reviewer`.
