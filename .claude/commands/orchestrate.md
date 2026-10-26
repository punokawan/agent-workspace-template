---
description: Single entry point for any non-trivial task in any project — triages, routes to the right specialist agents, runs them in parallel where safe, verifies, and synthesizes one answer
allowed-tools: Agent, Bash, Read, Glob, Grep, Edit, Write, Skill, AskUserQuestion, SendMessage, TaskOutput
---

Task: $ARGUMENTS

## Procedure

1. **Load** the `workspace-orchestration` skill. Also load `session-continuity` and `verification`.

2. **Bind state.**
   ```bash
   S=.claude/scripts/state.sh
   bash $S current || bash $S new <slug> "$ARGUMENTS"
   ```
   If a run already covers this task, resume it instead of starting a duplicate.

3. **Pre-flight.** New code work needs disk headroom:
   ```bash
   bash .claude/scripts/storage.sh report | tail -20
   ```
   CRITICAL verdict → prune before dispatching anything.

4. **Scope it yourself first.** Identify the repos and files involved before deciding whether to
   decompose. A quick scoping pass usually settles whether this is 1 task or N. Per the
   `workspace-orchestration` triage table, **default to doing it yourself** — decompose only on the
   listed signals.

5. **Plan the dispatch.** Before spawning anything, state to the user in ≤6 lines:
   ```
   PLAN
   Repos    : <project>/<repo>, …  (+ overlays to load)
   Agents   : <name (tier/effort) — why>  [∥ marks parallel groups]
   Sequence : <group 1> → <group 2> → …
   Gate     : verify.sh <targets> --<mode>
   ```
   If the task is ambiguous enough that two readings give materially different work, ask now.

6. **Dispatch.** Batch every independent agent into **one message with multiple Agent calls**.
   Each brief carries all six required elements from the `workspace-orchestration` skill. Respect the
   never-parallelise list — especially: no two full builds at once (shared cache).

7. **Supervise.** As each returns:
   - Read the real `git diff` — do not relay an agent's self-report as confirmed.
   - `bash $S log agent "<name>: <what it returned>"`
   - Conflicting findings → reconcile explicitly and say how.
   - Off-track agent → stop it rather than letting it finish.

8. **Gate.** Nothing is done until:
   ```bash
   bash .claude/scripts/verify.sh <targets> --full
   ```
   Exit 1 → route the failures back to the owning agent. Exit 2 → no evidence; you may not
   claim completion.

9. **Checkpoint** with `/checkpoint`, then report.

## Report format

```
DONE  <one-line outcome>

Changed   : <repo → files>
Agents    : <who did what>
Verified  : <checks + exit codes>   ← real output only
Open      : <assumptions, unresolved items, or "none">
Next      : <suggested follow-up, e.g. /wt-finish>
```

## Rules

- Never report an agent's claim as verified fact — check the diff and run the gate.
- Never invent progress. If an agent failed or returned nothing useful, say so.
- Never dispatch two agents onto the same file.
- Keep the user's answer synthesized — never paste raw agent transcripts.
