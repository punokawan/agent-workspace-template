---
name: churn-prevention
description: "Reduces voluntary and involuntary churn: cancel flows with exit surveys and reason-matched save offers, churn-risk signals and health scores, dunning and failed-payment recovery, and churn metrics; sizes the revenue at stake with a script. Use when the user wants to reduce churn, build or audit a cancellation flow, set up save offers, recover failed payments, or implement retention strategies. Also use when the user mentions 'churn,' 'cancel flow,' 'offboarding,' 'save offer,' 'dunning,' 'failed payment recovery,' 'win-back,' 'retention,' 'exit survey,' 'pause subscription,' 'involuntary churn,' 'people keep canceling,' 'churn rate is too high,' 'how do I keep users,' or 'customers are leaving,' 'how much revenue are we losing to churn,' or 'failed payments are killing us.' Use this whenever someone is losing subscribers or wants to build systems to prevent it. For post-cancel win-back email sequences, see emails. For in-app upgrade paywalls, see paywalls."
metadata:
  version: 1.0.0
  sources: "corey:churn-prevention@96798cf; ali:churn-prevention@8f08254"
---

# Churn Prevention

You are an expert in SaaS retention and churn prevention. Your goal is to help reduce both voluntary churn (customers choosing to cancel) and involuntary churn (failed payments) through well-designed cancel flows, dynamic save offers, proactive retention, and dunning strategies.

## Before Starting

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Current Churn Situation
- What's your monthly churn rate? (Voluntary vs. involuntary if known)
- How many active subscribers?
- What's the average MRR per customer?
- Do you have a cancel flow today, or does cancel happen instantly?

### 2. Billing & Platform
- What billing provider? (Stripe, Chargebee, Paddle, Recurly, Braintree)
- Monthly, annual, or both billing intervals?
- Do you support plan pausing or downgrades?
- Any existing retention tooling? (Churnkey, ProsperStack, Raaft)

### 3. Product & Usage Data
- Do you track feature usage per user?
- Can you identify engagement drop-offs?
- Do you have cancellation reason data from past churns?
- What's your activation metric? (What do retained users do that churned users don't?)

### 4. Constraints
- B2B or B2C? (Affects flow design)
- Self-serve cancellation required? (Some regulations mandate easy cancel)
- Brand tone for offboarding? (Empathetic, direct, playful)
- Save-offer budget: which discounts, pauses, extensions or support time can you give?
- Primary problem: too many cancellations, or failed payments?

Amounts in this skill are illustrations. Use the user's currency and market.

---

## How This Skill Works

Churn has two types requiring different strategies:

| Type | Cause | Solution |
|------|-------|----------|
| **Voluntary** | Customer chooses to cancel | Cancel flows, save offers, exit surveys |
| **Involuntary** | Payment fails | Dunning emails, smart retries, card updaters |

Voluntary churn is typically 50-70% of total churn. Involuntary churn is 30-50% but is often easier to fix.

This skill supports three modes:

1. **Build a cancel flow** — Design from scratch with survey, save offers, and confirmation
2. **Optimize an existing flow** — Analyze cancel data and improve save rates
3. **Set up dunning** — Failed payment recovery with retries and email sequences

Before you choose a mode, size the revenue at stake with the calculator (see Size the Revenue at Stake). It shows which lever is worth more: save rate or recovery rate. For an audit (mode 2), score the current flow with the audit rubric in [references/cancel-flow-templates.md](references/cancel-flow-templates.md) and fix the lowest-scoring dimensions first.

---

## Cancel Flow Design

### The Cancel Flow Structure

Every cancel flow follows this sequence:

```
Trigger → Survey → Dynamic Offer → Confirmation → Post-Cancel
```

**Step 1: Trigger**
Customer clicks "Cancel subscription" in account settings.

**Step 2: Exit Survey**
Ask why they're cancelling. This determines which save offer to show.

**Step 3: Dynamic Save Offer**
Present a targeted offer based on their reason (discount, pause, downgrade, etc.)

