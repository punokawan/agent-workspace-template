---
description: Check that this machine (macOS, Linux, or Windows via WSL2 or Git Bash) has what the workspace needs — bash, git, python3, working symlinks, and each project's toolchain — and print the fix for anything missing.
allowed-tools: Bash(bash .claude/scripts/env.sh:*)
---

Run and show the real output:

```bash
bash .claude/scripts/env.sh
```

Report each `MISS` and `WARN` line with its fix exactly as printed. Install nothing yourself:
installing software changes the user's machine, so give the commands and let the user run them.
