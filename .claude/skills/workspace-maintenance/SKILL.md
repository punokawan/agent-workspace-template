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

## Rule profiles

Rules live as modules in `templates/rules/`. `core/` is always on and renders into the root
`AGENTS.md`; `optional/` modules are chosen per project and render into that project's
`AGENTS.md`, between `<!-- BEGIN:rules` and `<!-- END:rules -->`. Never edit inside the block.

| Profile | Optional modules |
|---|---|
| `light` | none — core only |
| `standard` | verify-gate, code-style, surgical-changes, studio-defaults, commit-discipline |
| `strict` | all of the above plus worktree-flow, run-state, file-size, offline-tests, incident-analysis, capacity-review |
| custom | whatever `rules.sh profile new/add/remove` puts in it |

`templates/rules/profiles.json` is the source of these lists and of the default profile for new
projects. Its `source` is the template repository every generated block names as its origin — a
fork sets its own URL there, then runs `rules.sh sync`. A project stores its choice as `"rules": {"profile": …, "enable": […], "disable": […]}`
in `project.json`.

```bash
bash .claude/scripts/rules.sh list                         # every profile and project
bash .claude/scripts/rules.sh set <project> standard       # switch a project's profile
bash .claude/scripts/rules.sh enable <project> offline-tests
bash .claude/scripts/rules.sh disable <project> worktree-flow
bash .claude/scripts/rules.sh default light                # profile for new projects
bash .claude/scripts/rules.sh profile new team from standard
bash .claude/scripts/rules.sh profile add team capacity-review
bash .claude/scripts/rules.sh profile delete team          # refused while a project uses it
```

The built-in profiles cannot be edited or deleted; copy one instead. A module's order inside a
profile is the order it renders in.

To add a module: write `templates/rules/optional/<name>.md` starting with a `## ` heading, add
it to the profiles that should carry it, run `rules.sh sync`. `/doctor` fails when a block is
stale.

### Bringing in an existing project

- **A repo just cloned into `projects/<name>/<repo>/`, no manifest yet:**
  `project.sh new <name> --rules <profile>` registers the folder without overwriting anything in
  it, then `project.sh add-repo <name> <repo> <stack>` records the existing checkout.
- **A registered project that still keeps its guide in `CLAUDE.md`, or has no `rules` yet:**
  `rules.sh adopt <name> [profile]` moves that text to `AGENTS.md` verbatim, makes `CLAUDE.md`
  import it, sets the profile (the default when none is given) and renders the block.

`rules.sh list` flags a project with no `AGENTS.md`, and `/doctor` fails until it is adopted.
