#!/usr/bin/env python3
"""
schema_validator.py - extract and check JSON-LD structured data from HTML.

For every JSON-LD node it reports: parse errors, missing required and
recommended properties (the skill's minimum set; Google's feature pages are
the source of truth), relative URLs, bad dates, dateModified before
datePublished, formatted prices, non-URL availability values, breadcrumb
position gaps, placeholder values, and Google features that no longer exist
(FAQ and HowTo rich results, the sitelinks search box).

It reads the HTML you give it and does not run JavaScript. To include markup
that scripts inject, save the rendered HTML from a browser first.

Usage:
  python3 schema_validator.py page.html [--json]
  python3 schema_validator.py - < page.html
  python3 schema_validator.py --demo

Network: none. Writes: nothing; output goes to stdout. Stdlib only.
"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser

RULES = {
    "Organization": (["name", "url"], ["logo", "sameAs", "contactPoint", "description"]),
    "WebSite": (["name", "url"], ["alternateName", "publisher"]),
    "Article": (["headline", "image", "datePublished", "author"], ["dateModified", "publisher", "description", "mainEntityOfPage"]),
    "Product": (["name", "image", "offers"], ["description", "sku", "brand", "aggregateRating", "review"]),
    "SoftwareApplication": (["name", "offers"], ["applicationCategory", "operatingSystem", "aggregateRating"]),
    "FAQPage": (["mainEntity"], []),
    "HowTo": (["name", "step"], ["description", "totalTime", "image"]),
    "BreadcrumbList": (["itemListElement"], []),
    "LocalBusiness": (["name", "address"], ["telephone", "openingHoursSpecification", "geo", "url", "image", "priceRange"]),
    "Event": (["name", "startDate", "location"], ["endDate", "eventStatus", "eventAttendanceMode", "image", "description", "offers", "organizer"]),
    "VideoObject": (["name", "thumbnailUrl", "uploadDate"], ["description", "duration", "contentUrl", "embedUrl", "hasPart"]),
    "Recipe": (["name", "image"], ["author", "datePublished", "description", "recipeIngredient", "recipeInstructions", "totalTime", "recipeYield"]),
}

# Common subtypes validated with their parent type's rules.
SUBTYPES = {
    **{t: "Article" for t in ("BlogPosting", "NewsArticle", "TechArticle", "ScholarlyArticle", "Report", "LiveBlogPosting")},
    **{t: "Organization" for t in ("Corporation", "NGO", "EducationalOrganization", "OnlineStore", "NewsMediaOrganization")},
    **{t: "SoftwareApplication" for t in ("WebApplication", "MobileApplication", "VideoGame")},
    **{t: "Product" for t in ("IndividualProduct", "ProductModel")},
    **{t: "Event" for t in ("BusinessEvent", "EducationEvent", "MusicEvent", "SportsEvent", "Festival",
                            "TheaterEvent", "ExhibitionEvent", "SocialEvent", "ComedyEvent")},
    **{t: "LocalBusiness" for t in (
        "Store", "Restaurant", "FoodEstablishment", "CafeOrCoffeeShop", "Bakery", "BarOrPub", "Dentist",
        "MedicalClinic", "MedicalBusiness", "Physician", "LegalService", "Attorney", "AutoRepair",
        "AutomotiveBusiness", "HomeAndConstructionBusiness", "Plumber", "Electrician", "HVACBusiness",
        "Locksmith", "RoofingContractor", "GeneralContractor", "HousePainter", "MovingCompany",
        "ProfessionalService", "FinancialService", "AccountingService", "RealEstateAgent",
        "HealthAndBeautyBusiness", "LodgingBusiness", "Hotel", "ChildCare", "TravelAgency",
        "SportsActivityLocation", "EntertainmentBusiness", "EmploymentAgency")},
}

URL_KEYS = {"url", "image", "logo", "item", "thumbnailUrl", "contentUrl", "embedUrl", "sameAs", "@id"}
DATE_KEYS = {"datePublished", "dateModified", "uploadDate", "startDate", "endDate", "priceValidUntil", "validFrom"}
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}([T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:?\d{2})?)?$")
PLACEHOLDER_WORDS = re.compile(r"\{\{|\}\}|\blorem ipsum\b|^(n/?a|tbd|todo|xxx+|placeholder)$", re.I)
PLACEHOLDER_CAPS = re.compile(r"[A-Z]{2,}_[A-Z]{2,}")   # template tokens such as PRODUCT_NAME
RETIRED = {
    "FAQPage": "Google stopped showing FAQ rich results (2026); keep only if another consumer needs it.",
    "HowTo": "Google retired HowTo rich results (2023); keep only if another consumer needs it.",
}


class JSONLDExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.blocks, self._buf, self._on = [], [], False

    def handle_starttag(self, tag, attrs):
        if tag == "script" and (dict(attrs).get("type") or "").strip().lower() == "application/ld+json":
            self._on, self._buf = True, []

    def handle_endtag(self, tag):
        if tag == "script" and self._on:
            self._on = False
            self.blocks.append("".join(self._buf).strip())

    def handle_data(self, data):
        if self._on:
            self._buf.append(data)


def node_types(node):
    t = node.get("@type")
    return [x for x in (t if isinstance(t, list) else [t]) if isinstance(x, str)]


def rule_type(types):
    for t in types:
        if t in RULES:
            return t
        if t in SUBTYPES:
            return SUBTYPES[t]
    return None


def present(value):
    return value not in (None, "", [], {})


def walk_strings(value, key=""):
    """Yield (key, string) pairs for every string inside a value."""
    if isinstance(value, str):
        yield key, value
    elif isinstance(value, list):
        for item in value:
            yield from walk_strings(item, key)
    elif isinstance(value, dict):
        for k, v in value.items():
            yield from walk_strings(v, k)


def check_node(node, block, has_context):
    types = node_types(node)
    rtype = rule_type(types)
    label = "/".join(types) or "(no @type)"
    notes = []

    if not types:
        return {"block": block, "type": label, "score": 0, "status": "no_type",
                "required_missing": [], "recommended_missing": [], "notes": ["No @type on this node."]}
    if not has_context:
        notes.append("Missing \"@context\": \"https://schema.org\" for this block.")

    if rtype:
        required, recommended = RULES[rtype]
        req_missing = [f for f in required if not present(node.get(f))]
        rec_missing = [f for f in recommended if not present(node.get(f))]
        req_score = (len(required) - len(req_missing)) / len(required) * 70 if required else 70
        rec_score = (len(recommended) - len(rec_missing)) / len(recommended) * 30 if recommended else 30
        score = int(round(req_score + rec_score))
        status = "missing_required" if req_missing else "ok"
    else:
        req_missing, rec_missing, score, status = [], [], None, "no_rules"
        notes.append("No rules for this type here; check Google's feature page and validator.schema.org.")

    for t in types:
        if t in RETIRED:
            notes.append(RETIRED[t])
    if rtype == "WebSite" and node.get("potentialAction"):
        notes.append("SearchAction no longer earns a sitelinks search box (retired 2024); it can be removed.")

    for key, text in walk_strings({k: v for k, v in node.items() if k != "@context"}):
        if key in URL_KEYS and text and not re.match(r"^(https?:)?//", text) and not text.startswith("#"):
            notes.append(f"'{key}' is not an absolute URL: {text[:60]}")
        if key in DATE_KEYS and text and not ISO_DATE.match(text.strip()):
            notes.append(f"'{key}' is not ISO 8601 (YYYY-MM-DD or full timestamp): {text[:40]}")
        if PLACEHOLDER_WORDS.search(text) or PLACEHOLDER_CAPS.search(text):
            notes.append(f"Possible placeholder in '{key}': {text[:60]}")
        if key in ("url", "item", "@id") and re.search(r"//(www\.)?example\.(com|org|net)\b", text):
            notes.append(f"Example-domain URL left in '{key}': {text[:60]}")

    pub, mod = node.get("datePublished"), node.get("dateModified")
    if isinstance(pub, str) and isinstance(mod, str) and ISO_DATE.match(pub) and ISO_DATE.match(mod) and mod[:10] < pub[:10]:
        notes.append("dateModified is earlier than datePublished.")

    offers = node.get("offers")
    for offer in offers if isinstance(offers, list) else [offers] if isinstance(offers, dict) else []:
        if not isinstance(offer, dict):
            continue
        price = offer.get("price")
        if isinstance(price, str) and re.search(r"[^\d.,\s]", price):
            notes.append(f"offers.price should be a plain number (49.99) with priceCurrency, not '{price}'.")
        if present(price) and not present(offer.get("priceCurrency")):
            notes.append("offers has a price but no priceCurrency (ISO 4217, e.g. USD).")
        avail = offer.get("availability")
        if isinstance(avail, str) and avail and not re.match(r"^https?://schema\.org/", avail):
            notes.append(f"offers.availability should be a schema.org URL (https://schema.org/InStock), not '{avail}'.")

    if rtype == "BreadcrumbList" and isinstance(node.get("itemListElement"), list):
        positions = [i.get("position") for i in node["itemListElement"] if isinstance(i, dict)]
        try:
            ints = [int(p) for p in positions]
        except (TypeError, ValueError):
            ints = []
        if ints != list(range(1, len(positions) + 1)):
            notes.append("Breadcrumb positions must be 1, 2, 3... in order.")

    if rtype == "FAQPage" and isinstance(node.get("mainEntity"), list):
        for i, q in enumerate(node["mainEntity"], 1):
            answer = q.get("acceptedAnswer") if isinstance(q, dict) else None
            if not (isinstance(answer, dict) and present(answer.get("text"))):
                notes.append(f"Question {i} has no acceptedAnswer.text.")

    return {"block": block, "type": label, "rules": rtype, "score": score, "status": status,
            "required_missing": req_missing, "recommended_missing": rec_missing, "notes": notes}


def validate_block(raw, block):
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [{"block": block, "type": "PARSE_ERROR", "score": 0, "status": "parse_error",
                 "required_missing": [], "recommended_missing": [],
                 "notes": [f"Invalid JSON ({exc}). Fix the syntax first (trailing commas and comments are not allowed)."]}]
    results = []
    for top in data if isinstance(data, list) else [data]:
        if not isinstance(top, dict):
            continue
        has_context = "@context" in top
        nodes = top.get("@graph") if isinstance(top.get("@graph"), list) else [top]
        for node in nodes:
            if isinstance(node, dict):
                results.append(check_node(node, block, has_context or "@context" in node))
    return results


def grade(score):
    if score is None:
        return "not scored"
    return "excellent" if score >= 90 else "good" if score >= 70 else "needs work" if score >= 50 else "poor"


def print_report(blocks, results):
    print("=" * 64)
    print(f"  JSON-LD CHECK   {blocks} block(s), {len(results)} node(s)")
    print("=" * 64)
    if not results:
        print("  No JSON-LD found. If the page injects markup with JavaScript,")
        print("  save the rendered HTML from a browser and run this again.")
        return
    for r in results:
        score = "--" if r["score"] is None else f"{r['score']}/100"
        print(f"\n  Block {r['block']} - {r['type']}   {score} ({grade(r['score'])})")
        if r["required_missing"]:
            print(f"    Missing required: {', '.join(r['required_missing'])}")
        if r["recommended_missing"]:
            print(f"    Missing recommended: {', '.join(r['recommended_missing'])}")
        for note in r["notes"]:
            print(f"    - {note}")
    print("\n  Next: Rich Results Test for supported Google features, validator.schema.org")
    print("  for vocabulary, then Search Console enhancement reports after deploy.")


DEMO_HTML = """<html><head>
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "BlogPosting",
 "headline": "How to Write an Invoice", "image": "/img/invoice.jpg",
 "datePublished": "2026-03-10", "dateModified": "2026-03-01",
 "author": {"@type": "Person", "name": "Jane Doe"}}
