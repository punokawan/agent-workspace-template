## Instruction precedence

Guides stack: this file → `projects/<name>/AGENTS.md` → `<repo>/AGENTS.md`. Follow all of them.

- **When two disagree, the guide closest to the files being changed wins**: repo over project
  over workspace. Judge by the path of the file you edit, not the directory the session started
  in. A worktree `.wt/<project>/<repo>/<slug>` counts as `projects/<project>/<repo>`.
- A nested guide states only what differs. Each override is marked
  `Override (<file> §<section>):` so the rule it replaces stays visible.
- The user's instructions in the conversation outrank every guide.
- Optional rule modules come from each project's profile: `rules` in its `project.json`,
  rendered into its `AGENTS.md` by `rules.sh`. Toolkit agents and commands mention worktrees,
  `/verify` and run state; when the project's profile does not enable the module behind a step,
  treat that step as recommended, not required.
