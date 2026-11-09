# URL Design

URL notes by site type, redirect mapping, canonical tags, and status codes. The general URL rules live in SKILL.md (URL Structure); full page hierarchies and URL maps per site type are in [site-type-templates.md](site-type-templates.md); the migration sequence is in [platforms-and-migration.md](platforms-and-migration.md).

## Contents
- Notes by site type
- Redirect mapping
- Canonicalization
- Status codes

---

## Notes by Site Type

### SaaS / B2B software
- `/features/{name}` pages should be rankable landing pages, not only navigation targets.
- `/solutions/{use-case}` and `/solutions/{industry}` catch bottom-funnel searches ("email tool for sales teams").
- `/integrations/{tool}` pages carry high intent: give each one a real page.
- Pick one home for articles (`/blog/`, `/resources/`, or `/learn/`) and keep it.
- Pick one path for release notes (`/changelog` or `/releases`) and keep it.

| Do | Don't |
|---|---|
| `/features/email-automation` | `/product/features/email-automation/detail` (too deep) |
| `/solutions/sales-teams` | `/solutions-for-sales-teams` (flattens the section into the slug) |
| `/integrations/crm-name` | `/connect-with/crm-name-integration` (redundant words) |

### Blog / content site
- Date-based URLs (`/2024/03/15/slug`) look stale and get long. Leave dates out unless the site is a news publisher.
- Tag pages create thin, near-duplicate pages at scale: `noindex` them, or give each one real content.
- Under a few hundred posts, a flat `/blog/{slug}` is fine. Larger sites benefit from category folders (`/{category}/{slug}`) when each category is a real hub page.
- Build author pages as real pages with bio and credentials: they support E-E-A-T (see the **seo-audit** skill).

### E-commerce
- Product variants (size, color) are the biggest duplicate-content risk. Canonical each variant URL to the base product, unless a variant has its own search demand and its own content.
- Filter and sort URLs (`?sort=price-asc&brand=x`) should canonical to the base category page. Keep crawlers out of endless filter combinations with `robots.txt` rules, while leaving the filtered pages you want indexed as clean, linked URLs.
- Category pages need real content (an intro, buying guidance, FAQs) to rank, not only a product grid.
- Discontinued products: 301 to the closest replacement or the parent category; return 410 only when nothing relevant remains.

| Do | Don't |
|---|---|
| `/products/runner-270-black` | `/products?id=89472&color=black&size=10` |
| `/collections/mens-shoes` | `/products/shoes/men/athletic/running/all-styles` |

### Local business / service area
Single location:
```
/services/{service}            e.g. /services/plumbing-repair
/areas-served/{area}           optional, only with real local content per area
```

Multiple locations:
```
/locations/{city}              e.g. /locations/springfield
/locations/{city}/{service}    only where that location really offers the service
/services/{service}            general service pages
```

- Every location or area page needs locally relevant content (staff, address, local jobs, reviews), not the same text with the city swapped.
- Use subfolders (`/locations/{city}`) rather than a subdomain per city, unless locations run as independent businesses.
- Profiles, citations, and location-page content: see the **local-seo-manager** skill.

---

## Redirect Mapping

Changing URLs needs a 301 map: every old URL to its closest new URL.

1. Export the indexed URLs (Search Console page indexing report, plus a crawl of the current site).
2. Export the URLs with external links (Search Console's Links report or a backlink tool).
3. Map old to new for every URL, one to one. Never send everything to the homepage.
4. Implement 301s on the server or CDN, not with JavaScript or meta refresh.
5. Update internal links to point at the new URLs directly.
6. Watch Search Console for 404s after the change.

**Priority order when time is short:**
1. Pages with external links
2. Pages with organic traffic or conversions
3. Everything else (still redirect, at lower urgency)

**Avoid:**
- Redirect chains (`/old` → `/temp` → `/new`): point each old URL straight at the final one.
- A 302 for a permanent move: use 301 (or 308).
- Old URLs left live as duplicates without a redirect or canonical.

---

## Canonicalization

When the same content is reachable at several URLs, name the preferred one:

```html
<link rel="canonical" href="https://example.com/the-canonical-url" />
```

| Situation | What to do |
|---|---|
| `http://` and `https://` | 301 to `https://`; canonical to `https://` |
| `www` and non-www | Pick one; 301 the other |
| `/page` and `/page/` | Pick one; 301 the other |
| Filtered or sorted listings | Canonical to the base listing |
| Paginated series (`?page=2`) | Each page canonical to itself, not to page 1; link the pages to each other with normal links |
| Printer-friendly or tracking-parameter copies | Canonical to the main URL |
| Content syndicated to other sites | Ask the partner for a canonical to the original, or `noindex` on their copy |

A canonical is a hint, not a command. Internal links, sitemaps, and redirects that point at the same URL make it stick.

---

## Status Codes

| Code | Meaning | Use |
|---|---|---|
| 200 | OK | Normal page |
| 301 / 308 | Moved permanently | Permanent URL change; signals move to the new URL |
| 302 / 307 | Moved temporarily | Short-term moves only; a long-lived 302 may be treated as permanent, but don't rely on it |
| 404 | Not found | Page doesn't exist; serve a helpful 404 page |
| 410 | Gone | Page removed on purpose; can drop out of the index slightly faster than a 404 |
| 503 | Service unavailable | Planned maintenance; add `Retry-After` and keep it short |

---

*Site-type notes, the redirect priority order, canonical situations, and the status-code table are adapted from the ali library's `site-architecture` skill (url-design-guide.md, MIT), with outdated advice corrected (pagination canonicals, 302 handling, the retired Search Console URL-parameter tool).*
