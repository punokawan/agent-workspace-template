#!/usr/bin/env python3
"""A/B test sample size and duration calculator.

Computes the sample per variant for a conversion-rate test (two-proportion
z-test, two-sided, fixed horizon) from the baseline rate and the relative
minimum detectable effect (MDE). With --daily-traffic it also estimates how
many days collection takes, and it flags inputs that make a test impractical.

The variance is pooled under the null hypothesis, the same formula behind the
tables in references/sample-size-guide.md and common online calculators:

  n = [z(1-a/2) * sqrt(2 p(1-p)) + z(power) * sqrt(p1(1-p1) + p2(1-p2))]^2 / (p2 - p1)^2
  with p2 = p1 * (1 + MDE) and p = (p1 + p2) / 2

With more than two arms, alpha is split across the comparisons with control
(Bonferroni), which raises the sample per arm.

Usage:
  python3 sample_size_calculator.py --baseline 0.05 --mde 0.20
  python3 sample_size_calculator.py --baseline 0.05 --mde 0.20 --daily-traffic 2000
  python3 sample_size_calculator.py --baseline 0.05 --mde 0.20 --variants 3 --exposure 0.5 --daily-traffic 2000
  python3 sample_size_calculator.py --baseline 0.05 --mde 0.20 --json
  python3 sample_size_calculator.py            # demo scenarios

Writes nothing; prints to stdout.
Adapted from alirezarezvani/claude-skills, marketing-skill/ab-test-setup (MIT).
"""

import argparse
import json
import math
from statistics import NormalDist

FORMULA = ("n = [z(1-a/2)*sqrt(2p(1-p)) + z(power)*sqrt(p1(1-p1)+p2(1-p2))]^2 / (p2-p1)^2, "
           "p = (p1+p2)/2  [two-proportion z-test, two-sided, pooled variance under H0]")
ASSUMPTIONS = [
    "Fixed horizon: one analysis at the planned sample, no early stopping (not sequential).",
    "Binary outcome (converted or not), one observation per randomized unit.",
    "Independent units with equal allocation across arms.",
    "Relative MDE: p2 = baseline x (1 + MDE).",
    "No novelty-effect or seasonality correction.",
]


