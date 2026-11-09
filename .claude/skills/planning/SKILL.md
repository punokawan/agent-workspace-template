---
name: planning
description: Planning-system rules for every project — plan frontmatter as the status source of truth, plan.sh, folder roles, PRD and tech-doc split, templates, and the status update checklist. Load whenever creating, reviewing, scoring, updating, or organizing files under projects/<project>/planning/.
license: MIT
compatibility: Markdown planning docs, Claude agents, slash commands
---

# Planning System

Codex reads the generated root `AGENTS.md`; there is no separate Codex copy of this skill.

## Source of truth

Each project plans in `projects/<project>/planning/` (not a git repo — no worktree, no undo). Before
creating, scoring, or updating a plan, read in order:
1. `projects/<project>/planning/README.md` — that project's planning conventions
2. `projects/<project>/AGENTS.md` — vocabulary, product principles, known defects
3. `projects/<project>/**/.claude/skills/<project>-planning/SKILL.md` if it exists — extra records (master plan, score index,
   logs), scoring rubric, PRD structure, product context
4. `projects/<project>/planning/INDEX.md` and nearby plans in the same area

Local sources win over this file. If a project has no scoring rubric, do not invent one — say so.

## Status lives in frontmatter

Every file under `features/` and `improvements/` carries YAML frontmatter (`id`, `title`, `status`,
`area`, `ships_as`). `INDEX.md` is generated from it — never hand-edit the index or write a status line
in prose.

```bash
bash .claude/scripts/plan.sh set <plan-id> <status> "<why>"   # change a status
bash .claude/scripts/plan.sh index                            # regenerate INDEX.md
bash .claude/scripts/plan.sh audit                            # declared-vs-real drift
```

Statuses: `draft` `scoped` `in-progress` `partial` `shipped` `dropped` `needs-review`. Fill `ships_as:`
with the code symbol that proves the plan shipped as soon as it is known.

## Folder roles

- `planning/features/` — product PRDs for new features. One file per feature.
- `planning/features/tech/` — technical implementation specs, where the project uses them.
- `planning/improvements/` — engineering improvement plans, numbered sequentially.
- `planning/bugs/` — concrete bug-buster records.
- `planning/templates/` — `prd-template.md`, `improvement-template.md`, plus any project extras.
- `planning/research/`, `planning/reviews/`, `planning/reference/` — inputs to plans, not roadmap items.

## PRD + tech doc split

1. **PRD** (`planning/features/feature-name.md`) — product intent: what, why, user flows, locked rules,
   acceptance criteria. No file paths, no interface definitions, no schema.
2. **Tech doc** (`planning/features/tech/feature-name-tech.md`) — implementation spec: every file,
   interface, data shape, migration, DI wiring, locale key.

The PRD header links to the tech doc (`> **Technical doc:** [TECH — Feature Name](./tech/feature-name-tech.md)`),
and the tech doc links back (`> **PRD:** [PRD — Feature Name](../features/feature-name.md)`). Implement
from the PRD first, then the tech doc — never from the PRD alone when a tech doc exists.

Start every new PRD from `planning/templates/prd-template.md` unless the project overlay names another structure.

## Planning rules

- Keep copyable templates in `planning/templates/`, not the planning root.
- Keep audits and static references out of `features/` and `improvements/`.
- When two plans overlap, link them and say which one owns the shared scope.

## Status update checklist

When a feature or improvement ships:
- `plan.sh set <id> shipped "<what shipped>"` (or `partial` with the open gaps), then `plan.sh index`.
- Fill `ships_as:` if empty.
- Update any extra records the project overlay lists (master plan, score index, logs).
- If the work changes priority or duplicates another plan, update the connected plan's note.
