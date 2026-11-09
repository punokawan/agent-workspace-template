#!/usr/bin/env python3
"""
ad_health_scorer.py: weighted ad account health with evidence coverage kept separate.

Implements the scoring semantics in references/audit-guardrails.md:
  - every check is exactly one of: pass | fail | unknown | na
  - health   = severity-weighted pass share of the checks you verified (pass + fail)
  - coverage = verified checks / applicable checks (unknown lowers coverage, never health;
               na counts toward neither)
  - coverage 80%+ graded, 60-79% provisional, below 60% no health score at all
  - a platform that was not audited, or has no score, stays out of the roll-up

Severity multipliers: critical 5, high 3, medium 1.5, low 0.5.
Category weights per platform are in PLATFORM_WEIGHTS and references/health-scoring.md.

Usage:
  python3 ad_health_scorer.py --checks checks.json --platform google [--json]
  python3 ad_health_scorer.py --multi platforms.json [--json]
  python3 ad_health_scorer.py                     # demo account

Input for --checks: a JSON array of checks:
  [{"category": "conversion_tracking", "check": "Enhanced conversions enabled",
    "result": "fail", "severity": "critical",
    "detail": "what you saw, or the evidence you need", "effort": "low"}]
  effort (low | medium | high) is optional; a failed critical or high check with
  low effort is listed as a quick win.
Input for --multi: {"google": {"checks": [...], "budget": 3000},
                    "linkedin": {"audited": false, "reason": "no access"}}

Stdlib only. Reads the input file you pass; writes nothing.
"""

import argparse
import json
import sys

SEVERITY_MULTIPLIER = {"critical": 5.0, "high": 3.0, "medium": 1.5, "low": 0.5}
SEVERITY_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3}
RESULTS = {"pass": "pass", "fail": "fail", "unknown": "unknown", "na": "na",
           "n/a": "na", "not_applicable": "na", "not applicable": "na"}
UNLISTED_CATEGORY_WEIGHT = 0.10

PLATFORM_WEIGHTS = {
    "google": {"conversion_tracking": 0.25, "wasted_spend": 0.20, "account_structure": 0.15,
               "keywords": 0.15, "ads": 0.15, "settings": 0.10},
    "meta": {"pixel_capi": 0.30, "creative": 0.30, "structure": 0.20, "audience": 0.20},
    "linkedin": {"technical": 0.25, "targeting": 0.25, "creative": 0.25, "budget": 0.25},
    "tiktok": {"pixel": 0.25, "creative": 0.30, "targeting": 0.25, "budget": 0.20},
    "other": {},
}

DEMO = {
    "google": {"budget": 3000, "checks": [
        {"category": "conversion_tracking", "check": "Conversion tag fires on a test conversion",
         "result": "pass", "severity": "critical"},
        {"category": "conversion_tracking", "check": "Enhanced conversions enabled",
         "result": "fail", "severity": "critical", "effort": "low",
         "detail": "setting is off in the conversion action"},
        {"category": "conversion_tracking", "check": "Only revenue or qualified-pipeline actions are primary",
         "result": "unknown", "severity": "high",
         "detail": "need the conversion-action list with primary/secondary status"},
        {"category": "wasted_spend", "check": "Search terms reviewed in the last 30 days",
         "result": "unknown", "severity": "high", "detail": "need the search terms report"},
        {"category": "wasted_spend", "check": "Broad match only with smart bidding",
         "result": "pass", "severity": "critical"},
        {"category": "account_structure", "check": "Naming convention applied",
         "result": "pass", "severity": "low"},
        {"category": "keywords", "check": "No duplicate keywords across campaigns",
         "result": "pass", "severity": "high"},
        {"category": "ads", "check": "Sitelinks and callouts on every search campaign",
         "result": "fail", "severity": "medium", "effort": "low",
         "detail": "no callouts on 2 of 4 campaigns"},
        {"category": "ads", "check": "Shopping feed errors", "result": "na", "severity": "high"},
        {"category": "settings", "check": "Location targeting is presence, not interest",
         "result": "pass", "severity": "high"},
    ]},
    "meta": {"budget": 2000, "checks": [
        {"category": "pixel_capi", "check": "Pixel fires on purchase", "result": "pass",
         "severity": "critical"},
        {"category": "pixel_capi", "check": "Conversions API deduplicated with the pixel",
         "result": "fail", "severity": "critical", "effort": "medium",
         "detail": "no event_id on browser events"},
        {"category": "creative", "check": "At least three active concepts per ad set",
         "result": "fail", "severity": "high", "effort": "medium", "detail": "one concept per ad set"},
        {"category": "creative", "check": "Frequency below fatigue band on top spenders",
         "result": "pass", "severity": "high"},
        {"category": "audience", "check": "Customers excluded from prospecting",
         "result": "pass", "severity": "medium"},
    ]},
    "linkedin": {"audited": False, "reason": "no Campaign Manager access"},
}


