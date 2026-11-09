# Upstream

```upstream
repo: https://github.com/Owl-Listener/designer-skills
path: visual-critique/skills/critique-visual-hierarchy
commit: 9a6930cf84a822eb458624bd11c61aac5bbdf224
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/Owl-Listener/designer-skills |
| Path taken | `visual-critique/skills/critique-visual-hierarchy/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2026 MC Dean |

Keep `LICENSE` with any copy.

Vendored on 2026-11-04.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check critique-visual-hierarchy` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-03 (security + fit, read-only; no scripts run).

## Limits in this workspace

- Descriptions mention sibling skills (`visual-hierarchy`, `hicks-law`) that were not vendored; ignore those pointers.
- Only these three of the visual-critique family were taken; colour, typography and affordance are covered by jakubkrehel `better-*`.

## Updating

1. `bash .claude/scripts/upstream.sh diff critique-visual-hierarchy` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull critique-visual-hierarchy` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
