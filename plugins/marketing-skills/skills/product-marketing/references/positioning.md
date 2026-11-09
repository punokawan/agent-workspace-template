# Positioning

How to work out positioning before you record it in the context file. Positioning is the choice of market context that makes the product's value obvious to the customers who care most. Messaging is built on it; it isn't the messaging itself.

## Contents
- Start From Best-Fit Customers (ICP)
- The Positioning Chain
- Choosing a Positioning Style
- Capturing the Result
- Messaging Hierarchy
- Validating Positioning
- Positioning Map
- When to Revisit

## Start From Best-Fit Customers (ICP)

Positioning starts from the customers who already get the most value, not from the whole market. Derive the ICP from evidence:

1. **Pull the best customers.** Rank current customers by value (lifetime value or revenue), retention, and how fast they closed or activated. Take the top group; the top 20% is a common cut.
2. **Find what they share.** Firmographics (industry, size, stage, region), technographics (tools they use, technical maturity), and situation (the trigger that made them look, how much the problem hurts, their tolerance for risk).
3. **Name the buying roles.** For B2B: who uses it, who champions it, who signs, who can block it. Record them in the Personas section; sales-facing persona cards live in **sales-enablement**.
4. **Check the profile against outcomes.** A real ICP closes faster, retains better, and expands more than your median customer. If the profile doesn't separate on those numbers, it describes everyone.
5. **Write the anti-persona.** Who signs up and churns, needs heavy customization, or buys for the wrong reason.

**ICP evidence checklist.** Record the numbers, not just the ticks:
- [ ] At least 5 paying customers match the profile
- [ ] Sales cycle or time to activation shorter than your median
- [ ] Retention higher, and churn lower, than your median
- [ ] Strong product engagement
- [ ] Some would act as a reference or case study

With few customers, use the users who would be most disappointed if the product disappeared, and mark the ICP as a hypothesis in the context file.

| Dimension | Profile | Evidence |
|---|---|---|
| Industry or segment | | |
| Company size or stage (B2B), life situation (B2C) | | |
| Region and language | | |
| Tools or technical maturity | | |
| Trigger that starts the search | | |
| Pain level and cost of doing nothing | | |

To score leads against the ICP, see **revops** (fit scoring). To build prospect lists from it, see **prospecting**.

## The Positioning Chain

Work the components in order; each one depends on the one before (April Dunford, *Obviously Awesome*). Do it with founders, sales, product, and marketing in the room, and start from the best-fit customers above.

1. **Competitive alternatives.** What those customers would do if the product didn't exist: direct competitors, adjacent tools, building it in-house, spreadsheets or manual work, doing nothing. The status quo is often the biggest competitor. Ask customers:
   - "Before us, how did you handle this?"
   - "What else did you evaluate?"
   - "What would you switch to if we disappeared?"
2. **Unique attributes.** Capabilities the alternatives don't have. Check each candidate against each alternative and keep only what you can prove. Table stakes (everyone has them) drop out.
3. **Value.** What each unique attribute lets the customer do, and the outcome. Group the attributes into 2-4 value themes. Pattern: [attribute] enables [value], so customers get [outcome], with the proof next to it.
4. **Who cares a lot.** The segment for whom that value matters most. It should match the ICP; if it doesn't, one of the two is wrong.
5. **Market category.** The frame of reference that makes the value obvious and tells buyers what to compare you with.
6. **Relevant trend (optional).** A trend that makes the value more urgent now. Use it only if buyers feel it and you can stand behind it for years.

**Attribute audit** (example):

| Attribute | Alternative A | Alternative B | Status quo | Unique? | Proof |
|---|---|---|---|---|---|
| Real-time editing for any team size | Async only | Up to 5 editors | Email attachments | Yes | Load test, customer quote |
| 100 integrations | 500+ | 200+ | n/a | No (table stakes) | |

An alternative's missing feature counts only when their docs or a trial confirm it, under the same evidence rules as public comparison pages (see **competitors**, Evidence Discipline).

## Choosing a Positioning Style

