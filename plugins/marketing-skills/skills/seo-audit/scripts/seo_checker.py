#!/usr/bin/env python3
"""
seo_checker.py - score one page's on-page SEO basics from 0 to 100.

Checks: title, meta description, H1 count, heading levels, image alt text,
internal/external links, word count, viewport, canonical, and robots meta.

Reads static HTML only. Content or JSON-LD that JavaScript injects is invisible
to it, so save the rendered HTML from a browser when a page depends on scripts.
Length and word-count thresholds are heuristics, not ranking rules.

Usage:
  python3 seo_checker.py --file page.html [--json]
  python3 seo_checker.py --file - < page.html
  python3 seo_checker.py --url https://example.com/page [--json]
  python3 seo_checker.py --demo

Network: only with --url, and only to that URL (redirects followed).
Writes: nothing; output goes to stdout.
Stdlib only.
"""

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

MAX_BYTES = 5 * 1024 * 1024
GENERIC_ANCHORS = {"click here", "here", "read more", "learn more", "more", "this", "link"}
SKIP_TEXT_TAGS = {"script", "style", "template", "noscript", "title"}


class SEOParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self._in_title = False
        self.meta_description = None
        self.robots = []
        self.canonical = None
        self.viewport = False
        self.headings = []            # (level, text)
        self._h_level = None
        self._h_text = []
        self.images = []              # {"src", "alt"}; alt None = attribute missing
        self.links = []               # {"href", "text"}
        self._a_href = None
        self._a_text = []
        self.text_parts = []
        self._in_head = False
        self._skip_depth = 0
        self._svg_depth = 0

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "head":
            self._in_head = True
        elif tag == "body":
            self._in_head = False
        elif tag == "svg":
            self._svg_depth += 1
        if tag in SKIP_TEXT_TAGS:
            self._skip_depth += 1
        if tag == "title":
            # Only the document title counts; inline SVG icons carry their own <title>.
            self._in_title = not self._svg_depth and not self.title
        elif tag == "meta":
            name = a.get("name", "").lower()
            if name == "description" and self.meta_description is None:
                self.meta_description = a.get("content", "")
            elif name in ("robots", "googlebot"):
                self.robots.extend(t.strip().lower() for t in a.get("content", "").split(","))
            elif name == "viewport":
                self.viewport = True
        elif tag == "link":
            rels = a.get("rel", "").lower().split()
            if "canonical" in rels and self.canonical is None:
                self.canonical = a.get("href", "").strip()
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._h_level = int(tag[1])
            self._h_text = []
        elif tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a["alt"] if "alt" in a else None})
        elif tag == "a":
            self._a_href = a.get("href", "").strip()
            self._a_text = []

    def handle_endtag(self, tag):
        if tag in SKIP_TEXT_TAGS and self._skip_depth:
            self._skip_depth -= 1
        if tag == "svg" and self._svg_depth:
            self._svg_depth -= 1
        if tag == "head":
            self._in_head = False
        elif tag == "title":
            self._in_title = False
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._h_level is not None:
            self.headings.append((self._h_level, " ".join("".join(self._h_text).split())))
            self._h_level = None
        elif tag == "a" and self._a_href is not None:
            self.links.append({"href": self._a_href, "text": " ".join("".join(self._a_text).split())})
            self._a_href = None

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._h_level is not None:
            self._h_text.append(data)
        if self._a_href is not None:
            self._a_text.append(data)
        if not self._in_head and not self._skip_depth:
            self.text_parts.append(data)


def _strip_www(host):
    return host[4:] if host.startswith("www.") else host


def _host(url):
    return _strip_www((urlparse(url).hostname or "").lower())


def classify_links(links, base_url, domain):
    """Split links into internal and external; ignore fragments, mailto, tel, javascript."""
    site = _strip_www(domain.lower()) if domain else (_host(base_url) if base_url else "")
    internal, external = [], []
    for link in links:
        href = link["href"]
        if not href or href.startswith("#") or href.lower().startswith(("mailto:", "tel:", "javascript:", "data:")):
            continue
        absolute = urljoin(base_url, href) if base_url else href
        parsed = urlparse(absolute)
        if parsed.scheme and parsed.scheme not in ("http", "https"):
            continue
        if not parsed.netloc:              # relative link and no base URL to resolve it
            internal.append(link)
        elif site and _host(absolute) == site:
            internal.append(link)
        else:
            external.append(link)
    return internal, external


