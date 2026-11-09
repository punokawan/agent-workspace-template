#!/usr/bin/env python3
"""Score a product marketing context file for completeness (0-100).

Reads one Markdown file that follows the product-marketing template and
prints a report. Standard library only. No network access, no writes.

A field counts as filled only when it holds real content: template
placeholders such as [date], empty table rows, bare bullets, and labels
with nothing after the colon do not count. Optional sections the
product does not use (Personas, Content & SEO, Paid Ads) are skipped
when they are absent or empty.

Adapted from context_validator.py in alirezarezvani/claude-skills
(marketing-skill/skills/marketing-context, MIT).
"""

import argparse
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

# (display name, heading aliases, kind, weight)
#   required    always scored; listed when missing
#   optional    always scored; listed when missing
#   conditional scored only when present with at least one filled field
#   info        reported, never scored
SECTIONS = [
    ("Product Overview", ("product overview",), "required", 10),
    ("Target Audience", ("target audience",), "required", 10),
    ("Languages & Markets", ("languages and markets", "languages", "language and markets"), "required", 6),
    ("Personas", ("personas",), "conditional", 4),
    ("Problems & Pain Points", ("problems and pain points", "problems", "pain points"), "required", 9),
    ("Competitive Landscape", ("competitive landscape", "competitors"), "required", 9),
    ("Differentiation", ("differentiation",), "required", 9),
    ("Objections", ("objections",), "optional", 5),
    ("Switching Dynamics", ("switching dynamics",), "optional", 5),
    ("Customer Language", ("customer language",), "required", 10),
    ("Brand Voice", ("brand voice",), "required", 8),
    ("Proof Points", ("proof points",), "required", 7),
    ("Goals", ("goals",), "required", 4),
    ("Content & SEO", ("content and seo",), "conditional", 3),
    ("Paid Ads", ("paid ads",), "conditional", 3),
    ("Learnings", ("learnings",), "info", 0),
    ("Changelog", ("changelog",), "info", 0),
]

# Field labels the template defines per section (lowercase prefixes).
# A label that is absent from the file counts as an unfilled field.
# "(body)" is content that sits under the heading before any label,
# such as the Personas table.
EXPECTED_FIELDS = {
    "Product Overview": ("one-liner", "what it does", "product category", "product type", "business model"),
    "Target Audience": ("target companies", "decision-makers", "primary use case", "jobs to be done", "use cases"),
    "Languages & Markets": ("primary language", "languages", "target markets"),
    "Personas": ("(body)",),
    "Problems & Pain Points": ("core problem", "why alternatives fall short", "what it costs them", "emotional tension"),
    "Competitive Landscape": ("direct", "secondary", "indirect"),
    "Differentiation": ("key differentiators", "how we do it differently", "why that's better", "why customers choose us"),
    "Objections": ("(body)", "anti-persona"),
    "Switching Dynamics": ("push", "pull", "habit", "anxiety"),
    "Customer Language": ("how they describe the problem", "how they describe us", "words to use", "words to avoid", "glossary"),
    "Brand Voice": ("(body)", "tone by context", "terms we own", "never use", "style rules"),
    "Proof Points": ("metrics", "customers", "testimonials", "value themes"),
    "Goals": ("business goal", "conversion action", "current metrics"),
    "Content & SEO": ("keyword clusters", "key pages", "exemplary pieces", "length and format"),
    "Paid Ads": (
        "target cpa", "hard floor", "monthly budget", "conversions that count",
        "known tracking weaknesses", "good lead", "campaigns",
    ),
}

# Values the template ships pre-filled; they are not the user's content.
TEMPLATE_DEFAULTS = {
    "read, compare, flag, draft, recommend",
    "change budgets or bids, pause or launch, edit tracking, publish ads",
}

PLACEHOLDER_RE = re.compile(r"\[[^\]]*\](?!\()")
CHECKBOX_RE = re.compile(r"^\[[ xX]\]\s*")
LABEL_RE = re.compile(r"^\*\*([^*]+?)\*\*\s*:?\s*(.*)$")
BULLET_RE = re.compile(r"^(?:[-*+]|\d+[.)])\s+(.*)$")
TABLE_RE = re.compile(r"^\|.*\|\s*$")
SEPARATOR_RE = re.compile(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?\s*$")
ITALIC_NOTE_RE = re.compile(r"^(\*[^*].*\*|_[^_].*_)$")
QUOTE_RE = re.compile(r"\"[^\"\[\]]{3,}\"|“[^”]{3,}”|„[^“”]{3,}[“”]|«[^»]{3,}»|「[^」]{2,}」|『[^』]{2,}』")
ISO_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})")

