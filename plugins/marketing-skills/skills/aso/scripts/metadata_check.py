#!/usr/bin/env python3
"""Check App Store and Google Play listing metadata, build an Apple keyword
field, and measure competitor keyword coverage.

Subcommands:
  check          validate a listing JSON against store limits and rules
  keyword-field  build the Apple keyword field (100 bytes) from ranked terms
  coverage       count which terms competitor titles and subtitles use

Standard library only. No network access, no writes: every command reads
the files you pass and prints to stdout.

Limits follow references/apple-specs.md and references/google-play-specs.md
(Apple: name 30, subtitle 30, keyword field 100 bytes, promotional text 170,
description 4,000, What's New 4,000; Google Play: title 30, short
description 80, full description 4,000, release notes 500).

Term checks (claims, calls to action) use English words only; review other
languages by hand. Word splitting needs spaces between words; for Chinese,
Japanese, Thai and similar scripts, pass explicit terms.

Adapted from metadata_optimizer.py, keyword_analyzer.py and
competitor_analyzer.py in alirezarezvani/claude-skills
(marketing-skill/skills/app-store-optimization, MIT).
"""

import argparse
import json
import re
import sys

LIMITS = {
    "apple": {
        "name": ("chars", 30),
        "subtitle": ("chars", 30),
        "keywords": ("bytes", 100),
        "promotional_text": ("chars", 170),
        "description": ("chars", 4000),
        "whats_new": ("chars", 4000),
    },
    "google": {
        "title": ("chars", 30),
        "short_description": ("chars", 80),
        "full_description": ("chars", 4000),
        "whats_new": ("chars", 500),
    },
}
FIELD_ALIASES = {
    "apple": {"title": "name", "app_name": "name", "keyword_field": "keywords",
              "promo_text": "promotional_text", "release_notes": "whats_new"},
    "google": {"name": "title", "app_name": "title", "short_desc": "short_description",
               "description": "full_description", "release_notes": "whats_new"},
}
SHORT_FIELDS = {"apple": ("name", "subtitle"), "google": ("title", "short_description")}
CLAIM_TERMS = ("best", "#1", "no. 1", "number one", "top", "free", "no ads", "cheapest")
CTA_TERMS = ("download now", "install now", "update now", "play now", "try now", "get it now", "buy now")
APPLE_PLATFORM_TERMS = ("android", "google play")
NO_SPACE_SCRIPT = re.compile(r"[฀-๿぀-ヿ㐀-䶿一-鿿가-힯]")
EMOJI_RE = re.compile(r"[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]")
WORD_RE = re.compile(r"[^\W_]+(?:['’][^\W_]+)*", re.UNICODE)
EN_STOPWORDS = {
    "a", "an", "and", "app", "apps", "by", "for", "from", "in", "of", "on", "or", "the", "to",
    "with", "your", "you", "my", "it", "is", "&",
}

DEMO_LISTING = {
    "apple": {
        "name": "MyTasks - Todo List & Planner",
        "subtitle": "Daily Task Manager & Reminders",
        "keywords": "task, todo,checklist,reminder,organize,daily,planner,schedule,deadline,goals,habit,widget",
        "promotional_text": "New: shared lists for families.",
        "description": "Forget missed deadlines. MyTasks keeps every task, reminder, and project in one place.",
    },
    "google": {
        "title": "MyTasks: BEST Todo List & Planner",
        "short_description": "Free to-do list and planner. Download now and never miss a deadline!",
        "full_description": (
            "Forget missed deadlines. MyTasks keeps every task, reminder, and project in one place, "
            "so you focus on doing, not remembering. Build a to-do list in seconds, set reminders "
            "that fit your day, and plan your week with a simple planner. Share lists with family "
            "or your team. Widgets keep your to-do list on your home screen."
        ),
    },
}
DEMO_COVERAGE = {
    "yours": {"title": "MyTasks - Todo List & Planner", "subtitle": "Daily Task Manager & Reminders"},
    "competitors": [
        {"app": "Comp A", "title": "Listly: To Do List & Tasks", "subtitle": "Planner, reminders, checklist"},
        {"app": "Comp B", "title": "Dayplan - Daily Planner", "subtitle": "To do list, habit tracker"},
        {"app": "Comp C", "title": "Tickit Task Manager", "subtitle": "To do list with reminders"},
        {"app": "Comp D", "title": "Focus List: Checklist", "subtitle": "Tasks, goals and habit tracker"},
    ],
}


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def load_json(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        fail(f"file not found: {path}")
    except json.JSONDecodeError as err:
        fail(f"invalid JSON in {path}: {err}")


def words(text):
    return [w.lower() for w in WORD_RE.findall(text or "")]


def term_pattern(term):
    term = term.strip().lower()
    if NO_SPACE_SCRIPT.search(term):
        return re.compile(re.escape(term))
    return re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE)


