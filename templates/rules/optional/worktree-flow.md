## Worktree flow

- **New work happens in a worktree** on a short-lived branch off the repo's integration
  branch (`/wt-start`, `/wt-finish`, `/wt-drop`). The main checkouts stay untouched.
  Skill: `worktree-workflow`.
- **Two branches per repo**, named in `project.json`: integration and production.
  Promoting to production is the user's call. Skill: `git-workflow`.
- **Check disk before builds and new worktrees** (`/disk-report`). Skill: `storage-management`.
