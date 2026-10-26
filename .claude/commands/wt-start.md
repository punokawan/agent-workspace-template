---
description: Start new work in an isolated git worktree on a short-lived branch off the repo's integration branch (from project.json) — leaves the user's checkouts untouched and costs its source size, not GBs of build output
allowed-tools: Bash, Read, Skill, AskUserQuestion
---

Start isolated work: $ARGUMENTS

Expected: `<project>/<repo> <type>/<slug>` — e.g. `example/app feat/spending-alerts`.
Multiple repos may be given for a full-stack change; use the **same slug** for each.

## Procedure

1. Load `worktree-workflow` and `storage-management`.
2. If `$ARGUMENTS` is missing the repo or the branch, infer what you can from the task and
   **confirm with the user** before creating anything. Never guess a branch name into existence.
   Branch type must be one of `feat fix refactor chore hotfix release docs perf test`;
   slug kebab-case; whole branch ≤40 chars.
3. Create it (this runs the disk pre-flight and LRU prune itself):
   ```bash
   W=.claude/scripts
   bash $W/wt.sh start <project>/<repo> <type>/<slug>
   ```
   Repeat per repo for multi-repo work. If it refuses on disk or the cap, **stop** and report —
   do not override the cap.
4. Bind it to run state:
   ```bash
   bash $W/state.sh current || bash $W/state.sh new <slug> "<goal>"
   bash $W/state.sh bind worktree <path>
   bash $W/state.sh bind branch <type>/<slug>
   bash $W/state.sh bind repos "<repos>"
   ```
5. Report:
   ```
   WORKTREE READY
   Path   : <path>
   Branch : <branch> (from <integration branch> @ <short-sha>)
   Size   : <measured>
   Slots  : <n>/<cap>
   Run    : <run-id>
   ```

## Rules

- All work from now on happens **in that path**. Never edit the main checkouts.
- Do not `cd` the session into the worktree — pass the path with `git -C` / absolute paths, so
  the tooling at the workspace root stays reachable.
- If a worktree for this slug already exists, use it; do not create a duplicate.
- The base is the repo's **integration branch** as declared in `project.json`
  (`project.sh show <project>`). `wt.sh` resolves it; never pass `--from origin/<production>`.
- This branch is temporary. It gets merged into the integration branch and deleted the same day.