**Step 4: Confirmation**
If they still want to cancel, confirm clearly with end-of-billing-period messaging.

**Step 5: Post-Cancel**
Set expectations, offer easy reactivation path, trigger win-back sequence.

### Flow Rules

- **Cancel is easy to find.** Put it in billing settings; a support ticket or phone call as the only path is a dark pattern.
- **One required survey question.** Collect the reason before you show an offer, because the reason picks the offer. Optional free text, never required.
- **Each reason maps to one primary offer.** An ambiguous mapping turns into a generic discount and a low save rate.
- **One primary offer per attempt.** A secondary option (for example a downgrade link) is fine; a wall of offers is not. If they decline, go straight to confirmation.
- **Do not repeat a declined offer** if the same customer returns to cancel within 30 days.
- **Confirmation states the facts:** the exact access end date, how long data is kept, how to reactivate. Explicit "Yes, cancel" button, no pre-checked boxes.
- **Record every attempt:** `cancel_reason`, `save_offer_shown`, `save_offer_accepted` per customer, so save rate and offer performance can be measured.

Copy templates for every stage (intercept, survey, offer, confirmation, post-cancel emails) are in [references/cancel-flow-templates.md](references/cancel-flow-templates.md).

### Exit Survey Design

The exit survey is the foundation. Good reason categories:

| Reason | What It Tells You |
|--------|-------------------|
| Too expensive | Price sensitivity, may respond to discount or downgrade |
| Not using it enough | Low engagement, may respond to pause or onboarding help |
| Missing a feature | Product gap, show roadmap or workaround |
| Switching to competitor | Competitive pressure, understand what they offer |
| Technical issues / bugs | Product quality, escalate to support |
| Temporary / seasonal need | Usage pattern, offer pause |
| Business closed / changed | Unavoidable, learn and let go gracefully |
| Other | Catch-all, include free text field |

**Survey best practices:**
- 1 question, single-select with optional free text
- 5-8 reason options max (avoid decision fatigue)
- Put most common reasons first (review data quarterly)
- Don't make it feel like a guilt trip
- "Help us improve" framing works better than "Why are you leaving?"

### Dynamic Save Offers

The key insight: **match the offer to the reason.** A discount won't save someone who isn't using the product. A feature roadmap won't save someone who can't afford it.

**Offer-to-reason mapping:**

| Cancel Reason | Primary Offer | Fallback Offer |
|---------------|---------------|----------------|
| Too expensive | Discount (20-30% for 2-3 months) | Downgrade to lower plan |
| Not using it enough | Pause (1-3 months) | Free onboarding session |
| Missing feature | Roadmap preview + timeline | Workaround guide |
| Switching to competitor | Competitive comparison + discount | Feedback session |
| Technical issues | Escalate to support immediately | Credit + priority fix |
| Temporary / seasonal | Pause subscription | Downgrade temporarily |
| Too complicated | Free onboarding session | 1:1 support call |
| Business closed | Skip offer (respect the situation) | — |
| Just testing / wrong fit | Skip offer (let them go) | — |

### When Not to Use Each Offer

| Offer | Use for | Do not use for |
|-------|---------|----------------|
| Discount | Price objection | Adoption or feature issues |
| Pause | Seasonal need, project ended, low use | Price objection |
| Downgrade | Too expensive, light usage | Feature objection |
| Extended trial / feature unlock | Has not explored the full value; the feature exists on a higher plan | Power user who is churning |
| Human support | Complicated, stuck, frustrated | Price objection (support time does not fix price) |

**Offer presentation:** one headline ("Before you go — [offer]"), the value as an amount ("Save [amount]", not "Get a discount"), and two clear buttons ("Claim this offer" and "Continue cancelling"). Use a countdown only when the offer really expires.

### Save Offer Types

**Discount**
- 20-30% off for 2-3 months is the sweet spot
- Avoid 50%+ discounts (trains customers to cancel for deals)
- Time-limit the offer ("This offer expires when you leave this page")
- Show the amount saved, not just the percentage

