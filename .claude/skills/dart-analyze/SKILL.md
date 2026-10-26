---
name: dart-analyze
description: How to run and interpret dart/flutter analyze in any studio Flutter app — FVM, reading output, severity, fix workflow, when to run, and suppression rules. Each project's configured lint set lives in its analysis_options.yaml and app overlay.
license: Proprietary
compatibility: Flutter/Dart with flutter_lints, FVM
---

# Dart Analyze (studio)

## Source of truth

Read `projects/<project>/AGENTS.md`, `projects/<project>/<repo>/AGENTS.md` if it exists, the repo's
`analysis_options.yaml`, and `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and
`projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md` if they exist. The configured rules are whatever
`analysis_options.yaml` says — never assume another project's list. (For example:
`example-app-patterns/references/style-and-lint.md` tabulates its rule set.)

## Running

Every studio Flutter app pins its SDK with FVM (`.fvmrc`). Always:

```bash
fvm flutter analyze
```

Never bare `flutter analyze` — it bypasses the pinned version. The workspace gate runs analyze as
part of `bash .claude/scripts/verify.sh <project>/<repo>` (or `wt:<project>/<repo>/<slug>`); that
exit code is the evidence, not a local run alone.

## Lint baseline

All four apps include `package:flutter_lints/flutter.yaml` and add project overrides. Generated
files (`**/*.g.dart`, `**/*.freezed.dart`, `objectbox.g.dart`) and `build/**` are normally excluded.
Check `analysis_options.yaml` for `errors:` promotions — a rule promoted to `error` fails the gate.

## Reading output

```
  warning • Unnecessary lambda • lib/presentations/blocs/invoice/invoice_list_bloc.dart:22:18 • unnecessary_lambdas
  error   • Don't invoke 'print' in production code • lib/core/logging/log.dart:12:3 • avoid_print
```

Format: `severity • message • file:line:col • rule_id`.

- **error** — must fix; fails the gate and review.
- **warning** — fix; flagged Medium in review.
- **info** — fix when touching the file; fatal if the gate runs `--fatal-infos`.

Target: `No issues found!`

## Fix workflow

1. Capture: `fvm flutter analyze 2>&1 | tee <scratchpad>/analyze.txt`.
2. Errors first, then warnings by frequency.
3. Common fixes:
   - `avoid_relative_lib_imports` — use `package:<app>/...` imports.
   - `avoid_print` — route through the project logger.
   - `unnecessary_lambdas` — tear-offs: `dtos.map(InvoiceMapper.toEntity)`.
   - `cancel_subscriptions` — cancel in `dispose()` / BLoC `close()`.
   - `prefer_const_constructors` — add `const` (also a rebuild win).
4. Re-run until clean.

## When to run

| Moment | Command |
|---|---|
| Before committing | `fvm flutter analyze` |
| After scaffolding a feature | `fvm flutter analyze lib/<feature path>/` |
| After a refactor | `fvm flutter analyze` |
| In review (`mobile-reviewer`) | run it and report findings |
| Gate | `bash .claude/scripts/verify.sh <project>/<repo>` |

## Analyze vs test vs review

| Tool | Catches |
|---|---|
| `fvm flutter analyze` | type errors, lint violations, import issues |
| `fvm flutter test` | runtime behavior, BLoC states, mapper correctness |
| `mobile-reviewer` | architecture, SOLID, pattern drift — what analyze cannot see |

A file can pass analyze and still hold a Critical layer violation. Run all three.

## Suppressing a rule (rare)

Only when the rule fires on generated or framework code you cannot change:

```dart
// ignore: avoid_print
// ignore_for_file: invalid_annotation_target   // generated or freezed-annotated files only
```

Never suppress `avoid_print` in production code or any layer-boundary rule. Every suppression gets a
one-line reason.