def count_term(term, text):
    return len(term_pattern(term).findall((text or "").lower()))


def split_terms(raw):
    return [t.strip() for t in re.split(r"[,\n]", raw or "") if t.strip()]


def load_stopwords(option):
    """'' -> none, 'en' -> built-in English list, anything else -> a file of words."""
    if not option:
        return set()
    if option == "en":
        return set(EN_STOPWORDS)
    try:
        with open(option, encoding="utf-8") as handle:
            return {w.lower() for w in split_terms(handle.read())}
    except FileNotFoundError:
        fail(f"file not found: {option}")


# ---------------------------------------------------------------- check


def normalize_listing(platform, listing):
    if not isinstance(listing, dict):
        fail("listing JSON must be an object of field names to text")
    aliases = FIELD_ALIASES[platform]
    fields, unknown = {}, []
    for key, value in listing.items():
        name = aliases.get(key, key)
        if name in LIMITS[platform]:
            fields[name] = "" if value is None else str(value)
        else:
            unknown.append(key)
    return fields, unknown


def check_listing(platform, listing, keywords, competitors):
    fields, unknown = normalize_listing(platform, listing)
    errors, warnings, notes, lengths = [], [], [], {}
    for name, (unit, limit) in LIMITS[platform].items():
        if name not in fields:
            continue
        text = fields[name]
        size = len(text.encode("utf-8")) if unit == "bytes" else len(text)
        lengths[name] = {"used": size, "limit": limit, "unit": unit}
        if size > limit:
            errors.append(f"{name}: {size}/{limit} {unit}, over the limit by {size - limit}.")
        elif name in SHORT_FIELDS[platform] and limit - size > 3:
            why = ("a brand-only title can be a deliberate choice for a dominant brand"
                   if name in ("name", "title") else "unused characters are unused keyword and message space")
            notes.append(f"{name}: uses {size}/{limit} {unit}. Challenger apps usually fill to within 3; {why}.")
    if unknown:
        notes.append("Ignored fields (not checked for this store): " + ", ".join(unknown))

    short_text = {f: fields.get(f, "") for f in SHORT_FIELDS[platform]}
    for field, text in short_text.items():
        lower = text.lower()
        claims = [t for t in CLAIM_TERMS if count_term(t, lower)]
        ctas = [t for t in CTA_TERMS if count_term(t, lower)]
        if claims:
            warnings.append(f"{field}: claim or price words {claims} risk rejection or a policy flag.")
        if ctas:
            warnings.append(f"{field}: calls to action {ctas} are not allowed here.")
        if platform == "google":
            if EMOJI_RE.search(text):
                warnings.append(f"{field}: emoji are not allowed in the title or short description.")
            caps = [w for w in re.findall(r"\b[A-Z]{3,}\b", text)]
            if caps:
                warnings.append(f"{field}: ALL CAPS words {caps}: keep them only for a registered brand name "
                                "or an acronym (such as PDF); otherwise use normal case.")
            if re.search(r"([!?$*#])\1", text):
                warnings.append(f"{field}: repeated special characters are not allowed.")
    for name in competitors:
        for field in list(SHORT_FIELDS[platform]) + (["keywords"] if platform == "apple" else []):
            if count_term(name, fields.get(field, "")):
                warnings.append(f"{field}: competitor name '{name}' is a trademark and rejection risk.")

    if platform == "apple":
        check_apple_keywords(fields, warnings, notes)
        apple_platform = [t for t in APPLE_PLATFORM_TERMS
                          if any(count_term(t, fields.get(f, "")) for f in ("name", "subtitle", "keywords"))]
        if apple_platform:
            warnings.append(f"Other platform names {apple_platform} in Apple metadata risk rejection (2.3.10).")

    density = keyword_report(platform, fields, keywords, notes) if keywords else []
    notes.append("Claim and call-to-action checks use English terms only; review other languages by hand.")
    return {"platform": platform, "lengths": lengths, "errors": errors, "warnings": warnings,
            "keywords": density, "notes": notes}


