# Merge mapping: two upstream marketing libraries into one `marketing-skills`

Status: merge complete (2026-11-09). Full reasoning per topic: [COMPARISON.md](COMPARISON.md).

Sources (snapshots in `.cache/marketing-merge/sources/` of the workspace, read-only):

| Key | Upstream | Commit | Version | License |
|---|---|---|---|---|
| `corey` | github.com/coreyhaines31/marketingskills | 96798cf | 2.14.2 | MIT, (c) Corey Haines |
| `ali` | github.com/alirezarezvani/claude-skills, folder `marketing-skill/` | 8f08254 | 2.14.10 | MIT, (c) 2025 Alireza Rezvani |

Base rule: the plugin starts from `corey` verbatim (all 53 skills and `tools/`). A merged skill keeps the
`corey` name. Content from `ali` is folded in only where it adds something `corey` lacks. A skill that
exists only in `ali` keeps its `ali` name.

## Overlapping topics (merge work, by batch)

| Batch | Merged skill | corey source | ali source(s) |
|---|---|---|---|
| B1 CRO | `cro` | cro | page-cro, form-cro |
| B1 CRO | `signup` | signup | signup-flow-cro |
| B1 CRO | `onboarding` | onboarding | onboarding-cro |
| B1 CRO | `popups` | popups | popup-cro |
| B1 CRO | `paywalls` | paywalls | paywall-upgrade-cro |
| B1 CRO | `ab-testing` | ab-testing | ab-test-setup |
| B2 SEO | `seo-audit` | seo-audit | seo-audit |
| B2 SEO | `ai-seo` | ai-seo | aeo |
| B2 SEO | `schema` | schema | schema-markup |
| B2 SEO | `programmatic-seo` | programmatic-seo | programmatic-seo |
| B2 SEO | `site-architecture` | site-architecture | site-architecture |
| B2 SEO | `local-seo-manager` (kept; now also holds corey's former seo-audit local references) | seo-audit local references | local-seo-manager |
| B3 Copy & content | `copywriting` | copywriting | copywriting |
| B3 Copy & content | `copy-editing` | copy-editing | copy-editing |
| B3 Copy & content | `content-strategy` | content-strategy | content-strategy |
| B3 Copy & content | `marketing-psychology` | marketing-psychology | marketing-psychology |
| B3 Copy & content | `content-production` (keep or fold) | — | content-production |
| B3 Copy & content | `content-humanizer` (keep or fold) | — | content-humanizer |
| B4 Paid & measurement | `ads` | ads | paid-ads |
| B4 Paid & measurement | `ad-creative` | ad-creative | ad-creative |
| B4 Paid & measurement | `analytics` | analytics | analytics-tracking |
| B4 Paid & measurement | `attribution` / `campaign-analytics` (keep or fold) | attribution | campaign-analytics |
| B4 Paid & measurement | `marketing-demand-acquisition` (keep or fold) | (ads, marketing-plan) | marketing-demand-acquisition |
| B5 Channels | `emails` | emails | email-sequence |
| B5 Channels | `cold-email` | cold-email | cold-email |
| B5 Channels | `social` | social | social-content, social-media-manager |
| B5 Channels | `social-media-analyzer` (keep or fold) | (social, analytics) | social-media-analyzer |
| B5 Channels | `x-twitter-growth` (keep or fold) | (social) | x-twitter-growth |
| B5 Channels | `events` | events | webinar-marketing |
| B5 Channels | `video` | video | video-content-strategist (in `video-content-strategist/skills/`) |
| B6 Growth | `pricing` | pricing | pricing-strategy |
| B6 Growth | `referrals` | referrals | referral-program |
| B6 Growth | `free-tools` | free-tools | free-tool-strategy |
| B6 Growth | `launch` | launch | launch-strategy |
| B6 Growth | `churn-prevention` | churn-prevention | churn-prevention |
| B6 Growth | `marketing-ideas` | marketing-ideas | marketing-ideas |
| B7 Foundations | `product-marketing` | product-marketing | marketing-context |
| B7 Foundations | `competitors` | competitors | competitor-alternatives |
| B7 Foundations | `aso` | aso | app-store-optimization |
| B7 Foundations | `marketing-strategy-pmm` (keep or fold) | (product-marketing, competitor-profiling, sales-enablement, launch, marketing-plan) | marketing-strategy-pmm |

"Keep or fold": keep a separate skill only when its core job is not covered by a `corey` skill. Otherwise
fold its unique content into the covering skill (new section or `references/*.md`) and drop the folder.

## Single-source skills (no merge work)

- From `corey`, already in place: attribution (unless B4 folds into it), co-marketing, community-marketing,
  competitor-profiling, conversion-tracking, customer-research, directory-submissions, image,
  influencer-marketing, lead-magnets, link-building, marketing-council, marketing-loops, marketing-plan,
  offers, prospecting, public-relations, reverse-engineer-marketing, revops, sales-enablement, sms.
- From `ali`, already copied: ai-decision-authority, brand-guidelines, business-name-fit,
  local-seo-manager, prompt-engineer-toolkit, youtube-full.
- Rebuilt at the end by the controller: router `marketing-ops` (from ali marketing-ops + marketing-skills
  index, over the final skill list).
- Dropped: ali `content-creator` (deprecated alias), ali `marketing-skills` (index, replaced by the router).

## Old name → merged name (use when fixing cross-links)

page-cro→cro, form-cro→cro, signup-flow-cro→signup, onboarding-cro→onboarding, popup-cro→popups,
paywall-upgrade-cro→paywalls, ab-test-setup→ab-testing, aeo→ai-seo, schema-markup→schema,
paid-ads→ads, analytics-tracking→analytics, email-sequence→emails, social-content→social,
social-media-manager→social, webinar-marketing→events, video-content-strategist→video,
pricing-strategy→pricing, referral-program→referrals, free-tool-strategy→free-tools,
launch-strategy→launch, marketing-context→product-marketing, competitor-alternatives→competitors,
app-store-optimization→aso, content-creator→content-production, marketing-skills→marketing-ops.

Keep-or-fold results (final):

- content-humanizer→copy-editing; content-production kept.
- campaign-analytics→attribution (models), analytics (funnels), ads (ROAS, CPA, ROI).
- marketing-demand-acquisition→ads (paid acquisition), marketing-plan (demand planning, budget), revops (MQL→SQL).
- social-media-analyzer→social; x-twitter-growth→social.
- marketing-strategy-pmm→product-marketing (positioning, ICP, messaging), competitor-profiling (intelligence), launch (launch tiers), marketing-plan (international go-to-market).
- local-seo-manager kept; ai-decision-authority, brand-guidelines, business-name-fit, prompt-engineer-toolkit, youtube-full kept.

## Central passes (controller, after all batches)

- Product context location per project and audience language (`product-marketing` defines it; other
  skills point to it).
- Router `marketing-ops`, plugin manifest, LICENSE, UPSTREAM.md, README.md, COMPARISON.md.
- Validation: frontmatter, unique names, links, scripts compile, security scan.