**Pause subscription**
- 1-3 month pause maximum (longer pauses rarely reactivate)
- 60-80% of pausers eventually return to active
- Auto-reactivation with advance notice email
- Keep their data and settings intact

**Plan downgrade**
- Offer a lower tier instead of full cancellation
- Show what they keep vs. what they lose
- Position as "right-size your plan" not "downgrade"
- Easy path back up when ready

**Feature unlock / extension**
- Unlock a premium feature they haven't tried
- Extend trial of a higher tier
- Works best for "not getting enough value" reasons

**Personal outreach**
- For high-value accounts (top 10-20% by MRR)
- Route to customer success for a call
- Personal email from founder for smaller companies

### Cancel Flow UI Patterns

```
┌─────────────────────────────────────┐
│  We're sorry to see you go          │
│                                     │
│  What's the main reason you're      │
│  cancelling?                        │
│                                     │
│  ○ Too expensive                    │
│  ○ Not using it enough              │
│  ○ Missing a feature I need         │
│  ○ Switching to another tool        │
│  ○ Technical issues                 │
│  ○ Temporary / don't need right now │
│  ○ Other: [____________]            │
│                                     │
│  [Continue]                         │
│  [Never mind, keep my subscription] │
└─────────────────────────────────────┘
         ↓ (selects "Too expensive")
┌─────────────────────────────────────┐
│  What if we could help?             │
│                                     │
│  We'd love to keep you. Here's a    │
│  special offer:                     │
│                                     │
│  ┌───────────────────────────────┐  │
│  │  25% off for the next 3 months│  │
│  │  Save [amount]/month          │  │
│  │                               │  │
│  │  [Accept Offer]               │  │
│  └───────────────────────────────┘  │
│                                     │
│  Or switch to [Basic Plan] at       │
│  [price]/month →                    │
│                                     │
│  [No thanks, continue cancelling]   │
└─────────────────────────────────────┘
```

**UI principles:**
- Keep the "continue cancelling" option visible (no dark patterns)
- One primary offer + one fallback, not a wall of options
- Show specific savings amounts, not abstract percentages
- Use the customer's name and account data when possible
- Mobile-friendly (many cancellations happen on mobile)

For detailed cancel flow patterns by industry and billing provider, see [references/cancel-flow-patterns.md](references/cancel-flow-patterns.md).

---

## Churn Prediction & Proactive Retention

The best save happens before the customer ever clicks "Cancel."

### Risk Signals

Track these leading indicators of churn:

| Signal | Risk Level | Timeframe |
|--------|-----------|-----------|
| Login frequency drops 50%+ | High | 2-4 weeks before cancel |
| Key feature usage stops | High | 1-3 weeks before cancel |
| Support tickets spike then stop | High | 1-2 weeks before cancel |
| Email open rates decline | Medium | 2-6 weeks before cancel |
| Billing page visits increase | High | Days before cancel |
| Team seats removed | High | 1-2 weeks before cancel |
| Data export initiated | Critical | Days before cancel |
| Individual recommendation rating is 0–6 (detractor) | Medium | 1-3 months before cancel |

### Health Score Model

Build a simple health score (0-100) from weighted signals. Define every component on the **same 0–100 scale**, where higher means healthier, before applying weights. Use documented product-specific mappings for raw usage, sentiment, and billing values; do not add login counts, a 1–5 sentiment rating, and a percentage directly. The weights below are an illustrative starting point, not validated churn predictions.

Treat missing or stale signals as unavailable, rather than automatically healthy or zero. Set freshness windows and a minimum coverage policy before using the score. If the policy permits a partial score, compute `sum(weight × observed score) / sum(observed weights)` and report coverage (the sum of observed weights) alongside it; otherwise return “insufficient data.” All unavailable means no score. For example, only login (80) and feature usage (60) produce `(0.30×80 + 0.25×60)/0.55 = 70.91`, with 55% coverage. Do not promote that partial score into a healthy-account action without meeting the coverage policy.

An individual rating of 0–6 is a detractor; aggregate NPS (−100 to 100) is a different measure.

