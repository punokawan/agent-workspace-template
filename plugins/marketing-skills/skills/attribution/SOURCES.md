# Sources: attribution

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `attribution` @96798cf | skills/attribution/SKILL.md | edited: product-named "SavvyCal/Calendly attribution" trigger replaced by "score my journeys by model" to stay under 1024 characters; version reset to 1.0.0; `sources` added |
| SKILL.md § Boundaries — what this skill does NOT own | corey `attribution` @96798cf | skills/attribution/SKILL.md § Boundaries — what this skill does NOT own | as is |
| SKILL.md § Pillar A — Interpretation | corey `attribution` @96798cf | skills/attribution/SKILL.md § Pillar A — Interpretation | edited: "Score your own journeys" paragraph added at the end of §2; everything else as is |
| SKILL.md § Pillar A — Interpretation | ali `campaign-analytics` @8f08254 | skills/campaign-analytics/SKILL.md § How to Use (Attribution Analysis), § Scripts (1. attribution_analyzer.py) | edited: rewritten for the adapted script (six models, `--file`, `--credit`, sample-size note) and tied to §3 and §4 |
| SKILL.md § Pillar B — Own your attribution (first-party) | corey `attribution` @96798cf | skills/attribution/SKILL.md § Pillar B — Own your attribution (first-party) | as is |
| SKILL.md § Output format | corey `attribution` @96798cf | skills/attribution/SKILL.md § Output format | as is |
| SKILL.md § The question | corey `attribution` @96798cf | skills/attribution/SKILL.md § The question | as is |
| SKILL.md § Source of truth | corey `attribution` @96798cf | skills/attribution/SKILL.md § Source of truth | as is |
| SKILL.md § What each source says | corey `attribution` @96798cf | skills/attribution/SKILL.md § What each source says | as is |
| SKILL.md § Model comparison (for long cycles) | corey `attribution` @96798cf | skills/attribution/SKILL.md § Model comparison (for long cycles) | as is |
| SKILL.md § Confidence & gaps | corey `attribution` @96798cf | skills/attribution/SKILL.md § Confidence & gaps | as is |
| SKILL.md § Recommendation | corey `attribution` @96798cf | skills/attribution/SKILL.md § Recommendation | as is |
| SKILL.md § Tool Integrations | corey `attribution` @96798cf | skills/attribution/SKILL.md § Tool Integrations | as is |
| SKILL.md § Related Skills | corey `attribution` @96798cf | skills/attribution/SKILL.md § Related Skills | edited: ads line and closing "Sources and credits" line added |
| evals/evals.json | corey `attribution` @96798cf | skills/attribution/evals/evals.json | as is |
| references/attribution-models.md | corey `attribution` @96798cf | skills/attribution/references/attribution-models.md | edited: § Scoring your own journeys appended; everything else as is |
| references/attribution-models.md § Scoring your own journeys | ali `campaign-analytics` @8f08254 | skills/campaign-analytics/references/attribution-models-guide.md § Guidance on Half-Life Selection, § Practical Guidelines, § Data Requirements | edited: half-life table as is; "rank across models" rule and the three divergence patterns reworded with what to check; non-converting-journeys and under-100-journeys pitfalls became § Limits; data fields rewritten for the script's input |
| references/by-business-type.md | corey `attribution` @96798cf | skills/attribution/references/by-business-type.md | as is |
| references/first-party-tracking.md | corey `attribution` @96798cf | skills/attribution/references/first-party-tracking.md | as is |
| references/measurement-paradigms.md | corey `attribution` @96798cf | skills/attribution/references/measurement-paradigms.md | as is |
| scripts/attribution_analyzer.py | ali `campaign-analytics` @8f08254 | skills/campaign-analytics/scripts/attribution_analyzer.py | edited: last-non-direct model added (six models, matching references/attribution-models.md); `--file`/`--json` replace the positional file and `--format`; `--credit conversions` instead of silently crediting 1 when revenue is missing; optional conversion_timestamp for time-decay; ISO timestamps with Z or offsets normalised to UTC; per-journey validation errors; notes for samples under 100 and converted journeys without touches; demo journeys reproduce the reference's worked example |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
