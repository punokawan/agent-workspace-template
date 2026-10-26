---
description: Report disk usage across the whole studio workspace — reclaimable artifacts, shared cache, worktree slots, and a free-space verdict
allowed-tools: Bash(bash .claude/scripts/storage.sh:*), Read, Skill
model: haiku
---

Load the `storage-management` skill, then run:

```bash
bash .claude/scripts/storage.sh report
bash .claude/scripts/storage.sh doctor
```

Report the **actual script output**. Then state, in at most 4 lines:

1. The free-space verdict (HEALTHY / TIGHT / CRITICAL) and the measured free bytes.
2. Whether new work can start now, or whether a prune is required first.
3. Worktree slots used vs. cap.
4. Any worktree flagged by `doctor` as holding real (unlinked) build artifacts.

Do not estimate or extrapolate sizes — quote only numbers the script printed. If the script
fails, report the failure verbatim and stop.
