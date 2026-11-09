#!/usr/bin/env python3
"""
ad_copy_validator.py: check ad copy against platform character limits, common
rejection triggers, and the AI tells this skill bans, before anything ships.

Per field: hard maximum (FAIL), recommended length that truncates in preview
(REVIEW), ALL CAPS words, repeated punctuation, platform names, risky phrases,
claims that need substantiation, and AI tells (em dashes, stock phrases,
"it's not X, it's Y" reveals, stacked negations). Google search ads also get
asset counts, duplicate headlines, and exclamation marks in headlines.

Status per ad: FAIL (a limit or count is broken), REVIEW (a person must look),
PASS. A REVIEW flag is a prompt to check, not a rejection: the platform's policy
pages and the skill's copy rules win where they disagree with this script.

Usage:
  python3 ad_copy_validator.py --file ads.json [--json]
  cat ads.json | python3 ad_copy_validator.py --json
  python3 ad_copy_validator.py            # demo ads

Input: one ad object or an array of them.
  google_rsa      headlines[], descriptions[], path1, path2
  google_display  headlines[], long_headline, descriptions[], business_name
  meta_feed       primary_text, headline, description
  linkedin        intro_text, headline, description
  x               text, card_headline, card_description   (URLs count as 23)
  tiktok          ad_text, display_name
  Optional on any ad: "name", "allow_caps": ["HIPAA"], "review_terms": ["CompetitorCo"]

Character counts are Python string lengths; some platforms count an emoji as 2.
Stdlib only. Reads the input file or standard input; writes nothing.
"""

import argparse
import json
import re
import sys

PLATFORMS = {
    "google_rsa": {"name": "Google Ads responsive search ad", "fields": {
        "headlines": {"max": 30, "list": True, "min_count": 3, "max_count": 15},
        "descriptions": {"max": 90, "list": True, "min_count": 2, "max_count": 4},
        "path1": {"max": 15}, "path2": {"max": 15}}},
    "google_display": {"name": "Google Ads responsive display ad", "fields": {
        "headlines": {"max": 30, "list": True, "min_count": 1, "max_count": 5},
        "long_headline": {"max": 90},
        "descriptions": {"max": 90, "list": True, "min_count": 1, "max_count": 5},
        "business_name": {"max": 25}}},
    "meta_feed": {"name": "Meta feed ad", "fields": {
        "primary_text": {"rec": 125, "max": 2200},
        "headline": {"rec": 40, "max": 255},
        "description": {"rec": 30, "max": 255}}},
    "linkedin": {"name": "LinkedIn single image ad", "fields": {
        "intro_text": {"rec": 150, "max": 600},
        "headline": {"rec": 70, "max": 200},
        "description": {"rec": 100, "max": 300}}},
    "x": {"name": "X promoted post", "fields": {
        "text": {"max": 280, "urls_count_as": 23},
        "card_headline": {"max": 70},
        "card_description": {"max": 200}}},
    "tiktok": {"name": "TikTok in-feed ad", "fields": {
        "ad_text": {"rec": 80, "max": 100},
        "display_name": {"max": 40}}},
}

PLATFORM_ALIASES = {"twitter": "x", "twitter_x": "x", "meta": "meta_feed",
                    "facebook": "meta_feed", "instagram": "meta_feed",
                    "google_search": "google_rsa", "rsa": "google_rsa"}
FIELD_ALIASES = {"text": ["primary_text"], "ad_text": ["primary_text", "text"],
                 "intro_text": ["primary_text"], "headlines": ["headline"],
                 "descriptions": ["description"]}

PLATFORM_NAMES = ["facebook", "instagram", "meta", "google", "youtube", "tiktok",
                  "twitter", "linkedin", "snapchat", "whatsapp", "pinterest"]
RISKY_PHRASES = ["click here", "act now", "limited time offer", "guaranteed", "100% free",
                 "best in class", "world's best", "#1 rated", "number one", "risk-free"]
CLAIM_PATTERNS = [
    (r"\b(make|earn)\s+\$?\d[\d,.]*\s*k?\s*(per|a|/)\s*(day|week|month)\b", "income claim"),
    (r"\b\d{2,}\s*%\s*(return|roi|profit|gains?)\b", "investment return claim"),
    (r"\b(cures?|cured|heals?|healing)\b", "health claim"),
    (r"\blose\s+\d+\s*(pounds|lbs?|kg|kilos?)\b", "weight-loss claim"),
]
STOCK_PHRASES = ["say goodbye to", "reimagined", "unlock the power", "take it to the next level",
                 "here's the thing", "stop scrolling", "game-changer", "game changer",
                 "get started today", "join thousands"]
