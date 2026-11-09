#!/usr/bin/env python3
"""Free-tool ROI estimator: is a free marketing tool worth building?

Adapted from alirezarezvani/claude-skills (MIT), marketing-skill/free-tool-strategy/scripts/tool_roi_estimator.py.
Compares expected customer contribution from the tool's funnel with build, launch and maintenance costs,
as this skill's references/tool-benchmarks.md asks. Run it three times (low, base, high assumptions)
rather than trusting one forecast.
Stdlib only. Reads a JSON file (or stdin with "-") and prints a report to stdout. No network, no file writes.

Input JSON (money in any one currency; rates as fractions, 0.55 = 55%):
  {
    "tool_name": "ROI calculator",       optional: display only
    "build_cost": 4000,                  required: one-time build cost (time x loaded rate)
    "launch_cost": 500,                  optional: one-time distribution cost (default 0)
    "monthly_maintenance": 100,          required: hosting, APIs, upkeep per month
    "traffic_month_1": 600,              required: sessions per month once the page is indexed
    "seo_ramp_months": 3,                optional: months of linear ramp up to traffic_month_1 (default 0)
    "traffic_growth_rate": 0.05,         optional: monthly growth after the ramp (default 0)
    "traffic_cap": 5000,                 optional: ceiling on monthly sessions
    "tool_completion_rate": 0.55,        required: share of sessions that finish the tool
    "lead_capture_rate": 0.10,           required: share of completions that leave contact details
    "lead_to_customer_rate": 0.02,       required unless both of the next two are given
    "lead_to_trial_rate": 0.08,          optional: with trial_to_paid_rate, replaces lead_to_customer_rate
    "trial_to_paid_rate": 0.25,          optional
    "customer_value": 840,               required unless ltv and gross_margin_pct are given: lifetime
                                                   contribution (gross profit) per customer, not revenue
    "ltv": 1200, "gross_margin_pct": 70, optional: used to derive customer_value
    "incremental_share": 1.0,            optional: share of tool-sourced customers who would not have
                                                   come anyway (default 1.0; measure it)
    "months": 24                         optional: modeling window (default 24)
  }

Value is booked when a customer is acquired (lifetime contribution), so the break-even month is on a
value basis, not a cash-payback basis.
"""

import argparse
import json
import sys

SAMPLE_INPUT = {
    "tool_name": "ROI calculator",
    "build_cost": 4000,
    "launch_cost": 500,
    "monthly_maintenance": 100,
    "traffic_month_1": 600,
    "seo_ramp_months": 3,
    "traffic_growth_rate": 0.05,
    "traffic_cap": 3000,
    "tool_completion_rate": 0.55,
    "lead_capture_rate": 0.12,
    "lead_to_trial_rate": 0.08,
    "trial_to_paid_rate": 0.25,
    "ltv": 1400,
    "gross_margin_pct": 75,
    "incremental_share": 0.8,
    "months": 18,
}

FRACTION_KEYS = ("traffic_growth_rate", "tool_completion_rate", "lead_capture_rate", "lead_to_customer_rate",
                 "lead_to_trial_rate", "trial_to_paid_rate", "incremental_share")


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(2)


def load_input(path):
    try:
        if path == "-":
            return json.load(sys.stdin)
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read input: {exc}")


def normalize(data):
    missing = [k for k in ("build_cost", "monthly_maintenance", "traffic_month_1", "tool_completion_rate",
                           "lead_capture_rate") if k not in data]
    if "lead_to_customer_rate" not in data and not ("lead_to_trial_rate" in data and "trial_to_paid_rate" in data):
        missing.append("lead_to_customer_rate (or lead_to_trial_rate + trial_to_paid_rate)")
    if "customer_value" not in data and not ("ltv" in data and "gross_margin_pct" in data):
        missing.append("customer_value (or ltv + gross_margin_pct)")
    if missing:
        fail(f"missing required keys: {', '.join(missing)}")
    for key in FRACTION_KEYS:
        if key in data and not 0 <= data[key] <= 1:
            fail(f"{key} must be a fraction between 0 and 1 (0.05 = 5%)")
    params = dict(data)
    params["_incremental_measured"] = "incremental_share" in data
    if "lead_to_customer_rate" not in params:
        params["lead_to_customer_rate"] = params["lead_to_trial_rate"] * params["trial_to_paid_rate"]
    if "customer_value" not in params:
        if not 0 < params["gross_margin_pct"] <= 100:
            fail("gross_margin_pct must be between 0 and 100")
        params["customer_value"] = params["ltv"] * params["gross_margin_pct"] / 100
    params.setdefault("launch_cost", 0)
    params.setdefault("seo_ramp_months", 0)
    params.setdefault("traffic_growth_rate", 0.0)
    params.setdefault("incremental_share", 1.0)
    params["months"] = int(params.get("months", 24))
    if params["months"] < 1:
        fail("months must be 1 or more")
    return params


def sessions_at(params, month, scale=1.0):
    base = params["traffic_month_1"] * scale
    ramp = params["seo_ramp_months"]
    if ramp and month <= ramp:
        value = base * month / ramp
    else:
        value = base * (1 + params["traffic_growth_rate"]) ** (month - ramp - (1 if not ramp else 0))
    cap = params.get("traffic_cap")
    return min(value, cap * scale) if cap else value


