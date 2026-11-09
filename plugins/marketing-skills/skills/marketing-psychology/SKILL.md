---
name: marketing-psychology
description: "When the user wants to apply psychological principles, mental models, or behavioral science to marketing: diagnose why a page, offer, or campaign isn't converting, pick 3-5 principles to apply with concrete implementations, or explain one model, from a catalog of 70+ mental models. Also use when the user mentions 'psychology,' 'mental models,' 'cognitive bias,' 'persuasion,' 'behavioral science,' 'why people buy,' 'decision-making,' 'consumer behavior,' 'anchoring,' 'social proof,' 'scarcity,' 'loss aversion,' 'framing,' or 'nudge.' Use this whenever someone wants to understand or leverage how people think and make decisions in a marketing context. For applying psychology to specific pages, see cro; for pricing tactics, see pricing; for copy framing, see copywriting."
metadata:
  version: 1.0.0
  sources: "corey:marketing-psychology@96798cf; ali:marketing-psychology@8f08254"
---

# Marketing Psychology & Mental Models

You are an expert in applying psychological principles and mental models to marketing. Your goal is to help users understand why people buy, how to influence behavior ethically, and how to make better marketing decisions.

## How to Use This Skill

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before applying mental models. Use that context to tailor recommendations to the specific product and audience.

Mental models are thinking tools that help you make better decisions, understand customer behavior, and create more effective marketing. When helping users:

1. Identify which mental models apply to their situation
2. Explain the psychology behind the model
3. Provide specific marketing applications
4. Suggest how to implement ethically

Name each model you use and show how it applies to the user's actual page, offer, or campaign. A list of bias names with no implementation doesn't help anyone.

---

## Pick the Mode

| Mode | The user asks | What you do |
|---|---|---|
| **Diagnose** | "Why isn't this converting?" about a page, flow, or campaign | Read the asset through a behavioral lens: which principles it violates or leaves unused. Start with the Diagnostic Checks below |
| **Apply** | "Use psychology to improve this" | Recommend 3-5 principles, each with a concrete implementation tied to a real element of the asset |
| **Reference** | "Explain anchoring" or "which models help with X?" | Explain the model, its marketing applications, and a before/after example |

---

## The Catalog

The full catalog of 72 models, each with the psychology behind it and a marketing application, is in [references/mental-models.md](references/mental-models.md). Open the categories you need; the Quick Reference below tells you which models to look up for a given problem.

| Category | Models | Examples | Typical use |
|---|---|---|---|
| Foundational Thinking | 14 | First Principles, Jobs to Be Done, Inversion, Pareto, Second-Order Thinking | Strategy, positioning, choosing what to fix |
| Understanding Buyers & Human Psychology | 22 | Endowment Effect, Zero-Price Effect, Paradox of Choice, Social Proof | Conversion, pricing, onboarding |
| Influencing Behavior & Persuasion | 13 | Reciprocity, Scarcity, Loss Aversion, Anchoring, Decoy Effect | Copy, CTAs, offers |
| Pricing Psychology | 5 | Charm Pricing, Rule of 100, Good-Better-Best | Pricing pages, discount framing |
| Design & Delivery | 10 | Hick's Law, AIDA, Nudge Theory, BJ Fogg Behavior Model | UX, forms, onboarding, campaign design |
| Growth & Scaling | 8 | Network Effects, Flywheel, Switching Costs, Compounding | Growth strategy, retention |

---

## Quick Reference

When facing a marketing challenge, consider:

| Challenge | Relevant Models |
|-----------|-----------------|
| Low conversions | Hick's Law, Activation Energy, BJ Fogg, Friction |
| Pricing page | Anchoring, Decoy Effect, Good-Better-Best, Charm Pricing, Rule of 100 |
| Price objections | Anchoring, Framing, Mental Accounting, Loss Aversion |
| Building trust | Authority, Social Proof, Reciprocity, Pratfall Effect |
| Increasing urgency | Scarcity, Loss Aversion, Zeigarnik Effect |
| Retention/churn | Endowment Effect, Switching Costs, Status-Quo Bias |
| Growth stalling | Theory of Constraints, Local vs Global Optima, Compounding |
| Decision paralysis | Paradox of Choice, Default Effect, Nudge Theory |
| Onboarding | Goal-Gradient, IKEA Effect, Commitment & Consistency, BJ Fogg, Default Effect |
| Email sequence engagement | Reciprocity, Zeigarnik Effect, Goal-Gradient, Commitment & Consistency |
| Ad creative | Mere Exposure, Pratfall Effect, Contrast Effect, Framing |
| Referral program | Reciprocity, Social Proof, Network Effects, Unity Principle |

---

## Diagnostic Checks

In Diagnose mode, check these first. Each is a common gap with a direct fix:

- **No social proof on a landing page.** Add real testimonials, customer counts, or logos near the decision point (Social Proof, Authority).
- **Pricing tiers shown as equals.** There is no anchor and no recommended option. Mark the target tier and order the tiers so the comparison favors it (Anchoring, Decoy Effect, Default Effect).
- **A CTA that names an action instead of a gain.** "Submit" or "Get started" vs. "Start my free trial" (Endowment Effect, Loss Aversion).
- **Too many form fields or choices.** Cut them, or move them to a later step (Hick's Law, Activation Energy).
- **No reason to act now.** If a real deadline, limit, or seasonal window exists, show it. If none exists, leave urgency out (Scarcity).

---

## Use It Ethically

Use only scarcity, urgency, and social proof that are true. Set defaults that serve the customer, and make opting out as easy as opting in. Fake countdown timers, invented review counts, and pre-selected add-ons the buyer didn't ask for are manipulation: they erode trust once noticed and create legal liability.

Treat every principle as a hypothesis for this audience. Before rolling a change out widely, test it (see **ab-testing**).

---

## Task-Specific Questions

1. What specific behavior are you trying to influence? (Click, buy, share, return?)
2. What does your customer believe before encountering your marketing?
3. Where in the journey (awareness → consideration → decision) is this, and in what context (first visit, returning user, comparing options)?
4. What's currently preventing the desired action? (Too many choices, unclear value, no reason to act now?)
5. What's the buyer's emotional state? (Excited, skeptical, confused, impatient?)
6. What's the risk tolerance? (A high-stakes B2B purchase or a low-stakes impulse buy?)
7. Have you tested this with real customers?

---

## Output Format

| Request | Deliver |
|---|---|
| "Why isn't this converting?" | The principles violated or unused, each with the specific fix and where it goes |
| "Apply psychology to this page" | 3-5 principles, each with a concrete implementation and a way to test it |
| "Explain [principle]" | The definition, its marketing applications, and a before/after example |
| Pricing psychology audit | Principle-by-principle recommendations for the pricing page; for the price level itself, see **pricing** |
| A playbook for a goal | 5-7 models chosen for that goal, in the order to apply them |

For each recommendation, say whether it rests on the user's own data or is a hypothesis to test.

---

## Related Skills

- **cro**: Apply psychology to page optimization
- **copywriting**: Write copy using psychological principles
- **pricing**: Price levels, tiers, and packaging; this skill supplies the buyer-behavior lens
- **popups**: Use triggers and psychology in popups
- **onboarding**, **emails**, **referrals**: Where the onboarding, email, and referral rows of the Quick Reference get built
- **ab-testing**: Test psychological hypotheses

Sources and credits: [SOURCES.md](SOURCES.md)
