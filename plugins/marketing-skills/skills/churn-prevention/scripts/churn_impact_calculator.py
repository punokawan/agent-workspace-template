#!/usr/bin/env python3
"""Churn impact calculator: the revenue at stake from better save rates (cancel flow) and recovery rates (dunning).

Adapted from alirezarezvani/claude-skills (MIT), marketing-skill/churn-prevention/scripts/churn_impact_calculator.py.
Stdlib only. Reads a JSON file (or stdin with "-") and prints a report to stdout. No network, no file writes.

Input JSON (money in any one currency; rates in percent):
  {
    "mrr": 50000,                          required
    "monthly_churn_rate_pct": 4.5,         required: observed MRR churn per month, after today's saves
    "voluntary_churn_pct": 65,             required: share of churned MRR that customers chose to cancel
    "current_save_rate_pct": 8,            required: cancel-flow saves / cancel attempts
    "target_save_rate_pct": 20,            required
    "current_recovery_rate_pct": 15,       required: recovered / failed payments
    "target_recovery_rate_pct": 35,        required
    "avg_customer_mrr": 150,               optional: converts MRR into customer counts
    "post_save_monthly_churn_pct": 6,      optional: churn of saved customers afterwards (default: the
                                                     observed churn; saved customers often leave sooner)
    "gross_margin_pct": 80,                optional: converts retained revenue into contribution
    "months": 12                           optional: window (default 12)
  }

Observed churn is what is left after today's saves, so the MRR that reached the cancel flow or failed
payment is derived as churned / (1 - current rate).
"""

import argparse
import json
import sys

SAMPLE_INPUT = {
    "mrr": 50000,
    "monthly_churn_rate_pct": 4.5,
    "voluntary_churn_pct": 65,
    "current_save_rate_pct": 8,
    "target_save_rate_pct": 20,
    "current_recovery_rate_pct": 15,
    "target_recovery_rate_pct": 35,
    "avg_customer_mrr": 150,
    "post_save_monthly_churn_pct": 6,
    "gross_margin_pct": 80,
}

REQUIRED_KEYS = ("mrr", "monthly_churn_rate_pct", "voluntary_churn_pct", "current_save_rate_pct",
                 "target_save_rate_pct", "current_recovery_rate_pct", "target_recovery_rate_pct")


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


def validate(data):
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        fail(f"missing required keys: {', '.join(missing)}")
    for key in REQUIRED_KEYS[1:] + ("post_save_monthly_churn_pct", "gross_margin_pct"):
        if key in data and not 0 <= data[key] <= 100:
            fail(f"{key} must be between 0 and 100")
    for key in ("current_save_rate_pct", "current_recovery_rate_pct"):
        if data[key] >= 100:
            fail(f"{key} must be below 100")


