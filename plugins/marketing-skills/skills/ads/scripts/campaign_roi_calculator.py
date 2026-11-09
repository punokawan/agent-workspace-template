#!/usr/bin/env python3
"""
campaign_roi_calculator.py: unit economics for one campaign or a portfolio.

Per campaign: CTR, CPC, CPM, click-to-lead, lead-to-customer, CPL, CPA (cost per
customer), ROAS, revenue per customer. With a gross margin: gross profit,
contribution after ad spend, profit ROI, break-even ROAS (1 / margin) and
break-even CPA. With targets: ROAS and CPA against target.
Portfolio: blended totals, a non-brand roll-up (campaigns marked "brand": true
are left out of it), and a per-channel roll-up.

Facts only. It prints no verdicts from industry benchmarks. An input that is not
given prints as MISSING and is never estimated. Check sample size, conversion
lag and attribution windows before acting on any number.

Usage:
  python3 campaign_roi_calculator.py --file campaigns.json [--json]
  python3 campaign_roi_calculator.py --spend 5000 --revenue 18000 --customers 120 \\
      --clicks 2400 --impressions 90000 --margin 0.7 [--target-roas 3] [--json]
  python3 campaign_roi_calculator.py            # demo portfolio

Input file: an object with a "campaigns" array (or a bare array):
  {
    "gross_margin": 0.7,                 optional default for every campaign
    "campaigns": [
      {"name": "Search - Brand", "channel": "paid_search", "brand": true,
       "attribution_window": "30d click",
       "spend": 1200, "revenue": 9800, "impressions": 40000, "clicks": 3100,
       "customers": 70,
       "gross_margin": 0.7, "target_roas": 4, "target_cpa": 60}
    ]
  }
  Only "spend" is required. Gross margin is a fraction (0.7) or a percent (70).

Stdlib only. Reads the input file you pass; writes nothing.
"""

import argparse
import json
import sys

MISSING = "MISSING"
NOT_DEFINED = "n/a"

DEMO = {
    "gross_margin": 0.7,
    "campaigns": [
        {"name": "Search - Brand", "channel": "paid_search", "brand": True,
         "attribution_window": "30d click", "spend": 1200, "revenue": 9800,
         "impressions": 40000, "clicks": 3100, "customers": 70},
        {"name": "Search - Non-brand", "channel": "paid_search",
         "attribution_window": "30d click", "spend": 6400, "revenue": 17600,
         "impressions": 210000, "clicks": 5200, "customers": 110,
         "target_roas": 3.0},
        {"name": "Meta - Prospecting", "channel": "paid_social",
         "attribution_window": "7d click", "spend": 4800, "revenue": 9100,
         "impressions": 640000, "clicks": 6900, "customers": 52,
         "target_cpa": 80},
    ],
}


class InputError(ValueError):
    pass


def number(value, field, campaign, required=False):
    """Return a non-negative float, None when absent, or raise InputError."""
    if value is None:
        if required:
            raise InputError(f"campaign '{campaign}': '{field}' is required")
        return None
    if isinstance(value, bool):
        raise InputError(f"campaign '{campaign}': '{field}' must be a number")
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise InputError(f"campaign '{campaign}': '{field}' must be a number, got {value!r}")
    if result < 0:
        raise InputError(f"campaign '{campaign}': '{field}' cannot be negative")
    return result


def margin_fraction(value, campaign):
    """Accept 0.7 or 70; return a fraction in (0, 1], or None."""
    margin = number(value, "gross_margin", campaign)
    if margin is None:
        return None
    if margin == 0:
        raise InputError(f"campaign '{campaign}': gross margin must be above 0")
    if margin > 1:
        margin = margin / 100.0
    if margin > 1:
        raise InputError(f"campaign '{campaign}': gross margin above 100%")
    return margin


def ratio(numerator, denominator, scale=1.0):
    """numerator / denominator * scale, MISSING when an input is absent, n/a on zero."""
    if numerator is None or denominator is None:
        return MISSING
    if denominator == 0:
        return NOT_DEFINED
    return numerator / denominator * scale


def known(value):
    return isinstance(value, float) or isinstance(value, int)