def analyze_html(html, base_url="", domain=""):
    p = SEOParser()
    p.feed(html)
    p.close()
    r = {}

    title = " ".join(p.title.split())
    n = len(title)
    ok = 50 <= n <= 60
    r["title"] = {
        "value": title, "length": n, "pass": ok,
        "score": 100 if ok else (50 if title else 0),
        "note": "Good length (about 50-60 chars; Google truncates by pixel width)" if ok else (
            f"Too {'short' if n < 50 else 'long'} ({n} chars)" if title else "Missing <title>"),
    }

    desc = " ".join((p.meta_description or "").split())
    n = len(desc)
    ok = 150 <= n <= 160
    r["meta_description"] = {
        "value": desc[:90] + ("..." if n > 90 else ""), "length": n, "pass": ok,
        "score": 100 if ok else (50 if 100 <= n < 150 or 160 < n <= 200 else (30 if desc else 0)),
        "note": "Good length" if ok else (
            f"Too {'short' if n < 150 else 'long'} ({n} chars)" if desc else "Missing meta description"),
    }

    h1s = [t for lvl, t in p.headings if lvl == 1]
    ok = len(h1s) == 1
    r["h1"] = {
        "count": len(h1s), "values": h1s, "pass": ok,
        "score": 100 if ok else (50 if h1s else 0),
        "note": "Exactly one H1" if ok else (f"{len(h1s)} H1s" if h1s else "No H1"),
    }

    skips, prev = [], 0
    for lvl, _ in p.headings:
        if prev and lvl > prev + 1:
            skips.append(f"H{prev} -> H{lvl}")
        prev = lvl
    r["heading_levels"] = {
        "issues": skips, "pass": not skips, "score": max(0, 100 - 25 * len(skips)),
        "note": "No skipped levels" if not skips else f"Skipped levels: {', '.join(skips)}",
    }

    total = len(p.images)
    missing = sum(1 for i in p.images if i["alt"] is None)
    empty = sum(1 for i in p.images if i["alt"] is not None and not i["alt"].strip())
    covered = total - missing
    r["image_alt"] = {
        "images": total, "missing_alt": missing, "empty_alt": empty, "pass": missing == 0,
        "score": round(covered / total * 100) if total else 100,
        "note": ("No images" if not total else
                 ("Every image has an alt attribute" if not missing else f"{missing} image(s) missing alt"))
                + (f"; {empty} with alt=\"\" (fine only if decorative)" if empty else ""),
    }

    internal, external = classify_links(p.links, base_url, domain)
    counted = len(internal) + len(external)
    ratio = len(internal) / counted if counted else 1.0
    generic = sum(1 for link in internal if link["text"].lower().strip(" .:!?") in GENERIC_ANCHORS)
    r["links"] = {
        "internal": len(internal), "external": len(external), "generic_anchor_internal": generic,
        "pass": ratio >= 0.5 and not generic,
        "score": 100 if ratio >= 0.5 else round(ratio * 100),
        "note": (f"{len(internal)} internal, {len(external)} external" if counted else "No links")
                + (f"; {generic} internal link(s) with generic anchor text" if generic else ""),
    }

    words = len(re.findall(r"\w+", " ".join(p.text_parts)))
    ok = words >= 300
    r["word_count"] = {
        "count": words, "pass": ok, "score": 100 if ok else min(100, round(words / 300 * 100)),
        "note": f"{words} words" + ("" if ok else " (under 300: check the page has enough unique content)"),
    }

    r["viewport"] = {
        "pass": p.viewport, "score": 100 if p.viewport else 0,
        "note": "Viewport meta present" if p.viewport else "Missing viewport meta",
    }

    canon = p.canonical
    if canon is None:
        r["canonical"] = {"value": None, "pass": False, "score": 0, "note": "No canonical tag"}
    else:
        absolute = bool(urlparse(canon).scheme)
        note = "Canonical present" if absolute else "Canonical is relative; use an absolute URL"
        if base_url and absolute and canon.rstrip("/") != base_url.rstrip("/"):
            note += f"; points to another URL ({canon}) - confirm that is intended"
        r["canonical"] = {"value": canon, "pass": absolute, "score": 100 if absolute else 70, "note": note}

    noindex = "noindex" in p.robots or "none" in p.robots
    nofollow = "nofollow" in p.robots or "none" in p.robots
    r["robots_meta"] = {
        "directives": [d for d in p.robots if d], "pass": not noindex, "score": 0 if noindex else 100,
        "note": ("CRITICAL: noindex - this page will be dropped from search results" if noindex else
                 ("nofollow on all links" if nofollow else "Indexable (no blocking robots meta)")),
    }
    return r


