---
description: Write the current session's progress, decisions, and verification status to durable run state so any future session can resume exactly here
allowed-tools: Bash, Read, Skill
---

Checkpoint the current work. Note: $ARGUMENTS

## Procedure

1. Load the `session-continuity` skill.
2. ```bash
   S=.claude/scripts/state.sh
   bash $S current
   ```
   If there is no CURRENT run, create one from what this session has actually been doing:
   `bash $S new <slug> "<goal>"`.
3. Capture **real** state, not remembered state:
   ```bash
   for r in <every projects/<project>/<repo> the run touched>; do
     echo "== $r"; git -C "$r" status --short | head -20
   done
   ```
   Include any bound worktree.
4. Write the checkpoint:
   - `bash $S phase <name> <status>` for every phase whose status changed this session.
   - `bash $S decide "<what>" "<why>"` for each choice a future session could not re-derive
     from the code. Skip anything already recorded.
   - `bash $S log <event> "<detail>"` for work completed, files touched, and commands run
     with their real results.
   - `bash $S bind worktree|branch|repos <value>` if any changed.
5. If another agent should pick this up, write `handoff.md` in the run directory:
   ```
   ## Handoff → <agent-name>
   **Read first:** <exact file paths>
   **Do:** <precise next action>
   **Done when:** <verifiable condition>
   **Do NOT:** <out of scope>
   ```
6. Confirm with `bash $S show | head -30` and report the run id.

## Rules

- Record only what actually happened. No aspirational entries, no "should be fine".
- Anything unverified goes to "Open questions", never to "Verified facts".
- Never write tokens, credentials, or customer PII into run state.
