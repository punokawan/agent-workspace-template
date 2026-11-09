---
name: pricing
description: "Designs and audits pricing: value metric, packaging and tiers, price points, free plan or trial, price increases, and pricing-page teardowns for human buyers and AI agents; models price-change scenarios with a script. Use when someone is deciding what to charge, structuring plans, raising prices, or reviewing a pricing page. Also use when the user mentions 'pricing,' 'pricing tiers,' 'freemium,' 'free trial,' 'packaging,' 'price increase,' 'value metric,' 'Van Westendorp,' 'willingness to pay,' 'monetization,' 'how much should I charge,' 'my pricing is wrong,' 'pricing page,' 'annual vs monthly,' 'per seat pricing,' 'should I offer a free plan,' 'pricing page audit,' 'can AI read my pricing,' or 'model pricing scenarios.' For in-app upgrade screens, see paywalls. For offer construction (bonuses, guarantees, value framing, naming) on services, courses, coaching or high-ticket B2B, see offers."
metadata:
  version: 1.0.0
  sources: "corey:pricing@96798cf; ali:pricing-strategy@8f08254"
---

# Pricing Strategy

You are an expert in SaaS pricing and monetization strategy. Your goal is to help design pricing that captures value, drives growth, and aligns with customer willingness to pay.

## Before Starting

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Business Context
- What type of product? (SaaS, marketplace, e-commerce, service)
- What's your current pricing (if any)?
- What's your target market? (SMB, mid-market, enterprise)
- What's your go-to-market motion? (self-serve, sales-led, hybrid)

### 2. Value & Competition
- What's the primary value you deliver?
- What alternatives do customers consider?
- How do competitors price?

### 3. Current Performance
- What's your current conversion rate?
- What's your ARPU and churn rate?
- What does it cost to serve one customer per month? (sets the price floor)
- Any feedback on pricing from customers/prospects?

### 4. Goals
- Optimizing for growth, revenue, or profitability?
- Moving upmarket or expanding downmarket?
- Any constraints? (grandfathered customers, contract terms, channel-partner margins)

Work in the user's currency and market. Dollar amounts in this skill and its references are illustrations, not defaults.

---

## How This Skill Works

Pick the mode from the request, then work the sections it names:

| Mode | Use when | Work through |
|------|----------|--------------|
| **Design** | No pricing yet, or a full rebuild | Initial Pricing → Value Metrics → Tier Structure → Pricing Research |
| **Optimize** | Pricing exists, but conversion, expansion or fit is off | Proactive Flags → Pricing Research → Tier Structure |
| **Raise prices** | Value, costs or positioning have moved | When to Raise Prices → Model the Scenarios |
| **Audit the page** | The page is the problem, not the price | Pricing Page Best Practices → Pricing Page Teardown |

Decide the three axes in order: **value metric first, then packaging, then the price point.** Most teams start with the number; that is backwards, because a number means little until the metric and the packages are fixed.

---

## Pricing Fundamentals

### The Three Pricing Axes

**1. Packaging** — What's included at each tier?
- Features, limits, support level
- How tiers differ from each other

**2. Pricing Metric** — What do you charge for?
- Per user, per usage, flat fee
- How price scales with value

**3. Price Point** — How much do you charge?
- The actual dollar amounts
- Perceived value vs. cost

### Value-Based Pricing

Price should be based on value delivered, not cost to serve:

- **Customer's perceived value** — The ceiling
- **Your price** — Between alternatives and perceived value
- **Next best alternative** — The floor for differentiation
- **Your cost to serve** — Only a baseline, not the basis

**Key insight:** Price between the next best alternative and perceived value.

**Don't anchor on the wrong things:**
- **Not competitor-based** — matching a competitor's price copies their strategy, not their economics. It's a data point, not a target.
- **Not cost-based** — cost is a floor, never the basis. Value + differentiation set the price.

### Quantify the Value

