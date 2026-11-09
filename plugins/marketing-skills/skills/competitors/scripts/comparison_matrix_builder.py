#!/usr/bin/env python3
"""Build a feature comparison matrix for competitor comparison pages.

Reads a JSON file of features (your status and each competitor's status)
and prints one of:
  default     a plain-text internal summary: wins, ties, losses per
              competitor, your advantages and gaps, evidence warnings
  --markdown  the comparison table for a vs or alternatives page, with a
              status key and an "as of" line
  --json      the full analysis for other tools
Standard library only. No network access, no writes.

Evidence rules (from the competitors skill):
  - A competitor "no" counts only with a source (their docs or a trial).
    Without one it shows as "Not listed" and is left out of the counts.
  - "unknown" shows as "Not verified" and is left out of the counts.
  - "planned" is not shipped and scores like "no".

Input JSON:
{
  "your_product": "YourProduct",
  "as_of": "2026-03-14",                 (optional default date for competitor facts)
  "features": [
    {
      "name": "SSO / SAML",
      "category": "Security",             (optional, default "General")
      "weight": 3,                         (optional, default 1)
      "your_status": "full",              (full | partial | no | planned)
      "competitors": {
        "CompetitorA": "partial",
        "CompetitorB": {"status": "no", "source": "docs.example.com/sso", "as_of": "2026-03-14"},
        "CompetitorC": "unknown"
      },
      "notes": "Enterprise tier only"     (optional)
    }
  ]
}
Statuses: full (alias yes), partial, no, planned, unknown.

Adapted from comparison_matrix_builder.py in alirezarezvani/claude-skills
(marketing-skill/skills/competitor-alternatives, MIT).
"""

import argparse
import json
import sys

SCORE = {"full": 2, "partial": 1, "no": 0, "planned": 0}
ALIASES = {"yes": "full", "full": "full", "partial": "partial", "no": "no", "planned": "planned", "unknown": "unknown"}
LABEL = {
    "full": "Yes",
    "partial": "Partial",
    "no": "No",
    "planned": "Planned",
    "not_listed": "Not listed",
    "unknown": "Not verified",
}
KEY_TEXT = {
    "full": "available",
    "partial": "limited, or only on some plans",
    "no": "confirmed unavailable (docs or trial)",
    "planned": "announced, not shipped",
    "not_listed": "not found on their public pages",
    "unknown": "not checked yet",
}

DEMO_DATA = {
    "your_product": "SwiftBase",
    "as_of": "2026-03-14",
    "features": [
        {"name": "SSO / SAML", "category": "Security", "weight": 3, "your_status": "full",
         "competitors": {"AcmeSaaS": {"status": "no", "source": "acmesaas docs: security page"},
                         "ProStack": "partial"}, "notes": "All plans"},
        {"name": "2FA / MFA", "category": "Security", "weight": 3, "your_status": "full",
         "competitors": {"AcmeSaaS": "full", "ProStack": "full"}},
        {"name": "SOC 2 Type II", "category": "Security", "weight": 3, "your_status": "planned",
         "competitors": {"AcmeSaaS": "full", "ProStack": "no"}, "notes": "Audit in progress"},
        {"name": "Role-based access", "category": "Security", "weight": 2, "your_status": "full",
         "competitors": {"AcmeSaaS": "partial", "ProStack": "full"}},
        {"name": "REST API", "category": "Integrations", "weight": 3, "your_status": "full",
         "competitors": {"AcmeSaaS": "full", "ProStack": "full"}},
        {"name": "Webhooks", "category": "Integrations", "weight": 2, "your_status": "full",
         "competitors": {"AcmeSaaS": "full", "ProStack": "unknown"}},
        {"name": "Zapier integration", "category": "Integrations", "weight": 2, "your_status": "partial",
         "competitors": {"AcmeSaaS": "full", "ProStack": "full"}, "notes": "10 zaps"},
        {"name": "Custom domain", "category": "Branding", "weight": 2, "your_status": "full",
         "competitors": {"AcmeSaaS": "partial", "ProStack": "full"}},
        {"name": "Dedicated success manager", "category": "Support", "weight": 2, "your_status": "no",
         "competitors": {"AcmeSaaS": "full", "ProStack": "full"}, "notes": "Enterprise only"},
    ],
}


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def read_status(raw, default_as_of, warnings, where):
    """Return (status, source, as_of) for one competitor cell."""
    source, as_of = None, default_as_of
    if isinstance(raw, dict):
        source = raw.get("source") or None
        as_of = raw.get("as_of") or default_as_of
        raw = raw.get("status")
    value = str(raw if raw is not None else "unknown").strip().lower()
    status = ALIASES.get(value)
    if status is None:
        warnings.append(f"{where}: unrecognized status '{raw}', treated as unknown.")
        status = "unknown"
    return status, source, as_of


