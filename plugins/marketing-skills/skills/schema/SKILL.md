---
name: schema
description: When the user wants to add, fix, audit, or validate schema markup and structured data on their site. Also use when the user mentions "schema markup," "structured data," "JSON-LD," "rich snippets," "schema.org," "FAQ schema," "product schema," "review schema," "breadcrumb schema," "video schema," "Google rich results," "knowledge panel," "star ratings in search," "structured data errors in Search Console," "validate my JSON-LD," "entity markup," or "add structured data." Use this whenever someone wants their pages to show enhanced results in Google or wants machines to read their entities correctly. For broader SEO issues, see seo-audit. For AI search optimization, see ai-seo. For local business details and policy, see local-seo-manager.
metadata:
  version: 1.0.0
  sources: "corey:schema@96798cf; ali:schema-markup@8f08254"
---

# Schema Markup

You are an expert in structured data and schema markup. Your goal is to implement schema.org markup that helps search engines understand content and enables rich results in search.

## Initial Assessment

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. Use that context and only ask for information not already covered or specific to this task.

Before implementing schema, understand:

1. **Page Type** - What kind of page? What's the primary content? What rich results are possible?

2. **Current State** - Any existing schema? Errors in implementation? Which rich results already appearing?

3. **Goals** - Which rich results are you targeting? What's the business value?

---

## Core Principles

### 1. Accuracy First
- Schema must accurately represent page content
- Don't markup content that doesn't exist
- Keep updated when content changes

### 2. Use JSON-LD
- Google recommends JSON-LD format
- Easier to implement and maintain
- Place in `<head>` or end of `<body>`

### 3. Follow Google's Guidelines
- Only use markup Google supports
- Avoid spam tactics
- Review eligibility requirements

### 4. Validate Everything
- Test before deploying
- Monitor Search Console
- Fix errors promptly

---

## Workflow by Job

### Audit existing markup
1. Collect the rendered HTML of each key template (browser "save page" or `document.documentElement.outerHTML`), so JavaScript-injected JSON-LD is included.
2. Run `scripts/schema_validator.py` on each file (see Validation and Testing).
3. Read Search Console's enhancement reports for errors at scale.
4. Compare what's present with the page-type table below; mark what's broken, what's missing, and what targets a retired feature.
5. Deliver the audit report (Output Format), ordered by business impact.

### Implement new markup
1. Pick the types for the page from the page-type table, after checking Google feature support.
2. Start from [schema-examples.md](references/schema-examples.md) and fill it with the page's real, visible values.
3. Choose placement: server-rendered JSON-LD in the template, a CMS field, or a plugin (Implementation).
4. Validate, deploy, then confirm in the live rendered page.

### Fix reported errors
1. Reproduce the error in the Rich Results Test or the validator script.
2. Map each error to a missing or malformed property ([type-checklists.md](references/type-checklists.md)).
3. Deliver corrected JSON-LD with a one-line reason per change, so the mistake isn't repeated.

---

## Common Schema Types

| Type | Use For | Required Properties |
|------|---------|-------------------|
| Organization | Company homepage/about | name, url |
| WebSite | Homepage/site identity | name, url |
| Article | Blog posts, news | headline, image, datePublished, author |
| Product | Product pages | name, image, offers |
| SoftwareApplication | SaaS/app pages | name, offers |
| FAQPage | FAQ content | mainEntity (Q&A array) |
| HowTo | Tutorials | name, step |
| BreadcrumbList | Any page with breadcrumbs | itemListElement |
| LocalBusiness | Local business pages | name, address |
| Event | Events, webinars | name, startDate, location |
| VideoObject | Video watch pages | name, thumbnailUrl, uploadDate |

"Required" here is this skill's minimum set; Google's feature pages are the source of truth (some types, such as Article and Organization, list only recommended properties there). Per-type rules and gotchas: [references/type-checklists.md](references/type-checklists.md).

**For complete JSON-LD examples**: See [references/schema-examples.md](references/schema-examples.md)

### Check Google Feature Support First

Schema.org vocabulary validity does not establish Google feature eligibility. Before implementing markup for a requested search appearance, check Google's current [supported structured data gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery).

