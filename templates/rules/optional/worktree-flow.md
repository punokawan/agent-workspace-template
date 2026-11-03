## Worktree flow

- **New work happens in a worktree** on a short-lived branch off the repo's integration
  branch (`/wt-start`, `/wt-finish`, `/wt-drop`). The main checkouts stay untouched.
  Skill: `worktree-workflow`.
- **Two branches per repo**, named in `project.json`: integration and production.
  Promoting to production is the user's call. Skill: `git-workflow`.
- **A landed worktree does not stay on disk.** `wt.sh land` retires the worktree as soon as the
  fast-forward succeeds: gitignored local files (run ledgers, review diffs, an edited `.env`) are
  archived to `.cache/wt-archive/`, the worktree is removed and its local branch deleted.
  Pass `--keep` only while a follow-up is planned in it, then retire it the same day.
- **Sweep at the start and end of every session** (`/wt-sweep`, `wt.sh sweep [--apply]`): it
  retires every worktree that is clean, fully on its integration branch, and untouched for the
  idle window. It never touches dirty, unlanded or recently used worktrees, nor the remote
  branch (deleting that is outward-facing). `/doctor` fails while a landed worktree is left.
- **Check disk before builds and new worktrees** (`/disk-report`). Skill: `storage-management`.
