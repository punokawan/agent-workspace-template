# Funnel Analysis

Use this with `scripts/funnel_analyzer.py` when the question is where people drop off, why conversions fell, or which segment converts worse. The script computes the rates; this file covers what to feed it and how to read the result.

## Contents
- Define the stages first
- Read the output
- Diagnose a bottleneck
- Where to go next, by stage
- Anti-patterns
- Review cadence

## Define the stages first

- **Nested stages.** Each stage is a subset of the one before. If a count rises from one stage to the next, the stage definitions or the windows don't match; the script warns, and the rates are meaningless until it's fixed.
- **One closed window.** Take every count from the same closed observation window (Core Principles 6 in SKILL.md). A trial or lead still inside its window is pending, not lost.
- **A typical marketing funnel:** awareness (impressions, reach) → interest (clicks, engagement) → consideration (leads, signups) → intent (demos, trials, carts) → purchase → retention (repeat, upsell, referral). Use the event sequences in [event-library.md](event-library.md) for product funnels.

## Read the output

- **Largest absolute drop** shows where the most people leave; **largest relative drop** shows the weakest step. They often differ, so read both.
- **+1pt lift** is the relative gain in final conversions from one more percentage point at a stage: 100 ÷ the stage's rate, with every other rate held. A point at a 5% stage is worth +20% more completions; a point at a 40% stage, +2.5%. Low-rate stages pay most per point, while gains near the bottom turn into revenue soonest.
- **Segments** (channel, device, geography, cohort, campaign) often share an overall rate but break at different stages. Compare stage by stage, not only the overall rank.

## Diagnose a bottleneck

1. **Quantify it.** The rate, its change against the funnel's own history, and how many people it loses. Industry benchmarks come last and are directional only.
2. **Segment it.** Run the script with segments. An aggregate rate can hide one broken segment behind several healthy ones.
3. **Find the likely cause.**

   | Symptom | Likely cause | Check |
   |---|---|---|
   | High bounce on the landing page | Message mismatch with the ad, or a UX problem | Compare the ad with the page; test on mobile |
   | Long time on page, few conversions | Confusion or a missing CTA | Heatmap or session recordings |
   | Drop at the form | Too many fields or unclear value | Field-level form analytics |
   | Long gaps between stages | No nurture or slow follow-up | Email engagement, lead response time |
   | Drop after the pricing page | Price or packaging concerns | Pricing page tests, sales-call notes |
   | High cart or checkout abandonment | Checkout friction | Step-by-step checkout analysis |

4. **Hand it to the owning skill** (next section). Prioritize fixes with an ICE score from the **ab-testing** skill.

## Where to go next, by stage

| Transition | Common bottlenecks | Skill |
|---|---|---|
| Awareness → interest | Wrong audience, weak creative, message-market mismatch | ads, ad-creative |
| Interest → consideration | Page doesn't continue the ad, slow or broken mobile page, missing proof, form friction | cro, signup, copywriting |
| Consideration → intent | No nurture, unclear difference from alternatives, missing pricing, slow follow-up | emails, competitors, revops |
| Intent → purchase | Checkout friction, unhandled objections, no reason to act now | cro, pricing, offers |
| Purchase → retention | Slow onboarding, no ongoing engagement, no expansion path | onboarding, churn-prevention, referrals |

## Anti-patterns

1. **Optimizing the wrong stage.** Fixing checkout when the real problem is too little qualified traffic. Read the whole funnel first.
2. **Ignoring segment differences.** One healthy segment can hide a broken one.
3. **Raising the rate by shrinking the funnel.** Stricter targeting lifts conversion rate and can cut total conversions. Track rate and volume together.
4. **Watching one metric.** Pair them: CTR with CPA, CPA with volume.
5. **Reading too early.** Long B2B funnels take weeks or months to complete; an early read undercounts the bottom stages.

## Review cadence

| Review | Frequency | Focus |
|---|---|---|
| Campaign funnel check | Weekly | Stage rates of active campaigns |
| Full funnel review | Monthly | Overall health, where the bottleneck moved |
| Segment deep-dive | Monthly | Channel, device, and cohort comparisons |
| Funnel definition review | Quarterly | Stage definitions and how each stage is measured |
