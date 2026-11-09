# Upstream

```upstream
repo: https://github.com/mattpocock/skills
path: skills/productivity/writing-for-agents
commit: 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/mattpocock/skills |
| Path taken | `skills/productivity/writing-for-agents/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2026 Matt Pocock |

Keep `LICENSE` with any copy.

Vendored on 2026-11-06 at the owner's request: upstream name and content kept, with credit. Credit: Matt Pocock, "Skills for Real Engineers".

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check writing-for-agents` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-06 (read-only):
  - Markdown only: no scripts, no network calls, no install steps.

## Limits in this workspace

- It sets the structure of a skill or guide. `ste-writing` still sets the sentence style, and
  `workspace-maintenance` still sets where files live.

## Updating

1. `bash .claude/scripts/upstream.sh diff writing-for-agents` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull writing-for-agents` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
