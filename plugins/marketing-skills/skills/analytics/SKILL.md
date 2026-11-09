---
name: analytics
description: "Plans, implements, audits, and debugs analytics tracking, and reads funnel drop-off from the user's own counts. Use when the user wants to set up, improve, or audit analytics tracking and measurement, or mentions 'set up tracking,' 'GA4,' 'Google Analytics,' 'event tracking,' 'UTM parameters,' 'tag manager,' 'GTM,' 'tracking plan,' 'event naming,' 'how do I measure this,' 'Mixpanel,' 'Segment,' 'are my events firing,' 'events firing twice,' 'analytics isn't working,' 'where do users drop off,' or 'funnel conversion.' Use this whenever someone asks how to know if something is working. For getting conversions into ad platforms (pixels, conversion tags, CAPI, server-side) and verifying they arrived, see conversion-tracking. For attribution models, MMM, incrementality, or reconciling numbers across tools, see attribution. For ROAS, CPA, and campaign ROI math, see ads. For A/B test measurement, see ab-testing. Rate metrics divide matching closed windows — never full-period spend by partial-period results."
metadata:
  version: 1.0.0
  sources: "corey:analytics@96798cf; ali:analytics-tracking,campaign-analytics@8f08254"
---

# Analytics Tracking

You are an expert in analytics implementation and measurement. Your goal is to help set up tracking that provides actionable insights for marketing and product decisions.

**Scope.** This skill owns what to track and how it reaches the analytics tool: the tracking plan, event names and properties, GA4 and GTM, UTMs, debugging, and funnel reads. It stops where conversions must reach an ad platform (pixels, conversion tags, Conversions API, imports, "GA4 and Google Ads don't match"): that is **conversion-tracking**. Crediting channels is **attribution**; spend, ROAS, and CPA math is **ads**.

## Initial Assessment

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before implementing tracking, understand:

1. **Business Context** - What decisions will this data inform? What are key conversions?
2. **Current State** - What tracking exists? What tools are in use?
3. **Technical Context** - What's the tech stack? Any privacy/compliance requirements?
4. **Mode** - Building from scratch (start at the Tracking Plan Framework), auditing tracking nobody trusts (use the Tracking Audit output), or debugging one broken event (go to [references/debugging-playbook.md](references/debugging-playbook.md))?

---

## Core Principles

### 1. Track for Decisions, Not Data
- Every event should inform a decision
- Avoid vanity metrics
- Quality > quantity of events

### 2. Start with the Questions
- What do you need to know?
- What actions will you take based on this data?
- Work backwards to what you need to track

### 3. Name Things Consistently
- Naming conventions matter
- Establish patterns before implementing
- Document everything

### 4. Maintain Data Quality
- Validate implementation
- Monitor for issues
- Clean data > more data

### 5. Compute, Don't Eyeball
- Derive every total, rate, and delta from row-level data with a script or
  spreadsheet — never by scanning rows and summing mentally. One silently
  dropped row corrupts every figure downstream of it.
- Cross-check each headline figure a second, independent way (a
  reconciliation total, a recomputation from a different grouping) before
  reporting it, and chase any mismatch to the exact row.
- When a claim is about one segment — a single campaign, ad set, channel, or
  week — report that segment's own numbers. Never fold it into a neighboring
  group and let the group's total speak for it.

### 6. Match Observation Windows
- A rate or efficiency metric divides a numerator and denominator that cover
  the same closed observation window. Never divide a full period's spend by a
  partial period's conversions or revenue — restate both over the weeks that
  actually have data, and say which weeks those are.
- Cohort rates use only cohorts whose observation window has ended. A trial
  or signup still inside its window is pending, not failed — exclude it from
  the denominator and label it as pending rather than counting it against
  the rate.

### 7. Recommend Against the Stated Goal
- Analysis ends in a recommendation, and the recommendation must be argued
  from the goal the brief states — the launch target, audience, revenue, or
  positioning objective — not only from what is operationally easiest.
  Name which stated goal each option serves and what it trades away.

---

## Tracking Plan Framework

### Structure

```
Event Name | Category | Properties | Trigger | Notes
---------- | -------- | ---------- | ------- | -----
```

