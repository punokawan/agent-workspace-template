---
description: Review and fix a project's user-facing copy across any repo (Flutter app, Next.js web, Go backend) — voice, terminology, casing, punctuation — and apply the right localization rule for that surface. Pass a path, feature name, or leave empty to check the git diff.
argument-hint: [path or feature name]  e.g. "example/app/lib/.../goal" or "example/web pricing page" or leave empty for git diff
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <repo> <type>/<slug>` first. Never edit a checkout under
   `projects/<project>/<repo>/` directly — those are the user's working checkouts.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log copy-review "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# Copy Review (any project)

Scope: `$ARGUMENTS`

## What this does

1. Collects every user-facing string in scope across whichever repo(s) it touches.
2. Reviews them for voice/tone, casing, canonical terminology, punctuation, and clarity.
3. Applies the correct localization rule per surface.

## Step 1 — Determine scope & repo

- **Path given** (`<project>/<repo>/...`): review files under it; the repo's stack (`project.sh show <project>`) decides the surface.
- **Feature name**: review that feature's screens/pages/handlers in the relevant repo(s) of the active or named project.
- **No argument**: review the current worktree `git diff` for changed/added user-facing strings.

## Step 2 — Run the agent

Use `.claude/agents/ux-writer.md`. Pass the `<project>/<repo>` target(s) and the worktree path.

It loads `projects/<project>/AGENTS.md`, `.claude/skills/copywriting/SKILL.md`, and
`projects/<project>/**/.claude/skills/<project>-copywriting/SKILL.md` if it exists (plus `l10n` for Flutter), then fixes
hardcoded/inconsistent strings per surface: Flutter → l10n accessor + every ARB locale + gen-l10n;
web → i18n if wired, else centralized copy with missing i18n flagged; backend → stable `code`, clean `msg`.

## Severity

Use the overlay's severity table if it has one. Default:

| Severity | Examples |
|---|---|
| Blocking | Flutter hardcoded string or key missing from some locales; backend user-facing error with no stable `code`; money/date built by concatenation |
| High | Casing that breaks the project rule; a synonym for a vocabulary-table term; error text with codes or blame shown to users |
| Medium | Trailing punctuation on buttons/labels; inconsistent ellipsis; vague empty/error copy; duplicated web literals |
| Low | Wordiness, tone drift, missed reuse of an existing key |

## After

```bash
bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full
```

Report changed strings (before/after), localization actions per surface, locales still needing a human pass, and any out-of-scope copy issues found.
