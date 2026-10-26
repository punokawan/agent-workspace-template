---
description: Health check for the whole studio AI toolkit and the docs agents depend on — roster freshness, dangling references, dead paths in AGENTS.md, hardcoded credentials, worktree/disk state, and stale runs
allowed-tools: Bash, Read, Grep, Edit, Skill
---

Audit the toolkit for drift. Scope: $ARGUMENTS (empty = everything).

## Procedure

1. ```bash
   bash .claude/scripts/audit.sh
   ```
2. Report the **real output**. Exit 1 means drift was found.
3. For each FAIL, fix the cause — not the check:

   | Finding | Fix |
   |---|---|
   | Roster stale | `bash .claude/scripts/roster.sh` |
   | name/filename mismatch | Rename the file or the `name:` field so they agree, then update every reference |
   | Dangling agent reference | Point it at the real agent; never leave a name that cannot be dispatched |
   | Dead path in an AGENTS.md | **Verify what the real path is** (`find`/`ls`), then correct the doc. Never delete the line to silence the check |
   | Missing referenced script | Restore the script or correct the reference |
   | Hardcoded credential | Report location and class only. Never echo the value. Say it must be rotated, move it to an env var |
   | Storage doctor problem | `/disk-report`, then `storage.sh link <project> <repo> <slug>` |
   | Too many active runs | `state.sh close <id>` for finished ones |

4. Re-run `audit.sh` and confirm it exits 0.

## Beyond the automated checks

If `$ARGUMENTS` asks for a deep pass, also spot-check what a script cannot:

- **Do the docs match the code's actual conventions?** Sample real files and compare against what
  each `AGENTS.md` claims — naming, layering, patterns. A convention documented backwards is worse
  than one not documented at all, because agents follow it confidently.
  Quote counts as evidence (e.g. "88 of 89 component files are kebab-case").
- **Does `verify.sh` still match CI?** If a workflow runs checks the local gate doesn't, or vice
  versa, that drift will surface as "passed locally, failed in CI".
- **Are memory files still true?** `~/.claude/projects/-Users-agungnb-Code-studio/memory/` —
  verify any file, symbol, or flag they name still exists before trusting them.

## Rules

- Never make a check pass by weakening or deleting it.
- Every correction must be grounded: `find`/`grep` the real answer before rewriting a doc.
- Report what you fixed and what you left, with reasons.