def unit_metrics(spend, revenue, impressions, clicks, leads, customers, margin):
    """Shared math for a campaign and for any roll-up."""
    m = {
        "spend": spend,
        "revenue": revenue if revenue is not None else MISSING,
        "ctr_pct": ratio(clicks, impressions, 100),
        "cpc": ratio(spend, clicks),
        "cpm": ratio(spend, impressions, 1000),
        "click_to_lead_pct": ratio(leads, clicks, 100),
        "lead_to_customer_pct": ratio(customers, leads, 100),
        "click_to_customer_pct": ratio(customers, clicks, 100),
        "cpl": ratio(spend, leads),
        "cpa": ratio(spend, customers),
        "roas": ratio(revenue, spend),
        "revenue_per_customer": ratio(revenue, customers),
    }
    if margin is None or revenue is None:
        for key in ("gross_profit", "contribution", "profit_roi_pct",
                    "break_even_roas", "break_even_cpa"):
            m[key] = MISSING
        if margin is not None:
            m["break_even_roas"] = 1 / margin
        return m
    gross_profit = revenue * margin
    m["gross_profit"] = gross_profit
    m["contribution"] = gross_profit - spend
    m["profit_roi_pct"] = ratio(gross_profit - spend, spend, 100)
    m["break_even_roas"] = 1 / margin
    rpc = m["revenue_per_customer"]
    m["break_even_cpa"] = rpc * margin if known(rpc) else rpc
    return m


def campaign_result(raw, default_margin):
    name = str(raw.get("name", "Unnamed campaign"))
    spend = number(raw.get("spend"), "spend", name, required=True)
    revenue = number(raw.get("revenue"), "revenue", name)
    impressions = number(raw.get("impressions"), "impressions", name)
    clicks = number(raw.get("clicks"), "clicks", name)
    leads = number(raw.get("leads"), "leads", name)
    customers = number(raw.get("customers"), "customers", name)
    margin = margin_fraction(raw.get("gross_margin"), name)
    if margin is None:
        margin = default_margin
    target_roas = number(raw.get("target_roas"), "target_roas", name)
    target_cpa = number(raw.get("target_cpa"), "target_cpa", name)

    metrics = unit_metrics(spend, revenue, impressions, clicks, leads, customers, margin)
    flags = []
    roas = metrics["roas"]
    be_roas = metrics["break_even_roas"]
    if known(roas) and known(be_roas):
        if roas < be_roas:
            flags.append(f"below break-even ROAS ({roas:.2f} vs {be_roas:.2f}): "
                         f"contribution {fmt(metrics['contribution'])}")
        else:
            flags.append(f"above break-even ROAS ({roas:.2f} vs {be_roas:.2f})")
    if target_roas is not None and known(roas):
        word = "meets" if roas >= target_roas else "below"
        flags.append(f"ROAS {word} target ({roas:.2f} vs {target_roas:.2f})")
    cpa = metrics["cpa"]
    if target_cpa is not None and known(cpa):
        word = "within" if cpa <= target_cpa else "above"
        flags.append(f"CPA {word} target ({fmt(cpa)} vs {fmt(target_cpa)})")
    absent = [f for f, v in (("revenue", revenue), ("customers", customers),
                             ("gross_margin", margin)) if v is None]
    return {
        "name": name,
        "channel": str(raw.get("channel", "unspecified")),
        "brand": bool(raw.get("brand", False)),
        "attribution_window": raw.get("attribution_window"),
        "inputs": {"spend": spend, "revenue": revenue, "impressions": impressions,
                   "clicks": clicks, "leads": leads, "customers": customers,
                   "gross_margin": margin},
        "metrics": metrics,
        "flags": flags,
        "missing_inputs": absent,
    }


