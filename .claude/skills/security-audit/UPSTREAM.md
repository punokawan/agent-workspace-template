# Upstream

```upstream
repo: https://github.com/cloudflare/security-audit-skill
path: skills/security-audit
commit: c1c8a8c1471069fb0e188eeaff69b8e8db6564a8
mode: copy
licence: MIT
extra: LICENSE
```

Vendored unchanged from https://github.com/cloudflare/security-audit-skill
(`skills/security-audit/`, plus `LICENSE`), commit `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`, MIT.
Only this file is ours. To update: `bash .claude/scripts/upstream.sh diff security-audit`, then
`pull security-audit`, and rerun `node validate-findings.test.cjs` and `node validate-coverage-ledger.test.cjs`.