[Gainsight's measure-weight documentation](https://support.gainsight.com/gainsight_nxt/05Scorecards/02Admin_Guides/Measure_Weights_in_Scorecards) explains redistribution for unavailable measures.

Illustrative complete-data model:

```
Health Score = (
  Login frequency score × 0.30 +
  Feature usage score   × 0.25 +
  Support sentiment     × 0.15 +
  Billing health        × 0.15 +
  Engagement score      × 0.15
)
```

Validate score mappings and intervention thresholds against later observed renewal/churn outcomes before operational use; the following tiers are illustrative.

| Score | Status | Action |
|-------|--------|--------|
| 80-100 | Healthy | Upsell opportunities |
| 60-79 | Needs attention | Proactive check-in |
| 40-59 | At risk | Intervention campaign |
| 0-39 | Critical | Personal outreach |

### Proactive Interventions

**Before they think about cancelling:**

| Trigger | Intervention |
|---------|-------------|
| Usage drop >50% for 2 weeks | "We noticed you haven't used [feature]. Need help?" email |
| Approaching plan limit | Upgrade nudge (not a wall — paywalls handles this) |
| No login for 14 days | Re-engagement email with recent product updates |
| NPS detractor (0-6) | Personal follow-up within 24 hours |
| Support ticket unresolved >48h | Escalation + proactive status update |
| Annual renewal in 30 days | Value recap email + renewal confirmation |

---

## Involuntary Churn: Payment Recovery

Failed payments cause 30-50% of all churn but are the most recoverable.

### The Dunning Stack

```
Pre-dunning → Smart retry → Dunning emails → Grace period → Hard cancel
```

### Pre-Dunning (Prevent Failures)

- **Card expiry alerts**: Email 30, 15, and 7 days before card expires
- **Backup payment method**: Prompt for a second payment method at signup
- **Card updater services**: Visa/Mastercard auto-update programs (reduces hard declines 30-50%)
- **Pre-billing notification**: Email 3-5 days before charge for annual plans

### Smart Retry Logic

Not all failures are the same. Retry strategy by decline type:

| Decline Type | Examples | Retry Strategy |
|-------------|----------|----------------|
| Soft decline (temporary) | Insufficient funds, processor timeout | Retry 3-5 times over 7-10 days |
| Hard decline (permanent) | Card stolen, account closed | Don't retry — ask for new card |
| Authentication required | 3D Secure, SCA | Send customer to update payment |

**Retry timing best practices:**
- Retry 1: 24 hours after failure
- Retry 2: 3 days after failure
- Retry 3: 5 days after failure
- Retry 4: 7 days after failure (with dunning email escalation)
- After 4 retries: Hard cancel with reactivation path

**Smart retry tip:** Retry on the day of the month the payment originally succeeded (if Day 1 worked before, retry on Day 1). Stripe Smart Retries handles this automatically.

### Dunning Email Sequence

| Email | Timing | Tone | Content |
|-------|--------|------|---------|
| 1 | Day 0 (failure) | Friendly alert | "Your payment didn't go through. Update your card." |
| 2 | Day 3 | Helpful reminder | "Quick reminder — update your payment to keep access." |
| 3 | Day 7 | Urgency | "Your account will be paused in 3 days. Update now." |
| 4 | Day 10 | Final warning | "Last chance to keep your account active." |

**Dunning email best practices:**
- Direct link to payment update page (no login required if possible)
- Show what they'll lose (their data, their team's access)
- Don't blame ("your payment failed" not "you failed to pay")
- Include support contact for help
- Plain text performs better than designed emails for dunning

### Recovery Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| Soft decline recovery | <40% | 50-60% | 70%+ |
| Hard decline recovery | <10% | 20-30% | 40%+ |
| Overall payment recovery | <30% | 40-50% | 60%+ |
| Pre-dunning prevention | None | 10-15% | 20-30% |

For the complete dunning playbook with provider-specific setup, see [references/dunning-playbook.md](references/dunning-playbook.md).

---

## Metrics & Measurement

### Key Churn Metrics

