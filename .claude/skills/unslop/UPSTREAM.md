# Upstream

```upstream
repo: https://github.com/heydamir/unslop
path: skills/unslop
commit: 97daa3eb365670ea3f87ed85356cbfcee18105a5
mode: copy
licence: CC-BY-4.0
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/heydamir/unslop |
| Path taken | `skills/unslop/`, plus the repository `LICENSE` |
| Commit | see the block above (updated 2026-11-09 from `a6f121e`) |
| Licence | CC BY 4.0. Created by Damir Sokolovsky (@heydamir, https://x.com/heydamir) |

Keep this credit in any copy or adaptation, and keep the "unslop by @heydamir" credit in every story
video, as the licence asks.

Vendored on 2026-11-04 at the owner's request; updated to the newer upstream commit on 2026-11-09.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check unslop` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-04 (read-only): content, licence, secret scan, grep of both scripts; scripts not run.
- 2026-11-09 (read-only), update `a6f121e` → `97daa3e`, 3 files:
  - `SKILL.md`: snapshot accepts a local HTML file and scrolls before capture; two checklist items
    (table row states, button corners).
  - `scripts/snapshot.mjs`: stricter `--width`/`--height` parsing, local file paths turned into
    `file://` URLs, scroll pass in the page to load lazy content, image wait capped at 5 s. No new
    network target, no new writes, no shell.
  - `scripts/story.mjs`: no ffmpeg check in `--play`, robust `<meta>` parsing, frame validation, lint
    warnings, and removal of its own `<story folder>/.story-frames` on failure. `ffmpeg` still runs
    through `execFileSync` with an argument array (no shell).
  - `skill-security-auditor`: FAIL, same classes as the old version, all false positives:
    `execFileSync` import (fixed `ffmpeg` call), `RegExp.exec(...)` read as code execution, and the
    "Playwright is not installed" message read as a runtime install.
- The full line-by-line audit of both scripts before their first run (see Limits) is still open.

## Limits in this workspace

Routed from `.claude/agents/ui-designer.md`; the skill itself is unchanged.

- Use it only for public, landing and marketing pages, and for new mockups. Never on app screens that
  already follow a design system (the project's own design doc names it); use better-interface and
  audit-ai-design-slop there.
- Its job is the visual redesign. Marketing text on those pages belongs to the `marketing-skills`
  plugin: `copywriting` for new copy, `copy-editing` for copy that reads as AI-written. unslop's copy
  checklist items stay as checks; they do not replace those skills.
- Paid image generation (fal, Replicate, OpenAI images, Higgsfield) needs the owner's approval for each
  generation.
- Installing or connecting an MCP server needs the owner's approval. An agent never does it on its own.
- `scripts/snapshot.mjs` (fetches a live site or reads a local file with Playwright) and
  `scripts/story.mjs` (local server + ffmpeg) get a full line-by-line audit before their first run in
  this workspace. Record the audit date under Review.
- Its direction step must not override an owner-approved art direction or brand.

## Updating

1. `bash .claude/scripts/upstream.sh diff unslop` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull unslop` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is not
   real. Update the Commit row of the table.
