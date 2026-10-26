---
description: Show all active worktrees across every project — branch, size, dirty state, commits ahead of the integration branch — plus slot usage and disk verdict
allowed-tools: Bash, Read, Skill
model: haiku
---

```bash
W=.claude/scripts
bash $W/wt.sh list
bash $W/storage.sh doctor
bash $W/state.sh list
```

Report the real output, then in ≤4 lines:
1. Which worktrees have uncommitted work (at risk if pruned).
2. Which are clean and finishable, with their commit count.
3. Slots used vs. cap, and whether a new worktree can be started now.
4. Any worktree `doctor` flagged as holding real (unlinked) build artifacts, and the fix command.

Quote only measured numbers. Do not estimate sizes.
