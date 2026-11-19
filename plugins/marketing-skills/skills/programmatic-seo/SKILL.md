---
name: programmatic-seo
description: When the user wants to create SEO-driven pages at scale using templates and data. Also use when the user mentions "programmatic SEO," "template pages," "pages at scale," "directory pages," "location pages," "[keyword] + [city] pages," "comparison pages," "integration pages," "building many pages for SEO," "pSEO," "generate 100 pages," "data-driven pages," "templated landing pages," or "which CMS for pSEO." Use this whenever someone wants to create many similar pages targeting different keywords or locations, or wants to check a URL pattern before building it. For auditing existing SEO issues, see seo-audit. For content strategy planning, see content-strategy. For a local business's own location and service-area pages, see local-seo-manager. To audit a live page set with tools, use the claude-seo plugin's `/seo programmatic` instead.
metadata:
  version: 1.0.0
  sources: "corey:programmatic-seo@96798cf; ali:programmatic-seo@8f08254; claude-seo:seo-programmatic@468ed5b"
---

# Programmatic SEO

You are an expert in programmatic SEO—building SEO-optimized pages at scale using templates and data. Your goal is to create pages that rank, provide value, and avoid thin content penalties.

## Initial Assessment

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before designing a programmatic SEO strategy, understand:

1. **Business Context**
   - What's the product/service?
   - Who is the target audience?
   - What's the conversion goal for these pages?

2. **Opportunity Assessment**
   - What search patterns exist?
   - How many potential pages?
   - What's the search volume distribution?

3. **Competitive Landscape**
   - Who ranks for these terms now?
   - What do their pages look like?
   - Can you realistically compete?

---

## Core Principles

### 1. Unique Value Per Page
- Every page must provide value specific to that page
- Not just swapped variables in a template
- Maximize unique content—the more differentiated, the better

### 2. Proprietary Data Wins
Hierarchy of data defensibility:
1. Proprietary (you created it)
2. Product-derived (from your users)
3. User-generated (your community)
4. Licensed (exclusive access)
5. Public (anyone can use—weakest)

### 3. Clean URL Structure
**Prefer subfolders to subdomains.** Google doesn't rank one above the other, but a subfolder inherits the main site's internal links and structure, while a subdomain needs its own (see [implementation-platforms.md](references/implementation-platforms.md)):
- Good: `yoursite.com/templates/resume/`
- Bad: `templates.yoursite.com/resume/`

### 4. Genuine Search Intent Match
Pages must actually answer what people are searching for.

### 5. Quality Over Quantity
Better to have 100 great pages than 10,000 thin ones.

### 6. Avoid Google Penalties
- No doorway pages
- No keyword stuffing
- No duplicate content
- Genuine utility for users
- No site reputation abuse: third-party or hosted programmatic content on a strong domain is a policy risk. Since 2026-08-30 (Google announcement) enforcement depends on where the searcher is: manual actions apply outside the EEA, while for EEA users the third-party section may be categorized separately from the main domain. Report the risk for both audiences.

---

## The 12 Playbooks (Overview)

| Playbook | Pattern | Example |
|----------|---------|---------|
| Templates | "[Type] template" | "resume template" |
| Curation | "best [category]" | "best website builders" |
| Conversions | "[X] to [Y]" | "$10 USD to GBP" |
| Comparisons | "[X] vs [Y]" | "webflow vs wordpress" |
| Examples | "[type] examples" | "landing page examples" |
| Locations | "[service] in [location]" | "dentists in austin" |
| Personas | "[product] for [audience]" | "crm for real estate" |
| Integrations | "[product A] [product B] integration" | "slack asana integration" |
| Glossary | "what is [term]" | "what is pSEO" |
| Translations | Content in multiple languages | Localized content |
| Directory | "[category] tools" | "ai copywriting tools" |
| Profiles | "[entity name]" | "stripe ceo" |

**For detailed playbook implementation**: See [references/playbooks.md](references/playbooks.md)

---

## Choosing Your Playbook

| If you have... | Consider... |
|----------------|-------------|
| Proprietary data | Directories, Profiles |
| Product with integrations | Integrations |
| Design/creative product | Templates, Examples |
| Multi-segment audience | Personas |
| Local presence | Locations |
| Tool or utility product | Conversions |
| Content/expertise | Glossary, Curation |
| Competitor landscape | Comparisons |

You can layer multiple playbooks (e.g., "Best coworking spaces in San Diego").

---

## Implementation Framework

### 1. Keyword Pattern Research

**Identify the pattern:**
- What's the repeating structure?
- What are the variables?
- How many unique combinations exist?

**Validate demand:**
- Aggregate search volume
- Volume distribution (head vs. long tail)
- Trend direction

### 2. Data Requirements

**Identify data sources:**
- What data populates each page?
- Is it first-party, scraped, licensed, public?
- How is it updated?

### 3. Size the URL Space

Expand the pattern before designing templates, and cut variables until the page count matches the data you have:

```bash
python3 scripts/url_pattern_generator.py pattern.json      # --json for every URL, --demo for a sample
```

The config holds a `template` such as `{service}-in-{city}`, a `base_url`, and either `rows` (only the combinations your data supports, preferred) or `variables` (every combination). The script reports the page count and URL lengths, and flags slug collisions (two inputs, one URL), reverse pairs (`a-vs-b` and `b-vs-a`: publish one order and 301 the other), empty or non-ASCII slugs, and placeholders without data. It reads only the config file and writes nothing. A clean report means the URL pattern is sound, not that each page deserves to exist.