Put numbers on both ends of the range before you pick a price:

1. **Next best alternative** — what the customer would do without you (a competitor, a spreadsheet, a manual process, a hire) and what that costs them.
2. **Value delivered** — time saved × the user's loaded hourly cost, revenue gained or protected, and the cost of errors or risk avoided. Ask your best customers: "What would you lose if you stopped using us tomorrow?"
3. **Price inside the range** — a common heuristic is 10–20% of documented value (the 10:1 value/price ratio in [references/pricing-models.md](references/pricing-models.md) is the low end). Near 50% of value, customers feel they overpay; below the next best alternative, you signal that you don't believe in the product.

---

## Initial Pricing — "Pick a Price You Can Learn From"

The frameworks below (value metrics, tiers, Van Westendorp) are for optimizing a price. **On day one you don't have a price to optimize — you have a bet to place.** The goal of your first price is *learning*, not precision. Pick a number, ship it, and let real buyers tell you if it's wrong.

### The $10 / $100 / $1,000 rule of thumb

When you have nothing to go on, start with the order of magnitude that matches who you serve:

- **~$10/mo** — prosumer / individual, high volume, low touch
- **~$100/mo** — SMB / team tool, the SaaS default
- **~$1,000/mo** — mid-market / business-critical / sales-assisted

Pick the bucket by **who the customer is and how much value you deliver**, then start near the round number. You can move within the bucket fast once you have signal.

### Avoid the $9 trap

Resist the urge to price ultra-low (e.g. **$9/mo**) to reduce friction. Ultra-low pricing:
- Creates **false traction** — signups that look like validation but come from people who'd never pay a real price
- **Traps you** — it's far harder to raise a price 5–10x later than to have started higher, and your cheapest customers churn most and complain loudest (see [references/pricing-models.md](references/pricing-models.md) on low-price retention)

Round-and-slightly-higher beats clever-and-cheap.

### "Just charge $50 and see what happens"

When early Intercom agonized over pricing, Jason Fried's advice was essentially: **just charge $50 and see what happens.** Stop modeling; get a real signal. If people pay without flinching, raise it. If nobody bites, you've learned something for the cost of a week, not a quarter.

**For the eight ways to structure how you charge (flat, usage, tier, user, feature, credit, outcome, hybrid) and the value/price ratio:** See [references/pricing-models.md](references/pricing-models.md).

---

## Value Metrics

### What is a Value Metric?

The value metric is what you charge for—it should scale with the value customers receive.

**Good value metrics:**
- Align price with value delivered
- Are easy to understand
- Scale as customer grows
- Are hard to game

### Common Value Metrics

| Metric | Best For | Example |
|--------|----------|---------|
| Per user/seat | Collaboration tools | Slack, Notion |
| Per usage | Variable consumption | AWS, Twilio |
| Per feature | Modular products | HubSpot add-ons |
| Per contact/record | CRM, email tools | Mailchimp |
| Per transaction | Payments, marketplaces | Stripe |
| Flat fee | Simple products | Basecamp |

### Choosing Your Value Metric

Ask: "As a customer uses more of [metric], do they get more value?"
- If yes → good value metric
- If no → price doesn't align with value

**Red flags:**
- Per-seat pricing where one power user does the work and the team only views results — seats don't track value
- A flat fee when some customers get 10× the value of others — light users subsidize heavy users
- Per-call or per-event pricing when usage swings week to week — unpredictable bills push customers to cap usage or churn

**The value metric picks the pricing model.** Once you know what scales with value, choose how to charge on it — flat, usage, tier, user, feature, credit, outcome, or a hybrid. See [references/pricing-models.md](references/pricing-models.md).

---

## Tier Structure Overview

### Good-Better-Best Framework

**Good tier (Entry):** Core features, limited usage, low price
**Better tier (Recommended):** Full features, reasonable limits, anchor price
**Best tier (Premium):** Everything, advanced features, 2-3x Better price

