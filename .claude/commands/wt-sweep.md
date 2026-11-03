---
description: Retire every worktree whose work is already on its integration branch — clean, fully landed, idle — archiving its local-only files first, so disk and slots come back
allowed-tools: Bash, Read, Skill
---

Sweep worktrees: $ARGUMENTS

## Procedure

1. Load `worktree-workflow` (section "Retiring worktrees").
2. Dry run and show the user the list:
   ```bash
   bash .claude/scripts/wt.sh sweep
   ```
   Each worktree is `retire` (clean, fully on the local integration branch, idle) or `keep`
   with the reason (uncommitted changes, commits not landed, recently used, this session's own).
3. Apply — no extra confirmation needed for `retire` rows; they hold nothing git lacks and their
   local-only files are archived to `.cache/wt-archive/`:
   ```bash
   bash .claude/scripts/wt.sh sweep --apply
   ```
4. Report: worktrees retired, archives written, disk freed (`df -h .` before and after), slots
   used, and any `keep` rows that look abandoned (ask the user about those — never force).

## Rules

- Never `--force` a drop to retire a dirty worktree, and never retire one with unlanded commits.
- Remote branch deletion stays outward-facing: print the command the sweep suggests, ask first.
- Run it at the start and end of every session that used worktrees.