def build_matrix(data):
    if not isinstance(data, dict) or not data.get("features"):
        fail("input needs a non-empty 'features' list")
    your = data.get("your_product") or "Your product"
    default_as_of = data.get("as_of")
    warnings = []

    competitors = []
    for feature in data["features"]:
        for name in (feature.get("competitors") or {}):
            if name not in competitors:
                competitors.append(name)

    rows, sourced, total_facts, dates = [], 0, 0, []
    for feature in data["features"]:
        fname = feature.get("name") or "(unnamed feature)"
        weight = feature.get("weight", 1)
        if not isinstance(weight, (int, float)) or weight <= 0:
            warnings.append(f"{fname}: weight must be a positive number, used 1.")
            weight = 1
        your_raw = str(feature.get("your_status", "unknown")).strip().lower()
        your_status = ALIASES.get(your_raw, "unknown")
        if your_raw not in ALIASES:
            warnings.append(f"{fname}: unrecognized your_status '{your_raw}', treated as unknown.")
        cells = {}
        for comp in competitors:
            raw = (feature.get("competitors") or {}).get(comp, "unknown")
            status, source, as_of = read_status(raw, default_as_of, warnings, f"{comp} / {fname}")
            display = status
            if status == "no" and not source:
                display = "not_listed"
                warnings.append(
                    f'{comp} "No" for "{fname}" has no source: confirm it in their docs or a trial, '
                    f'or publish it as "Not listed (as of <date>)".'
                )
            if status != "unknown":
                total_facts += 1
                sourced += 1 if source else 0
                if as_of:
                    dates.append(str(as_of))
            comparable = your_status != "unknown" and display in SCORE
            cells[comp] = {"status": status, "display": display, "source": source,
                           "as_of": as_of, "comparable": comparable}
        rows.append({"name": fname, "category": feature.get("category") or "General",
                     "weight": weight, "your_status": your_status, "cells": cells,
                     "notes": feature.get("notes") or ""})

    summary = {}
    for comp in competitors:
        wins = ties = losses = skipped = 0
        w_wins = w_total = 0.0
        for row in rows:
            cell = row["cells"][comp]
            if not cell["comparable"]:
                skipped += 1
                continue
            mine, theirs = SCORE[row["your_status"]], SCORE[cell["display"]]
            w_total += row["weight"]
            if mine > theirs:
                wins += 1
                w_wins += row["weight"]
            elif mine == theirs:
                ties += 1
            else:
                losses += 1
        pct = round(w_wins / w_total * 100) if w_total else 0
        summary[comp] = {"wins": wins, "ties": ties, "losses": losses, "not_comparable": skipped,
                         "weighted_win_pct": pct, "verdict": verdict(pct) if w_total else "No verified data"}

    advantages, gaps, parity, unverifiable = [], [], [], []
    for row in rows:
        comparable = {c: cell for c, cell in row["cells"].items() if cell["comparable"]}
        if not comparable:
            unverifiable.append(row["name"])
            continue
        mine = SCORE[row["your_status"]]
        ahead = [c for c, cell in comparable.items() if SCORE[cell["display"]] > mine]
        if ahead:
            gaps.append({"feature": row["name"], "ahead": ahead})
        elif all(SCORE[cell["display"]] < mine for cell in comparable.values()):
            advantages.append(row["name"])
        else:
            parity.append(row["name"])

    scored = [s["weighted_win_pct"] for s in summary.values() if s["verdict"] != "No verified data"]
    overall = round(sum(scored) / len(scored)) if scored else 0
    return {
        "your_product": your,
        "competitors": competitors,
        "total_features": len(rows),
        "overall_weighted_win_pct": overall,
        "overall_verdict": verdict(overall) if scored else "No verified data",
        "competitor_summary": summary,
        "advantages": advantages,
        "gaps": gaps,
        "parity": parity,
        "unverifiable": unverifiable,
        "facts_with_source": sourced,
        "facts_total": total_facts,
        "oldest_as_of": min(dates) if dates else None,
        "warnings": warnings,
        "features": rows,
    }


