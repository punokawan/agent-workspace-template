---
name: workspace-maintenance
description: How this workspace's toolkit is organised — where shared, project and repo skills live, how Codex reaches them, where agents, commands and scripts go, and how to register a project. Load before adding, moving or renaming a skill, agent, command or project.
---

# Workspace maintenance

Moved out of the workspace `AGENTS.md` because it matters only when the toolkit
itself changes.

## Skills, agents and commands

| What it carries | Where it lives |
|---|---|
| Shared conventions, no project data | `.claude/skills/<name>/` |
| One repo's conventions | `<repo>/.claude/skills/<project>-<topic>/`, committed in that repo |
| One project's conventions, across its repos | `projects/<project>/.claude/skills/<project>-<topic>/` |

- Agents look a project skill up as `projects/<project>/**/.claude/skills/<project>-<topic>/`,
  which finds it at either level. A project with no repo here keeps every skill at project level.
- Next to every `.claude/skills` sits `.agents/skills` → `../.claude/skills`, so Claude Code and
  Codex read the same files. Skills are plain markdown; read the one that matches the task.
- Agents, commands and scripts live only in `.claude/`. Codex has no slash commands: it runs the
  script from the Scripts table in the workspace `AGENTS.md`.
- After adding or renaming an agent, command or skill: `bash .claude/scripts/roster.sh`.

## Adding a project

Register it with `/new-project`. It needs `projects/<name>/project.json` and
`projects/<name>/AGENTS.md` (with a `CLAUDE.md` that imports it). Project conventions go in that
guide and in the project's own skills, never in the workspace `AGENTS.md` or in the shared
agents. `projects/_example/` shows where every file goes.
