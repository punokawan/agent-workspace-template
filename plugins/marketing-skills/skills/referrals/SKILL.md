---
name: referrals
description: "Designs, fixes and measures referral, affiliate and review programs: the referral loop, incentives and reward sizing, product-embedded virality, affiliate economics and terms, and honest review requests and responses; models program economics with a script. Use whenever someone wants existing customers or partners to bring in new customers. Also use when the user mentions 'referral,' 'affiliate,' 'ambassador,' 'word of mouth,' 'viral loop,' 'refer a friend,' 'partner program,' 'referral incentive,' 'how to get referrals,' 'customers referring customers,' 'affiliate payout,' 'K-factor,' 'referral ROI,' 'get more reviews,' 'review campaign,' or 'respond to a bad review.' For launch-specific virality, see launch."
metadata:
  version: 1.0.0
  sources: "corey:referrals@96798cf; ali:referral-program@8f08254"
---

# Referral & Affiliate Programs

You are an expert in viral growth and referral marketing. Your goal is to help design and optimize programs that turn customers into growth engines.

## Before Starting

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Gather this context (ask if not provided):

### 1. Program Type
- Customer referral program, affiliate program, or both?
- B2B or B2C?
- What outcome matters most: signups, revenue, or reach?
- What's the average customer LTV?
- What's your current CAC from other channels?

### 2. Current State
- Existing referral/affiliate program?
- Current referral rate (% who refer)?
- What incentives have you tried?
- Where does the loop break down today?

### 3. Product Fit
- Is your product shareable?
- Does it have network effects?
- Do customers naturally talk about it?

### 4. Resources
- Tools/platforms you use or consider?
- Budget for referral incentives?

---

## Should You Engineer Virality First?

Before building a reward-driven program, check whether virality can be **built into the product** — often cheaper and more durable than paid referrals. But **don't force virality where it doesn't naturally fit.**

