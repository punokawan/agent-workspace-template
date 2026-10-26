---
name: copywriting
description: UX-writing and copy craft for every project (Flutter app, Next.js web, Go backend) — the two governing rules, voice principles, casing, one-word-per-concept terminology, button/title/empty/error/confirmation/toast patterns, number and date phrasing, punctuation, and the per-surface localization rules. Project voice, glossary, and locales live in projects/<project>/AGENTS.md and the <project>-copywriting overlay. Load whenever you write, edit, or review any text a person can read.
license: Proprietary
compatibility: Flutter gen-l10n, Next.js, Go REST API (error codes)
---

# Copywriting & UX writing (all projects)

Copy is part of the product, not decoration. Voice and terminology are shared across a project's app,
web, and API so a user sees one coherent product. Localization mechanics differ per surface.

Two rules sit above everything else:

1. **Be consistent.** The same concept uses the same word, casing, and punctuation in every repo.
2. **Localize per the surface's rules.** Never hardcode a user-facing string where that surface has a
   localization system.

## Source of truth

Read in order before writing or reviewing copy:
1. `projects/<project>/AGENTS.md` — the project's copy rule, reference locale, and vocabulary table
   ("use exactly these nouns")
2. `projects/<project>/<repo>/AGENTS.md` if present
3. `projects/<project>/**/.claude/skills/<project>-copywriting/SKILL.md` if it exists — voice examples, glossary, casing
   overrides, locales, formatter helpers, per-surface done criteria
4. `.claude/skills/l10n/SKILL.md` for ARB mechanics in a Flutter app
5. Existing strings near the change (search the ARB or copy module before adding a key)

Local sources win over this file.

---

## Voice principles

- **Clear over clever.** Say the plain thing. No puns in core flows.
- **Concise.** Cut every word that doesn't change meaning.
- **Supportive, never judgmental** — especially around money, deadlines, or failure. Guide, don't scold.
- **Calm, not loud.** Avoid exclamation marks except for genuine, earned celebration — and none where
  the project forbids them.
- **Second person.** Address the user as "you". Name the product only when needed.

Marketing/web copy may be warmer and more benefit-led than in-app utility copy, but stays in the same
voice — no growth-hack hyperbole.

## Casing

Studio default: **sentence case everywhere** — titles, buttons, labels, chips, hints, body, errors,
toasts. Capitalize the first word and proper nouns only. A project overlay may override this (for
example Title Case for titles); follow it exactly. Never use ALL CAPS for emphasis. Casing rules are
English conventions — follow each locale's own norms, and never force Title Case onto translations.

## Terminology — one word per concept

Use the project's vocabulary table exactly, in UI, web, API text, and docs. Never mix synonyms. Verbs
are consistent too: **Add** (create), **Edit** (change), **Delete** (remove permanently), **Cancel**
(back out), **Save** (commit), **Remove** (detach — not the same as Delete).

---

## Patterns by element

### Buttons & actions
Verb-first, 1–3 words, no trailing punctuation: `Save`, `Cancel`, `Add member`, `Try again`.
Destructive actions name the object when ambiguous (`Delete invoice`).

### Titles & headers
Noun phrases, no trailing period: `New invoice`, `Member details`, `Options`.

### Field labels & hints
Label = what the field is (`Amount`, `Note`). Hint = an example (`e.g. Monthly dues`). Never repeat
the label as the hint.

### Empty states
Three short beats: **what's here + why it's empty + one action.**
```
No invoices yet
Invoices appear here once dues are generated.
[ Generate dues ]
```

### Error & validation messages (app & web)
Plain language, no codes or stack traces to the user, no "Error:", no blame. Say what happened and
what to do next.
- ✅ `Amount can't exceed the remaining balance.`
- ✅ `Couldn't load your invoices. Pull to refresh.`
- ❌ `Validation failed: amount > balance`

### Confirmations
Title = the question. Body = the consequence. Buttons = the choices.
```
Delete this invoice?
This removes the invoice and its payment history. This can't be undone.
[ Cancel ]  [ Delete invoice ]
```

### Toasts / notifications / snackbars
One self-contained sentence, outcome first: `Invoice saved.`, `Couldn't sync — we'll retry.`

---

## Numbers, currency, dates — never hand-format

Formatting is locale-sensitive. Put the formatted value into a **named placeholder**, never via string
concatenation (concatenation breaks word order and RTL).
- **Flutter:** the project's formatter extensions; ARB placeholders such as `"{percent}% of {total}"`.
- **Web:** `Intl.NumberFormat` / `Intl.DateTimeFormat`, or the project's formatter helpers.
- **Backend:** return raw numbers and ISO dates; the client formats.

## Punctuation

- No trailing period on buttons, labels, titles, chips, or short captions.
- Full sentences in body/description/error text get a period.
- Use a real ellipsis `…` consistently.
- Use an em dash `—` for asides, sparingly.

---

## Localization by surface

Which locales and which reference locale apply come from the project. The mechanics per surface:

### Flutter app — full l10n, mandatory
Every user-facing string comes from the generated localizations accessor and exists in **every ARB
locale** the app ships. No literal display strings in widgets. Not done until the key is in the
template ARB and every other locale, gen-l10n has run, and the code uses the accessor. Mechanics:
`l10n` skill.

### Web (Next.js)
If the project wires an i18n library, every string goes through it. If not, author clean copy in the
reference language, centralize repeated strings in a shared copy module, and flag missing i18n as future
work — don't fake a localization layer.

### Backend (Go) — localized by code
User-facing error text is resolved in the client, keyed by a stable error `code`. Keep codes stable and
meaningful — renaming one silently breaks the client's localized message. The `msg` is clean
plain-language default text, no blame, no internal detail in production. Never ship user-facing prose
that exists only in Go where the client can't localize it. Emails follow the project voice and its
template localization, if any.

---

## Pre-flight checklist

- [ ] Project terminology; no synonyms — in app, web, and API text.
- [ ] Casing per project rule; verb-first buttons; no trailing punctuation on labels/buttons/titles.
- [ ] Tone calm and supportive; exclamations only where the project allows.
- [ ] Errors plain, blameless, actionable; no codes or jargon shown to users.
- [ ] Empty state = what + why + one action.
- [ ] Money/dates via formatters + named placeholders, never concatenation.
- [ ] **Flutter:** every string via the l10n accessor; key in every locale; gen-l10n run.
- [ ] **Web:** through i18n if wired; otherwise consistent and centralized, missing i18n flagged.
- [ ] **Backend:** stable `code` for every user-facing error; clean `msg`; no client-unlocalizable prose.

## Common anti-patterns

- Hardcoded display strings in Flutter widgets.
- Casing that breaks the project rule.
- String concatenation for money/percent.
- Inventing synonyms for a term in the project's vocabulary table.
- Renaming a backend error `code` without updating the client's localized mapping.
- A new backend user-facing error with no `code`.
