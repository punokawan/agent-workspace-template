# Upstream

Vendored unchanged from https://github.com/jakubkrehel/skills (`skills/break`, plus `LICENSE`), commit `60bf140e43c98b248e6594487384ec967e89d98a`, MIT.
Only this file is ours. Reviewed 2026-11-03 (security + fit, read-only; no scripts run).
To update: re-download every file at a newer commit, change the SHA here, and review the diff.

Notes:
- Web recipes (CSS/Tailwind/ARIA). For the Flutter app the principles and numbers apply; `flutter-ui-patterns` stays the code authority.
- Motion values differ from emilkowalski `animate` (press scale 0.96 vs 0.97, base easing). A project's own motion tokens win; with none, `animate` is the motion authority.
