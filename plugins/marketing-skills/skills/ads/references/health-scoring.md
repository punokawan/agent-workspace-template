# Health Scoring: Weighting the Audit

Load this with [audit-guardrails.md](audit-guardrails.md) when an audit has to end in a number. The guardrails define what each check result means and when a score may be shown at all; this file defines how results are weighted. `scripts/ad_health_scorer.py` implements both, so the arithmetic is computed, not eyeballed.

## Contents
- The model
- Severity multipliers
- Category weights by platform
- Quick wins
- Input and usage

## The model

- Every check resolves to exactly one of **pass / fail / unknown / na** (not applicable). A partial pass is a fail with a detail that says what is missing.
- **Category health** = sum of the multipliers of passed checks ÷ sum of the multipliers of verified checks × 100. Verified means pass or fail.
- **Platform health** = category health × category weight, summed over the categories that have at least one verified check, divided by the weights used.
- **Evidence coverage** = verified checks ÷ applicable checks. An unknown lowers coverage, never health; na counts toward neither.
- **Coverage bands** (from audit-guardrails): 80%+ graded, 60–79% provisional, below 60% no health score at all. The script withholds the number below 60%.
- **Roll-up across platforms**: budget-weighted (equal weights when a budget is missing) over the platforms that have a score. A platform that was not audited, or sits below 60% coverage, stays out, and the roll-up is labeled partial.

## Severity multipliers

| Severity | Multiplier | Meaning | Fix within |
|---|---|---|---|
| Critical | 5 | Blocks revenue or burns budget | Now |
| High | 3 | Significant performance impact | 1 week |
| Medium | 1.5 | Optimization opportunity | 1 month |
| Low | 0.5 | Polish or best practice | Backlog |

One critical fail pulls its category down hard. That is intended: a missing conversion tag invalidates everything downstream of it.

## Category weights by platform

### Google Ads

| Category | Weight | Typical checks |
|---|---|---|
| conversion_tracking | 25% | Tag fires on a test conversion, enhanced conversions, primary actions, conversion window |
| wasted_spend | 20% | Search terms reviewed, negatives from real data, broad match only with smart bidding |
| account_structure | 15% | Naming, ad group themes, campaign types |
| keywords | 15% | Quality Score on top spenders, duplicates, match types vs intent |
| ads | 15% | RSA asset count, assets and extensions, active tests |
| settings | 10% | Location targeting, schedule, networks, bid strategy |

### Meta

| Category | Weight | Typical checks |
|---|---|---|
| pixel_capi | 30% | Pixel fires, Conversions API active, event deduplication, domain verification |
| creative | 30% | Format and concept diversity, fatigue, safe zones, copy length |
| structure | 20% | Campaign budget setup, naming, Advantage+ settings |
| audience | 20% | Seed size, exclusions, overlap, custom audiences |

### LinkedIn

| Category | Weight | Typical checks |
|---|---|---|
| technical | 25% | Insight Tag, conversion events, matched audiences |
| targeting | 25% | Audience size, job function vs title, company lists |
| creative | 25% | Format mix, call to action matches the offer |
| budget | 25% | Daily budget sufficiency, bid strategy, pacing |

### TikTok

| Category | Weight | Typical checks |
|---|---|---|
| pixel | 25% | Pixel installed, events configured, match quality |
| creative | 30% | Native feel, format mix, hook rate, creator content share |
| targeting | 25% | Interest vs behavior, custom audiences, lookalikes |
| budget | 20% | Enough budget to exit learning, pacing |

A category outside the platform's table gets weight 0.10 and is listed in the output. For another platform, run `--platform other`: every category then weighs the same.

The weights are a scoring convention, not a measurement. Edit `PLATFORM_WEIGHTS` in the script when the account's economics call for it, and say so in the readout.

## Quick wins

A failed critical or high check that the auditor marks `"effort": "low"`: a setting toggle, a missing asset, an exclusion list. List them first in the readout, each as a draft change for approval.

## Input and usage

One platform, an array of checks:

```json
[
  {"category": "conversion_tracking", "check": "Enhanced conversions enabled",
   "result": "fail", "severity": "critical", "effort": "low",
   "detail": "setting is off in the conversion action"},
  {"category": "wasted_spend", "check": "Search terms reviewed in the last 30 days",
   "result": "unknown", "severity": "high", "detail": "need the search terms report"}
]
```

Several platforms, with budgets and the ones you could not audit:

```json
{"google": {"checks": [], "budget": 3000},
 "meta": {"checks": [], "budget": 2000},
 "linkedin": {"audited": false, "reason": "no Campaign Manager access"}}
```

```bash
python3 scripts/ad_health_scorer.py --checks google.json --platform google
python3 scripts/ad_health_scorer.py --multi account.json --json
python3 scripts/ad_health_scorer.py            # demo account
```

For an ecommerce Google Ads account, the 32 checks in [google-ads-audit-checklist.md](google-ads-audit-checklist.md) are the check list: map each to a category above. Put the evidence you saw, or the evidence you still need, in `detail`, so the output doubles as the request list for unknowns.