| Metric | Formula | Target |
|--------|---------|--------|
| Monthly churn rate | Churned customers / Start-of-month customers | <5% B2C, <2% B2B |
| Revenue churn (net) | (Lost MRR - Expansion MRR) / Start MRR | Negative (net expansion) |
| Cancel flow save rate | Saved / Total cancel sessions | 25-35% |
| Offer acceptance rate | Accepted offers / Shown offers | 15-25% |
| Pause reactivation rate | Reactivated / Total paused | 60-80% |
| Dunning recovery rate | Recovered / Total failed payments | 50-60% |
| Time to cancel | Days from first churn signal to cancel | Track trend |
| Exit survey completion | Surveys completed / Cancel sessions | >80% |
| Win-back rate | Reactivations within 90 days / Cancellations | 5-10% |

Save-rate and recovery-rate benchmarks vary by source: a save rate of 10-15% is a common "good" bar and 25-35% a mature-flow target; dunning recovery is cited from 25-40% up to 50-60%. Vendor-reported figures skew high. Set targets from the user's own baseline.

**Red flags:**
- Save rate below 5% → offers do not match reasons
- Exit survey completion below 70% → survey too long or optional
- Payment recovery below 20% → retry logic or dunning emails need work

### Cohort Analysis

Segment churn by:
- **Acquisition channel** — Which channels bring stickier customers?
- **Plan type** — Which plans churn most?
- **Tenure** — When do most cancellations happen? (30, 60, 90 days?)
- **Cancel reason** — Which reasons are growing?
- **Save offer type** — Which offers work best for which segments?

### Cancel Flow A/B Tests

Test one variable at a time:

| Test | Hypothesis | Metric |
|------|-----------|--------|
| Discount % (20% vs 30%) | Higher discount saves more | Save rate, LTV impact |
| Pause duration (1 vs 3 months) | Longer pause increases return rate | Reactivation rate |
| Survey placement (before vs after offer) | Survey-first personalizes offers | Save rate |
| Offer presentation (modal vs full page) | Full page gets more attention | Save rate |
| Copy tone (empathetic vs direct) | Empathetic reduces friction | Save rate |

**How to run cancel flow experiments:** Use the **ab-testing** skill to design statistically rigorous tests. PostHog is a good fit for cancel flow experiments — its feature flags can split users into different flows server-side, and its funnel analytics track each step of the cancel flow (survey → offer → accept/decline → confirm). See the [PostHog integration guide](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/posthog.md) for setup.

---

## Size the Revenue at Stake

`scripts/churn_impact_calculator.py` (Python 3, standard library only) sizes the MRR kept by raising the cancel-flow save rate and the dunning recovery rate. It prints to the terminal and writes no files.

```bash
python3 scripts/churn_impact_calculator.py --sample                    # see the input shape and report
python3 scripts/churn_impact_calculator.py churn.json --currency "<code>"   # label amounts
python3 scripts/churn_impact_calculator.py churn.json --json           # machine-readable
```

Inputs are documented at the top of the script: MRR, observed monthly churn, the voluntary share, and current and target save and recovery rates; optionally average MRR per customer, gross margin and the churn of saved customers. It reports the extra MRR kept per month by each lever, the churn rate after, the revenue retained over the window, and which lever to fix first.

Saved customers often churn again sooner. The script uses the observed churn rate for them unless `post_save_monthly_churn_pct` is given; set it from data where you have it and say which you used. Target rates are **assumptions** until a test confirms them.

---

## Proactive Flags

Raise these without being asked:

- **Instant cancellation, no flow** → revenue leaks at every cancel; even one survey question and one offer saves some. Priority fix.
- **One generic discount for everyone** → depresses revenue and trains customers to wait for deals. Map offers to reasons.
- **No dunning sequence** → failed payments cancel silently; that is often a third or more of churn. Flag immediately.
- **Optional exit survey** → completion drops and the data stops being usable. Make it one required question.
- **No post-cancel reactivation email** → the first week after cancel is the strongest win-back moment.
- **Monthly churn above 5%** (B2B) → retention work alone will not fix it; flag a product and ICP review alongside it.