CONTRAST_REVEAL = re.compile(r"\b(it'?s|this is|that'?s) not\b[^.!?\n]{1,60}?[,;.:]\s*(it'?s|this is|that'?s)\b",
                             re.IGNORECASE)
NOT_BECAUSE = re.compile(r"\bnot because\b[^.!?\n]{1,60}[.;]\s*because\b", re.IGNORECASE)
STACKED_NO = re.compile(r"(\bno\b[^.!?\n]{1,30}[.!?]\s*){3,}", re.IGNORECASE)
URL = re.compile(r"https?://\S+")
REPEATED_PUNCT = re.compile(r"[!?]{2,}|\.{3,}|…")
EM_DASH = "—"


class InputError(ValueError):
    pass


def text_length(text, urls_count_as=None):
    if urls_count_as:
        text = URL.sub("x" * urls_count_as, text)
    return len(text.strip())


def scan(text, platform, field, ad):
    """Content checks shared by every field. Returns (level, message) pairs."""
    issues = []
    lowered = text.lower()
    allow = {a.upper() for a in ad.get("allow_caps", [])}
    caps = [w for w in re.findall(r"[A-Za-z]{4,}", text) if w.isupper() and w not in allow]
    if caps:
        issues.append(("REVIEW", "ALL CAPS: " + ", ".join(sorted(set(caps)))))
    punct = REPEATED_PUNCT.findall(text)
    if punct:
        issues.append(("REVIEW", "repeated punctuation: " + " ".join(sorted(set(punct)))))
    if platform == "google_rsa" and field == "headlines" and "!" in text:
        issues.append(("REVIEW", "exclamation mark in a headline (Google disapproves these)"))
    names = [n for n in PLATFORM_NAMES if re.search(r"\b" + re.escape(n) + r"\b", lowered)]
    names += [t for t in ad.get("review_terms", []) if t.lower() in lowered]
    if names:
        issues.append(("REVIEW", "platform or trademark name: " + ", ".join(names)))
    phrases = [p for p in RISKY_PHRASES if p in lowered]
    if phrases:
        issues.append(("REVIEW", "risky phrase: " + ", ".join(phrases)))
    for pattern, label in CLAIM_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            issues.append(("REVIEW", f"{label}: needs substantiation and is restricted on most platforms"))
    if EM_DASH in text:
        issues.append(("REVIEW", "em dash (AI tell; rewrite the sentence)"))
    stock = [p for p in STOCK_PHRASES if p in lowered]
    if stock:
        issues.append(("REVIEW", "stock phrase (AI tell): " + ", ".join(stock)))
    if CONTRAST_REVEAL.search(text) or NOT_BECAUSE.search(text):
        issues.append(("REVIEW", "contrast reveal (AI tell): state the point directly"))
    if STACKED_NO.search(text):
        issues.append(("REVIEW", "stacked negations: keep the one that matters, use the space for a fact"))
    return issues


def field_values(ad, field, spec):
    value = ad.get(field)
    if value is None:
        for alias in FIELD_ALIASES.get(field, []):
            if ad.get(alias) is not None:
                value = ad.get(alias)
                break
    if value is None:
        return None
    if spec.get("list"):
        if isinstance(value, str):
            value = [value]
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            raise InputError(f"'{field}' must be a list of strings")
        return value
    if not isinstance(value, str):
        raise InputError(f"'{field}' must be a string")
    return [value]


