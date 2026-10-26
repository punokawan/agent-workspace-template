---
description: Audit a project's Go backend code for layer violations, error handling gaps, missing validations, and convention breaches. Runs the backend-reviewer agent on changed or specified files.
argument-hint: [<project>/<repo>] [path or package]  e.g. "example/backend pkg/service/resource/transaction.go" or "example/backend budget" — leave path empty to check git diff
---

## Harness (applies before anything below)

1. **Read-only.** This command analyses; it does not change code. Report findings — do not fix
   unless the user asks. Silent fixes hide regressions.
2. **Load** `verification`. Every finding is Grade **A** (a command's real output + exit code) or
   Grade **B** (a `path:line` you actually read). Anything else is **C — inferred** (show your
   inputs) or `ASSUMPTION:`. Never invent a file, symbol, line number, or severity.
3. **Ground static findings in a real run** where the toolchain can answer:
   `bash .claude/scripts/verify.sh <project>/<repo> --quick`
   Distinguish what the tool found from what you concluded.
4. **Record:** `bash .claude/scripts/state.sh log api-review "<n findings, top severity>"`.

---

# API Review — Go backend

You are auditing Go code for architecture and convention compliance.

## Input
Scope: `$ARGUMENTS`

---

## Step 1 — Resolve the target and scope

**Target.** Take `<project>/<repo>` from the arguments or the bound run. If missing, run
`bash .claude/scripts/project.sh show <project>` and pick the repo whose stack is `go`; if still
ambiguous, ask. Review a bound worktree (`.wt/<project>/<repo>/<slug>`) when there is one,
otherwise the checkout read-only.

**If the scope is a file path**: audit that file + any directly related files (handler, service, data access for the same domain).

**If the scope is a package or domain name** (e.g., `budget`, `identity`): audit all files for that
domain across every layer the project's layering section names (handler/transport, routes,
service, data access/store, entity/domain, DTOs, migrations). If
`projects/<project>/**/.claude/skills/<project>-backend-patterns/references/review-checklist.md` exists, use its file map.

**If the scope is empty**: run `git -C <repo path> diff --name-only HEAD` to find changed `.go` and migration files. Audit those.
If no git changes, ask: "Which package or file should I review?"

---

## Step 2 — Read the files

Use the Read tool to read each file in scope, plus `projects/<project>/AGENTS.md` and the
`<project>-backend-patterns` overlay if it exists.

---

## Step 3 — Delegate to backend-reviewer agent

Use the `backend-reviewer` agent (`.claude/agents/backend-reviewer.md`).

Pass:
- The target `<project>/<repo>` and the path reviewed
- The list of files in scope
- The scope context

---

## Step 4 — Report

Present the agent's findings verbatim.

For each ❌ CRITICAL violation, show:
- Exact file + line
- The current code
- The corrected code

For each ⚠️ WARNING, show a one-line explanation and fix.

---

## Step 5 — Optional fix

Ask: `Fix critical violations? (yes / no)`

If yes: fixes happen in a worktree only (`/wt-start` if none is bound), one violation at a time,
then `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`.

The project's quick reference of top violations, when it has one, is in its
`<project>-backend-patterns` overlay (`references/review-checklist.md`).