SAMPLE = """# Product Marketing Context

**Document version:** v3
**Last updated:** 2026-09-02

## Product Overview
**One-liner:** Invoicing that chases late payments for freelancers.
**What it does:** Sends invoices, reminds late clients at 3, 7, and 14 days, and pays out within 2 days.
**Product category:** Invoicing software for freelancers
**Product type:** SaaS
**Business model:** Free plan; Pro at 12 per month

## Target Audience
**Target companies:** Solo freelancers and two-person studios in design and development
**Decision-makers:** The freelancer
**Primary use case:** Getting paid on time without awkward follow-ups
**Jobs to be done:**
- Get paid for finished work without chasing
**Use cases:**
- A designer with five retainer clients on net-30 terms

## Languages & Markets
**Primary language and locale:** en-CA
**Languages:**
| Language / locale | Used for | Tone and form of address |
|-------------------|----------|--------------------------|
| en-CA | Site, app, support | Plain, informal |
| fr-CA | Site and support for Quebec | Plain; formal "vous" in support replies |
**Target markets / regions:**
| Market or region | Priority | What differs (currency, pricing, regulation, channels, proof) |
|------------------|----------|----------------------------------------------------------------|
| Canada | 1 | CAD pricing, sales tax per province |

## Problems & Pain Points
**Core problem:** Clients pay late and freelancers hate chasing them.
**Why alternatives fall short:**
- Spreadsheets and email reminders depend on remembering to send them
**What it costs them:** About 4 hours a month chasing, and cash-flow gaps
**Emotional tension:** Fear of sounding pushy with a client they need

## Competitive Landscape
**Direct:** Generic invoicing apps — reminders are manual or sound robotic
**Secondary:** Accounting suites — built for accountants, too heavy for one person
**Indirect:** Email and a spreadsheet — nothing happens unless you remember

## Differentiation
**Key differentiators:**
- Reminders sent from the freelancer's own address, in their words
**Why customers choose us:** They get paid faster without writing a single reminder

## Customer Language
**How they describe the problem:**
- "I feel like a debt collector"
**How they describe us:**
- "It nags my clients so I don't have to"
**Words to use:** get paid, chase, late invoice
**Words to avoid:** accounts receivable, dunning

## Brand Voice
| Attribute | Means | Doesn't mean | Example line |
|-----------|-------|--------------|--------------|
| Plain-spoken | Short words, numbers over adjectives | Vague | "You'll get paid in 2 days instead of 30." |
**Terms we own:** Payout
**Never use (and why):** "Seamless" (we have edge cases and say so)

## Proof Points
**Metrics:** Median payment time fell from 34 to 9 days for 1,200 users
**Customers:** Independent designers and developers

## Goals
**Business goal:** Grow Pro subscriptions
**Conversion action:** Start the free plan
**Current metrics:** 3.1% visitor-to-signup

## Changelog
- v3 (2026-09-02) — Added fr-CA for Quebec support.
- v2 (2026-06-10) — Reworded the one-liner after 6 customer interviews.
- v1 (2026-03-01) — Initial context.
"""


def normalize_heading(text):
    t = text.lower()
    t = re.sub(r"\(.*?\)", " ", t)
    t = t.replace("&", " and ")
    t = re.sub(r"[^a-z0-9 -]+", " ", t)
    return re.sub(r"\s+", " ", t).strip()


def match_section(heading):
    norm = normalize_heading(heading)
    for name, aliases, kind, weight in SECTIONS:
        for alias in aliases:
            if norm == alias or norm.startswith(alias + " "):
                return name
    return None


def is_filled(value):
    if not value:
        return False
    value = CHECKBOX_RE.sub("", value.strip())
    if PLACEHOLDER_RE.search(value):
        return False
    norm = re.sub(r"\s+", " ", value.strip().strip("*_ ").lower())
    if norm in TEMPLATE_DEFAULTS:
        return False
    rest = re.sub(r"[\s|*_>\"'`“”‘’«»„:;,.\-–—]+", "", value)
    return len(rest) >= 2


