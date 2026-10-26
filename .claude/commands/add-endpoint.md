---
description: Add a new HTTP endpoint to a project's Go backend — handler method, route registration, service method, data access and DTOs if needed. For operations that don't fit the project's generic resource pattern.
argument-hint: [<project>/<repo>] <domain> <method> <path> [description]  e.g. "example/backend identity POST /identity/v1/user/resend-verification Resend verification email"
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <project>/<repo> <type>/<slug>` first. Never edit a checkout under
   `projects/<project>/<repo>/` directly — those are the user's working checkouts.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log add-endpoint "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# Add Endpoint — Go backend

You are adding a new standalone HTTP endpoint. Use this when the operation doesn't fit the project's generic resource pattern (if it has one) — e.g., identity flows, special actions, admin ops.

## Input
`$ARGUMENTS`

---

## Step 1 — Resolve target, parse & clarify

**Target.** Take `<project>/<repo>` from the arguments or the bound run. If missing, run
`bash .claude/scripts/project.sh show <project>` and pick the repo whose stack is `go`; if still
ambiguous, ask.

Read `projects/<project>/AGENTS.md` (backend layering), `projects/<project>/<repo>/AGENTS.md` if
present, and `projects/<project>/**/.claude/skills/<project>-backend-patterns/SKILL.md` if it exists. When that overlay has
`references/endpoint.md`, it holds the exact templates — use them for Steps 3–6.

Extract:
- **Domain**: the handler/service package that owns the operation (or a new domain)
- **HTTP method**: `GET`, `POST`, `DELETE`, `PUT`, `PATCH`
- **Path**: full path string, matching the project's versioning style
- **Description**: what this endpoint does

If any are missing, ask before proceeding.

Also clarify:
- Is auth required? (protected or public middleware, as the project names them)
- What request body does it expect? (field names and types)
- What does it return on success? (entity, simple message, void)
- Does it need a new data-access method, or can it reuse existing ones?
- Which tenant/owner scope applies, and where it comes from in the auth context

---

## Step 2 — Show the plan

```
Endpoint:   {METHOD} {path}
Domain:     {domain}
Auth:       {protected | public}

Files to create/modify:
  <handler file>        ← new handler method
  <routes file>         ← new route registration
  <service file>        ← new interface method + impl
  <DTO file>            ← new request/response DTO (if needed)
  <data-access file>    ← new query method (if needed)
  <migration file>      ← if the schema changes
```

Take every path from the nearest existing endpoint in the same domain. Ask: `Proceed?`

---

## Step 3 — Handler and route

- Handler is always thin: decode → validate → call one service method → write the response once
- Always `return` after an early error write
- Owner/tenant id comes from the authenticated context, never the body
- Register the route next to its siblings with the project's middleware for protected or public
- For security-sensitive responses (e.g., forgot password): always return success regardless of whether the account exists

---

## Step 4 — Service

Add the method to the service interface (if the package uses one) and implement it: validate
input, call data access with `ctx`, return the project's application error type — never a raw
driver or ORM error.

---

## Step 5 — Data access (if a new DB operation is needed)

Add the method where the domain's queries live. It takes `ctx`, is scoped by construction,
checks every error, and translates driver/ORM errors to the project's typed errors. Multi-step
writes go in one transaction. Schema changes get a numbered, forward-only migration.

---

## Step 6 — DTOs (if new request/response types are needed)

Match the project's DTO file, tags, and validation method or schema exactly.

---

## Step 7 — Architecture check

Run `backend-reviewer` agent on all new/modified files.

---

## Rules
- All code complete — no `// TODO` or `// ...`
- Wrap all external errors in the project's error type
- Never write the response more than once without `return` after early writes
- For security endpoints: always return success to prevent information leakage