class InputError(ValueError):
    pass


def band(coverage):
    if coverage >= 80:
        return "graded"
    if coverage >= 60:
        return "provisional"
    return "insufficient evidence"


def normalise(check, index, platform):
    if not isinstance(check, dict):
        raise InputError(f"{platform}: check #{index + 1} must be an object")
    name = str(check.get("check", f"check #{index + 1}"))
    raw = str(check.get("result", "")).strip().lower()
    if raw not in RESULTS:
        raise InputError(f"{platform}: '{name}' has result {check.get('result')!r}; "
                         "use pass, fail, unknown or na (a partial pass is a fail with a detail)")
    severity = str(check.get("severity", "medium")).strip().lower()
    if severity not in SEVERITY_MULTIPLIER:
        raise InputError(f"{platform}: '{name}' has severity {check.get('severity')!r}; "
                         "use critical, high, medium or low")
    effort = check.get("effort")
    effort = str(effort).strip().lower() if effort is not None else None
    return {"category": str(check.get("category", "other")), "check": name,
            "result": RESULTS[raw], "severity": severity, "effort": effort,
            "detail": str(check.get("detail", ""))}


def score_platform(platform, checks, audited=True, reason=""):
    if not audited:
        return {"platform": platform, "audited": False, "reason": reason or "not audited",
                "health": None, "status": "not audited"}
    if not isinstance(checks, list) or not checks:
        raise InputError(f"{platform}: 'checks' must be a non-empty array")
    items = [normalise(c, i, platform) for i, c in enumerate(checks)]
    weights = PLATFORM_WEIGHTS.get(platform, {})

    applicable = [c for c in items if c["result"] != "na"]
    verified = [c for c in applicable if c["result"] in ("pass", "fail")]
    coverage = 100.0 * len(verified) / len(applicable) if applicable else 0.0
    status = band(coverage)

    categories = {}
    for c in items:
        entry = categories.setdefault(c["category"], {"verified": 0, "applicable": 0,
                                                       "passed_weight": 0.0, "verified_weight": 0.0})
        if c["result"] == "na":
            continue
        entry["applicable"] += 1
        if c["result"] in ("pass", "fail"):
            mult = SEVERITY_MULTIPLIER[c["severity"]]
            entry["verified"] += 1
            entry["verified_weight"] += mult
            if c["result"] == "pass":
                entry["passed_weight"] += mult

    unlisted = sorted(cat for cat in categories if weights and cat not in weights)
    weighted_sum = 0.0
    weight_total = 0.0
    category_health = {}
    for cat, entry in sorted(categories.items()):
        if entry["verified_weight"] == 0:
            category_health[cat] = None
            continue
        health = 100.0 * entry["passed_weight"] / entry["verified_weight"]
        category_health[cat] = health
        weight = weights.get(cat, UNLISTED_CATEGORY_WEIGHT) if weights else 1.0
        weighted_sum += health * weight
        weight_total += weight
    health = weighted_sum / weight_total if weight_total else None

    if status == "insufficient evidence":
        health = None
        category_health = {cat: None for cat in category_health}

    by_severity = lambda c: SEVERITY_ORDER[c["severity"]]
    fails = sorted((c for c in items if c["result"] == "fail"), key=by_severity)
    unknowns = sorted((c for c in items if c["result"] == "unknown"), key=by_severity)
    quick_wins = [c for c in fails if c["severity"] in ("critical", "high") and c["effort"] == "low"]

    return {
        "platform": platform, "audited": True, "status": status,
        "health": health, "coverage_pct": coverage,
        "verified": len(verified), "applicable": len(applicable),
        "not_applicable": len(items) - len(applicable),
        "categories": {cat: {"health": category_health[cat],
                             "verified": categories[cat]["verified"],
                             "applicable": categories[cat]["applicable"]}
                       for cat in sorted(categories)},
        "unweighted_categories": unlisted,
        "fails": fails, "unknowns": unknowns, "quick_wins": quick_wins,
    }


def rollup(results, budgets):
    included = [r for r in results if r["health"] is not None]
    excluded = [{"platform": r["platform"],
                 "reason": r.get("reason") or r["status"]} for r in results if r["health"] is None]
    if not included:
        return {"health": None, "status": "no platform has a score", "excluded": excluded}
    if all(budgets.get(r["platform"]) for r in included):
        raw = {r["platform"]: float(budgets[r["platform"]]) for r in included}
        basis = "budget share"
    else:
        raw = {r["platform"]: 1.0 for r in included}
        basis = "equal weights (budget missing for at least one platform)"
    total = sum(raw.values())
    shares = {p: v / total for p, v in raw.items()}
    health = sum(r["health"] * shares[r["platform"]] for r in included)
    status = "graded" if all(r["status"] == "graded" for r in included) else "provisional"
    if excluded:
        status += ", partial: not every platform is in it"
    return {"health": health, "status": status, "weighting": basis,
            "shares": shares, "excluded": excluded}