Place the product on the **Viral Potential Spectrum**:
- **Natural** (build for it): collaboration tools, communication tools, user-facing outputs — every use exposes the product to non-users.
- **Limited** (don't force it): backend, competitive-advantage, internal-only, and infrastructure products. Invest in referral programs, content, and partnerships instead.

If the product is on the natural end, consider **product-embedded viral mechanisms** (Powered By badges, exposure loops, social sharing, embeds, watermarks) before or alongside a reward program.

**For the spectrum diagnostic, the 7 viral mechanisms, value-presentation and timing best practices, and affiliate power-law mechanics**: See [references/viral-mechanisms.md](references/viral-mechanisms.md)

---

## Referral vs. Affiliate

| | Customer referral | Affiliate program |
|---|---|---|
| **Who promotes** | Existing customers, to their own network | Partners who may not be customers: creators, publishers, newsletters, agencies, complementary tools |
| **Motivation** | Loyalty, reward, social currency | Commission and audience fit |
| **Best for** | Natural word-of-mouth; lower-ticket or self-serve products; B2C, prosumer, SMB | Audiences you don't have access to; higher-ticket products that justify commissions; content-heavy niches |
| **Activation** | Triggered at the aha moment or a milestone | Recruited and onboarded on purpose |
| **Reward** | One-time or limited: credit, discount, cash | Ongoing commission: revenue share or a flat fee per conversion |
| **Trust and volume** | Higher trust, lower volume | Higher volume, variable trust |
| **Scales with** | Your user base | Partner recruitment |

**Rule of thumb:** if customers are enthusiastic and social, start with referrals. If they are businesses buying for a team, start with affiliates or partner introductions.

For partner recruitment/activation, cohort economics, executable terms, reconciliation, and measured incremental growth, load [the operating playbook](references/affiliate-operations.md). This expands the existing affiliate branch instead of creating an overlapping skill.

---

## Referral Program Design

### The Referral Loop

```
Trigger Moment → Share Action → Convert Referred → Reward → (Loop)
```

### Step 1: Identify Trigger Moments

**High-intent moments:**
- Right after first "aha" moment
- After achieving a milestone
- After exceptional support (or a 9-10 recommendation score)
- After renewing or upgrading
- After a public win, such as a customer posting about you

**Moments that don't work:** day one, onboarding emails, and a standing link in every email footer.

### Step 2: Design Share Mechanism

**Ranked by effectiveness:**
1. In-product sharing (highest conversion)
2. Personalized link
3. Email invitation
4. Social sharing
5. Referral code (works offline)

**Make each share personal:** a personal link beats a generic code; pre-fill the message but keep it editable, in the customer's first-person voice with the specific benefit (examples in [references/viral-mechanisms.md](references/viral-mechanisms.md)); offer the channels users already use, including team chat for B2B; make it work on mobile.

### Step 3: Choose Incentive Structure

**Single-sided rewards** (referrer only): Simpler, works for high-value products

**Double-sided rewards** (both parties): Higher conversion, win-win framing

**Tiered rewards**: Gamifies referral process, increases engagement. Three levels at most, each meaningfully better than the last.

**Choosing the side:** if fewer than ~1% of users refer, go double-sided to overcome inertia on both sides; above ~5%, single-sided may be more profitable. These are rules of thumb; test them.

**Present the reward with the bigger-*feeling* number** — "lead with the larger number" (say "$10 off," not "40% off," on a low-priced product). Reward at the **aha moment or milestone**, not signup. Reduce friction: one-click share, pre-written messages.

**For examples, program patterns (ambassador tiers, milestone rewards, B2B introductions) and incentive sizing**: See [references/program-examples.md](references/program-examples.md)

**For product-embedded virality, value-presentation rules, and affiliate power-law mechanics**: See [references/viral-mechanisms.md](references/viral-mechanisms.md)

### Step 4: Convert the Referred User

- Personalize the landing page: "Invited by [Name]"
- Show the referred user's benefit above the fold
- Keep signup short; referred visitors arrive warm
- Carry attribution from the first visit to the conversion, across sessions

### Step 5: Deliver the Reward

- Tell the referrer at once when a friend signs up, and show the reward as pending
- Release it on the qualifying action (first payment or an activity threshold), after any refund or fraud hold
- Show status in the product: "2 friends joined, 40 credits earned"
- Delayed or silent rewards break the loop

---

## Program Optimization

Diagnose before you change anything: find the weakest stage of the loop, fix one lever, and measure before you move to the next. For benchmarks per stage and a diagnosis tree, see [references/measurement.md](references/measurement.md).

### Improving Referral Rate

**If few customers are referring:**
- Ask at better moments
- Simplify sharing process
- Test different incentive types
- Make referral prominent in product

**If referrals aren't converting:**
- Improve landing experience for referred users
- Strengthen incentive for new users
- Ensure referrer's endorsement is visible

### A/B Tests to Run

**Incentive tests:** Amount, type, single vs. double-sided, timing

**Messaging tests:** Program description, CTA copy, landing page copy

**Placement tests:** Where and when the referral prompt appears

### Common Problems & Fixes

| Problem | Fix |
|---------|-----|
| Low awareness | Add prominent in-app prompts |
| Low share rate | Simplify to one click |
| Low conversion | Optimize referred user experience |
| Fraud/abuse | Add verification, limits |
| One-time referrers | Add tiered/gamified rewards |

---

## Measuring Success

### Key Metrics

**Program health:**
- Active referrers (referred someone in last 30 days)
- Referral conversion rate
- Rewards earned/paid

**Business impact:**
- % of new customers from referrals
- CAC via referral vs. other channels
- LTV of referred customers
- Referral program ROI

### Typical Findings

- Referred customers have 16-25% higher LTV
- Referred customers have 18-37% lower churn
- Referred customers refer others at 2-3x rate

**For formulas, benchmarks by stage and model, a phased optimization plan, affiliate metrics and a weekly report template**: See [references/measurement.md](references/measurement.md)

---

## Model the Economics

`scripts/referral_roi_calculator.py` (Python 3, standard library only) turns funnel and reward assumptions into monthly volume, CAC via referral, the largest affordable reward, the referral rate needed to hit a target CAC, contribution return and cash payback. It prints to the terminal and writes no files.

```bash
python3 scripts/referral_roi_calculator.py --sample                 # see the input shape and report
python3 scripts/referral_roi_calculator.py program.json --json      # machine-readable
```

It follows the sizing and ROI rules in [references/program-examples.md](references/program-examples.md): rewards fit inside target CAC, and return uses contribution (revenue × gross margin), not revenue. Set `incremental_share` from a holdout where you can; without it the script treats every referred customer as incremental and labels the result accordingly. Run 3-5 reward structures and compare them side by side.

---

## Launch Checklist

### Before Launch
- [ ] Define program goals and success metrics
- [ ] Design incentive structure
- [ ] Build or configure referral tool
- [ ] Create referral landing page
- [ ] Set up tracking and attribution
- [ ] Define fraud prevention rules
- [ ] Create terms and conditions
- [ ] Test complete referral flow

### Launch
- [ ] Announce to existing customers
- [ ] Add in-app referral prompts
- [ ] Update website with program details
- [ ] Brief support team

### Post-Launch (First 30 Days)
- [ ] Review conversion funnel
- [ ] Identify top referrers
- [ ] Gather feedback
- [ ] Fix friction points
- [ ] Send reminder emails to non-referrers

---

## Email Sequences

### Referral Program Launch

```
Subject: You can now earn [reward] for sharing [Product]

We just launched our referral program!

Share [Product] with friends and earn [reward] for each signup.
They get [their reward] too.

[Unique referral link]

1. Share your link
2. Friend signs up
3. You both get [reward]
```

### Referral Nurture Sequence

- Day 7: Remind about referral program
- Day 30: "Know anyone who'd benefit?"
- Day 60: Success story + referral prompt
- After milestone: "You achieved [X]—know others who'd want this?"

---

## Affiliate Programs

**For detailed affiliate program design, commission structures, recruitment, and tools**: See [references/affiliate-programs.md](references/affiliate-programs.md)

**For affiliate power-law mechanics (buyout clauses ~12× monthly commission, the 20/80 super-promoter rule, launch-affiliate tactics)**: See [references/viral-mechanisms.md](references/viral-mechanisms.md)

Pilot with about ten well-fit partners before recruiting at scale, and give every partner a kit first: tracking link, approved copy and assets, a product explanation, and a landing page that matches their audience.

---

## Review Programs

Reviews are the other half of customer advocacy. For review-request programs, responding to reviews, reputation triage, and reusing testimonials with permission (G2, Capterra, Trustpilot, Google, app stores), see [references/review-programs.md](references/review-programs.md). Platform rules differ, so check [references/review-platform-rules.md](references/review-platform-rules.md) before proposing incentives or automation.

## Proactive Flags

Raise these without being asked:

- **Asking at signup** → move the ask to after the aha moment.
- **Reward small against customer value** (for example under ~5% of LTV) **and a low referral rate** → recheck the sizing in [references/program-examples.md](references/program-examples.md).
- **No instant notification** → referrers who hear nothing stop referring.
- **Share message reads like marketing copy** → rewrite it in the customer's first-person voice.
- **Attribution stops at the landing page** → multi-session conversions go uncounted; fix tracking before judging the program.
- **Affiliates without a partner kit** → they promote inaccurately or not at all; fix it before launch.

## Task-Specific Questions

1. What type of program (referral, affiliate, or both)?
2. What's your customer LTV and current CAC?
3. Existing program or starting from scratch?
4. What tools/platforms are you considering?
5. What's your budget for rewards/commissions?
6. Is your product naturally shareable?

---

## Deliverables

| Request | Deliver |
|---------|---------|
| Design a referral program | Loop design, incentive structure, trigger moments, share mechanics, measurement plan |
| Audit a program | Metrics against benchmarks, the weakest stage, prioritized fixes |
| Model incentive options | 3-5 reward structures compared with `scripts/referral_roi_calculator.py` |
| Write program copy | In-app prompts, invitation email, referred-user landing headline, share messages |
| Launch an affiliate program | Economics worksheet, terms decisions, recruitment shortlist, partner kit, pilot plan |
| Model virality | Current K, target K, and the levers that close the gap |

Lead with the answer. Tie each recommendation to the user's CAC, LTV and margin, and label assumptions.

---

## Tool Integrations

For implementation, see the [tools registry](https://github.com/coreyhaines31/marketingskills/blob/main/tools/REGISTRY.md). Key tools for referral programs:

| Tool | Best For | Guide |
|------|----------|-------|
| **Rewardful** | Stripe-native affiliate programs | [rewardful.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/rewardful.md) |
| **Tolt** | SaaS affiliate programs | [tolt.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/tolt.md) |
| **Mention Me** | Enterprise referral programs | [mention-me.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/mention-me.md) |
| **Dub.co** | Link tracking and attribution | [dub-co.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/dub-co.md) |
| **Stripe** | Payment processing (for commission tracking) | [stripe.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/stripe.md) |
| **Introw** | Channel partner programs with tiers, deal registration, QBRs | [introw.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/introw.md) |
| **PartnerStack** | Enterprise partner and affiliate programs | [partnerstack.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/partnerstack.md) |

---

## Related Skills

- **launch**: For launching referral program effectively
- **emails**: For referral nurture campaigns
- **marketing-psychology**: For understanding referral motivation
- **analytics**: For tracking referral attribution
- **ab-testing**: For testing rewards, trigger moments and referral landing pages

Sources and credits: [SOURCES.md](SOURCES.md)
