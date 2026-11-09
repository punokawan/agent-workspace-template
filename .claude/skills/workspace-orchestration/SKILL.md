---
name: workspace-orchestration
description: Routing brain for work in every project — decides whether to decompose a task, which specialist agent to dispatch, what runs in parallel vs. sequence, which model tier and effort each gets, and the handoff contract between them. Load this at the start of any non-trivial task and whenever more than one repo or discipline is involved. For the specialist agents in this workspace's .claude/agents only — not Orca workers or savvy-flow.
license: MIT
compatibility: Claude Code Agent tool
---

# Orchestration

The main session is the orchestrator. Specialist agents do the work; you route, supervise, and
reconcile. **Agents cannot spawn agents** — every dispatch comes from the main session.

## Step 1 — Triage. Default to doing it yourself.

Decompose only when the task is genuinely large or parallelizable:

| Decompose | Do it yourself |
|---|---|
| 2+ independent chunks (e.g. backend API + mobile UI + web page) | Single-file edit, one bug fix |
| A chunk generates heavy exploratory noise you won't need again | A direct question or quick lookup |
| Many workers → one synthesizer (audit N modules) | Strictly sequential steps each needing the last's full output |
| A discipline you'd otherwise re-derive conventions for | Anything where writing the brief costs more than the work |

If unsure, do a scoping pass yourself first — listing the files usually reveals whether it's 1
task or N.

## Step 2 — Route

### Platform lane (implementation)

| Signal in the request | Agent | Repo stack |
|---|---|---|
| Dart, Flutter, BLoC, screen, widget, ObjectBox, ARB/l10n | `senior-mobile-engineer` | `flutter` |
| Go, endpoint, DAO, handler, resource, DB migration | `senior-backend-engineer` | `go` |
| Next.js, React, TypeScript, page, Supabase, shadcn | `senior-frontend-engineer` | `nextjs` |
| CI, GitHub Actions, deploy, Heroku, App Store, secrets, env, build tooling, disk | `senior-devops-engineer` | all |

### Review lane — always a *different* agent than the one that wrote the code

| Signal | Agent |
|---|---|
| Review Dart/Flutter: layers, SOLID, testability | `mobile-reviewer` |
| Review Go: layer violations, error handling, validation | `backend-reviewer` |
| Review TS/Next: type safety, a11y, patterns | `frontend-reviewer` |
| Crash / data-loss / sync / leak sweep | `bug-hunter` |
| Rebuild waste, list perf, jank, query patterns | `performance-auditor` |
| Auth, RLS, permissions, payments, uploads, secrets, PII, pre-release security pass | `security-auditor` |

### Test lane

| Signal | Agent |
|---|---|
| BLoC / use-case / mapper / repo tests | `mobile-test-engineer` |
| Jest + Playwright | `frontend-test-engineer` |
| Test *strategy*, scenarios, acceptance criteria (not code) | `qa-reviewer` |

### Product & planning lane

`product-manager` (PRDs) → `plan-scorer` (70+ gate) → `ux-designer` (flows/states) →
`implementation-planner` (file-by-file plan) → … → `master-plan-updater` (records).

### Cross-cutting

| Signal | Agent |
|---|---|
| Commits, short-lived branches, landing on the integration branch, rebases, releases | `git-steward` |
| User-facing copy in any repo | `ux-writer` |
| `docs/` pages | `docs-writer` / `tech-docs-updater` (post-change accuracy) |
| Dependency or SDK upgrades | `dependency-maintainer` |
| Scaffold a whole backend resource | `resource-handler-scaffold` |

## Step 3 — Tier and effort

**Every agent pins its tier in its own frontmatter** (`model:` + `effort:`). Do not pass a
`model` or `effort` override on dispatch — the frontmatter is the policy, and `/doctor` fails if
an agent lacks it. Override only when this task is clearly harder or easier than the agent's
usual work, and say why in the plan line.

| Tier | Agents | Why |
|---|---|---|
| **Opus** | `implementation-planner`, `principal-infrastructure-engineer`, `security-auditor`, `ux-designer`, `ui-designer`, `brand-director`, `product-manager`, `mobile-reviewer`, `backend-reviewer`, `frontend-reviewer`, `bug-hunter`, `senior-frontend-engineer` | Architecture, security, design system, high-stakes prose, independent review, and **all UI/visual work** (the web engineer builds user-facing screens; a Sonnet-built studio was rejected on 2026-10-20) — a wrong call costs more than the tokens |
| **Sonnet** | backend and mobile platform engineers, test engineers, `performance-auditor`, `qa-reviewer`, `plan-scorer`, `dependency-maintainer`, `ux-writer`, docs agents, `git-steward`, `resource-handler-scaffold` | Implementation and review against written rules |
| **Haiku** | `master-plan-updater` | Mechanical record-keeping |

**Quality outranks cost.** When unsure which tier fits, pick the higher one. Save tokens only where the result cannot get worse. **Any UI or visual task goes to an Opus agent** — when a Sonnet-pinned agent must touch UI, override `model: opus` and say why.

Effort is the second lever: `high` for reviewers, `bug-hunter`, planner, security, and
infrastructure; `low` for docs, git, scaffolding, and records; `medium` elsewhere.