**Tier rules of thumb:**
- The entry tier is **not** a free plan. Free is a separate acquisition decision (freemium or trial); see [references/tier-structure.md](references/tier-structure.md).
- Price the entry tier at or above your cost floor. It serves the segment that would churn at a higher price.
- Better is commonly 2-3x Good. Mark it as recommended; it is where you push most customers.
- Best holds what larger customers need: SSO, audit logs, SLA, dedicated support, custom contracts. It can be "Contact us" once deal sizes justify a sales conversation.

### Tier Differentiation

- **Feature gating** — Basic vs. advanced features
- **Usage limits** — Same features, different limits
- **Support level** — Email → Priority → Dedicated
- **Access** — API, SSO, custom branding

**For detailed tier structures and persona-based packaging**: See [references/tier-structure.md](references/tier-structure.md)

---

## Pricing Research

### Van Westendorp Method

Four questions that identify acceptable price range:
1. Too expensive (wouldn't consider)
2. Too cheap (question quality)
3. Expensive but might consider
4. A bargain

Use intersections to identify perceived price acceptability and candidate prices to test. The named "Optimal Price Point" is a survey intersection, not proof of revenue or profit maximization. The four questions alone do not estimate conversion, churn or demand at a new price.

### MaxDiff Analysis

Identifies which features customers value most:
- Show sets of features
- Ask: Most important? Least important?
- Results inform tier packaging

### Competitor Benchmark

Record what real alternatives charge, what each price includes, and where you over- or under-deliver against each. Use it as positioning input, not as a target.

**For detailed research methods, including the competitor benchmark steps**: See [references/research-methods.md](references/research-methods.md)

---

## When to Raise Prices

### Signs It's Time

**Market signals:**
- Competitors have raised prices
- Prospects don't flinch at price
- "It's so cheap!" feedback

**Business signals:**
- Very high conversion rates (>40%)
- Very low churn (<3% monthly)
- Strong unit economics
- Price unchanged for 2+ years while costs and delivered value rose

**Product signals:**
- Significant value added since last pricing
- Product more mature/stable

**Fix churn first.** If monthly churn is above ~5%, an increase speeds up the customers already leaving. Work the churn-prevention skill before raising prices.

### Price Increase Strategies

| Strategy | Use when | Risk |
|----------|----------|------|
| **Grandfather existing** — new price for new customers only | Strong pushback is likely, or you want a clean market read first | Low — the existing base is untouched |
| **Delayed increase** — announce 3-6 months out | Loyal base, contract risk | Medium — customers feel respected |
| **Tied to value** — raise the price, add features | Clear new value has shipped | Low — easy to justify |
| **Plan restructure** — change plans entirely | Packaging no longer fits the segments | Medium — migration complexity |
| **Uniform increase** — everyone moves at once | Price is clearly below market and value is proven | Medium-high |

### Rollout Methodology

A price change is a rollout, not a switch you flip. Sequence it to de-risk:

1. **Test on new customers first.** Raise the price only for *new* signups and watch conversion. New customers have no anchor and no relationship at stake, so they give you a clean read on whether the market accepts the number — before you touch a single existing account.
2. **Don't reflexively grandfather forever.** Grandfathering feels kind, but it can leave enormous money on the table. Run the math: a customer paying **$50/mo** who *should* be at **$250/mo** is a **$2,400/yr** gap — and $200/mo you're subsidizing indefinitely across your whole base. Grandfather as a *transition* (a grace period), not a permanent exemption.
3. **Roll out small, then gradually.** Move **5–10%** of existing customers to the new price first. Watch churn and support volume for a cycle, then expand in staggered waves. A staggered rollout contains the blast radius and gives you an off-ramp if churn spikes.
4. **Communicate the *why*, months ahead, with a generous offer.** Tell customers why the price is changing (usually: more value shipped) well in advance. Soften it: lock-in-the-old-price-if-you-upgrade-to-annual-now, an extended grace window, or a one-time credit. Advance notice + a generous option converts a resentment moment into a loyalty one.

**Before the first wave:**
- **Quantify the move.** Model existing-base MRR at 100%, 90%, 80% and 70% retention. An increase of *x* loses money on the existing base only if more than *x*/(1+*x*) of it leaves (20% for a 25% increase). See Model the Scenarios.
- **Segment by risk.** Annual contracts, champions vs. detractors, accounts already showing churn signals.
- **Set the notice period.** Commonly 60-90 days for existing customers and never under 30; contracts and local consumer rules can require more.
- **Brief support and success.** FAQ, talking points, and clear authority over which offers they may make.

**After each wave:** watch churn, downgrades and support volume for at least 60 days. A 20-30% increase often costs 5-15% of the affected customers (a rule of thumb, not a benchmark); continue while net revenue impact stays positive.

Expect — and accept — some churn. The customers most likely to leave over a justified increase are usually your least-profitable, highest-support, most price-sensitive accounts.

---

## Model the Scenarios

`scripts/pricing_modeler.py` (Python 3, standard library only) turns current plans into revenue projections for price changes, a cost floor, a market position and a sanity tier ladder. It prints to the terminal and writes no files.

```bash
python3 scripts/pricing_modeler.py --sample                   # see the input shape and report
python3 scripts/pricing_modeler.py pricing.json --currency "<code>"   # label amounts
python3 scripts/pricing_modeler.py pricing.json --json        # machine-readable
```

Inputs are documented at the top of the script: current plans with prices and customer counts, monthly new customers and churn, and optionally the trial-to-paid rate, competitor prices, cost to serve and the price changes to test. For each change it reports revenue over the window when applied to everyone and to new customers only, plus the break-even churn.

The one-time churn after an increase is an **assumption** (`increase_churn_leak`, default 0.25 of the increase). Replace it with data from a past change or a small first wave, and say so when you present the numbers. The ladder is a sanity check from cost and competitor prices, not a recommendation; set prices from value research.

---

## Pricing Page Best Practices

### Above the Fold
- Clear tier comparison table
- Recommended tier highlighted
- Monthly/annual toggle
- Primary CTA for each tier

### Common Elements
- Feature comparison table
- Who each tier is for
- FAQ section that answers the buying objections: cancel anytime, what happens at limits, refunds, data security, switching plans
- Annual discount callout (17-20%)
- Money-back guarantee
- Customer logos/trust signals
- Security and compliance badges for B2B buyers (only the ones you hold)

### Annual vs. Monthly Toggle
- Default to annual (or highlight it) when you prefer annual billing; it raises take-up and LTV
- State the saving outright: "Save 20%" or "2 months free"
- Never hide the monthly price; hiding it builds distrust

### Pricing Psychology
- **Anchoring:** Show higher-priced option first
- **Decoy effect:** Middle tier should be best value
- **Charm pricing:** $49 vs. $50 (for value-focused)
- **Round pricing:** $50 vs. $49 (for premium)

**For page structure, plan-card anatomy, plan names, CTA and price-display copy, and pricing-page test ideas**: See [references/pricing-page-design.md](references/pricing-page-design.md)

---

## Pricing Page Teardown

When someone wants to audit an existing pricing *page* for **clarity, transparency, and AI-readability** (not the pricing strategy itself, and not conversion-rate optimization — that's `cro`), run a **teardown** that scores it across two axes and returns prioritized fixes:

- **Human buyer experience** — value-prop clarity, plan differentiation, cognitive load, trust signals, pricing psychology, and price transparency.
- **AI-agent readiness** — whether the LLMs and agents that increasingly shortlist and compare tools can actually read and quote your pricing: machine-readable prices (not locked in an image or behind "Contact us"), extractable FAQ/objection coverage, per-tier depth stated in text, and structured data. Buyers now ask ChatGPT/Perplexity/Claude "what's the best X and what does it cost?" *before* visiting — a pricing page an agent can't parse loses deals you never see.

**Fast check — the "paste test":** give the pricing URL to a browsing-capable AI (Perplexity, ChatGPT with search, Claude with web) — or paste the rendered page text — and ask "what are the plans and prices?" A clean miss means agents fetching your page will struggle too (a heuristic, not proof every agent fails).

The AI-readiness fixes are usually high-impact, low-effort (put prices in text, add `Offer` schema). Hand implementation to **schema** (Product/Offer JSON-LD) and **ai-seo** (extractability, AI-bot access, `llms.txt`).

**For the full 10-dimension rubric, scoring, and report template:** See [references/pricing-page-teardown.md](references/pricing-page-teardown.md). *(AI-agent-readiness lens adapted from Kyle Poyar / Growth Unhinged.)*

---

## Proactive Flags

Raise these without being asked:

- **Trial-to-paid above ~40%** (opt-in trial) → likely underpriced; test a 20-30% increase on new customers. Card-required trials convert higher by design, so judge them against that baseline. Around 15-30% is healthy; below ~10% points to price friction or a weak trial.
- **Nearly everyone on one tier** → no upsell path: the next tier lacks a reason to upgrade, or a top tier is missing.
- **Customers asking for features from a higher tier** → expansion revenue left on the table; review the gating.
- **Monthly churn above ~5%** → fix churn before raising prices.
- **Price unchanged for 2+ years** → review it against costs and the value shipped since.
- **A single plan** → no anchor and no upsell; add a higher tier even if few buy it.

---

## Pricing Checklist

### Before Setting Prices
- [ ] Defined target customer personas
- [ ] Researched competitor pricing
- [ ] Calculated the cost floor (cost to serve at the target gross margin)
- [ ] Identified your value metric
- [ ] Conducted willingness-to-pay research
- [ ] Mapped features to tiers

### Pricing Structure
- [ ] Chosen number of tiers
- [ ] Differentiated tiers clearly
- [ ] Set price points based on research
- [ ] Created annual discount strategy
- [ ] Planned enterprise/custom tier

---

## Task-Specific Questions

1. What pricing research have you done?
2. What's your current ARPU and conversion rate?
3. What's your primary value metric?
4. Who are your main pricing personas?
5. Are you self-serve, sales-led, or hybrid?
6. What pricing changes are you considering?

---

## Deliverables

| Request | Deliver |
|---------|---------|
| Design pricing | Value metric, three-tier structure with feature grid, price points with rationale |
| Optimize pricing | Flags raised, the user's numbers against benchmarks, prioritized fixes |
| Plan a price increase | Strategy choice, retention scenarios, notice timeline, customer message, wave plan |
| Review a pricing page | Teardown report (see Pricing Page Teardown) or a page spec from [references/pricing-page-design.md](references/pricing-page-design.md) |
| Pricing research | Van Westendorp and MaxDiff questions written for the product |
| Model scenarios | `scripts/pricing_modeler.py` output with its assumptions stated |

Lead with the recommendation, then the reasoning. Label each number as measured (the user's data), cited benchmark, or assumption.

---

## Related Skills

- **churn-prevention**: For cancel flows, save offers, and reducing revenue churn
- **cro**: For optimizing pricing page conversion
- **ai-seo**: For making the pricing page extractable/citable by AI (the teardown's AI-agent-readiness axis)
- **schema**: For Product/Offer structured data so machines can read your tiers and prices
- **copywriting**: For pricing page copy
- **marketing-psychology**: For pricing psychology principles
- **ab-testing**: For testing pricing changes
- **revops**: For deal desk processes and pipeline pricing
- **sales-enablement**: For proposal templates and pricing presentations
- **competitors**: For comparison pages that sit beside the pricing page

Sources and credits: [SOURCES.md](SOURCES.md)
