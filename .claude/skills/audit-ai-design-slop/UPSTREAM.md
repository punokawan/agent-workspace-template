# Upstream

```upstream
repo: https://github.com/MengTo/Skills
path: agent-skills/ui/audit-ai-design-slop
commit: 1de14e21b2ba8937c0f7f6ddca581cf7cd9d94af
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/MengTo/Skills |
| Path taken | `agent-skills/ui/audit-ai-design-slop/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2026 Meng To |

Keep `LICENSE` with any copy.

Vendored on 2026-11-04.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check audit-ai-design-slop` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-03 (security + fit, read-only; no scripts run).

## Limits in this workspace

- `audit-ai-design-slop` reads `../no-ai-design-slop/ARTICLE.md`; keep both installed together.
- ARTICLE.md credits the "Impeccable" slop catalog. The Impeccable repo (pbakaus/impeccable) is Apache-2.0 (checked 2026-11-03); whether its impeccable.style web page shares that licence is unverified.

## Updating

1. `bash .claude/scripts/upstream.sh diff audit-ai-design-slop` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull audit-ai-design-slop` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
