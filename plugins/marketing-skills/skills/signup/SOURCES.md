# Sources: signup

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `signup` @96798cf | skills/signup/SKILL.md | edited: description opens with what the skill does; version reset to 1.0.0; `sources` added |
| frontmatter | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Proactive Triggers | edited: point 4 (should we require a credit card) became a description trigger, with SSO |
| SKILL.md § title and intro | corey `signup` @96798cf | skills/signup/SKILL.md § Signup Flow CRO | as is |
| SKILL.md § Initial Assessment | corey `signup` @96798cf | skills/signup/SKILL.md § Initial Assessment | edited: product context pointer now refers to product-marketing (per-product location, central pass) |
| SKILL.md § Find Where the Flow Leaks | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Related Skills | edited: WHEN/WHEN NOT routing for page-cro and onboarding-cro turned into a loss-by-step table (renamed cro, onboarding) |
| SKILL.md § Find Where the Flow Leaks | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Tools | edited: "start the audit at the worst step" rule |
| SKILL.md § Find Where the Flow Leaks | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Proactive Triggers | edited: point 2 (low trial conversion: wrong expectations or wrong users) |
| SKILL.md § Core Principles | corey `signup` @96798cf | skills/signup/SKILL.md § Core Principles | as is |
| SKILL.md § Field-by-Field Optimization | corey `signup` @96798cf | skills/signup/SKILL.md § Field-by-Field Optimization | as is |
| SKILL.md § Single-Step vs. Multi-Step | corey `signup` @96798cf | skills/signup/SKILL.md § Single-Step vs. Multi-Step | as is |
| SKILL.md § Trust and Friction Reduction | corey `signup` @96798cf | skills/signup/SKILL.md § Trust and Friction Reduction | as is |
| SKILL.md § Mobile Signup Optimization | corey `signup` @96798cf | skills/signup/SKILL.md § Mobile Signup Optimization | as is |
| SKILL.md § Post-Submit Experience | corey `signup` @96798cf | skills/signup/SKILL.md § Post-Submit Experience | as is |
| SKILL.md § Measurement | corey `signup` @96798cf | skills/signup/SKILL.md § Measurement | edited: Key Metrics and What to Track kept; Find the Drop-Off Step subsection added |
| SKILL.md § Measurement › Find the Drop-Off Step | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Tools | edited: rewritten for the adapted script (input format, stage field, 25% threshold, quote numbers in Impact) |
| SKILL.md § Output Format | corey `signup` @96798cf | skills/signup/SKILL.md § Output Format | edited: field set grouped by step and screen-by-screen copy added to Form Redesign |
| SKILL.md § Output Format | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Output Artifacts | edited: field set by signup step, flow spec with copy per screen, SSO and auth decision table |
| SKILL.md § Output Format | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Communication | edited: points 2-6 (field-removal test, SSO always considered, post-submit always covered, mobile separate, fix vs. test) became the audit standards |
| SKILL.md § Common Signup Flow Patterns | corey `signup` @96798cf | skills/signup/SKILL.md § Common Signup Flow Patterns | as is |
| SKILL.md § Experiment Ideas | corey `signup` @96798cf | skills/signup/SKILL.md § Experiment Ideas | as is |
| SKILL.md § Task-Specific Questions | corey `signup` @96798cf | skills/signup/SKILL.md § Task-Specific Questions | as is |
| SKILL.md § Enrichment and Sales-Assisted Routing | corey `signup` @96798cf | skills/signup/SKILL.md § Enrichment and Sales-Assisted Routing | as is |
| SKILL.md § Related Skills | corey `signup` @96798cf | skills/signup/SKILL.md § Related Skills | edited: the two cro lines merged; routing conditions added |
| SKILL.md § Related Skills | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/SKILL.md § Related Skills | edited: conditions for onboarding-cro, page-cro and ab-test-setup ("instrument drop-off first"), plus the paywall-upgrade-cro line; renamed to onboarding, cro, ab-testing, paywalls; analytics line added for the instrumentation step |
| SKILL.md § closing sources line | merge | — | new: links this file, as the library requires |
| scripts/funnel_drop_analyzer.py | ali `signup-flow-cro` @8f08254 | skills/signup-flow-cro/scripts/funnel_drop_analyzer.py | edited: input validation (order, counts, keys); optional "stage" field and safer stage guessing; cause lists re-keyed so each drop gets causes for the step people failed to reach; medium drops at known stages get the stage list; tool names and the arbitrary 0-100 health score removed; no-loss funnels handled; emoji removed |
| evals/evals.json | corey `signup` @96798cf | skills/signup/evals/evals.json | as is |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