### Event Types

| Type | Examples |
|------|----------|
| Pageviews | Automatic, enhanced with metadata |
| User Actions | Button clicks, form submissions, feature usage |
| System Events | Signup completed, purchase, subscription changed |
| Custom Conversions | Goal completions, funnel stages |

**For comprehensive event lists**: See [references/event-library.md](references/event-library.md)

---

## Event Naming Conventions

### Recommended Format: Object-Action

```
signup_completed
button_clicked
form_submitted
article_read
checkout_payment_completed
```

### Best Practices
- Lowercase with underscores
- Be specific: `cta_hero_clicked` vs. `button_clicked`
- Include context in properties, not event name
- Avoid spaces and special characters
- Document decisions
- Keep provider-defined names when using automatic or recommended events (e.g. GA4 `click`, `view_search_results`, `purchase`). Map internal business names explicitly; naming a custom event does not make the provider collect it automatically.
- Use one verb per meaning (`_completed`, never also `_done` or `_finished`). The standard verb list is in [references/event-library.md](references/event-library.md) § Naming Vocabulary.
- Mark each property in the plan as required or optional. QA fails an event that arrives without a required property.

---

## Essential Events

### Marketing Site

| Event | Properties |
|-------|------------|
| cta_clicked | button_text, location |
| form_submitted | form_type |
| signup_completed | method, source |
| demo_requested | - |

### Product/App

| Event | Properties |
|-------|------------|
| onboarding_step_completed | step_number, step_name |
| feature_used | feature_name |
| purchase_completed | plan, value |
| subscription_cancelled | reason |

**For full event library by business type**: See [references/event-library.md](references/event-library.md)

---

## Event Properties

### Standard Properties

| Category | Properties |
|----------|------------|
| Page | page_title, page_location, page_referrer |
| User | user_id, user_type, account_id, plan_type |
| Campaign | source, medium, campaign, content, term |
| Product | product_id, product_name, category, price |

### Best Practices
- Use consistent property names
- Include relevant context
- Don't duplicate automatic properties
- Avoid PII in properties

---

## GA4 Implementation

### Quick Setup

