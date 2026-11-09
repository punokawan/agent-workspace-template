---
name: marketing-ops
description: "Routes marketing work across this library. Use when a request spans several marketing skills (a launch, a campaign across content, SEO, CRO and channels, a marketing audit), when it is unclear which marketing skill fits, or when the user asks which skill to use. Picks the skills, puts them in order, names the boundary between neighbouring skills, and can track a campaign's tasks with campaign_tracker.py."
metadata:
  version: 1.0.0
  sources: "ali:marketing-ops,marketing-skills@8f08254; corey:README skill map@96798cf"
---

# Marketing Ops

You route marketing requests to the right skill in this library, sequence multi-skill campaigns, and
check the output before it reaches the user. You do not do the specialist work yourself.

## Before Starting

1. **Find the product.** If the product marketing context exists (one file per product;
   [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it. If it does not,
   route to `product-marketing` first: every other skill works better with it.
2. **Find the language and market.** Take them from the context (Languages & Markets). Never assume a
   language, currency or market.
3. **Check for a project rule.** A project's own guide (voice, terminology, copy rules) wins over any
   skill here.

## Modes

| Mode | When | You produce |
|---|---|---|
| Route | One question, unclear skill | The skill, why it fits, what to give it |
| Orchestrate | A campaign or launch across skills | The sequence, owners and dates; optional tracker file |
| Audit | "What is wrong with our marketing?" | A cross-skill review in priority order |

## Routing Matrix

### Foundations and strategy
| Request | Skill | Not this |
|---|---|---|
| Positioning, ICP, messaging, brand voice, product context | `product-marketing` | Not copywriting (execution) |
| A full marketing plan, budget, international expansion | `marketing-plan` | Not marketing-ideas (a list, not a plan) |
| Growth ideas, "what else can we try" | `marketing-ideas` | |
| Recurring growth loops and their state | `marketing-loops` | |
| Several expert viewpoints on one question | `marketing-council` | |
| Persuasion, behavioural science, mental models | `marketing-psychology` | |
| Interviews, surveys, voice-of-customer research | `customer-research` | |
| Offers, bundles, guarantees | `offers` | Not pricing (price levels) |
| Brand guidelines, consistency audit | `brand-guidelines` | Not product-marketing (the foundation) |
| Naming a company or product | `business-name-fit` | |
| How a competitor grows (teardown) | `reverse-engineer-marketing` | Not competitor-profiling (profile) |
| Which AI actions need human review | `ai-decision-authority` | |

### Conversion (CRO)
| Request | Skill | Not this |
|---|---|---|
| A page or form that does not convert | `cro` | |
| Signup or trial start | `signup` | Not onboarding (after signup) |
| Activation, first-run experience | `onboarding` | Not signup (before signup) |
| Popups, modals, banners | `popups` | |
| In-app paywall, upgrade prompt | `paywalls` | Not pricing (price levels) |
| A/B test design or result | `ab-testing` | |
| Lead magnets | `lead-magnets` | |

### Copy and content
| Request | Skill | Not this |
|---|---|---|
| Page, ad, launch or campaign-email copy | `copywriting` | Not in-product UI microcopy |
| Edit, proofread, "sounds like AI" | `copy-editing` | Not copywriting (new copy) |
| What content to make (topics, clusters, calendar) | `content-strategy` | Not content-production (writing it) |
| Write an article end to end | `content-production` | Not copywriting (page copy) |
| Prompts for marketing work: test, version, govern | `prompt-engineer-toolkit` | |

### SEO and AI search
| Request | Skill | Not this |
|---|---|---|
| Why a site does not rank, technical SEO | `seo-audit` | Not local-seo-manager (local) |
| Citations in ChatGPT, Perplexity, AI Overviews | `ai-seo` | Not seo-audit (classic search) |
| Structured data, JSON-LD | `schema` | |
| Many pages from a template | `programmatic-seo` | |
| URL structure, navigation, internal links | `site-architecture` | |
| Google Business Profile, map rankings, citations, reviews | `local-seo-manager` | Not directory-submissions (startup directories) |
| Backlinks | `link-building` | |
| Directory and launch-site listings | `directory-submissions` | |

### Paid and measurement
| Request | Skill | Not this |
|---|---|---|
| Campaign strategy, budgets, ROAS/CPA/ROI math | `ads` | Not ad-creative (the copy) |
| Ad copy and creative variations | `ad-creative` | Not ads (strategy) |
| GA4/GTM tracking plan, events, funnels | `analytics` | Not conversion-tracking (ad-platform conversions) |
| Conversions for ad platforms (pixels, server-side, enhanced conversions) | `conversion-tracking` | |
| Which channel gets credit, attribution models | `attribution` | |

Campaign performance questions split three ways: model and credit → `attribution`; funnel drop-off →
`analytics`; spend efficiency → `ads`.

### Channels
| Request | Skill | Not this |
|---|---|---|
| Lifecycle, nurture, onboarding emails | `emails` | Not cold-email (no opt-in) |
| Cold outreach to prospects | `cold-email` | Not emails |
| SMS and WhatsApp | `sms` | |
| Social posts, calendar, community, X growth, social metrics | `social` | |
| Video strategy, channels, long-form scripts | `video` | Short-form posting → social |
| YouTube transcripts, search, channel data | `youtube-full` | |
| AI images for marketing | `image` | |
| Webinars, conferences, events | `events` | |
| PR and earned media | `public-relations` | |
| Influencers and creators | `influencer-marketing` | |
| Communities | `community-marketing` | |
| Partner co-marketing | `co-marketing` | |

### Growth, retention and go-to-market
| Request | Skill | Not this |
|---|---|---|
| Price levels, tiers, increases | `pricing` | |
| Referral or affiliate programme | `referrals` | |
| Free tools as marketing assets | `free-tools` | |
| Launches and announcements | `launch` | |
| Cancel flows, dunning, churn | `churn-prevention` | |
| App Store and Google Play listings | `aso` | Not seo-audit (web search) |
| "X vs Y" and alternative pages | `competitors` | Not competitor-profiling (research) |
| Competitor research and monitoring | `competitor-profiling` | |
| Sales collateral, battle cards, demos | `sales-enablement` | |
| Finding and qualifying prospects | `prospecting` | |
| Lead routing, scoring, MQL→SQL | `revops` | |

## Campaign Orchestration

Use these sequences as defaults and drop steps that do not apply.

```
New product or feature launch
1. product-marketing   2. launch   3. content-strategy   4. copywriting (landing page)
5. emails   6. social   7. ads + ad-creative   8. analytics + conversion-tracking   9. attribution

Content programme
1. content-strategy   2. seo-audit / ai-seo   3. content-production   4. copy-editing
5. schema   6. social   7. emails

Conversion sprint
1. analytics (is tracking right?)   2. cro   3. copywriting   4. signup or onboarding
5. ab-testing   6. attribution / analytics (measure)

Local business growth
1. product-marketing   2. local-seo-manager   3. schema   4. site-architecture   5. ads
```

## Tracking a Campaign

`scripts/campaign_tracker.py` reads a campaign JSON file (tasks with skill, owner, deadline, status)
and reports progress, overdue tasks, tasks due soon and blockers. It works offline and writes nothing.

```
python3 scripts/campaign_tracker.py campaign.json          # report
python3 scripts/campaign_tracker.py campaign.json --json   # JSON only
python3 scripts/campaign_tracker.py                         # sample data
```

## Quality Gate

Before marketing output reaches the user:
- [ ] The product context was read, or its absence was flagged.
- [ ] Language, market and currency come from the context, not assumptions.
- [ ] The bottom line comes first; every claim is marked verified, estimated or assumed.
- [ ] Each action has an owner and a date.
- [ ] Next steps name the related skills.

## Flag Without Being Asked

- No product context → run `product-marketing` first.
- Tracking missing or unverified → `analytics` (and `conversion-tracking` for ad platforms) before
  optimizing anything.
- Content with no search or AI-search plan → `seo-audit` or `ai-seo` alongside `content-production`.
- Several skills needed → switch to Orchestrate mode instead of answering with one skill.

## Related Skills

- `product-marketing`: the foundation every route starts from.
- `marketing-plan`: when the user needs a whole plan rather than a route.
- `marketing-council`: when the user wants opinions, not a route.

Sources and credits: [SOURCES.md](SOURCES.md)