### 4. Template Design

**Page structure:**
- Header with target keyword
- Unique intro (not just variables swapped)
- Data-driven sections
- Related pages / internal links
- CTAs appropriate to intent

**Ensuring uniqueness:**
- Each page needs unique value
- Conditional content based on data
- Original insights/analysis per page

### 5. Internal Linking Architecture

**Hub and spoke model:**
- Hub: Main category page
- Spokes: Individual programmatic pages
- Cross-links between related spokes

**Avoid orphan pages:**
- Every page reachable from main site
- XML sitemap for all pages
- Breadcrumbs with structured data

### 6. Indexation Strategy

- Prioritize high-volume patterns
- Noindex very thin variations
- Manage crawl budget thoughtfully
- Separate sitemaps by page type

### 7. Choose the Build Platform

Check that the platform can hold the page count, refresh the data, render server-side HTML, branch on data for conditional sections, and control indexation per page. Prefer the existing site's CMS if it can; otherwise serve the set on a subpath of the main domain. Options and tradeoffs: [references/implementation-platforms.md](references/implementation-platforms.md).

---

## Quality Checks

### Pre-Launch Checklist

**Content quality:**
- [ ] Each page provides unique value
- [ ] Answers search intent
- [ ] Readable and useful

**Technical SEO:**
- [ ] Unique titles and meta descriptions
- [ ] Proper heading structure
- [ ] Schema markup implemented
- [ ] Page speed acceptable

**Internal linking:**
- [ ] Connected to site architecture
- [ ] Related pages linked
- [ ] No orphan pages

**Indexation:**
- [ ] In XML sitemap
- [ ] Crawlable
- [ ] No conflicting noindex

### Scale Gates (heuristics, not Google rules)

claude-seo uses these gates. They are its own heuristics, not Google rules, and claude-seo itself is not consistent: its sitemap skill warns at 30+ location pages and asks for 60%+ unique content. Use them as review triggers, not pass marks.

| Gate | claude-seo threshold |
|---|---|
| Page count | Warn at 100+ pages without a content review; stop at 500+ pages without justification and an explicit go-ahead |
| Unique content per page | Flag as thin under 40%; stop under 30% |
| Rollout | Publish in batches of 50–100 pages, watch indexing and rankings for 2–4 weeks before the next batch |
| Human review | Read a 5–10% sample of generated pages before publishing |

### Post-Launch Monitoring

Define the plan before launch, not after a problem appears:

| Metric | Source | Act when | Cadence |
|---|---|---|---|
| Indexation rate (indexed ÷ submitted, per page type) | Search Console page indexing, one sitemap per page type | Low or falling 6–8 weeks after launch | Weekly |
| Impressions, clicks, rankings for the page set | Search Console filtered by folder; a rank-tracked query sample | Falls for several weeks in a row | Weekly |
| Engagement and conversion | Analytics, by template | Below comparable hand-built pages | Monthly |
| Thin or duplicate signals | "Crawled - currently not indexed," duplicate-canonical reports | Growing share of the set | Monthly |
| Manual actions and crawl errors | Search Console | Any | Weekly |

---

## Common Mistakes

- **Thin content**: Just swapping city names in identical content
- **Keyword cannibalization**: Multiple pages targeting same keyword
- **Over-generation**: Creating pages with no search demand
- **Poor data quality**: Outdated or incorrect information
- **Ignoring UX**: Pages exist for Google, not users

---

## Output Format

### Strategy Document
- Opportunity analysis (lead with it)
- Implementation plan
- Content guidelines

**Opportunity analysis table:**

| Pattern | Example query | Pages (from data) | Aggregate search volume | Data source and type | Who ranks now | Thin-content risk |
|---|---|---|---|---|---|---|

Rate the data type with the defensibility hierarchy above. Call out thin-content risk explicitly whenever the data is public or scraped.

### Page Template
- URL structure
- Title/meta templates
- Content outline
- Schema markup

---

## Task-Specific Questions

1. What keyword patterns are you targeting?
2. What data do you have (or can acquire)?
3. How many pages are you planning?
4. What does your site authority look like?
5. Who currently ranks for these terms?
6. What's your technical stack?

---

## Measure with claude-seo

If the claude-seo plugin is installed (Claude Code only; not in Codex), run these for live data. Otherwise use the method in this skill.

| Need | Command | What it adds |
|---|---|---|
| Audit or plan a programmatic page set | `/seo programmatic [url\|plan]` | Applies the scale gates above; `metadata_template.py` finds one templated title/description shape repeated across the set (a deterministic string heuristic) |
| Sitemaps for the set | `/seo sitemap <url>` | `sitemap_discovery.py` finds the sitemaps; checks size and split limits |
| Index status of sample pages | `/seo google inspect <url>` | `gsc_inspect.py` URL Inspection; needs Google API setup |

---

## Related Skills

- **seo-audit**: For auditing programmatic pages after launch
- **schema**: For adding structured data
- **site-architecture**: For page hierarchy, URL structure, and internal linking
- **competitors**: For comparison page frameworks
- **content-strategy**: For deciding whether a playbook fits the wider content plan
- **local-seo-manager**: For a local business's own location and service-area pages

Sources and credits: [SOURCES.md](SOURCES.md)
