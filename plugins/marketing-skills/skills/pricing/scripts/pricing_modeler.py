#!/usr/bin/env python3
"""Pricing modeler: revenue scenarios for a price change, a cost floor and a starting tier ladder.

Adapted from alirezarezvani/claude-skills (MIT), marketing-skill/pricing-strategy/scripts/pricing_modeler.py.
Stdlib only. Reads a JSON file (or stdin with "-") and prints a report to stdout. No network, no file writes.

Input JSON (prices and costs are per customer per month, in any one currency):
  {
    "current_plans": [                         required
      {"name": "Starter", "price": 29, "customer_count": 180},
      {"name": "Pro", "price": 79, "customer_count": 100}
    ],
    "monthly_new_customers": 25,               required
    "monthly_churn_rate_pct": 3.5,             required
    "trial_to_paid_rate_pct": 18,              optional: enables the conversion signal
    "trial_requires_card": false,              optional: card-required trials convert higher by design
    "competitor_prices": [49, 89, 249],        optional: monthly list prices of real alternatives
    "cogs_per_customer_monthly": 8,            optional: cost to serve; enables the cost floor
    "target_gross_margin_pct": 75,             optional: used with the cost floor (default 75)
    "price_increases_pct": [5, 15, 25],        optional: scenarios to model (default 5, 15, 25)
    "increase_churn_leak": 0.25,               optional: ASSUMPTION, see below (default 0.25)
    "tier_ratio": 2.5,                         optional: step between ladder tiers (default 2.5)
    "months": 12                               optional: projection length (default 12)
  }

Model assumptions (state them when you report results):
  - A price increase of x% applied to existing customers causes a one-time extra churn of
    x% * increase_churn_leak. The default 0.25 is a placeholder, not a benchmark: replace it with your
    own data from a past change or a small rollout.
  - New-customer volume and monthly churn stay constant after the change.
  - "New customers only" scenarios keep existing customers on their current price.
"""

import argparse
import json
import math
import sys

SAMPLE_INPUT = {
    "current_plans": [
        {"name": "Starter", "price": 29, "customer_count": 180},
        {"name": "Pro", "price": 79, "customer_count": 100},
        {"name": "Business", "price": 199, "customer_count": 20},
    ],
    "monthly_new_customers": 25,
    "monthly_churn_rate_pct": 3.5,
    "trial_to_paid_rate_pct": 18,
    "competitor_prices": [49, 89, 249],
    "cogs_per_customer_monthly": 8,
    "target_gross_margin_pct": 75,
}

REQUIRED_KEYS = ("current_plans", "monthly_new_customers", "monthly_churn_rate_pct")


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
    plans = data["current_plans"]
    if not isinstance(plans, list) or not plans:
        fail("current_plans must be a non-empty list")
    for plan in plans:
        for key in ("name", "price", "customer_count"):
            if key not in plan:
                fail(f"each plan needs name, price and customer_count (missing {key})")
        if plan["price"] < 0 or plan["customer_count"] < 0:
            fail("plan price and customer_count must be zero or more")
    if sum(p["customer_count"] for p in plans) <= 0:
        fail("current_plans has no customers")
    if not 0 <= data["monthly_churn_rate_pct"] < 100:
        fail("monthly_churn_rate_pct must be between 0 and 100")


def two_sig(value):
    """Round to two significant figures, so the ladder stays currency-neutral."""
    if value <= 0:
        return 0.0
    exponent = math.floor(math.log10(value)) - 1
    step = 10 ** exponent
    return round(math.floor(value / step + 0.5) * step, max(0, -exponent))


def project(base_customers, old_arpu, new_arpu, new_per_month, churn, months, leak, apply_to):
    """Return MRR per month and total revenue for one scenario."""
    increase = (new_arpu - old_arpu) / old_arpu if old_arpu > 0 else 0.0
    one_time_churn = max(0.0, increase) * leak if apply_to == "all" else 0.0
    existing = base_customers * (1 - one_time_churn)
    existing_arpu = new_arpu if apply_to == "all" else old_arpu
    newer = 0.0
    series = []
    for _ in range(months):
        series.append(existing * existing_arpu + newer * new_arpu)
        existing *= 1 - churn
        newer = newer * (1 - churn) + new_per_month
    return {
        "one_time_churn_pct": round(one_time_churn * 100, 1),
        "mrr_by_month": [round(v, 2) for v in series],
        "total_revenue": round(sum(series), 2),
    }