def calculate(baseline, mde, alpha=0.05, power=0.80, variants=2):
    p1 = baseline
    p2 = baseline * (1 + mde)
    if not 0 < p1 < 1:
        raise ValueError(f"--baseline must be between 0 and 1 (got {p1})")
    if mde == 0:
        raise ValueError("--mde must not be 0")
    if not 0 < p2 < 1:
        raise ValueError(f"baseline x (1 + mde) = {p2:.4f} falls outside 0-1; use a smaller --mde")
    if not 0 < alpha < 1:
        raise ValueError(f"--alpha must be between 0 and 1 (got {alpha})")
    if not 0 < power < 1:
        raise ValueError(f"--power must be between 0 and 1 (got {power})")
    if variants < 2:
        raise ValueError("--variants counts every arm including control, so it must be 2 or more")

    comparisons = variants - 1
    alpha_per = alpha / comparisons
    nd = NormalDist()
    z_alpha = nd.inv_cdf(1 - alpha_per / 2)
    z_power = nd.inv_cdf(power)
    p_bar = (p1 + p2) / 2
    n_raw = (z_alpha * math.sqrt(2 * p_bar * (1 - p_bar))
             + z_power * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2 / (p2 - p1) ** 2
    n = math.ceil(n_raw)
    return {
        "inputs": {
            "baseline_rate": p1,
            "mde_relative": mde,
            "variant_rate": round(p2, 6),
            "alpha": alpha,
            "alpha_per_comparison": round(alpha_per, 6),
            "power": power,
            "arms": variants,
        },
        "z_scores": {"z_alpha": round(z_alpha, 4), "z_power": round(z_power, 4)},
        "results": {
            "sample_per_variant": n,
            "total_sample": n * variants,
            "absolute_change": round(p2 - p1, 6),
        },
        "formula": FORMULA,
        "assumptions": ASSUMPTIONS,
    }


def add_duration(result, daily_traffic, exposure):
    if daily_traffic <= 0:
        raise ValueError("--daily-traffic must be above 0")
    if not 0 < exposure <= 1:
        raise ValueError("--exposure must be above 0 and at most 1")
    total = result["results"]["total_sample"]
    days = math.ceil(total / (daily_traffic * exposure))
    result["duration"] = {
        "daily_eligible_traffic": daily_traffic,
        "exposure": exposure,
        "days": days,
        "weeks": round(days / 7, 1),
        "formula": "days = sample per variant x arms / (daily eligible traffic x exposure)",
    }
    return result


def flags(result):
    """Warnings drawn from the duration and feasibility rules in references/sample-size-guide.md."""
    out = []
    i = result["inputs"]
    if i["baseline_rate"] < 0.01:
        out.append("Baseline under 1%: samples get very large; consider a higher-traffic or upstream metric.")
    if abs(i["mde_relative"]) < 0.05:
        out.append("MDE under 5% relative: needs a very large sample; confirm an effect this small is worth detecting.")
    if i["alpha"] > 0.10:
        out.append("Alpha above 0.10: high false-positive risk; document the choice.")
    if i["power"] < 0.80:
        out.append("Power below 80%: real effects of the MDE size are likely to be missed.")
    if i["arms"] >= 5:
        out.append("5 or more arms: consider testing fewer variants.")
    d = result.get("duration")
    if d:
        if d["days"] > 60:
            out.append(f"{d['days']:,} days: over 60 days, consider a larger MDE, an upstream metric, "
                       "fewer variants, or not testing.")
        elif d["days"] > 30:
            out.append(f"{d['days']:,} days: over 30 days is acceptable only for high-impact tests; "
                       "watch for novelty effects and outside events.")
        elif d["days"] < 7:
            out.append(f"{d['days']:,} days: run at least one full week (two business cycles for B2B) "
                       "to cover day-of-week swings.")
    return out


def print_report(result, label=None, details=True):
    i, r, z = result["inputs"], result["results"], result["z_scores"]
    print()
    print("A/B TEST SAMPLE SIZE" + (f" - {label}" if label else ""))
    print("=" * 64)
    print(f"  Baseline rate        : {i['baseline_rate'] * 100:.2f}%")
    print(f"  Variant rate         : {i['variant_rate'] * 100:.2f}%  "
          f"(MDE {i['mde_relative'] * 100:+.1f}% relative, {r['absolute_change'] * 100:+.3f} pp absolute)")
    alpha_note = ""
    if i["arms"] > 2:
        alpha_note = f"  ({i['alpha_per_comparison']} per comparison, Bonferroni over {i['arms'] - 1})"
    print(f"  Alpha (two-sided)    : {i['alpha']}{alpha_note}")
    print(f"  Power                : {i['power'] * 100:.0f}%")
    print(f"  Arms                 : {i['arms']} (control + {i['arms'] - 1} variant(s))")
    print(f"  z values             : z_alpha = {z['z_alpha']}, z_power = {z['z_power']}")
    print()
    print(f"  Sample per variant   : {r['sample_per_variant']:,}")
    print(f"  Total sample         : {r['total_sample']:,}")
    d = result.get("duration")
    if d:
        print(f"  Collection time      : {d['days']:,} days (about {d['weeks']} weeks) at "
              f"{d['daily_eligible_traffic']:,} eligible/day, {d['exposure']:.0%} exposed")
    if result["flags"]:
        print()
        print("  Flags:")
        for f in result["flags"]:
            print(f"    - {f}")
    print()
    if not details:
        return
    print(f"  Formula: {result['formula']}")
    print("  Assumptions:")
    for a in result["assumptions"]:
        print(f"    - {a}")
    print()


DEMO_SCENARIOS = [
    {"label": "Checkout, low baseline", "baseline": 0.03, "mde": 0.20, "daily_traffic": 800},
    {"label": "Free-trial signup, medium baseline", "baseline": 0.08, "mde": 0.15, "daily_traffic": 2000},
    {"label": "CTA click, high baseline", "baseline": 0.25, "mde": 0.10, "daily_traffic": 5000},
]


def run(args):
    result = calculate(args.baseline, args.mde, args.alpha, args.power, args.variants)
    if args.daily_traffic is not None:
        add_duration(result, args.daily_traffic, args.exposure)
    result["flags"] = flags(result)
    return result


def main():
    parser = argparse.ArgumentParser(
        description="Sample size and duration for a conversion-rate A/B test (stdlib only).",
        epilog="With neither --baseline nor --mde, runs three demo scenarios.",
    )
    parser.add_argument("--baseline", type=float, help="baseline conversion rate as a fraction, e.g. 0.05")
    parser.add_argument("--mde", type=float, help="minimum detectable effect as a relative lift, e.g. 0.20 for +20%%")
    parser.add_argument("--alpha", type=float, default=0.05, help="significance level, two-sided (default 0.05)")
    parser.add_argument("--power", type=float, default=0.80, help="statistical power (default 0.80)")
    parser.add_argument("--variants", type=int, default=2, help="number of arms including control (default 2)")
    parser.add_argument("--daily-traffic", type=int, help="eligible visitors or users per day, all arms together")
    parser.add_argument("--exposure", type=float, default=1.0,
                        help="share of eligible traffic entered into the test, 0-1 (default 1.0)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    args = parser.parse_args()

    try:
        if args.baseline is None and args.mde is None:
            results = []
            for sc in DEMO_SCENARIOS:
                args.baseline, args.mde, args.daily_traffic = sc["baseline"], sc["mde"], sc["daily_traffic"]
                res = run(args)
                res["scenario"] = sc["label"]
                results.append(res)
            if args.json:
                print(json.dumps(results, indent=2))
            else:
                print("Demo mode: three sample scenarios.")
                for n, res in enumerate(results, 1):
                    print_report(res, res["scenario"], details=n == len(results))
            return
        if args.baseline is None or args.mde is None:
            parser.error("--baseline and --mde go together (omit both for the demo)")
        result = run(args)
    except ValueError as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
