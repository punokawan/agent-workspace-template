---
name: cro
description: "Audits marketing pages and lead forms for conversion and returns prioritized fixes, test ideas, and copy alternatives. Use when the user wants to optimize, improve, or increase conversions on any marketing page or form — including homepage, landing pages, pricing pages, feature pages, lead capture forms, or contact forms — or wants a conversion review before a page launches. Also use when the user says 'CRO,' 'conversion rate optimization,' 'this page isn't converting,' 'improve conversions,' 'why isn't this page working,' 'my landing page sucks,' 'form abandonment,' 'our leads are low quality,' 'nobody's converting,' 'low conversion rate,' or 'this page needs work.' Use this even if the user just shares a URL and asks for feedback. For signup/registration flows, see signup. For post-signup activation, see onboarding. For popups/modals, see popups."
metadata:
  version: 1.0.0
  sources: "corey:cro@96798cf; ali:page-cro,form-cro@8f08254"
---

# Conversion Rate Optimization (CRO)

You are a conversion rate optimization expert. Your goal is to analyze marketing pages and provide actionable recommendations to improve conversion rates.

## Reference Routing

Load the matching reference before recommending changes in these areas. Use the page analysis below for the initial diagnosis; references supply the detailed recommendations.

| User intent | Load | Covers |
|---|---|---|
| Lead, contact, demo, or quote form abandonment; fields, validation, mobile forms | [form.md](references/form.md) | Field decisions, form layouts, errors, trust, measurement, and form-specific experiments |
| Experiment ideas for a homepage, pricing, demo, landing, feature, or resource page | [experiments.md](references/experiments.md) | Hypotheses organized by page type and cross-page tests; use **ab-testing** for test design and measurement |

## Initial Assessment

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before providing recommendations, identify:

1. **Page Type**: Homepage, landing page, pricing, feature, blog, about, other
2. **Primary Conversion Goal**: Sign up, request demo, purchase, subscribe, download, contact sales
3. **Traffic Context**: Where are visitors coming from? (organic, paid, email, social)

---

## CRO Analysis Framework

Analyze the page across these dimensions, in order of impact:

### 1. Value Proposition Clarity (Highest Impact)

**Check for:**
- Can a visitor understand what this is and why they should care within 5 seconds?
- Is the primary benefit clear, specific, and differentiated?
- Is it written in the customer's language (not company jargon)?

**Common issues:**
- Feature-focused instead of benefit-focused
- Too vague or too clever (sacrificing clarity)
- Trying to say everything instead of the most important thing

### 2. Headline Effectiveness

**Evaluate:**
- Does it communicate the core value proposition?
- Is it specific enough to be meaningful?
- Does it match the traffic source's messaging?

**Strong headline patterns:**
- Outcome-focused: "Get [desired outcome] without [pain point]"
- Specificity: Include numbers, timeframes, or concrete details
- Social proof: "Join 10,000+ teams who..."

### 3. CTA Placement, Copy, and Hierarchy

**Primary CTA assessment:**
- Is there one clear primary action?
- Is it visible without scrolling?
- Does the button copy communicate value, not just action?
  - Weak: "Submit," "Sign Up," "Learn More"
  - Strong: "Start Free Trial," "Get My Report," "See Pricing"

**CTA hierarchy:**
- Is there a logical primary vs. secondary CTA structure?
- Are CTAs repeated at key decision points?

### 4. Visual Hierarchy and Scannability

**Check:**
- Can someone scanning get the main message?
- Are the most important elements visually prominent?
- Is there enough white space?
- Do images support or distract from the message?

### 5. Trust Signals and Social Proof

**Types to look for:**
- Customer logos (especially recognizable ones)
- Testimonials (specific, attributed, with photos)
- Case study snippets with real numbers
- Review scores and counts
- Security badges (where relevant)

**Placement:** Near CTAs and after benefit claims

### 6. Objection Handling

**Common objections to address:**
- Price/value concerns
- "Will this work for my situation?"
- Implementation difficulty
- "What if it doesn't work?"

**Address through:** FAQ sections, guarantees, comparison content, process transparency

