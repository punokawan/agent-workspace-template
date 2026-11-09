#!/usr/bin/env python3
"""
nap_checker.py - compare a business's verified name, address, phone, and website
with the listings you collected by hand or exported from a listing tool.

You supply two JSON files:

  canonical.json  the verified public facts (source of truth)
    {
      "name": "Harbor Cycle",
      "phone": "020 7946 0000",
      "country_code": "44",            optional: strips +44 / 0044 and the trunk 0
      "website": "https://example.com/bristol",
      "address": "12 Quay Street, Bristol BS1 4XX",   string, or a dict of parts
      "address_hidden": false,         true for a service-area business whose address is private
      "abbreviations": {"rd": "road"}  optional: extra address abbreviations to expand
    }

  listings.json   one object per listing you observed
    [
      {"platform": "Maps platform", "priority": 1, "url": "https://...",
       "listed": true, "name": "...", "phone": "...", "website": "...", "address": "..."}
    ]

priority is yours to set (1 = most used by your customers, 3 = least); default 2.

What it reports, per listing:
  FIX    a different name, phone, website host, or address; a private address
         that is published; or a listing for a different business
  CHECK  differences that may be formatting only (legal suffix, phone prefix,
         website path), and fields missing from the listing
  NOT LISTED  the platform has no listing; decide whether it matters to customers
         before creating one, and skip platforms that demand a private address

Abbreviations: common English street-type abbreviations are expanded by default
(St/Street, Ave/Avenue, ...). Add your market's abbreviations in "abbreviations".

Usage:
  python3 nap_checker.py --canonical canonical.json --listings listings.json [--json]
  python3 nap_checker.py --demo

Network: none. Writes: nothing; output goes to stdout. Stdlib only.
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse

DEFAULT_ABBREVIATIONS = {
    "st": "street", "ave": "avenue", "av": "avenue", "blvd": "boulevard", "dr": "drive",
    "rd": "road", "ln": "lane", "ct": "court", "pl": "place", "sq": "square", "hwy": "highway",
    "pkwy": "parkway", "ste": "suite", "fl": "floor", "bldg": "building", "apt": "apartment",
    "n": "north", "s": "south", "e": "east", "w": "west",
}
LEGAL_SUFFIXES = {"llc", "inc", "incorporated", "corp", "corporation", "ltd", "limited", "co",
                  "company", "plc", "gmbh", "sa", "sas", "srl", "bv", "pty", "pt", "tbk", "kk"}
ADDRESS_FIELDS = ("street", "locality", "city", "region", "state", "postal_code", "zip", "country")

DEMO_CANONICAL = {
    "name": "Harbor Cycle",
    "phone": "020 7946 0000",
    "country_code": "44",
    "website": "https://example.com/bristol",
    "address": "12 Quay Street, Bristol BS1 4XX",
    "address_hidden": False,
}
DEMO_LISTINGS = [
    {"platform": "Maps platform A", "priority": 1, "url": "https://maps.example/a", "listed": True,
     "name": "Harbor Cycle", "phone": "+44 20 7946 0000", "website": "https://www.example.com/bristol/",
     "address": "12 Quay St, Bristol BS1 4XX"},
    {"platform": "Maps platform B", "priority": 1, "url": "", "listed": False},
    {"platform": "Local directory", "priority": 2, "url": "https://directory.example/harbor", "listed": True,
     "name": "Harbor Cycle Ltd", "phone": "020 7946 0999", "website": "http://example.com/",
     "address": "40 Old Market Road, Bristol BS2 0XX"},
    {"platform": "Industry directory", "priority": 3, "url": "https://industry.example/harbor", "listed": True,
     "name": "Harbour Cycles Bristol Bike Repair", "phone": "", "website": "https://example.com/bristol?utm_source=dir"},
]


def words(text):
    return re.sub(r"[^\w\s]", " ", str(text or "").lower()).split()


def norm_name(name):
    w = words(name)
    core = [x for x in w if x not in LEGAL_SUFFIXES]
    return " ".join(w), " ".join(core)


def phone_digits(phone, country_code=""):
    raw = str(phone or "").strip()
    digits = re.sub(r"\D", "", raw)
    if country_code:
        cc = re.sub(r"\D", "", str(country_code))
        if digits.startswith("00" + cc):
            digits = digits[2 + len(cc):]
        elif raw.startswith("+") and digits.startswith(cc):
            digits = digits[len(cc):]
        if digits.startswith("0"):
            digits = digits[1:]
    return digits


def norm_address(value, abbreviations):
    if isinstance(value, dict):
        value = " ".join(str(value.get(k, "")) for k in ADDRESS_FIELDS if value.get(k))
    return " ".join(abbreviations.get(w, w) for w in words(value))


def norm_site(url):
    if not url:
        return "", ""
    p = urlparse(url if "://" in url else "https://" + url)
    host = (p.netloc or "").lower()
    if host.startswith("www."):
        host = host[4:]
    return host, (p.path or "/").rstrip("/") or "/"


def compare(canon, listing, abbreviations):
    """Return a list of (level, field, message) for one listing."""
    out = []
    # Name
    if listing.get("name"):
        cfull, ccore = norm_name(canon.get("name", ""))
        lfull, lcore = norm_name(listing["name"])
        if cfull != lfull:
            if ccore == lcore:
                out.append(("CHECK", "name", f"legal suffix differs: '{listing['name']}' (usually fine)"))
            else:
                out.append(("FIX", "name", f"'{listing['name']}' vs verified '{canon.get('name', '')}'"
                                           " (keyword-stuffed, old, or a different business?)"))
    else:
        out.append(("CHECK", "name", "missing from listing"))
    # Phone
    cc = canon.get("country_code", "")
    cp, lp = phone_digits(canon.get("phone"), cc), phone_digits(listing.get("phone"), cc)
    if cp and not lp:
        out.append(("CHECK", "phone", "missing from listing"))
    elif cp and lp != cp:
        if len(cp) >= 7 and len(lp) >= 7 and (cp.endswith(lp) or lp.endswith(cp)):
            out.append(("CHECK", "phone", f"'{listing['phone']}' differs only by prefix; set country_code to confirm"))
        else:
            out.append(("FIX", "phone", f"'{listing['phone']}' vs verified '{canon.get('phone', '')}'"))
    # Address
    laddr = listing.get("address")
    if canon.get("address_hidden"):
        if laddr:
            out.append(("FIX", "address", "address published, but the verified address is private: hide it or remove the listing"))
    elif canon.get("address"):
        if not laddr:
            out.append(("CHECK", "address", "missing from listing"))
        else:
            ca, la = norm_address(canon["address"], abbreviations), norm_address(laddr, abbreviations)
            if ca != la:
                level = "CHECK" if set(ca.split()) <= set(la.split()) or set(la.split()) <= set(ca.split()) else "FIX"
                note = " (one is a subset of the other: unit, region, or country added?)" if level == "CHECK" else ""
                out.append((level, "address", f"'{laddr if isinstance(laddr, str) else json.dumps(laddr)}'{note}"))
    # Website
    ch, cpath = norm_site(canon.get("website"))
    lh, lpath = norm_site(listing.get("website"))
    if ch and not lh:
        out.append(("CHECK", "website", "missing from listing"))
    elif ch and lh != ch:
        out.append(("FIX", "website", f"host '{lh}' vs verified '{ch}'"))
    elif ch and lpath != cpath:
        out.append(("CHECK", "website", f"path '{lpath}' vs '{cpath}': link the matching location page"))
    return out


def run(canon, listings):
    abbreviations = dict(DEFAULT_ABBREVIATIONS)
    abbreviations.update({str(k).lower(): str(v).lower() for k, v in (canon.get("abbreviations") or {}).items()})
    results = []
    for item in listings:
        entry = {"platform": item.get("platform", "unknown"), "priority": int(item.get("priority", 2)),
                 "url": item.get("url", ""), "listed": bool(item.get("listed", True)), "issues": []}
        if entry["listed"]:
            entry["issues"] = [{"level": a, "field": b, "message": c} for a, b, c in compare(canon, item, abbreviations)]
        results.append(entry)
    results.sort(key=lambda r: (r["priority"], not any(i["level"] == "FIX" for i in r["issues"])))
    summary = {
        "listings": len(results),
        "not_listed": sum(1 for r in results if not r["listed"]),
        "with_fix": sum(1 for r in results if any(i["level"] == "FIX" for i in r["issues"])),
        "with_check_only": sum(1 for r in results if r["issues"] and all(i["level"] == "CHECK" for i in r["issues"])),
        "clean": sum(1 for r in results if r["listed"] and not r["issues"]),
    }
    return results, summary


def print_report(canon, results, summary):
    print("=" * 64)
    print("  NAP CONSISTENCY")
    print("=" * 64)
    shown = "(private)" if canon.get("address_hidden") else canon.get("address", "")
    print(f"  Verified: {canon.get('name', '')} | {canon.get('phone', '')} | {canon.get('website', '')}")
    print(f"            {shown if isinstance(shown, str) else json.dumps(shown)}")
    for r in results:
        print(f"\n  [P{r['priority']}] {r['platform']}  {r['url']}")
        if not r["listed"]:
            print("    NOT LISTED  decide whether customers use this platform before creating a listing")
        elif not r["issues"]:
            print("    OK")
        for i in r["issues"]:
            print(f"    {i['level']:<6} {i['field']:<8} {i['message']}")
    print("\n" + "-" * 64)
    print(f"  {summary['listings']} listings: {summary['with_fix']} need a fix, {summary['with_check_only']} need a check, "
          f"{summary['clean']} clean, {summary['not_listed']} not listed.")
    print("  Fix wrong phones, old addresses, published private addresses, and duplicates first.")


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"error: {path}: {exc}")


def main():
    ap = argparse.ArgumentParser(description="Compare verified NAP facts with observed listings (offline).",
                                 epilog=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--canonical", help="JSON file with the verified public facts")
    ap.add_argument("--listings", help="JSON file: a list of observed listings")
    ap.add_argument("--demo", action="store_true", help="Run on built-in sample data")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of the text report")
    args = ap.parse_args()

    if args.demo:
        canon, listings = DEMO_CANONICAL, DEMO_LISTINGS
    elif args.canonical and args.listings:
        canon, listings = load(args.canonical), load(args.listings)
    else:
        ap.print_help()
        return
    if not isinstance(canon, dict) or not isinstance(listings, list):
        sys.exit("error: canonical must be a JSON object and listings a JSON list")

    results, summary = run(canon, listings)
    if args.json:
        print(json.dumps({"summary": summary, "listings": results}, indent=2, ensure_ascii=False))
    else:
        print_report(canon, results, summary)


if __name__ == "__main__":
    main()
