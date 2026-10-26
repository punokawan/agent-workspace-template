---
description: List the projects this workspace hosts, show one project's repos and branches, or switch the active project that bare repo names resolve against.
model: haiku
---

# /projects

Inspect and switch between the projects in this workspace.

## Harness contract

- **Where you may write:** only `.claude/agentic-state/CURRENT_PROJECT`, and only via
  `project.sh use`. This command never edits a manifest — changing a repo, stack, or branch
  is `/new-project`'s job or a deliberate hand edit of `projects/<name>/project.json`.
- **Evidence required:** grade **A**. Report what the commands printed; never describe a
  project from memory or from an earlier session's context.
- **Gate:** none — this command is read-only apart from the active-project pointer.

## Steps

With no argument, list everything and show the active project:

```bash
bash .claude/scripts/project.sh list      # * marks the active project
```

With a project name, show its detail:

```bash
bash .claude/scripts/project.sh show <name>
```

To switch which project a bare repo id resolves against:

```bash
bash .claude/scripts/project.sh use <name>
```

If anything looks wrong — a repo listed that has no checkout, a stack that does not exist —
run the validator and report exactly what it says:

```bash
bash .claude/scripts/project.sh check
```

## Notes for the reader

- Targets are addressed **`<project>/<repo>`**. The active project only matters when
  someone writes a bare repo id.
- `projects/<name>/AGENTS.md` holds that project's conventions and known defects. Point the
  user at it rather than summarising it from memory.
- A project's repos, stacks, branches and deploy targets all come from
  `projects/<name>/project.json`. That file is the source of truth; if prose anywhere
  disagrees with it, the prose is wrong.
