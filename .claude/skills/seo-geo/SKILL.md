---
name: seo-geo
description: Search (SEO) and AI-answer (GEO) visibility for every Next.js App Router web repo — metadata and metadataBase, canonical and hreflang, sitemap and robots, noindex for private and preview routes, URLs and internal links, server-rendered content and Core Web Vitals, structured data (JSON-LD), answer-first content AI engines can cite, the AI-crawler policy, programmatic pages, privacy limits, and review severities. Project domain, locales, crawler policy and page types live in the <project>-seo overlay. Load when adding or changing a public route, page metadata, sitemap/robots, structured data, or marketing content.
license: MIT
compatibility: Next.js App Router (Metadata API, MetadataRoute)
---

<!-- Parts adapted from marketing-skills by Alireza Rezvani (MIT): https://github.com/alirezarezvani/claude-skills -->
# SEO and GEO (Next.js, all projects)

Two audiences read a public page: search engines that rank it, and AI answer engines (ChatGPT,
Perplexity, Google AI Overviews, Claude, Gemini) that quote it. Both need the same base: a page
that renders on the server, says clearly what it is, and is reachable only when it should be.

Scope: public routes — marketing, landing, public event or product pages, docs, blog. Dashboards,
consoles and anything behind auth are `noindex` and otherwise out of scope.

## Source of truth

Read in order before changing anything:
1. `projects/<project>/AGENTS.md` and `projects/<project>/<repo>/AGENTS.md` if present
2. `projects/<project>/**/.claude/skills/<project>-seo/SKILL.md` if it exists — domain, locales,
   AI-crawler policy, page types and their schema, which route groups are public
3. What the repo already has. Search first: `app/robots.ts`, `app/sitemap.ts`, `metadataBase` in
   the root layout, an existing JSON-LD helper, `opengraph-image` files. Extend them; never add a
   second sitemap, robots file or schema helper.

Local sources win over this file. This file is the engineering contract; the `marketing-skills`
plugin skills go deeper on method when they are installed. They are a Claude Code plugin only:
Codex does not have them, so in Codex this file stands alone — follow it without the plugins.

| Task | Plugin skill |
|---|---|
| Audit a live site (technical + on-page), build a findings register | `marketing-skills:seo-audit` |
| Make pages citable by AI answers, entity/facts page, `llms.txt` | `marketing-skills:ai-seo` |
| Choose and validate JSON-LD types | `marketing-skills:schema-markup` |
| URL structure, internal links, hub pages, sitemap split | `marketing-skills:site-architecture` |
| Many data-backed pages (directory, location, template pages) | `marketing-skills:programmatic-seo` |
| Rewrite claims and page copy | `marketing-skills:copywriting`, with the workspace `copywriting` skill for voice |

A larger SEO pass works as a phased plan: audit → findings register with IDs → one task per
fix → evidence (built HTML, `curl` headers, validator output) → owner actions (Search Console,
DNS) listed separately, never done by the agent. Audit in this order, because a later layer
cannot fix an earlier one: crawlable and indexed → technical (fast, working) → on-page →
content quality → authority. Each finding states Issue, Impact, Evidence, Fix and Priority, with
quick wins listed apart from heavy work. Two pages competing for the same query
(cannibalization) is a finding: merge them or canonicalize one.

## 1. Metadata

- **`metadataBase`** is set once, in the root layout, from the project's public origin (env, not a
  literal). Without it relative OG and canonical URLs break.
- **Every public route has a unique `title` and `description`**, static `metadata` or
  `generateMetadata` when it depends on data. Use a `title.template` in the layout so pages give
  only their own part and the brand is not repeated. Title about 50–60 characters, topic first,
  brand last; description about 150–160 characters, plain sentences that say what the page is
  and why to open it. No two pages share a title or description.
- **One metadata builder per project** (a small helper the public pages call) gives every
  public page the same canonical, OG and Twitter defaults and a default 1200×630 share image;
  pages override only what differs.
- **Canonical:** `alternates.canonical` on every indexable page, pointing at the one URL that
  should rank (no tracking params, consistent trailing slash).
- **Locales:** a page with translations lists them in `alternates.languages` (hreflang), including
  `x-default`. Locale list comes from the overlay.
- **Social:** `openGraph` and `twitter` fields, with an `opengraph-image` file or generated image
  per route type. Image text matches the page.
- `generateMetadata` that fetches data reuses the page's fetch (same cached call), and calls
  `notFound()` for a missing record so the page returns 404, not an empty 200.

## 2. Indexing control

- **`app/sitemap.ts`** (`MetadataRoute.Sitemap`) lists indexable URLs only, with real `lastModified`
  values. Over 50 000 URLs: `generateSitemaps`.
