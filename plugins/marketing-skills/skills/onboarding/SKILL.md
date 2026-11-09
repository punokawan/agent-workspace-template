---
name: onboarding
description: Designs and audits post-signup onboarding so new users reach their aha moment fast — activation definition, first-run flow, checklists, empty states, onboarding emails, and recovery of stalled users. Use when the user wants to optimize post-signup onboarding, user activation, first-run experience, or time-to-value. Also use when the user mentions "onboarding flow," "activation rate," "user activation," "first-run experience," "empty states," "onboarding checklist," "aha moment," "new user experience," "users aren't activating," "nobody completes setup," "low activation rate," "users sign up but don't use the product," "low day-1 or day-7 retention," "time to value," or "first session experience." Use this whenever users are signing up but not sticking around. For signup/registration optimization, see signup. For ongoing email sequences, see emails.
metadata:
  version: 1.0.0
  sources: "corey:onboarding@96798cf; ali:onboarding-cro@8f08254"
---

# Onboarding CRO

You are an expert in user onboarding and activation. Your goal is to help users reach their "aha moment" as quickly as possible and establish habits that lead to long-term retention.

## Initial Assessment

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before providing recommendations, understand:

1. **Product Context** - What type of product? B2B or B2C? Core value proposition?
2. **Activation Definition** - What's the "aha moment"? What action indicates a user "gets it"?
3. **Current State** - What happens after signup? Where do users drop off?

---

## Diagnose Before Prescribing

Common symptoms, and where they usually point:

- **Low day-1 or day-7 retention** → ask for the activation event and the current post-signup flow before proposing fixes.
- **"Users sign up but don't come back," or a big drop between signup and the first key action** → treat it as an activation problem, not an acquisition or marketing problem.
- **Low trial-to-paid conversion** → check that activation is defined and reached before assuming pricing is the blocker.
- **"Our onboarding emails aren't working"** → review the in-app onboarding first; email should support it, not replace it.

---

## Core Principles

### 1. Time-to-Value Is Everything
Remove every step between signup and experiencing core value. Design the **Minimum Path to Value (MPTV)** — the least number of steps to experience enough value to make a confident decision (see [references/minimum-path-to-value.md](references/minimum-path-to-value.md)).

### 2. One Goal Per Session
Focus first session on one successful outcome. Save advanced features for later.

### 3. Do, Don't Show
Interactive > Tutorial. Doing the thing > Learning about the thing.

### 4. Progress Creates Motivation
Show advancement. Celebrate completions. Make the path visible. (See onboarding psychology below for the mechanisms.)

---

## Onboarding Psychology

The principles that make progress mechanics, checklists, and prompts actually work:

- **Endowed Progress Effect** — people finish faster when progress is already started for them. A checklist that opens at "20% done" (a step pre-completed on their behalf) drives roughly **+40% completion** vs. starting at 0%. Give users a head start, don't make them start from nothing.
- **Peak-End Rule** — users remember an experience by its most intense moment (the *peak*) and its *end*, not the average. Engineer a clear high point (a win, a wow, a celebration) and end each session on a positive note.
- **Goldilocks Rule** — motivation peaks when a task is neither too easy nor too hard, but *just right* on the edge of ability. Tune early steps so they're achievable but not trivial.
- **BJ Fogg Behavior Model** — a behavior happens only when **Motivation × Ability × Prompt** converge at the same moment. If a step isn't happening, one of the three is missing: raise motivation, make it easier (Ability), or add a better-timed Prompt.
- **Mario Kart boosters & blockers** (Ramli John) — treat onboarding like a race track. Add **boosters** (accelerants: pre-filled data, templates, quick wins, celebrations) and remove **blockers** (friction: required fields, dead ends, confusing empty states). Speed users toward value and clear obstacles from the lane.

## Onboarding Toolkit (10 Components)

The components you assemble an onboarding experience from. Use the fewest that reach value:

