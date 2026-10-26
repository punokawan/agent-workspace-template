---
description: Write or update any documentation page in a project's docs (projects/<project>/docs/) — feature guides, architecture overviews, flows, setup guides, backend or web sections. Pass a topic, feature name, or doc path to scope the work.
argument-hint: [<project>] <topic, feature name, or docs/ path>  e.g. "example wallet feature" or "app/flows/sync-strategy" or "new: backend/architecture/caching"
---

## Harness (applies before anything below)

1. **No worktree needed.** This command writes to `projects/<project>/planning/` or
   `projects/<project>/docs/`, which are not git repositories. Never touch repo source here.
2. **Load** `verification`. Anything asserted about the codebase needs a `path:line`; anything not
   grounded is written `ASSUMPTION:` or `unverified`. Do not describe code you have not read.
3. **Record:** `bash .claude/scripts/state.sh log write-docs "<file written>"`,
   and `state.sh decide` for any choice a future session could not re-derive.

---

# Write Documentation

Topic / Path: `$ARGUMENTS` (project = first word if it names a project, else the active project)

## What this does

1. Identifies which doc page to create or update based on `$ARGUMENTS`
2. Reads the relevant source code to extract accurate, current information
3. Writes or rewrites the doc page — never speculating, always from code
4. Registers new pages in `projects/<project>/mkdocs.yml` if a new file is created

## Agent

Use `.claude/agents/docs-writer.md`. Pass the project, the topic or path, and the instruction to load
`.claude/skills/mkdocs/SKILL.md` and `projects/<project>/**/.claude/skills/<project>-docs/SKILL.md` (if it exists) first.

## Task types inferred from $ARGUMENTS

The overlay's routing table wins when it exists. Default:

| Input | What to do |
|---|---|
| Feature name | Write/update the app feature page and the feature's technical reference |
| Flow / architecture topic | Write/update the matching page under the repo's section |
| Explicit path (e.g., "docs/shared/data-contracts.md") | Update that specific file |
| "new:" prefix | Create a new page and register it in `mkdocs.yml` |
| No argument | Audit the project's docs for stale content — report inaccuracies found vs current code |

## After writing

```bash
mkdocs serve -f projects/<project>/mkdocs.yml   # open http://127.0.0.1:8000
python3 .claude/scripts/_docs.py
```
