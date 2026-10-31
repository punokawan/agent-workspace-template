---
description: Hand a task to Codex end to end — Claude writes the brief, Codex makes it (2D image or sprite, 3D model through Blender, or code), Claude reviews, sends fixes back, and delivers
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Skill
---

Delegate to Codex: $ARGUMENTS

`$ARGUMENTS` describes what to make, e.g. `32x32 sprite of a green slime for example/game`,
`low-poly 3D treasure chest`, `implement the CSV export in example/api`. Empty → ask what to make.

## Procedure

1. Load the `codex-delegate` skill and follow its six steps: intake, brief, dispatch, review,
   fix loop, deliver.
2. Confirm the runner works before the first dispatch: `command -v codex` (missing → tell the
   user to install Codex and run `codex login`; stop).
3. For code in a client repo, load the project's `AGENTS.md` and open the worktree its profile
   asks for before dispatching with `--write`.
4. Finish with the skill's delivery report. Do not commit unless the user asks.
