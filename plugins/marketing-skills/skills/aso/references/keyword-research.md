# App Store Keyword Research

How to find, rank and place keywords for an App Store or Google Play listing. Do this once per
storefront and language: searchers in each market use their own words, so translate the method,
not the keyword list.

## Contents

- Generate Seed Keywords
- Expand the List
- Filter
- Prioritize
- Competitor Keyword Coverage
- Map Keywords to Fields
- Track and Iterate

## Generate Seed Keywords

Collect candidates from four sources:

1. **Core app functions.** List every action the app performs or problem it solves (create tasks,
   set reminders, track deadlines, plan the day).
2. **User language.** Translate product terms into the words users type. Customer interviews, reviews
   and support tickets show these words; the context file's Customer Language section often has them.

   | Product term | What users search |
   |---|---|
   | Task management | todo list, task app, tasks |
   | Deadline tracking | due date reminder, deadline app |
   | Time blocking | schedule planner, calendar app |

3. **Store autocomplete.** Type each seed into the store search box and record the suggestions. Do it
   on a device set to the target storefront and language.
4. **Competitor metadata.** Titles, subtitles and short descriptions of the top apps in the category
   (see **Competitor Keyword Coverage**).

## Expand the List

Combine each core term with:

| Technique | Example (seed: "todo") |
|---|---|
| Actions | make todo list, organize todo |
| Platforms and surfaces | todo widget, todo for watch |
| Audiences | todo for students, family todo |
| Features | todo with reminders, todo calendar |
| Problems | forgot tasks, procrastination |
| Modifiers | simple todo, free todo |

Modifiers such as "free" or "best" show what people search, but they are claim or price words: keep
them out of the title, subtitle, short description and keyword field (see the store rules in
[apple-specs.md](apple-specs.md) and [google-play-specs.md](google-play-specs.md)).

## Filter

Remove:

| Remove | Why |
|---|---|
| Competitor brand names | Guideline violation and rejection risk (Apple 2.3.7) |
| Terms for a different category | Searchers will not convert |
| Words already in the title or subtitle (Apple keyword field) | Apple indexes each word once |
| The store's category name | Already associated through the category choice |
| A second word form (plural or singular) | Usually wasted bytes; keep both only if rankings show the other form needs its own entry |

## Prioritize

Rank the filtered list on four factors. Relevance comes first: a high-volume term that does not
describe the app brings installs that churn, and stores learn from that.

| Factor | Weight | What makes it high |
|---|---|---|
| Relevance | 35% | Describes the core function, not a side feature |
| Volume | 25% | High search volume in this storefront (from an ASO tool's estimate) |
| Competition | 25% | The top-ranking apps are weak: few ratings, low ratings, poor keyword targeting |
| Intent | 15% | The searcher wants an app like this now ("[app type] app", "[app type] for [use]") rather than information |

Score each factor 0-100, take the weighted sum, and sort:

| Weighted score | Tier | Where it goes |
|---|---|---|
| 80-100 | Primary | Title; Apple keyword field |
| 60-79 | Secondary | Subtitle or short description; Apple keyword field |
| 40-59 | Tertiary | Google Play full description; Apple keyword field if bytes remain |
| Under 40 | Drop | Do not target |

Volume and competition are estimates. No store publishes search volume, so state the tool and date
behind each number, and say when a figure is a guess.

## Competitor Keyword Coverage

1. Pick 5-10 competitors: direct (same job, same audience), indirect (overlapping audience), and the
   category leaders.
2. Collect their title, subtitle (Apple) or short description (Google), and the first 100 words of the
   description.
3. Build the coverage matrix: which apps use each term, and what share of the set that is. The bundled
   script does this from a JSON file (`metadata_check.py coverage`, see SKILL.md).
4. Read the coverage:

   | Coverage | Read |
   |---|---|
   | 60% or more | Category term: searchers expect it; missing it is a gap |
   | 40-59% | Common: worth targeting if it fits the app |
   | Under 40% | Rare: a differentiator, a long-tail opportunity, or irrelevant |

5. For each gap, decide: the app already has the feature (update metadata), the feature is missing
   (product roadmap, not metadata), or the term is irrelevant (ignore).

Coverage shows what competitors target, not what users search. Check volume before you act on a gap.

## Map Keywords to Fields

| Field | Search weight | Notes |
|---|---|---|
| Title (both stores) | Highest | Brand plus the primary keyword |
| Subtitle (Apple) | High | New words only; Apple indexes each word once |
| Keyword field (Apple) | High | Hidden; 100 bytes; commas, no spaces |
| Short description (Google) | High | Visible without expanding |
| Full description (Google) | Medium | Indexed; natural use, about 2-3% for the primary keyword |
| Description (Apple) | None | Not indexed; write it for conversion |

Write the map down before writing copy:

```
PRIMARY (title, keyword field):        task manager, todo list
SECONDARY (subtitle / short desc):     reminder, daily planner
TERTIARY (Google full description):    checklist, schedule, deadline, project
```

### Apple keyword field, step by step

1. List every target term in priority order.
2. Remove words already in the title and subtitle.
3. Split phrases into single words: Apple combines words across the title, subtitle and keyword field,
   so "habit,tracker" also covers "habit tracker".
4. Remove competitor names, other platform names and claim or price words.
5. Fill the 100 bytes in priority order, comma-separated with no spaces. Non-Latin scripts take 2-3
   bytes per character.

`metadata_check.py keyword-field` does steps 2-5 and reports what it skipped and why.

### Google Play full description

Place keywords where they read naturally: the primary keyword in the first sentences, secondary
keywords in the feature paragraphs, long-tail phrases in benefit and differentiator paragraphs. Google
uses natural-language understanding and penalizes stuffing; `metadata_check.py check --keywords ...`
reports density and flags anything over 5%.

## Track and Iterate

| Cadence | Action |
|---|---|
| Weekly | Rankings for the primary and secondary keywords |
| Monthly | Full keyword set and competitor coverage |
| Quarterly | Repeat the research from the seed step |

Monthly review:

1. Record the current position and 30-day trend for each tracked keyword.
2. Push keywords ranked 11-20: move them to a stronger field.
3. Keep keywords in the top 10 where they are.
4. Replace keywords stuck beyond position 50 with the next candidates.
5. Log every change with its reason and check again after two weeks (Apple keyword-field changes ship
   only with a new app version).

Keyword change log:

```
CHANGE ID: KW-<date>-<n>
STOREFRONT / LANGUAGE:
FIELD:            keyword field | subtitle | title | short description | full description
ADDED:            <term> (replacing <term>)
RATIONALE:        <volume, relevance or gap evidence, with source and date>
BASELINE RANK:    <term>: <position or not ranked>
RESULT (30 DAYS): <term>: <position>
DECISION:         keep | revert | move to a stronger field
```

Attribute a ranking change to a keyword change only when nothing else changed in the same period
(ratings, a feature, seasonality, a competitor's update).
