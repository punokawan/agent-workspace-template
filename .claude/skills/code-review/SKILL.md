---
name: code-review
description: How to review code in any studio project — severity taxonomy, consistency contract, finding format, scope, verdict, plus the Flutter/Clean Architecture checklist. Load when reviewing a diff, a landed change, or a newly scaffolded feature. Go and Next.js reviews also use backend-reviewer / frontend-reviewer and their stack skills.
license: Proprietary
compatibility: Any stack; detailed checklist for Flutter/Dart (Clean Architecture + BLoC)
---

# Code Review (studio)

Review is always done by a different agent than the one that wrote the code. The taxonomy, finding
format, and verdict below apply to every stack. The checklist section is Flutter; Go backend and
Next.js web changes are reviewed by `backend-reviewer` and `frontend-reviewer`, which carry their own
stack checklists but report in this format.

## Source of truth

Before reviewing, read, in this order:
1. `projects/<project>/AGENTS.md` — layering rules, vocabulary, known defects
2. `projects/<project>/<repo>/AGENTS.md` if it exists
3. `projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md` and `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` (or the repo's `<project>-backend-patterns` / `<project>-web-patterns`), each only if it exists — their naming, import, and false-positive lists are part of the gate
4. The nearest unchanged file of the same kind, to judge local consistency

## Severity taxonomy

| Level | Label | Meaning | Action |
|---|---|---|---|
| 1 | **Critical** | Wrong behavior, security hole, data loss risk, or layer contract violation | Block. Must fix. |
| 2 | **High** | Architecture violation, testability destroyed, performance cliff | Block. Strong expectation to fix. |
| 3 | **Medium** | Wrong naming, pattern inconsistency, missing guard | Fix before landing; defer only with a reason. |
| 4 | **Low** | Style, readability, minor naming | Fix if touching the area. Don't block. |
| — | **Note** | Observation, suggestion, question | No action required. |

## Every stack: consistency, comments, duplicated actions

- Comments longer than two concise lines per function/class/widget/method/logical block → **Medium**
- Comments that restate code, preserve history, or hide unclear structure → **Low/Medium**
- Duplicate buttons or controls in one section that trigger the same action → **Medium**
- Duplicate destructive or financial actions that can mislead users → **High**
- New helper, widget, rule, route, endpoint, formatter, or constant duplicating an existing owner → **Medium/High**
- Secrets or PII in code, logs, fixtures, or changelog → **Critical** (report location and class, never the value)
- A `/verify` file-size warning (the change grew a file past its stack limit, or added one over it) → **Medium**; name the split the project's File size rule describes. Files already large and untouched are not findings.

## Flutter checklist (priority order)

### 1. Imports (Critical gate)
Read imports before the body. Wrong imports = wrong layer.

| File | Forbidden |
|---|---|
| `domain/**` | `data/`, `presentations/`, DI/wiring module, HTTP client, database package, Firebase, Flutter UI |
| shared primitives (`core/` or equivalent) | feature-specific code |
| `presentations/blocs/` | HTTP client, database package, Firebase, datasources, DTOs |
| `presentations/screens/`, `widgets/` | anything in `data/` |

### 2. Result contract (Critical)
Every repository method returns the project's `Result` and never throws. Check each `async` repo
method for a surrounding `try/catch` that converts to a failure.

### 3. BLoC patterns (High/Critical)
- Missing loading guard where double-submit is possible → **High**
- Missing `try/catch` in an async handler → **Critical** (an unhandled throw kills the stream)
- Service-locator lookup inside a BLoC body → **High** (untestable)
- Direct storage or network access in a BLoC → **Critical**
- One BLoC serving several unrelated operations → **Medium**

### 4. Naming (Medium)
Against `dart-style` and the project overlay: entity without suffix, DTO suffix per project,
`*UseCase` + `*Param`, `<Feature><Operation>Bloc`, verb events, prefixed states.

### 5. Testability (Medium/High)
- BLoC depends on a concrete class it could receive as an abstraction → **High**
- Business rule in a widget `build()` → **Medium**
- Use case with untested branching logic → **Medium**
- Clock, UUID, payment, or network not injectable where tests need determinism → **Medium**

### 6. Dart and UI patterns (Low/Medium)
- Mutable field in an event or state → **Medium**
- Domain entity with `fromJson` → **Medium**; with database annotations → **Critical**
- Hardcoded user-facing string where l10n exists → **Medium**
- Raw color literal where a theme token exists, raw route string → **Low**

## What to ignore

- The DI/wiring module, app root, and `main*.dart` importing across layers — that is their job.
- `part` directives — codegen, not import violations.
- Generated files (`*.g.dart`, `*.freezed.dart`, `objectbox.g.dart`) — skip entirely.
- Project-specific false positives listed in the overlay.

## Finding format

```
[Critical] lib/data/repositories/invoice_repository_impl.dart:34
load() can throw — no try/catch. The Result contract requires every exception to be caught
and returned as a failure.

Fix:
  try {
    final dtos = await _remote.load();
    return Result.success(dtos.map(InvoiceMapper.toEntity).toList());
  } catch (e, s) {
    return Result.failure(Failure.fromException(e, s));
  }
```

Lead with severity and exact `path:line`; state what is happening, the risk, and the fix.
Every finding is evidence grade B (read) or A (executed) — never a guessed line.

## Scope

- Once there is a Critical/High finding, review the whole change set — violations cluster.
- Skip generated files, files the diff did not touch, and test fixture data.
- Always check, even if unchanged: DI registration when new classes were added, and any global
  provider list when new global BLoCs were added.

## Summary

```
Review Summary
--------------
Critical: N
High:     N
Medium:   N
Low:      N
Files reviewed: N

Verdict: BLOCK / APPROVE WITH NOTES / APPROVE
```

- **BLOCK** — any Critical or High.
- **APPROVE WITH NOTES** — Medium/Low only.
- **APPROVE** — clean.
