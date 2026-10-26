---
name: l10n
description: Localization rules for Flutter apps using ARB files and gen-l10n — where strings live, how to add one to every locale, key naming, parameterized and plural strings, the generate step, and common mistakes. Project facts (locales, template locale, generated class, accessor, generate command) live in the project's app overlay.
license: Proprietary
compatibility: Flutter gen-l10n, ARB
---

# Localization (l10n) — Flutter gen-l10n

## Source of truth

Before adding or changing a string, read in this order:
1. `projects/<project>/AGENTS.md` — supported locales and the **reference locale** (not always English)
2. `projects/<project>/<repo>/AGENTS.md` if it exists
3. `projects/<project>/**/.claude/skills/<project>-app-patterns/references/l10n.md` only if it exists — accessor, generated
   class, ARB path, locale list, generate command (example: `example-app-patterns`)
4. The repo's `l10n.yaml` — `arb-dir`, `template-arb-file`, `output-class`, `output-dir`

Local sources win over this file. `copywriting` governs voice; this skill governs mechanics.

---

## How to access strings

Every user-facing string comes from the generated localization class through the project's accessor
(usually a `BuildContext` extension). Never hardcode a string in `build()`, a snackbar, a dialog, or
an error message shown to the user. Never call `Localizations.of<...>(context, ...)` directly when
the project has a non-nullable accessor.

```dart
Text(context.l10n.save)        // ✅ via the project accessor
Text('Save')                   // ❌ shows one language to every user
```

---

## Adding a new string

1. **Search first.** Grep the template ARB for an existing key with the same meaning. Do not duplicate.
2. **Add to the template ARB** (named by `template-arb-file` in `l10n.yaml`).
3. **Add the same key to every other locale ARB** in the same commit. A missing key breaks
   generation or falls back silently. If a translation is not ready, use the template string as a
   placeholder — never leave the key out.
4. **Regenerate** with the project's command (`flutter gen-l10n`, through FVM or a make target if the
   project uses one). Never edit generated files — they are overwritten on the next run.
5. **Use it** through the accessor.

---

## Parameterized strings

Placeholders use `{name}` in the ARB; gen-l10n turns them into method parameters.

```json
"orderShipped": "Order \"{name}\" shipped",
"transferred": "{amount} moved from {source} to {target}"
```

```dart
context.l10n.orderShipped(name: order.name ?? context.l10n.unnamed)
```

Always pass non-null strings. Nullable input gets a localized fallback or `?? ''` — never `null`,
which shows "null" or throws.

---

## Plural and select forms

Use ICU syntax when grammar changes with the count:

```json
"itemCount": "{count, plural, =0{No items} =1{1 item} other{{count} items}}"
```

For purely informational counts a non-plural string is fine. Languages without plural inflection
still need the key.

---

## Key naming

Keys are `lowerCamelCase`, named by meaning, not by screen path.

| Pattern | Example | Use for |
|---|---|---|
| Noun | `order`, `amount` | Single-word labels |
| NounAdjective | `orderArchived` | State descriptions |
| VerbNoun | `saveOrder`, `deleteMember` | Action button labels |
| ContextNoun | `orderCreateTitle`, `invoiceEmptyState` | Screen-specific strings |
| …Desc / …Caption | `noOrdersThisMonthDesc` | Body/description text |

Avoid path prefixes like `settings_order_archive_confirm` — `archiveConfirmationDesc` is reusable.

---

## Common mistakes

| Mistake | Symptom | Fix |
|---|---|---|
| Key missing from one locale ARB | Generation fails, or key name / fallback shown in that locale | Add to every ARB in the same commit |
| Edited a generated file | Change lost on next generate | Edit the template ARB, regenerate |
| Hardcoded string in a widget | One language for all users | Reuse or add a key (reviewers flag as Medium) |
| `null` passed to a parameterized string | "null" shown or runtime error | Localized fallback |
| Changed `l10n.yaml` casually | Generated class or paths move | Change only with a reason, regenerate, fix imports |

---

## Checklist for new features

- [ ] Every user-facing string goes through the project accessor
- [ ] No string literals in `build()`, error messages, or snackbar text
- [ ] New keys searched for first, added to the template ARB with meaningful names
- [ ] Same keys added to every other locale ARB
- [ ] Generate command run — no errors
- [ ] Parameterized strings get non-null inputs