def calculate(data):
    mrr = data["mrr"]
    churn = data["monthly_churn_rate_pct"] / 100
    voluntary_share = data["voluntary_churn_pct"] / 100
    cur_save, tgt_save = data["current_save_rate_pct"] / 100, data["target_save_rate_pct"] / 100
    cur_rec, tgt_rec = data["current_recovery_rate_pct"] / 100, data["target_recovery_rate_pct"] / 100
    post_churn = data.get("post_save_monthly_churn_pct", data["monthly_churn_rate_pct"]) / 100
    months = int(data.get("months", 12))
    if months < 1:
        fail("months must be 1 or more")

    churned = mrr * churn
    voluntary_lost = churned * voluntary_share
    involuntary_lost = churned - voluntary_lost
    cancel_attempts = voluntary_lost / (1 - cur_save)
    failed_payments = involuntary_lost / (1 - cur_rec)
    save_gain = cancel_attempts * (tgt_save - cur_save)
    recovery_gain = failed_payments * (tgt_rec - cur_rec)
    monthly_gain = save_gain + recovery_gain

    # Each month's extra saves keep paying, decaying at the post-save churn rate.
    revenue_retained, run_rate = 0.0, 0.0
    for _ in range(months):
        revenue_retained += run_rate
        run_rate = run_rate * (1 - post_churn) + monthly_gain

    if save_gain > recovery_gain * 1.5:
        focus = "cancel flow and save offers"
    elif recovery_gain > save_gain * 1.5:
        focus = "dunning and payment recovery"
    else:
        focus = "both are similar; start with dunning (usually faster to fix)"

    flags = []
    if churn > 0.05:
        flags.append("Monthly churn above 5%: review product fit and ICP alongside retention work.")
    if tgt_save < cur_save or tgt_rec < cur_rec:
        flags.append("A target is below the current rate; the gain for that lever is negative.")

    result = {
        "baseline": {
            "mrr": mrr,
            "churned_mrr_per_month": round(churned, 2),
            "voluntary_churned_mrr": round(voluntary_lost, 2),
            "involuntary_churned_mrr": round(involuntary_lost, 2),
            "mrr_reaching_cancel_flow": round(cancel_attempts, 2),
            "mrr_in_failed_payments": round(failed_payments, 2),
        },
        "gain_per_month": {
            "from_save_rate": round(save_gain, 2),
            "from_recovery_rate": round(recovery_gain, 2),
            "total": round(monthly_gain, 2),
            "churn_rate_after_pct": round((churned - monthly_gain) / mrr * 100, 2) if mrr else None,
        },
        "over_window": {
            "months": months,
            "post_save_monthly_churn_pct": round(post_churn * 100, 2),
            "extra_mrr_at_end": round(run_rate, 2),
            "extra_revenue_retained": round(revenue_retained, 2),
        },
        "focus": focus,
        "flags": flags,
    }
    if "avg_customer_mrr" in data and data["avg_customer_mrr"] > 0:
        result["gain_per_month"]["customers_kept"] = round(monthly_gain / data["avg_customer_mrr"], 1)
    if "gross_margin_pct" in data:
        result["over_window"]["extra_contribution_retained"] = round(
            revenue_retained * data["gross_margin_pct"] / 100, 2)
    return result


def money(value, currency, decimals=0):
    text = f"{value:,.{decimals}f}"
    return f"{text} {currency}" if currency else text


def print_report(result, currency, sample):
    line = "=" * 64
    print(line)
    print("CHURN IMPACT" + ("  (SAMPLE DATA)" if sample else ""))
    print(line)
    b = result["baseline"]
    print("\nBaseline per month")
    print(f"  MRR:                        {money(b['mrr'], currency)}")
    print(f"  Churned MRR:                {money(b['churned_mrr_per_month'], currency)} "
          f"(voluntary {money(b['voluntary_churned_mrr'], currency)}, "
          f"involuntary {money(b['involuntary_churned_mrr'], currency)})")
    print(f"  Reaching the cancel flow:   {money(b['mrr_reaching_cancel_flow'], currency)}")
    print(f"  In failed payments:         {money(b['mrr_in_failed_payments'], currency)}")
    g = result["gain_per_month"]
    print("\nExtra MRR kept each month at target rates")
    print(f"  From save rate:             {money(g['from_save_rate'], currency)}")
    print(f"  From recovery rate:         {money(g['from_recovery_rate'], currency)}")
    print(f"  Total:                      {money(g['total'], currency)}"
          + (f" ({g['customers_kept']} customers)" if "customers_kept" in g else ""))
    print(f"  Monthly churn after:        {g['churn_rate_after_pct']}%")
    w = result["over_window"]
    print(f"\nOver {w['months']} months (saved customers then churn at {w['post_save_monthly_churn_pct']}%/month)")
    print(f"  Extra MRR at the end:       {money(w['extra_mrr_at_end'], currency)}")
    print(f"  Extra revenue retained:     {money(w['extra_revenue_retained'], currency)}")
    if "extra_contribution_retained" in w:
        print(f"  Extra contribution:         {money(w['extra_contribution_retained'], currency)}")
    print(f"\nFocus first on: {result['focus']}")
    for flag in result["flags"]:
        print(f"  - {flag}")
    print(line)


def main():
    parser = argparse.ArgumentParser(
        description="Size the MRR at stake from better cancel-flow save rates and dunning recovery rates.",
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
    validate(data)
    result = calculate(data)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result, args.currency, args.sample)


if __name__ == "__main__":
    main()
