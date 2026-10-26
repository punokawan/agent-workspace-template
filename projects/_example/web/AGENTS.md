# Example `web/` — repo guide

> Refines `projects/example/AGENTS.md` for this repo. When guides disagree, the one nearest
> the edited file wins (workspace `AGENTS.md` §Instruction precedence).

## Layering — Next.js App Router

```
app/(public)/     booking pages — no staff data
app/(staff)/      the staff desk
features/<f>/     components, hooks, schemas, services
lib/              pure utilities
```

1. **`app/(public)/` never imports from `app/(staff)/`.**
2. **Every boundary shape has a zod schema.** A hand-written cast at a boundary is a defect.