def check_apple_keywords(fields, warnings, notes):
    raw = fields.get("keywords")
    if raw is None:
        return
    cleaned = ",".join(t.strip() for t in raw.split(","))
    saved = len(raw.encode("utf-8")) - len(cleaned.encode("utf-8"))
    if saved:
        unit = "byte" if saved == 1 else "bytes"
        warnings.append(f"keywords: spaces around commas waste {saved} {unit}; write 'a,b,c'.")
    terms = [t.strip().lower() for t in raw.split(",")]
    if any(not t for t in terms):
        warnings.append("keywords: empty entries (double or trailing commas).")
    terms = [t for t in terms if t]
    dupes = sorted({t for t in terms if terms.count(t) > 1})
    if dupes:
        warnings.append(f"keywords: duplicate terms {dupes}.")
    indexed = set(words(fields.get("name", ""))) | set(words(fields.get("subtitle", "")))
    repeated = sorted({w for t in terms for w in words(t) if w in indexed})
    if repeated:
        warnings.append(
            f"keywords: {repeated} already appear in the name or subtitle; Apple indexes each word once, "
            "so these bytes add nothing."
        )
    name_words = set(words(fields.get("name", "")))
    sub_words = set(words(fields.get("subtitle", "")))
    overlap = sorted((name_words & sub_words) - EN_STOPWORDS)
    if overlap:
        warnings.append(f"name and subtitle repeat {overlap}; use the subtitle for new words.")
    if NO_SPACE_SCRIPT.search(raw):
        notes.append("keywords: CJK and Thai characters take 3 bytes each in UTF-8; the byte count above includes this.")


def keyword_report(platform, fields, keywords, notes):
    if platform == "apple":
        indexed = " ".join(fields.get(f, "") for f in ("name", "subtitle", "keywords"))
        report = []
        for term in keywords:
            parts = words(term) or [term.lower()]
            found = all(count_term(p, indexed) for p in parts)
            report.append({"keyword": term, "in_indexed_fields": found})
        notes.append("Apple: the description is not indexed for search, so density is not measured.")
        return report
    full = fields.get("full_description", "")
    total = len(full.split())
    first = " ".join(re.split(r"(?<=[.!?])\s+|\n+", full.strip())[:3])
    if NO_SPACE_SCRIPT.search(full):
        notes.append("full_description: word count needs spaces between words; density is unreliable here.")
    report = []
    for term in keywords:
        hits = count_term(term, full)
        n_words = max(1, len(term.split()))
        density = round(hits * n_words / total * 100, 2) if total else 0.0
        if density > 5:
            status = "stuffing risk (over 5%)"
        elif density > 3:
            status = "high (3-5%)"
        elif density >= 2:
            status = "on target (2-3%)"
        elif density >= 1:
            status = "light (1-2%)"
        else:
            status = "sparse (under 1%)"
        in_short = bool(count_term(term, fields.get("title", "") + " " + fields.get("short_description", "")))
        report.append({"keyword": term, "occurrences": hits, "density_pct": density, "status": status,
                       "in_first_3_sentences": bool(count_term(term, first)),
                       "in_title_or_short_description": in_short})
    return report


def print_check(result):
    print(f"Listing check ({result['platform']})")
    for name, info in result["lengths"].items():
        print(f"  {name:<18} {info['used']:>5}/{info['limit']} {info['unit']}")
    for title, key in (("Errors", "errors"), ("Warnings", "warnings")):
        if result[key]:
            print(f"\n{title}:")
            for item in result[key]:
                print(f"- {item}")
    if result["keywords"]:
        print("\nTarget keywords:")
        for row in result["keywords"]:
            if "density_pct" in row:
                print(f"- {row['keyword']}: {row['occurrences']}x, {row['density_pct']}% ({row['status']}); "
                      f"first 3 sentences: {'yes' if row['in_first_3_sentences'] else 'no'}; "
                      f"title or short description: {'yes' if row['in_title_or_short_description'] else 'no'}")
            else:
                print(f"- {row['keyword']}: {'in' if row['in_indexed_fields'] else 'NOT in'} "
                      "name, subtitle, or keyword field")
    if result["notes"]:
        print("\nNotes:")
        for item in result["notes"]:
            print(f"- {item}")


