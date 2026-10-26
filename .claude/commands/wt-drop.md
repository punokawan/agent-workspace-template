---
description: Remove a finished worktree after its work has landed on the repo's integration branch — verifies it is clean and merged first, then deletes the short-lived branch
allowed-tools: Bash, Read, Skill, AskUserQuestion
---

Drop worktree: $ARGUMENTS  (expected `<project>/<repo> <slug>`)

## Procedure

1. Load `worktree-workflow`.
2. **Check for unmerged work before touching anything:**
   ```bash
   WT=.wt/<project>/<repo>/<slug>
   git -C $WT status --short
   base=$(bash -c "source .claude/scripts/lib.sh; base_branch <project> <repo>")
   git -C $WT log --oneline origin/$base..HEAD
   git -C $WT log --oneline HEAD..origin/$base | head -3
   ```
3. Classify and act:
   - **Dirty** → show the changes, ask whether to commit, stash, or discard. Never discard on
     your own initiative.
   - **Clean but has commits not on the integration branch** → the work has not landed. Say so
     and offer `/wt-finish` instead. Do not drop unlanded work without explicit confirmation.
   - **Clean and fully merged** → proceed.
4. ```bash
   bash .claude/scripts/wt.sh drop <project>/<repo> <slug>
   ```
5. Delete the branch — in this model a landed branch must **not** survive. Still confirm, since
   deleting a remote branch is outward-facing:
   ```bash
   git -C projects/<project>/<repo> branch -d <branch>       # -d, not -D
   git -C projects/<project>/<repo> push origin --delete <branch>
   ```
   Only run these on explicit confirmation. Use `-d` so git refuses to delete unmerged work.
   Leaving a landed branch alive is the thing the two-branch model exists to prevent.
6. Close the run if this was its last worktree:
   `bash .claude/scripts/state.sh close`
7. Report reclaimed space (measured) and remaining slots.

## Rules

- The `drop` script refuses dirty worktrees by design. Do not pass `--force` to get past that
  unless the user has explicitly said to discard those specific changes.
- Never use `git branch -D` unless the user explicitly asks to discard unmerged commits.
