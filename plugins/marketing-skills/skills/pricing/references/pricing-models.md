# Pricing Models

The eight core ways to structure *how* you charge. This is distinct from the value metric (what unit you charge on) and the tier structure (how you package). Most real products **combine** two or more of these.

## Contents
- The 8 Pricing Models
- Model Variants and Failure Modes
- Choosing a Model: Five Questions
- Combining Models
- The Value/Price Ratio
- The Low-Price Retention Counterpoint
- Benchmarks by Stage

---

## The 8 Pricing Models

| Model | How it works | Best when | Reference |
|-------|-------------|-----------|-----------|
| **Flat-rate** | One price, one product, everyone pays the same | Simple product, one persona, you want zero pricing friction | Basecamp |
| **Usage-based** | Pay for what you consume (metered) | Value scales directly with volume; consumption is variable and easy to meter | Stripe |
| **Tier-based** | Good-better-best packages at set prices | Distinct segments with different needs and budgets | Kinsta |
| **User-based** | Price per seat/user | Value grows as more people in the org use it (collaboration) | Notion |
| **Feature-based** | Price gated by which capabilities are unlocked | Clear feature tiers map to willingness to pay | Intercom |
| **Credit-based** | Buy a bucket of credits, spend them on actions | Usage is lumpy or bursty; you want prepaid commitment and simple mental accounting | Audible |
| **Outcome-based** | Pay per result delivered (resolution, task completed) | You can measure and attribute the outcome, and the outcome is what the buyer actually wants | Intercom Fin, Zapier |
| **Hybrid** | Deliberate mix (e.g. platform fee + usage, or seats + credits) | A single model under- or over-charges different customers | Drift |

### When to reach for each

- **Flat-rate** — reach for it first if you can. It's the easiest to sell, easiest to understand, easiest to forecast. The tradeoff: you leave money on the table with your biggest customers.
- **Usage-based** — the fairest model when consumption tracks value, but revenue is less predictable and buyers fear a surprise bill. Pair with spend caps or alerts.
- **Tier-based** — the default for self-serve SaaS. Lets one page serve SMB through mid-market.
- **User-based** — only if value genuinely rises with headcount. If it doesn't, seats punish adoption (teams share logins to avoid paying).
- **Feature-based** — powerful for segmentation, but don't gate the feature that delivers your core value; gate the ones that separate casual from serious users.
- **Credit-based** — good for AI/actions-based products where each action has a cost. Credits decouple price from a single unit and make prepayment feel natural.
- **Outcome-based** — the emerging model for AI agents (charge per resolved ticket, per automation run). Highest trust because the buyer only pays when they win — but only viable when the outcome is measurable and clearly attributable to you.
- **Hybrid** — where most mature products end up. A base platform fee for predictability plus a usage/outcome component for upside.

---

## Model Variants and Failure Modes

### Per-seat variants

| Variant | How it works | Example |
|---------|--------------|---------|
| Named seat | Each license belongs to one person | Salesforce |
| Concurrent seat | N people can be signed in at once | Legacy enterprise software |
| Creator/viewer split | Creators pay; viewers are free or cheap | Figma, Miro |
| Minimum seat count | A plan requires at least N seats | Most enterprise deals |

Creator/viewer pricing suits tools where one team creates and many consume: free viewers spread the product while paying creators carry the revenue.

**Per-seat fails when** one power user does the work and the rest only view results, when contractors or outside stakeholders need access (billing turns into a negotiation), or when shared logins are easy and enforcement is hard.

### Usage variants

| Variant | How it works | Example |
|---------|--------------|---------|
| Pure consumption | Pay only for what you use | AWS Lambda |
| Prepaid credits | Buy credits, consume at your own pace | OpenAI, Resend |
| Committed use + overage | Flat fee with an included allowance, then per unit | Stripe, Twilio at volume |
| Tiered usage | Lower unit price at higher volumes | Mailchimp email tiers |

**Usage pricing fails when** bills become unpredictable (customers cap usage to avoid overages, so you engineer your own ceiling), when usage drops in a downturn (revenue drops with it), or when neither side can forecast spend. Many mature usage-based products add a small platform fee for a revenue floor and to soften low-usage months.

### Other failure modes

- **Feature tiers** fail when the tiers don't match real needs (customers cluster in one tier and none move), when the enterprise features don't justify the jump (you stall mid-market), or when there are too many tiers.
- **Flat fee** fails through adverse selection: heavy users are subsidized by light users, so heavy users stay and light users churn. It also leaves no path to grow revenue from existing customers without tiers, add-ons or increases.

---

## Choosing a Model: Five Questions

Start from the value metric; these questions pick between the models that fit it.

1. **Does value scale with users?** Linearly → per seat. Not linearly → creator/viewer or role-based seats.
2. **Does value scale with usage?** Measurably → usage-based. Hard to measure → feature tiers with usage caps.
3. **Is the buyer a small business that wants simplicity?** Yes → flat fee or 2-3 simple feature tiers.
4. **Do enterprise buyers need governance and compliance?** Yes → an enterprise tier, even if it is "Contact us". No → three tiers at most.
5. **Is it a developer or technical product?** Yes → usage-based with a free tier is the market norm. No → feature tiers are easier to buy.

---

## Combining Models

These aren't mutually exclusive. Common combinations:

- **Tiers + per-user** — seats within each package (most B2B SaaS)
- **Platform fee + usage** — predictable base, variable upside (Twilio-style)
- **Seats + credits** — pay per person, then top up credits for heavy actions
- **Feature tiers + outcome** — unlock capabilities by tier, charge per result on top

Pick the primary model from the value metric, then layer a second only if a single model clearly mis-prices a real segment.

---

## The Value/Price Ratio

Aim for roughly a **10:1 value-to-price ratio** (Ryan Kulp): the customer should perceive about **10x more value than they pay**. This is the buffer that makes the purchase feel obvious rather than negotiated, and it leaves headroom to raise prices later as you add value.

If you can't articulate 10x value, the problem is usually the offer or the positioning, not the price point.

---

## The Low-Price Retention Counterpoint

Charging too little is not the safe choice. **Low prices hurt retention** (Patrick Campbell / ProfitWell data, echoed by operators like Josh Pigford of SpyFu and Tyler Tringas): under-priced customers churn *more*, not less, because a low price signals low value and attracts the least-committed, most price-sensitive buyers.

Related: the **discount-asker signal** — customers who negotiate for a discount tend to churn at roughly **2x** the rate of full-price customers. Discounting to close a deal often buys a customer who leaves anyway.

**Implication:** when in doubt, price higher. It's easier to grandfather a price down than to claw one up, and a higher price selects for better-fit, longer-retained customers.

---

## Benchmarks by Stage

Rough, unsourced rules of thumb from practitioner experience. Use them to spot outliers, then compare against your own cohorts. Card-required trials convert higher by design (see [tier-structure.md](tier-structure.md)).

| Metric | Early stage | Growth | Scale |
|--------|-------------|--------|-------|
| Trial-to-paid rate | 15-25% | 20-35% | 25-40% |
| Annual share of customers | 30-50% | 40-60% | 50-70% |
| Expansion revenue (% of MRR) | 0-10% | 10-20% | 20-40% |
| Price review cadence | Ad hoc | Yearly | Yearly |
| Monthly churn | 2-8% | 1-4% | 0.5-2% |

**LTV:CAC** should be at least 3:1. Below that, pricing, retention or both need work.
