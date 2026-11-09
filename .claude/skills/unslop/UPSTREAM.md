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
- 2026-11-09 (read-only), full line-by-line audit of both scripts at `97daa3e` (`snapshot.mjs` 197 lines,
  `story.mjs` 503 lines; `node --check` passes). Safe to run under the conditions in Limits. Facts:
  - Both load Playwright from Node's resolution or the current project's `node_modules`, and launch a
    fresh browser profile (no cookies or logins from the user's browser). `CHROME_PATH` is the only
    environment variable read.
  - `snapshot.mjs` visits the given URL or local file headless, scrolls, then fetches only the
    stylesheets and assets the page references and inlines them (under 3 MB each). It writes
    `<out>.html` and `<out>.live.png`, overwriting them. Scripts are removed from the copy, but inline
    `on…` handlers and `javascript:` links stay.
  - `story.mjs` reads the story HTML, serves its folder on `127.0.0.1` at a random port for the run
    only, renders frames into `<story folder>/.story-frames` (deleted at start, on failure and at the
    end) and runs `ffmpeg -y` through `execFileSync` with an argument array. Its path check is a plain
    prefix check, so a sibling folder whose name starts with the story folder's name is readable over
    that local port. `--play` opens a visible browser and writes nothing.
  - No other network access, no shell, no writes outside the paths above.

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
- The scripts (audited 2026-11-09, see Review) run only under these conditions:
  - Run them from a project folder whose `node_modules` you trust: Playwright is loaded from there.
    Installing Playwright, its browser or ffmpeg is the owner's call.
  - Write output into a new folder such as `unslop/`: both scripts overwrite their output files, and
    `story.mjs` deletes `<story folder>/.story-frames`.
  - Keep the story HTML in its own folder (for example `unslop/story/`), so its local server cannot
    reach a sibling folder with a similar name.
  - Treat a snapshot of a third-party site as untrusted: render it with the Playwright renderer or a
    browser profile with no logins, because inline handlers survive.
- Its direction step must not override an owner-approved art direction or brand.

## Updating

1. `bash .claude/scripts/upstream.sh diff unslop` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull unslop` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is not
   real. Update the Commit row of the table.
