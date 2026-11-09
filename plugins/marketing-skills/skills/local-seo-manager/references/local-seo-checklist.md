# Local SEO Audit Checklist

A pass/fail list for a full local audit. Mark each item pass, fail, or unknown, and record the evidence. An unknown item is a question for the owner, not a failure. Policy details and the reasons behind each rule are in [local-seo-profile-and-citations.md](local-seo-profile-and-citations.md) and [local-seo-pages-and-measurement.md](local-seo-pages-and-measurement.md).

## Contents
- Business model and eligibility
- Profile fields
- Citations and NAP
- Reviews
- Website and location pages
- Technical basics
- Measurement
- Common quick wins

---

## 1. Business Model and Eligibility
- [ ] Business type confirmed: storefront, service-area, hybrid, multi-location, or online only
- [ ] One profile per real, eligible location; no profiles for cities that are only served
- [ ] Service-area business: address hidden where customers aren't served there
- [ ] No duplicate, unverified, or suspended profiles (or a plan to resolve each)
- [ ] A recent move was handled as an update to the existing profile

## 2. Profile Fields
- [ ] Name matches real-world branding, with no added keywords or cities
- [ ] Primary category is the most specific accurate one; additional categories each justified
- [ ] Services listed are the ones actually offered, with availability conditions
- [ ] Description is factual: services, coverage, what makes the business distinct; no links or promotions
- [ ] Regular and special hours confirmed with the owner
- [ ] Phone routes to the business; website link goes to the matching location page, with consistent campaign tags
- [ ] Real photos of the exterior or entrance, interior, team, or work; permission for any identifiable customer
- [ ] Posts, products, and other features used only where they carry current, true information
- [ ] No reliance on Q&A seeding (the Q&A API was discontinued; see the profile reference)

## 3. Citations and NAP
- [ ] Canonical record written down: name, public address or "hidden," phone, hours, website, profile ID
- [ ] Listings collected from the platforms customers use in that market (see "Which listings to fix first")
- [ ] `scripts/nap_checker.py` run on the collected listings; every FIX resolved or explained
- [ ] Old phone numbers and old addresses corrected first
- [ ] True duplicates merged or removed through the platform's process
- [ ] No listing exposes a private home address

## 4. Reviews
- [ ] A neutral request process exists, sent to all eligible customers, not only happy ones
- [ ] Request links point to the correct location
- [ ] No incentives, required wording, or rating-directed asks
- [ ] Replies are specific, courteous, and disclose no customer details
- [ ] Policy violations reported through the platform; genuine criticism answered, not "removed"
- [ ] Recurring feedback themes fed back into operations

## 5. Website and Location Pages
- [ ] Each real location has its own page with accurate contact details, hours, and directions
- [ ] Service-area pages state that they describe coverage and imply no office
- [ ] Each local page carries information specific to its place (no city-name swaps)
- [ ] Location pages are linked from a location index and from the relevant service pages
- [ ] Contact details on the site match the canonical record; phone numbers are click-to-call links
- [ ] Titles and meta descriptions are unique per page

## 6. Technical Basics
- [ ] Location and service pages are indexable and in the XML sitemap (see the **seo-audit** skill)
- [ ] LocalBusiness markup uses the most specific accurate subtype and matches visible facts (see the **schema** skill)
- [ ] No hidden residential address in markup; no profile rating copied into markup
- [ ] Markup checked on the rendered page, not a stripped text fetch
- [ ] Mobile performance checked with field data where available
- [ ] Changed URLs redirect with 301s

## 7. Measurement
- [ ] Baseline by location and period: qualified calls, bookings, and leads
- [ ] Profile interactions exported where available
- [ ] Search Console filtered to local pages and queries
- [ ] Visibility checks use the same queries, search locations, and method each time

---

## Common Quick Wins

Usually high value for little effort, once the evidence supports them:

1. Correct a wrong phone number or old address on the profile and the most-used listings.
2. Reply to unanswered reviews, specifically and courteously.
3. Fix the profile's website link so it lands on the matching location page.
4. Replace a keyword-stuffed business name with the real-world name.
5. Add real photos of the location, team, or work.
6. Add or fix LocalBusiness markup with accurate, visible facts.

---

*Adapted from the ali library's `local-seo-manager` checklist by Stan Varashilov (Steffonet), MIT. Removed: geotagged photos, Q&A seeding, legal-name and toll-free-number rules, review-count and posting-frequency targets, FAQ rich-result items, word-count targets, and the 80-point score.*
