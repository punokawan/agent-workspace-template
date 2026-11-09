# Referral Program Measurement

Formulas, benchmarks, a diagnosis tree, a phased optimization plan and a weekly report. For ROI and incentive sizing, see [program-examples.md](program-examples.md); for affiliate cohort economics, see [affiliate-operations.md](affiliate-operations.md).

The benchmarks below are unsourced practitioner rules of thumb. They shift with the definition and the time window, so compare against your own baseline first and state the definition you use. Revenue thresholds are in USD for orientation only.

## Contents
- Core Metric Stack
- Benchmarks by Stage and Model
- Diagnosing the Broken Stage
- Optimization Playbook
- Affiliate Metrics
- Weekly Report Template

## Core Metric Stack

Track these weekly; everything else is secondary.

| Metric | Formula | Rule of thumb (SaaS) | What it tells you |
|--------|---------|----------------------|-------------------|
| Program awareness | Users who know the program / active users | >40% | Whether you promote it at all |
| Active referrer rate | Users who sent ≥1 referral in the period / active users | 5-15% | How many users take part |
| Referrals per active referrer | Referrals sent / active referrers | 2-5 per period | How motivated referrers are |
| Share rate | Users who share / users who saw the prompt | 20-40% | Prompt placement and share-flow friction |
| Referral conversion rate | Converted referrals / referrals sent | 15-30% | Quality of referred traffic |
| Reward redemption rate | Rewards redeemed / rewards issued | >70% within 30 days | Whether the reward is wanted |
| CAC via referral | Program cost / customers acquired via referral | <50% of paid CAC | Efficiency against other channels |
| K-factor | Invitations per user × conversion rate | >0.5 meaningful, >1 self-sustaining | Viral growth |

Define the window. A period-based active referrer rate runs lower than the share of customers who have ever referred (the referral rate in [program-examples.md](program-examples.md)).

---

## Benchmarks by Stage and Model

### Early-stage SaaS (<$1M ARR)
| Metric | Expected | Strong |
|--------|----------|--------|
| Active referrer rate | 2-5% | >8% |
| Referral conversion rate | 10-20% | >25% |
| CAC via referral vs. paid | 30-50% of paid CAC | <25% of paid CAC |

### Growth-stage SaaS ($1M-$10M ARR)
| Metric | Expected | Strong |
|--------|----------|--------|
| Active referrer rate | 5-10% | >12% |
| Referral share of new signups | 10-20% | >25% |
| Referral share of revenue | 5-15% | >20% |

### Consumer / prosumer products
| Metric | Expected | Strong |
|--------|----------|--------|
| Active referrer rate | 8-20% | >25% |
| Referral conversion rate | 20-40% | >50% (with a double-sided reward) |
| K-factor | 0.3-0.7 | >1.0 (a true viral loop) |

### B2B mid-market (ACV $10k+)
| Metric | Expected | Strong |
|--------|----------|--------|
| Active referrer rate | 3-8% | >10% |
| Referral conversion rate | 20-40% (warm introductions convert higher) | >50% |
| Deal size via referral vs. standard | Similar | 20-40% higher (trust shortens negotiation) |

---

## Diagnosing the Broken Stage

```
Is the referral rate low?
  └── Is awareness low?                 → Promote the program
  └── Is the trigger at the wrong time? → Move it to a better moment
  └── Is the reward too weak?           → Test a larger or different reward
  └── Is the share flow complex?        → Simplify it

Is referral conversion low?
  └── Is the landing page cold?             → Personalize it for referred users
  └── Is the referred user's benefit unclear? → Put it above the fold
  └── Is signup friction high?              → Cut required fields

Is reward redemption low?
  └── Is the notification late?   → Send it on the qualifying event
  └── Is the reward type wrong?   → Test cash vs. credit vs. feature unlock
  └── Is redemption complex?      → Apply credits automatically
```

---

## Optimization Playbook

Work in this order and change one thing at a time.

### Phase 1: Foundation (month 1)
Goal: baseline awareness and share rate.
1. Check whether users know the program exists
2. Promote it in the product: dashboard banner, post-activation prompt, success-state trigger
3. Add it to the regular activation or product email
4. Make sure the share flow works on mobile

Success gate: awareness >30%, active referrer rate >3%.

### Phase 2: Trigger optimization (month 2)
Goal: ask at the right moment, not any moment.
1. Map every current trigger point
2. Define the aha moment, then move or add a trigger there
3. Test: trigger after the aha moment vs. after 7 days of retention
4. Add a recommendation-score trigger: a 9-10 score gets an immediate referral ask

Success gate: active referrer rate up 30% over Phase 1.

### Phase 3: Incentive tuning (month 3)
Goal: the right reward, at the right time, delivered well.
1. Ask lapsed referrers why they stopped
2. Test single-sided vs. double-sided if not yet tested
3. Test reward type: credit vs. cash vs. feature unlock
4. Add a reward-status widget: "You've earned X. [View details]"
5. Release rewards on the qualifying event, not at month-end

Success gate: redemption >70%, CAC via referral <40% of paid CAC.

### Phase 4: Referred-user conversion (month 4)
Goal: referred users convert at about twice the organic rate.
1. Personalize the referred-user landing page (referrer's name where available)
2. Put the referred user's incentive above the fold
3. Test sending referred users to the product vs. a dedicated landing page
4. Add a "referred by" onboarding track with a faster path to first value

Success gate: referred-user conversion of 20% or more, against the organic baseline.

### Phase 5: Scale and gamification (month 5+)
Goal: turn the top 5% of referrers into an advocacy channel.
1. Identify top referrers and contact them personally
2. Offer early access, ambassador status or a product-input role
3. Launch a tiered reward structure (see [program-examples.md](program-examples.md))
4. Run periodic referral challenges for the top referrers

---

## Affiliate Metrics

| Metric | Formula | Rule of thumb |
|--------|---------|---------------|
| Active affiliate rate | Active affiliates / enrolled affiliates | 20-40% |
| Revenue per active affiliate | Affiliate revenue / active affiliates | Varies by niche |
| Affiliate CAC | Commission paid / new customers via affiliates | Below standard CAC |
| Top-affiliate concentration | Revenue share of the top 20% of affiliates | 80%+ is normal (see the 20/80 rule in [viral-mechanisms.md](viral-mechanisms.md)) |
| Click-to-conversion time | Days from click to first payment | Compare with your sales cycle |

**Concentration risk:** if one or two partners bring more than 80% of affiliate revenue, losing one of them can empty the channel. Recruit and activate more partners before that happens.

---

## Weekly Report Template

```
REFERRAL PROGRAM — Week of [date]

Active referrers: X (up/down vs. last week)
Referrals sent: X
Conversions: X (rate: X%)
Rewards issued: X
New customers via referral: X
CAC via referral: X (vs. X paid CAC)

TOP THIS WEEK:
- [Name or segment] sent 12 referrals, 4 converted
- [Test name] shows +18% active referrers

ISSUES:
- [What's broken and the plan to fix it]

NEXT ACTION:
- [One thing we do this week to improve the program]
```