def rollup(results, label):
    """Blended metrics. A sum is only reported when every campaign has the input."""
    def total(field):
        values = [r["inputs"][field] for r in results]
        if any(v is None for v in values):
            return None
        return sum(values)

    spend = sum(r["inputs"]["spend"] for r in results)
    revenue = total("revenue")
    metrics = unit_metrics(spend, revenue, total("impressions"), total("clicks"),
                           total("leads"), total("customers"), None)
    margins_known = all(r["inputs"]["gross_margin"] is not None for r in results)
    if margins_known and revenue is not None:
        gross_profit = sum(r["inputs"]["revenue"] * r["inputs"]["gross_margin"]
                           for r in results)
        metrics["gross_profit"] = gross_profit
        metrics["contribution"] = gross_profit - spend
        metrics["profit_roi_pct"] = ratio(gross_profit - spend, spend, 100)
    metrics.pop("break_even_roas", None)
    metrics.pop("break_even_cpa", None)
    gaps = {}
    for field in ("revenue", "impressions", "clicks", "leads", "customers", "gross_margin"):
        n = sum(1 for r in results if r["inputs"][field] is None)
        if 0 < n < len(results):
            gaps[field] = n
    return {"label": label, "campaigns": len(results), "metrics": metrics,
            "campaigns_missing_input": gaps}


def analyse(data):
    if isinstance(data, list):
        data = {"campaigns": data}
    if not isinstance(data, dict) or not isinstance(data.get("campaigns"), list):
        raise InputError("input needs a 'campaigns' array (or be an array of campaigns)")
    if not data["campaigns"]:
        raise InputError("'campaigns' is empty")
    default_margin = margin_fraction(data.get("gross_margin"), "defaults")
    results = []
    for raw in data["campaigns"]:
        if not isinstance(raw, dict):
            raise InputError("each campaign must be an object")
        results.append(campaign_result(raw, default_margin))

    summary = {"portfolio": rollup(results, "portfolio")}
    brand = [r for r in results if r["brand"]]
    non_brand = [r for r in results if not r["brand"]]
    if brand and non_brand:
        summary["non_brand"] = rollup(non_brand, "non-brand")
    channels = {}
    for r in results:
        channels.setdefault(r["channel"], []).append(r)
    summary["channels"] = [rollup(rs, ch) for ch, rs in sorted(channels.items())]

    windows = sorted({str(r["attribution_window"]) for r in results
                      if r["attribution_window"]})
    warnings = []
    if len(windows) > 1:
        warnings.append("campaigns use different attribution windows (" + ", ".join(windows) +
                        "): blended revenue and customers mix definitions; compare them "
                        "side by side or use a neutral source such as the CRM")
    unlabeled = [r["name"] for r in results if not r["attribution_window"]]
    if windows and unlabeled:
        warnings.append("attribution window not given for: " + ", ".join(unlabeled))

    def rank_key(r):
        value = r["metrics"]["contribution"]
        if known(value):
            return (0, -value)
        value = r["metrics"]["roas"]
        return (1, -value) if known(value) else (2, 0)

    ordered = sorted(results, key=rank_key)
    return {"summary": summary, "campaigns": ordered, "warnings": warnings}


def fmt(value, digits=2):
    if isinstance(value, str):
        return value
    if value is None:
        return MISSING
    return f"{value:,.{digits}f}"


def pct(value):
    return value if isinstance(value, str) else f"{value:.2f}%"


def plural(n, word):
    return f"{n} {word}" if n == 1 else f"{n} {word}s"


def print_rollup(block, indent="  "):
    m = block["metrics"]
    print(f"{indent}Spend {fmt(m['spend'])} | Revenue {fmt(m['revenue'])} | "
          f"ROAS {fmt(m['roas'])} | Contribution {fmt(m.get('contribution', MISSING))} | "
          f"Profit ROI {pct(m.get('profit_roi_pct', MISSING))}")
    print(f"{indent}CTR {pct(m['ctr_pct'])} | CPC {fmt(m['cpc'])} | CPL {fmt(m['cpl'])} | "
          f"CPA {fmt(m['cpa'])} | Click-to-customer {pct(m['click_to_customer_pct'])}")
    if block["campaigns_missing_input"]:
        gaps = ", ".join(f"{k} ({n})" for k, n in block["campaigns_missing_input"].items())
        print(f"{indent}Not summed, input missing in some campaigns: {gaps}")