---

## Common Mistakes

- **No cancel flow at all** — Instant cancel leaves money on the table. Even a simple survey + one offer saves 10-15%
- **Making cancellation hard to find** — Hidden cancel buttons breed resentment and bad reviews. Many jurisdictions require easy online cancellation; check the rules where the customers live (see Compliance Notes in [references/cancel-flow-patterns.md](references/cancel-flow-patterns.md))
- **Same offer for every reason** — A blanket discount doesn't address "missing feature" or "not using it"
- **Discounts too deep** — 50%+ discounts train customers to cancel-and-return for deals
- **Ignoring involuntary churn** — Often 30-50% of total churn and the easiest to fix
- **No dunning emails** — Letting payment failures silently cancel accounts
- **Guilt-trip copy** — "Are you sure you want to abandon us?" damages brand trust
- **Not tracking save offer LTV** — A "saved" customer who churns 30 days later wasn't really saved
- **Pausing too long** — Pauses beyond 3 months rarely reactivate. Set limits.
- **No post-cancel path** — Make reactivation easy and trigger win-back emails, because some churned users will want to come back

---

## Deliverables

| Request | Deliver |
|---------|---------|
| Design a cancel flow | Five-stage flow with copy per stage, reason-to-offer map, confirmation email |
| Audit a cancel flow | Audit rubric scores, the user's metrics against benchmarks, prioritized fixes |
| Set up dunning | Retry schedule by decline type, email sequence with subject lines and body copy, card updater checklist |
| Design an exit survey | 5-8 reasons, each mapped to one primary offer |
| Size churn impact | `scripts/churn_impact_calculator.py` output with its assumptions stated |
| Proactive retention | Risk signals, health score model and interventions for the product |

Lead with the revenue at stake or the expected save and recovery rate, then the method. Give each recommendation an owner and a date. Label each number as measured (the user's data), cited benchmark, or assumption.

---

## Tool Integrations

For implementation, see the [tools registry](https://github.com/coreyhaines31/marketingskills/blob/main/tools/REGISTRY.md).

### Retention Platforms

| Tool | Best For | Key Feature |
|------|----------|-------------|
| **Churnkey** | Full cancel flow + dunning | AI-powered adaptive offers, 34% avg save rate |
| **ProsperStack** | Cancel flows with analytics | Advanced rules engine, Stripe/Chargebee integration |
| **Raaft** | Simple cancel flow builder | Easy setup, good for early-stage |
| **Chargebee Retention** | Chargebee customers | Native integration, was Brightback |

### Billing Providers (Dunning)

| Provider | Smart Retries | Dunning Emails | Card Updater |
|----------|:------------:|:--------------:|:------------:|
| **Stripe** | Built-in (Smart Retries) | Built-in | Automatic |
| **Chargebee** | Built-in | Built-in | Via gateway |
| **Paddle** | Built-in | Built-in | Managed |
| **Recurly** | Built-in | Built-in | Built-in |
| **Braintree** | Manual config | Manual | Via gateway |

### Related CLI Tools

| Tool | Use For |
|------|---------|
| `stripe` | Subscription management, dunning config, payment retries |
| `customer-io` | Dunning email sequences, retention campaigns |
| `posthog` | Cancel flow A/B tests via feature flags, funnel analytics |
| `mixpanel` / `ga4` | Usage tracking, churn signal analysis |
| `segment` | Event routing for health scoring |

---

## Related Skills

- **emails**: For win-back email sequences after cancellation
- **paywalls**: For in-app upgrade moments and trial expiration
- **pricing**: For plan structure and annual discount strategy
- **onboarding**: For activation to prevent early churn
- **analytics**: For setting up churn signal events
- **ab-testing**: For testing cancel flow variations with statistical rigor
- Dunning emails stay in this skill; lifecycle and onboarding sequences go to **emails**
- When the root cause of churn is pricing or packaging, use **pricing**; save-offer design stays here

Sources and credits: [SOURCES.md](SOURCES.md)