# --------------------------------------------------------- keyword-field


def build_keyword_field(name, subtitle, candidates, competitors, limit_bytes, keep_phrases, stopwords):
    indexed = set(words(name)) | set(words(subtitle))
    blocked = {c.lower() for c in competitors}
    included, skipped, seen = [], [], set()
    for phrase in candidates:
        if keep_phrases or NO_SPACE_SCRIPT.search(phrase):
            parts = [phrase.strip().lower()]
        else:
            parts = words(phrase)
        for term in parts:
            if term in seen:
                continue
            seen.add(term)
            if term in stopwords:
                skipped.append({"term": term, "reason": "stopword"})
                continue
            if term in indexed:
                skipped.append({"term": term, "reason": "already in name or subtitle"})
                continue
            if term in blocked or any(count_term(c, term) for c in blocked):
                skipped.append({"term": term, "reason": "competitor name"})
                continue
            trial = ",".join(included + [term])
            if len(trial.encode("utf-8")) > limit_bytes:
                skipped.append({"term": term, "reason": "did not fit"})
                continue
            included.append(term)
    field = ",".join(included)
    return {"keyword_field": field, "bytes_used": len(field.encode("utf-8")), "limit_bytes": limit_bytes,
            "included": included, "skipped": skipped}


def print_keyword_field(result):
    print(f"Keyword field ({result['bytes_used']}/{result['limit_bytes']} bytes):")
    print(result["keyword_field"])
    if result["skipped"]:
        print("\nSkipped:")
        for item in result["skipped"]:
            print(f"- {item['term']}: {item['reason']}")
    print("\nPlurals and other word forms are kept as given; drop them yourself if the singular ranks.")


# -------------------------------------------------------------- coverage


def app_text(app, include_description):
    keys = ["title", "name", "subtitle", "short_description"]
    if include_description:
        keys += ["description", "full_description"]
    return " ".join(str(app.get(k) or "") for k in keys)


def coverage(data, terms, stopwords, min_apps, include_description):
    explicit = bool(terms)
    comps = data.get("competitors") or []
    if not comps:
        fail("coverage input needs a non-empty 'competitors' list")
    texts = {str(c.get("app") or f"app {i + 1}"): app_text(c, include_description) for i, c in enumerate(comps)}
    yours = app_text(data.get("yours") or {}, include_description)
    if not terms:
        found = set()
        for text in texts.values():
            tokens = [w for w in words(text) if len(w) > 1]
            found.update(w for w in tokens if w not in stopwords)
            found.update(f"{a} {b}" for a, b in zip(tokens, tokens[1:])
                         if not (a in stopwords and b in stopwords))
        terms = sorted(found)
    rows = []
    for term in terms:
        users = [app for app, text in texts.items() if count_term(term, text)]
        if not explicit and len(users) < min_apps:
            continue
        pct = round(len(users) / len(texts) * 100)
        if pct >= 60:
            read = "category term: expected by searchers"
        elif pct >= 40:
            read = "common: worth targeting if relevant"
        else:
            read = "rare: differentiator or irrelevant"
        rows.append({"term": term, "apps": users, "coverage_pct": pct,
                     "in_yours": bool(count_term(term, yours)) if yours.strip() else None, "read": read})
    rows.sort(key=lambda r: (-r["coverage_pct"], r["term"]))
    missing = [r["term"] for r in rows if r["in_yours"] is False and r["coverage_pct"] >= 60]
    return {"competitors": list(texts), "terms": rows, "category_terms_missing_from_yours": missing}


def print_coverage(result):
    print(f"Keyword coverage across {len(result['competitors'])} competitors: {', '.join(result['competitors'])}")
    print(f"\n{'Term':<28}{'Apps':>5}{'Cover':>7}  {'Yours':<6} Read")
    for row in result["terms"]:
        yours = "-" if row["in_yours"] is None else ("yes" if row["in_yours"] else "no")
        print(f"{row['term'][:27]:<28}{len(row['apps']):>5}{row['coverage_pct']:>6}%  {yours:<6} {row['read']}")
    if result["category_terms_missing_from_yours"]:
        print("\nCategory terms missing from your metadata: " + ", ".join(result["category_terms_missing_from_yours"]))
    print("\nCoverage shows what competitors target, not search volume; check volume before you act on a gap.")


