---
name: worktree-workflow
description: How all new work is done in every project — in an isolated git worktree on a short-lived branch, never in the main checkouts, so the user can keep working undisturbed. Covers worktree lifecycle, the storage-safe creation path, merging into the repo's integration branch without a PR, changelog hand-off, and cleanup. Load this before starting any code change, and before creating or merging a branch.
license: Proprietary
compatibility: git worktree, gh CLI, macOS
---

# Worktree Workflow

**Every new piece of work happens in a worktree.** Every product checkout
(`projects/<project>/<repo>/`) belongs to the user — an agent
never changes branches, stashes, or commits there. The user must be able to keep
working while you build.

## Layout

```
<workspace root>/
  projects/<project>/<repo>/            ← the user's checkouts. Read-only to agents.
  .wt/<project>/<repo>/<slug>/          ← agent workspaces
  .cache/<project>/<repo>/<name>/       ← shared build output (see storage-management)
```

Repos are addressed as `<project>/<repo>` (e.g. `example/app`); `project.sh show <project>`
lists them.

A worktree costs only its source size because build dirs are symlinked into `.cache/`.
A raw `git worktree add` followed by a build costs GBs. **Never call `git worktree add` directly.**

## Lifecycle

```bash
W=.claude/scripts

bash $W/wt.sh start <project>/<repo> <type>/<slug>     # branch off the integration branch, link caches, copy config
bash $W/wt.sh list                           # what's in flight, dirty state, commits ahead
bash $W/wt.sh push  <project>/<repo> <slug>            # rebase on the integration branch, push
bash $W/wt.sh drop  <project>/<repo> <slug>            # remove worktree (refuses if dirty)
```

`start` enforces the invariants automatically: disk pre-flight, LRU prune at the cap of 10,
the repo's **integration branch** as the base (declared per repo in `project.json`; read it
with `project.sh show <project>`), kebab-case
`<type>/<slug>` naming, cache symlinks, and copying the untracked local config each stack
declares as `local_config` (`.env*`, `google-services.json`, `GoogleService-Info.plist`,
`.fvmrc`, …) that the worktree needs to build.

Branch types: `feat` `fix` `refactor` `chore` `hotfix` `release` `docs` `perf` `test`.
Slug is kebab-case, whole branch ≤ 40 chars. See `git-workflow` for full conventions.

## Multi-repo work

A full-stack change needs one worktree **per repo**, all on the **same slug**:

```bash
bash $W/wt.sh start <project>/backend feat/spending-alerts
bash $W/wt.sh start <project>/app     feat/spending-alerts
```

Slots are shared by every project and session (cap 10) — finish or drop before starting more. Each repo gets its own branch and its own changelog entry, and each merges into its own
integration branch independently. Mention the sibling repos in the changelog entry so the
full-stack change is traceable from either side.

## Finishing

1. Commit inside the worktree, following `git-workflow` commit conventions. The subject line
   becomes the changelog entry — write it as user-facing documentation.
2. Verify: `bash $W/verify.sh wt:<project>/<repo>/<slug> --full` → **must exit 0**.
3. Changelog: `bash $W/changelog.sh add <project>/<repo> <slug>` — folds commits into `[Unreleased]`.
   Commit that too.
4. Rebase onto the integration branch: `bash $W/wt.sh push <project>/<repo> <slug>`.
5. Merge it in — fast-forward only — and push the integration branch.
6. Delete the branch (local **and** remote) and drop the worktree:
   `bash $W/wt.sh drop <project>/<repo> <slug>`.

There is **no pull request**. Feature work lands on the integration branch directly. Promoting the
integration branch to `main` is the user's decision and happens separately — see `git-workflow`.

`/wt-finish` runs all of this in order with the right gates.

## Hard rules

- **Never** commit, checkout, rebase, stash, or reset in `projects/<project>/<repo>/` directly.
  Those are the user's working checkouts.
- **Never** branch from the production branch. Always the repo's **integration branch** from
  `project.json` (`origin/<integration>`). Production may sit behind. (`--from` exists for hotfixes off a release tag.)
- **Never** merge into `main`, push to `main`, or open an integration → `main` PR. That promotion
  is the user's alone.
- **Never** `git worktree add` by hand — it skips cache linking and the disk pre-flight.
- **Never** drop a dirty worktree without the user's explicit say-so; `drop` refuses by design.
- **Never** run two full builds at once — worktrees share one build cache.
- **Never** push without an exit-0 verification and the user's confirmation. Pushing is
  outward-facing and hard to reverse.
- **Always** delete the working branch once its work is on the integration branch — local and
  remote. A branch that outlives its merge is the thing this model exists to prevent.

## Binding to run state

```bash
bash $W/state.sh bind worktree .wt/<project>/<repo>/<slug>
bash $W/state.sh bind branch   <type>/<slug>
```

`state.sh show` then prints live `git status` for that worktree on resume — so a fresh session
sees the real tree, not a stale description of it.