1. Create GA4 property and data stream
2. Install gtag.js or GTM
3. Enable enhanced measurement, then turn off each automatic event you will also send from GTM (outbound clicks, file downloads, video), or it counts twice
4. Configure custom events
5. Mark key events in Admin (GA4's name for conversions since 2024). Mark only the few that drive decisions or ad bidding; a property allows 30

### Event Example

```javascript
// GA4's recommended sign_up event, not a custom name, so it feeds built-in reports.
// Your tracking plan can still call this signup_completed; map the name explicitly.
gtag('event', 'sign_up', {
  'method': 'email',
  'plan': 'free'
});
```

**For detailed GA4 implementation**: See [references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Container Structure

| Component | Purpose |
|-----------|---------|
| Tags | Code that executes (GA4, pixels) |
| Triggers | When tags fire (page view, click) |
| Variables | Dynamic values (click text, data layer) |

### Data Layer Pattern

```javascript
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});
```

**For detailed GTM implementation**: See [references/gtm-implementation.md](references/gtm-implementation.md)

---

## UTM Parameter Strategy

### Standard Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| utm_source | Traffic source | google, newsletter |
| utm_medium | Marketing medium | cpc, email, social |
| utm_campaign | Campaign name | spring-sale |
| utm_content | Differentiate versions | hero-cta |
| utm_term | Paid search keywords | running-shoes |

### Naming Conventions
- **Lowercase everything.** GA4 treats `LinkedIn` and `linkedin` as two sources, and the split never merges back.
- **Hyphens between words.** No spaces, underscores, or `+`. Pick one separator for the whole company; this skill uses hyphens.
- **One spelling per source.** `linkedin`, never also `li` or `linkedin.com`. Keep the allowed values in a shared sheet and build links from it.
- **No personal data.** Never put emails, names, phone numbers, or user IDs in a UTM. They land in analytics reports and in referrer logs, and Google's terms prohibit sending PII to GA4.
- **Specific but short:** `blog-footer-cta`, not `cta1`.
- **Test the final URL.** Shorteners and redirects can drop or double parameters. Click the live link and check the landing URL before the campaign ships.
- **External links only.** A UTM on a link between your own pages overwrites the visitor's real source. Tag links that bring people in, never links within the site.

### UTM Patterns by Partner Type

Partner links break most often because each deal gets named on the spot. Fix the pattern per partner type once: `utm_medium` names the kind of deal, `utm_source` names who sent the traffic.

| Partner type | utm_source | utm_medium | utm_campaign | utm_content |
|---|---|---|---|---|
| Newsletter | `{partner}` (one per partner, across all their publications) | `newsletter` | `{partner}-{publication}-{yyyy}-{mm}` | `{placement}-{yyyy-mm-dd}` |
| Creator (YouTube, LinkedIn, TikTok) | `{platform}` | `creator` | `{creator}` | `{post-date}` or the video ID |
| Podcast | `{podcast}` | `podcast` | `{podcast}-{yyyy}-{mm}` | `{spot}-{yyyy-mm-dd}` (pre-roll, mid-roll) |
| Affiliate | `{partner}` | `affiliate` | `{partner}-affiliate` | placement, if they have several |
| Community | `{community}` | `community` | `{community}-{program}` | the channel or post, if known |

- **Use `creator` as the medium for paid creator deals**, not `social` (which mixes them with your organic posts) or `video` (which mixes them with paid video ads). The platform goes in `utm_source`.
- **One link per placement.** A newsletter that runs you on two dates gets two links, so each date's clicks stay separate. The monthly `utm_campaign` rolls them up.
- **Add a custom channel group in GA4.** GA4's default grouping sends mediums like `newsletter`, `creator`, `podcast`, and `community` to Unassigned (only `affiliate` and `email` map to a default channel). Create a channel group with a rule per medium so partner traffic shows up as its own channels.
- Podcast and video links often aren't clickable, so pair the UTM link with a promo code or vanity URL. See **influencer-marketing** for the rest of partner measurement.

*The partner-type pattern is adapted from Wispr Flow's link-creator skill (MIT), published in the skills.marketing library.*

### Traffic From AI Assistants

You can't tag links that ChatGPT, Claude, Perplexity, Gemini, or Copilot put in their answers. Some of those visits arrive with a referrer (`chatgpt.com`, `perplexity.ai`) or an assistant-added `utm_source`; many arrive as direct, or come later through a branded search.

- Add a GA4 channel group rule that matches known assistant referrers and sources into an "AI assistants" channel, and update the list as new assistants appear.
- Treat that channel as the floor. Assistant-driven visits that show up as direct or branded search can be most of the effect, and they won't carry the referrer.
- For measuring the full effect (exposure, delayed visits, and longer attribution windows), see **ai-seo**. For reconciling it with other sources, see **attribution**.

---

## Debugging and Validation

### Testing Tools

| Tool | Use For |
|------|---------|
| GA4 DebugView | Real-time event monitoring |
| GTM Preview Mode | Test triggers before publish |
| Browser Extensions | Tag Assistant, dataLayer Inspector |

### Validation Checklist

- [ ] Events firing on correct triggers
- [ ] Property values populating correctly
- [ ] No duplicate events
- [ ] Works across browsers and mobile
- [ ] Conversions recorded correctly
- [ ] No PII leaking

### Common Issues

| Issue | Check |
|-------|-------|
| Events not firing | Trigger config, GTM loaded |
| Wrong values | Variable path, data layer structure |
| Duplicate events | Multiple containers, trigger firing twice |

For the layer-by-layer method (dataLayer → GTM → network request → GA4) and fixes per symptom, see [references/debugging-playbook.md](references/debugging-playbook.md).

### Flag Without Being Asked

Raise these when you see them during any task:

- **An event fires on every page load** → misconfigured trigger; the counts are inflated.
- **No `user_id` on events from signed-in users** → analytics cannot join the CRM or build cohorts.
- **Pages report as `(not set)` or one generic path** → single-page app route changes are not tracked (see [references/gtm-implementation.md](references/gtm-implementation.md) § Single-Page App Page Views).
- **Paid campaigns arrive as direct** → UTMs missing or stripped by a redirect.
- **No consent mode where consent is required** → legal exposure, and the numbers are under-reported without anyone knowing by how much.
- **GA4 and an ad platform disagree on conversions** → hand to **conversion-tracking** before calling it a bug.

---

## Privacy and Compliance

### Considerations
- Cookie consent required in EU/UK/CA
- No PII in analytics properties
- Data retention settings
- User deletion capabilities

### Implementation
- Use consent mode (wait for consent). Basic mode sends nothing until the visitor consents; advanced mode sends cookieless pings before consent so GA4 can model the declined share. Say which one the numbers come from.
- IP anonymization
- Only collect what you need
- Integrate with consent management platform

---

## Funnel Analysis

When the question is where people drop off, why conversions fell, or which segment converts worse, compute the rates instead of reading them off a chart (Core Principle 5):

```bash
python3 scripts/funnel_analyzer.py --file funnel.json   # one funnel, or segments sharing the stages
python3 scripts/funnel_analyzer.py --file funnel.json --json
```

It reports stage conversion, drop-off, cumulative conversion, the largest absolute and relative drop, and the lift in final conversions one more point at each stage would give, and warns when counts rise between stages (stages not nested or windows mismatched). Run it with no arguments for a demo. For how to define stages, read the output, and route each bottleneck to the owning skill, see [references/funnel-analysis.md](references/funnel-analysis.md).

---

## Output Format

### Tracking Plan Document

```markdown
# [Site/Product] Tracking Plan

## Overview
- Tools: GA4, GTM
- Last updated: [Date]

## Events

| Event Name | Description | Properties | Trigger |
|------------|-------------|------------|---------|
| signup_completed | User completes signup | method, plan | Success page |

## Custom Dimensions

| Name | Scope | Parameter |
|------|-------|-----------|
| user_type | User | user_type |

## Conversions

| Conversion | Event | Counting |
|------------|-------|----------|
| Signup | signup_completed | Once per session |
```

### Tracking Audit

1. **Bottom line first** — what is broken or missing, before the method.
2. **Coverage gaps** — each funnel step from the tracking plan with its event status: tracked and verified, tracked but wrong, or missing.
3. **Findings** — each one gives what is wrong, why it matters (which decision or report it corrupts), and the fix, with an owner.
4. **Confidence** — mark each finding verified (seen in DebugView, Preview, or the network request), estimated, or assumed.
5. **Prioritized fix list** — conversion events and data-quality faults (duplicates, missing required properties, PII) first.

---

## Task-Specific Questions

1. What tools are you using (GA4, Mixpanel, etc.)?
2. What key actions do you want to track?
3. What decisions will this data inform?
4. Who implements - dev team or marketing?
5. Are there privacy/consent requirements?
6. What's already tracked?

---

## Tool Integrations

For implementation, see the [tools registry](https://github.com/coreyhaines31/marketingskills/blob/main/tools/REGISTRY.md). Key analytics tools:

| Tool | Best For | MCP | Guide |
|------|----------|:---:|-------|
| **GA4** | Web analytics, Google ecosystem | ✓ | [ga4.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/ga4.md) |
| **Mixpanel** | Product analytics, event tracking | - | [mixpanel.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/mixpanel.md) |
| **Amplitude** | Product analytics, cohort analysis | - | [amplitude.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/amplitude.md) |
| **PostHog** | Open-source analytics, session replay | - | [posthog.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/posthog.md) |
| **Segment** | Customer data platform, routing | - | [segment.md](https://github.com/coreyhaines31/marketingskills/blob/main/tools/integrations/segment.md) |

---

## Related Skills

- **ab-testing**: For experiment tracking
- **conversion-tracking**: For getting conversions (including GA4 key events from forms and bookings) to ad platforms and GA4, and verifying they arrive
- **attribution**: For attribution models, multi-touch/MMM/incrementality, and reconciling conflicting numbers across tools (once tracking is live)
- **seo-audit**: For organic traffic analysis
- **cro**: For conversion optimization (uses this data)
- **revops**: For pipeline metrics, CRM tracking, and revenue attribution
- **ads**: For campaign ROAS, CPA, and ROI math on spend data (its campaign calculator)

Sources and credits: [SOURCES.md](SOURCES.md)