# ------------------------------------------------------------------ main


def main():
    parser = argparse.ArgumentParser(
        description="Check app store metadata, build an Apple keyword field, or measure competitor "
        "keyword coverage. Reads the files you pass; prints to stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command", metavar="{check,keyword-field,coverage}")
    sub.required = True

    p_check = sub.add_parser("check", help="validate a listing against store limits and rules")
    p_check.add_argument("--platform", choices=("apple", "google"), required=True)
    src = p_check.add_mutually_exclusive_group(required=True)
    src.add_argument("--input", help="listing JSON: field name to text (e.g. name, subtitle, keywords)")
    src.add_argument("--demo", action="store_true", help="check a built-in sample listing")
    p_check.add_argument("--keywords", default="", help="comma-separated target keywords to look for")
    p_check.add_argument("--competitors", default="", help="comma-separated competitor names to flag")
    p_check.add_argument("--json", action="store_true", help="print JSON")

    p_field = sub.add_parser("keyword-field", help="build the Apple keyword field from ranked terms")
    p_field.add_argument("--name", default="", help="app name (its words are skipped)")
    p_field.add_argument("--subtitle", default="", help="subtitle (its words are skipped)")
    cands = p_field.add_mutually_exclusive_group(required=True)
    cands.add_argument("--candidates", help="comma-separated terms, highest priority first")
    cands.add_argument("--candidates-file", help="file with one term per line or comma-separated, priority order")
    p_field.add_argument("--competitors", default="", help="comma-separated competitor names to exclude")
    p_field.add_argument("--limit-bytes", type=int, default=100, help="field size in bytes (default 100)")
    p_field.add_argument("--keep-phrases", action="store_true", help="keep multi-word terms whole")
    p_field.add_argument("--stopwords", default="", help="'en' for a small built-in English list, or a file path")
    p_field.add_argument("--json", action="store_true", help="print JSON")

    p_cov = sub.add_parser("coverage", help="count which terms competitor metadata uses")
    csrc = p_cov.add_mutually_exclusive_group(required=True)
    csrc.add_argument("--input", help='JSON: {"yours": {...}, "competitors": [{"app": ..., "title": ..., "subtitle": ...}]}')
    csrc.add_argument("--demo", action="store_true", help="use built-in sample data")
    p_cov.add_argument("--terms", default="", help="comma-separated terms to check (default: derive from titles)")
    p_cov.add_argument("--stopwords", default="", help="'en' for a small built-in English list, or a file path")
    p_cov.add_argument("--min-apps", type=int, default=2, help="minimum competitors using a derived term (default 2)")
    p_cov.add_argument("--include-description", action="store_true", help="also scan descriptions")
    p_cov.add_argument("--json", action="store_true", help="print JSON")

    args = parser.parse_args()

    if args.command == "check":
        listing = DEMO_LISTING[args.platform] if args.demo else load_json(args.input)
        result = check_listing(args.platform, listing, split_terms(args.keywords), split_terms(args.competitors))
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_check(result)
        sys.exit(1 if result["errors"] else 0)

    if args.command == "keyword-field":
        if args.candidates_file:
            try:
                with open(args.candidates_file, encoding="utf-8") as handle:
                    candidates = split_terms(handle.read())
            except FileNotFoundError:
                fail(f"file not found: {args.candidates_file}")
        else:
            candidates = split_terms(args.candidates)
        result = build_keyword_field(args.name, args.subtitle, candidates, split_terms(args.competitors),
                                     args.limit_bytes, args.keep_phrases, load_stopwords(args.stopwords))
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_keyword_field(result)
        return

    data = DEMO_COVERAGE if args.demo else load_json(args.input)
    if not isinstance(data, dict):
        fail("coverage input must be a JSON object")
    result = coverage(data, split_terms(args.terms), load_stopwords(args.stopwords),
                      args.min_apps, args.include_description)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_coverage(result)


if __name__ == "__main__":
    main()