def print_text(report):
    print("CAMPAIGN ROI REPORT")
    print("Facts only. Check sample size, conversion lag and attribution windows before acting.")
    for w in report["warnings"]:
        print(f"WARNING: {w}")
    s = report["summary"]
    if s["portfolio"]["campaigns"] > 1:
        print(f"\nPORTFOLIO, BLENDED ({plural(s['portfolio']['campaigns'], 'campaign')})")
        print_rollup(s["portfolio"])
    if "non_brand" in s:
        print(f"\nNON-BRAND ({plural(s['non_brand']['campaigns'], 'campaign')}): set targets and bids on this")
        print_rollup(s["non_brand"])
    if len(s["channels"]) > 1:
        print("\nBY CHANNEL")
        for block in s["channels"]:
            print(f"  {block['label']} ({plural(block['campaigns'], 'campaign')})")
            print_rollup(block, indent="    ")
    print("\nCAMPAIGNS (by contribution, else ROAS)")
    for r in report["campaigns"]:
        m = r["metrics"]
        tags = [r["channel"]]
        if r["brand"]:
            tags.append("brand")
        if r["attribution_window"]:
            tags.append(str(r["attribution_window"]))
        print(f"  {r['name']} [{', '.join(tags)}]")
        print(f"    Spend {fmt(m['spend'])} | Revenue {fmt(m['revenue'])} | ROAS {fmt(m['roas'])} | "
              f"Break-even ROAS {fmt(m['break_even_roas'])} | Contribution {fmt(m['contribution'])}")
        print(f"    CTR {pct(m['ctr_pct'])} | CPC {fmt(m['cpc'])} | CPM {fmt(m['cpm'])} | "
              f"CPL {fmt(m['cpl'])} | CPA {fmt(m['cpa'])} | Break-even CPA {fmt(m['break_even_cpa'])}")
        for flag in r["flags"]:
            print(f"    - {flag}")
        if r["missing_inputs"]:
            print(f"    MISSING inputs: {', '.join(r['missing_inputs'])}")


def main():
    parser = argparse.ArgumentParser(
        description="Campaign unit economics: ROAS, CPA, CPL, CTR, break-even ROAS and "
                    "margin-based contribution, with blended, non-brand and channel roll-ups.",
        epilog="No input runs a demo portfolio. Reads only --file; writes nothing.")
    parser.add_argument("--file", help="JSON file with a 'campaigns' array")
    parser.add_argument("--spend", type=float, help="single campaign: ad spend")
    parser.add_argument("--revenue", type=float, help="single campaign: attributed revenue")
    parser.add_argument("--impressions", type=float, help="single campaign: impressions")
    parser.add_argument("--clicks", type=float, help="single campaign: clicks")
    parser.add_argument("--leads", type=float, help="single campaign: leads")
    parser.add_argument("--customers", type=float, help="single campaign: customers or purchases")
    parser.add_argument("--margin", type=float, help="gross margin, fraction (0.7) or percent (70)")
    parser.add_argument("--target-roas", type=float, help="single campaign: target ROAS")
    parser.add_argument("--target-cpa", type=float, help="single campaign: target CPA")
    parser.add_argument("--name", default="Campaign", help="single campaign: name")
    parser.add_argument("--channel", default="unspecified", help="single campaign: channel")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    try:
        if args.file:
            try:
                with open(args.file, "r", encoding="utf-8") as handle:
                    data = json.load(handle)
            except OSError as exc:
                raise InputError(f"cannot read {args.file}: {exc.strerror}")
            except json.JSONDecodeError as exc:
                raise InputError(f"invalid JSON in {args.file}: {exc}")
        elif args.spend is not None:
            data = {"campaigns": [{
                "name": args.name, "channel": args.channel, "spend": args.spend,
                "revenue": args.revenue, "impressions": args.impressions,
                "clicks": args.clicks, "leads": args.leads, "customers": args.customers,
                "gross_margin": args.margin, "target_roas": args.target_roas,
                "target_cpa": args.target_cpa}]}
        else:
            data = DEMO
            if not args.json:
                print("No input given: running the demo portfolio.\n")
        report = analyse(data)
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(rounded(report), indent=2))
    else:
        print_text(report)


def rounded(value):
    if isinstance(value, float):
        return round(value, 4)
    if isinstance(value, dict):
        return {k: rounded(v) for k, v in value.items()}
    if isinstance(value, list):
        return [rounded(v) for v in value]
    return value


if __name__ == "__main__":
    main()
