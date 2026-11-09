#!/usr/bin/env python3
"""Referral program economics: funnel volume, CAC via referral, affordable reward and contribution return.

Adapted from alirezarezvani/claude-skills (MIT), marketing-skill/referral-program/scripts/referral_roi_calculator.py.
The economics follow this skill's references/program-examples.md: reward budget = target CAC minus other
acquisition cost, and return = (incremental contribution - program costs) / program costs.
Stdlib only. Reads a JSON file (or stdin with "-") and prints a report to stdout. No network, no file writes.

Input JSON (money in any one currency; rates as fractions, 0.05 = 5%):
  {
    "active_users": 800,                 required: users who could refer
    "referral_rate": 0.06,               required: share of active users who refer in a month
    "referrals_per_referrer": 2.0,       required: invitations per active referrer per month
    "referral_conversion_rate": 0.20,    required: share of invitations that become paying customers
    "referrer_reward": 50,               required: reward per converted referral, face value
    "referred_reward": 30,               optional: reward to the new customer (default 0, single-sided)
    "reward_cost_ratio": 1.0,            optional: economic cost per unit of face value (credits and free
                                                   months usually cost less than face value; default 1.0)
    "program_overhead_monthly": 200,     optional: tools, operations, amortized engineering (default 0)
    "ltv": 1200,                         required: lifetime revenue per customer
    "gross_margin_pct": 70,              required: turns revenue into contribution
    "paid_cac": 350,                     required: current CAC of paid channels ("cac" also accepted)
    "target_cac": 175,                   optional: default target_cac_ratio x paid_cac
    "target_cac_ratio": 0.5,             optional: default 0.5
    "incremental_share": 1.0,            optional: share of referred customers who would NOT have bought
                                                   anyway (default 1.0 = all incremental; measure it)
    "monthly_churn_rate": 0.04,          optional: enables a cash payback month
    "months": 12                         optional: modeling window (default 12)
  }
"""

import argparse
import json
import sys

SAMPLE_INPUT = {
    "active_users": 800,
    "referral_rate": 0.06,
    "referrals_per_referrer": 2.0,
    "referral_conversion_rate": 0.20,
    "referrer_reward": 50,
    "referred_reward": 30,
    "program_overhead_monthly": 200,
    "ltv": 1200,
    "gross_margin_pct": 70,
    "paid_cac": 350,
    "incremental_share": 0.7,
    "monthly_churn_rate": 0.04,
    "months": 12,
}

REQUIRED_KEYS = ("active_users", "referral_rate", "referrals_per_referrer", "referral_conversion_rate",
                 "referrer_reward", "ltv", "gross_margin_pct")
FRACTION_KEYS = ("referral_rate", "referral_conversion_rate", "incremental_share", "monthly_churn_rate",
                 "reward_cost_ratio", "target_cac_ratio")


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
    if "paid_cac" not in data and "cac" not in data:
        missing.append("paid_cac")
    if missing:
        fail(f"missing required keys: {', '.join(missing)}")
    for key in FRACTION_KEYS:
        if key in data and not 0 <= data[key] <= 1:
            fail(f"{key} must be a fraction between 0 and 1 (0.05 = 5%)")
    if not 0 < data["gross_margin_pct"] <= 100:
        fail("gross_margin_pct must be between 0 and 100")


def calculate(data):
    paid_cac = data.get("paid_cac", data.get("cac"))
    months = int(data.get("months", 12))
    if months < 1:
        fail("months must be 1 or more")
    incremental_share = data.get("incremental_share", 1.0)
    cost_ratio = data.get("reward_cost_ratio", 1.0)
    overhead = data.get("program_overhead_monthly", 0)
    target_cac = data.get("target_cac", data.get("target_cac_ratio", 0.5) * paid_cac)
    contribution_per_customer = data["ltv"] * data["gross_margin_pct"] / 100

    active_referrers = data["active_users"] * data["referral_rate"]
    invitations = active_referrers * data["referrals_per_referrer"]
    conversions = invitations * data["referral_conversion_rate"]
    incremental = conversions * incremental_share
    reward_face = data["referrer_reward"] + data.get("referred_reward", 0)
    reward_cost = reward_face * cost_ratio
    monthly_cost = reward_cost * conversions + overhead

    def per(total, count):
        return round(total / count, 2) if count > 0 else None

    other_cost_per_conversion = per(overhead, conversions)
    max_reward = None
    if other_cost_per_conversion is not None:
        max_reward = round(max(0.0, target_cac - other_cost_per_conversion), 2)

    # Referral rate at which attributed CAC reaches the target: reward + overhead / conversions = target.
    breakeven_rate = None
    per_rate = data["active_users"] * data["referrals_per_referrer"] * data["referral_conversion_rate"]
    if target_cac > reward_cost and per_rate > 0:
        breakeven_rate = round(overhead / (target_cac - reward_cost) / per_rate, 4)

    total_cost = monthly_cost * months
    lifetime_contribution = incremental * months * contribution_per_customer
    roi = round((lifetime_contribution - total_cost) / total_cost * 100, 1) if total_cost > 0 else None

    payback_month = None
    observed_contribution = None
    churn = data.get("monthly_churn_rate")
    if churn:
        # Steady state: lifetime contribution = monthly contribution / churn.
        monthly_contribution = contribution_per_customer * churn
        active, cumulative_value, cumulative_cost = 0.0, 0.0, 0.0
        for month in range(1, months + 1):
            active = active * (1 - churn) + incremental
            cumulative_value += active * monthly_contribution
            cumulative_cost += monthly_cost
            if payback_month is None and cumulative_value >= cumulative_cost:
                payback_month = month
        observed_contribution = round(cumulative_value, 2)

    return {
        "funnel_per_month": {
            "active_referrers": round(active_referrers, 1),
            "invitations": round(invitations, 1),
            "attributed_customers": round(conversions, 2),
            "incremental_customers": round(incremental, 2),
            "k_factor_per_active_user": round(data["referral_rate"] * data["referrals_per_referrer"]
                                              * data["referral_conversion_rate"], 4),
        },
        "costs_per_month": {
            "reward_economic_cost": round(reward_cost * conversions, 2),
            "overhead": round(overhead, 2),
            "total": round(monthly_cost, 2),
        },
        "cac": {
            "paid_cac": paid_cac,
            "target_cac": round(target_cac, 2),
            "referral_cac_attributed": per(monthly_cost, conversions),
            "referral_cac_incremental": per(monthly_cost, incremental),
        },
        "reward_sizing": {
            "current_reward_face_value": reward_face,
            "current_reward_economic_cost": round(reward_cost, 2),
            "max_affordable_reward_economic_cost": max_reward,
            "break_even_referral_rate_for_target_cac": breakeven_rate,
            "current_referral_rate": data["referral_rate"],
        },
        "return_over_window": {
            "months": months,
            "program_costs": round(total_cost, 2),
            "projected_lifetime_contribution_incremental": round(lifetime_contribution, 2),
            "contribution_return_pct": roi,
            "contribution_observed_in_window": observed_contribution,
            "cash_payback_month": payback_month,
        },
        "assumptions": {
            "incremental_share": incremental_share,
            "incremental_share_measured": "incremental_share" in data,
            "reward_cost_ratio": cost_ratio,
            "steady_monthly_volume": True,
        },
    }


