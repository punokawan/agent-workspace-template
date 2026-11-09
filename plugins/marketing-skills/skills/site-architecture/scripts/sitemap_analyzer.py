#!/usr/bin/env python3
"""
sitemap_analyzer.py - structural audit of an XML sitemap.

Reports URL depth distribution, top sections and URL patterns, query-string
URLs, deep URLs, the same slug in several directories, URL hygiene (uppercase,
underscores, mixed trailing slashes, mixed hosts or protocols, duplicates),
lastmod quality, and the 50,000-URL limit. Handles hreflang, image, and video
sitemaps and .gz files. For a sitemap index it lists the child sitemaps; run
it again on each child you want analyzed.

Orphan check (optional): pass --linked with a crawl export of URLs that have at
least one internal link (one URL per line, or a CSV whose first column is the
URL). Sitemap URLs missing from that list are orphan candidates; linked URLs
missing from the sitemap are listed too.

URL depth is not click depth: a short URL can still be five clicks from the
homepage. Use a crawler for click depth.

Usage:
  python3 sitemap_analyzer.py sitemap.xml [--linked linked.txt] [--json]
  python3 sitemap_analyzer.py https://example.com/sitemap.xml
  python3 sitemap_analyzer.py - < sitemap.xml
  python3 sitemap_analyzer.py --demo

Network: only when the source is an http(s) URL, and only to that URL.
Writes: nothing; output goes to stdout. Stdlib only.
"""

import argparse
import csv
import gzip
import json
import re
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from datetime import datetime, timezone
from urllib.parse import urlparse, urlunparse

MAX_BYTES = 60 * 1024 * 1024
URL_LIMIT = 50_000

DEMO = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
  <url><loc>https://example.com/</loc><lastmod>2026-01-05</lastmod>
    <xhtml:link rel="alternate" hreflang="de" href="https://example.com/de/"/></url>
  <url><loc>https://example.com/pricing</loc><lastmod>2026-01-05</lastmod></url>
  <url><loc>https://example.com/features/analytics</loc><lastmod>2026-01-05</lastmod></url>
  <url><loc>https://example.com/features/Automation</loc><lastmod>2026-01-05</lastmod></url>
  <url><loc>https://example.com/blog/email-tips/</loc><lastmod>2026-01-05</lastmod></url>
  <url><loc>https://example.com/blog/cold_email_guide</loc><lastmod>2026-01-05</lastmod></url>
  <url><loc>https://example.com/resources/email-tips</loc><lastmod>2026-01-05</lastmod></url>
  <url><loc>https://example.com/resources/guides/email/outreach/templates</loc></url>
  <url><loc>https://example.com/search?q=email&amp;sort=new</loc></url>
  <url><loc>http://www.example.com/customers/12345</loc><lastmod>2099-01-01</lastmod></url>
