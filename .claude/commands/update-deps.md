---
description: Safe dependency update session for any project — Flutter SDK, Dart packages, Android/iOS platform layers, Go modules, npm/Next.js packages. Reads current versions first, upgrades one layer at a time, runs analysis and codegen between each layer, and fixes all breakage before continuing.
argument-hint: <project>/<repo> [scope]  e.g. "example/app firebase" or "example/backend go" — empty scope = outdated report
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <project>/<repo> chore/<slug>` first. Never edit `projects/<project>/<repo>/`
   directly — it is the user's working checkout.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log update-deps "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# Dependency Update

Scope: `$ARGUMENTS`

## What this does

1. Resolves the target (`project.sh show <project>`) and reads the actual version files
2. Runs the stack's outdated check (`fvm flutter pub outdated` / `go list -m -u all` / `npm outdated`)
3. Executes upgrades one layer at a time — Flutter SDK → packages → codegen → Android → iOS; Go; npm
4. Runs analyze + codegen + tests between every layer (wrappers from `<project>-dependencies`, if it exists)
5. Fixes every breaking change before moving to the next layer
6. Produces a session report: what changed, what broke, what was fixed, what was deferred

## Agent

Use `.claude/agents/dependency-maintainer.md`.

Pass:
- The target `<project>/<repo>` and worktree path
- The scope from `$ARGUMENTS` (empty = full maintenance pass with report)
- Instruction to load `.claude/skills/dependency-maintenance/SKILL.md` first, then
  `projects/<project>/**/.claude/skills/<project>-dependencies/SKILL.md` only if it exists

## Scope mapping

| `$ARGUMENTS` | What to upgrade |
|---|---|
| empty | Run `pub outdated`, report what's stale, ask which layers to proceed with |
| `all` | Full session: all layers, conservative package upgrade |
| `flutter sdk` | Layer 1 only: FVM install + switch |
| `packages` | Layer 2 only: `fvm flutter pub upgrade` (conservative) |
| `packages major` | Layer 2: `fvm flutter pub upgrade --major-versions` |
| `firebase` | Firebase packages only (all together) |
| `objectbox` | ObjectBox + objectbox_generator + codegen |
| `freezed` | freezed + freezed_annotation + json_serializable + codegen |
| `android` | Layer 4: Kotlin, compileSdk, targetSdk, AGP |
| `ios` | Layer 5: deployment target + pod update |
| `go` | Layer 6: Go toolchain + modules |
| `npm` / `next` | Layer 7: npm packages (patch/minor, then majors one at a time) |

## After the session

Run the overlay's post-update checklist if one exists, then the gate:
```bash
bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full
```
Flutter only: also `fvm flutter build apk --debug` once in the worktree.