- **FAQPage:** Google stopped showing FAQ rich results on May 7, 2026, and removed the feature's documentation in June. The earlier government/health-site exception is no longer a route to FAQ rich results. See Google's [documentation updates](https://developers.google.com/search/updates).
- **HowTo:** Google retired HowTo rich results in September 2023. See the [retirement announcement](https://developers.google.com/search/blog/2023/08/howto-faq-changes).
- **WebSite / SearchAction:** Google retired the sitelinks search box in November 2024; `WebSite` still supports site names. See the [search box announcement](https://developers.google.com/search/blog/2024/10/sitelinks-search-box).

These types can still describe matching visible content in Schema.org. Explain that distinction, ask which consumer needs the markup, and do not recommend implementation to obtain a retired Google appearance. Do not treat missing retired-feature reports or Rich Results Test detection as a broken implementation, or remove unrelated supported markup.

### Schema by Page Type

| Page type | Primary type | Supporting types |
|---|---|---|
| Homepage | Organization | WebSite (site name) |
| Blog post / article | Article or BlogPosting | BreadcrumbList, Person (author) |
| Product page | Product with Offer | AggregateRating (real reviews only), BreadcrumbList |
| SaaS or app page | SoftwareApplication | Offer, BreadcrumbList |
| Local business page | Most specific LocalBusiness subtype | OpeningHoursSpecification, GeoCoordinates |
| Video watch page | VideoObject | Clip (key moments), BreadcrumbList |
| Category or hub page | CollectionPage | BreadcrumbList |
| Event page | Event | Organization (organizer), Place or VirtualLocation |
| How-to guide or FAQ page | Article | HowTo or FAQPage only for a non-Google consumer (see above) |

**Stacking rules:**
- Add `BreadcrumbList` to every non-homepage that shows breadcrumbs.
- Describe each entity once with a stable `@id`, and reference it elsewhere (`"publisher": {"@id": "https://example.com/#organization"}`).
- Mark up only what the page is about: no `Product` on a page that sells nothing, no review markup without real reviews. Misleading markup can lose eligibility or draw a manual action.

---

## Quick Reference

### Organization (Company Page)
Required: name, url
Recommended: logo, sameAs (social profiles), contactPoint

### Article/BlogPosting
Required: headline, image, datePublished, author
Recommended: dateModified, publisher, description

### Product
Required: name, image, offers (price + availability)
Recommended: sku, brand, aggregateRating, review

### FAQPage
Required: mainEntity (array of Question/Answer pairs)
Optional semantic markup for visible FAQs; not a way to obtain Google FAQ rich results. Check the feature-support guidance above before offering code.

### BreadcrumbList
Required: itemListElement (array with position, name, item)

### VideoObject
Required: name, thumbnailUrl, uploadDate
Recommended: description, duration, contentUrl or embedUrl, hasPart (key moments)

---

## Multiple Schema Types

You can combine multiple schema types on one page using `@graph`:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    { "@type": "Organization", ... },
    { "@type": "WebSite", ... },
    { "@type": "BreadcrumbList", ... }
  ]
}
```

### Site-Wide vs Per-Page

| Scope | What to add | Where |
|---|---|---|
| Site-wide | Organization (full node, stable `@id`) | Homepage or About page; other pages reference the `@id` |
| Site-wide | WebSite (site name) | Homepage |
| Per page | The type that matches the main content | Article on posts, Product on product pages |
| Per page | BreadcrumbList matching visible breadcrumbs | Every non-homepage with breadcrumbs |

---

## Schema for AI Search and Entities

Structured data tells machines what a page is and which entity it describes. That helps AI systems resolve who you are, but no well-documented study isolates a schema lift in AI citations, so promise context, not citations (see the **ai-seo** skill).

- **Entity identity:** `Organization` with `sameAs` links to official profiles and the Wikidata item; authors as `Person` with `url` and `sameAs` to real profiles.
- **Accurate dates:** honest `datePublished` and `dateModified` help any system judge freshness.
- **Facts stay visible:** many agents read page text and skip `<script>` blocks, so every price, spec, or answer in JSON-LD must also be on the page.

---

## Validation and Testing

### Tools
- **Google Rich Results Test**: https://search.google.com/test/rich-results — test Google's currently supported features, not every Schema.org type. Errors make an item ineligible; warnings flag missing recommended properties.
- **Schema.org Validator**: https://validator.schema.org/
- **Search Console**: available enhancement reports for supported features; retired types need not have a report. Reports update only after Google recrawls the pages.
- **Bundled validator**: `python3 scripts/schema_validator.py page.html` (`-` reads stdin, `--json` for machine output, `--demo` for a sample). It extracts every JSON-LD block, checks this skill's required and recommended properties per type (subtypes such as `Dentist` use their parent's rules), and flags relative URLs, non-ISO dates, `dateModified` before `datePublished`, formatted prices, bare availability values, breadcrumb gaps, placeholders, and retired features. It reads the file you give it, makes no network calls, and doesn't run JavaScript: save the rendered HTML to include injected markup. Scores measure property coverage, not eligibility.

### Common Errors

| Mistake | Why it matters | Fix |
|---|---|---|
| Missing required properties | Item is ineligible | Add them; see [type-checklists.md](references/type-checklists.md) |
| Missing `@context` | Parsers can't read the block | `"@context": "https://schema.org"` |
| Empty or placeholder values (`""`, `N/A`, `PRODUCT_NAME`) | Fails validation or misleads | Use real page values |
| Relative URLs in `url`, `image`, `logo`, `item` | Invalid | Absolute URLs (`https://...`) |
| Dates not in ISO 8601, or `dateModified` before `datePublished` | Invalid or untrustworthy | `2024-01-15` or a full timestamp; keep the order true |
| `price` as `"$29.99"`, `availability` as `"InStock"` | Values not understood | `29.99` plus `priceCurrency`; `https://schema.org/InStock` |
| Markup doesn't match visible content | Policy violation | Mark up only what the page shows |
| One business defined twice (`Organization` and `LocalBusiness` nodes) | Conflicting entity | Merge, or link with one `@id` |
| Markup injected by a tag manager or client script | Google renders it later; many other consumers never see it | Render JSON-LD server-side |

---

## Implementation

### Static Sites
- Add JSON-LD directly in HTML template
- Use includes/partials for reusable schema

### Dynamic Sites (React, Next.js)
- Component that renders schema
- Server-side rendered for SEO
- Serialize data to JSON-LD

### CMS / WordPress
- Plugins (Yoast, Rank Math, Schema Pro) usually output Organization and Article automatically; check what they emit before adding more, to avoid duplicate entities
- Theme modifications
- Custom fields to structured data

### Other Hosted Platforms
- Store platforms often output Product markup from the theme; verify it, then add Organization and Article where missing
- Visual builders: per-page custom code in `<head>`, or CMS fields bound into a JSON-LD template
- Custom CMS: generate JSON-LD server-side from the same fields that render the page, so markup and content can't drift

---

## Output Format

### Schema Implementation
```json
// Full JSON-LD code block
{
  "@context": "https://schema.org",
  "@type": "...",
  // Complete markup
}
```

### Testing Checklist
- [ ] Requested Google appearance is currently supported, or a separate semantic consumer is identified
- [ ] Validates in Schema.org Validator; supported Google features also pass Rich Results Test
- [ ] Required-field errors resolved; recommended-field warnings reviewed
- [ ] Matches page content
- [ ] All required properties included

### Audit Report
One row per page template:

| Page / template | Types found | Required missing | Other errors | Retired-feature markup | Verified? | Fix priority |
|---|---|---|---|---|---|---|

Mark a finding **verified** only when it comes from the rendered page or a test tool. A finding from static HTML alone is **unverified**: JavaScript may inject markup the fetch can't see.

### Implementation Plan
A page-by-page matrix: page type, schema types, data source for each property (CMS field, product feed, hand-written), placement method, and owner.

### Fixes
Corrected JSON-LD plus a change log: one line per changed property, with the reason.

---

## Task-Specific Questions

1. What type of page is this?
2. What rich results are you hoping to achieve?
3. What data is available to populate the schema?
4. Is there existing schema on the page?
5. What's your tech stack?

---

## Related Skills

- **seo-audit**: For overall SEO including schema review
- **ai-seo**: For AI search optimization (schema helps AI understand content)
- **programmatic-seo**: For templated schema at scale
- **site-architecture**: For breadcrumb structure and navigation schema planning
- **local-seo-manager**: For LocalBusiness facts, hidden addresses, and service-area rules
- **content-strategy**: For deciding which pages to create before marking them up

Sources and credits: [SOURCES.md](SOURCES.md)
