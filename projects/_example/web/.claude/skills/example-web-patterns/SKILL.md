---
name: example-web-patterns
description: Example repo-level skill (reference only). Shows where one repo's detailed patterns live — committed in that repo so they travel with every checkout and worktree. Load when working in the Example web repo.
---

# Example web — patterns

A repo-level skill lives in `<repo>/.claude/skills/` and is committed in that repo. Use it for
detail too long for the repo `AGENTS.md`: checklists, templates, worked examples.

## New booking page checklist

1. Route under `app/(public)/`, server-rendered.
2. Input schema in `features/booking/schemas.ts`.
3. Call the backend; never decide availability in the browser (EX1).