Built-in and plugin agents carry no local frontmatter — pass `model` for those: `Explore` and
grep-and-summarise work on `haiku`, `Plan` on `opus`. Never use Fable — route that work to Opus.

**The main session is the biggest cost.** Routine sessions (docs, rule-following code, landing)
should run on Sonnet; switch the session to Opus for design, architecture, and security work.
On an Opus session, delegate implementation to the Sonnet agents instead of writing it inline.

## Step 4 — Dispatch

**Batch independent work into one message with multiple Agent calls.** Never dispatch
sequentially what could run concurrently.

Keep at most **five implementation agents active**, each on disjoint files or its own worktree
(worktree cap is 10). Reserve a slot for the orchestrator or a short read-only review. When one finishes, checkpoint its handoff before starting the next.
Large shared histories cost more than the parallelism saves.

Safe to parallelise:
- Different repos (mobile + backend + frontend)
- Read-only work (review, audit, planning, docs research) anywhere
- `verify.sh --quick` across repos

**Never parallelise:**
- Two agents editing the same file — serialise or split by file
- Two `--full` verifications or builds — the build cache is shared (see `storage-management`)
- Write-then-review of the same code — the reviewer must see the finished diff
- Anything where one agent's output is the next one's input

### Brief contract — every dispatch must carry all six

1. **Goal** — one sentence, the definition of done
2. **Scope** — exact files/dirs, and an explicit stop condition
   ("if it's not in these 3 files, report back rather than searching further")
3. **Context** — what's already ruled out, decisions already made, the run id
4. **Constraints** — the target as `<project>/<repo>` (and `wt:<project>/<repo>/<slug>` if a
   worktree exists); read `.claude/skills/verification/SKILL.md`; obey the project and repo
   AGENTS.md and the project overlays below
5. **Return format** — the final diff/data/decision, not a narrated walkthrough
6. **Handoff** — who's next

Write the brief in the `ste-writing` style: one instruction per sentence, imperative, condition first, exact values verbatim, rulings a reviewer can mark ✅ or ❌.

Point at **paths**, don't paste file contents — agents can read. Paste an excerpt only when
precision beats a re-read.

### Project overlays

Shared agents and skills are generic. Product facts live in overlay skills named
`projects/<project>/**/.claude/skills/<project>-<topic>/SKILL.md`. Topics in use: `app-patterns`, `backend-patterns`,
`web-patterns`, `code-consistency`, `analytics`, `copywriting`, `planning`, `dependencies`,
`release` —
each applies **only if the file exists** for that project (`ls .claude/skills | grep '^<project>-'`).

To brief an agent:
- Name the target: `example/backend`, not "the backend". Resolve repo, stack, and branches with
  `bash .claude/scripts/project.sh show <project>` — never assume `dev` or `main`.
- List the overlays that exist for that project and topic, e.g. "read
  `projects/example/AGENTS.md`, then `example-backend-patterns` and
  `example-code-consistency`".
- Local sources win: overlay and the project and repo AGENTS.md override the generic agent text.

## Step 5 — Supervise

- **Trust but verify.** An agent's summary is what it *intended*. For code changes, read
  `git diff` yourself before relaying anything as done.
- **Run the gate.** No task is complete until `verify.sh` exits 0 (see `verification`).
- **Reconcile conflicts explicitly.** When two agents disagree, say so and say how you resolved
  it. Never silently pick one.
- **Synthesize.** The user gets one integrated conclusion, not N transcripts.
- **Kill early.** An agent visibly off-track, or a task smaller than expected — stop it.
- **Reuse over respawn.** Continuing work an agent already has context on → `SendMessage` to it,
  not a fresh brief.
- **Event-driven waits.** Start a gate once, let `verify.sh` own its timeout and completion record,
  and read the result summary when it returns. Do not spend agent turns polling a test process or
  ingesting a successful test log.

## The HANDOFF block

Every agent ends with this; the pipeline advances only when the next agent has read it. Write
it and every report in the `ste-writing` style (section 8): status first, one fact per line, exact
commands and exit codes.

```
HANDOFF → <agent name or "user">
Read first: <exact paths>
Did:        <what changed, file by file>
Verified:   <commands actually run + exit codes, or "unverified">
Open:       <unresolved questions / assumptions made>
Do next:    <precise action>
Done when:  <verifiable condition>
```

## Worked shape — a full-stack feature

```
1. product-manager → plan-scorer            (sequential: score gates the PRD)
2. ux-designer ∥ implementation-planner     (parallel: independent inputs)
3. senior-backend-engineer                  (API first — the contract others consume)
4. senior-mobile-engineer ∥ senior-frontend-engineer   (parallel: different repos)
5. mobile-reviewer ∥ backend-reviewer ∥ frontend-reviewer  (parallel: read-only)
6. verify.sh all --full                     (sequential: shared build cache)
7. mobile-test-engineer ∥ frontend-test-engineer
8. tech-docs-updater ∥ ux-writer
9. git-steward → senior-devops-engineer     (land on integration branch, then release)
10. master-plan-updater
```

Skip any lane the task doesn't touch. A backend-only bug fix is steps 3, 5, 6, 9 — not ten phases.

## State

Bind every orchestrated task to a run (`session-continuity` skill). Log each dispatch and each
returned handoff so a fresh session can see what was delegated and what came back.
