# Writing App Store Metadata

Patterns and worked examples for writing or rewriting a listing's text fields. Field limits and
store rules are in [apple-specs.md](apple-specs.md) and [google-play-specs.md](google-play-specs.md);
keyword choice is in [keyword-research.md](keyword-research.md). Write each localization in its own
language from its own keyword research; a literal translation keeps the source language's keywords.

## Contents

- Title
- Subtitle and Short Description
- Apple Keyword Field
- Description
- Screenshot Captions
- Before and After Examples

## Title

Formula for Challenger and most Established apps (see the brand tiers in SKILL.md):

```
[Brand] - [Primary keyword] [& Secondary keyword or benefit]
```

Checklist:
- [ ] Primary keyword within the first three words after the brand
- [ ] Within 30 characters, ideally within 3 of the limit
- [ ] Reads as a name, not a list
- [ ] No claim or price words ("best", "#1", "free"), calls to action, emoji or ALL CAPS
- [ ] No competitor or other-platform names

A Dominant brand can use the brand alone; that is a choice, not a gap.

## Subtitle and Short Description

Apple subtitle (30 characters, indexed): add words the title doesn't already have.

| Formula | Example |
|---|---|
| Verb + benefit | "Organize Your Whole Week" |
| Adjective + category | "Smart Task Manager" |
| Feature + feature | "Lists, Reminders & Notes" |
| Audience + solution | "Planner for Busy Teams" |

Google short description (80 characters, indexed, visible without expanding): one benefit-led
sentence with the secondary keyword. No performance claims, calls to action or unattributed
testimonials.

## Apple Keyword Field

- 100 bytes, comma-separated, no spaces after commas
- Single words, not phrases: Apple combines words across the title, subtitle and keyword field
- No word already in the title or subtitle
- One word form per term unless rankings show the other form needs its own entry
- No competitor names, other platform names, or claim and price words
- Changes ship only with a new app version, so plan them with releases

`scripts/metadata_check.py keyword-field` builds the field from a ranked list and reports what it
skipped.

## Description

On Apple the description is not indexed: write it for conversion only. On Google Play the full
description is indexed: write it for conversion first, then place keywords naturally.

Structure (both stores):

```
1. HOOK (first 1-3 sentences, visible before "more")
   The user's problem or desired outcome, the main value proposition,
   and on Google Play the primary keyword.

2. FEATURES (3-5 items)
   Each feature stated as a benefit. Short lines or bullets for scanning.
   On Google Play, secondary keywords where they fit.

3. PROOF
   Rating, review count, awards or press, a summarized user quote.
   Use only numbers you can verify today.

4. CLOSE
   What happens after install (free trial, no account needed, what's included).
   Disclose in-app purchases and subscriptions.
```

Keyword use on Google Play: primary keyword around 2-3% of words, secondary keywords around 1-2%
each, nothing above 5%. Measure with `metadata_check.py check --platform google --keywords ...`.

Apple promotional text (170 characters) sits above the description, does not affect search, and
changes without a new version: use it for time-bound news (a new feature, a seasonal event).

## Screenshot Captions

One message per screenshot, a few words, benefit first. Apple indexes caption text, so captions can
carry a keyword when it reads naturally.

| Version | Caption | Read |
|---|---|---|
| Weak | "Task List Feature" | Names a feature |
| Better | "Create Task Lists" | Action, but still a feature |
| Best | "Never Miss a Deadline" | States the outcome |

## Before and After Examples

These examples are in English; apply the same moves in the listing's language.

### Title

| Before | After | Why |
|---|---|---|
| "MyTasks" (7 chars) | "MyTasks - Todo List & Planner" (29) | Brand only → primary and secondary keywords |
| "FitTrack Pro" (12) | "FitTrack: Workout Log & Gym" (27) | Generic modifier → category keywords |

### Subtitle (Apple)

| Before | After | Why |
|---|---|---|
| "Get Things Done" | "Daily Task Manager & Reminders" | Vague slogan → two keywords and a clear benefit |

### Keyword field (Apple)

Before, phrases with spaces and repeats:

```
task manager, todo list, productivity app, daily planner, reminder app
```

After, title and subtitle words removed (MyTasks, todo, list, planner, daily, task, manager,
reminders), single words, no spaces:

```
checklist,habit,tracker,schedule,goals,widget,calendar,organizer,productivity,focus,notes,deadline
```

### Description opening

Before:

```
MyTasks is a comprehensive task management solution designed to help busy
professionals organize their daily activities and boost productivity.
```

After:

```
Forget missed deadlines. MyTasks keeps every task, reminder, and project in
one place, so you focus on doing, not remembering.
```

The rewrite opens on the user's problem, names a specific outcome instead of "boost productivity",
and keeps keywords natural. Add a proof line only with a number you can verify.
