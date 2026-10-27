# Agent workspace template

One workspace for running several product projects with **Claude Code** and **Codex** from a
single shared toolkit: 27 specialist agents, 32 slash commands, 26 skills and the scripts behind
them. Each project picks how strict its rules are.

## What you get

- **One guide per level.** `AGENTS.md` at the workspace, project and repo level; each `CLAUDE.md`
  only imports its `AGENTS.md`, so both agents read the same text. The guide nearest the edited
  file wins.
- **Rule profiles per project.** `light`, `standard` or `strict`, or single modules on and off.
  Core rules (precedence, security, confirm before outward actions, never write production data)
  always apply.
- **Worktree flow.** Every change on a short-lived branch in `.wt/`, with project guides and
  skills linked in automatically.
- **Verification and run state.** `/verify` reports real exit codes; `/checkpoint` and `/resume`
  let another session pick work up.
- **Project data stays in the project.** Shared skills hold no project data; project and repo
  skills live with their project. `.agents/skills` links let Codex find the same skills.
- **A self-check.** `/doctor` fails on stale rosters, dead references, stale rule blocks and
  broken links.

## Requirements

- Claude Code and/or Codex
- `git`, `bash`, `python3`; `node` for the Ponytail plugin's hooks
- The toolchain of each stack you use (Flutter, Go, Node.js — see `templates/stacks/`). A Flutter
  repo that pins its SDK in `.fvmrc` also needs [fvm](https://fvm.app).

Run `bash .claude/scripts/env.sh` (`/env-check`) to see what is missing and how to install it on
your platform.

| Platform | How |
|---|---|
| macOS | Works as is. |
| Linux | Works as is. |
| Windows | **WSL2 (recommended):** clone and work inside the Linux file system. **Git Bash:** turn on Developer Mode, run `git config --global core.symlinks true` and set `MSYS=winsymlinks:nativestrict` *before* cloning, so `.agents/skills` and worktree links are real links; make `python3` resolve to Python 3. |

## Start

1. Create a repository from this template (**Use this template** on GitHub), or clone it.
2. Open Claude Code or Codex **in the workspace root** — the toolkit in `.claude/` is invisible
   from a subfolder. `.claude/settings.json` declares the Ponytail plugin; each person installs
   it once with `/plugin install ponytail@ponytail`.
3. Add a project:

   ```bash
   bash .claude/scripts/project.sh new my-app --title "My App" --desc "One line" --rules standard
   bash .claude/scripts/project.sh add-repo my-app web nextjs --clone <git-url>
   bash .claude/scripts/project.sh check
   ```

   In Claude Code, `/new-project` walks through the same steps and fills in the project guide
   from the code.

4. Run `bash .claude/scripts/audit.sh` (`/doctor`) — it must say `CONSISTENT`.

### A project you already have

- **Repo already cloned into `projects/<name>/<repo>/`:** run `project.sh new <name> --rules …`
  then `project.sh add-repo <name> <repo> <stack>`. Nothing in the folder is overwritten.
- **Registered project whose guide is still a `CLAUDE.md`:** run
  `bash .claude/scripts/rules.sh adopt <name> [profile]`. The text moves to `AGENTS.md` verbatim.

## Rule profiles

| Profile | Adds to the core rules |
|---|---|
| `light` | nothing |
| `standard` | verification gate, code style (Ponytail), surgical changes, studio defaults, commit discipline |
| `strict` | standard, plus worktree flow, run state, offline unit tests, incident analysis, capacity review |
| your own | any modules you list — see below |

```bash
bash .claude/scripts/rules.sh list                       # every profile and project
bash .claude/scripts/rules.sh set my-app strict          # switch a project
bash .claude/scripts/rules.sh enable my-app offline-tests
bash .claude/scripts/rules.sh disable my-app worktree-flow
bash .claude/scripts/rules.sh default light              # profile for new projects
```

**Custom profiles.** The three built-ins stay fixed so their names mean the same everywhere;
make your own beside them:

```bash
bash .claude/scripts/rules.sh profile new team from standard   # copy a profile, or start empty
bash .claude/scripts/rules.sh profile add team offline-tests
bash .claude/scripts/rules.sh profile remove team surgical-changes
bash .claude/scripts/rules.sh set my-app team
```

A rule only one project needs goes straight into that project's `AGENTS.md`, outside the
generated block. A rule several projects share becomes a module: write
`templates/rules/optional/<name>.md` starting with a `## ` heading, then add it to a profile.

Modules live in `templates/rules/`. The choice is stored in the project's `project.json` and
rendered into its `AGENTS.md`, because Codex cannot import files. Edit a module, then run
`rules.sh sync`; never edit inside a generated block.

## Layout

```
AGENTS.md            workspace guide (core rules + orientation)     CLAUDE.md imports it
.claude/
  agents/            specialist agents
  commands/          slash commands
  skills/            shared skills, no project data
  scripts/           project, rules, verify, wt, state, plan, changelog, storage, audit
  settings.json      Ponytail plugin, skill visibility
.agents/skills       link to .claude/skills, for Codex
templates/
  rules/             rule modules and profiles
  project/           what a new project starts from
  stacks/            per-stack verify commands and defaults
projects/
  _example/          reference layout — not a project, never a target
  <name>/            your project: project.json, AGENTS.md, its own git for the guides
    <repo>/          each repo: its own git checkout, its own AGENTS.md
.wt/                 worktrees (gitignored)
```

`projects/*` is gitignored except `_example`: each project keeps its guides in its own
repository, so this template never carries project data.

## Everyday commands

| Claude Code | Script (`bash .claude/scripts/…`), also for Codex |
|---|---|
| `/projects` | `project.sh list` |
| `/wt-start` · `/wt-finish` | `wt.sh start <project>/<repo> <type>/<slug>` · `wt.sh land …` |
| `/verify` | `verify.sh <project>/<repo> [--full]` |
| `/checkpoint` · `/resume` | `state.sh phase …` · `state.sh show` |
| `/doctor` | `audit.sh` |
| `/env-check` | `env.sh` |

The full table is in `AGENTS.md`; every agent, command and skill is listed in
`.claude/AGENTS.md`.

## Customising

- **Reports and decisions:** the `owner-report` skill shapes write-ups for non-developers, and
  `architecture-decision` structures trade-off questions.
- **Change the toolkit** (a skill, agent, command, or how projects are registered): load the
  `workspace-maintenance` skill first. Run `bash .claude/scripts/roster.sh` after adding or
  renaming one.
- **Fork it:** set `source` in `templates/rules/profiles.json` to your repository and run
  `rules.sh sync`, so generated blocks name your fork.

## License

The skills are marked `license: Proprietary`, except `security-audit`, vendored from
Cloudflare under MIT (see its `LICENSE` and `UPSTREAM.md`). This repository is private; do not redistribute
it without the owner's permission.
