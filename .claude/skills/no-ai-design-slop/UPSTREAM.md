# Upstream

```upstream
repo: https://github.com/MengTo/Skills
path: agent-skills/ui/no-ai-design-slop
commit: 1de14e21b2ba8937c0f7f6ddca581cf7cd9d94af
mode: copy
licence: MIT
extra: LICENSE
```

Vendored unchanged from https://github.com/MengTo/Skills (`agent-skills/ui/no-ai-design-slop`, plus `LICENSE`), commit `1de14e21b2ba8937c0f7f6ddca581cf7cd9d94af`, MIT.
Only this file is ours. Reviewed 2026-11-03 (security + fit, read-only; no scripts run).
To update: `bash .claude/scripts/upstream.sh diff no-ai-design-slop`, then `pull no-ai-design-slop`.

Notes:
- `audit-ai-design-slop` reads `../no-ai-design-slop/ARTICLE.md`; keep both installed together.
- ARTICLE.md credits the "Impeccable" slop catalog. The Impeccable repo (pbakaus/impeccable) is Apache-2.0 (checked 2026-11-03); whether its impeccable.style web page shares that licence is unverified.
