# Upstream

- Source: https://github.com/miqdadbadjuber/anti-slop, `skills/antislop-code/SKILL.md` and `LICENSE`
- Commit: 941b1532f9cc8ffde766bca5921d75257c9e5762 (main, 2026-11-04)
- Licence: MIT. Keep `LICENSE` with any copy.
- Vendored unchanged on 2026-11-04 at the owner's request ("pilihkan yang memang belum dan berguna saja"). Only this skill was taken: the other five antislop skills overlap skills this workspace already has (no-ai-design-slop, audit-ai-design-slop, unslop, copywriting, ste-writing, better-*), and the core `antislop` skill is about 54 KB and is built to load in every session.

## Review (read-only, 2026-11-04)

- The file is instructions only: no scripts, no network calls, no install steps. `allowed-tools` lists Read, Write, Edit, Glob, Grep.
- Its scope guardrail matches this workspace's surgical-changes rule: it edits comments only, never code.

## Limits in this workspace

- The skill cites the upstream core (`antislop.md`, rules R-XX, the Delivery Gate), which is not vendored. Use the Code Comment Checklist at the end of SKILL.md on its own; the workspace `verification` skill stays the delivery gate.
- Repo comment rules win where they differ (for example a repo that requires a `// prisma-containment:` header or an owner-decision note keeps it).
- Do not edit SKILL.md here; update by re-vendoring a newer upstream commit and updating this file.
