# projects/_example — reference layout

A sample project that shows where each file goes. It is **not a project**: the leading `_` keeps
it out of `project.sh list`, `check` and every other script, so nothing ever targets it. Copy
its shape, never its content. To start a real project, run `/new-project`.

```
projects/<name>/                    own git, tracking only the files below
  .gitignore                        from templates/project/gitignore.tmpl (left out here, so this
                                    folder stays visible to the boilerplate's git)
  project.json                      repos, stacks, branches, deploy, and "rules": {"profile": …}
  AGENTS.md                         project guide, always loaded for this project's files; its
                                    rules block is rendered by rules.sh from the profile
  CLAUDE.md                         @AGENTS.md
  CONTRACTS.md, GLOSSARY.md, ...    long reference text the guide points to (optional)
  .claude/skills/<name>-<topic>/    skills for the whole project, may carry project data
  .agents/skills -> ../.claude/skills   so Codex sees the same skills
  <repo>/                           its own git checkout (listed in project.json)
    AGENTS.md                       repo guide: only what differs, e.g. layering
    CLAUDE.md                       @AGENTS.md
    .claude/skills/<name>-<topic>/  skills for this repo only, committed in the repo
    .agents/skills -> ../.claude/skills
  docs/, planning/                  local to this machine, not in any git
```

Guides stack workspace → project → repo; the one nearest the edited file wins (workspace
`AGENTS.md` §Instruction precedence). `web/` here holds only its guide and skill — a real repo
holds its code beside them.
