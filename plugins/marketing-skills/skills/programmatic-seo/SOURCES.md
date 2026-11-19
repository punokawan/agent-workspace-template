# Sources: programmatic-seo

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md (frontmatter) | edited: URL-pattern trigger and local-seo-manager pointer added; version reset to 1.0.0; sources added; 2026-11-19: claude-seo pointer sentence and source added |
| SKILL.md § Initial Assessment | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Initial Assessment | edited: product context pointer now refers to product-marketing (per-product location, central pass) |
| SKILL.md § Core Principles | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Core Principles | edited; 2026-11-19: site reputation abuse bullet added under Avoid Google Penalties (next row) |
| SKILL.md § Core Principles | claude-seo `seo-programmatic` @468ed5b | skills/seo-programmatic/SKILL.md (site reputation abuse bullet) | new: EEA-dependent enforcement since 2026-08-30 |
| SKILL.md § The 12 Playbooks (Overview) | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § The 12 Playbooks (Overview) | as is |
| SKILL.md § Choosing Your Playbook | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Choosing Your Playbook | as is |
| SKILL.md § Implementation Framework | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Implementation Framework | edited: steps renumbered around the new step 3 |
| SKILL.md § Implementation Framework | ali `programmatic-seo` @8f08254 | skills/programmatic-seo/SKILL.md § Implementation Framework (3. URL Pattern Generation) | edited: step 3 "Size the URL Space" describes the reworked script (rows mode, collisions, reverse pairs) |
| SKILL.md § Quality Checks | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Quality Checks | edited: Post-Launch Monitoring lists turned into a table |
| SKILL.md § Quality Checks | ali `programmatic-seo` @8f08254 | skills/programmatic-seo/SKILL.md § Output Artifacts (Post-Launch Monitoring Plan), § Communication | edited: metric, source, trigger, and cadence columns; "define before launch" rule |
| SKILL.md § Quality Checks | claude-seo `seo-programmatic` @468ed5b | skills/seo-programmatic/SKILL.md (quality gates table, progressive rollout, human review, <30% recommendation); skills/seo-sitemap/SKILL.md § Mode 2: Generate New Sitemap (30+ / 60% gate) | new: Scale Gates table, labelled as claude-seo heuristics, with the internal disagreement noted |
| SKILL.md § Common Mistakes | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Common Mistakes | as is |
| SKILL.md § Output Format | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Output Format | edited: opportunity analysis leads the strategy document |
| SKILL.md § Output Format | ali `programmatic-seo` @8f08254 | skills/programmatic-seo/SKILL.md § Output Artifacts (Opportunity Analysis), § Communication | edited: opportunity table columns; thin-content callout for public or scraped data |
| SKILL.md § Task-Specific Questions | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Task-Specific Questions | as is |
| SKILL.md § Measure with claude-seo | claude-seo `seo-programmatic` @468ed5b | skills/seo/SKILL.md § Quick Reference; skills/seo-programmatic/SKILL.md; skills/seo-sitemap/SKILL.md; skills/seo-google/SKILL.md | new: pointers to /seo commands |
| SKILL.md § Related Skills | corey `programmatic-seo` @96798cf | skills/programmatic-seo/SKILL.md § Related Skills | edited: local-seo-manager added |
| SKILL.md § Related Skills | ali `programmatic-seo` @8f08254 | skills/programmatic-seo/SKILL.md § Related Skills | edited: content-strategy entry |
| references/playbooks.md | corey `programmatic-seo` @96798cf | skills/programmatic-seo/references/playbooks.md | as is |
| references/implementation-platforms.md | corey `programmatic-seo` @96798cf | skills/programmatic-seo/references/implementation-platforms.md | as is |
| scripts/url_pattern_generator.py | ali `programmatic-seo` @8f08254 | skills/programmatic-seo/scripts/url_pattern_generator.py | edited: argparse (`--help`, `--demo`, `--json`, `--sample`); data-backed `rows` mode; Unicode-aware slugs; collision, reverse-pair, empty-slug, non-ASCII, and unused-field checks; invented score removed; input errors reported cleanly |
| evals/evals.json | corey `programmatic-seo` @96798cf | skills/programmatic-seo/evals/evals.json | as is |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