WEIGHTS = {"title": 20, "meta_description": 10, "h1": 15, "heading_levels": 5, "image_alt": 10,
           "links": 5, "word_count": 10, "viewport": 5, "canonical": 10, "robots_meta": 10}

LABELS = {"title": "Title tag", "meta_description": "Meta description", "h1": "H1",
          "heading_levels": "Heading levels", "image_alt": "Image alt text", "links": "Links",
          "word_count": "Word count", "viewport": "Viewport", "canonical": "Canonical",
          "robots_meta": "Robots meta"}


def overall_score(results):
    return round(sum(results[k]["score"] * w for k, w in WEIGHTS.items()) / sum(WEIGHTS.values()))


def fetch(url):
    if urlparse(url).scheme not in ("http", "https"):
        sys.exit("error: --url must start with http:// or https://")
    req = urllib.request.Request(url, headers={"User-Agent": "seo_checker.py (stdlib urllib)"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:  # fetches only the URL the user passed
            body = resp.read(MAX_BYTES)
            charset = resp.headers.get_content_charset() or "utf-8"
            return body.decode(charset, errors="replace"), resp.geturl()
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        sys.exit(f"error: could not fetch {url}: {exc}")


DEMO_HTML = """<!DOCTYPE html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Invoice Templates for Freelancers: 12 Free Downloads</title>
<meta name="description" content="Download 12 free invoice templates for freelancers in Word, Excel, and PDF. Each one includes payment terms, tax fields, and a late-fee line you can edit.">
<link rel="canonical" href="https://example.com/templates/invoice">
</head><body>
<h1>Invoice Templates for Freelancers</h1>
<p>Pick a template, add your details, and send it. Every file below is free to edit.</p>
<h2>Templates by format</h2>
<img src="word.png" alt="Invoice template in Word with a late-fee line">
<img src="divider.png" alt="">
<h4>Word</h4>
<p>Best when clients ask for an editable file.</p>
<a href="/templates/invoice/word">Word invoice template</a>
<a href="https://example.org/tax-guide">Tax guide</a>
<a href="/blog/payment-terms">click here</a>
<img src="excel.png">
</body></html>"""


def main():
    ap = argparse.ArgumentParser(description="Score one page's on-page SEO basics (0-100) from static HTML.")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--file", help="HTML file to check ('-' reads stdin)")
    src.add_argument("--url", help="Fetch and check this one URL (http or https)")
    src.add_argument("--demo", action="store_true", help="Run on built-in sample HTML")
    ap.add_argument("--domain", default="", help="Site host for internal-link detection (defaults to the --url host)")
    ap.add_argument("--json", action="store_true", help="Print JSON instead of the text report")
    args = ap.parse_args()

    base_url = ""
    if args.url:
        html, base_url = fetch(args.url)
    elif args.file == "-":
        html = sys.stdin.read()
    elif args.file:
        try:
            with open(args.file, encoding="utf-8", errors="replace") as fh:
                html = fh.read()
        except OSError as exc:
            sys.exit(f"error: {exc}")
    elif args.demo:
        html = DEMO_HTML
        base_url = "https://example.com/templates/invoice"
    else:
        ap.print_help()
        return

    results = analyze_html(html, base_url=base_url, domain=args.domain)
    score = overall_score(results)
    if args.json:
        print(json.dumps({"url": base_url or None, "overall_score": score, "checks": results}, indent=2))
        return

    print("=" * 64)
    print(f"  ON-PAGE CHECK   score {score}/100" + (f"   {base_url}" if base_url else ""))
    print("=" * 64)
    for key in WEIGHTS:
        res = results[key]
        status = "PASS" if res["pass"] else "FAIL"
        print(f"  {status}  {LABELS[key]:<17} [{res['score']:>3}]  {res['note']}")
    print("=" * 64)
    print("  Static HTML only: JS-injected content and schema are not seen.")


if __name__ == "__main__":
    main()