</urlset>"""


def local(tag):
    return tag.rsplit("}", 1)[-1]


def read_source(source):
    """Return sitemap bytes from a path, '-', or an http(s) URL. Decompresses gzip."""
    if source == "-":
        raw = sys.stdin.buffer.read()
    elif re.match(r"^https?://", source, re.I):
        req = urllib.request.Request(source, headers={"User-Agent": "sitemap_analyzer.py (stdlib urllib)"})
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:  # fetches only the URL the user passed
                raw = resp.read(MAX_BYTES)
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            sys.exit(f"error: could not fetch {source}: {exc}")
    elif "://" in source:
        sys.exit("error: only http(s) URLs or local files are supported")
    else:
        try:
            with open(source, "rb") as fh:
                raw = fh.read(MAX_BYTES)
        except OSError as exc:
            sys.exit(f"error: {exc}")
    if raw[:2] == b"\x1f\x8b":
        try:
            raw = gzip.decompress(raw)
        except (OSError, EOFError) as exc:
            sys.exit(f"error: could not decompress gzip data: {exc}")
    return raw


def parse(raw):
    """Return ('urlset', [ {url, lastmod} ]) or ('index', [child sitemap URLs])."""
    if re.search(rb"<!DOCTYPE|<!ENTITY", raw, re.I):
        sys.exit("error: DTD or entity declarations found; sitemaps never need them, so the file was not parsed")
    try:
        root = ET.fromstring(raw)
    except ET.ParseError as exc:
        sys.exit(f"error: XML parse error: {exc}")
    kind = local(root.tag)
    if kind == "sitemapindex":
        return "index", [loc.text.strip() for loc in root.iter() if local(loc.tag) == "loc" and loc.text]
    entries = []
    for node in root:
        if local(node.tag) != "url":
            continue
        loc = lastmod = None
        for child in node:              # direct children only: skips image:loc and video:* inside <url>
            name = local(child.tag)
            if name == "loc" and child.text:
                loc = child.text.strip()
            elif name == "lastmod" and child.text:
                lastmod = child.text.strip()
        if loc:
            entries.append({"url": loc, "lastmod": lastmod})
    return kind, entries


def segments(path):
    return [s for s in path.split("/") if s]


def pattern_of(path):
    segs = segments(path)
    if not segs:
        return "/"
    norm = ["{id}" if re.fullmatch(r"\d+|[0-9a-f]{8,}", s, re.I) else s for s in segs[:-1]]
    return "/" + "/".join(norm + ["{slug}"])


def norm_url(url):
    p = urlparse(url.strip())
    path = p.path.rstrip("/") or "/"
    return urlunparse((p.scheme.lower(), (p.netloc or "").lower(), path, "", p.query, ""))


def load_linked(path):
    urls = set()
    try:
        with open(path, encoding="utf-8", errors="replace", newline="") as fh:
            for row in csv.reader(fh):
                if row and re.match(r"^https?://", row[0].strip(), re.I):
                    urls.add(norm_url(row[0]))
    except OSError as exc:
        sys.exit(f"error: {exc}")
    return urls


def analyze(entries, linked=None):
    urls = [e["url"] for e in entries]
    parsed = [urlparse(u) for u in urls]
    depths = Counter(len(segments(p.path)) for p in parsed)
    sections = Counter((segments(p.path) or ["/"])[0] for p in parsed)
    patterns = Counter(pattern_of(p.path) for p in parsed)

    by_slug = defaultdict(set)
    for p in parsed:
        segs = segments(p.path)
        if segs:
            by_slug[segs[-1].lower()].add("/".join(segs[:-1]))
    dup_slugs = {s: sorted(d) for s, d in by_slug.items() if len(d) > 1}

    non_root = [p for p in parsed if p.path not in ("", "/")]
    slash = sum(1 for p in non_root if p.path.endswith("/"))
    hosts = Counter(p.netloc.lower() for p in parsed)
    schemes = Counter(p.scheme.lower() for p in parsed)

    today = datetime.now(timezone.utc).date().isoformat()
    lastmods = [e["lastmod"] for e in entries if e["lastmod"]]
    top_lastmod = Counter(l[:10] for l in lastmods).most_common(1)

    result = {
        "total_urls": len(urls),
        "over_limit": len(urls) > URL_LIMIT,
        "depth_distribution": dict(sorted(depths.items())),
        "top_sections": dict(sections.most_common(15)),
        "top_patterns": dict(patterns.most_common(10)),
        "query_urls": [u for u, p in zip(urls, parsed) if p.query],
        "deep_urls": [u for u, p in zip(urls, parsed) if len(segments(p.path)) >= 4],
        "same_slug_in_several_directories": dup_slugs,
        "uppercase_urls": [u for u, p in zip(urls, parsed) if p.path != p.path.lower()],
        "underscore_urls": [u for u, p in zip(urls, parsed) if "_" in p.path],
        "trailing_slash": {"with": slash, "without": len(non_root) - slash},
        "hosts": dict(hosts),
        "schemes": dict(schemes),
        "duplicate_urls": [u for u, n in Counter(urls).items() if n > 1],
        "lastmod": {
            "missing": len(urls) - len(lastmods),
            "future": sum(1 for l in lastmods if l[:10] > today),
            "most_common_share": round(top_lastmod[0][1] / len(lastmods), 2) if top_lastmod else 0,
        },
    }
    if linked is not None:
        in_sitemap = {norm_url(u) for u in urls}
        sitemap_hosts = {urlparse(u).netloc.lower() for u in in_sitemap}
        result["orphan_candidates"] = sorted(in_sitemap - linked)
        result["linked_not_in_sitemap"] = sorted(u for u in linked - in_sitemap if urlparse(u).netloc in sitemap_hosts)
    return result


def findings(a):
    issues, warnings = [], []
    if a["over_limit"]:
        issues.append(f"{a['total_urls']:,} URLs: a sitemap file may hold at most {URL_LIMIT:,}. Split it and use a sitemap index.")
    if len(a["schemes"]) > 1 or len(a["hosts"]) > 1:
        issues.append(f"Mixed protocols or hosts {a['schemes']} {a['hosts']}: list only canonical URLs (one protocol, one host).")
    if a["duplicate_urls"]:
        warnings.append(f"{len(a['duplicate_urls'])} URL(s) listed more than once.")
    if a["query_urls"]:
        warnings.append(f"{len(a['query_urls'])} URL(s) with query strings: keep only canonical, indexable URLs in the sitemap.")
    if a["uppercase_urls"]:
        warnings.append(f"{len(a['uppercase_urls'])} URL(s) with uppercase letters: lowercase paths and 301 the variants.")
    if a["underscore_urls"]:
        warnings.append(f"{len(a['underscore_urls'])} URL(s) with underscores: use hyphens for new URLs.")
    ts = a["trailing_slash"]
    if ts["with"] and ts["without"]:
        warnings.append(f"Mixed trailing slashes ({ts['with']} with, {ts['without']} without): pick one form and redirect the other.")
    if a["deep_urls"]:
        warnings.append(f"{len(a['deep_urls'])} URL(s) 4+ directories deep: flatten if the folders aren't real pages, "
                        "and check these pages are still a few clicks from the homepage.")
    if a["same_slug_in_several_directories"]:
        warnings.append(f"{len(a['same_slug_in_several_directories'])} slug(s) appear in several directories: check for duplicate topics.")
    lm = a["lastmod"]
    if lm["future"]:
        warnings.append(f"{lm['future']} lastmod date(s) in the future.")
    if a["total_urls"] >= 10 and lm["most_common_share"] >= 0.9:
        warnings.append("90%+ of lastmod values are identical: likely generated at build time. Search engines ignore lastmod they can't trust.")
    if lm["missing"] and lm["missing"] < a["total_urls"]:
        warnings.append(f"{lm['missing']} URL(s) without lastmod.")
    if "orphan_candidates" in a and a["orphan_candidates"]:
        issues.append(f"{len(a['orphan_candidates'])} sitemap URL(s) have no internal link in the crawl export (orphan candidates).")
    if a.get("linked_not_in_sitemap"):
        warnings.append(f"{len(a['linked_not_in_sitemap'])} linked URL(s) are missing from the sitemap: add them if they are canonical and indexable.")
    return issues, warnings


def print_report(a, issues, warnings, limit=5):
    print("=" * 64)
    print(f"  SITEMAP STRUCTURE   {a['total_urls']:,} URLs")
    print("=" * 64)
    print("\n  URL depth (directories in the path; not click depth):")
    for depth, n in a["depth_distribution"].items():
        print(f"    depth {depth}: {n:6,}  {'#' * max(1, round(n / a['total_urls'] * 40))}")
    print("\n  Top sections:")
    for s, n in a["top_sections"].items():
        print(f"    /{s if s != '/' else '':<30} {n:6,}")
    print("\n  Top URL patterns:")
    for pat, n in a["top_patterns"].items():
        print(f"    {pat:<40} {n:6,}")
    for title, items in (("ISSUES", issues), ("WARNINGS", warnings)):
        if items:
            print(f"\n  {title}:")
            for item in items:
                print(f"    - {item}")
    for key, label in (("orphan_candidates", "Orphan candidates"), ("query_urls", "Query-string URLs"),
                       ("deep_urls", "Deep URLs"), ("uppercase_urls", "Uppercase URLs")):
        items = a.get(key) or []
        if items:
            print(f"\n  {label} (first {min(limit, len(items))}):")
            for u in items[:limit]:
                print(f"    {u}")
    if not issues and not warnings:
        print("\n  No structural problems found in this sitemap.")


def main():
    ap = argparse.ArgumentParser(description="Structural audit of an XML sitemap (file, '-', or one http(s) URL).")
    ap.add_argument("source", nargs="?", help="sitemap.xml path, .xml.gz, '-' for stdin, or an http(s) URL")
    ap.add_argument("--linked", help="Crawl export of internally linked URLs (one per line or CSV first column)")
    ap.add_argument("--demo", action="store_true", help="Run on a built-in sample sitemap")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of the text report")
    args = ap.parse_args()

    if args.demo:
        raw = DEMO.encode("utf-8")
    elif args.source:
        raw = read_source(args.source)
    else:
        ap.print_help()
        return

    kind, items = parse(raw)
    if kind == "index":
        if args.json:
            print(json.dumps({"type": "sitemapindex", "children": items}, indent=2))
        else:
            print(f"Sitemap index with {len(items)} child sitemap(s). Run this script on each one you want analyzed:")
            for child in items:
                print(f"  {child}")
        return
    if not items:
        sys.exit("error: no <url><loc> entries found")

    analysis = analyze(items, load_linked(args.linked) if args.linked else None)
    issues, warnings = findings(analysis)
    if args.json:
        print(json.dumps({"type": "urlset", "issues": issues, "warnings": warnings, "analysis": analysis}, indent=2))
    else:
        print_report(analysis, issues, warnings)


if __name__ == "__main__":
    main()