| Style | When it fits | Risk |
|---|---|---|
| **Head-to-head** | You can win an existing category on the buyer's main criteria | Medium: you fight the leader on its terms |
| **Big fish, small pond** | You're clearly best for one subsegment of an existing category | Low: a smaller market that's easier to own |
| **Create a new game** | No existing category frames the value, and you can afford to sell the problem and the solution | High: rare, slow, and expensive |

Default to an existing category. Categories usually emerge rather than get created, and educating a market takes years.

## Capturing the Result

Record positioning in the context file: the category in **Product Overview**, the ICP in **Target Audience** and **Personas**, the alternatives in **Competitive Landscape**, and the attributes and value themes in **Differentiation** and **Proof Points**. Log a real repositioning in the **Changelog**.

A short summary helps people share it. The classic statement format (Geoffrey Moore, *Crossing the Chasm*) works as a summary, but only after the chain is done. Filled in first, it produces answers with nothing behind them.

```
For [best-fit customer]
who [need or trigger],
[product] is a [market category]
that [key value].
Unlike [main alternative],
[product] [primary unique attribute, with proof].
```

For a one-liner: `[Product] helps [best-fit customer] [reach outcome] by [unique approach].`

For a spoken version (about 30 seconds: intros, events, the first minute of a call), run the same chain in four lines:

```
You know how [best-fit customer] struggles with [pain or trigger]?
[Product] is a [market category] that [primary unique attribute].
Unlike [main alternative], we [value that attribute delivers].
Customers see [specific outcome, with proof] within [timeframe].
```

Fill the last line only with an outcome from **Proof Points**; drop it rather than invent a number.

## Messaging Hierarchy

Build messaging on the positioning, one level at a time. Every level traces back to the chain:

| Level | Length | Comes from |
|---|---|---|
| Headline | 5-10 words | The main value theme, in customer language |
| Subhead | 1 sentence | Category, who it's for, and the key value |
| Benefits | 3-4 bullets | The value themes |
| Feature-to-value pairs | One per unique attribute | Attribute, value, outcome |
| Proof | Logos, numbers, quotes | The Proof Points section |

Use the buyer's own words from **Customer Language**. Persona-specific value propositions and deck variants live in **sales-enablement**; page copy lives in **copywriting**.

## Validating Positioning

Positioning stays a hypothesis until customers repeat it back.

**Interviews.** Talk to 10 or more best-fit customers for 15-20 minutes each. Ask open questions and don't lead:
1. "How would you describe [product] to a colleague?"
2. "What problem does it solve for you?"
3. "What else did you consider?"
4. "Why did you choose it over [alternative]?"
5. "What would make you stop using it?"

Write down exact phrases. A working bar, not a statistic: most interviewees (around 7 of 10) describe the core value in similar words without prompting. If they describe a different value, the chain is off; revisit attributes and value before you touch the copy. Add new phrases to **Customer Language**.

**Live tests.** Test the new positioning against the old one where it shows up: homepage headline, ad angles, outbound openers. For sample size and stopping rules, see **ab-testing**. Record results in **Learnings**.

## Positioning Map

A 2x2 map helps the team see where the alternatives sit and where you can win. Pick axes buyers actually use to choose, on which your place is clear:

| Useful axes | Weak axes |
|---|---|
| Ease of use vs. power | Quality vs. price (everyone claims quality) |
| Speed vs. depth | Innovation vs. stability (subjective) |
| Specialist vs. broad | Customer focus vs. product focus (not a buying criterion) |
| Self-serve vs. guided | |

Place each alternative with the evidence for its position and the date you checked. The map is an internal thinking tool; any public claim it suggests follows the evidence rules in **competitors**.

## When to Revisit

Review positioning when any of these happen, and log a real change as a new version with a Changelog entry:
- Win rate against a named competitor drops, or a new alternative starts showing up in deals
- A competitor repositions or changes pricing or packaging
- Your best customers no longer match the ICP (new segment, new use case)
- Messaging has drifted apart across the homepage, deck, and ads
- The product changed enough that the category no longer fits

Signs that positioning works: buyers describe the value unprompted, sales cycles shorten for the ICP, win rate rises against the main alternative, and positioning-led pages convert better than the versions they replaced.
