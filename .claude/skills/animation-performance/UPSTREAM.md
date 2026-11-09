# Upstream

```upstream
repo: https://github.com/emilkowalski/skills
path: skills/animation-performance
commit: f1090bec277140d02ed202440185ad9d02ac1490
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/emilkowalski/skills |
| Path taken | `skills/animation-performance/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2026 Emil Kowalski |

Keep `LICENSE` with any copy.

Vendored on 2026-11-04.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check animation-performance` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-03 (security + fit, read-only; no scripts run).

## Limits in this workspace

- Each SKILL.md opens with a canned "Initial Response" greeting; harmless, kept unchanged.
- Motion authority when a project has no motion tokens of its own (see jakubkrehel `better-ui`).

## Updating

1. `bash .claude/scripts/upstream.sh diff animation-performance` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull animation-performance` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