</script>
<script type="application/ld+json">
[{"@context": "https://schema.org", "@type": "Product", "name": "Invoice Pro",
  "image": "https://example.org/img/pro.png",
  "offers": {"@type": "Offer", "price": "$29.00", "availability": "InStock"}},
 {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.org/"},
  {"@type": "ListItem", "position": 3, "name": "Invoice Pro", "item": "https://example.org/pro"}]}]
</script>
<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
 {"@type": "Question", "name": "Is there a free plan?", "acceptedAnswer": {"@type": "Answer", "text": ""}}]}
</script>
</head><body><h1>How to Write an Invoice</h1></body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Extract and check JSON-LD structured data from an HTML file.")
    ap.add_argument("file", nargs="?", help="HTML file to check ('-' reads stdin)")
    ap.add_argument("--demo", action="store_true", help="Run on built-in sample HTML")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of the text report")
    args = ap.parse_args()

    if args.demo:
        html = DEMO_HTML
    elif args.file == "-":
        html = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, encoding="utf-8", errors="replace") as fh:
                html = fh.read()
        except OSError as exc:
            sys.exit(f"error: {exc}")
    else:
        ap.print_help()
        return

    extractor = JSONLDExtractor()
    extractor.feed(html)
    extractor.close()
    results = []
    for i, raw in enumerate(extractor.blocks, 1):
        results.extend(validate_block(raw, i))

    if args.json:
        scored = [r["score"] for r in results if r["score"] is not None]
        print(json.dumps({"blocks_found": len(extractor.blocks), "nodes": len(results),
                          "average_score": round(sum(scored) / len(scored)) if scored else None,
                          "results": results}, indent=2))
    else:
        print_report(len(extractor.blocks), results)


if __name__ == "__main__":
    main()
