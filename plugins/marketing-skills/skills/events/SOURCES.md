# Sources: events

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `events` @96798cf | skills/events/SKILL.md | edited: description opens with what the skill does; webinar format, follow-up, and evergreen triggers added; some synonym triggers collapsed; `sources` added |
| frontmatter | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/SKILL.md § frontmatter | edited: "scores each funnel stage to find where it leaks" folded into the description |
| SKILL.md § Before Starting | corey `events` @96798cf | skills/events/SKILL.md § Before Starting | edited: product context pointer now refers to product-marketing (per-product location, central pass) |
| SKILL.md § Pick Your Role | corey `events` @96798cf | skills/events/SKILL.md § Pick Your Role | as is |
| SKILL.md § Which Events to Invest In (Portfolio First) | corey `events` @96798cf | skills/events/SKILL.md § Which Events to Invest In (Portfolio First) | as is |
| SKILL.md § The Universal Arc: 20% Event, 80% Before-and-After | corey `events` @96798cf | skills/events/SKILL.md § The Universal Arc: 20% Event, 80% Before-and-After | as is |
| SKILL.md § Hosting: Choose the Format for the Job | corey `events` @96798cf | skills/events/SKILL.md § Hosting: Choose the Format for the Job | edited: webinar row links the new webinar-formats.md and webinar-plan-template.md |
| SKILL.md § Attending (No Booth, No Stage) | corey `events` @96798cf | skills/events/SKILL.md § Attending (No Booth, No Stage) | as is |
| SKILL.md § The Content Arc: Every Event Is a Content Engine | corey `events` @96798cf | skills/events/SKILL.md § The Content Arc: Every Event Is a Content Engine | as is |
| SKILL.md § Measurement: Pipeline, Not Applause | corey `events` @96798cf | skills/events/SKILL.md § Measurement: Pipeline, Not Applause | edited: subsection "Score a Webinar Funnel" appended |
| SKILL.md § Measurement › Score a Webinar Funnel | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/SKILL.md § How This Skill Works (Mode 2: Optimize / Rescue) | edited: rewritten for the updated script (`--json`, input fields); "measured vs. benchmark" rule kept without confidence emoji |
| SKILL.md § Common Mistakes | corey `events` @96798cf | skills/events/SKILL.md § Common Mistakes | as is |
| SKILL.md § Related Skills | corey `events` @96798cf | skills/events/SKILL.md § Related Skills | edited: cro and ads lines appended |
| SKILL.md § Related Skills | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/SKILL.md § Related Skills | edited: page-cro and paid-ads lines, renamed to cro and ads; the others were already covered |
| SKILL.md § closing sources line | merge | — | new: links this file, as the library requires |
| references/webinar-funnel.md | corey `events` @96798cf | skills/events/references/webinar-funnel.md | edited: intro, funnel-at-a-glance table, Stages 0–4 base text, Metrics That Diagnose kept; footer updated to credit the merged material |
| references/webinar-funnel.md § intro: "By audience temperature" table and other stage ranges | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/references/benchmarks.md § Funnel Stage Benchmarks, § By Audience Temperature | edited: implication column folded into the conversion column; ranges marked directional |
| references/webinar-funnel.md § Plan Backward from the Goal | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/SKILL.md § The Funnel Math (Plan Backward) | edited: worked example kept; "label every assumed rate as a benchmark" replaces the emoji tags |
| references/webinar-funnel.md § Stage 0: format bullet | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/references/webinar-formats.md § Format Selector | edited: one bullet pointing to webinar-formats.md and webinar-plan-template.md |
| references/webinar-funnel.md § Stage 1: outcome-first headline, sales and community channels, separate tracks, two-week runway table | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/references/promotion-playbook.md § Promotion Timeline (3-Week Runway), § Channel Playbook, § Copy Patterns | edited: runway compressed to corey's two weeks; the three email sends mapped onto days −14, −7, 0 |
| references/webinar-funnel.md § Stage 2: reason to attend live | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/SKILL.md § The Five Stages (2. Show-Up); references/benchmarks.md § Show-Up Rate Factors; references/promotion-playbook.md § Copy Patterns | edited: live-only incentive, its copy line, and the single-reminder vs. full-sequence show-up figures merged into one bullet |
| references/webinar-funnel.md § Stage 3: 60-minute limit | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/references/webinar-formats.md § Structure Templates; SKILL.md § Proactive Triggers | edited: one sentence |
| references/webinar-funnel.md § Stage 4: 24-hour recording, day-by-day table, no-show opener, evergreen version | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/references/promotion-playbook.md § The Follow-Up Sequence, § Copy Patterns; SKILL.md § How This Skill Works (Mode 3: Evergreen / On-Demand) | edited: table kept; evergreen steps condensed to one bullet |
| references/webinar-funnel.md § Metrics That Diagnose: scorer and goal metrics | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/references/benchmarks.md § Conversion Benchmarks | edited: four goals in one bullet; scorer pointer added |
| references/webinar-formats.md | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/references/webinar-formats.md | edited: table of contents dropped; office hours added to the selector text; hook step names the offer upfront to match corey's live-to-close arc; summit links co-marketing |
| references/webinar-plan-template.md | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/templates/webinar-plan-template.md | edited: moved to references/; confidence emoji replaced by measured/benchmark; platform brand list replaced by a placeholder; T-5 minutes reminder added to match webinar-funnel.md |
| references/event-portfolio-strategy.md | corey `events` @96798cf | skills/events/references/event-portfolio-strategy.md | as is |
| references/speaking.md | corey `events` @96798cf | skills/events/references/speaking.md | as is |
| references/sponsorship-roi.md | corey `events` @96798cf | skills/events/references/sponsorship-roi.md | as is |
| scripts/webinar_funnel_scorer.py | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/scripts/webinar_funnel_scorer.py | edited: `--json` flag; unknown audience reported instead of silently replaced; missing optional fields no longer crash `safe_div`; docstring states stdlib only, no writes |
| evals/evals.json | corey `events` @96798cf | skills/events/evals/evals.json | edited: evals 1–7 as is; evals 8–9 appended |
| evals/evals.json: evals 8–9 | ali `webinar-marketing` @8f08254 | skills/webinar-marketing/evals/evals.json | edited: rescue-low-attendance and write-segmented-followup prompts kept; expected output rewritten for this skill's files; assertions added; plan-from-scratch dropped (corey evals cover planning) |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
