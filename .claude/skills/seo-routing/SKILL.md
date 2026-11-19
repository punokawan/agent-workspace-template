---
name: seo-routing
description: Parent map of every SEO and AI-search (GEO) skill in this workspace — picks the right one for a request. Three layers, Code (seo-geo plus the project's <project>-seo overlay, for editing a Next.js repo), Method (marketing-skills, for strategy, copy and judgment) and Measure (the claude-seo plugin's /seo commands, for tool-backed checks of a live URL with real data). Load at the start of any SEO, GEO, schema, sitemap, Core Web Vitals, Search Console, backlink, local-SEO or AI-citation task when it is not obvious which skill applies, or when a task spans more than one layer.
license: MIT
---

# SEO routing (parent)

Every SEO request falls in one of three layers. Pick the layer first, then the child skill.

| Layer | The request is about | Child |
|---|---|---|
| **Code** | Changing files in a web repo: metadata, `robots.ts`, `sitemap.ts`, JSON-LD helper, rendering | `seo-geo` + `projects/<project>/**/.claude/skills/<project>-seo/` overlay |
| **Method** | Deciding what to do: strategy, priorities, copy, page plans, policy | a `marketing-skills:*` skill (table below) |
| **Measure** | Facts about a deployed URL: what Google sees, real speed, index status, links | a claude-seo `/seo <command> <url>` |

Most real tasks chain them: **Measure → Method → Code → Measure.** Audit the live page, decide the
fix, change the code, then check the deployed page again. Only the Code layer edits a repository.

## Child map

| Need | Method (marketing-skills) | Measure (claude-seo) |
|---|---|---|
| Full site health check | `seo-audit` | `/seo audit <url>` |
| One page in depth | `seo-audit` | `/seo page <url>` |
| Crawl, index, render, JS gaps, TLS, headers | `seo-audit` | `/seo technical <url>` |
| Real Core Web Vitals, Search Console, GA4 | — | `/seo google …` |
| Did a deploy break SEO (before/after) | — | `/seo drift baseline` then `/seo drift compare` |
| Structured data | `schema` | `/seo schema <url>` |
| AI answers and citations (AI Overviews, ChatGPT, Perplexity) | `ai-seo` | `/seo geo <url>` |
| Can AI agents use the site (Lighthouse agentic, WebMCP, llms.txt) | `ai-seo` | `/seo agentic <url>` |
| Sitemaps | `site-architecture` | `/seo sitemap <url>` |
| URL structure, navigation, internal links | `site-architecture` | — |
| Keyword clusters, hub and spoke | `content-strategy` | `/seo cluster <seed>` |
| SEO roadmap | `content-strategy` | `/seo plan` |
| Content brief | `content-production` | `/seo content-brief <topic or url>` |
| Content quality and E-E-A-T of a live page | `seo-audit` | `/seo content <url>` |
| Page type does not match search intent | — | `/seo sxo <url>` |
| Pages at scale from data | `programmatic-seo` | `/seo programmatic <url>` |
| Comparison and "alternatives" pages | `competitors` | `/seo competitor-pages` |
| Earn links | `link-building` | — |
| Measure a link profile | — | `/seo backlinks <url>` |
| Local business, Google Business Profile | `local-seo-manager` | `/seo local <url>`, `/seo maps` |
| Images on a page | `seo-audit` | `/seo images <url>` |
| Generate an OG or hero image | `image` | `/seo image-gen` (paid, needs an extension) |
| hreflang and translations | `seo-audit` | `/seo hreflang <url>` |
| Bing, IndexNow | — | `/seo bing` |
| Stores and products | — | `/seo ecommerce <url>` |

Check the exact `/seo` command list in the hub skill `claude-seo:seo` before running one.

## Rules

- **Method skills are the default for advice.** When a Method skill and claude-seo disagree on a
  rule, the Method skill wins unless claude-seo cites a dated Google source the Method skill lacks.
  For example, disavow only after a manual action or self-made spam (`link-building`), never because
  a tool's "toxic ratio" is high. Word counts and page-count gates are heuristics, not Google rules.
- **Measure needs a deployed URL.** For local code, build and `curl` the page (seo-geo "Done when"),
  or measure a preview deployment.
- **Load on a live site is a capacity decision.** A full `/seo audit` fetches many pages. On a
  project whose hosting runs on a free plan, run `/seo page` on a few key URLs first. Ask the owner
  before a full crawl.
- **Fetch once, check the saved copy.** Run as written, the `/seo page` steps refetch the page in
  every script, probe every image, run Lighthouse twice and request about 12 extra paths: about
  60–100 requests for 4 URLs. Fetching each page once (`fetch_page.py`) and running `page_checks.py`
  and `parse_html.py` on the saved file gave the same findings with 6 requests (trial on a production site,
  2026-11-19).
- **Review findings before acting.** In that trial 4 of 7 page findings were false or misleading:
  lazy loading flagged on an image far below the fold, missing width/height on an image whose
  container already reserves its space, `<head>` child count flagged as "slow to lay out", and the
  brand name in a normal sentence flagged as a brand suffix.
- **Google data needs a key.** PageSpeed without a key uses a shared quota that is often exhausted
  (HTTP 429), and CrUX always needs an API key. The owner creates the key; it lives in an
  environment variable, never in a repository.
- **Paid APIs need the owner each time:** DataForSEO, Moz, Ahrefs, image generation. Free sources
  (PageSpeed, CrUX, Search Console with the owner's sign-in, Common Crawl) still need the owner to
  connect the account once.
- **Owner actions stay with the owner:** Search Console settings (including the "Search generative
  AI" control), Google Business Profile, DNS, Cloudflare and robots policy for AI bots.
- claude-seo adds a PostToolUse hook: after an Edit or Write of `.html`, `.tsx`, `.jsx`, `.vue` and
  similar files, it validates JSON-LD in that file. It blocks only on placeholders or retired types.
  It does not check `.ts` helpers or JSON built with `JSON.stringify`, so the seo-geo validation
  step still applies.
- **Codex:** claude-seo is a Claude Code plugin only. In Codex, use `seo-geo` and marketing-skills,
  and measure with `curl`, the PageSpeed Insights page and Search Console in a browser.
