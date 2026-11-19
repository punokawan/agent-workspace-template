# Sources: seo-audit

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md (frontmatter) | edited: local triggers moved to local-seo-manager; added E-E-A-T, cannibalization, and migration triggers; version reset to 1.0.0; sources added; 2026-11-19: claude-seo pointer sentence and sources added |
| frontmatter | ali `seo-audit` @8f08254 | skills/seo-audit/SKILL.md § Proactive Triggers | edited: the migration trigger became a description phrase |
| SKILL.md § Initial Assessment | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Initial Assessment | edited: product context pointer now refers to product-marketing (per-product location, central pass) |
| SKILL.md § Audit Framework | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Audit Framework | as is |
| SKILL.md § Technical SEO Audit | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Technical SEO Audit | edited: speed factors and tools lists moved to references/core-web-vitals.md |
| SKILL.md § Technical SEO Audit | ali `seo-audit` @8f08254 | skills/seo-audit/SKILL.md § Audit Framework | edited: three-band Core Web Vitals table and the 75th-percentile rule replace the single thresholds |
| SKILL.md § Technical SEO Audit | claude-seo `seo-technical` @468ed5b | skills/seo-technical/SKILL.md § 1. Crawlability, § 2. Indexability, § 3. Security (back-button hijacking), § JavaScript SEO: Canonical & Indexing Guidance (December 2025) | new: dated facts on fetch limits (2 MB HTML, 64 MB PDF), crawl-rate setting removed Jan 2024, canonical re-evaluation up to two weeks, JS canonical/noindex/non-200 rules (Dec 2025), back-button hijacking policy (2026-04-13, enforced 2026-06-15) |
| SKILL.md § International SEO & Localization | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § International SEO & Localization | as is |
| SKILL.md § On-Page SEO Audit | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § On-Page SEO Audit | edited; 2026-11-19: meta description 150-160 characters corrected to a ~120-160 truncation heuristic (Google publishes no limit); "lazy loading implemented" corrected to never lazy-load the LCP or first image |
| SKILL.md § On-Page SEO Audit | claude-seo `seo-page` @468ed5b | skills/seo-page/SKILL.md § Step 1: Run the Deterministic Checks (length-threshold note, `first-image-lazy-loaded`), § What to Analyze (On-Page SEO) | new: basis for the meta description and lazy-loading corrections |
| SKILL.md § Content Quality Assessment | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Content Quality Assessment | edited: E-E-A-T bullets condensed into a table; full list moved to references/eeat.md; 2026-11-19: engagement metrics (time on page, bounce rate) marked as UX diagnostics, not documented Google ranking signals |
| SKILL.md § Content Quality Assessment | ali `seo-audit` @8f08254 | skills/seo-audit/references/eeat-framework.md § The four signals | edited: trust-first rule and the YMYL line |
| SKILL.md § Common Issues by Site Type | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Common Issues by Site Type | edited: local pointer now names the local-seo-manager skill |
| SKILL.md § Output Format | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Output Format | edited: Priority field uses the four-level scale |
| SKILL.md § Output Format | ali `seo-audit` @8f08254 | skills/seo-audit/scripts/seo_health_scorer.py (docstring) | edited: severity levels with fix-by times became the priority scale table |
| SKILL.md § Output Format | ali `seo-audit` @8f08254 | skills/seo-audit/SKILL.md § Output Artifacts, § Communication | edited: keyword cannibalization map as a table; plain-language and evidence rule |
| SKILL.md § References | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § References | edited: added core-web-vitals and eeat; local entry points to local-seo-manager |
| SKILL.md § Tools Referenced | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Tools Referenced | edited: retired Mobile-Friendly Test replaced by Lighthouse; duplicate schema note folded into one line |
| SKILL.md § Tools Referenced | ali `seo-audit` @8f08254 | skills/seo-audit/SKILL.md § Tools | edited: usage and limits of the bundled on-page checker |
| SKILL.md § Task-Specific Questions | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Task-Specific Questions | as is |
| SKILL.md § Measure with claude-seo | claude-seo `seo-audit`, `seo-page`, `seo-technical`, `seo-google`, `seo-sitemap` @468ed5b | skills/seo/SKILL.md § Quick Reference; skills/seo-audit/SKILL.md; skills/seo-page/SKILL.md; skills/seo-technical/SKILL.md; skills/seo-google/SKILL.md; skills/seo-sitemap/SKILL.md | new: pointers to /seo commands |
| SKILL.md § Related Skills | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Related Skills | edited: added local-seo-manager |
| SKILL.md § Related Skills | ali `seo-audit` @8f08254 | skills/seo-audit/SKILL.md § Related Skills | edited: content-strategy entry |
| references/ai-writing-detection.md | corey `seo-audit` @96798cf | skills/seo-audit/references/ai-writing-detection.md | as is |
| references/international-seo.md | corey `seo-audit` @96798cf | skills/seo-audit/references/international-seo.md | as is |
| references/title-tags.md | corey `seo-audit` @96798cf | skills/seo-audit/references/title-tags.md | as is |
| references/rankings-push.md | corey `seo-audit` @96798cf | skills/seo-audit/references/rankings-push.md | as is |
| references/core-web-vitals.md | ali `seo-audit` @8f08254 | skills/seo-audit/references/cwv-thresholds.md | edited: CLS font fix corrected (metric-matched fallback or `font-display: optional`), LCP and INP fixes expanded, field-data lag added |
| references/core-web-vitals.md | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Technical SEO Audit (Speed Factors, Tools) | edited: moved here from SKILL.md |
| references/eeat.md | ali `seo-audit` @8f08254 | skills/seo-audit/references/eeat-framework.md | edited: checklist kept; YMYL rule reworded (experience supports but does not replace expertise); scorer mapping dropped |
| references/eeat.md | corey `seo-audit` @96798cf | skills/seo-audit/SKILL.md § Content Quality Assessment (E-E-A-T Signals) | edited: bullets merged into the checklist |
| references/eeat.md § What not to do | aeo-box (MIT, Alireza Rezvani) via ali `aeo` @8f08254 | skills/aeo/references/aeo_eeat_canon.md § Anti-Patterns | edited: fabricated credentials and outbound-link authority, credit line kept in the file |
| scripts/seo_checker.py | ali `seo-audit` @8f08254 | skills/seo-audit/scripts/seo_checker.py | edited: --domain now works, og:description no longer counts as a meta description, alt="" treated as decorative, canonical and robots-meta checks added, http(s)-only fetch with size cap, plain-text output |
| evals/evals.json | corey `seo-audit` @96798cf | skills/seo-audit/evals/evals.json | edited: local cases 11–13 moved to local-seo-manager/evals/evals.json |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