- **`app/robots.ts`** (`MetadataRoute.Robots`) points at the sitemap and disallows private areas.
- **Preview, staging and dev deployments are `noindex`**: robots returns `disallow: '/'` and the
  layout sets `robots: { index: false }` whenever the env is not production. A staging site in
  the index is a High finding.
- **Private and auth routes** set `robots: { index: false, follow: false }` in their layout and are
  absent from the sitemap. Robots `Disallow` alone does not keep a linked URL out of the index.
- **Non-HTML and API responses** get `X-Robots-Tag: noindex` from middleware or `headers()` in
  `next.config` — page metadata cannot reach them. Exception: the OG image route stays crawlable.
- **Internal search and filter URLs** (`?q=`, sort, pagination params) are `noindex` and carry a
  canonical to the unfiltered page.
- **One canonical host:** the non-canonical host (`www` or apex) 308-redirects to the canonical
  one, and internal links are host-free relative paths. Search Console verification is an owner
  action.
- Large or data-backed URL sets get their own sitemap (`generateSitemaps` or a route handler)
  built from the database; a sitemap or index page stays 200 when a non-critical count fails.
- Debug, test and error-demo routes return 404 in production.
- Redirects use `permanentRedirect` (308) for moved content and `redirect` for flow steps; a
  removed page returns 404 or 410, never a 200 "not found" screen.

## 3. URLs and internal links

- **URLs are for people:** lowercase, hyphenated words, no IDs or query strings on public
  content, one trailing-slash convention. At most three levels; create a directory only when its
  own page deserves to rank. Programmatic sets live in a subfolder, never a subdomain.
- **Changing a public URL ships its redirect in the same change** (`permanentRedirect` or a
  `redirects()` entry), old URL → new URL, never through a chain.
- **Breadcrumbs** on every page below home, each segment a real link, with a `BreadcrumbList`
  that matches them.
