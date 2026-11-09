# Upstream

```upstream
repo: https://github.com/cloudflare/security-audit-skill
path: skills/security-audit
commit: c1c8a8c1471069fb0e188eeaff69b8e8db6564a8
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/cloudflare/security-audit-skill |
| Path taken | `skills/security-audit/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2025-2026 Cloudflare, Inc. |

Keep `LICENSE` with any copy.

Vendored on 2026-10-27.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check security-audit` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- Not recorded when it was vendored (commit 99d0e6a, 2026-10-27). Review before the next pull.

## Limits in this workspace

- None recorded yet beyond the workspace rules.

## Updating

1. `bash .claude/scripts/upstream.sh diff security-audit` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull security-audit` — copies the files, bumps the commit, runs the scan.
3. Rerun `node validate-findings.test.cjs` and `node validate-coverage-ledger.test.cjs`.
4. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
