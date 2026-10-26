---
description: Proactive bug sweep across a project's Flutter app — static analysis, crash risks, data integrity, sync bugs, and resource leaks. Pass a feature name or path to scope the hunt, or leave empty for a full sweep.
argument-hint: [<project>/app] [feature name or path]  e.g. "example/app wallet" or "lib/data/repositories" or leave empty for full sweep
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
4. **Record:** `bash .claude/scripts/state.sh log hunt-bugs "<n findings, top severity>"`.

---

# Bug Hunt

Scope: `$ARGUMENTS`

## Target

`$ARGUMENTS` may start with a `<project>/app` target (e.g. `example/app`). If it does not, use the
active project (marked `*` in `bash .claude/scripts/project.sh list`) and its `flutter` repo from
`bash .claude/scripts/project.sh show <project>`; if it has none, stop and say so. Then read
`projects/<project>/AGENTS.md`, `projects/<project>/app/AGENTS.md` if present, and — only if they
exist — `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and `projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md`.

## What this does

1. Runs the repo's analyze command (`fvm flutter analyze` where FVM is used) and reports all errors and warnings
2. Hunts for bugs the analyzer can't catch: uncaught exceptions, project invariant breaches (e.g. sync flags), null-dereference in mappers, BLoC state machine gaps, DI mismatches, list mutation bugs, stream leaks, wrong DateTime handling
3. Produces a prioritized fix list: CRASH → DATA LOSS → SILENT FAILURE → LEAK → STYLE

## Agent

Use `.claude/agents/bug-hunter.md`.

Pass:
- The `<project>/app` target and the scope from `$ARGUMENTS` (feature name, path, or "full sweep")
- Instruction to start by running the analyzer

## After the hunt

If bugs are found, ask: `Fix automatically? (yes / no / critical only)`
- **yes**: fix all findings using senior-mobile-engineer conventions
- **critical only**: fix CRASH and DATA LOSS findings only
- **no**: report only, user fixes manually

After any fixes, re-run the analyzer to confirm clean.
