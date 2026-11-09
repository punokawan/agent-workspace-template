# Upstream

```upstream
repo: https://github.com/mattpocock/skills
path: skills/engineering/wizard
commit: 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/mattpocock/skills |
| Path taken | `skills/engineering/wizard/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2026 Matt Pocock |

Keep `LICENSE` with any copy.

Vendored on 2026-11-06 at the owner's request: upstream name and content kept, with credit. Credit: Matt Pocock, "Skills for Real Engineers".

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check wizard` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-06 (read-only):
  - `template.sh` runs only when a human starts it. It opens URLs, reads input, upserts `.env`
    (mode 0600), and sets GitHub secrets or variables through `gh`. No other network calls.

## Limits in this workspace

- A wizard is run by the owner, never by the agent. It does not lift the core rules in
  `AGENTS.md`: a production write stays dry-run by default, needs an explicit `--apply`, and
  checks the database host before it writes.

## Updating

1. `bash .claude/scripts/upstream.sh diff wizard` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull wizard` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