def split_sections(text):
    preamble, sections, current, in_code = [], [], None, False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code and re.match(r"^##\s+\S", line) and not line.startswith("###"):
            current = (line[2:].strip(), [])
            sections.append(current)
        elif current is None:
            preamble.append(line)
        else:
            current[1].append(line)
    return preamble, sections


def parse_fields(lines):
    """Group a section's lines into fields; return a list of dicts."""
    fields = []
    current = None
    stripped_lines = [ln.strip() for ln in lines]

    def attach(value):
        nonlocal current
        if current is None:
            current = {"label": "(body)", "values": []}
            fields.append(current)
        current["values"].append(value)

    for i, line in enumerate(stripped_lines):
        if not line or line.startswith("#") or ITALIC_NOTE_RE.match(line):
            continue
        label = LABEL_RE.match(line)
        if label:
            current = {"label": label.group(1).strip().rstrip(":").strip(), "values": [label.group(2)]}
            fields.append(current)
            continue
        if TABLE_RE.match(line):
            if SEPARATOR_RE.match(line):
                continue
            nxt = stripped_lines[i + 1] if i + 1 < len(stripped_lines) else ""
            if SEPARATOR_RE.match(nxt):
                continue  # header row
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            row = " | ".join(cells)
            attach("" if PLACEHOLDER_RE.search(row) else " ".join(c for c in cells if c))
            continue
        bullet = BULLET_RE.match(line)
        if bullet:
            value = CHECKBOX_RE.sub("", bullet.group(1).strip())
            labelled = re.match(r"^([^:\"“]{1,60}):\s*(.*)$", value)
            attach(labelled.group(2) if labelled else value)
            continue
        if line.startswith(">"):
            attach(line.lstrip("> ").strip())
            continue
        attach(line)
    for field in fields:
        field["filled"] = any(is_filled(v) for v in field["values"])
        field["text"] = " ".join(v for v in field["values"] if is_filled(v))
    return fields


def count_fields(name, fields):
    """Return (filled, total) for a section, counting absent template labels as unfilled."""
    expected = sorted(EXPECTED_FIELDS.get(name, ()), key=len, reverse=True)
    matched = {label: False for label in expected}
    extra_total = extra_filled = 0
    for field in fields:
        label = field["label"].lower()
        hit = next((e for e in expected if label.startswith(e)), None)
        if hit:
            matched[hit] = matched[hit] or field["filled"]
        else:
            extra_total += 1
            extra_filled += 1 if field["filled"] else 0
    return sum(matched.values()) + extra_filled, len(expected) + extra_total


def find_meta(text, label):
    for line in text.splitlines():
        if re.search(label, line, re.IGNORECASE):
            return line
    return None


