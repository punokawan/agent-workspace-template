# Upstream

```upstream
repo: https://github.com/jakubkrehel/skills
path: skills/explain-interface
commit: 60bf140e43c98b248e6594487384ec967e89d98a
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/jakubkrehel/skills |
| Path taken | `skills/explain-interface/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2026 Jakub Krehel |

Keep `LICENSE` with any copy.

Vendored on 2026-11-04.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check explain-interface` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-03 (security + fit, read-only; no scripts run).

## Limits in this workspace

- Web recipes (CSS/Tailwind/ARIA). For the Flutter app the principles and numbers apply; `flutter-ui-patterns` stays the code authority.
- Motion values differ from emilkowalski `animate` (press scale 0.96 vs 0.97, base easing). A project's own motion tokens win; with none, `animate` is the motion authority.

## Updating

1. `bash .claude/scripts/upstream.sh diff explain-interface` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull explain-interface` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
