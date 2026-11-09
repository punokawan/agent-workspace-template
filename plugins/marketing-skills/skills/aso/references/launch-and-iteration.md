# Store Launch, Reviews, and Iteration

The store-side work around a launch and after it: listing readiness, ratings and reviews, update
cadence, and listing tests. For the wider launch (channels, press, community), see the **launch**
skill; for test design and sample sizes, see **ab-testing**.

## Contents

- Store Launch Timeline
- Pre-Launch Listing Checklist
- Ratings and Review Prompts
- Responding to Reviews
- Update Cadence
- Testing the Listing

## Store Launch Timeline

| When | Store work |
|---|---|
| 4 weeks before | Keywords and metadata final per storefront and language; all visual assets in every required size; analytics and install attribution set up (see **analytics**) |
| 2 weeks before | Build submitted for review, leaving time for a rejection and resubmission; compliance checked (age rating, privacy details, data safety); review-response templates and rating-prompt rules ready |
| Launch day | Listing live and correct in every storefront; launch announced on owned channels; review monitoring starts |
| Days 1-7 | Daily installs, conversion rate and crashes; reply to reviews within 24-48 hours; log issues for a quick fix release |
| Day 7 | Retrospective: results against the plan, quick listing fixes, first keyword and metadata update planned |
| About 2 weeks after | First update: fixes from launch feedback and the first metadata iteration |

Avoid a launch day right before the team is offline (a weekend or holiday in the main market), so
crashes and bad reviews get a fast response. Check the main markets' calendars for seasonal peaks
that suit the category and for major competitor releases.

## Pre-Launch Listing Checklist

| Area | Items |
|---|---|
| Metadata | Title, subtitle or short description, keyword field (Apple), description, promotional text (Apple), What's New, per localization |
| Visual assets | Icon, screenshots for each required device size, preview video, feature graphic (Google Play) |
| Compliance | Age or content rating, privacy policy URL, Apple privacy details, Google Play data safety, content rights |
| Measurement | Analytics and attribution SDKs, store console access for the team |
| Validation | `scripts/metadata_check.py check` passes for every storefront and language |

## Ratings and Review Prompts

Ask for a rating after a success, not at random:

- **Prompt after:** a completed core action, a milestone (first project done, a streak), several
  successful sessions, or a positive answer to an in-app "Was this helpful?"
- **Never prompt:** in the first session, after an error or crash, in the middle of a task, or
  repeatedly in a short period.
- Use the platform's native review prompt. On Apple, the system shows it at most three times in
  365 days and may show it less, so spend those chances on happy moments.
- Fix the issues behind 1-star reviews quickly; a fix release plus a reply to the reviewer often
  earns an updated rating.

## Responding to Reviews

**Negative (1-2 stars):**

1. Acknowledge the specific issue (one sentence).
2. Apologize without excuses (one sentence).
3. Give a fix, a workaround, or when a fix ships (one or two sentences).
4. Offer a direct support channel (one sentence).

```
We're sorry syncing is failing for you. A fix is in the next update; until then,
signing out and back in solves it for most people. If it doesn't, write to
<support channel> and we'll look at your account directly.
```

**Positive (4-5 stars):**

1. Thank them.
2. Name the specific thing they praised.
3. Invite them to keep going or share the app.

Reply in the reviewer's language. Prioritize recent negative reviews and reviews that describe a bug
others will hit; at very high review volumes, reply to patterns rather than to every review.

## Update Cadence

| Update | Typical rhythm | Store effect |
|---|---|---|
| Bug fixes | As needed | Protects the rating |
| Minor features | Every few weeks | Keeps the listing fresh |
| Major features | Every month or two | A real story for What's New and promotional text |
| Metadata refresh | Every 4-6 weeks | One keyword and copy iteration (see keyword-research.md) |

Write What's New for users: what they can do now that they couldn't before. Generic notes are
acceptable only for a frequent release train at a well-known brand (see the tier rules in SKILL.md).

## Testing the Listing

Use the stores' own tools: Apple Product Page Optimization and Google Play Store Listing Experiments
(limits in the specs references). Test one element at a time, in this order unless data says
otherwise:

| Element | Impact | Effort |
|---|---|---|
| Icon | High | Medium (design) |
| First screenshot | High | Medium |
| Title (Google Play; on Apple the title changes only with a new version) | High | Low |
| Short description | Medium | Low |
| Screenshots 2-5 | Medium | Medium |
| Preview video | Medium | High |

Test brief:

```
TEST ID:     ASO-<date>-<n>
STOREFRONT:
ELEMENT:
HYPOTHESIS:  If we <change>, then <metric> will <move> by <amount>, because <reason>.
METRIC:      store conversion rate (page view or impression to install)
SAMPLE:      <per-variant visitors needed, from the ab-testing calculator>
DURATION:    at least 7 days and full weeks, until the sample is reached
RESULT:      control <rate>, variant <rate>, confidence <value>
DECISION:    ship | keep control | retest
LEARNING:
```

Work out the sample size with the **ab-testing** skill's calculator from the listing's real baseline
conversion rate before starting. A low-traffic listing may not reach a readable result; then make the
change on judgment and watch the trend instead of calling a test.