def validate(text, today=None, max_age_days=180):
    today = today or date.today()
    preamble, raw_sections = split_sections(text)
    found, unrecognized = {}, []
    for heading, lines in raw_sections:
        name = match_section(heading)
        if name is None:
            unrecognized.append(heading)
        elif name not in found:
            found[name] = parse_fields(lines)

    report = {
        "score": 0,
        "label": "",
        "sections": {},
        "missing_required": [],
        "missing_optional": [],
        "skipped": [],
        "unrecognized_sections": unrecognized,
        "warnings": [],
    }
    earned = total = 0.0
    for name, aliases, kind, weight in SECTIONS:
        fields = found.get(name)
        if fields is None:
            status, completeness, filled, count = "missing", 0.0, 0, 0
        else:
            if kind == "info":
                filled, count = sum(1 for f in fields if f["filled"]), len(fields)
            else:
                filled, count = count_fields(name, fields)
            completeness = filled / count if count else 0.0
            status = "complete" if completeness >= 0.75 else ("partial" if filled else "empty")
        entry = {"status": status, "filled_fields": filled, "fields": count, "kind": kind}
        if kind == "info":
            report["sections"][name] = entry
            continue
        if kind == "conditional" and filled == 0:
            entry["status"] = "skipped"
            report["skipped"].append(name)
            report["sections"][name] = entry
            continue
        if status == "missing":
            (report["missing_required"] if kind == "required" else report["missing_optional"]).append(name)
        entry["score"] = round(weight * completeness, 1)
        entry["max_score"] = weight
        earned += weight * completeness
        total += weight
        report["sections"][name] = entry

    report["score"] = round(earned / total * 100) if total else 0
    report["label"] = (
        "strong" if report["score"] >= 85
        else "usable" if report["score"] >= 70
        else "incomplete: fill the gaps before relying on it"
    )

    warnings = report["warnings"]
    lang = found.get("Languages & Markets")
    primary = [f for f in (lang or []) if f["label"].lower().startswith("primary language")]
    if not primary or not any(f["filled"] for f in primary):
        warnings.append("No primary language recorded: drafting skills must ask which language to write in.")
    customer = found.get("Customer Language")
    if customer is not None:
        quotes = " ".join(f["text"] for f in customer)
        if not QUOTE_RE.search(quotes):
            warnings.append("No verbatim customer quotes in Customer Language: copy will sound generic.")
    proof = found.get("Proof Points")
    if proof is not None:
        proof_text = " ".join(f["text"] for f in proof).strip()
        if proof_text and not re.search(r"\d", proof_text):
            warnings.append("Proof Points has no numbers: add metrics, counts, or dated results.")
    if not find_meta(text, r"document version"):
        warnings.append("No 'Document version' line.")
    changelog = found.get("Changelog")
    if not changelog or not any(f["filled"] for f in changelog):
        warnings.append("No Changelog entries.")
    updated_line = find_meta(text, r"last updated")
    if not updated_line:
        warnings.append("No 'Last updated' line.")
    else:
        match = ISO_DATE_RE.search(updated_line)
        if not match:
            warnings.append("'Last updated' has no ISO date (YYYY-MM-DD).")
        else:
            try:
                updated = datetime.strptime(match.group(1), "%Y-%m-%d").date()
                age = (today - updated).days
                if age > max_age_days:
                    warnings.append(
                        f"Last updated {updated.isoformat()} is {age} days old: review positioning "
                        f"(threshold {max_age_days} days)."
                    )
            except ValueError:
                warnings.append(f"'Last updated' date {match.group(1)} is not a valid date.")
    if unrecognized:
        warnings.append("Sections not scored (heading not in the template): " + ", ".join(unrecognized))
    return report


def print_report(source, report):
    print(f"Product marketing context: {source}")
    print(f"Score: {report['score']}/100 ({report['label']})")
    print()
    print(f"{'Section':<24}{'Status':<11}{'Filled':<9}Score")
    for name, entry in report["sections"].items():
        if entry["kind"] == "info":
            score = "-"
        elif entry["status"] == "skipped":
            score = "not used"
        else:
            score = f"{entry['score']:g}/{entry['max_score']}"
        filled = f"{entry['filled_fields']}/{entry['fields']}" if entry["fields"] else "-"
        print(f"{name:<24}{entry['status']:<11}{filled:<9}{score}")
    for title, key in (
        ("Missing required sections", "missing_required"),
        ("Missing optional sections", "missing_optional"),
        ("Skipped (not used)", "skipped"),
        ("Warnings", "warnings"),
    ):
        if report[key]:
            print(f"\n{title}:")
            for item in report[key]:
                print(f"- {item}")


def main():
    parser = argparse.ArgumentParser(
        description="Score a product marketing context file for completeness (0-100). "
        "Reads the file only; prints a report to stdout."
    )
    parser.add_argument("file", nargs="?", help="path to the context Markdown file")
    parser.add_argument("--json", action="store_true", help="print the result as JSON only")
    parser.add_argument("--demo", action="store_true", help="score a built-in sample instead of a file")
    parser.add_argument(
        "--max-age-days", type=int, default=180,
        help="warn when 'Last updated' is older than this many days (default 180)",
    )
    parser.add_argument("--today", help="date to measure age against, YYYY-MM-DD (default: today)")
    args = parser.parse_args()

    if bool(args.file) == bool(args.demo):
        parser.error("pass a context file path, or --demo")
    today = None
    if args.today:
        try:
            today = datetime.strptime(args.today, "%Y-%m-%d").date()
        except ValueError:
            parser.error("--today must be YYYY-MM-DD")

    if args.demo:
        source, text = "built-in sample", SAMPLE
    else:
        path = Path(args.file)
        if not path.is_file():
            print(f"Error: file not found: {path}", file=sys.stderr)
            sys.exit(1)
        source = str(path)
        text = path.read_text(encoding="utf-8")

    report = validate(text, today=today, max_age_days=args.max_age_days)
    if args.json:
        print(json.dumps({"file": source, **report}, indent=2, ensure_ascii=False))
    else:
        print_report(source, report)


if __name__ == "__main__":
    main()
