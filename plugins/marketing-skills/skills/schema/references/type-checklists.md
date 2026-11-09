# Schema Type Checklists

Per-type property checklists and the mistakes that cost eligibility. Use this when writing or auditing markup for a specific type. Full JSON-LD examples are in [schema-examples.md](schema-examples.md).

"Minimum" below is this skill's working set. Google's feature documentation is the source of truth for eligibility, and some types (Article, Organization) list only recommended properties there. Check Google's [search gallery](https://developers.google.com/search/docs/appearance/structured-data/search-gallery) before promising a result.

## Contents
- Article / BlogPosting / NewsArticle
- Product, Offer, and AggregateRating
- Organization
- LocalBusiness
- BreadcrumbList
- VideoObject
- WebSite
- FAQPage and HowTo (semantic only)

---

## Article / BlogPosting / NewsArticle

**Shows as:** article details in Search, Top Stories, and Discover (no guarantee).
**Minimum:** `headline`, `image`, `datePublished`, `author`.
**Recommended:** `dateModified`, `publisher` (Organization with `logo`), `description`, `mainEntityOfPage`.

- `headline` should match the visible title or H1.
- `image`: absolute URLs; supply large images (Google asks for high resolution, ideally in 16:9, 4:3, and 1:1 crops).
- `author`: a `Person` or `Organization` with only the name in `name` (no job titles); add `url` to an author page. For several authors, use an array of objects.
- Keep `dateModified` honest: change it when the content changes, never on a schedule.
- Use `NewsArticle` for news and `BlogPosting` for blog posts; both are Article subtypes.

## Product, Offer, and AggregateRating

**Shows as:** price, availability, and review stars on product results; merchant listings.
**Minimum:** `name`, `image`, `offers`.
**Recommended:** `description`, `sku`, `brand`, `aggregateRating`, `review`.

**Offer:**
- `price` as a number (`49.99`), not `"$49.99"`; currency goes in `priceCurrency` (ISO 4217, such as `USD` or `EUR`).
- `availability` as a schema.org URL: `https://schema.org/InStock` (values in [schema-examples.md](schema-examples.md)).
- `priceValidUntil` when a price expires.
- The price in markup must match the price on the page.

**AggregateRating:** `ratingValue` plus `ratingCount` or `reviewCount`; add `bestRating` when the scale isn't 1–5.
- Ratings must come from real reviews collected for that product. Never fabricate them, and don't copy ratings from other sites into your markup.
- Self-serving review markup on `LocalBusiness` or `Organization` pages doesn't earn stars.

## Organization

**Shows as:** logo and knowledge panel details (not guaranteed).
**Minimum:** `name`, `url`. **Recommended:** `logo`, `sameAs`, `contactPoint`, `description`, `address`.

- Put the full node on the homepage or About page, give it a stable `@id` (`https://example.com/#organization`), and reference that `@id` from other pages (`publisher`, `author`).
- `sameAs` ties the entity together: official social profiles, Crunchbase, Wikipedia, and the Wikidata item (`https://www.wikidata.org/wiki/Q...`) when one exists.
- Describe the company once. Two different nodes for the same business (say `Organization` and `LocalBusiness`) should be merged, or linked by `@id`.

## LocalBusiness

**Shows as:** business details in Search and Maps surfaces.
**Minimum:** `name`, `address`. **Recommended:** `telephone`, `openingHoursSpecification`, `geo`, `url`, `image`, `priceRange`.

- Use the most specific subtype (`Dentist`, `Plumber`, `Restaurant`) and one node per real location, each with its own `@id` and URL.
- `address` as a `PostalAddress` matching the public business profile; `telephone` with the country code.
- Hours in 24-hour `HH:MM`. Open all day: `00:00` to `23:59`. Closed all day: `opens` and `closes` both `00:00`.
- Don't publish a hidden home address, and don't mark service cities as branches. Local rules are in the **local-seo-manager** skill.

## BreadcrumbList

**Shows as:** a breadcrumb path instead of the raw URL.
**Minimum:** `itemListElement`, each `ListItem` with `position`, `name`, and `item` (absolute URL; the last item may omit `item`).

- Positions run 1, 2, 3 with no gaps.
- The markup mirrors the visible breadcrumb trail on the page.

## VideoObject

**Shows as:** video results and key moments.
**Minimum:** `name`, `thumbnailUrl`, `uploadDate`.
**Recommended:** `description`, `duration` (ISO 8601, `PT12M30S`), `contentUrl` or `embedUrl`, `hasPart` (key moments).

- Video features need a page where the video is the main content (a watch page).
- `thumbnailUrl` must resolve to a real image Google can fetch.
- Give `contentUrl` or `embedUrl` so Google can fetch the video itself.
- Key moments: one `Clip` per chapter with `name`, `startOffset`, `endOffset` (seconds), and a `url` that starts playback at that point.
- Videos behind a login or paywall aren't eligible for video features.

## WebSite

**Shows as:** the site name in results.
**Minimum:** `name`, `url` on the homepage; add `alternateName` for an acronym or short name.

- Google retired the sitelinks search box in November 2024; `SearchAction` no longer earns one.

## FAQPage and HowTo (semantic only)

Google no longer shows FAQ or HowTo rich results (see the feature-support section in SKILL.md). The vocabulary is still valid for other consumers:

- `FAQPage`: `mainEntity` array of `Question` items, each with `acceptedAnswer.text`. Every question and answer must be visible on the page.
- `HowTo`: `name` and `step` (`HowToStep` items with `text`). Steps must be visible on the page; use `Recipe` for recipes.