def conversion_signal(rate, card_required):
    if rate > 40:
        label, step = "likely underpriced", "test a 20-30% increase on new customers first"
    elif rate > 30:
        label, step = "possible headroom", "test a modest increase on new customers"
    elif rate >= 15:
        label, step = "healthy range", "focus on value metric and packaging before the number"
    elif rate >= 10:
        label, step = "possible price friction", "audit the trial experience before cutting price"
    else:
        label, step = "high friction", "check pricing, trial experience and customer fit"
    note = ("Bands assume an opt-in trial (no card). Card-required trials convert higher by design, "
            "so read this against that baseline.") if card_required else \
        "Bands assume an opt-in trial (no card)."
    return {"trial_to_paid_rate_pct": rate, "signal": label, "next_step": step, "note": note}


def model(data, leak_override=None):
    plans = data["current_plans"]
    customers = sum(p["customer_count"] for p in plans)
    mrr = sum(p["price"] * p["customer_count"] for p in plans)
    arpu = mrr / customers
    churn = data["monthly_churn_rate_pct"] / 100
    new_per_month = data["monthly_new_customers"]
    months = int(data.get("months", 12))
    if months < 1:
        fail("months must be 1 or more")
    leak = leak_override if leak_override is not None else data.get("increase_churn_leak", 0.25)
    increases = data.get("price_increases_pct", [5, 15, 25])

    warnings = []
    if "current_mrr" in data and abs(data["current_mrr"] - mrr) > 0.01 * max(mrr, 1):
        warnings.append(f"current_mrr ({data['current_mrr']}) differs from the plan sum ({round(mrr, 2)}); "
                        "the plan sum is used")
    if "current_customers" in data and data["current_customers"] != customers:
        warnings.append(f"current_customers ({data['current_customers']}) differs from the plan sum "
                        f"({customers}); the plan sum is used")

    result = {
        "current_state": {
            "mrr": round(mrr, 2),
            "customers": customers,
            "arpu": round(arpu, 2),
            "monthly_churn_rate_pct": data["monthly_churn_rate_pct"],
        },
        "assumptions": {
            "increase_churn_leak": leak,
            "new_customer_volume": "constant",
            "months": months,
        },
        "warnings": warnings,
    }

    cogs = data.get("cogs_per_customer_monthly")
    floor = None
    if cogs is not None:
        margin_target = data.get("target_gross_margin_pct", 75)
        if not 0 <= margin_target < 100:
            fail("target_gross_margin_pct must be between 0 and 100")
        floor = cogs / (1 - margin_target / 100)
        result["cost_floor"] = {
            "cost_to_serve": cogs,
            "target_gross_margin_pct": margin_target,
            "minimum_price": round(floor, 2),
            "current_gross_margin_pct": round((arpu - cogs) / arpu * 100, 1) if arpu > 0 else None,
            "plans_below_floor": [p["name"] for p in plans if p["price"] < floor],
        }

    competitors = data.get("competitor_prices") or []
    if competitors:
        average = sum(competitors) / len(competitors)
        gap = (arpu - average) / average if average > 0 else 0.0
        position = "at market" if abs(gap) < 0.15 else ("below market" if gap < 0 else "above market")
        result["market"] = {
            "competitor_min": min(competitors),
            "competitor_max": max(competitors),
            "competitor_average": round(average, 2),
            "arpu_vs_average_pct": round(gap * 100, 1),
            "arpu_position": position,
        }

    if floor is not None or competitors:
        ratio = data.get("tier_ratio", 2.5)
        entry = max(floor or 0.0, 0.9 * min(competitors) if competitors else 0.0)
        result["starting_ladder"] = {
            "basis": "max(cost floor, 0.9 x lowest competitor price), then x tier_ratio per step",
            "tier_ratio": ratio,
            "good": two_sig(entry),
            "better": two_sig(entry * ratio),
            "best": two_sig(entry * ratio * ratio),
            "note": "A sanity ladder for discussion, not a recommendation: set prices from value "
                    "research, then choose charm or round endings deliberately.",
        }

    rate = data.get("trial_to_paid_rate_pct")
    if rate is not None:
        result["conversion_signal"] = conversion_signal(rate, bool(data.get("trial_requires_card", False)))

    scenarios = []
    for pct in [0] + [p for p in increases if p != 0]:
        new_arpu = arpu * (1 + pct / 100)
        everyone = project(customers, arpu, new_arpu, new_per_month, churn, months, leak, "all")
        new_only = project(customers, arpu, new_arpu, new_per_month, churn, months, leak, "new")
        increase = pct / 100
        scenarios.append({
            "price_change_pct": pct,
            "arpu": round(new_arpu, 2),
            "break_even_one_time_churn_pct": round(increase / (1 + increase) * 100, 1) if increase > 0 else None,
            "existing_base_mrr_at_retention": {
                f"{r}%": round(customers * r / 100 * new_arpu, 2) for r in (100, 90, 80, 70)
            },
            "all_customers": everyone,
            "new_customers_only": new_only,
        })
    result["scenarios"] = scenarios
    return result


