# {{TITLE}} — planning

The `planning` skill governs this folder. Status lives in each plan's frontmatter, never in prose.

| Folder | Holds |
|---|---|
| `features/` | Product PRDs, one per feature. Tech specs go in `features/tech/` |
| `improvements/` | Engineering improvement plans, numbered |
| `bugs/` | Bug-buster records |
| `templates/` | `prd-template.md` and `improvement-template.md` — copy, don't edit in place |

Every plan in `features/` and `improvements/` starts with this frontmatter:

```yaml
---
id: <kebab-case-id>
title: <title>
status: draft        # draft scoped in-progress partial shipped dropped needs-review
area: <area>
ships_as:            # the code symbol that proves it shipped, once known
---
```

```bash
bash .claude/scripts/plan.sh set <id> <status> "<why>" --project {{NAME}}
bash .claude/scripts/plan.sh index --project {{NAME}}     # regenerates INDEX.md
```
