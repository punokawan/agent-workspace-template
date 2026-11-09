# Comparison: two marketing skill libraries

Full topic-by-topic comparison of the two libraries this plugin merges, and what the merge took from each.

- **corey** = [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) @ `96798cf` (v2.14.2), MIT, Corey Haines
- **ali** = [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) `marketing-skill/` @ `8f08254` (v2.14.10), MIT, Alireza Rezvani

## At a glance

| | corey | ali | merged |
|---|---|---|---|
| Skills | 53 | 50 | 61 |
| Markdown files (excl. SOURCES.md) | 339 | 156 | 390 |
| Markdown lines | 61,411 | 34,780 | 69,938 |
| Script files in skills | 29 | 62 | 61 |

37 merged skills take material from both libraries. Topics both cover use corey as the base: in almost every shared topic ali's skill is an older fork of corey's plus ali-only blocks (flags, deliverables, output tables, scripts). ali-only skills keep their name; ali skills whose job a corey skill already covers were folded in, never kept as a second skill (one skill per topic).

## How it was compared

Seven domain batches (CRO, SEO, copy and content, paid and measurement, channels, growth, foundations). For each topic the ali version was read in full and the corey SKILL.md in full with its references, each aspect was judged, and the stronger text kept. Every ali script was read, compiled, run with `--help` and on sample input; scripts that gave misleading results, wrote outside a user-given path or only filled templates were dropped. Each skill's `SOURCES.md` records, part by part, where its content came from.

## Where the ali skills went

See [MAPPING.md](MAPPING.md) for the full old-name → merged-name list. Keep-or-fold results:

| ali skill | Result |
|---|---|
| page-cro, form-cro | folded into `cro` |
| content-humanizer | folded into `copy-editing` |
| content-production | kept |
| campaign-analytics | split: models → `attribution`, funnels → `analytics`, ROAS/CPA/ROI → `ads` |
| marketing-demand-acquisition | folded: paid → `ads`, planning → `marketing-plan`, MQL→SQL → `revops` |
| social-content, social-media-manager, social-media-analyzer, x-twitter-growth | folded into `social` |
| webinar-marketing | folded into `events` |
| video-content-strategist | folded into `video` |
| marketing-strategy-pmm | folded: positioning → `product-marketing`, intelligence → `competitor-profiling`, launch tiers → `launch`, international GTM → `marketing-plan` |
| local-seo-manager | kept (now also holds corey's former seo-audit local references) |
| ai-decision-authority, brand-guidelines, business-name-fit, prompt-engineer-toolkit, youtube-full | kept as is (light edits) |
| marketing-ops + marketing-skills | rebuilt as the router `marketing-ops` |
| content-creator | dropped (deprecated alias) |

## B1: CRO

Sources: corey = coreyhaines31/marketingskills @96798cf · ali = alirezarezvani/claude-skills `marketing-skill/` @8f08254.
Every ali skill in this batch is an older fork of the matching corey skill, plus four ali-only blocks (Communication, Proactive Triggers, Output Artifacts, WHEN/WHEN NOT related skills) and, for five of the seven, a Python script. Per-file provenance is in each skill's `SOURCES.md`.

| Merged | corey | ali | Base | Added from ali | Kept/folded | Score corey/ali |
|---|---|---|---|---|---|---|
| `cro` | cro | page-cro, form-cro | corey | audit output standards, routing conditions, required-field rule, lead-quality check, form output standards, form field analyzer (fixed) | both folded into `cro`; form playbook and conversion_audit.py dropped | 4/3 |
| `signup` | signup | signup-flow-cro | corey | leak-routing table, audit standards, auth-options table, funnel drop analyzer (fixed) | folded; playbook dropped (duplicate) | 4/3 |
| `onboarding` | onboarding | onboarding-cro | corey | symptom diagnostics, output standards, activation funnel analyzer with what-if (fixed) | folded | 5/3 |
| `popups` | popups | popup-cro | corey | output standards (frequency rule, full copy set, mobile, compliance), onboarding link | folded; playbook dropped (duplicate) | 4/3 |
| `paywalls` | paywalls | paywall-upgrade-cro | corey | diagnostics, the missing Output Format, emails and pricing links | folded | 4/3 |
| `ab-testing` | ab-testing | ab-test-setup | corey | sample size calculator (reworked to match corey's tables), sizing rule, cross-check caveat | folded; both ali references dropped (older or duplicate) | 5/2 |

### cro
- Sources: corey `cro` (198 lines, 2 refs, 0 scripts) · ali `page-cro` (232 lines, 0 refs, 1 script) + `form-cro` (219 lines, 1 ref, 1 script)
- Coverage: corey has reference routing, a 248-line page-experiments reference, a newer form reference (current enrichment examples, label rationale), the revops lead-routing hand-off and evals / ali adds audit output standards (severity per dimension, fix vs. test, traffic context), WHEN/WHEN NOT routing to signup, onboarding, popups, copywriting and ab-testing, the "every required field needs a downstream use" rule with a 3-5 field ceiling, a lead-quality diagnosis, form output standards, and two scripts
- Quality: corey 4 · ali 3 — ali's text is mostly an older copy of corey's; its own additions are useful, but both scripts are weak (the page scorer rates its demo 100/100; the form analyzer misses labels that come before their inputs)
- Taken from ali:
  - Output Artifacts (severity summary, at most five quick wins, rationale/effort/metric, test-ideas table) → SKILL.md § Output Format
  - Communication points 2, 4, 5, 6 (tie to dimension, apply page-type framework, fix vs. test, traffic and audience context) → SKILL.md § Output Format, audit standards
  - WHEN/WHEN NOT conditions, plus onboarding and analytics lines → SKILL.md § Related Skills
  - Proactive triggers "new page before launch" and "bad lead quality" → SKILL.md frontmatter description
  - Core principles (3-5 field ceiling, 7+ required fields is high priority, required fields need a downstream use, phone/company size/address friction) → references/form.md § Core Principles 4
  - "Leads but bad quality" trigger → references/form.md § When the Complaint Is Lead Quality
  - Communication points 1-6 and the top 3-5 hypotheses rule → references/form.md § Output Standards
  - analytics-tracking related line → references/form.md § Related Skills, as `analytics`
  - form_field_analyzer.py, with fixes → scripts/form_field_analyzer.py; usage → SKILL.md § Form Optimization › Form Field Analyzer
- Dropped from ali:
  - page-cro body (Initial Assessment through Task-Specific Questions) → older copy of corey's text
  - form-cro body and references/form-cro-playbook.md → older copy of corey's references/form.md
  - conversion_audit.py → keyword-count heuristic: its demo page scores 100/100, it counts phrases such as "learn more" as CTAs and rewards five or more CTAs (against the one-primary-action rule), and it cannot judge value-proposition clarity, the framework's top dimension; reading the page under the framework covers the same signals with judgement
  - "Open the audit with the conversion_audit score" → script dropped; the dimension severity summary replaces it
  - Proactive triggers 1, 3, 4, 5 (page-cro) and 1, 2, 4, 5 (form-cro) → already in corey's description triggers and page-type frameworks, or are offers to run the skill during other work
  - Copy alternatives as a side-by-side table → corey already requires 2-3 alternatives with rationale; format left open
  - marketing-context line and the `.claude/product-marketing-context.md` path → corey's Initial Assessment covers the context file; the central pass owns its path
  - Form analyzer's 0-100 score and the "#1 abandonment trigger" and "~5-10% per field" claims → arbitrary or unsourced
- Conflicts resolved:
  - Field-count bands: ali script (over 7 = issue, 5-7 = warning) and ali text (3-5 ceiling) vs. corey (3 = baseline, 4-6 = 10-25% loss, 7+ = 25-50%+) → script uses corey's bands; ali's 3-5 ceiling kept as a decision rule in form.md
  - ali documented the analyzer as reading `forms.json`; the script reads HTML → documented as HTML
  - Audit order: ali opens with the script score, corey with the framework → corey's order kept
- Result: SKILL.md 221 lines (was 198) + refs 689 lines (form.md 441, experiments.md 248); scripts kept: form_field_analyzer.py (431 lines); SOURCES.md 28 rows

### signup
- Sources: corey `signup` (363 lines, 0 refs, 0 scripts) · ali `signup-flow-cro` (233 lines, 1 ref, 1 script)
- Coverage: corey has the enrichment and sales-assist routing note, the newer label rationale and evals; ali's playbook repeats corey's core sections / ali adds routing by where the funnel leaks (page vs. form vs. activation vs. paid conversion), "instrument drop-off before testing", audit standards (field-removal test, SSO always considered, post-submit always covered, mobile separate, fix vs. test), an auth-options decision table, field sets by step, and the funnel drop analyzer
- Quality: corey 4 · ali 3 — same core text; ali's standards and analyzer add rigor, but the analyzer had an arbitrary health score and misattributed landing-page causes
- Taken from ali:
  - WHEN/WHEN NOT routing, the "start at the worst step" rule and the low-trial-conversion check → SKILL.md § Find Where the Flow Leaks (new)
  - funnel_drop_analyzer.py, with fixes → scripts/funnel_drop_analyzer.py; usage → SKILL.md § Measurement › Find the Drop-Off Step
  - Output Artifacts (field set by step, copy per screen, SSO and auth decision table) → SKILL.md § Output Format
  - Communication points 2-6 → SKILL.md § Output Format, audit standards
  - Related-skill conditions and the paywall-upgrade-cro line (as `paywalls`) → SKILL.md § Related Skills
  - "Should we require a credit card?" trigger → SKILL.md frontmatter description
- Dropped from ali:
  - SKILL.md body and references/signup-cro-playbook.md → older copy of corey's text
  - Analyzer's 0-100 funnel health score (log scale against a fixed 10% target) → arbitrary; healthy end-to-end rates differ by funnel
  - Session-recording vendor names in the analyzer → generic wording
  - Proactive triggers 1, 3, 5 → covered by the onboarding route, corey's trial experiments and the mobile section
  - marketing-context line → covered by corey's Initial Assessment
- Conflicts resolved:
  - ali signup-flow-cro says "users sign up but don't activate" is a signup audit; ali onboarding-cro calls it an activation problem → routed to onboarding, with signup keeping only the post-submit experience (matches corey's eval 6)
  - Analyzer attached landing-page content advice to drops into the landing step → each drop now gets causes for the step people failed to reach; the landing stage covers load, redirects and tracking
- Result: SKILL.md 404 lines (was 363), no refs; scripts kept: funnel_drop_analyzer.py (236 lines); SOURCES.md 27 rows

### onboarding
- Sources: corey `onboarding` (267 lines, 3 refs, 0 scripts) · ali `onboarding-cro` (257 lines, 0 refs, 1 script)
- Coverage: corey has onboarding psychology, the 10-component toolkit, a cohort-and-window aha-moment method that separates correlation from causation, minimum path to value, activation models, an experiments reference and evals / ali adds symptom-to-diagnosis rules (early retention, signup-to-first-action drop, trial-to-paid, onboarding emails), output standards (lead with the highest-leverage finding, name the step or metric), richer artifacts (activation definition, email trigger map, experiment backlog), and an activation analyzer with a what-if projection
- Quality: corey 5 · ali 3 — corey's activation method is rigorous; ali's aha-moment advice is correlation-only and its analyzer led with an arbitrary score, but its diagnostics and projection are useful
- Taken from ali:
  - Proactive triggers 1-5 (2 and 3 merged) → SKILL.md § Diagnose Before Prescribing (new)
  - activation_funnel_analyzer.py, with fixes and `--recover` → scripts/activation_funnel_analyzer.py; usage → SKILL.md § Measurement
  - Communication (lead with highest-leverage finding, name step/metric/trigger, brand voice) → SKILL.md § Output Format
  - Output Artifacts (activation definition, flow with drop-offs and branches, checklist copy, email trigger map, experiment backlog) → SKILL.md § Output Format
  - paywall-upgrade-cro "not before value" condition and popup-cro line → SKILL.md § Related Skills, as `paywalls` and `popups`
  - "Low day-1 or day-7 retention" trigger → SKILL.md frontmatter description
- Dropped from ali:
  - Older copies of corey's sections, including the correlation-only "Find Your Aha Moment" → corey's cohort method is stronger
  - Activation score 0-100 (20% activation = 100) and "lead with the score" → arbitrary target; the audit now leads with the highest-leverage finding
  - marketing-context "always load" line → covered by corey's Initial Assessment
- Conflicts resolved:
  - ali onboarding-cro sends in-product modals and tooltips to popup-cro, while ali popup-cro sends them back to onboarding-cro → onboarding owns in-app onboarding (tours, tooltips, checklists, which corey already covers); popups is linked only for overlay trigger, frequency and dismissal rules, and popups points in-app onboarding work back here
  - "Halve the worst drop" was presented as a gain → labeled an upper bound; the recovered share is a parameter
- Result: SKILL.md 294 lines (was 267) + refs 367 lines (activation-models 60, experiments 258, minimum-path-to-value 49); scripts kept: activation_funnel_analyzer.py (200 lines); SOURCES.md 31 rows

### popups
- Sources: corey `popups` (453 lines, 0 refs, 0 scripts) · ali `popup-cro` (229 lines, 1 ref, 0 scripts)
- Coverage: corey holds all popup guidance (ali's playbook is an older copy of it), the lead-magnets link and evals / ali adds output standards (name trigger, audience and frequency rule for every popup; complete copy set; proactive compliance), mobile adaptation notes, a compliance checklist, success metrics per test, and an onboarding link for in-app modals
- Quality: corey 4 · ali 3 — identical core; ali's standards make the deliverable more complete
- Taken from ali:
  - Communication (trigger/audience/frequency per popup, complete copy set, compliance) → SKILL.md § Output Format
  - Output Artifacts (mobile adaptation, compliance checklist, test success metric) → SKILL.md § Output Format
  - onboarding-cro related line → SKILL.md § Related Skills, as `onboarding`
  - "Low email list growth" trigger → SKILL.md frontmatter description
- Dropped from ali:
  - SKILL.md body and references/popup-cro-playbook.md → older copy of corey's text
  - Proactive triggers 2-5 → covered by corey's Trigger Strategies, Audience Targeting and Compliance sections; trigger 5 (popups to lift trial signups) is a speculative cross-sell
  - "Preview text" in the copy set → no meaning for a popup
  - marketing-context line → covered by corey's Initial Assessment
- Conflicts resolved:
  - In-app modal ownership → see onboarding
- Result: SKILL.md 459 lines (was 453), no refs, no scripts (ali had none); SOURCES.md 22 rows

### paywalls
- Sources: corey `paywalls` (230 lines, 2 refs, 0 scripts) · ali `paywall-upgrade-cro` (258 lines, 0 refs, 0 scripts)
- Coverage: corey has the mobile subscription-app reference (store fees, plan presentation, review checklist), the experiments reference, the fake-countdown dark pattern and evals / ali adds the output deliverables corey lacked (trigger map, full screen copy, upgrade flow, anti-pattern audit, test backlog), "confirm the aha moment first", the limit-frustration vs. wrong-audience split, "decide free vs. paid before placing paywalls", and an emails link
- Quality: corey 4 · ali 3 — corey is broader and current, but had no output format; ali supplies it
- Taken from ali:
  - Communication ("confirm aha first") and proactive triggers 1-3 → SKILL.md § Diagnose Before Designing (new)
  - Output Artifacts and the complete-copy and ethical-alternative rules → SKILL.md § Output Format (new)
  - onboarding-cro condition and email-sequence line → SKILL.md § Related Skills, as `onboarding` and `emails`
- Dropped from ali:
  - SKILL.md body → older copy of corey's text
  - Proactive trigger 4 (audit a shared trial-expiry screen) → folded into the anti-pattern audit output
  - Proactive trigger 5 (store billing rules) → corey's references/mobile-subscription-paywalls.md covers it in depth
  - marketing-context line → covered by corey's Initial Assessment
- Conflicts resolved: none
- Result: SKILL.md 262 lines (was 230) + refs 237 lines (experiments 168, mobile-subscription-paywalls 69); no scripts (ali had none); SOURCES.md 23 rows

### ab-testing
- Sources: corey `ab-testing` (361 lines, 2 refs, 0 scripts) · ali `ab-test-setup` (316 lines, 2 refs, 1 script)
- Coverage: corey has correct p-value and confidence-interval interpretation, a results table that forbids extending a finished fixed-horizon test, triggered analysis for opt-in elements, the growth experimentation program (ICE, velocity, playbook, cadence), corrected sample-size tables and an unequal-allocation duration formula / ali adds a sample size and duration calculator, the "size before approval" rule and cross-check calculators
- Quality: corey 5 · ali 2 — ali's calculator is the best script in the batch, but its text says p < 0.05 means "<5% chance the result is random", tells you to add traffic to an inconclusive test, and its reference tables overstate samples about 2.3x (1% baseline, 10% lift: 380,000 vs. 160,000 per variant), contradicting its own SKILL.md
- Taken from ali:
  - sample_size_calculator.py, reworked → scripts/sample_size_calculator.py; usage → SKILL.md § Sample Size › Calculate It
  - "Cross-check calculators" label → SKILL.md § Sample Size, with a fixed-horizon caveat
  - "Size a test" and "read a test result" triggers → SKILL.md frontmatter description
  - page-cro and analytics-tracking conditions and the pricing-strategy line → SKILL.md § Related Skills, as `cro`, `analytics`, `pricing`
- Dropped from ali:
  - SKILL.md body, including its Statistical Significance bullets and results table → incorrect; corey's versions kept
  - references/sample-size-guide.md → older, with tables about 2.3x too high
  - references/test-templates.md → identical to corey's apart from the contents list
  - Output Artifacts → covered by corey's references/test-templates.md (test plan with owner, duration and QA checklist; results template; hypothesis bank)
  - Proactive triggers → covered by description triggers; "suggest a test instead of guessing" conflicts with cro's fix-vs.-test rule
  - campaign-analytics related line → its final name depends on batch B4 (keep or fold)
  - Calculator's 0-100 design-quality score → replaced by flags
  - marketing-context line → covered by corey's Initial Assessment
- Conflicts resolved:
  - Formula: ali's calculator used unpooled variance; corey's tables use variance pooled under the null (checked: all 25 table cells match) → calculator switched to pooled; 1%/10% gives 163,095 (table 160k), 10%/50% gives 686 (table 690)
  - Quick reference: ali 163k and 683 vs. corey 160k and 690 → corey's two-significant-figure table kept; the script gives exact values
  - Duration flags: ali 30/90 days vs. corey's guide 7/30/60 days → corey's rules
  - ali said both linked calculators agree with the script → qualified: fixed-horizon calculators agree, sequential ones differ
- Result: SKILL.md 378 lines (was 361) + refs 555 lines (sample-size-guide 278, test-templates 277); scripts kept: sample_size_calculator.py (232 lines); SOURCES.md 27 rows

## B2: SEO and AI search

Sources: corey = coreyhaines31/marketingskills @96798cf · ali = alirezarezvani/claude-skills `marketing-skill/` @8f08254. Line counts are SKILL.md lines; refs are files under `references/`. Per-file provenance is in each skill's `SOURCES.md`.

In this batch ali's `seo-audit`, `schema-markup`, `programmatic-seo`, and `site-architecture` are older forks of the corey skills plus ali-only blocks (Proactive Triggers, Output Artifacts, Communication) and one or two Python scripts each. ali's `aeo` is a port of [alirezarezvani/aeo-box](https://github.com/alirezarezvani/aeo-box) (MIT), and `local-seo-manager` is a third-party contribution by Stan Varashilov (Steffonet). Two kept scripts fetch a URL the user passes (seo_checker.py, sitemap_analyzer.py): only that URL, http(s) only, with a size cap, and they write nothing. schema_validator.py, url_pattern_generator.py, and nap_checker.py read local files only.

| Merged | corey | ali | Base | Added from ali | Kept/folded | Score corey/ali |
|---|---|---|---|---|---|---|
| `seo-audit` | seo-audit | seo-audit | corey | three-band CWV table and reference, E-E-A-T reference, priority scale, cannibalization map, on-page checker (fixed) | folded; corey's local references moved to `local-seo-manager` | 5/3 |
| `ai-seo` | ai-seo | aeo | corey | takeaways block, page assembly, domain trust tactics, stable/fragile/gap prompt labels and drop diagnosis, fabricated-credentials rule | folded (aeo-box credit kept); 3 scripts dropped | 5/3 |
| `schema` | schema | schema-markup | corey | jobs workflow, page-type table and stacking rules, VideoObject, site-wide vs per-page, AI-entity section, error table, audit outputs, type checklists, validator (fixed) | folded | 4/3 |
| `programmatic-seo` | programmatic-seo | programmatic-seo | corey | URL-space sizing step with the URL pattern checker (reworked), monitoring table, opportunity table | folded | 5/3 |
| `site-architecture` | site-architecture | site-architecture | corey | Choose the Job (audit, plan, linking), constraints, directory test, nav rules, topic-cluster steps, linking priority, Structural Problems table, audit and URL-change outputs, linking playbook, URL design reference, sitemap analyzer (rewritten) | folded | 5/3 |
| `local-seo-manager` | (seo-audit local references) | local-seo-manager | corey local text, ali structure | jobs table, NAP checker (rewritten), audit checklist (rebuilt), review templates (neutralized), page outline, NAP-difference table, listing priority | kept (no corey skill covers local SEO); 2 scripts and 1 reference dropped | 5/2 |

New old→new names: none (`aeo`→`ai-seo` and `schema-markup`→`schema` are already in MAPPING; `local-seo-manager` keeps its name).

### seo-audit
- Sources: corey `seo-audit` (497 lines, 7 refs, 0 scripts) · ali `seo-audit` (172 lines, 4 refs, 2 scripts)
- Coverage: corey has the full audit framework, international SEO, title-tag rewrites, striking-distance pushes, AI-writing detection, the schema-detection caveat, evals, and three local references / ali has a three-band Core Web Vitals table, an E-E-A-T checklist with YMYL rules, severity levels with fix-by times, a cannibalization artifact, communication rules, and two scripts
- Quality: corey 5 · ali 3 — ali's body is a condensed older copy of corey's (its long reference repeats corey's text); its additions are useful but the scorer's weights are invented
- Taken from ali:
  - CWV three-band table and 75th-percentile rule → SKILL.md § Technical SEO Audit; cwv-thresholds.md (CLS font fix corrected) → references/core-web-vitals.md
  - eeat-framework.md → references/eeat.md; trust-first and YMYL lines → SKILL.md § Content Quality Assessment
  - severity levels (from seo_health_scorer.py) → SKILL.md § Output Format priority scale
  - cannibalization map, plain-language and evidence rule → SKILL.md § Output Format
  - migration trigger → frontmatter
  - seo_checker.py (fixed: --domain, og:description, decorative alt, canonical and robots checks, http(s)-only fetch with cap) → scripts/; usage → SKILL.md § Tools Referenced
  - fabricated-credentials anti-pattern (aeo-box, via `aeo`) → references/eeat.md
- Dropped from ali:
  - seo_health_scorer.py → weighted 0-100 score with invented category weights; only its severity scale survives
  - seo-audit-reference.md → older copy of corey's SKILL.md text
  - schema-types.md → covered by the `schema` skill
  - body sections (Initial Assessment, Audit Framework, Task-Specific Questions) → older copies of corey's
- Conflicts resolved: corey's single CWV thresholds replaced by the three-band table; Mobile-Friendly Test (retired) replaced by Lighthouse; local triggers and references moved to `local-seo-manager`
- Result: SKILL.md 498 lines, 6 refs (core-web-vitals, eeat added; three local refs moved out); scripts kept: seo_checker.py

### ai-seo
- Sources: corey `ai-seo` (500 lines, 15 refs, 0 scripts) · ali `aeo` (226 lines, 5 refs, 3 scripts)
- Coverage: corey has platform ranking factors, agent readiness, prompt portfolio, citation-vs-recommendation, attribution, answer accuracy, multilingual and commerce, and many sourced third-party credits / ali has extractable content patterns (takeaways block, page assembly), industry E-E-A-T signals, a bot-access and monitoring protocol, anti-patterns, and three scripts
- Quality: corey 5 · ali 3 — corey is broader and better sourced; aeo-box adds a few useful patterns but leans on numeric scores and a script that writes a local data store
- Taken from ali:
  - Pattern 7 (Key Takeaways block) and Combining Patterns → references/content-patterns.md (credit line)
  - industry E-E-A-T critical signals (health, finance, legal, e-commerce, publishing, education) → references/content-patterns.md § Domain-Specific GEO Tactics, without numeric thresholds
  - monitoring protocol and citation-ledger fields → references/prompt-portfolio.md § Classify prompts, then diagnose drops (rate-based labels, crawler names corrected)
  - fabricated credentials → SKILL.md § What NOT to Do item 4
- Dropped from ali:
  - aeo_audit.py → composite 0-100 E-E-A-T score with industry thresholds that no source supports
  - aeo_optimizer.py → deterministic rewriting of content; output quality not reliable enough to recommend
  - citation_tracker.py → writes to `~/.aeo-data/`, outside a user-given path; its ledger fields survive as a spreadsheet layout
  - aeo_vs_seo.md, llm_citation_patterns.md → covered by corey's How AI Search Works and platform-ranking-factors.md
- Conflicts resolved: training crawlers vs search/user agents (ali mixed them) follow corey's purpose split; "use only the blocks the query needs" aligned with Google's no-fragmenting guidance
- Result: SKILL.md 503 lines, 15 refs (2 edited); no scripts

### schema
- Sources: corey `schema` (191 lines, 1 ref, 0 scripts) · ali `schema-markup` (233 lines, 2 refs, 1 script)
- Coverage: corey has core principles, current Google feature support (FAQ and HowTo retired), examples, and evals / ali has audit/implement/fix modes, a page-type selection table, site-wide vs per-page scoping, a schema-and-AI section, a mistakes table, output artifacts, a types guide, implementation patterns, and a validator
- Quality: corey 4 · ali 3 — ali's structure is useful, but several claims were outdated (FAQ, HowTo, and sitelinks rich results; FAQPage raising AI citations)
- Taken from ali:
  - modes 1-3 → SKILL.md § Workflow by Job (rendered HTML first)
  - page-type table and stacking rules (rows corrected) → SKILL.md § Common Schema Types
  - VideoObject → SKILL.md § Quick Reference and references/schema-examples.md
  - Per-Page vs Site-Wide → SKILL.md § Multiple Schema Types
  - Schema and AI Search → SKILL.md § Schema for AI Search and Entities (evidence-based stance)
  - Common Mistakes, Testing & Validation, Proactive Triggers → SKILL.md § Validation and Testing error table
  - CMS shortcuts → SKILL.md § Implementation
  - Output Artifacts, Communication → SKILL.md § Output Format (verified/unverified)
  - schema-types-guide.md → references/type-checklists.md (corrected to current features)
  - duration and availability values → references/schema-examples.md § Values Reference
  - schema_validator.py (fixed: arrays, subtypes, URL/date/price/placeholder/retired-feature checks, --json, --demo) → scripts/
- Dropped from ali:
  - claims that FAQPage, HowTo, or sitelinks markup earns rich results → retired by Google
  - "Product inside Article is invalid" → not a rule
  - most of implementation-patterns.md → duplicates corey's schema-examples.md
- Conflicts resolved: required-property sets follow Google's feature pages; confidence emoji replaced by verified/unverified tied to rendering
- Result: SKILL.md 289 lines, 2 refs (type-checklists added); scripts kept: schema_validator.py

### programmatic-seo
- Sources: corey `programmatic-seo` (242 lines, 2 refs, 0 scripts) · ali `programmatic-seo` (288 lines, 0 refs, 1 script)
- Coverage: corey has the 12 playbooks with a reference, implementation platforms, and evals / ali has a URL-pattern step with a generator, a monitoring plan, opportunity analysis, communication rules, and proactive triggers
- Quality: corey 5 · ali 3 — ali is corey's older text plus a script that invented a quality score and missed slug collisions
- Taken from ali:
  - URL Pattern Generation step → SKILL.md § Implementation Framework step 3 "Size the URL Space"
  - url_pattern_generator.py (reworked: rows mode, Unicode slugs, collision, reverse-pair, empty-slug, unused-field checks; score removed) → scripts/
  - Post-Launch Monitoring Plan and "define before launch" → SKILL.md § Quality Checks table
  - Opportunity Analysis and thin-content callout → SKILL.md § Output Format
  - content-strategy related entry → SKILL.md § Related Skills
- Dropped from ali:
  - body sections → older copies of corey's
  - Proactive Triggers → already covered by the description and Initial Assessment
  - Playbook Selection Matrix artifact → duplicates corey's Choosing Your Playbook
- Conflicts resolved: none
- Result: SKILL.md 270 lines, 2 refs; scripts kept: url_pattern_generator.py

### site-architecture
- Sources: corey `site-architecture` (359 lines, 4 refs, 0 scripts) · ali `site-architecture` (289 lines, 2 refs, 1 script)
- Coverage: corey has site-type templates, ASCII and Mermaid sitemap formats, navigation patterns, URL patterns by page type, platform choice and migration, and evals / ali has audit/plan/linking modes, constraints, the directory test, topic-cluster steps, a linking priority stack, an architecture-mistakes table, proactive triggers, output artifacts, an internal-linking playbook, a URL design guide, and a sitemap analyzer
- Quality: corey 5 · ali 3 — ali covers audits and internal linking better, but has outdated advice (pagination canonical to page 1, 302 "passes no equity," the retired Search Console URL-parameter tool), anchor-text percentage quotas without a source, and a sitemap analyzer that promised orphan detection it never computed and failed on hreflang sitemaps
- Taken from ali:
  - How This Skill Works (modes 1-3) → SKILL.md § Choose the Job, with analyzer usage
  - Before Starting (current state, constraints) → SKILL.md § Before Planning
  - flat-vs-layered rule of thumb → SKILL.md § Page Hierarchy Design (directory test)
  - Primary Navigation Rules, nav-to-utility trigger → SKILL.md § Navigation Design
  - Keywords in URLs, URL Construction Rules → SKILL.md § URL Structure principles 7-8
  - Silo Structure (cluster steps), Linking Priority Stack → SKILL.md § Internal Linking Strategy
  - Common Architecture Mistakes, Proactive Triggers → SKILL.md § Structural Problems to Flag
  - Output Artifacts, Communication → SKILL.md § Output Format (audit, URL change, standards)
  - WHEN conditions → SKILL.md § Related Skills
  - internal-linking-playbook.md (shortened) → references/internal-linking-playbook.md
  - url-design-guide.md (site-type notes, redirect tiers, canonical situations, status codes; corrected) → references/url-design.md
  - sitemap_analyzer.py (rewritten: --linked orphan check, index/gzip/hreflang/image/video sitemaps, hygiene and lastmod checks, 50,000-URL limit, DTD refusal) → scripts/
- Dropped from ali:
  - anchor-text percentage mix and the "exact match 1-2x per page" quota → no source
  - per-type URL structures in url-design-guide.md → repeat corey's site-type-templates.md
  - quarterly link-audit checklist → corey's Link Audit Checklist covers it
  - "Google uses silos to determine topical authority" → unsupported claim
  - owners-and-deadlines rule, confidence emoji → replaced by verified/assumed tags
  - duplicate seo-audit related entry → merged
- Conflicts resolved: header nav size kept at corey's 4-7 items (ali 5-8); corey's "NOT for XML sitemaps" narrowed so the skill may read a sitemap to audit structure; parameter-URL fix no longer relies on robots.txt alone
- Result: SKILL.md 466 lines, 6 refs (internal-linking-playbook, url-design added); scripts kept: sitemap_analyzer.py

### local-seo-manager
- Sources: corey — no skill; three local references in `seo-audit` (local-seo.md 86 lines, profile-and-citations 41, pages-and-measurement 39) · ali `local-seo-manager` (304 lines, 3 refs, 3 scripts)
- Coverage: corey has a policy-accurate decision flow (business model, eligibility, hidden addresses, the retired Q&A API, neutral review requests, doorway-page limits, rich-result vs Schema.org validity, outcome measurement) and three evals / ali has a mode structure, field checklists, a service-area page template, NAP error examples, review reply templates, output artifacts, and three scripts
- Quality: corey 5 · ali 2 — ali's operational structure is useful, but much of its advice is outdated or against policy (geotagged photos, Q&A seeding, legal-name and toll-free rules, review-count and response-rate "ranking signals," 1,000-word neighborhood pages with keyword counts, FAQ rich results, self-serving AggregateRating, US-only directories, WordPress/Rank Math defaults)
- Overlap check: `seo-audit` now routes local work here and keeps only a pointer; `schema` owns markup and points here for LocalBusiness facts and hidden addresses; `directory-submissions` covers software/startup directories, and its "Tier 9 — Local business directories" row overlaps local citations (see report); `link-building` routes reviews to referrals, which still holds platform review rules that this skill links to
- Taken from ali:
  - The 4 Modes → SKILL.md § Choose the Job (five jobs, each tied to a reference)
  - Before Starting point 5 (map-pack competitors) → SKILL.md § Start With the Business Model
  - ranking-factor framing (control relevance, build prominence) → SKILL.md § Diagnose the Local Search Problem
  - Neighborhood Page Uniqueness Checklist → SKILL.md § Build Useful Location and Service Pages (without quotas)
  - Output Artifacts → SKILL.md § Return a Decision and an Actionable Artifact (table)
  - Common NAP Errors, Priority Directories → references/local-seo-profile-and-citations.md (formatting vs conflict table; market-neutral priority)
  - Service Area Page Template → references/local-seo-pages-and-measurement.md § Page Outline (industry-neutral)
  - local-seo-checklist.md → rebuilt on corey's policy
  - review-response-templates.md and the SKILL.md frameworks → neutralized templates
  - nap_checker.py → rewritten (user-set priorities, country code, extra abbreviations, hidden-address and website checks, FIX/CHECK levels, `--demo`)
- Dropped from ali:
  - local-schema-types.md → FAQ/HowTo rich results, self-serving AggregateRating, WordPress-only setup; `schema` and the pages reference cover LocalBusiness correctly
  - schema_generator.py → hard-coded US country and trade type, default price range, profile rating copied into markup, address published for service-area businesses
  - service_area_generator.py → appliance-repair brief with invented claims ("same-day service available") and word-count targets that encourage doorway pages
  - `local-seo-context.md` context file → replaced by the library's product-context file
  - author/category/updated frontmatter → credit moved to a closing line and SOURCES.md
- Conflicts resolved: corey's text wins on every policy point (business name, hidden addresses, Q&A, review solicitation, markup, page justification); ali's ranking claims removed; corey's `local-seo.md` became SKILL.md, so the separate file was removed
- Result: SKILL.md 140 lines, 4 refs (2 corey, edited; 2 ali, rebuilt); scripts kept: nap_checker.py; evals: corey seo-audit cases 11-13

## B3: Copy and content

corey = coreyhaines31/marketingskills @96798cf · ali = alirezarezvani/claude-skills `marketing-skill/` @8f08254. Line counts are SKILL.md lines; refs are files under `references/` (plus templates where noted).

| Merged | corey | ali | Base | Added from ali | Kept/folded | Score corey/ali |
|---|---|---|---|---|---|---|
| `copywriting` | copywriting | copywriting | corey | 2 quality checks, "which means…" bridge, headline-only and CTA-only deliverables, worded annotation labels, 2 related skills | merged | 5/3 |
| `copy-editing` | copy-editing | copy-editing | corey | Output Format (verdict and top fixes first, deliverable per request), 2 related skills; humanizing workflow and voice-matching reference from content-humanizer | merged | 5/3 |
| `content-strategy` | content-strategy | content-strategy | corey | Classify Each Topic table, Problems to Flag, calendar and gap-table outputs | merged | 5/3 |
| `marketing-psychology` | marketing-psychology | marketing-psychology | corey text, ali structure | Modes, catalog index (count fixed), 4 quick-reference rows, Diagnostic Checks, 2 task questions, output table | merged | 4/4 |
| `content-production` | — | content-production | ali | whole skill; readability_scorer.py from ali copy-editing | kept | –/3 |
| `content-humanizer` | (copy-editing; copywriting ai-tells.md) | content-humanizer | corey | humanizing workflow, voice-matching reference, 5 long-form tells, per-1,000-words triage | folded into copy-editing (and copywriting/references/ai-tells.md) | 5/2 |

New old→new names: `content-humanizer` → `copy-editing`. `content-production` keeps its name (`content-creator` → `content-production` is already in MAPPING).

### copywriting
- Sources: corey `copywriting` (339 lines, 3 refs, 0 scripts) · ali `copywriting` (305 lines, 2 refs, 1 script)
- Coverage: corey has the A/B/C input diagnosis, the drafting protocol (decompose and lock, three-question gate, rationed punch, leave-it-alone test), claims-must-be-supportable with an unlock path, the No AI Tells section with a sourced blacklist (ai-tells.md), and the Clarity & Message-Market Fit tools ("Now you can", Human Action Model, Perception Gap) / ali has proactive triggers (copy opens with "We", no social proof, features without benefits), an output-artifacts table (headline-only, CTA-only), confidence tagging, and headline_scorer.py
- Quality: corey 5 · ali 3 — ali is an older snapshot of corey's text plus generic triggers, and its scorer rewards clickbait
- Taken from ali:
  - "Opens with 'We' or the company name" and "no social proof" triggers → SKILL.md § Writing Style Rules (Quick Quality Check)
  - "which means…" bridge for features → SKILL.md § Copywriting Principles (Benefits Over Features)
  - Headline options (five, one per formula family) and CTA options (3-5) deliverables → SKILL.md § Output Format
  - Confidence tagging, as worded labels (confident / worth testing / blocked on proof) → SKILL.md § Output Format (Annotations)
  - Related skills content-strategy and social (was social-content) → SKILL.md § Related Skills
- Dropped from ali:
  - scripts/headline_scorer.py → misleading: it scored the hero line credited with tripling conversions ("You shouldn't have to feel awkward sending out your scheduling link") 30/100 (F) and "Unlock the Secret Formula That Top Experts Use to Grow Revenue Fast" 60/100, the best of the five tested; its power-word list rewards words the AI-tells reference caps or bans (unlock, powerful, ultimate, secret)
  - references/copy-frameworks.md → subset of corey's file (corey adds the Clarity & Message-Market Fit section); its one extra formula, "Everything you need to {outcome}", is on corey's banned-phrase list
  - references/natural-transitions.md → older version of corey's file; its extra phrases ("The outcome?", "The bottom line?", "Let's break this down step by step") are the AI tells corey removed
  - Triggers "vague value proposition" and "weak CTA verbs" → already covered by Specificity, the three-question gate, and CTA Copy Guidelines
  - Output artifact "page copy review" → editing belongs to copy-editing
  - Communication block (bottom line first, emoji confidence tags) → ali house format; corey's Output Format already covers it
- Conflicts resolved:
  - Scope: corey sent all email copy to emails; the owner wants marketing and conversion copy here (pages, ads, emails, launches) → one-off campaign and launch emails stay here, multi-email sequences go to emails (matches its "any multi-email automated flow"); one-off ad copy stays here, variations at scale go to ad-creative
  - The description now excludes in-product UI microcopy (button labels, error messages, empty states, tooltips), so it does not collide with a UI-copy skill
  - Ali's "never present a sub-60 headline" (scorer-driven) → corey's three-question gate and swap test decide instead
  - Long-form articles → routed to content-production (description and Related Skills)
- Result: SKILL.md 354 lines + 3 refs (copy-frameworks.md 432, natural-transitions.md 256, ai-tells.md 316); no scripts. natural-transitions.md keeps "Adapted from: University of Manchester Academic Phrasebank (2023), Plain English Campaign, web content best practices". SOURCES.md: 30 rows.

### copy-editing
- Sources: corey `copy-editing` (491 lines, 3 refs, 0 scripts) · ali `copy-editing` (240 lines, 3 refs, 2 scripts)
- Coverage: corey has edit modes A/B/C with point-edit mode, the Seven Sweeps inline, Expert Panel Scoring, the AI-Tell Check, the "replace with the fact" table, the content-refresh reference (SERP coverage grid, refresh vs. rewrite), and a checklist with AI-tell items / ali has an output-artifacts table, communication rules (bottom line first, prioritize by conversion impact), proactive triggers, readability_scorer.py, ai_content_detector.py with ai-detection-patterns.md, and the sweeps moved to a reference
- Quality: corey 5 · ali 3 — ali compresses corey's older text and adds a synonym-swap table and a regex AI detector that mislead
- Taken from ali:
  - Output Artifacts and Communication (verdict and top fixes first, then sweep by sweep; worded edit labels; deliverable per request type) → SKILL.md § Output Format (new)
  - scripts/readability_scorer.py → content-production/scripts/readability_scorer.py (as is), linked from SKILL.md § Quick-Pass Editing Checks for long copy
  - Related skills content-strategy and social → SKILL.md § Related Skills
  - The folded content-humanizer material is listed under content-humanizer below
- Dropped from ali:
  - scripts/ai_content_detector.py → regex detector: a test passage built only from corey's banned patterns scored 8.7/100 "LIKELY_HUMAN"; it recommends "replace repeated words with synonyms", the synonym cycling corey bans
  - references/ai-detection-patterns.md → documents the dropped detector; its fixes ("This matters." "Here's why." fragments; "wield", "craft", "extract" as verb swaps) are tells in corey's list
  - references/sweeps-detail.md → same sweeps and checklist as corey's SKILL.md and checklist.md, minus the edit modes and AI-tell items
  - references/plain-english-alternatives.md → identical to corey's apart from corey's contents list
  - Word-table rows "Innovative → New", "Robust → Strong", "Seamless → Smooth", "Cutting-edge → New/Modern" → corey replaced them with "write the fact instead", because a synonym swap is a new tell
  - Triggers "no stated goal", "tone shifts", "features outnumber benefits 2:1" → covered by corey's checklist (Before You Start) and sweeps 2-3
- Conflicts resolved:
  - Ali says both "deliver findings sweep by sweep" and "prioritize by conversion impact" → verdict and top fixes first, then corey's sweep-by-sweep loop
  - Length: the new Output Format and Humanizing sections pushed SKILL.md past 500 lines → corey's Expert Panel Scoring moved verbatim to references/expert-panel.md, with a one-paragraph summary left in SKILL.md
  - Readability script location: placed in content-production, where the Flesch pass is a defined step and replaces content_scorer.py, and linked from here, so there is one copy
- Result: SKILL.md 491 lines + 5 refs (plain-english-alternatives.md, checklist.md, content-refresh.md, expert-panel.md moved from SKILL.md, voice-matching.md new); no scripts in this folder. SOURCES.md: 33 rows.

### content-strategy
- Sources: corey `content-strategy` (444 lines, 2 refs, 0 scripts) · ali `content-strategy` (146 lines, 1 ref, 1 script)
- Coverage: corey has Treat Content Like a Product, the information-gain gate, link-earning format data, the 60/30/10 calendar split, per-format discipline, Create Once Distribute Twice with the distribution reference, and the headless-CMS reference / ali has an explicit searchable-vs-shareable decision rule with success measures and time horizons, proactive triggers, output shapes for a calendar and a gap analysis, and topic_cluster_mapper.py
- Quality: corey 5 · ali 3 — ali's reference is an older copy of corey's body; its own additions are short but useful
- Taken from ali:
  - Searchable/shareable decision rule and "judged by" measures → SKILL.md § Searchable vs Shareable (Classify Each Topic)
  - Triggers 2-5 (flat traffic, no keyword target, diluted ICP, outranked on core topics) → SKILL.md § Problems to Flag (new)
  - Calendar and competitor-gap output shapes; "match depth to the request" → SKILL.md § Output Format (sections 4-5)
  - Related skills content-production and copy-editing → SKILL.md § Related Skills
- Dropped from ali:
  - scripts/topic_cluster_mapper.py → lexical grouping misleads: on its own 20-topic demo it put "Instagram marketing tips" in the email cluster and "content marketing ROI" in the social cluster, split the email and SEO topics into two clusters each, then named the largest lexical cluster "highest-priority… start here", which contradicts the weighted scoring
  - references/content-strategy-reference.md → older copy of corey's SKILL.md body; its scoring example shows 8.0 where the weights give 7.9
  - Trigger 1, "propose a 3-pillar starter strategy with 10 seed topics before asking more questions" → conflicts with corey's context-first approach
  - "Content brief" output → belongs to content-production
- Conflicts resolved:
  - Who writes the piece: corey said copywriting → content-production for articles, copywriting for page copy (description, Per-Format Execution Discipline, Related Skills); evals/evals.json eval 6 updated to expect content-production
  - Trigger 1 vs. gathering context first → corey kept
- Result: SKILL.md 477 lines + 2 refs (content-distribution.md, headless-cms.md); no scripts. SOURCES.md: 25 rows.

### marketing-psychology
- Sources: corey `marketing-psychology` (455 lines, 0 refs, 0 scripts) · ali `marketing-psychology` (123 lines, 1 ref, 0 scripts)
- Coverage: corey has the 72-model catalog inline, a 4-step method, an 8-row quick reference, and task questions / ali has the same catalog as a reference, three modes (diagnose, apply, reference), a categories-at-a-glance index, quick-reference rows for pricing pages, email sequences, ad creative, and referral programs, proactive triggers, an output-artifacts table, and questions on emotional state and risk tolerance
- Quality: corey 4 · ali 4 — the catalog text is identical; corey wraps it in a thin method, ali has the better structure but miscounts a category and repeats catalog entries
- Taken from ali:
  - Structure (method in SKILL.md, catalog behind a pointer) → references/mental-models.md holds corey's catalog text unchanged
  - Modes → SKILL.md § Pick the Mode
  - Categories at a glance, count corrected → SKILL.md § The Catalog
  - Rows pricing page, email sequence engagement, ad creative, referral program; BJ Fogg and Default Effect in the onboarding row → SKILL.md § Quick Reference
  - Proactive triggers, with the models behind each → SKILL.md § Diagnostic Checks
  - Emotional state, risk tolerance, and context questions → SKILL.md § Task-Specific Questions
  - Output artifacts → SKILL.md § Output Format
  - "Fake urgency backfires" and "data beats theory" → SKILL.md § Use It Ethically
- Dropped from ali:
  - "Most-Used Models" list → shorter repeats of catalog entries; the quick reference already routes to them
  - Rows "Landing page not converting" and "Reducing churn" → repeat corey's "Low conversions" and "Retention/churn" rows
  - references/mental-models-catalog.md as a separate file → same text as corey's catalog, which is the version moved
  - Communication block (self-verify, emoji confidence tags) → replaced by one data-or-hypothesis line in Output Format
- Conflicts resolved:
  - Inline catalog (corey) vs. catalog in references (ali) → ali's structure: with the method additions SKILL.md would pass 500 lines, and each task needs only a few of the 72 models
  - Ali lists 17 buyer-psychology models; the catalog has 22 (72 in total) → corrected
  - Sunk cost: ali applies it to churn (the customer's sunk cost), corey to killing campaigns (the marketer's) → corey's rows kept
- Result: SKILL.md 130 lines + 1 ref (mental-models.md 405); no scripts. SOURCES.md: 21 rows.

### content-production
- Sources: corey — (no execution pipeline skill; content-strategy and copywriting are nearest) · ali `content-production` (276 lines, 4 refs + 1 template, 4 scripts)
- Coverage: corey's content-strategy decides what to write and sets per-format discipline, copywriting covers page copy, seo-audit and ai-seo cover on-page and AI-search optimization; none produces an article end to end / ali covers brief → draft → optimize → pre-publish gates for blog posts, articles, and guides
- Quality: corey – · ali 3 — a sound pipeline and brief guide, but three of four scripts mislead or are trivial and the AI-citation reference repeats ai-seo
- Taken from ali (kept, edited to fit):
  - SKILL.md (modes, brief, draft, optimize, gates, flags, outputs) → content-production/SKILL.md
  - content-brief-guide.md, content-templates.md, optimization-checklist.md → content-production/references/
  - templates/content-brief-template.md → content-production/assets/content-brief-template.md
  - scripts/content_quality_gates.py → content-production/scripts/ (demo statistics with company names replaced by labelled placeholders)
  - readability_scorer.py from ali copy-editing → content-production/scripts/ (as is)
  - New pointers to corey material instead of copies: copy-editing content-refresh coverage grid, content-strategy information-gain gate, copywriting AI-tells self-check, copy-editing voice-matching, seo-audit, ai-seo, schema
- Dropped from ali:
  - scripts/seo_optimizer.py → pushes keyword density to 1-3% ("Increase keyword density"), lists frequent words as "LSI keywords", and proposes templated titles ("{Keyword} - Complete Guide") and descriptions ("Learn everything about…") that fail corey's swap test; its in-headings check is never computed
  - scripts/content_scorer.py → its engagement score rewards question marks, the words "imagine", "consider", and "here's", and raw number counts, nudging drafts toward AI tells and invented stats; `--json` prints the text report before the JSON; its readability part is replaced by readability_scorer.py
  - scripts/brand_voice_analyzer.py → a "voice profile" built from 4-6 keyword substring matches per category and a variety score from the count of distinct sentence lengths; replaced by the voice-matching reference
  - references/ai-citation-readiness.md → covered by ai-seo (extractable passages, 40-60-word answers, freshness signals); its examples carry unsourced numbers, and it lists gate checks the script does not implement (only the freshness check exists)
  - Emoji confidence tags and "actions have owners and deadlines" → ali house format
- Conflicts resolved:
  - Thin content judged by word count (ali) vs. "ignore competitors' word counts" (corey content-refresh) → coverage of expected subtopics is the measure
  - Conclusion as "summary of the core argument" (ali) vs. corey's recap-ending ban and ali's own summary-conclusion tell → one or two sentences of synthesis that add something
  - Passive-voice target 20% (checklist) vs. 10% (scorer) → 10%
  - 4-7 H2s (SKILL.md) vs. 4-6 (brief guide) → 4-6
  - `templates/` folder → `assets/` (Agent Skills directory convention); the quality-gate H1 check (50-60 characters) vs. the checklist's H1 ≤ 70 → documented that the script assumes the H1 doubles as the title tag
- Result: kept as `content-production`: SKILL.md 244 lines + 3 refs (content-brief-guide.md 146, content-templates.md 101, optimization-checklist.md 141) + 1 asset (content-brief-template.md 126); scripts kept: content_quality_gates.py, readability_scorer.py (both pass `python3 -I -m py_compile` and `--help`). SOURCES.md: 22 rows.

### content-humanizer
- Sources: corey `copy-editing` and `copywriting` references/ai-tells.md (nearest: AI-Tell Check, build-a-writer, rewrite rules, self-check; both claim "this sounds like AI", "AI slop", "make it sound human") · ali `content-humanizer` (269 lines, 2 refs, 1 script)
- Coverage: corey covers the core job with a sourced blacklist, second-generation tells, build-a-writer, rewrite-from-facts rules, and a self-check / ali adds a detect → humanize → voice workflow, voice-profile extraction from a sample, named voice stances, a few long-form tonal tells, a count-based triage, and triggers for missing voice context, tone mismatch, and over-editing
- Quality: corey 5 · ali 2 — ali's own "humanized" example and rhythm advice produce tells corey bans, and its scorer rates tell-dense text as human
- Taken from ali:
  - Detect → rewrite → voice workflow; voice-context, specificity-gap, tone-mismatch, and over-editing triggers; audit deliverable → copy-editing/SKILL.md § Humanizing AI Drafts
  - Voice-profile table, voice stances, anecdote and honest-admission devices (user-supplied facts only), voice check → copy-editing/references/voice-matching.md
  - False warmth, unearned escalation, artificial enthusiasm, bold scattered through prose, a colon and list in every section → copywriting/references/ai-tells.md (§ Tone, § Formatting)
  - Per-1,000-words triage (up to 5 / 6-12 / more than 12) → copywriting/references/ai-tells.md § The Self-Check, step 7
  - Trigger phrases "sounds like ChatGPT" and "this doesn't sound like us" → copy-editing description
- Dropped from ali:
  - scripts/humanizer_scorer.py → regex score: a test passage built only from corey's banned patterns scored 79/100 "Mostly human"; it rewards short paragraphs and sentence-length spread, which pushes toward staccato tells; substring matching counts "vital" inside "revitalize"
  - "Replace filler words" table (delve → "here's what matters", crucial → "the part that actually matters") → synonym swaps that corey's rewrite rules ban, some of them tells themselves
  - Rhythm formulas ("Long. Short. Long, long. Short.", "Question? Answer. Proof.") and "add friction" phrases ("Actually, let me back up…", "What's interesting here is…") → planned rhythm, self-answered questions, and self-narration are corey tells
  - Before/after example → the "after" opens with "Here's the thing nobody says out loud", has a contrast reveal with an em dash, and ends on a wisdom-shaped line
  - Voice-type techniques that break the AI-tells rules ("no rhetorical questions unless you immediately answer them", "The thing is…", the contrarian setup "Everyone says X. The data shows Y.", the staccato signature, swearing) and voice examples with invented statistics
  - references/ai-tells-checklist.md vocabulary tables → corey's Vocabulary section covers the words, and its "what humans say instead" columns are synonym swaps
  - Emoji severity markers → worded severity
- Conflicts resolved:
  - Keep or fold → folded: corey copy-editing already owns "this sounds like AI / AI slop / make it sound human", so the core job is covered; new name mapping content-humanizer → copy-editing
  - Ali's generic-to-specific example invents a named-company statistic (with a note to use a real one) vs. corey's "never invent" → corey's rule, gaps marked `[NEED: source]`
- Result: no folder; the material lives in copy-editing (SKILL.md § Humanizing AI Drafts, references/voice-matching.md 60 lines) and copywriting (references/ai-tells.md); no scripts kept.

## B4: Paid and measurement

Sources: corey = coreyhaines31/marketingskills @96798cf · ali = alirezarezvani/claude-skills `marketing-skill/` @8f08254.
ali `paid-ads`, `ad-creative` and `analytics-tracking` are older forks of the matching corey skills, plus ali-only blocks (Proactive Triggers, Output Artifacts, Communication) and one or two Python scripts each. ali `campaign-analytics` and `marketing-demand-acquisition` have no corey twin. Their jobs are split across corey skills, so both are folded and neither folder is created. Per-file provenance is in each skill's `SOURCES.md`.

| Merged | corey | ali | Base | Added from ali | Kept/folded | Score corey/ali |
|---|---|---|---|---|---|---|
| `ads` | ads | paid-ads (+ campaign-analytics, marketing-demand-acquisition parts) | corey | break-even ROAS from margin, campaign ROI calculator (merged from two scripts), health scoring with evidence coverage, campaign brief, regional expansion gate, monthly review | paid-ads folded | 5/3 |
| `ad-creative` | ad-creative | ad-creative (+ paid-ads copy frameworks) | corey | funnel-stage copy frame, copy frameworks reference, policy and rejection triggers, creative matrix, ad copy validator (reworked) | folded | 5/3 |
| `analytics` | analytics | analytics-tracking (+ campaign-analytics funnel parts) | corey | scope boundary, modes, naming vocabulary, retention events, governance, debugging playbook, SPA page views, key events, consent modes, audit output, funnel analysis + analyzer | folded; tracking_plan_generator.py dropped | 4/3 |
| `attribution` | attribution | campaign-analytics (attribution parts) | corey | journey scoring script (six models), half-life table, reading divergent models | campaign-analytics folded into attribution, analytics and ads | 5/3 |
| `marketing-demand-acquisition` | (ads, marketing-plan, revops) | marketing-demand-acquisition | — | campaign brief and regional expansion (both into `ads`, see above) | folded; no folder; marketing-plan unchanged | —/2 |

### ads
- Sources: corey `ads` (477 lines, 15 refs, 0 scripts) · ali `paid-ads` (363 lines, 5 refs, 2 scripts); also parts of ali `campaign-analytics` and `marketing-demand-acquisition`
- Coverage: corey has the Andromeda-era Meta playbook, Meta decision system, Google search and audit playbooks, RSA output spec, audit guardrails (pass/fail/unknown/na, coverage), payback period, B2B/ABM/LinkedIn playbooks and evals / ali adds margin-based break-even ROAS, a ROAS calculator, an account health scorer with a weighted scoring system, launch deliverables (Output Artifacts), and the ali-only blocks
- Quality: corey 5 · ali 3 — ali's body and three of its references are an older copy of corey's (the references differ only by a missing contents list); its scripts are useful but used letter grades, "warn" results and benchmark verdicts that clash with corey's evidence-first guardrails
- Taken from ali:
  - break-even ROAS = 1 ÷ gross margin → SKILL.md § Reporting & Analysis
  - roas_calculator.py (paid-ads) + campaign_roi_calculator.py (campaign-analytics) → one scripts/campaign_roi_calculator.py with portfolio, non-brand and channel roll-ups, MISSING handling and an attribution-window warning; usage → SKILL.md § Reporting & Analysis › Campaign Math
  - scoring-system.md → references/health-scoring.md, refit to corey's pass/fail/unknown/na model and coverage bands
  - ad_health_scorer.py → scripts/ad_health_scorer.py (health withheld below 60% coverage); usage → SKILL.md § Audit & Recommendation Guardrails
  - Output Artifacts (paid-ads) + Campaign Brief Template (marketing-demand-acquisition) → references/campaign-brief.md
  - international-playbooks.md (marketing-demand-acquisition): expansion gate, campaign localization and legal checklists → references/regional-expansion.md
  - campaign_report_template.md (campaign-analytics) → references/operating-check.md § The monthly review
- Dropped from ali:
  - paid-ads body, ad-copy-templates.md, audience-targeting.md, platform-setup-checklists.md → older copies of corey's
  - copy-frameworks.md → moved to ad-creative (copy belongs there)
  - Proactive Triggers and Communication → covered by corey's fatigue, learning-phase and landing-page rules and its facts/hypotheses/MISSING guardrail
  - letter grades, "warn" results, industry benchmark tables and verdicts → arbitrary or market-specific; corey's guardrails forbid unverified verdicts
- Conflicts resolved:
  - ali loss formula (spend − revenue) vs. margin → contribution = revenue × margin − spend
  - health score vs. evidence coverage → kept apart; health reported only when coverage is high enough
  - pre-existing upstream broken link in references/google-ads-audit-checklist.md (`conversion-tracking.md`) → points to ../../conversion-tracking/SKILL.md
- Result: SKILL.md 499 lines + 18 refs; scripts kept: ad_health_scorer.py, campaign_roi_calculator.py

### ad-creative
- Sources: corey `ad-creative` (476 lines, 12 refs, 0 scripts, 1 asset) · ali `ad-creative` (267 lines, 2 refs, 1 script) + ali `paid-ads` references/copy-frameworks.md
- Coverage: corey has grounded inputs, generative visual tools, static templates, hook system, creative roadmap and retro, review page, motion/short-form/chat-reveal video formats, AI-tell rules and evals / ali adds a copy frame per funnel stage, a creative frameworks reference (AIDA, FAB, contrarian, specificity), policy and rejection triggers per platform, a creative matrix for multi-platform runs, and a copy validator
- Quality: corey 5 · ali 3 — ali's modes and headline formulas are a thinner version of corey's; its frameworks and policy notes are real additions; its validator scored copy with a number and used limits that disagreed with the specs
- Taken from ali:
  - Creative Framework by Funnel Stage → SKILL.md § Generating Ad Copy, Step 2 table
  - Quality Checklist (platform compliance) → SKILL.md § Generating Ad Copy, Step 4 validator paragraph
  - Mode 3 and Output Artifacts (creative matrix) → SKILL.md § Output Formats › Creative Matrix
  - Proactive Triggers "copy lifted from landing page" and "fake urgency" → SKILL.md § Common Mistakes
  - creative-frameworks.md (ali ad-creative) + copy-frameworks.md (ali paid-ads: product-type picker, 4P, star-story-solution) → references/copy-frameworks.md
  - platform-specs.md: Ad Strength, Performance Max, LinkedIn conversation-ad buttons, X link counting, § Policy and Rejection Triggers → references/platform-specs.md
  - ad_copy_validator.py → scripts/ad_copy_validator.py (limits aligned with platform-specs.md, duplicates, asset counts, AI tells, PASS/REVIEW/FAIL)
- Dropped from ali:
  - Headline Formulas, Iteration Methodology, the four modes → covered by corey's hook system, iteration section and modes
  - PAS, BAB and social-proof frameworks → already in ads/references/ad-copy-templates.md
  - platform constraint table and brand-voice axes (paid-ads copy-frameworks.md) → in platform-specs.md, and in brand-guidelines and product-marketing
  - validator's numeric score → arbitrary
- Conflicts resolved: Meta's mislabeled "first-person pronouns" policy item → folded into the personal-attributes row
- Result: SKILL.md 503 lines + 13 refs; scripts kept: ad_copy_validator.py

### analytics
- Sources: corey `analytics` (370 lines, 3 refs, 0 scripts) · ali `analytics-tracking` (387 lines, 3 refs, 1 script); also the funnel parts of ali `campaign-analytics`
- Coverage: corey has core principles (compute, matched windows, recommend against the goal), provider-defined names, UTM rules and partner patterns, AI-assistant traffic, larger GA4 and GTM references and evals / ali adds set-up/audit/debug modes, a verb vocabulary, retention and save-flow events, required vs optional properties, taxonomy governance, a debugging playbook, SPA page views, publishing protocol, key events (GA4's 2024 rename), consent mode detail, proactive triggers, audit output standards, and a tracking plan generator
- Quality: corey 4 · ali 3 — corey is broader and more careful (its GA4 reference still said "Mark as conversion"); ali's debugging and governance material is good; ali's platform conversion and attribution-window section belongs to conversion-tracking, and two ali claims were wrong (key events apply retroactively; 50 item-scoped dimensions)
- Taken from ali:
  - How This Skill Works (modes) → SKILL.md § Initial Assessment item 4
  - action vocabulary and naming rules → references/event-library.md § Naming Vocabulary; pointer and required/optional rule → SKILL.md § Event Naming Conventions
  - retention events (save offer, pause, reactivation, churn risk) and required/optional columns → references/event-library.md
  - Taxonomy Governance (status/owner columns, change protocol, schema_version) → references/event-library.md § Tracking Plan Governance
  - debugging-playbook.md → references/debugging-playbook.md (GA4-vs-Ads section handed to conversion-tracking)
  - GA4 Setup: enhanced-measurement duplicates, key events and the 30 limit → SKILL.md § GA4 Implementation; key events, filter activation, cross-domain test, dimension limits → references/ga4-implementation.md
  - gtm-patterns.md Pattern 4, Pattern 6, Version Control → references/gtm-implementation.md § Single-Page App Page Views, publishing protocol, environments, wait_for_update, basic vs advanced consent
  - UTM rule "never tag organic or direct" → SKILL.md § UTM Parameter Strategy as "External links only"
  - Proactive Triggers → SKILL.md § Debugging and Validation › Flag Without Being Asked
  - Output Artifacts (audit) and Communication → SKILL.md § Output Format › Tracking Audit
  - campaign-analytics funnel-optimization-framework.md → references/funnel-analysis.md; funnel_analyzer.py → scripts/funnel_analyzer.py; usage → SKILL.md § Funnel Analysis
- Dropped from ali:
  - tracking_plan_generator.py → returns the same canned event list whatever the input (key_pages unused; conversion actions only toggle names), uses custom names where GA4 recommended events exist (`checkout_completed` vs `purchase`), against corey's provider-name rule, and points to the retired "Admin > Conversions"; event-library.md and the Tracking Plan Document template do the job with judgement
  - Conversion Tracking: Platform-Specific and Attribution Windows → conversion-tracking and attribution own these
  - event-taxonomy-guide.md SaaS catalog and custom dimension tables → overlap corey's event-library.md and ga4-implementation.md examples
  - gtm-patterns.md patterns 1, 2, 3, 5 and Common GTM Mistakes → covered by corey's data layer patterns and the debugging playbook
  - "Key events are retroactive" → false
  - consent rates by region, 0-100 data quality score, emoji confidence tags → unsourced or arbitrary
  - Related Skills to gdpr-dsgvo-expert → not in this library
- Conflicts resolved:
  - ali names custom events everywhere vs. corey keeps provider names → corey's rule stays; ali's verb vocabulary applies to custom events
  - ali "basic consent mode" as a dataLayer push → dropped; the consent API commands are corey's
  - GA4 custom dimension limits: ali says 50 item-scoped → 10 on standard properties
  - boundary with conversion-tracking → stated in the SKILL.md Scope paragraph, the description, the debugging playbook and Flag Without Being Asked
- Result: SKILL.md 414 lines + 5 refs; scripts kept: funnel_analyzer.py

### attribution
- Sources: corey `attribution` (227 lines, 4 refs, 0 scripts) · ali `campaign-analytics` (228 lines, 3 refs, 3 scripts, 5 assets)
- Coverage: corey has model limits, the three measurement paradigms, self-reported attribution, source reconciliation, blind spots, business-type defaults, first-party identity stitching, a readout format and evals / ali has five rule-based models as a script, an attribution models guide, a funnel analyzer, a campaign ROI calculator, a benchmarks reference, a funnel framework and report templates
- Keep or fold: fold. Every part of campaign-analytics' job has a corey home: attribution models → attribution; funnel drop-off → analytics; ROAS, CPA and ROI → ads; reporting → ads operating-check. The old name `campaign-analytics` maps to `attribution` for model questions, `analytics` for funnels, `ads` for spend math (a note for the `marketing-ops` router)
- Quality: corey 5 · ali 3 — ali's scripts are deterministic and useful, but its attribution guide repeats corey's models at less depth, and its benchmarks are unsourced, USD and stale-prone
- Taken from ali:
  - attribution_analyzer.py → scripts/attribution_analyzer.py (last non-direct added, `--credit`, conversion timestamps, validation, sample-size notes; demo reproduces the worked journey); usage → SKILL.md § Pillar A §2 "Score your own journeys"
  - attribution-models-guide.md: half-life table, divergence patterns, pitfalls, data fields → references/attribution-models.md § Scoring your own journeys
  - funnel parts → analytics; ROI calculator and report template → ads (see those entries)
- Dropped from ali:
  - attribution-models-guide.md model descriptions and comparison matrix → corey's attribution-models.md covers them with a worked example
  - campaign-metrics-benchmarks.md → unsourced industry ranges in one currency; corey's skills judge against the account's own history and break-even
  - assets/ab_test_template.md → ab-testing owns test plans
  - assets/channel_comparison_template.md → covered by the attribution readout and the ads monthly review
  - assets/sample_campaign_data.json, expected_output.json → test fixtures for dropped script versions; each kept script has a built-in demo
  - Best Practices "compare at least 3 models" → kept as "rank across models" in the reference; "include all costs" → already in marketing-plan budget-planning.md (blended CAC)
- Conflicts resolved: ali time-decay counted back from the last touch → kept as default, with optional conversion_timestamp
- Result: SKILL.md 241 lines + 4 refs; scripts kept: attribution_analyzer.py

### marketing-demand-acquisition
- Sources: corey — (covered by `ads`, `marketing-plan`, `revops`) · ali `marketing-demand-acquisition` (312 lines, 4 refs, 1 script)
- Keep or fold: fold, no folder. Its core job (plan demand generation and paid acquisition across channels and budget) is covered: channel setup and scaling → ads; funnel-stage prioritization, budget methods and blended CAC → marketing-plan (aarrr-framework.md, budget-planning.md); lead scoring, MQL→SQL criteria and handoff SLAs → revops; SEO checklist → seo-audit; partnerships → co-marketing, referrals
- Coverage: ali-only material worth keeping was the campaign brief and the regional expansion playbook; both already folded into `ads`
- Quality: corey — · ali 2 — written for one profile (Series A, EU/US/Canada, hybrid PLG/sales, one CRM vendor) with fixed USD budgets, CAC ranges and benchmark targets; the CAC script has no input besides editing its source
- Taken from ali:
  - campaign-templates.md § Campaign Brief Template → ads/references/campaign-brief.md
  - international-playbooks.md (expansion gate, campaign and legal localization) → ads/references/regional-expansion.md
- Dropped from ali:
  - calculate_cac.py → hard-coded sample data, no input, prints USD benchmarks; ads campaign_roi_calculator.py computes channel and blended CAC from the user's file
  - SKILL.md channel matrix, budget allocation, benchmarks, weekly dashboard targets → fixed USD figures for one company stage and market
  - hubspot-workflows.md, attribution-guide.md (HubSpot setup, W-shaped model, dashboards, ICE testing) → vendor-specific; covered by revops, attribution, ab-testing
  - campaign-templates.md LinkedIn, Google, Meta structures and ad copy → covered by ads playbooks and ad-creative
  - international-playbooks.md regional budget splits, CAC ranges, tone stereotypes → market-specific or unsupported
  - SEO Strategy, Partnerships → seo-audit, co-marketing, referrals
  - MQL→SQL handoff and proactive triggers → revops (handoff SLA, scoring) and marketing-plan (diversify channels, LTV)
- Conflicts resolved: none
- Result: no folder; marketing-plan not edited (nothing unique left to add)

## B5: Channels

Sources: corey = coreyhaines31/marketingskills @96798cf · ali = alirezarezvani/claude-skills `marketing-skill/` @8f08254.
corey is the base for every topic. ali's `email-sequence`, `cold-email`, and `social-content` are older forks of the matching corey skills plus ali-only blocks (Proactive Triggers, Output Artifacts, Communication) and scripts. `social-media-manager`, `social-media-analyzer`, `x-twitter-growth`, `webinar-marketing`, and `video-content-strategist` add real material that corey lacks, but each one's core job sits inside a corey skill, so all of them were folded. No ali skill in this batch is kept as a separate folder. Per-file provenance is in each skill's `SOURCES.md`.

| Merged | corey | ali | Base | Added from ali | Kept/folded | Score corey/ali |
|---|---|---|---|---|---|---|
| `emails` | emails | email-sequence | corey | diagnose-before-writing list, output fields (branches, suppression, subject variants), delivery rules, sequence analyzer (fixed) | folded; playbook dropped (older copy of corey) | 5/3 |
| `cold-email` | cold-email | cold-email | corey | request table, running-campaign diagnosis, audience voice table, flag list, four avoid items, deliverability and follow-up additions, frameworks shapes, sequence analyzer (fixed) | folded | 4/3 |
| `social` | social | social-content, social-media-manager | corey | modes, strategy and community reference, pillar mix, community management, calendar generator (fixed) | both folded | 4/3 |
| `social` (from `social-media-analyzer`) | social, analytics | social-media-analyzer | corey | performance-analysis reference (formulas, benchmarks, diagnosis), social_metrics.py (two modules rebuilt as one CLI) | folded into `social`; folder not created | — /2 |
| `social` (from `x-twitter-growth`) | social | x-twitter-growth | corey | x-growth reference (profile audit, post types, cadence by size, 60-day plan, pitfalls), angle bank, competitor comparison | folded into `social`; all 5 scripts dropped | — /3 |
| `events` | events | webinar-marketing | corey | audience-temperature benchmarks, backward plan, promotion runway, live-only reason, day-by-day follow-up, evergreen, goal metrics, formats reference, plan template, funnel scorer (fixed), 2 evals | folded | 4/3 |
| `video` | video | video-content-strategist | corey | strategy section and video-strategy reference (channel setup, keyword targets, 90-day plan, long-form script, repurposing pipeline, flags, deliverables), 1 new eval | folded | 4/3 |

### emails
- Sources: corey `emails` (342 lines, 3 refs, 0 scripts) · ali `email-sequence` (145 lines, 1 ref, 1 script)
- Coverage: corey has reference routing, the full sequence-type and email-type catalog, copy guidelines, tool integrations, and evals / ali adds proactive triggers, delivery rules, output artifacts with branches and suppression, and a sequence analyzer
- Quality: corey 5 · ali 3 — ali's playbook is an older copy of corey's sections; its own additions are small but useful; the analyzer flagged "free" as spam and used thresholds that contradicted corey
- Taken from ali:
  - Five proactive triggers → SKILL.md § Initial Assessment ("Diagnose before you write"), with a note on privacy-inflated opens
  - Communication delivery rules (complete drafts, overview table for 5+ emails, collision flag) and Branches / Suppression / Subject variants fields → SKILL.md § Output Format
  - Tools → SKILL.md § Check the Sequence
  - cold-email, launch, analytics → SKILL.md § Related Skills (merged names)
  - sequence_analyzer.py → scripts/ (thresholds aligned with corey, preview and AI-tell checks, whole-word matching, spam list corrected, input errors handled)
- Dropped from ali: references/email-sequence-playbook.md → older copy of corey's SKILL.md sections; confidence emoji → not this library's voice
- Conflicts resolved: subject length and per-type word counts in the analyzer set to corey's numbers
- Result: SKILL.md 376 lines + 3 refs; scripts kept: sequence_analyzer.py

### cold-email
- Sources: corey `cold-email` (214 lines, 10 refs, 0 scripts) · ali `cold-email` (282 lines, 3 refs, 1 script)
- Coverage: corey has personalization, outbound plays, LinkedIn and multichannel cadences, reply handling, benchmarks, and evals / ali adds three working modes, an audience voice table, proactive flags, authentication record shapes, a layered deliverability diagnosis, a follow-up angle bank, framework shapes, and a sequence scorer
- Quality: corey 4 · ali 3 — ali's flags allow 150-word emails, against corey's ~80-word rule; its follow-up and deliverability material is solid
- Taken from ali:
  - Modes and output artifacts → SKILL.md § What to Deliver (request table, running-campaign diagnosis on placement, reply, positive reply, meetings)
  - Voice calibration → SKILL.md § Voice & Tone (audience table, lengths capped at ~80 words)
  - Proactive triggers → SKILL.md § Quality Check (flag list); Tools → "Score the draft"
  - Four avoid items → SKILL.md § What to Avoid; content-strategy → § Related Skills
  - Authentication records, layered diagnosis, sender-name rule, bought-lists mistake → references/deliverability.md
  - Angle bank, follow-up types, shorter sequences, breakup variant → references/follow-up-sequences.md
  - Three common shapes, choosing and combining → references/frameworks.md
  - Real-referral subject line → references/subject-lines.md
  - email_sequence_analyzer.py → scripts/ (corey thresholds, AI-tell and jargon checks, syllable fix, 5-email cap, `--json`)
- Dropped from ali: warmup schedule, platform limits, open-rate warning signs, legal table → open rates are unreliable and limits go stale; subject-line frameworks → contradict corey's 2–4 word lowercase rule; ali email-sequence and marketing-strategy-pmm related links → covered by emails and product-marketing
- Conflicts resolved: word limit (150 → ~80), first-touch ask (meeting → interest question or 15 minutes), sequence length capped at 5
- Result: SKILL.md 267 lines + 10 refs; scripts kept: email_sequence_analyzer.py

### social
- Sources: corey `social` (457 lines, 9 refs, 0 scripts) · ali `social-content` (323 lines, 3 refs, 0 scripts) + `social-media-manager` (205 lines, 0 refs, 1 script)
- Coverage: corey has hook formulas, repurposing, calendar structure, reverse engineering, short-form video, listening, platform limits, the X algorithm, and evals / ali adds three working modes, platform selection, a company pillar mix, growth levers, community management with escalation, an audit checklist, output artifacts, and a calendar generator
- Quality: corey 4 · ali 3 — social-content is an older fork (its three references are near-copies of corey's, 5–69 differing lines each); social-media-manager adds the strategy and community layer corey lacks
- Taken from ali:
  - Modes and current-state questions → SKILL.md § Before Creating Content ("Pick the mode") and references/strategy-and-community.md
  - Pillar mix and promotional share → SKILL.md § Content Pillars Framework; full table → references/strategy-and-community.md
  - Calendar design → SKILL.md § Content Calendar Structure ("Generate the Calendar")
  - Community engagement (1:1 rule, response framework) → SKILL.md § Engagement Strategy; escalation, growth levers, audit checklist, deliverables → references/strategy-and-community.md
  - social-content proactive triggers and output artifacts → references/strategy-and-community.md (flag list, deliverables)
  - social_calendar_generator.py → scripts/ (per-pillar formats, slots per day, config and date errors handled)
- Dropped from ali: social-content references (reverse-engineering, platforms, post-templates) → near-copies of corey's; cadence table → corey's Platform Quick Reference covers it; batch workflow → corey's batching covers it; "consistency matters more than quality" trigger → unsupported
- Conflicts resolved: "LinkedIn thread" deliverable corrected to a thread; campaign-analytics link replaced by analytics
- Result: SKILL.md 500 lines + 12 refs; scripts kept: social_calendar_generator.py, social_metrics.py (see the next entry)

### social-media-analyzer (folded into social)
- Sources: corey `social` (457 lines, 9 refs, 0 scripts) and `analytics` · ali `social-media-analyzer` (310 lines, 1 ref, 2 scripts, plus sample input and expected output)
- Coverage: corey `social` has metrics by platform and a weekly review; `analytics` covers tracking setup / ali adds engagement, per-follower, and cost formulas, platform benchmark tables, a diagnosis table, and two calculation modules
- Quality: corey — (no matching skill) · ali 2 — the scripts were library modules with no CLI; ROI assigned $2.50 to every engagement; rating bands and posting-time tables had no source
- Keep or fold: folded. Measuring social posts is part of corey `social` (§ Analytics & Optimization); a separate skill would split one job across two folders.
- Taken from ali:
  - Analysis workflow, metric and cost formulas, merged benchmark tables (marked unsourced), diagnosis table → references/performance-analysis.md
  - Tools → SKILL.md § Analytics & Optimization ("Measure Posts")
  - Stalled growth, competitor far ahead, high impressions flags → references/strategy-and-community.md
  - calculate_metrics.py + analyze_performance.py + sample_input.json → scripts/social_metrics.py (one CLI; saves in engagement; per-follower, share, and save rates; follower growth; median; top and bottom posts; content-type averages; ROI only from real revenue; overridable benchmarks)
- Dropped from ali: $2.50 value per engagement and the ROI rating scale → invented numbers; generic rating bands, posting-time and frequency tables → unsourced; expected_output.json, HOW_TO_USE.md → tied to the old modules
- Conflicts resolved: the account's own median is the first baseline, benchmarks second
- Result: no folder; added to `social` as 1 ref + 1 script

### x-twitter-growth (folded into social)
- Sources: corey `social` (457 lines, 9 refs incl. x-algorithm.md, 0 scripts) · ali `x-twitter-growth` (232 lines, 1 ref, 5 scripts)
- Coverage: corey has the X algorithm reference, platform limits, and hook formulas / ali adds a profile audit, post types, cadence by account size, a 60-day plan, competitor research, reach killers, and pitfalls
- Quality: corey — (no X growth playbook) · ali 3 — the playbook is useful; its ranking claims are unverified and its algorithm-signals reference overlaps corey's x-algorithm.md
- Keep or fold: folded. X growth is one platform inside corey `social`.
- Taken from ali:
  - Steps 1–6 and pitfalls → references/x-growth.md
  - profile_auditor.py rules (bio length, stage focus by follower count) → references/x-growth.md as checklist lines
  - content_planner.py TOPIC_ANGLES → references/strategy-and-community.md (Content Angle Bank, platform-neutral)
  - competitor_analyzer.py logic → references/performance-analysis.md (Comparing Competitors)
  - X growth pointer → SKILL.md § Platform Quick Reference
- Dropped from ali:
  - growth_tracker.py → writes snapshots into the skill folder (`.growth-data/`), against the no-writes rule
  - tweet_composer.py → fills fixed hook templates; corey's hook formulas cover it without canned output
  - profile_auditor.py, content_planner.py, competitor_analyzer.py → their useful rules now live as reference text (rows above); a script adds nothing over the list
  - references/algorithm-signals.md and unverified ranking claims → corey's x-algorithm.md is the single source
  - engagement-bait reply prompts → against corey's engagement guidance
- Conflicts resolved: "question tweets" reworded to questions you want answered
- Result: no folder; added to `social` as 1 ref (x-growth.md) plus additions to 2 others; 0 scripts

### events
- Sources: corey `events` (131 lines, 4 refs, 0 scripts) · ali `webinar-marketing` (216 lines, 3 refs, 1 script, 1 template, 3 evals)
- Coverage: corey has all four event roles, portfolio selection, the before/after arc, sponsorship ROI, speaking, and a full webinar funnel reference / ali adds backward funnel math, benchmarks by audience temperature, a three-week promotion runway, a day-by-day follow-up, an evergreen mode, a format selector with run-of-show templates, a plan template, and a funnel scorer
- Quality: corey 4 · ali 3 — corey's webinar-funnel.md already covered the stages (credited to ali as the idea source); ali's numbers and templates are the practical layer it lacked
- Taken from ali:
  - benchmarks.md (stage ranges, audience-temperature table, show-up factors, goal metrics) → references/webinar-funnel.md (intro, Stage 2, Metrics That Diagnose)
  - Funnel math → references/webinar-funnel.md § Plan Backward from the Goal
  - promotion-playbook.md (runway, channel playbook, separate tracks, follow-up table, copy lines) → references/webinar-funnel.md Stages 1, 2, 4
  - Mode 3 evergreen → references/webinar-funnel.md Stage 4; 60-minute limit → Stage 3
  - webinar-formats.md → references/webinar-formats.md
  - templates/webinar-plan-template.md → references/webinar-plan-template.md
  - Mode 2 and Tools → SKILL.md § Measurement › Score a Webinar Funnel
  - webinar_funnel_scorer.py → scripts/ (`--json`, unknown audience reported, optional fields no longer crash)
  - Evals rescue-low-attendance and write-segmented-followup → evals/evals.json (ids 8–9, with assertions)
  - page-cro and paid-ads related links → SKILL.md § Related Skills as cro and ads
- Dropped from ali: three-week runway → compressed to corey's two weeks; confidence emoji → replaced by "measured / benchmark"; platform brand list in the template → placeholder; plan-from-scratch eval → corey evals cover planning; Communication block → not this library's voice
- Conflicts resolved: runway length (3 weeks → 2); show-up cadence keeps corey's T-5 minutes reminder alongside ali's T-1 hour and live
- Result: SKILL.md 148 lines + 6 refs; scripts kept: webinar_funnel_scorer.py

### video
- Sources: corey `video` (351 lines, 4 refs, 0 scripts) · ali `video-content-strategist` (218 lines, 0 refs, 0 scripts)
- Coverage: corey has production only: tool choice, programmatic video (Hyperframes, Remotion), AI generation models, avatars, editing and repurposing tools, edit reverse-engineering, demo recording, code-rendered films, per-account films / ali has strategy only: niche and positioning, pillars, YouTube keyword targets, a 90-day plan, long-form and short-form script structures, a repurposing pipeline, flags, and deliverables
- Quality: corey 4 · ali 3 — ali fills corey's missing strategy layer, but leans on unsourced numbers (70% decide in 30 s, 40% retention drop, 60–80% reach penalty) and the "algorithm punishes gaps" claim
- Taken from ali:
  - How This Skill Works → SKILL.md § Start with Strategy (routing table)
  - Mode 1 (niche, pillars, keyword targets, 90-day plan) → references/video-strategy.md § Channel Setup
  - Mode 2 long-form structure → references/video-strategy.md § Long-Form Script Structure (chapter rules made concrete)
  - Mode 3 atomization, blog-to-video table, workflow → references/video-strategy.md § Repurposing Pipeline
  - Proactive Triggers + Anti-Patterns → references/video-strategy.md § Flags to Raise Unprompted
  - Output Artifacts → references/video-strategy.md § Deliverables
  - Strategy triggers → SKILL.md frontmatter; launch → § Related Skills
  - One eval for the channel-strategy path → evals/evals.json (id 11, new)
- Dropped from ali: short-form script structure → social `references/short-form-video.md` covers it, so video points there; unsourced percentages and "second-largest search engine" → replaced by checking the user's own retention data; tags advice → tags carry little weight; Communication block → not this library's voice; content-production and seo-audit links → ai-seo covers the video text layer
- Conflicts resolved: corey's description sent "video strategy" to social; now video owns channel and long-form strategy and social owns short-form posting (matches social's own Related Skills line)
- Result: SKILL.md 373 lines + 5 refs; no scripts

## B6: Growth

Sources: corey = coreyhaines31/marketingskills @96798cf · ali = alirezarezvani/claude-skills `marketing-skill/` @8f08254.
In this batch, three ali skills (pricing-strategy, referral-program, free-tool-strategy) are separate rewrites with their own structure. The other three (launch-strategy, churn-prevention, marketing-ideas) are shorter or older copies of the corey skill. Each ali skill adds the same four blocks (Proactive Triggers, Output Artifacts, Communication, WHEN/WHEN NOT related skills), and five of the six have a Python script. Every ali script needed fixes before it could be kept. Per-file provenance is in each skill's `SOURCES.md`.

| Merged | corey | ali | Base | Added from ali | Kept/folded | Score corey/ali |
|---|---|---|---|---|---|---|
| `pricing` | pricing | pricing-strategy | corey | mode table, value quantification, metric red flags, tier rules, price-increase table and rollout checklist, page-design reference, model variants and failure modes, pricing modeler (fixed) | folded | 4/3 |
| `referrals` | referrals | referral-program | corey (ali table for referral vs. affiliate) | referral-vs-affiliate table, loop steps 4-5, trigger moments, measurement reference, partner-type commissions, pilot and partner kit, ROI calculator (fixed) | folded | 4/3 |
| `free-tools` | free-tools | free-tool-strategy | corey | mode table, design principles, gating rules, SEO page structure, scorecard anchors and a ninth factor, launch-and-measurement reference, converters and data tools, ROI estimator (fixed) | folded | 4/3 |
| `launch` | launch | launch-strategy | corey | completion bar for plans, borrowed-channel lead time, phase timeline, proactive flags, deliverables, readiness scorer (rebuilt) | folded; framework reference dropped (older copy of corey) | 5/2 |
| `churn-prevention` | churn-prevention | churn-prevention | corey | flow rules, offer when-not table, two survey reasons, metrics and red flags, proactive flags, deliverables, cancel-flow templates and audit rubric, dunning additions, churn calculator (fixed) | folded | 5/3 |
| `marketing-ideas` | marketing-ideas | marketing-ideas | corey | curate-and-ask rule, effort and confidence fields, proactive flags, deliverables, routing conditions | folded; ideas list identical, nothing to merge | 4/3 |

### pricing
- Sources: corey `pricing` (295 lines, 4 refs, 0 scripts) · ali `pricing-strategy` (323 lines, 2 refs, 1 script)
- Coverage: corey has initial-pricing guidance, the pricing-page teardown (human and AI-agent readers), MaxDiff, a deeper tier-structure reference and evals / ali has a three-mode workflow, a "metric, then packaging, then price" order, value quantification steps, value-metric red flags, tier rules of thumb, price-increase strategies with risk, a pre-rollout checklist, a pricing-page playbook, model failure modes and stage benchmarks, and a modeler script
- Quality: corey 4 · ali 3 — ali is well organized, but has a 0-100 scorecard, a Van Westendorp reading that contradicts corey's, unsourced thresholds, and a script with silent defaults and invented headroom numbers
- Taken from ali:
  - How This Skill Works and the three-axes order rule → SKILL.md § How This Skill Works (mode table, plus a fourth mode for corey's teardown)
  - Value-Based Pricing steps → SKILL.md § Pricing Fundamentals › Quantify the Value
  - Value-metric red flags → SKILL.md § Value Metrics
  - Tier rules of thumb → SKILL.md § Tier Structure Overview
  - Competitor benchmark summary → SKILL.md § Pricing Research; five-step benchmark → references/research-methods.md
  - Price-increase strategies (use-when and risk columns), pre-rollout checklist, 60-day monitoring, fix-churn-first guard → SKILL.md § When to Raise Prices
  - FAQ objections, security badges, annual-toggle rules → SKILL.md § Pricing Page Best Practices
  - Proactive Triggers and the conversion signal → SKILL.md § Proactive Flags
  - Output Artifacts and Communication → SKILL.md § Deliverables
  - Pricing-page playbook → references/pricing-page-design.md
  - Seat and usage variants, failure modes, model choice questions, stage benchmarks, LTV:CAC rule → references/pricing-models.md
  - Freemium math and usage-limited trial → references/tier-structure.md
  - pricing_modeler.py, with fixes → scripts/pricing_modeler.py; usage → SKILL.md § Model the Scenarios
- Dropped from ali:
  - 0-100 pricing scorecard → corey's teardown does the job with evidence
  - Van Westendorp reading and n≥30 rule → conflicts with corey's research-methods reference
  - Per-model descriptions → duplicate corey's model table
  - Page playbook's 0-2 audit checklist, SEO note, 500-visitor rule → duplicate the teardown or unsourced
  - Script's ARPU-as-mid-tier scenario and headroom numbers → invented
  - Related skills outside this library
- Conflicts resolved:
  - Value-capture heuristic: ali 10-20% of value vs. corey's 10:1 value-to-price ratio → stated together as one rule
  - Card-required trials distort conversion bands → caveat added to the flags
- Result: SKILL.md 408 lines (was 295) + 5 refs (778 lines); scripts kept: pricing_modeler.py (338 lines); SOURCES.md 40 rows

### referrals
- Sources: corey `referrals` (283 lines, 8 refs, 0 scripts) · ali `referral-program` (286 lines, 2 refs, 1 script)
- Coverage: corey has the "engineer virality first?" gate, review programs (4 refs), affiliate operations, email sequences, a launch checklist, tool integrations and evals / ali has a referral-vs-affiliate comparison table, loop steps for converting the referred user and delivering the reward, trigger moments, a diagnose-then-fix-one-lever rule, a measurement framework, partner-type commissions, a ten-partner pilot, and an ROI calculator
- Quality: corey 4 · ali 3 — ali's mechanics are clear; its CAC example has an order-of-operations error, and its script booked full LTV up front and used two different target CACs
- Taken from ali:
  - Outcome and loop-break questions → SKILL.md § Before Starting
  - Comparison table and rule of thumb → SKILL.md § Referral vs. Affiliate (ali's table is better than corey's two bullet lists)
  - Trigger moments, personal-share rules, double- vs. single-sided rule, three-tier limit, steps 4 and 5 → SKILL.md § Referral Program Design
  - "Diagnose, fix one lever, measure" → SKILL.md § Program Optimization
  - Ten-partner pilot and partner kit → SKILL.md § Affiliate Programs
  - Proactive Triggers → SKILL.md § Proactive Flags; Output Artifacts → SKILL.md § Deliverables
  - Measurement framework → references/measurement.md
  - Ambassador tiers, milestone and B2B introduction patterns → references/program-examples.md
  - Commission by partner type and fraud signals → references/affiliate-programs.md
  - Share-message example → references/viral-mechanisms.md
  - referral_roi_calculator.py, with fixes → scripts/referral_roi_calculator.py; usage → SKILL.md § Model the Economics
- Dropped from ali:
  - CAC worked example → duplicates corey's sizing framework and has an arithmetic-order error
  - Cookie windows and platform list → covered by corey's affiliate references
  - Related skills that duplicate corey's list or sit outside this library
- Conflicts resolved:
  - Fraud warning signs: ali treats them as verdicts, corey as signals → reframed as signals to review
  - ROI basis: ali used revenue; corey uses contribution and incrementality → script uses contribution and an incremental share
- Result: SKILL.md 343 lines (was 283) + 8 refs (921 lines); scripts kept: referral_roi_calculator.py (274 lines); SOURCES.md 40 rows

### free-tools
- Sources: corey `free-tools` (191 lines, 2 refs, 0 scripts) · ali `free-tool-strategy` (278 lines, 2 refs, 1 script)
- Coverage: corey has core principles, MVP scope, build vs. buy, an eight-factor scorecard, benchmarks, common pitfalls and evals / ali has a three-mode workflow, design principles, when-to-gate rules, progressive profiling, SEO page structure, a launch playbook, converters and data tools, no-code options by type, "five ways to be 10x better", a 6-factor evaluation, and an ROI estimator
- Quality: corey 4 · ali 3 — ali adds useful execution detail; it has unsourced figures ("50%+ mobile", "~10% per field"), launch-platform tactics, and a script that valued revenue, not contribution, and added speculative backlink value
- Taken from ali:
  - Win definition and maintainer questions → SKILL.md § Initial Assessment
  - Mode workflows → SKILL.md § How This Skill Works
  - Converter and data-tool rows → SKILL.md § Tool Types Overview; types detail → references/tool-types.md
  - Validate-before-build line → SKILL.md § Ideation Framework
  - Design principles → SKILL.md § Design Principles
  - Gating rules, progressive profiling → SKILL.md § Lead Capture Strategy
  - Landing-page structure, keyword placement, link-magnet sources → SKILL.md § SEO Considerations
  - 1-vs-5 anchors and lead-capture potential as a ninth factor → SKILL.md § Evaluation Scorecard
  - Launch playbook and metrics → SKILL.md § Launch and Measurement; references/launch-and-measurement.md
  - Proactive Triggers → SKILL.md § Proactive Flags; Output Artifacts → SKILL.md § Deliverables
  - tool_roi_estimator.py, with fixes → scripts/tool_roi_estimator.py; usage → SKILL.md § Estimate the ROI
- Dropped from ali:
  - Separate 30-point scale → corey's scorecard extended instead
  - Schema JSON → hand-off to the schema skill
  - Launch-platform posting hour, weekday and upvote tactics → launch skill covers launches
  - Unsourced reach, freshness and mobile figures; analytics product names
- Conflicts resolved:
  - Two scorecards (corey 8 factors / 40, ali 6 factors / 30) → one nine-factor scorecard, thresholds rescaled to 28/17 of 45
  - ali's 90-day targets vs. corey's evidence rules → kept as labeled review gates
  - Grader in the no-code table → corrected (no-code fits a fixed rubric)
- Result: SKILL.md 336 lines (was 191) + 3 refs (492 lines); scripts kept: tool_roi_estimator.py (266 lines); SOURCES.md 36 rows

### launch
- Sources: corey `launch` (385 lines, 2 refs, 0 scripts) · ali `launch-strategy` (95 lines, 1 ref, 1 script)
- Coverage: corey has the ORB framework, readiness gate, five phases, launch-platform strategy, post-launch and ongoing launches, site-launch QA and shipped-changes references, and evals / ali's reference is an older copy of corey's body; ali adds a quality bar for plans, a phase timeline, proactive triggers, output artifacts and a readiness scorer
- Quality: corey 5 · ali 2 — ali's own text is short, and its scorer's categories did not match the gate, its template export printed demo statuses
- Taken from ali:
  - Quality bar (all three channel types, owner and date per action) → SKILL.md § Core Philosophy, as a completion criterion
  - "Start borrowed-channel relationships weeks before launch day" → SKILL.md § The ORB Framework
  - Scorer usage and the slip-the-date gate → SKILL.md § Readiness Gate › Score Readiness
  - 2-6 week pre-launch, time-boxed launch day, 30-day post-launch → SKILL.md § Five-Phase Launch Approach
  - Proactive Triggers → SKILL.md § Proactive Flags; Output Artifacts → SKILL.md § Deliverables
  - Related skills pricing, ads, social, content-strategy → SKILL.md § Related Skills
  - launch_readiness_scorer.py, rebuilt around this skill's gate → scripts/launch_readiness_scorer.py
- Dropped from ali:
  - references/launch-frameworks-and-checklists.md → older copy of corey's SKILL.md body
  - Launch-platform product name in triggers → generalized
  - Output format column → not needed
- Conflicts resolved:
  - Idea numbers in Related Skills (#22, #23 pointed at the wrong tactics) → corrected to #78 and #79
- Result: SKILL.md 434 lines (was 385) + 2 refs (141 lines); scripts kept: launch_readiness_scorer.py (243 lines); SOURCES.md 27 rows

### churn-prevention
- Sources: corey `churn-prevention` (434 lines, 2 refs, 0 scripts) · ali `churn-prevention` (240 lines, 2 refs, 1 script)
- Coverage: corey has proactive retention (risk signals, health score with coverage rules, interventions), decline-type retries, pre-dunning, grace periods, provider setup, cohort analysis, cancel-flow A/B tests, segment and billing-interval patterns, compliance notes, tool tables and evals / ali adds flow rules (one required question before the offer, one offer per reason, do not repeat a declined offer), a when-not-to-use table per offer, offer presentation rules, exit-survey completion and win-back metrics, red flags, stage copy templates, post-cancel emails, an audit scorecard, a fifth dunning email, a never-retry rule for fraud and lost cards, and a churn impact script
- Quality: corey 5 · ali 3 — ali's flow rules and templates are useful; its benchmarks are lower than corey's without sources, its scorecard bands do not fit its scale (max 70, "60-70 solid"), and its script applied save rates to churned MRR and booked a 1/churn LTV
- Taken from ali:
  - Save-offer budget and primary-problem questions → SKILL.md § Before Starting
  - Flow rules (cancel visible, one required question, one offer per reason, no repeat within 30 days, confirmation facts, tracked fields) → SKILL.md § Cancel Flow Design › Flow Rules
  - "Too complicated" and "Just testing" reasons, When Not to Use Each Offer, offer presentation → SKILL.md § Cancel Flow Design
  - Exit-survey completion and win-back rows, red flags, benchmark range note → SKILL.md § Metrics & Measurement
  - Proactive Triggers → SKILL.md § Proactive Flags
  - Output Artifacts and Communication → SKILL.md § Deliverables
  - email-sequence and pricing-strategy conditions → SKILL.md § Related Skills (as emails, pricing)
  - Decision tree, stage copy, confirmation and post-cancel emails, audit scorecard (as a 0/1/2 rubric) → references/cancel-flow-templates.md
  - Fraud/lost decline row and never-retry rule, Email 5, build-or-buy guidance, per-step and card-updater metrics → references/dunning-playbook.md
  - churn_impact_calculator.py, with fixes → scripts/churn_impact_calculator.py; usage → SKILL.md § Size the Revenue at Stake
- Dropped from ali:
  - Retry schedule (days 3/8/13/16) and four-row dunning table → corey's decline-type schedule and playbook cover it
  - Full offer-mapping table in the playbook → duplicate of SKILL.md
  - Card updater config table, worked dunning math, third-party tool list, platform notes → duplicates of corey's provider setup, ROI calculation and tool tables
  - "$500k MRR" build-or-buy threshold → arbitrary
  - Win-back email row in deliverables → emails skill owns win-back sequences
  - customer-success-manager, campaign-analytics, signup-flow-cro related lines → outside this library or not about retention
  - Confidence emoji → measured / benchmark / assumption labels
- Conflicts resolved:
  - Save-rate benchmark: ali 10-15% good, 20%+ excellent vs. corey 25-35% target → corey's target kept, a range note added and targets set from the user's baseline
  - Recovery benchmark: ali 25-35% (25-40% in its guide) vs. corey 50-60% → same treatment
  - Share of churn from failed payments: ali 20-40% vs. corey 30-50% → corey's figure kept; the flag says "often a third or more"
  - One offer only (ali) vs. primary plus fallback (corey) → one primary offer, a secondary option allowed, no wall of offers
  - 5% monthly churn flag (ali) vs. corey's targets (<5% B2C, <2% B2B) → flag scoped to B2B
  - FTC Click-to-Cancel rule cited as current (corey) → status note: vacated by a US appeals court in July 2025; state automatic-renewal laws still apply
- Result: SKILL.md 524 lines (was 434) + 3 refs (963 lines); scripts kept: churn_impact_calculator.py (212 lines); SOURCES.md 29 rows

### marketing-ideas
- Sources: corey `marketing-ideas` (172 lines, 2 refs, 0 scripts) · ali `marketing-ideas` (211 lines, 1 ref, 0 scripts)
- Coverage: corey has the guerrilla-marketing deep dive, a contents block in the ideas list, and evals / ali's body and 139-idea list are word-for-word copies of corey's; ali adds proactive triggers, output artifacts, communication rules and routing conditions
- Quality: corey 4 · ali 3 — same core; ali's additions are small and useful
- Taken from ali:
  - "Never list all 139; ask when stage, budget or timeline is unclear" → SKILL.md § How to Use This Skill
  - Effort/time and confidence fields, top-three-first rule → SKILL.md § Output Format
  - Proactive Triggers → SKILL.md § Proactive Flags
  - Output Artifacts → SKILL.md § Deliverables, with hand-offs to marketing-plan, reverse-engineer-marketing and competitor-profiling
  - Routing conditions for marketing-context, content-strategy, copywriting, copy-editing, social-content, content-production, seo-audit → SKILL.md § Related Skills (as product-marketing, social)
- Dropped from ali:
  - references/ideas-by-category.md → the same 139 ideas as corey's, no idea to add and no duplicate to remove
  - free-tool-strategy related line → corey's free-tools line covers it
  - Confidence emoji → words
- Conflicts resolved:
  - "Founder-led sales (#47)" points at idea #47 Founder Welcome Email (in both sources) → relabelled "Founder welcome emails (#47)"
- Result: SKILL.md 211 lines (was 172) + 2 refs (422 lines, unchanged); no scripts; SOURCES.md 19 rows

## B7: Foundations and positioning

Sources: corey = coreyhaines31/marketingskills @96798cf · ali = alirezarezvani/claude-skills `marketing-skill/` @8f08254.
Two ali skills in this batch (marketing-context, competitor-alternatives) are older forks of the matching corey skill plus ali-only blocks and one script each. app-store-optimization is an independent skill whose eight scripts are library modules with no command line. marketing-strategy-pmm is a PMM overview whose parts all have a corey home. Per-file provenance is in each skill's `SOURCES.md`.

| Merged | corey | ali | Base | Added from ali | Kept/folded | Score corey/ali |
|---|---|---|---|---|---|---|
| `product-marketing` | product-marketing | marketing-context (+ marketing-strategy-pmm positioning) | corey | gap flags, style rules, Content & SEO section, completeness validator (rewritten), positioning reference (ICP, Dunford chain, messaging hierarchy, validation, map, 30-second pitch); new: per-product context location, Languages & Markets | marketing-context folded | 4/3 |
| `competitors` | competitors | competitor-alternatives | corey | comparison matrix builder (rewritten with evidence rules), migration block, "when to suggest more pages" | folded | 4/3 |
| `aso` | aso | app-store-optimization | corey | metadata-writing mode, keyword research method, metadata patterns and examples, launch/review/test reference, one consolidated metadata script | folded; 7 of 8 scripts and the audit template dropped | 4/3 |
| `marketing-strategy-pmm` | (product-marketing, competitor-profiling, sales-enablement, launch, marketing-plan) | marketing-strategy-pmm | — | positioning → product-marketing; intel program → competitor-profiling; launch tiers → launch; international GTM → marketing-plan | folded; no folder | —/3 |

### product-marketing
- Sources: corey `product-marketing` (320 lines, 1 ref, 0 scripts) · ali `marketing-context` (183 lines, 1 template, 1 script) + positioning parts of `marketing-strategy-pmm` (see that entry)
- Coverage: corey has the versioned document with Changelog, the Learnings table and its write rules, Paid Ads section, brand-voice reference, auto-draft workflow, and evals / ali adds proactive gap triggers, a Style Guide section, a Content & SEO Context section with keyword-cluster and internal-link tables, a "validate the result" step and a completeness script; ali lacks versioning, Learnings and the brand-voice reference
- Quality: corey 4 · ali 3 — ali's body is an older copy of corey's; its additions are useful, but its validator matched keywords, so an empty template scored well
- Taken from ali:
  - Proactive triggers (no customer language, no competitors, no voice, no proof, context older than 6 months) → SKILL.md § Workflow, Step 1 "flag gaps" bullet
  - Style Guide → SKILL.md § Sections to Capture, Brand Voice style-rules bullet and template line
  - Content & SEO Context and its template tables → optional section 14 and template block, one keyword set per language
  - Validate the Result (below 70, fill the gaps) → SKILL.md § Checking Completeness
  - context_validator.py → scripts/context_validator.py, rewritten to parse fields (empty template scores 0), merged sections, language/version/Changelog checks
  - (from marketing-strategy-pmm) ICP workflow, Dunford positioning chain, Moore statement as summary, messaging hierarchy, validation interviews, positioning map, 30-second spoken pitch → references/positioning.md; positioning triggers → SKILL.md § When Positioning Isn't Settled
- Dropped from ali:
  - Body sections 1–10, 12, 14 and Tips → older copy of corey's text
  - Rest of the template → duplicated corey's template
  - Output Artifacts and Communication (confidence emoji tags) → generic; corey's Step 4 covers confirmation
  - Related skills pointing outside this library → replaced by a new Related Skills list
- Conflicts resolved:
  - Context location: corey `.agents/product-marketing.md`, ali `.claude/product-marketing-context.md` → new "Where the Context Lives" rule: `projects/<project>/product-marketing.md` per product in a multi-product workspace, `.agents/product-marketing.md` in a single-product repo, legacy paths read and offered for moving, never written where another product can read it, ask when the product is unclear
  - Audience language: neither source recorded it → new section 3 Languages & Markets (primary language and locale, other locales, tone per language, target markets); no default language, chat language is not evidence
- Result: SKILL.md 423 lines + refs 269 lines (brand-voice.md 112, positioning.md 157); scripts kept: context_validator.py (455 lines); evals 11 (4 added); SOURCES.md 39 rows

### competitors
- Sources: corey `competitors` (287 lines, 2 refs, 0 scripts) · ali `competitor-alternatives` (300 lines, 2 refs, 1 script)
- Coverage: corey has Evidence Discipline (principle 5), the competitive asset audit, provenance fields in the data file, newer references and evals / ali adds a comparison matrix script, a migration-guide artifact and proactive triggers for new pages
- Quality: corey 4 · ali 3 — same core text, ali's is older; its script counted an unsourced "no" as a win and ignored weights
- Taken from ali:
  - comparison_matrix_builder.py → scripts/comparison_matrix_builder.py with Evidence Discipline (unsourced "no" shown as Not listed and left out of scores, `unknown` status, `source` and `as_of`, status key and "as of" line), weights applied, text labels, input errors handled
  - Tools section → SKILL.md § Content Architecture › Building the Comparison Table; one sentence in § Essential Sections › Feature Comparison
  - Migration Guide artifact → SKILL.md § Output Format › Migration Block
  - Proactive triggers 1–4 → SKILL.md § When to Suggest More Pages
  - content-strategy related entry → SKILL.md § Related Skills
- Dropped from ali:
  - SKILL.md body and both references → older copies of corey's
  - Proactive trigger 5 (pricing comparisons off the pricing page) → opinion without evidence
  - Other Output Artifacts and Communication → duplicate corey's Output Format; emoji confidence tags
  - Related skills outside this library
- Conflicts resolved: script scoring vs. corey's Evidence Discipline → the script follows Evidence Discipline
- Result: SKILL.md 327 lines + refs 503 lines (templates.md 226, content-architecture.md 277); scripts kept: comparison_matrix_builder.py (330 lines); evals 10 (2 added); SOURCES.md 22 rows

### aso
- Sources: corey `aso` (314 lines, 5 refs, 0 scripts) · ali `app-store-optimization` (487 lines, 3 refs + 1 asset template, 8 scripts; 2.6k lines of Python)
- Coverage: corey has a live-listing audit (fetch, brand-maturity tiers, 6-dimension weighted score, report template), current and dated platform specs (Google title 30, keyword field in bytes, Android Vitals, CPP/CSL, caption indexing) and sourced benchmarks / ali has a keyword-research method with scoring, a metadata-writing workflow (title formula, subtitle formulas, description structure), before/after examples, competitor keyword coverage, launch and A/B workflows, review-response frameworks and review-prompt timing; corey cannot write new metadata, ali has outdated limits (Google title 50, keyword field "100 characters")
- Quality: corey 4 · ali 3 — ali's workflows are useful, but its specs are stale, many numbers are unsourced (star lifts, conversion lifts, sample-size table from a wrong formula), and none of its eight scripts has a command line despite the documented usage
- Taken from ali:
  - Keyword Research and Metadata Optimization workflows → SKILL.md § Writing and Optimizing Metadata (one 8-step workflow, store rules from corey's specs, deliverable table)
  - keyword-research-guide.md (seeds, expansion, filtering, scoring weights, coverage reading, placement map, iOS field steps, Google description placement, tracking and change log) → references/keyword-research.md
  - Title formula and checklist, subtitle formulas, description structure, caption ladder, before/after examples → references/metadata-writing.md
  - App Launch and A/B Testing workflows, review-response frameworks, prompt timing, update cadence, test priority → references/launch-and-iteration.md
  - Competitor Analysis Workflow steps 3–4 and the coverage reading → SKILL.md § Phase 3
  - metadata_optimizer.py, keyword_analyzer.py, competitor_analyzer.py → one CLI, scripts/metadata_check.py (`check`, `keyword-field`, `coverage`); usage → SKILL.md § Metadata Script
  - Keyword filtering (competitor brand names) → SKILL.md § Common Issues Checklist item
  - Google Play What's New limit (500) → references/google-play-specs.md
  - "before writing metadata" and keyword/metadata triggers → frontmatter description
- Dropped from ali:
  - aso_scorer.py → duplicates corey's 6-dimension rubric with conflicting weights (4 × 25%) and a 5% "optimal" density that contradicts corey's 2-3% target
  - ab_test_planner.py and the sample-size table → the ab-testing skill's calculator covers sizing; ali's formula treats the effect as an absolute 5 points
  - review_analyzer.py → sentiment from a 12-word lexicon blended 60/40 with the star rating; misleading as analysis
  - launch_checklist.py → static lists with fixed weekdays per category and invented seasonal advice; kept as prose in launch-and-iteration.md
  - localization_helper.py → fabricated revenue shares per market and a flat $0.12/word translation cost
  - assets/aso-audit-template.md → duplicates references/report-template.md and the scoring criteria
  - platform-requirements.md → older copy of corey's specs (Google title 50); its What's New limit kept
  - aso-best-practices.md impact numbers (+0.3 stars, 10-35% lifts, funnel benchmarks) → unsourced; corey's benchmarks.md has sourced figures
  - Keyword volume bands and "competition from top-10 average rating" → arbitrary; replaced by qualitative criteria with tool-and-date sourcing
  - Fixed launch weekday and seasonal calendar (tax season, back to school) → market-specific; replaced by "check the main markets' calendars"
  - Priority-markets tables → a fixed market list; the skill now works per storefront and language from the context file
  - Vendor names (Firebase, Mixpanel), Proactive Triggers (covered by corey's checklist), Output Artifacts, Communication
- Conflicts resolved:
  - Google title 50 vs. 30, keyword field characters vs. bytes → corey's specs win; ali text corrected
  - "Remove plurals (Apple indexes both)" vs. no rule in corey → keep one form unless rankings show the other needs its own entry; the script keeps forms as given
  - Density: ali scorer "optimal 5%" vs. ali text and corey 2-3% → 2-3% target, over 5% flagged as stuffing
  - Modifiers "free/best" as expansion seeds vs. store claim rules → kept as research signals only, never in indexed fields
  - English-only examples and term lists → stated as English; keyword research redone per language
- Result: SKILL.md 405 lines + refs 1,254 lines (5 corey refs; new keyword-research.md, metadata-writing.md, launch-and-iteration.md); scripts kept: metadata_check.py (492 lines; compiled, `--help`, demo runs on both stores, CJK input, missing-file error); evals 9 (2 added); SOURCES.md 29 rows

### marketing-strategy-pmm
- Sources: corey — no single skill; covered by `product-marketing`, `competitor-profiling` (442 lines), `sales-enablement` (427 lines, 6 refs), `launch`, `marketing-plan` · ali `marketing-strategy-pmm` (399 lines, 4 refs, 0 scripts; 1.9k lines)
- Coverage: corey covers every core job: positioning and ICP (product-marketing), competitor research (competitor-profiling), battle cards, win-loss, decks, demos, objections, ROI and persona value props (sales-enablement), launches (launch), GTM plans and market sizing (marketing-plan) / ali adds competitor tiers with the status quo and intel signals beyond the website, tiered cross-team launch timelines with a metrics board and post-launch report, an international market-entry playbook, a 30-second pitch template
- Quality: corey n/a · ali 3 — sound PMM structure, but many fixed numbers (firmographic ranges, Series A market sequence with ARR targets, budgets per launch tier, CPLs per country, KPI targets) and country stereotypes
- Decision: fold. No corey gap justifies a separate skill; one skill per topic.
- Taken from ali:
  - ICP, positioning, messaging hierarchy, validation, positioning map → product-marketing/references/positioning.md (previous agent)
  - Elevator Pitch (30 Seconds) → product-marketing/references/positioning.md § Capturing the Result (this pass)
  - Competitive Intelligence (tiers incl. status quo, trials, sales-call mentions, job postings, monitoring cadence) → competitor-profiling/references/intel-program.md, linked from § Updating Profiles; competitor-profiling/SOURCES.md created
  - launch-checklists.md and Product Launch Planning (tier selection, Tier 1/2/3 timelines, metrics board, post-launch report) → launch/references/launch-tiers.md (new file only; link and SOURCES row pending, see report)
  - International Expansion and international-gtm.md (prioritization, readiness gate, market profile, entry phases, staffing options, localization checklist, per-market measurement) → marketing-plan/references/international-gtm.md (new file only; link and SOURCES pending)
- Dropped from ali:
  - Battlecard template, win/loss tracking, sales deck structure, demo flow, sales-marketing handoff rhythm → sales-enablement's battle card, win-loss workflow and reference, deck frameworks and demo scripts are more complete
  - messaging-templates.md persona messaging, objection scripts, competitive statements, channel copy → sales-enablement (value prop by persona, objection library), copywriting, ads; the examples carry invented claims ("95% accuracy", "only use 20% of features")
  - Firmographics template ranges, Series A market sequence, launch budgets, per-country channel mixes and CPLs, PMM KPI targets and monthly rhythm → fixed numbers and a default market order, against the no-default-market rule
  - US/UK/DACH/France/Canada playbooks → country generalizations; replaced by a market-profile template filled from the business's own evidence
  - Proactive Triggers → already in product-marketing § When Positioning Isn't Settled; Output Artifacts and Communication → generic
- Conflicts resolved: battle card structure (ali "they say / reality") vs. corey's evidence-based card → corey's kept
- Result: no folder; content spread over 4 skills (1 edit in batch, 3 outside: one fully done, two new files awaiting link lines)

