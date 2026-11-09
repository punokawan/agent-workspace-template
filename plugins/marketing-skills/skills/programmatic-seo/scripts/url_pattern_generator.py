#!/usr/bin/env python3
"""
url_pattern_generator.py - expand a programmatic SEO URL pattern and check it
before any page is built.

Two input modes in one JSON config:
  "variables": every combination of the value lists (cartesian product)
  "rows":      only the combinations your data actually supports (preferred)

Example config:
{
  "template": "{tool}-vs-{competitor}",
  "base_url": "https://example.com/compare",
  "variables": {"tool": ["Acme", "Globex"], "competitor": ["Initech", "Globex"]},
  "skip_same_value": true
}
or
{
  "template": "{service}-in-{city}",
  "base_url": "https://example.com/services",
  "rows": [{"service": "Plumbing", "city": "Austin"}, {"service": "Roofing", "city": "Austin"}]
}

Reports page count, URL lengths, slug collisions (two inputs, one URL),
reverse pairs ("a-vs-b" and "b-vs-a"), empty or non-ASCII slug parts, and
template placeholders without data.

Usage:
  python3 url_pattern_generator.py config.json [--json] [--sample N]
  python3 url_pattern_generator.py --demo

Network: none. Writes: nothing; output goes to stdout. Stdlib only.
"""

import argparse
import json
import re
import sys
from itertools import product

PLACEHOLDER = re.compile(r"\{(\w+)\}")
LONG_URL = 75          # characters; long URLs are harder to read, share, and scan
WARN_PAGES = 1_000
ISSUE_PAGES = 10_000

DEMO = {
    "template": "{tool}-vs-{competitor}",
    "base_url": "https://example.com/compare",
    "variables": {
        "tool": ["Acme CRM", "Globex", "Initech"],
        "competitor": ["Globex", "Initech", "Umbrella Corp", "umbrella corp"],
    },
    "skip_same_value": True,
}


def slugify(value):
    """Lowercase; collapse anything that isn't a letter or digit into one hyphen. Keeps non-Latin letters."""
    return re.sub(r"[\W_]+", "-", str(value).strip().lower(), flags=re.UNICODE).strip("-")


def load_combinations(config):
    """Return a list of {variable: value} dicts from rows or from the cartesian product of variables."""
    if config.get("rows"):
        rows = config["rows"]
        if not isinstance(rows, list) or not all(isinstance(r, dict) for r in rows):
            raise ValueError('"rows" must be a list of objects')
        return [dict(r) for r in rows]
    variables = config.get("variables") or {}
    if not isinstance(variables, dict) or not variables:
        raise ValueError('config needs "rows" or a non-empty "variables" object')
    names = list(variables)
    combos = [dict(zip(names, values)) for values in product(*(variables[n] for n in names))]
    if config.get("skip_same_value", True):
        combos = [c for c in combos if len({slugify(v) for v in c.values()}) == len(c)]
    return combos


def generate(config):
    template = config.get("template")
    if not template or not PLACEHOLDER.search(template):
        raise ValueError('"template" must contain at least one {placeholder}')
    base = (config.get("base_url") or "https://example.com").rstrip("/")
    needed = PLACEHOLDER.findall(template)
    pages, problems = [], []
    for combo in load_combinations(config):
        missing = [n for n in needed if n not in combo or str(combo[n]).strip() == ""]
        if missing:
            problems.append(f"Input {combo} has no value for: {', '.join(missing)}")
            continue
        parts = {n: slugify(combo[n]) for n in needed}
        empty = [n for n, s in parts.items() if not s]
        if empty:
            problems.append(f"Input {combo} gives an empty slug for: {', '.join(empty)}")
            continue
        slug = PLACEHOLDER.sub(lambda m: parts[m.group(1)], template)
        pages.append({"url": f"{base}/{slug}", "slug": slug, "variables": combo})
    unused = sorted({k for p in pages for k in p["variables"]} - set(needed))
    return pages, problems, unused


