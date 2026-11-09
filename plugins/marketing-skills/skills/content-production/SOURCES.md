# Sources: content-production

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | ali `content-production` @8f08254 | skills/content-production/SKILL.md § frontmatter | edited: description rewritten (scope, triggers, bundled tools, routing to neighbouring skills); `license`, `author`, `category`, `updated` fields dropped; version 1.0.0; `sources` added |
| SKILL.md § intro (title and role) | ali `content-production` @8f08254 | skills/content-production/SKILL.md § intro | edited: audience list removed from the role; the "execution engine" line reworded to route strategy to content-strategy |
| SKILL.md § Before Starting | ali `content-production` @8f08254 | skills/content-production/SKILL.md § Before Starting | edited: context check uses this library's product-marketing wording; list kept |
| SKILL.md § How This Skill Works | ali `content-production` @8f08254 | skills/content-production/SKILL.md § How This Skill Works | edited: the three modes turned into a numbered list |
| SKILL.md § Mode 1: Research & Brief | ali `content-production` @8f08254 | skills/content-production/SKILL.md § Mode 1 | edited: `[NEED: source]` added to the sourcing rule; sources and success criteria added to the brief fields; template path moved to assets/ |
| SKILL.md § Mode 1: Research & Brief (coverage-grid and information-gain pointers) | merge | — | new: link the corey gap methods in copy-editing and content-strategy instead of repeating them |
| SKILL.md § Mode 2: Draft | ali `content-production` @8f08254 | skills/content-production/SKILL.md § Mode 2, § More in this skill | edited: Pick the Format added as a pointer to content-templates.md; H1 asks for a specific promise; 4-6 H2s to match the brief guide; the conclusion no longer restates the intro |
| SKILL.md § Mode 2: Draft (Draft Without AI Tells) | merge | — | new: applies the copywriting AI-tells self-check and the copy-editing humanizing workflow to drafts |
| SKILL.md § Mode 3: Optimize & Polish | ali `content-production` @8f08254 | skills/content-production/SKILL.md § Mode 3 | edited: the seo_optimizer.py, content_scorer.py, and brand_voice_analyzer.py runs removed; script checks and manual checks separated; what the gate script checks, and its H1 caveat, spelled out |
| SKILL.md § Mode 3: Optimize & Polish (Readability Pass script and targets) | ali `copy-editing` @8f08254 | skills/copy-editing/references/sweeps-detail.md § Sweep 1: Clarity, process step 1 | edited: scorer usage moved here; Flesch and passive-voice targets stated |
| SKILL.md § Mode 3: Optimize & Polish (seo-audit, ai-seo, schema pointers; AI-tell gate; voice-matching pointer) | merge | — | new: route on-page depth, AI-search extractability, structured data, and voice to the skills that cover them |
| SKILL.md § Problems to Flag | ali `content-production` @8f08254 | skills/content-production/SKILL.md § Proactive Triggers | edited: thin-content risk judged by subtopic coverage, not word count; cannibalization fix points to content refresh |
| SKILL.md § Output Format | ali `content-production` @8f08254 | skills/content-production/SKILL.md § Output Artifacts, § Communication | edited: rows reworded; the example finding kept; owner/deadline rule and emoji confidence tags dropped |
| SKILL.md § Related Skills (content-strategy, copy-editing, copywriting, ai-seo, seo-audit lines) | ali `content-production` @8f08254 | skills/content-production/SKILL.md § Related Skills | edited: aeo renamed to ai-seo; content-humanizer folded into copy-editing |
| SKILL.md § Related Skills (schema and social lines) | merge | — | new: structured data and distribution for the finished piece |
| SKILL.md last line (Sources and credits) | merge | — | new: links this file |
| references/content-brief-guide.md | ali `content-production` @8f08254 | skills/content-production/references/content-brief-guide.md | edited: the "competitor blog posts" red-flag line reworded to trace claims to primary sources |
| references/content-templates.md | ali `content-production` @8f08254 | skills/content-production/references/content-templates.md | edited: title and intro reworded; lengths marked as typical; competitors pointer added; em dashes removed from H2 skeletons; pillar H1 no longer "The Complete Guide to"; the duplicate quality checklist replaced with a pointer (its answer-first and external-link items moved to optimization-checklist.md) |
| references/optimization-checklist.md | ali `content-production` @8f08254 | skills/content-production/references/optimization-checklist.md | edited: content_scorer.py replaced by readability_scorer.py; passive-voice target 20% to 10%; answer-first H2 and external-link checks added; "in my experience" limited to real experience; context path wording; AI-tell self-check added to Gate 7 |
| assets/content-brief-template.md | ali `content-production` @8f08254 | skills/content-production/templates/content-brief-template.md | edited: moved from templates/ to assets/ (Agent Skills directory convention); text unchanged |
| scripts/content_quality_gates.py | ali `content-production` @8f08254 | skills/content-production/scripts/content_quality_gates.py | edited: demo statistics attributed to named companies replaced with labelled placeholders |
| scripts/readability_scorer.py | ali `copy-editing` @8f08254 | skills/copy-editing/scripts/readability_scorer.py | as is |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
