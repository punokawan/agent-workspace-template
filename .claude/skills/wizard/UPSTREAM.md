# Upstream

- Credit: Matt Pocock, "Skills for Real Engineers" — https://github.com/mattpocock/skills
- Source: `skills/engineering/wizard/` (SKILL.md, template.sh, agents/openai.yaml) and `LICENSE`
- Commit: 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d (upstream HEAD on 2026-11-06)
- Licence: MIT, Copyright (c) 2026 Matt Pocock. Keep `LICENSE` with any copy.
- Vendored unchanged on 2026-11-06 at the owner's request: upstream name and content kept, with credit.

## Review (read-only, 2026-11-06)

- `template.sh` runs only when a human starts it. It opens URLs, reads input, upserts `.env`
  (mode 0600), and sets GitHub secrets or variables through `gh`. No other network calls.

## Limits in this workspace

- A wizard is run by the owner, never by the agent. It does not lift the core rules in
  `AGENTS.md`: a production write stays dry-run by default, needs an explicit `--apply`, and
  checks the database host before it writes.
- Do not edit the files here; update by re-vendoring a newer upstream commit and updating this file.