def verdict(pct):
    if pct >= 70:
        return "Strong advantage"
    if pct >= 50:
        return "Slight advantage"
    if pct >= 35:
        return "Competitive parity"
    return "Trailing"


def to_markdown(result):
    comps = result["competitors"]
    lines = [
        "| Feature | " + " | ".join([result["your_product"]] + comps) + " | Notes |",
        "|---|" + "|".join(["---"] * (len(comps) + 1)) + "|---|",
    ]
    used, category = set(), None
    for row in result["features"]:
        if row["category"] != category:
            category = row["category"]
            lines.append(f"| **{category}** |" + " |" * (len(comps) + 2))
        cells = [LABEL[row["your_status"]]]
        used.add(row["your_status"])
        for comp in comps:
            display = row["cells"][comp]["display"]
            used.add(display)
            cells.append(LABEL[display])
        lines.append(f"| {row['name']} | " + " | ".join(cells) + f" | {row['notes']} |")
    lines.append("")
    key = [f"{LABEL[s]} = {KEY_TEXT[s]}" for s in LABEL if s in used]
    lines.append("Key: " + "; ".join(key) + ".")
    if result["oldest_as_of"]:
        lines.append(f"Competitor details as of {result['oldest_as_of']}.")
    else:
        lines.append("Competitor details as of: ADD A DATE BEFORE PUBLISHING.")
    return "\n".join(lines)


def to_text(result):
    out = [
        f"Comparison matrix: {result['your_product']} vs {', '.join(result['competitors'])} "
        f"({result['total_features']} features)",
        f"Overall weighted win rate: {result['overall_weighted_win_pct']}% ({result['overall_verdict']})",
        "",
        f"{'Competitor':<22}{'Wins':>5}{'Ties':>6}{'Losses':>8}{'Skipped':>9}{'Win %':>8}  Verdict",
    ]
    for comp, s in result["competitor_summary"].items():
        out.append(f"{comp[:21]:<22}{s['wins']:>5}{s['ties']:>6}{s['losses']:>8}"
                   f"{s['not_comparable']:>9}{s['weighted_win_pct']:>7}%  {s['verdict']}")
    out.append("")
    out.append("Your advantages (ahead of every competitor with verified data):")
    if result["advantages"]:
        out.extend(f"- {name}" for name in result["advantages"])
    else:
        out.append("- none")
    out.append("Gaps (at least one competitor ahead):")
    if result["gaps"]:
        out.extend(f"- {g['feature']} ({', '.join(g['ahead'])})" for g in result["gaps"])
    else:
        out.append("- none")
    if result["unverifiable"]:
        out.append("Not comparable (no verified competitor data):")
        out.extend(f"- {name}" for name in result["unverifiable"])
    out.append("")
    out.append(f"Competitor facts with a source: {result['facts_with_source']} of {result['facts_total']}.")
    out.append(f"Oldest 'as of' date: {result['oldest_as_of'] or 'none recorded'}.")
    if result["warnings"]:
        out.append("Evidence warnings:")
        out.extend(f"- {w}" for w in result["warnings"])
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(
        description="Build a feature comparison matrix for competitor pages (stdlib only). "
        "Reads the input JSON only; prints to stdout.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--input", help="path to the JSON input file")
    parser.add_argument("--demo", action="store_true", help="use built-in sample data")
    out = parser.add_mutually_exclusive_group()
    out.add_argument("--markdown", action="store_true", help="print the page table as Markdown")
    out.add_argument("--json", action="store_true", help="print the full analysis as JSON")
    args = parser.parse_args()

    if bool(args.input) == bool(args.demo):
        parser.error("pass --input FILE, or --demo")
    if args.demo:
        data = DEMO_DATA
    else:
        try:
            with open(args.input, encoding="utf-8") as handle:
                data = json.load(handle)
        except FileNotFoundError:
            fail(f"file not found: {args.input}")
        except json.JSONDecodeError as err:
            fail(f"invalid JSON in {args.input}: {err}")

    result = build_matrix(data)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif args.markdown:
        print(to_markdown(result))
        for warning in result["warnings"]:
            print(f"warning: {warning}", file=sys.stderr)
    else:
        print(to_text(result))


if __name__ == "__main__":
    main()
