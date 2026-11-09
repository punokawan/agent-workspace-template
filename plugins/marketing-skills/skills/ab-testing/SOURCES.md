# Sources: ab-testing

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md | edited: description opens with what the skill does; "sample size" trigger added; version reset to 1.0.0; `sources` added |
| frontmatter | ali `ab-test-setup` @8f08254 | skills/ab-test-setup/SKILL.md § frontmatter | edited: "size a test" and "read a test result" triggers taken from its description |
| SKILL.md § title and intro | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § A/B Test Setup | as is |
| SKILL.md § Initial Assessment | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Initial Assessment | edited: product context pointer now refers to product-marketing (per-product location, central pass) |
| SKILL.md § Core Principles | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Core Principles | as is |
| SKILL.md § Hypothesis Framework | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Hypothesis Framework | as is |
| SKILL.md § Test Types | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Test Types | as is |
| SKILL.md § Sample Size | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Sample Size | edited: Quick Reference table kept; calculators relabeled as cross-checks, with the fixed-horizon caveat |
| SKILL.md § Sample Size › Calculate It | ali `ab-test-setup` @8f08254 | skills/ab-test-setup/SKILL.md § Sample Size › Calculate It (bundled tool) | edited: rewritten for the adapted script (--variants, --exposure, flags); "size before approval" rule kept |
| SKILL.md § Metrics Selection | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Metrics Selection | as is |
| SKILL.md § Designing Variants | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Designing Variants | as is |
| SKILL.md § Traffic Allocation | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Traffic Allocation | as is |
| SKILL.md § Implementation | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Implementation | as is |
| SKILL.md § Running the Test | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Running the Test | as is |
| SKILL.md § Analyzing Results | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Analyzing Results | as is |
| SKILL.md § Documentation | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Documentation | as is |
| SKILL.md § Growth Experimentation Program | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Growth Experimentation Program | as is |
| SKILL.md § [Experiment Name] | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § [Experiment Name] | as is (the playbook template inside a code block in § Growth Experimentation Program, through Experiment Cadence) |
| SKILL.md § Common Mistakes | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Common Mistakes | as is |
| SKILL.md § Task-Specific Questions | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Task-Specific Questions | as is |
| SKILL.md § Related Skills | corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Related Skills | edited: cro and analytics lines given conditions |
| SKILL.md § Related Skills | ali `ab-test-setup` @8f08254 | skills/ab-test-setup/SKILL.md § Related Skills | edited: page-cro (ideas vs. design) and analytics-tracking (before the test) conditions, plus the pricing-strategy line; renamed to cro, analytics, pricing |
| SKILL.md § closing sources line | merge | — | new: links this file, as the library requires |
| references/sample-size-guide.md | corey `ab-testing` @96798cf | skills/ab-testing/references/sample-size-guide.md | edited: one sentence ties the tables to the bundled calculator's formula |
| references/test-templates.md | corey `ab-testing` @96798cf | skills/ab-testing/references/test-templates.md | as is |
| scripts/sample_size_calculator.py | ali `ab-test-setup` @8f08254 | skills/ab-test-setup/scripts/sample_size_calculator.py | edited: pooled-variance formula so results match the reference tables; standard-library NormalDist replaces the hand-coded inverse CDF; --variants (Bonferroni) and --exposure added; duration uses the guide's formula; the 0-100 design score replaced by flags on the guide's 7/30/60-day rules; input validation; emoji removed |
| evals/evals.json | corey `ab-testing` @96798cf | skills/ab-testing/evals/evals.json | as is |
| Credit: American Statistical Association p-value statement, cited in § Analyzing Results and in references/sample-size-guide.md | third party, via corey `ab-testing` @96798cf | skills/ab-testing/SKILL.md § Analyzing Results | as is |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