def money(value, currency, decimals=2):
    text = f"{value:,.{decimals}f}"
    return f"{text} {currency}" if currency else text


def print_report(result, currency, sample):
    line = "=" * 72
    print(line)
    print("PRICING MODELER" + ("  (SAMPLE DATA)" if sample else ""))
    print(line)
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    cur = result["current_state"]
    print("\nCurrent state")
    print(f"  MRR:            {money(cur['mrr'], currency, 0)}")
    print(f"  Customers:      {cur['customers']}")
    print(f"  ARPU:           {money(cur['arpu'], currency)} per month")
    print(f"  Monthly churn:  {cur['monthly_churn_rate_pct']}%")

    if "cost_floor" in result:
        floor = result["cost_floor"]
        print("\nCost floor")
        print(f"  Minimum price at {floor['target_gross_margin_pct']}% gross margin: "
              f"{money(floor['minimum_price'], currency)}")
        print(f"  Current gross margin: {floor['current_gross_margin_pct']}%")
        if floor["plans_below_floor"]:
            print(f"  Plans below the floor: {', '.join(floor['plans_below_floor'])}")

    if "market" in result:
        market = result["market"]
        print("\nMarket")
        print(f"  Competitor range: {money(market['competitor_min'], currency)} to "
              f"{money(market['competitor_max'], currency)} (average {money(market['competitor_average'], currency)})")
        print(f"  ARPU vs. average: {market['arpu_vs_average_pct']}% ({market['arpu_position']})")
        print("  Competitor prices are a data point, not a target.")

    if "starting_ladder" in result:
        ladder = result["starting_ladder"]
        print("\nStarting ladder (sanity check only)")
        print(f"  Good {money(ladder['good'], currency)} | Better {money(ladder['better'], currency)} | "
              f"Best {money(ladder['best'], currency)}  (ratio {ladder['tier_ratio']})")
        print(f"  {ladder['note']}")

    if "conversion_signal" in result:
        signal = result["conversion_signal"]
        print("\nConversion signal")
        print(f"  Trial-to-paid {signal['trial_to_paid_rate_pct']}%: {signal['signal']}; {signal['next_step']}.")
        print(f"  {signal['note']}")

    months = result["assumptions"]["months"]
    print(f"\nScenarios over {months} months (one-time churn leak assumption: "
          f"{result['assumptions']['increase_churn_leak']})")
    header = f"  {'Change':>7} {'ARPU':>12} {'Break-even churn':>17} {'Revenue (all)':>16} {'Revenue (new only)':>19}"
    print(header)
    print("  " + "-" * (len(header) - 2))
    for s in result["scenarios"]:
        breakeven = f"{s['break_even_one_time_churn_pct']}%" if s["break_even_one_time_churn_pct"] is not None else "-"
        print(f"  {s['price_change_pct']:>6}% {money(s['arpu'], currency):>12} {breakeven:>17} "
              f"{money(s['all_customers']['total_revenue'], currency, 0):>16} "
              f"{money(s['new_customers_only']['total_revenue'], currency, 0):>19}")
    print("\n  Break-even churn: the one-time loss of existing customers at which the increase")
    print("  leaves existing-base MRR unchanged. Compare it with the churn you expect.")
    base = result["scenarios"][0]["all_customers"]["total_revenue"]
    best = max(result["scenarios"], key=lambda s: s["all_customers"]["total_revenue"])
    print(f"\n  Highest modeled revenue: {best['price_change_pct']}% change "
          f"({money(best['all_customers']['total_revenue'] - base, currency, 0)} vs. no change).")
    print("  The ranking depends on the churn-leak assumption; new-customer volume and churn are")
    print("  held constant. Test on new customers first.")
    print(line)


def main():
    parser = argparse.ArgumentParser(
        description="Model revenue scenarios for a price change, a cost floor and a starting tier ladder.",
        epilog="Input format and assumptions are documented at the top of this file.",
    )
    parser.add_argument("input", nargs="?", help="JSON input file, or - to read stdin")
    parser.add_argument("--sample", action="store_true", help="run with built-in sample data")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    parser.add_argument("--currency", default="", help="label for amounts, e.g. a currency code (default: none)")
    parser.add_argument("--churn-leak", type=float, default=None,
                        help="override increase_churn_leak (share of the increase lost as one-time churn)")
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
    result = model(data, args.churn_leak)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result, args.currency, args.sample)


if __name__ == "__main__":
    main()
