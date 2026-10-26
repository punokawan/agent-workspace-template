---
description: Scaffold a complete new resource for a project's Go backend — migration, entity, DTOs, data access, service, handler, and all registration wiring — following that project's resource pattern.
argument-hint: [<project>/<repo>] <name> [field:GoType ...]  e.g. "example/backend recurring_transaction amount:float64 note:string walletID:string categoryID:string nextDate:string"
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <project>/<repo> <type>/<slug>` first. Never edit a checkout under
   `projects/<project>/<repo>/` directly — those are the user's working checkouts.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log new-resource "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# New Resource — Go backend

You are adding a new resource to a project's Go backend, following that project's own resource pattern.

## Input
`$ARGUMENTS`

---

## Step 1 — Resolve target, parse & clarify

**Target.** Take `<project>/<repo>` from the arguments or the bound run. If missing, run
`bash .claude/scripts/project.sh show <project>` and pick the repo whose stack is `go`; if still
ambiguous, ask.

Read `projects/<project>/AGENTS.md` (backend layering), `projects/<project>/<repo>/AGENTS.md` if
present, and `projects/<project>/**/.claude/skills/<project>-backend-patterns/SKILL.md` if it exists. When that overlay has
`references/resource-scaffold.md`, that template defines the plan, the files, the wiring, and the client usage example.

Extract:
- **Resource name**: snake_case (e.g., `recurring_transaction`, `tag`)
- **Fields**: remaining `field:GoType` pairs (Go types: `string`, `float64`, `int`, `bool`, `*bool`, `*string`)

If the name is missing, ask:
> What is the resource name (snake_case)? What fields does it have (name:GoType)?

If fields are missing but name provided, ask:
> What fields should `{Name}` have? Use `fieldName:GoType` format. Id, owner/tenant id, and timestamps are added automatically.

Do NOT proceed until you have both name and fields.

---

## Step 2 — Show the plan

List every file to create and every file to modify, each with a one-line reason — from the overlay
template if it exists, otherwise from where the nearest existing resource lives (migration,
entity/domain, data access, DTOs, service, handler/routes, wiring). Include the table name, the
tenant/owner scope column, and any manual DB step.

Ask: `Proceed with generation?`

---

## Step 3 — Delegate to resource-handler-scaffold agent

Use the `resource-handler-scaffold` agent (`.claude/agents/resource-handler-scaffold.md`).

Pass:
- Target `<project>/<repo>` and the worktree path
- Resource name (PascalCase and snake_case)
- Complete field list with Go types
- Whether this resource has pagination (default yes) and delete cascade

---

## Step 4 — Write and wire

Write the new files and apply every registration from the scaffold's checklist with the Edit tool.
Show the migration SQL, and say whether it still has to be applied by hand.

---

## Step 5 — Architecture check

Run the `backend-reviewer` agent on all newly created/modified files.

Report findings.

---

## Step 6 — Usage example

Show the client API calls for list, get, create, update, and delete — from the overlay template if it
has one, otherwise from the routes just registered.

---

## Rules throughout
- All Go code complete — no `// TODO` or `// ...`
- Owner/tenant id never exposed in JSON and never taken from the request body
- Every DTO field carries the tags the project's decoder needs; every DTO is validated
- Wrap all external errors in the project's error type
