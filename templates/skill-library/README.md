# {{name}}

{{title}}. Every skill credits where each part came from in its own `SOURCES.md`.

## Install

The skills follow the open Agent Skills format (a folder with `SKILL.md`): they work in Claude Code,
Codex and any agent that reads that format.

- **Claude Code:** `/plugin marketplace add punokawan/agent-workspace-template`, then
  `/plugin install {{name}}@punokawan`.
- **Codex:** `codex plugin marketplace add punokawan/agent-workspace-template`, then
  `codex plugin add {{name}}@punokawan`.
- **Other agents, or only some skills:** copy folders from `skills/` into `.agents/skills/` (or the
  folder your agent reads). Keep `LICENSE` with any copy.

## Skills

<!-- SKILLS:START -->
<!-- SKILLS:END -->

## Credits

This library is an adaptation. All credit for the original skills goes to their authors.

**Every skill has its own `SOURCES.md`.** It lists each section of the skill and each file, the
upstream repository, skill, file and commit it came from, and whether it is used as is, edited (and
how) or new. When two sources cover the same topic they become one skill, and that skill's table
shows which part came from which source.

| Key | Repository | Path taken | Commit | Licence and copyright |
|---|---|---|---|---|
{{sources_table}}

## Licence

`LICENSE` holds the licence of this adaptation and every upstream licence in full. Keep it with any
copy.
