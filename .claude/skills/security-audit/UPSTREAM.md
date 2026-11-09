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

- Not recorded when it was vendored (commit 99d0e6a, 2026-10-27).
- 2026-11-09 (security + fit, read-only), at `c1c8a8c`:
  - `validate-findings.cjs` and `validate-coverage-ledger.cjs` use only `fs`, `path` and `TextDecoder`,
    and only read the file they are given (`open`, `read`, `readFile`). No network, no process, no writes.
  - The two test files write only inside their own `mkdtemp` folders and start only `node` and
    `mkfifo`. Run with Node 24.22.0: 65 tests, 65 pass, nothing left in the repository.
  - The markdown (SKILL.md and 13 companion files, about 1,700 lines) describes attack classes and
    forbids probing deployed endpoints, external services, production identities and live control
    planes, installing dependencies, and running target code without an OS-enforced sandbox.
  - `skill-security-auditor`: FAIL on the two `child_process` imports in the tests (`spawnSync` of
    `node` and `mkfifo`): false positives.

## Limits in this workspace

- Guidance mode by default. Full audit mode (six phases, report files) only when the owner asks for a
  full codebase audit or pen test; the skill itself asks one question when the request is unclear.
- Full audit mode delegates many agents. Agree a `budget` (maximum agent calls) with the owner first;
  the workspace default is a medium-size run.
- Its output folder defaults to `~/security-audit-skill/<repo>/run-<N>`, outside every repository. The
  files hold findings: never commit, paste or publish them.
- It never changes target source. Fixes go through the normal project flow; for a pre-landing review
  of a change, use the `security-auditor` agent.
- Its no-live-testing rule matches the workspace production-data rule: no probes against production
  or shared services.

## Updating

1. `bash .claude/scripts/upstream.sh diff security-audit` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull security-audit` — copies the files, bumps the commit, runs the scan.
3. Rerun `node validate-findings.test.cjs` and `node validate-coverage-ledger.test.cjs`.
4. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
