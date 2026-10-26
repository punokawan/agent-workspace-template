---
description: Resume an in-flight run in any project — reads durable state, reconciles it against live git, and continues from the exact point the last session stopped
allowed-tools: Bash, Read, Glob, Grep, Skill, AskUserQuestion
---

Resume work. Target run: $ARGUMENTS (empty = the CURRENT run).

## Procedure

1. Load the `session-continuity` skill.
2. Establish what is in flight:
   ```bash
   S=.claude/scripts/state.sh
   bash $S list
   ```
   - If `$ARGUMENTS` names a run → `bash $S use <id>`.
   - If nothing is CURRENT and several runs are open → ask the user which one. Do not guess.
   - If no runs exist at all → say so and ask what to start.
3. Read the full briefing:
   ```bash
   bash $S show
   ```
4. **Reconcile intent against reality.** `run.md` says what was planned; git says what exists.
   For the bound worktree/branch, check the actual tree:
   ```bash
   git -C <worktree> status --short && git -C <worktree> log --oneline -10
   ```
   Where they disagree, **git wins**. Correct `run.md` with `bash $S log reconcile "<what differed>"`
   before doing anything else.
5. Re-verify rather than trusting the record. Run `/verify` for the affected repos — a stale
   "tests passed" from three days ago is not evidence about the tree as it stands now.
6. Report back in this exact shape, then continue working:

   ```
   RESUMING <run-id>
   Goal      : <goal>
   Done      : <completed phases>
   Next      : <the single next action>
   Drift     : <what run.md got wrong vs git, or "none">
   Blockers  : <blockers, or "none">
   ```

## Rules

- Never re-do a phase marked `done` without first checking whether its output still exists on disk.
- Never invent progress that is not in `progress.jsonl` or visible in git.
- If the run is bound to a worktree that no longer exists, say so plainly and ask whether to
  recreate it (`/wt-start`) or close the run.
