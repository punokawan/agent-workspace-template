# Sources: cro

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `cro` @96798cf | skills/cro/SKILL.md | edited: description opens with what the skill does; version reset to 1.0.0; `sources` added |
| frontmatter | ali `page-cro` @8f08254 | skills/page-cro/SKILL.md § Proactive Triggers | edited: point 2 (review a new page before launch) became a description trigger |
| frontmatter | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Proactive Triggers | edited: point 3 (bad lead quality) became a description trigger |
| SKILL.md § title and intro | corey `cro` @96798cf | skills/cro/SKILL.md § Conversion Rate Optimization (CRO) | as is |
| SKILL.md § Reference Routing | corey `cro` @96798cf | skills/cro/SKILL.md § Reference Routing | as is |
| SKILL.md § Initial Assessment | corey `cro` @96798cf | skills/cro/SKILL.md § Initial Assessment | edited: product context pointer now refers to product-marketing (per-product location, central pass) |
| SKILL.md § CRO Analysis Framework | corey `cro` @96798cf | skills/cro/SKILL.md § CRO Analysis Framework | as is |
| SKILL.md § Output Format | corey `cro` @96798cf | skills/cro/SKILL.md § Output Format | edited: the four output blocks kept; each block given its required detail |
| SKILL.md § Output Format | ali `page-cro` @8f08254 | skills/page-cro/SKILL.md § Output Artifacts | edited: severity summary per dimension, at most five quick wins, rationale/effort/metric per high-impact change, test-ideas table |
| SKILL.md § Output Format | ali `page-cro` @8f08254 | skills/page-cro/SKILL.md § Communication | edited: points 2, 4, 5 and 6 (tie to dimension, apply the page-type framework, fix vs. test, traffic and audience context) became the audit standards |
| SKILL.md § Page-Specific Frameworks | corey `cro` @96798cf | skills/cro/SKILL.md § Page-Specific Frameworks | as is |
| SKILL.md § Experiment Ideas | corey `cro` @96798cf | skills/cro/SKILL.md § Experiment Ideas | as is |
| SKILL.md § Task-Specific Questions | corey `cro` @96798cf | skills/cro/SKILL.md § Task-Specific Questions | as is |
| SKILL.md § Related Skills | corey `cro` @96798cf | skills/cro/SKILL.md § Related Skills | edited: signup, popups, copywriting and ab-testing lines kept with routing conditions added |
| SKILL.md § Related Skills | ali `page-cro` @8f08254 | skills/page-cro/SKILL.md § Related Skills | edited: WHEN/WHEN NOT conditions for signup-flow-cro, popup-cro, copywriting, ab-test-setup and onboarding-cro, renamed to signup, popups, ab-testing, onboarding |
| SKILL.md § Related Skills | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Related Skills | edited: analytics-tracking line, renamed to analytics |
| SKILL.md § Form Optimization | corey `cro` @96798cf | skills/cro/SKILL.md § Form Optimization | edited: revops hand-off and form.md pointer kept; Form Field Analyzer subsection and the closing sources line appended |
| SKILL.md § Form Optimization › Form Field Analyzer | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Tools | edited: rewritten for the adapted script (HTML input, new checks, no score) |
| SKILL.md § closing sources line | merge | — | new: links this file, as the library requires |
| references/form.md | corey `cro` @96798cf | skills/cro/references/form.md | edited: Core Principle 4, the lead-quality note, Output Standards and the analytics link added; everything else as is |
| references/form.md § Core Principles › 4. Every Required Field Needs a Downstream Use | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Core Principles | edited: points 1-3 (field ceiling, required-field justification, high-friction fields) reworded |
| references/form.md § Core Principles › When the Complaint Is Lead Quality | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Proactive Triggers | edited: point 3 expanded with the volume trade-off |
| references/form.md § Output Format › Output Standards | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Communication | edited: points 1-6 reworded |
| references/form.md § Output Format › Output Standards | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Output Artifacts | edited: "top 3-5 test hypotheses with variant, metric, priority" point |
| references/form.md § Related Skills | ali `form-cro` @8f08254 | skills/form-cro/SKILL.md § Related Skills | edited: analytics-tracking line, renamed to analytics |
| references/experiments.md | corey `cro` @96798cf | skills/cro/references/experiments.md | as is |
| scripts/form_field_analyzer.py | ali `form-cro` @8f08254 | skills/form-cro/scripts/form_field_analyzer.py | edited: argparse with --help; label detection fixed (label for=id in any order, wrapping labels, fieldset legends, aria names); radio and checkbox groups counted once; field-count thresholds aligned with references/form.md; address and company-size checks; email/phone input-type and autocomplete=off checks; button type=button ignored; numeric score, unsourced claims and emoji removed; unreadable file is an error, not demo mode |
| evals/evals.json | corey `cro` @96798cf | skills/cro/evals/evals.json | as is |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