- **No orphans:** every URL in the sitemap has at least one internal link from a crawlable page,
  and key pages are no more than three clicks from home. Anchor text names the target ("pricing
  for teams"), never "click here".
- Hub and category pages carry their own content, not just a list of links; the hub links to
  every child and each child links back.

## 4. Rendering and performance

- **Content that should rank or be quoted is in the server-rendered HTML**: Server Components,
  static or ISR. Text that only appears after client JS runs is invisible to most AI crawlers.
- One `h1` per page, headings in order, descriptive link text, `alt` on meaningful images.
- Use `next/image` and `next/font`; keep LCP content out of client-only components. Core Web
  Vitals "good": LCP ≤ 2.5 s, CLS ≤ 0.1, INP ≤ 200 ms, TTFB under 800 ms. For a performance audit
  load the `web-perf` plugin skill instead of guessing.

## 5. Structured data (JSON-LD)

- One helper per project builds JSON-LD from typed data; pages pass data, never hand-write JSON.
  Render it as `<script type="application/ld+json">` with `JSON.stringify(data).replace(/</g,
  '\\u003c')` so user text cannot close the tag. It renders on the server; JSON-LD injected
  client-side or by a tag manager is often never indexed.
- **One site-wide `@graph`** with stable `@id`s (`Organization`, `WebSite`, and the product as
  `SoftwareApplication` or `Product` with offers read from the live pricing config); other pages
  reference those `@id`s instead of redeclaring them. `SearchAction` only when site search exists.
  One entity is declared once: never a separate `Organization` and `LocalBusiness` for the same
  company. `Organization.sameAs` lists the official profiles.
- Pick types that match the page: `Organization` and `WebSite` on the home page, `BreadcrumbList`
  on nested pages, then per page type (`Event`, `Product`/`Offer`, `FAQPage`, `Article`,
  `SoftwareApplication`). The overlay maps page types to schema.
- **Markup states only what the visible page states.** No hidden FAQ, no `aggregateRating`
  without real, shown reviews, no testimonials that are not verified and switched on by the owner.
  Mismatch is a Medium finding; fabricated reviews, ratings or prices are High.
- **Valid by construction:** `@context` present, absolute URLs for `url` and `image`, ISO 8601
  dates, `dateModified` not earlier than `datePublished`, a `Product` always with `offers`
  (price, currency, availability). `Article` carries `author` (a `Person`, with `sameAs` when
  there is a real profile), an `image`, and accurate dates — AI engines weigh freshness.
- Validate with the Rich Results Test or Schema.org validator before calling it done.

## 6. GEO — being cited by AI answers

- **Answer first.** Each section opens with a direct, self-contained answer (definition, number,
  date, price, steps), then the detail. An engine quotes a passage, not a page. Each `h2`
  section must still make sense when quoted alone.
- **Extractable blocks**, as the content calls for them: a one- or two-sentence definition in the
  first ~300 words; numbered steps (5–10, each verb-first and self-contained) for "how to";
  a table for "X vs Y"; an FAQ block worded the way people ask, with `FAQPage` markup.
- **Sources on every statistic** ("<source>, <year>") and name and role on every quote; an
  unsourced number is less likely to be cited.
- **Concrete and checkable:** numbers with units, dates, named entities, a short comparison table
  where one helps. Keep facts identical across pages and in the JSON-LD.
- **Every claim is verifiable.** "Free forever", "end-to-end encrypted", "official app", "used by
  hundreds of …" stay only when the owner confirms them; otherwise replace with what is true. AI
  engines repeat claims verbatim, so a false one spreads.
- **An entity (facts) page** states who and what the product is — name, maker, what it does,
  plans, contact — in short plain sentences, and a **pricing page** (static or ISR) shows prices
  from the same config the app uses. Both are linked from the footer and listed in the sitemap.
- **Stable structure:** descriptive `h2`/`h3`, anchors that do not change, FAQ blocks for real
  questions users ask, and an author/organisation and updated date where trust matters.
- **AI-crawler policy is the project's decision**, written in its overlay and implemented in
  `robots.ts`. Search-and-answer bots (`OAI-SearchBot`, `ChatGPT-User`, `PerplexityBot`,
  `Claude-SearchBot`, `Claude-User`) decide whether the site can be cited; training bots
  (`GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`, `CCBot`) decide whether content
  trains models. Blocking a search bot removes citations; never change the policy without the
  owner's call. Scrapers that ignore limits (e.g. `Bytespider`) are blocked by default. AI bots
  get the same disallow list as everyone else: public paths only.
- `llms.txt` (a short markdown map of the key public pages) and optionally `llms-full.txt` are
  served by a route handler generated from config — prices and plans included — never a
  hand-edited static file that drifts. Add them when the overlay asks.
- **Monitoring is an owner action** listed in the plan: test the top target queries in Perplexity
  and ChatGPT, check AI Overview impressions in Search Console. When citations vanish, check
  `robots.ts` first, then whether the page structure changed.

## 7. Programmatic pages

Pages generated from data (directories, locations, integrations, comparisons, glossaries):
- **Each page has value of its own** — data or text specific to it, not a template with one word
  swapped. Variants too thin to stand alone are `noindex` and left out of the sitemap.
- Prefer data the project owns (its own or its users') over public data anyone can copy.
- Hub-and-spoke linking from a real hub page, breadcrumbs, and a sitemap per page type.
- **Before launch:** unique title and description per page, matching schema, in its sitemap, no
  conflicting `noindex`, reachable by internal links, one page per query (no cannibalization).

## 8. Privacy limits

- Never index a page that shows personal data, guest lists, tokens, private invitations or
  per-user links. Token or invite URLs are `noindex`, absent from the sitemap, and carry no
  personal data in title, description, OG image or JSON-LD.
- Never put personal data in URLs, query strings or metadata.
- A public page that a person chose to publish (an invitation they share) follows the overlay's
  rule; when the overlay is silent, treat it as `noindex`.

## Review severities

| Finding | Severity |
|---|---|
| Personal data or a private/token route indexable, in the sitemap, or in metadata | Critical |
| Staging/preview indexable; production site set to `noindex`; public content client-only | High |
| Fabricated or hidden structured data | High |
| Unverified marketing claim on a public page or in `llms.txt` | High |
| Public route without unique title/description or canonical; missing hreflang on a translated page; 200 for a missing record | Medium |
| API or search-result URLs indexable; two hosts both serving 200 | Medium |
| JSON-LD that disagrees with the page, or injected client-side; second sitemap/robots/schema helper | Medium |
| Public URL changed without a redirect; orphan page in the sitemap; thin generated pages indexable | Medium |
| Weak or over-long title/description, generic anchor text, missing OG image, heading order | Low |

## Done when

- Every new or changed public route has title, description, canonical and OG, and appears in the
  sitemap; every private route is `noindex` and absent from it.
- Production HTML (`curl` the built page) shows the content, metadata and JSON-LD without JS.
- Structured data validates; robots and sitemap respond on a production build.

## Project overlay: `<project>-seo`

Keep it short and factual:
- Public origin env var, locales and default locale
- Which route groups are public and which are `noindex`
- Page types → schema types, and where the JSON-LD helper lives
- AI-crawler policy (allow/deny per bot group) and whether `llms.txt` is wanted
- Privacy rule for user-published pages