def validate(ad, index):
    if not isinstance(ad, dict):
        raise InputError(f"ad #{index + 1} must be an object")
    key = str(ad.get("platform", "")).strip().lower()
    key = PLATFORM_ALIASES.get(key, key)
    if key not in PLATFORMS:
        raise InputError(f"ad #{index + 1}: unknown platform {ad.get('platform')!r}; "
                         "use " + ", ".join(sorted(PLATFORMS)))
    spec = PLATFORMS[key]
    lines, problems = [], []
    for field, fspec in spec["fields"].items():
        values = field_values(ad, field, fspec)
        if values is None:
            if fspec.get("min_count"):
                problems.append(("FAIL", f"{field}: none given (minimum {fspec['min_count']})"))
            continue
        if fspec.get("list"):
            n = len(values)
            if fspec.get("min_count") and n < fspec["min_count"]:
                problems.append(("FAIL", f"{field}: {n} given, minimum {fspec['min_count']}"))
            if fspec.get("max_count") and n > fspec["max_count"]:
                problems.append(("FAIL", f"{field}: {n} given, maximum {fspec['max_count']}"))
            seen = {}
            for v in values:
                seen.setdefault(v.strip().lower(), 0)
                seen[v.strip().lower()] += 1
            dupes = [k for k, c in seen.items() if c > 1]
            if dupes:
                problems.append(("FAIL", f"{field}: duplicate entries: " + "; ".join(dupes)))
        for i, text in enumerate(values, 1):
            label = f"{field} {i}" if fspec.get("list") else field
            length = text_length(text, fspec.get("urls_count_as"))
            limit = fspec["max"]
            mark = "ok"
            if length > limit:
                mark = "OVER"
                problems.append(("FAIL", f"{label}: {length} characters, maximum {limit}"))
            elif fspec.get("rec") and length > fspec["rec"]:
                mark = "long"
                problems.append(("REVIEW", f"{label}: {length} characters, truncates after "
                                           f"about {fspec['rec']} in preview"))
            shown = f"{length}/{fspec['rec']} rec, {limit} max" if fspec.get("rec") else f"{length}/{limit}"
            lines.append(f"{label}: \"{text}\" ({shown}) {mark}")
            for level, message in scan(text, key, field, ad):
                problems.append((level, f"{label}: {message}"))
    status = "PASS"
    if any(level == "REVIEW" for level, _ in problems):
        status = "REVIEW"
    if any(level == "FAIL" for level, _ in problems):
        status = "FAIL"
    return {"name": str(ad.get("name", f"ad {index + 1}")), "platform": key,
            "platform_name": spec["name"], "status": status,
            "fields": lines, "issues": [{"level": l, "message": m} for l, m in problems]}


DEMO = [
    {"name": "Reporting RSA", "platform": "google_rsa",
     "headlines": ["Cut Reporting Time by 80%", "Automated Reports, Zero Effort",
                   "Try Free for 14 Days", "GUARANTEED Results Now!!!",
                   "Try Free for 14 Days", "Reports Your Team Actually Reads"],
     "descriptions": ["Connect your tools once and get the weekly report every Monday. Free trial.",
                      "Say goodbye to spreadsheets — it's not a dashboard, it's your new analyst."],
     "path1": "reports", "path2": "free-trial"},
    {"name": "Meta prospecting", "platform": "meta_feed",
     "primary_text": "Your team ships every week, but nobody can see which work moved revenue. "
                     "[Product] joins your tools and shows the impact in one view, updated daily. "
                     "Start a free trial.",
     "headline": "See which work moved revenue"},
    {"name": "X launch post", "platform": "x",
     "text": "Monday reports, done before you log in. Connect your tools once and the "
             "weekly report writes itself. Free trial: https://example.com/start-your-trial"},
]


def main():
    parser = argparse.ArgumentParser(
        description="Check ad copy against platform limits, rejection triggers and AI tells.",
        epilog="No input runs demo ads. Reads only --file or standard input; writes nothing.")
    parser.add_argument("--file", help="JSON file with one ad object or an array of ads")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    try:
        data = None
        if args.file:
            try:
                with open(args.file, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
            except OSError as exc:
                raise InputError(f"cannot read {args.file}: {exc.strerror}")
            except json.JSONDecodeError as exc:
                raise InputError(f"invalid JSON in {args.file}: {exc}")
        elif not sys.stdin.isatty():
            raw = sys.stdin.read().strip()
            if raw:
                try:
                    data = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise InputError(f"invalid JSON on standard input: {exc}")
        if data is None:
            data = DEMO
            if not args.json:
                print("No input given: running the demo ads.\n")
        ads = data if isinstance(data, list) else [data]
        results = [validate(ad, i) for i, ad in enumerate(ads)]
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        return
    for r in results:
        print(f"{r['name']} | {r['platform_name']} | {r['status']}")
        for line in r["fields"]:
            print(f"  {line}")
        for issue in r["issues"]:
            print(f"  {issue['level']}: {issue['message']}")
        print()
    counts = {s: sum(1 for r in results if r["status"] == s) for s in ("PASS", "REVIEW", "FAIL")}
    print(f"SUMMARY: {len(results)} ads: {counts['PASS']} pass, {counts['REVIEW']} review, "
          f"{counts['FAIL']} fail")


if __name__ == "__main__":
    main()
