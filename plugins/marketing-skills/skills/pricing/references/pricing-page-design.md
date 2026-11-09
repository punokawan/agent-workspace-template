# Pricing Page Design

Build guidance for a pricing page: structure, plan cards, copy and tests. To score an existing page, use [pricing-page-teardown.md](pricing-page-teardown.md).

## Contents
- The Page's Job
- Page Structure (above the fold, below the fold)
- Copy Frameworks (plan names, CTA copy, price display)
- Conversion Tactics
- Test Ideas

## The Page's Job

A visitor on the pricing page is already interested. They ask three questions, in this order:

1. "Which plan is for me?"
2. "Is it worth the price?"
3. "What's the catch?"

Everything on the page answers one of them, or it goes.

---

## Page Structure

### Above the fold

**Billing toggle (monthly/annual)** sits at the top, before the plan cards. Show the saving as a badge ("Save 20%"), not only as math.

**Plan cards (usually three):**

```
┌─────────────┬─────────────┬─────────────┐
│   Starter   │    Pro      │ Enterprise  │
│             │ ★ Popular   │             │
│   $29/mo    │   $99/mo    │  Custom     │
│             │             │             │
│ For small   │ For growing │ For teams   │
│ teams       │ teams       │ needing     │
│             │             │ control     │
│ • Feature   │ • Feature   │ • Feature   │
│ • Feature   │ • Feature   │ • Feature   │
│ • Feature   │ • Feature   │ • Feature   │
│             │             │             │
│ [Start free]│[Start free] │[Contact us] │
└─────────────┴─────────────┴─────────────┘
```

Each card carries:
- A plan name tied to a segment or use, not just "Basic/Pro"
- The price, with billing period and a per-seat note where relevant
- One positioning line ("For growing teams who need X")
- 4-6 differentiators for that tier
- An action-oriented CTA (see CTA copy)
- A "Most popular" or "Recommended" badge on the tier you want most buyers in

### Below the fold

- **Feature comparison table** — every feature, grouped (core, collaboration, analytics, admin, support); ✓ and — only, no conditional wording; a sticky header so plan names stay visible while scrolling.
- **Social proof** — quotes matched to each tier where possible, recognizable logos, and only numbers that are true.
- **FAQ (5-7 questions)** — answer the buying objections plainly:
  1. Can I cancel anytime? → Yes, from settings, with no call needed.
  2. What happens at the end of my trial? → Say exactly what happens.
  3. Can I switch plans? → Yes; explain proration.
  4. Which payment methods do you accept? → List them, including invoicing for annual plans if offered.
  5. Is my data secure? → Name the certifications you actually hold, or give a short security statement.
  6. What if I need more than the top plan? → Link to the sales form.
- **Enterprise call to action** — a separate row below the cards: "Need custom pricing or a demo?" with a sales button. Say who it is for: seat counts, compliance needs, custom contracts.

---

## Copy Frameworks

### Plan names

Named plans anchor to identity, not just price.

| Generic | Better | Why |
|---------|--------|-----|
| Free / Basic / Pro | Solo / Studio / Agency | Maps to a customer segment |
| Starter / Growth / Enterprise | Developer / Team / Business | Maps to a use case |
| Individual / Team / Organization | Creator / Collaborator / Company | Maps to a role |

When the segments are genuinely vague, keep plain names. Creative names that confuse cost more than they earn.

### CTA copy

| Context | CTA |
|---------|-----|
| Free trial | "Start free trial" |
| Freemium | "Get started free" |
| Direct purchase, no trial | "Get [Plan name]" |
| Enterprise / sales-led | "Talk to us" or "Get a demo" |
| High-price annual commitment | "Schedule a call" |

Avoid "Sign up" (no value stated), "Subscribe" (reads like a newsletter), "Buy now" (transactional) and "Learn more" (a dead end on a pricing page).

### Price display

| Scenario | Show it as |
|----------|-----------|
| Monthly | "$99/month" |
| Annual, billed monthly | "$83/month, billed annually" |
| Annual, billed upfront | "$996/year" with a per-month equivalent |
| Per seat | "$15/user/month" |
| Usage-based | "From $0.002 per call" |
| Enterprise | "Custom" or "Starting at $X" |

Show the annual saving as a percentage or as an amount, whichever reads larger.

---

## Conversion Tactics

- **Anchoring** — the first price seen sets the frame: after a 500/month plan, 99 feels small. To push the middle tier, order plans from highest to lowest, or give the middle card the strongest visual treatment.
- **Recommended badge** — make it obvious: brand color or a darker background, a slightly taller card, "Most popular" or "Recommended for most teams", and the first CTA in tab order.
- **Annual default** — defaulting the toggle to annual raises the annual take rate. Default to monthly when you want lower-commitment customers, for example while testing cash flow or a low-commitment product.

---

## Test Ideas

**High impact, easy to run:**
1. Default billing toggle (annual vs. monthly)
2. "Most popular" badge placement
3. CTA copy ("Start free trial" vs. "Get Pro")
4. Price display (per month vs. per year)

**Medium impact, more setup:**
5. Plan names (segment-based vs. feature-based)
6. Number of bullets on the cards (3 vs. 6)
7. Social proof above vs. below the fold
8. FAQ accordion vs. expanded

**High impact, hard to run:**
9. Price points (slow to reach significance)
10. Two tiers vs. three
11. Adding or removing a free tier

Size each test before you run it: pricing pages often lack the traffic to detect small effects. Use the **ab-testing** skill's sample-size guidance.