| Component | Purpose |
|-----------|---------|
| Welcome forms | Capture role/goal to personalize the path (keep short — Hick's Law) |
| Initial screens | First-run screens that orient and point to one clear action |
| Drip emails | Multi-touch nurture — **one concept per email**, don't overload |
| Skippable tutorials | Optional guidance users can bypass — never trap them |
| Videos | Show complex workflows visually |
| Docs / help center | Self-serve reference for when users get stuck |
| Onboarding calls | Human touch for complex or high-value accounts |
| Data inputs | Getting the user's real data in so value feels "real" |
| Checklists | Ordered, value-first steps with visible progress (see below) |
| Empty states | Guided first-action opportunities, not dead ends (see below) |

---

## Defining Activation

**Judge activation by lead→customer conversion + 90-day retention, not lead volume.** More signups mean nothing if they don't convert and stick.

Choose an **activation model** (freemium, free trial, paid trial, money-back, consultation) before designing the flow — the model shapes the whole onboarding path. See [references/activation-models.md](references/activation-models.md) for the 5 models, the credit-card tradeoff, Model-Market Fit, and the Evernote-vs-Notion parable.

### Find Your Aha Moment

Find early value actions associated with later retention, using a defined cohort and timeline:

1. Define signup as time zero, an early activation window, and a separate retention outcome after the activation window. For example, first-seven-day actions and return activity in week four; choose windows that fit the product cadence.
2. Include all eligible signups with full follow-up through the retention window. Show recent, immature cohorts separately; do not count them as churned or restrict the denominator to users who already activated.
3. Compare actions recorded within the early window. Exclude behavior during the retention outcome window: a week-four return cannot also be the early activation predictor of week-four retention.
4. Treat high-correlation events and frequency thresholds as candidate hypotheses. Report counts, uncertainty, and acquisition/product segments; confirm the definition on a later mature cohort before adopting it.
5. Test whether an onboarding intervention improves later retention or customer conversion. Correlation alone does not prove that forcing the action causes retention.

[Amplitude's Compass setup](https://amplitude.com/docs/analytics/charts/compass/compass-aha-moment) separates early actions from later retention and requires time for every cohort member to retain; its [interpretation guide](https://amplitude.com/docs/analytics/charts/compass/compass-interpret-1) distinguishes correlation from causation.

**Examples by product type:**
- Project management: Create first project + add team member
- Analytics: Install tracking + see first report
- Design tool: Create first design + export/share
- Marketplace: Complete first transaction

### Activation Metrics
- % of signups who reach activation
- Time to activation
- Steps to activation
- Activation by cohort/source

---

## Onboarding Flow Design

### Immediate Post-Signup (First 30 Seconds)

| Approach | Best For | Risk |
|----------|----------|------|
| Product-first | Simple products, B2C, mobile | Blank slate overwhelm |
| Guided setup | Products needing personalization | Adds friction before value |
| Value-first | Products with demo data | May not feel "real" |

**Whatever you choose:**
- Clear single next action
- No dead ends
- Progress indication if multi-step

### Onboarding Checklist Pattern

**When to use:**
- Multiple setup steps required
- Product has several features to discover
- Self-serve B2B products

**Best practices:**
- 3-7 items (not overwhelming)
- Order by value (most impactful first)
- Start with quick wins
- Progress bar/completion %
- Celebration on completion
- Dismiss option (don't trap users)

### Empty States

Empty states are onboarding opportunities, not dead ends.

**Good empty state:**
- Explains what this area is for
- Shows what it looks like with data
- Clear primary action to add first item
- Optional: Pre-populate with example data

### Tooltips and Guided Tours

**When to use:** Complex UI, features that aren't self-evident, power features users might miss

**Best practices:**
- Max 3-5 steps per tour
- Dismissable at any time
- Don't repeat for returning users

---

## Multi-Channel Onboarding

### Email + In-App Coordination

**Trigger-based emails:**
- Welcome email (immediate)
- Incomplete onboarding (24h, 72h)
- Activation achieved (celebration + next step)
- Feature discovery (days 3, 7, 14)

**Email should:**
- Reinforce in-app actions, not duplicate them
- Drive back to product with specific CTA
- Be personalized based on actions taken

---

## Handling Stalled Users

### Detection
Define "stalled" criteria (X days inactive, incomplete setup)

### Re-engagement Tactics

1. **Email sequence** - Reminder of value, address blockers, offer help
2. **In-app recovery** - Welcome back, pick up where left off
3. **Human touch** - For high-value accounts, personal outreach

---

## Measurement

### Key Metrics

| Metric | Description |
|--------|-------------|
| Activation rate | % reaching activation event |
| Time to activation | How long to first value |
| Onboarding completion | % completing setup |
| Day 1/7/30 retention | Return rate by timeframe |

### Funnel Analysis

Track drop-off at each step:
```
Signup → Step 1 → Step 2 → Activation → Retention
100%      80%       60%       40%         25%
```

Identify biggest drops and focus there. Run the bundled analyzer on step counts for one signup cohort instead of eyeballing:

```bash
python3 scripts/activation_funnel_analyzer.py funnel.json                 # text report
python3 scripts/activation_funnel_analyzer.py funnel.json --json          # JSON for pipelines
python3 scripts/activation_funnel_analyzer.py funnel.json --recover 0.3   # what-if: recover 30% of the worst drop
python3 scripts/activation_funnel_analyzer.py                             # demo funnel
```

Input is the steps in funnel order, such as `{"steps": [{"name": "Signup completed", "users": 1000}, {"name": "First project created", "users": 290}]}`. The report gives per-step drop-off and users lost, names the step with the worst drop-off rate and the step that loses the most users, and projects the activation gain from recovering part of the worst drop (50% by default). The projection is an upper bound: it assumes regained users convert downstream at today's rates. Start the audit at the steps it names.

---

## Output Format

### Onboarding Audit
Lead with the highest-leverage finding. For each issue: Finding → Impact → Recommendation → Priority, naming the specific step, metric, or trigger it concerns.

### Onboarding Flow Design
- Activation definition: the aha event, its time window, and the metric that confirms it
- Step-by-step flow, with the drop-off points and decision branches
- Checklist items (if applicable): 3-7, ordered by value, with completion messaging
- Empty state copy
- Email sequence triggers: condition, timing, and goal for each email
- Metrics plan
- Experiment backlog, sorted by expected impact

Write onboarding copy in the product's brand voice.

---

## Common Patterns by Product Type

| Product Type | Key Steps |
|--------------|-----------|
| B2B SaaS | Setup wizard → First value action → Team invite → Deep setup |
| Marketplace | Complete profile → Browse → First transaction → Repeat loop |
| Mobile App | Permissions → Quick win → Push setup → Habit loop |
| Content Platform | Follow/customize → Consume → Create → Engage |

---

## Experiment Ideas

When recommending experiments, consider tests for:
- Flow simplification (step count, ordering)
- Progress and motivation mechanics
- Personalization by role or goal
- Support and help availability

**For comprehensive experiment ideas**: See [references/experiments.md](references/experiments.md)

---

## References

- **[references/minimum-path-to-value.md](references/minimum-path-to-value.md)** — MPTV, Hick's Law, the inventory→remove→reconstruct process, abandonment benchmarks (40–60% after one session; 75–80% within day one), and patterns (Stripe, Calendly, Notion).
- **[references/activation-models.md](references/activation-models.md)** — the 5 activation models, credit-card tradeoff, Model-Market Fit, Evernote vs. Notion.
- **[references/experiments.md](references/experiments.md)** — comprehensive A/B test and experiment ideas.

---

## Task-Specific Questions

1. Which early action predicts later retention, using what activation window and fully observed signup cohort?
2. What happens immediately after signup?
3. Where do users currently drop off?
4. What's your activation rate target?
5. Do you have cohort analysis on successful vs. churned users?

---

## Related Skills

- **signup**: For optimizing the signup before onboarding
- **emails**: For onboarding email series
- **paywalls**: For converting to paid during/after onboarding, once users have reached value; if they meet paywalls before the aha moment, fix onboarding first
- **popups**: For trigger, frequency, and dismissal rules when onboarding uses modals or announcement overlays
- **ab-testing**: For testing onboarding changes

Sources and credits: [SOURCES.md](SOURCES.md)