def analyze(pages, problems, unused, config):
    issues, warnings = list(problems), []
    total = len(pages)
    if total > ISSUE_PAGES:
        issues.append(f"{total:,} pages: thin-content and crawl risk. Cut variables to combinations with real data and demand.")
    elif total > WARN_PAGES:
        warnings.append(f"{total:,} pages: confirm each one has unique data and search demand before building.")

    by_url = {}
    for p in pages:
        by_url.setdefault(p["url"], []).append(p["variables"])
    collisions = {u: v for u, v in by_url.items() if len(v) > 1}
    if collisions:
        issues.append(f"{len(collisions)} URL(s) produced by more than one input (slug collision). Deduplicate the data.")

    seen, reverse_pairs = {}, 0
    needed = PLACEHOLDER.findall(config["template"])
    if len(set(needed)) == 2:
        for p in pages:
            key = tuple(sorted(slugify(p["variables"][n]) for n in set(needed)))
            if key in seen and seen[key] != p["url"]:
                reverse_pairs += 1          # same pair, other order (exact duplicates are collisions)
            seen.setdefault(key, p["url"])
        if reverse_pairs:
            warnings.append(f"{reverse_pairs} reverse pair(s) such as 'a-vs-b' and 'b-vs-a': publish one order and 301 the other.")

    long_urls = [p["url"] for p in pages if len(p["url"]) > LONG_URL]
    if long_urls:
        warnings.append(f"{len(long_urls)} URL(s) longer than {LONG_URL} characters: shorten the template or the values.")
    non_ascii = [p["slug"] for p in pages if not p["slug"].isascii()]
    if non_ascii:
        warnings.append(f"{len(non_ascii)} slug(s) with non-ASCII letters: browsers show them, but they are percent-encoded "
                        "in links. Choose transliteration or native script per market on purpose.")
    if unused:
        warnings.append(f"Input fields not used in the template: {', '.join(unused)} (fine if they feed page content).")

    return {
        "total_pages": total,
        "avg_url_length": round(sum(len(p["url"]) for p in pages) / total) if total else 0,
        "max_url_length": max((len(p["url"]) for p in pages), default=0),
        "collisions": collisions,
        "issues": issues,
        "warnings": warnings,
    }


def print_report(config, pages, analysis, sample):
    print("=" * 64)
    print("  PROGRAMMATIC SEO - URL PATTERN CHECK")
    print("=" * 64)
    print(f"  Template:   {config['template']}")
    print(f"  Base URL:   {(config.get('base_url') or 'https://example.com').rstrip('/')}")
    print(f"  Input mode: {'rows (data-backed)' if config.get('rows') else 'variables (every combination)'}")
    print(f"  Pages:      {analysis['total_pages']:,}   URL length avg {analysis['avg_url_length']}, max {analysis['max_url_length']}")
    for title, items in (("ISSUES", analysis["issues"]), ("WARNINGS", analysis["warnings"])):
        if items:
            print(f"\n  {title}:")
            for item in items:
                print(f"    - {item}")
    for url, inputs in list(analysis["collisions"].items())[:5]:
        print(f"    collision {url} <- {inputs}")
    if not analysis["issues"] and not analysis["warnings"]:
        print("\n  No pattern problems found. Page value still depends on the data behind each URL.")
    print(f"\n  SAMPLE URLS (first {min(sample, len(pages))}):")
    for p in pages[:sample]:
        print(f"    {p['url']}")
    if len(pages) > sample:
        print(f"    ... and {len(pages) - sample:,} more (use --json for the full list)")


def main():
    ap = argparse.ArgumentParser(description="Expand and check a programmatic SEO URL pattern from a JSON config.")
    ap.add_argument("config", nargs="?", help="JSON config with template, base_url, and rows or variables")
    ap.add_argument("--demo", action="store_true", help="Run on a built-in comparison-page config")
    ap.add_argument("--json", action="store_true", help="Print every URL and the analysis as JSON")
    ap.add_argument("--sample", type=int, default=10, help="Sample URLs to show in the text report (default 10)")
    args = ap.parse_args()

    if args.demo:
        config = DEMO
    elif args.config:
        try:
            with open(args.config, encoding="utf-8") as fh:
                config = json.load(fh)
        except (OSError, json.JSONDecodeError) as exc:
            sys.exit(f"error: cannot read config: {exc}")
    else:
        ap.print_help()
        return

    try:
        pages, problems, unused = generate(config)
    except (ValueError, TypeError) as exc:
        sys.exit(f"error: {exc}")
    analysis = analyze(pages, problems, unused, config)

    if args.json:
        print(json.dumps({"config": config, "analysis": analysis, "urls": pages}, indent=2, ensure_ascii=False))
    else:
        print_report(config, pages, analysis, max(0, args.sample))


if __name__ == "__main__":
    main()