def fmt_score(value):
    return "withheld" if value is None else f"{value:.1f}"


def print_platform(r):
    if not r["audited"]:
        print(f"{r['platform'].upper()}: not audited ({r['reason']}). No score; not in the roll-up.")
        return
    score = "withheld" if r["health"] is None else f"{r['health']:.1f}/100"
    print(f"{r['platform'].upper()}: health {score}, {r['status']} "
          f"(coverage {r['coverage_pct']:.0f}%: {r['verified']} of {r['applicable']} applicable "
          f"checks verified; {r['not_applicable']} not applicable)")
    if r["status"] == "insufficient evidence":
        print("  Below 60% coverage: report the findings below, not a score.")
    print(f"  {'Category':<24} {'Health':>8} {'Verified':>10}")
    for cat, c in r["categories"].items():
        print(f"  {cat:<24} {fmt_score(c['health']):>8} {c['verified']:>4}/{c['applicable']:<5}")
    if r["unweighted_categories"]:
        print(f"  Categories without a platform weight (weighted {UNLISTED_CATEGORY_WEIGHT}): "
              + ", ".join(r["unweighted_categories"]))
    if r["fails"]:
        print("  Fails, by severity:")
        for c in r["fails"]:
            detail = f": {c['detail']}" if c["detail"] else ""
            print(f"    [{c['severity']}] {c['check']}{detail}")
    if r["unknowns"]:
        print("  Unknown, evidence needed:")
        for c in r["unknowns"]:
            detail = f": {c['detail']}" if c["detail"] else ""
            print(f"    [{c['severity']}] {c['check']}{detail}")
    if r["quick_wins"]:
        print("  Quick wins (critical or high, low effort):")
        for c in r["quick_wins"]:
            print(f"    {c['check']}")


def print_rollup(agg):
    if agg["health"] is None:
        print(f"Roll-up: none ({agg['status']}).")
    else:
        shares = ", ".join(f"{p} {s:.0%}" for p, s in agg["shares"].items())
        print(f"Roll-up: {agg['health']:.1f}/100, {agg['status']}. Weighting: {agg['weighting']} "
              f"({shares}).")
    for e in agg["excluded"]:
        print(f"  Not in the roll-up: {e['platform']} ({e['reason']})")


def load(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise InputError(f"cannot read {path}: {exc.strerror}")
    except json.JSONDecodeError as exc:
        raise InputError(f"invalid JSON in {path}: {exc}")


def run_multi(data):
    if not isinstance(data, dict) or not data:
        raise InputError("--multi input must be an object keyed by platform")
    results, budgets = [], {}
    for platform, pdata in data.items():
        if not isinstance(pdata, dict):
            raise InputError(f"{platform}: value must be an object")
        audited = pdata.get("audited", True) is not False
        results.append(score_platform(str(platform).lower(), pdata.get("checks"), audited,
                                      str(pdata.get("reason", ""))))
        if pdata.get("budget") is not None:
            budgets[str(platform).lower()] = pdata["budget"]
    return {"platforms": results, "rollup": rollup(results, budgets)}


def rounded(value):
    if isinstance(value, float):
        return round(value, 2)
    if isinstance(value, dict):
        return {k: rounded(v) for k, v in value.items()}
    if isinstance(value, list):
        return [rounded(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(
        description="Weighted ad account health with evidence coverage kept separate "
                    "(pass / fail / unknown / na).",
        epilog="No input runs a demo account. Reads only the file you pass; writes nothing.")
    parser.add_argument("--checks", help="JSON array of checks for one platform")
    parser.add_argument("--platform", default="google", choices=sorted(PLATFORM_WEIGHTS),
                        help="platform for --checks (sets the category weights)")
    parser.add_argument("--multi", help="JSON object of platforms for a budget-weighted roll-up")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    try:
        if args.multi:
            report = run_multi(load(args.multi))
        elif args.checks:
            report = {"platforms": [score_platform(args.platform, load(args.checks))]}
        else:
            if not args.json:
                print("No input given: running the demo account.\n")
            report = run_multi(DEMO)
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(rounded(report), indent=2))
        return
    for r in report["platforms"]:
        print_platform(r)
        print()
    if "rollup" in report:
        print_rollup(report["rollup"])


if __name__ == "__main__":
    main()
