# Upstream

```upstream
repo: https://github.com/jakubkrehel/skills
path: skills/explain-interface
commit: 60bf140e43c98b248e6594487384ec967e89d98a
mode: copy
licence: MIT
extra: LICENSE
```

Vendored unchanged from https://github.com/jakubkrehel/skills (`skills/explain-interface`, plus `LICENSE`), commit `60bf140e43c98b248e6594487384ec967e89d98a`, MIT.
Only this file is ours. Reviewed 2026-11-03 (security + fit, read-only; no scripts run).
To update: `bash .claude/scripts/upstream.sh diff explain-interface`, then `pull explain-interface`.

Notes:
- Web recipes (CSS/Tailwind/ARIA). For the Flutter app the principles and numbers apply; `flutter-ui-patterns` stays the code authority.
- Motion values differ from emilkowalski `animate` (press scale 0.96 vs 0.97, base easing). A project's own motion tokens win; with none, `animate` is the motion authority.