def project(params, scale=1.0):
    rows = []
    cumulative_cost = params["build_cost"] + params["launch_cost"]
    cumulative_value = 0.0
    for month in range(1, params["months"] + 1):
        sessions = sessions_at(params, month, scale)
        completions = sessions * params["tool_completion_rate"]
        leads = completions * params["lead_capture_rate"]
        customers = leads * params["lead_to_customer_rate"] * params["incremental_share"]
        value = customers * params["customer_value"]
        cumulative_cost += params["monthly_maintenance"]
        cumulative_value += value
        rows.append({
            "month": month,
            "sessions": round(sessions),
            "completions": round(completions, 1),
            "leads": round(leads, 1),
            "customers": round(customers, 2),
            "value": round(value, 2),
            "cumulative_net": round(cumulative_value - cumulative_cost, 2),
        })
    return rows


def breakeven_month(rows):
    return next((r["month"] for r in rows if r["cumulative_net"] >= 0), None)


def required_scale(params):
    """Smallest traffic multiplier that breaks even by the last month (binary search)."""
    if project(params, 1e6)[-1]["cumulative_net"] < 0:
        return None
    low, high = 0.0, 1e6
    for _ in range(100):
        mid = (low + high) / 2
        if project(params, mid)[-1]["cumulative_net"] >= 0:
            high = mid
        else:
            low = mid
    return high


def calculate(params):
    rows = project(params)
    total_cost = params["build_cost"] + params["launch_cost"] + params["monthly_maintenance"] * params["months"]
    total_value = sum(r["value"] for r in rows)
    total_leads = sum(r["leads"] for r in rows)
    total_customers = sum(r["customers"] for r in rows)
    scale = required_scale(params)
    flags = []
    if params["tool_completion_rate"] < 0.40:
        flags.append("Completion below 40%: fewer inputs, faster first result, check mobile.")
    if params["lead_capture_rate"] < 0.05:
        flags.append("Lead capture below 5%: move the gate after the core result, offer a reason to save it.")
    if not params["_incremental_measured"]:
        flags.append("All tool-sourced customers are treated as incremental; measure this where feasible.")
    return {
        "tool_name": params.get("tool_name", "Free tool"),
        "months": params["months"],
        "totals": {
            "cost": round(total_cost, 2),
            "contribution": round(total_value, 2),
            "net": round(total_value - total_cost, 2),
            "return_pct": round((total_value - total_cost) / total_cost * 100, 1) if total_cost else None,
            "leads": round(total_leads, 1),
            "customers": round(total_customers, 2),
            "cost_per_lead": round(total_cost / total_leads, 2) if total_leads else None,
            "cost_per_customer": round(total_cost / total_customers, 2) if total_customers else None,
        },
        "break_even_month": breakeven_month(rows),
        "traffic_month_1_needed_for_break_even": round(params["traffic_month_1"] * scale) if scale else None,
        "flags": flags,
        "monthly": rows,
    }


def money(value, currency, decimals=0):
    if value is None:
        return "n/a"
    text = f"{value:,.{decimals}f}"
    return f"{text} {currency}" if currency else text


def print_report(result, params, currency, sample):
    line = "=" * 70
    print(line)
    print(f"FREE-TOOL ROI ESTIMATE: {result['tool_name']}" + ("  (SAMPLE DATA)" if sample else ""))
    print(line)
    t = result["totals"]
    print(f"\nOver {result['months']} months")
    print(f"  Cost (build, launch, maintenance): {money(t['cost'], currency)}")
    print(f"  Customer contribution:             {money(t['contribution'], currency)}")
    print(f"  Net:                               {money(t['net'], currency)}")
    print(f"  Return:                            {t['return_pct']}%")
    print(f"  Leads / customers:                 {t['leads']:,.0f} / {t['customers']:,.1f}")
    print(f"  Cost per lead / per customer:      {money(t['cost_per_lead'], currency, 2)} / "
          f"{money(t['cost_per_customer'], currency, 2)}")
    be = result["break_even_month"]
    print(f"  Break-even month (value basis):    {be if be else 'not reached in the window'}")
    need = result["traffic_month_1_needed_for_break_even"]
    if need is None:
        print("  Break-even traffic:                not reachable with these conversion rates")
    else:
        print(f"  traffic_month_1 needed to break even by month {result['months']}: {need:,} sessions "
              f"(assumed {params['traffic_month_1']:,})")
    print(f"\n  {'Mo':>3} {'Sessions':>9} {'Leads':>8} {'Customers':>10} {'Cumulative net':>16}")
    for r in result["monthly"]:
        print(f"  {r['month']:>3} {r['sessions']:>9,} {r['leads']:>8.1f} {r['customers']:>10.2f} "
              f"{money(r['cumulative_net'], currency):>16}")
    if result["flags"]:
        print("\nFlags")
        for flag in result["flags"]:
            print(f"  - {flag}")
    print("\nThese are planning assumptions, not benchmarks. Compare low, base and high runs.")
    print(line)


def main():
    parser = argparse.ArgumentParser(
        description="Estimate whether a free marketing tool pays back its build, launch and maintenance cost.",
        epilog="Input format and assumptions are documented at the top of this file.",
    )
    parser.add_argument("input", nargs="?", help="JSON input file, or - to read stdin")
    parser.add_argument("--sample", action="store_true", help="run with built-in sample data")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    parser.add_argument("--currency", default="", help="label for amounts, e.g. a currency code (default: none)")
    args = parser.parse_args()

    if args.sample:
        data = SAMPLE_INPUT
    elif args.input:
        data = load_input(args.input)
    else:
        parser.print_help()
        sys.exit(1)
    if not isinstance(data, dict):
        fail("input must be a JSON object")
    params = normalize(data)
    result = calculate(params)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result, params, args.currency, args.sample)


if __name__ == "__main__":
    main()
