# Sources: schema

| Part | From | Upstream file | Changed here |
|---|---|---|---|
| frontmatter | corey `schema` @96798cf | skills/schema/SKILL.md (frontmatter) | edited: audit, validation, video, Search Console error, and entity triggers added; local-seo-manager pointer; version reset to 1.0.0; sources added |
| SKILL.md § Initial Assessment | corey `schema` @96798cf | skills/schema/SKILL.md § Initial Assessment | edited: product context pointer now refers to product-marketing (per-product location, central pass) |
| SKILL.md § Core Principles | corey `schema` @96798cf | skills/schema/SKILL.md § Core Principles | as is |
| SKILL.md § Workflow by Job | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § How This Skill Works (Modes 1–3) | edited: rendered HTML first, so JS-injected markup is audited; retired-feature check added; tied to this skill's references |
| SKILL.md § Common Schema Types | corey `schema` @96798cf | skills/schema/SKILL.md § Common Schema Types | edited: VideoObject row; note that "Required" is this skill's minimum and Google's pages decide |
| SKILL.md § Common Schema Types | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § Schema Type Selection | edited: page-type table and stacking rules kept; SearchAction, HowTo, and FAQPage rich-result rows corrected; video and SaaS rows added |
| SKILL.md § Quick Reference | corey `schema` @96798cf | skills/schema/SKILL.md § Quick Reference | edited: VideoObject entry added (next row); the rest as is |
| SKILL.md § Quick Reference | ali `schema-markup` @8f08254 | skills/schema-markup/references/schema-types-guide.md § VideoObject | edited: required set reduced to name, thumbnailUrl, uploadDate |
| SKILL.md § Multiple Schema Types | corey `schema` @96798cf | skills/schema/SKILL.md § Multiple Schema Types | edited: Site-Wide vs Per-Page table added (next row); the rest as is |
| SKILL.md § Multiple Schema Types | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § Per-Page vs Site-Wide | edited: sitelinks search box row removed; Organization placed on homepage or About page and referenced by `@id` |
| SKILL.md § Schema for AI Search and Entities | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § Schema and AI Search | edited: "FAQPage increases citation likelihood" replaced by the evidence-based stance of ai-seo; visible-facts rule added |
| SKILL.md § Validation and Testing | corey `schema` @96798cf | skills/schema/SKILL.md § Validation and Testing | edited: Common Errors list replaced by the table below |
| SKILL.md § Validation and Testing | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § Testing & Validation, § Common Mistakes, § Proactive Triggers | edited: errors-versus-warnings and recrawl notes; error table merged with corey's three errors and four proactive checks; "Product inside Article is invalid" dropped; bundled validator usage |
| SKILL.md § Implementation | corey `schema` @96798cf | skills/schema/SKILL.md § Implementation | edited: plugin note on duplicate entities |
| SKILL.md § Implementation | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § Per-Page vs Site-Wide (CMS implementation shortcuts) | edited: platform names generalized; server-side generation rule |
| SKILL.md § Output Format | corey `schema` @96798cf | skills/schema/SKILL.md § Output Format | edited: audit report, implementation plan, and fixes formats added (next row); the rest as is |
| SKILL.md § Output Format | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § Output Artifacts, § Communication | edited: audit report table, implementation matrix, change-log fixes; confidence tags became verified/unverified tied to rendering |
| SKILL.md § Task-Specific Questions | corey `schema` @96798cf | skills/schema/SKILL.md § Task-Specific Questions | as is |
| SKILL.md § Related Skills | corey `schema` @96798cf | skills/schema/SKILL.md § Related Skills | edited: local-seo-manager added |
| SKILL.md § Related Skills | ali `schema-markup` @8f08254 | skills/schema-markup/SKILL.md § Related Skills | edited: content-strategy entry |
| references/schema-examples.md | corey `schema` @96798cf | skills/schema/references/schema-examples.md | edited: Wikidata `sameAs` in the Organization example; contents list |
| references/schema-examples.md § VideoObject | ali `schema-markup` @8f08254 | skills/schema-markup/references/implementation-patterns.md § VideoObject | edited: placeholders replaced with example values; watch-page note |
| references/schema-examples.md § Values Reference | ali `schema-markup` @8f08254 | skills/schema-markup/references/implementation-patterns.md § Duration Format Reference, § Availability Values Reference | edited: itemCondition and date lines added |
| references/type-checklists.md | ali `schema-markup` @8f08254 | skills/schema-markup/references/schema-types-guide.md | edited: corrected to current Google features (no FAQ, HowTo, or sitelinks rich results; closed-day hours as 00:00–00:00; VideoObject description recommended; no copied ratings); LocalBusiness privacy rule from corey's local references |
| scripts/schema_validator.py | ali `schema-markup` @8f08254 | skills/schema-markup/scripts/schema_validator.py | edited: top-level arrays and subtypes handled; rules aligned with SKILL.md; @context, URL, date, date-order, price, placeholder, and retired-feature checks; --json and --demo flags; unused import and emoji removed |
| evals/evals.json | corey `schema` @96798cf | skills/schema/evals/evals.json | as is |

corey = https://github.com/coreyhaines31/marketingskills (MIT, Corey Haines) · ali = https://github.com/alirezarezvani/claude-skills, folder marketing-skill/ (MIT, Alireza Rezvani)
