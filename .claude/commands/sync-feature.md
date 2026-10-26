---
description: Add remote sync capability (upsert + delete BLoCs) to an existing local-only feature in a project's offline-first Flutter app, following that app's existing remote BLoC pattern.
argument-hint: <feature>  e.g. "tag"
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <repo> <type>/<slug>` first. Never edit a checkout under
   `projects/<project>/<repo>/` directly — those are the user's working checkouts.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log sync-feature "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# Sync Feature

You are adding remote sync BLoCs to an existing feature that currently only persists locally. This
applies only to apps with an offline-first sync layer — if the target app has none, stop and say so.

## Input
Feature: `$ARGUMENTS` (target `<project>/<repo>`, the Flutter repo)

---

## Step 1 — Read the pattern

Read `projects/<project>/AGENTS.md`, `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` if it exists,
and `projects/<project>/**/.claude/skills/<project>-planning/references/scaffold-and-sync.md` if it exists — it names the
reference BLoCs, file paths, use cases, provider and DI lines for that app. Then read one existing
feature's upsert-remote and delete-remote BLoCs end to end.

## Step 2 — Validate the feature exists

Confirm the feature's domain entity and local repository interface exist. If not, stop and tell the
user to run `/new-feature` first.

## Step 3 — Remote repository and datasource

If the feature has no remote repository interface, implementation, and remote datasource, list what
will be created (mirroring the reference feature) and ask to confirm.

## Step 4 — Generate

Delegate to `senior-mobile-engineer` in the worktree: upsert-remote and delete-remote BLoCs (loading
guard, try/catch, result handling as in the reference), their use cases, provider registration, DI
registration, and the listener in the screen that fires remote sync after a local success.

## Step 5 — Verify and review

`bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`, then `/arch-review` on the new files.
