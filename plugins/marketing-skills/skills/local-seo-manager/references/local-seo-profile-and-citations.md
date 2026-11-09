# Profiles and Citations

Use this for profile eligibility, field changes, and name/address/phone cleanup. Verify facts with the owner and the current [business representation guidelines](https://support.google.com/business/answer/3038177).

## Model the Real Business

| Business | Profile approach | Common mistake |
|---|---|---|
| Staffed storefront receiving customers | Actual location, public address and customer-facing hours | Keyword-stuffed name or wrong entrance |
| Service-area business visiting customers | Actual base with address hidden when customers are not served there | Profiles for every city or exposing a home address |
| Hybrid | Real customer-facing location plus actual coverage | Claiming unstaffed locations |
| Multiple locations | Verify each location and its staffing/eligibility separately | Assuming a location page or rented mailbox establishes eligibility |
| Online only | Use organic/AI search strategy appropriate to the business | Creating a fictitious local presence |

Exceptions for practitioners, departments, co-located businesses, and special business types require their specific rules. Do not merge two legitimately distinct entities just because they share an address. An actual relocation needs an update to the existing business identity rather than an unexplained new duplicate.

## Field-Level Review

- **Name:** match real-world branding. Put services and coverage in their proper fields rather than adding search keywords to the name.
- **Categories:** use the most specific accurate primary category and only justified additional categories. Check the current category options for that market.
- **Services:** describe services actually offered; distinguish availability, territory, and appointment requirements.
- **Description:** write factual business/service information. Keep promotions and links out of this field.
- **Hours and contact:** confirm regular/special hours, correct phone routing, and a location-specific working website/booking link.
- **Photos:** propose real exterior/entrance, interior, team, or service imagery appropriate to the business. Confirm permission before publishing identifiable customers.
- **Posts:** use them for relevant current updates, offers, or events where available; do not invent a posting-frequency ranking benefit.
- **Q&A:** Google [discontinued its Q&A API on November 3, 2025](https://developers.google.com/my-business/content/qanda/change-log). Do not prescribe API seeding or a universal editable Q&A section. Verify current interface availability; answer common customer questions in website content and accurate profile fields when a profile feature is unavailable.

For service areas, confirm actual coverage using [Google's service-area guidance](https://support.google.com/business/answer/9157481). Listing another town does not create a new location or remove searcher distance as a ranking factor.

## Citation Cleanup Table

Use one row per observed listing:

| Location/entity | Listing URL | Observed public facts | Verified source of truth | Correction / duplicate action | Access/status | Verification date |
|---|---|---|---|---|---|---|

Compare meaning, not merely punctuation: an abbreviation need not be an identity conflict. A wrong phone, old address, mismatched business, or duplicate that diverts customers deserves priority. Preserve location distinctions and legitimate branch phone numbers.

For a home-based service business, use supported hidden-address listings or skip platforms that require publishing private information. Maintain the private operating address separately from public citation data.

### Common NAP differences

Sort each difference into identity conflicts and formatting before fixing anything:

| Difference | Usually | Action |
|---|---|---|
| Phone written differently (`(020) 7946 0000` vs `+44 20 7946 0000`) | Formatting | None, if the digits match |
| Old phone number still live on a legacy listing | Conflict | Correct it first: it sends customers to a dead line |
| Legal suffix added or dropped ("Ltd," "LLC") | Formatting | Optional tidy-up |
| Keywords or a city added to the name | Conflict | Restore the real-world name |
| Street-type abbreviation ("St" vs "Street") | Formatting | None |
| Missing unit or suite number | Conflict for visitors | Add it where customers need it to arrive |
| Old address after a move | Conflict | Update the existing listing; don't open a new one |

`scripts/nap_checker.py` sorts collected listings this way; see SKILL.md.

### Which listings to fix first

1. The maps platforms customers in that market actually use.
2. Major general directories and review sites that rank for the business's name.
3. Industry and local listings (trade bodies, chambers, booking platforms) that send real enquiries.

The right platforms differ by country and industry: check which listings appear when searching for the business's name and its category in the target area, rather than working from a fixed list.

Select listings for customer relevance and accurate discovery. Bulk low-quality links, lifetime domain metrics, or a directory count alone do not demonstrate improved local outcomes. DIY corrections are a valid path; paid listing management is optional when its coverage, control, cost, and verification process fit the business.