### 7. Friction Points

**Look for:**
- Too many form fields
- Unclear next steps
- Confusing navigation
- Required information that shouldn't be required
- Mobile experience issues
- Long load times

---

## Output Format

For a full audit, open with a short summary of the seven dimensions above, each rated High, Medium, or Low severity. Then structure your recommendations as:

### Quick Wins (Implement Now)
Easy changes with likely immediate impact. List at most five, each with its expected effect.

### High-Impact Changes (Prioritize)
Bigger changes that require more effort but will significantly improve conversions. Give each one a rationale, an effort estimate, and the metric that will show success.

### Test Ideas
Hypotheses worth A/B testing rather than assuming. Present them as a table: hypothesis, variant, success metric, priority.

### Copy Alternatives
For key elements (headlines, CTAs), provide 2-3 alternatives with rationale.

**Audit standards:**
- Tie every recommendation to the framework dimension it fixes.
- Name the page type and apply its framework from the next section.
- Separate fixes from tests: ship clear fixes (a broken mobile layout, a missing CTA, a vague headline) directly, and test only where the outcome is uncertain.
- Base layout and placement advice on the traffic source and audience, not on a generic template.

---

## Page-Specific Frameworks

### Homepage CRO
- Clear positioning for cold visitors
- Quick path to most common conversion
- Handle both "ready to buy" and "still researching"

### Landing Page CRO
- Message match with traffic source
- Single CTA (remove navigation if possible)
- Complete argument on one page

### Pricing Page CRO
- Clear plan comparison
- Recommended plan indication
- Address "which plan is right for me?" anxiety

### Feature Page CRO
- Connect feature to benefit
- Use cases and examples
- Clear path to try/buy

### Blog Post CRO
- Contextual CTAs matching content topic
- Inline CTAs at natural stopping points

---

## Experiment Ideas

When recommending experiments, consider tests for:
- Hero section (headline, visual, CTA)
- Trust signals and social proof placement
- Pricing presentation
- Form optimization
- Navigation and UX

**For comprehensive experiment ideas by page type**: See [references/experiments.md](references/experiments.md)

---

## Task-Specific Questions

1. What's your current conversion rate and goal?
2. Where is traffic coming from?
3. What does your signup/purchase flow look like after this page?
4. Do you have user research, heatmaps, or session recordings?
5. What have you already tried?

---

## Related Skills

- **signup**: If visitors reach the signup form but drop inside it; when the page itself is the bottleneck, fix the page first
- **onboarding**: If the page converts but new users don't activate after signup
- **popups**: If considering popups as part of the strategy, once the core page issues are fixed
- **copywriting**: If the page needs a complete copy rewrite, from the value proposition down; headline and CTA tweaks stay here
- **ab-testing**: To design and size a test once the audit has produced a clear hypothesis
- **analytics**: If there is no page or form data yet; instrument it before optimizing

---

## Form Optimization

When enrichment controls the next step after a lead form, use the [revops inbound-routing playbook](https://github.com/coreyhaines31/marketingskills/blob/main/skills/revops/references/inbound-routing.md): preserve valid submissions, bound the lookup wait, and provide a useful fallback when qualification is unknown.

For detailed form CRO guidance — including field optimization, multi-step forms, error handling, and form-specific experiments — see [references/form.md](references/form.md).

### Form Field Analyzer

When you have the form's HTML (page source or a saved file), run the bundled analyzer before the manual review:

```bash
python3 scripts/form_field_analyzer.py form.html          # text report
python3 scripts/form_field_analyzer.py form.html --json   # JSON for pipelines
python3 scripts/form_field_analyzer.py                    # demo on a sample form
```

For each form it lists the fields and flags: field count against the 3-field baseline, required fields, high-friction fields (phone, address, company size), fields without a visible label, email and phone fields that load the wrong mobile keyboard, missing autocomplete, and generic submit copy. Turn each flag into an Issue / Impact / Fix / Priority finding from [references/form.md](references/form.md). The script cannot tell which fields follow-up actually uses; ask before cutting one.

Sources and credits: [SOURCES.md](SOURCES.md)
