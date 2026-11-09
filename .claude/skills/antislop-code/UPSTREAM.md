# Upstream

```upstream
repo: https://github.com/miqdadbadjuber/anti-slop
path: skills/antislop-code
commit: 941b1532f9cc8ffde766bca5921d75257c9e5762
mode: copy
licence: MIT
extra: LICENSE
files: SKILL.md
```

| | Source |
|---|---|
| Repository | https://github.com/miqdadbadjuber/anti-slop |
| Path taken | `skills/antislop-code/` (only `SKILL.md`), plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2026 Miqdad Badjuber (antislop) |

Keep `LICENSE` with any copy.

Vendored on 2026-11-04 at the owner's request ("pilihkan yang memang belum dan berguna saja"). Only this skill was taken: the other five antislop skills overlap skills this workspace already has (no-ai-design-slop, audit-ai-design-slop, unslop, copywriting, ste-writing, better-*), and the upstream core (antislop, not vendored) is about 54 KB and is built to load in every session.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check antislop-code` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-04 (read-only):
  - The file is instructions only: no scripts, no network calls, no install steps. `allowed-tools` lists Read, Write, Edit, Glob, Grep.
  - Its scope guardrail matches this workspace's surgical-changes rule: it edits comments only, never code.

## Limits in this workspace

- The skill cites the upstream core (`antislop.md`, rules R-XX, the Delivery Gate), which is not vendored. Use the Code Comment Checklist at the end of SKILL.md on its own; the workspace `verification` skill stays the delivery gate.
- Repo comment rules win where they differ (for example a repo that requires a `// prisma-containment:` header or an owner-decision note keeps it).

## Updating

1. `bash .claude/scripts/upstream.sh diff antislop-code` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull antislop-code` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
