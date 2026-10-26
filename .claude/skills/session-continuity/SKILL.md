---
name: session-continuity
description: Durable run-state protocol for work in every project — how to create, update, and resume a run so any session can pick up an in-flight task after /clear, a crash, or days away. Load this at the start of any multi-step task and whenever the user says "resume", "continue", or "where were we".
license: Proprietary
compatibility: bash, git
---

# Session Continuity

Context windows end. Sessions crash. Work spans days. **Nothing important may live only in
the conversation.** Every multi-step task writes durable state to disk, and every session
starts by reading it.

## Where state lives

```
.claude/agentic-state/
  CURRENT                          # run id of the active run
  <YYYYMMDD-HHMM>-<slug>/
    run.md                         # goal, phases, decisions, verified facts   ← the briefing
    progress.jsonl                 # append-only event log                     ← the audit trail
    handoff.md                     # what the next agent must do (optional)
    verification.md                # last /verify output                       (optional)
```

Paths are absolute from `.`, so state is reachable from any
worktree, any repo, any session.

## The protocol

### At the start of every multi-step task

```bash
S=.claude/scripts/state.sh
bash $S current          # is a run already in flight?
bash $S list             # what else is open?
```

- If a relevant run exists → `bash $S show <id>` and continue it. **Do not start a duplicate.**
- If not → `bash $S new <slug> "<one-line goal>"`

Then **bind this session to that run** before writing anything else:

```bash
export STUDIO_RUN=<run-id>
```

`CURRENT` is a single file shared by every Claude session on this machine, so two sessions running
at once will write into each other's runs — on 2026-09-20 one session's `close` landed on another
session's live run, and a third session's `landed` event appeared in a fourth's log. `$STUDIO_RUN`
takes precedence over `CURRENT`, so an exported session cannot be diverted by whatever anyone else
does to the pointer. Unset, everything behaves as it always did.

Two guards back this up: an implicit resolve prints a warning when a different run was written more
recently, and an implicit `close` is **refused** in that situation — name the run
(`bash $S close <id>`) or export `STUDIO_RUN`.

### While working — write state at these five moments, not at the end

| Moment | Command |
|---|---|
| Phase starts / finishes | `bash $S phase <name> active\|done\|blocked` |
| A choice is made that a future session could not re-derive | `bash $S decide "<what>" "<why>"` |
| A verification runs | `bash $S log verify "<real command output summary>"` |
| A branch/worktree is created | `bash $S bind worktree <path>` / `bind branch <name>` |
| Anything is blocked | `bash $S phase <name> blocked` + `bash $S log blocked "<reason>"` |

Rule of thumb: **if losing this fact would make a fresh session redo work or guess, write it.**

### At the end

```bash
bash $S close
```

## Resuming

`bash $S show` prints a full briefing: goal, phase table, decisions with rationale, the last
25 events, any pending handoff, the last verification, and **live `git status` for the bound
worktree**. That last part matters — `run.md` records intent, git records reality. If they
disagree, **git is the truth**; reconcile `run.md` to match before continuing.

## Writing rules

- **`run.md` is a briefing, not a diary.** Keep it under ~100 lines. Long narratives go to
  `progress.jsonl`.
- **Decisions are append-only.** Never edit an old decision. If it changes, add a new one
  saying "supersedes <date> decision: …".
- **The "Verified facts" section takes only grounded claims** — a `file:line` you actually
  read, or output from a command you actually ran. Everything else belongs under "Open
  questions" or is labelled `ASSUMPTION`. See the `verification` skill.
- Never store secrets, tokens, or customer PII in run state. It is plaintext on disk.

## Housekeeping

`bash $S gc --force` drops closed runs older than 30 days. Run state is KB-sized; it is not a
disk concern, but stale open runs cause duplicate work — close runs when done.