def money(value, currency, decimals=2):
    if value is None:
        return "n/a"
    text = f"{value:,.{decimals}f}"
    return f"{text} {currency}" if currency else text


def print_report(result, currency, sample):
    line = "=" * 68
    print(line)
    print("REFERRAL PROGRAM ECONOMICS" + ("  (SAMPLE DATA)" if sample else ""))
    print(line)
    f = result["funnel_per_month"]
    print("\nFunnel per month")
    print(f"  Active referrers:        {f['active_referrers']}")
    print(f"  Invitations:             {f['invitations']}")
    print(f"  Attributed customers:    {f['attributed_customers']}")
    print(f"  Incremental customers:   {f['incremental_customers']}")
    print(f"  K per active user:       {f['k_factor_per_active_user']} (K > 1 means self-sustaining growth)")

    c = result["costs_per_month"]
    cac = result["cac"]
    print("\nCost and CAC per month")
    print(f"  Reward cost:             {money(c['reward_economic_cost'], currency)}")
    print(f"  Overhead:                {money(c['overhead'], currency)}")
    print(f"  CAC via referral:        {money(cac['referral_cac_attributed'], currency)} attributed, "
          f"{money(cac['referral_cac_incremental'], currency)} incremental")
    print(f"  Paid CAC / target CAC:   {money(cac['paid_cac'], currency)} / {money(cac['target_cac'], currency)}")

    r = result["reward_sizing"]
    print("\nReward sizing")
    print(f"  Current reward:          {money(r['current_reward_face_value'], currency)} face value, "
          f"{money(r['current_reward_economic_cost'], currency)} economic cost")
    print(f"  Max affordable reward:   {money(r['max_affordable_reward_economic_cost'], currency)} "
          "(target CAC minus overhead per customer)")
    if r["break_even_referral_rate_for_target_cac"] is None:
        print("  Break-even referral rate: not reachable; the reward alone meets or exceeds the target CAC")
    else:
        print(f"  Referral rate needed for target CAC: {r['break_even_referral_rate_for_target_cac'] * 100:.2f}% "
              f"(now {r['current_referral_rate'] * 100:.2f}%)")

    w = result["return_over_window"]
    print(f"\nReturn over {w['months']} months")
    print(f"  Program costs:                         {money(w['program_costs'], currency, 0)}")
    print(f"  Projected lifetime contribution:       {money(w['projected_lifetime_contribution_incremental'], currency, 0)}")
    roi = "n/a" if w["contribution_return_pct"] is None else f"{w['contribution_return_pct']}%"
    print(f"  Contribution return:                   {roi}")
    if w["contribution_observed_in_window"] is not None:
        print(f"  Contribution observed in the window:   {money(w['contribution_observed_in_window'], currency, 0)}")
        payback = w["cash_payback_month"]
        print(f"  Cash payback month:                    {payback if payback else 'not reached in the window'}")

    a = result["assumptions"]
    print("\nAssumptions")
    if not a["incremental_share_measured"]:
        print("  - All referred customers are treated as incremental. Attribution is not incrementality;")
        print("    label this 'attributed contribution return' unless a holdout supports it.")
    else:
        print(f"  - Incremental share {a['incremental_share']} (state how it was measured).")
    print(f"  - Reward economic cost = {a['reward_cost_ratio']} x face value; steady monthly volume.")
    print(line)


def main():
    parser = argparse.ArgumentParser(
        description="Model referral program funnel volume, CAC, affordable reward and contribution return.",
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
