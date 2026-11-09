#!/usr/bin/env python3
"""Activation funnel analyzer for onboarding.

Reads user counts for each onboarding step, in order (signup completed through
activation), and reports per-step drop-off, users lost and conversion from the
first step. It names the step with the worst drop-off rate and the step that
loses the most users, then projects what recovering part of the worst step's
drop-off would add to activation.

Usage:
  python3 activation_funnel_analyzer.py funnel.json                 # text report
  python3 activation_funnel_analyzer.py funnel.json --json          # JSON
  python3 activation_funnel_analyzer.py funnel.json --recover 0.3   # recover 30%, not 50%
  python3 activation_funnel_analyzer.py                             # demo funnel

Input: {"steps": [{"name": "Signup completed", "users": 1000}, ...]} in funnel
order, or a bare list of steps; "step" and "count" are accepted too. Every step
must count the same signup cohort, so counts never rise from one step to the next.

The projection is an upper bound: it assumes recovered users move through the
later steps at today's rates, and users won back at a hard step are often less
engaged than those who passed it unaided.

Reads only the file you pass. Writes nothing; prints to stdout.
Adapted from alirezarezvani/claude-skills, marketing-skill/onboarding-cro (MIT).
"""

import argparse
import json


def load_steps(data):
    """Normalize the input into [{"name", "users"}] and validate it."""
    if isinstance(data, dict):
        data = data.get("steps")
    if not isinstance(data, list) or len(data) < 2:
        raise ValueError("input must contain at least 2 steps: {\"steps\": [...]} or a list")
    steps = []
    for i, raw in enumerate(data, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"step {i} is not an object")
        name = raw.get("name", raw.get("step"))
        users = raw.get("users", raw.get("count"))
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"step {i} needs a \"name\" (or \"step\") string")
        if isinstance(users, bool) or not isinstance(users, (int, float)) or users < 0:
            raise ValueError(f"step {i} ('{name}') needs a non-negative \"users\" (or \"count\")")
        steps.append({"name": name.strip(), "users": int(users)})
    if steps[0]["users"] <= 0:
        raise ValueError("the first step must have more than 0 users")
    for prev, cur in zip(steps, steps[1:]):
        if cur["users"] > prev["users"]:
            raise ValueError(f"'{cur['name']}' ({cur['users']}) is higher than '{prev['name']}' "
                             f"({prev['users']}): list steps in funnel order and count one cohort")
    return steps


def analyze(steps, recover):
    start = steps[0]["users"]
    rows = []
    for i, s in enumerate(steps):
        prev = steps[i - 1]["users"] if i else s["users"]
        lost = prev - s["users"]
        rows.append({
            "step": s["name"],
            "users": s["users"],
            "from_start_pct": round(s["users"] / start * 100, 1),
            "drop_pct": round(lost / prev * 100, 1) if i and prev else 0.0,
            "lost": lost,
        })

    later = list(range(1, len(rows)))
    worst = max(later, key=lambda i: (rows[i]["drop_pct"], rows[i]["lost"]))
    biggest = max(later, key=lambda i: (rows[i]["lost"], rows[i]["drop_pct"]))

    projection = None
    if rows[worst]["lost"] > 0:
        regained = int(rows[worst]["lost"] * recover)
        # Carry the regained users through the later steps at today's step rates.
        carry = 1.0
        for j in range(worst + 1, len(steps)):
            before = steps[j - 1]["users"]
            carry *= steps[j]["users"] / before if before else 0.0
        extra = int(regained * carry)
        final = steps[-1]["users"]
        projection = {
            "step": rows[worst]["step"],
            "recover_share_of_drop": recover,
            "drop_pct_now": rows[worst]["drop_pct"],
            "drop_pct_after": round(rows[worst]["drop_pct"] * (1 - recover), 1),
            "users_regained_at_step": regained,
            "extra_users_at_last_step": extra,
            "last_step_conversion_pct_now": round(final / start * 100, 1),
            "last_step_conversion_pct_after": round((final + extra) / start * 100, 1),
            "note": "Upper bound: assumes regained users convert downstream at today's rates.",
        }

    any_loss = rows[biggest]["lost"] > 0
    return {
        "summary": {
            "start_users": start,
            "last_step": rows[-1]["step"],
            "last_step_users": rows[-1]["users"],
            "overall_conversion_pct": rows[-1]["from_start_pct"],
            "worst_drop_step": rows[worst]["step"] if any_loss else None,
            "worst_drop_pct": rows[worst]["drop_pct"],
            "most_users_lost_step": rows[biggest]["step"] if any_loss else None,
            "most_users_lost": rows[biggest]["lost"],
        },
        "steps": rows,
        "projection": projection,
    }


def print_report(result):
    s = result["summary"]
    rows = result["steps"]
    print()
    print("ONBOARDING ACTIVATION FUNNEL")
    print("=" * 70)
    print(f"  {s['start_users']:,} -> {s['last_step_users']:,} reached '{s['last_step']}' "
          f"({s['overall_conversion_pct']}% of the first step)")
    if s["worst_drop_step"] is None:
        print("  No users lost between steps.")
    else:
        print(f"  Worst drop rate : {s['worst_drop_step']} ({s['worst_drop_pct']}% of the step before)")
        print(f"  Most users lost : {s['most_users_lost_step']} ({s['most_users_lost']:,} users)")
    print()
    top = rows[0]["users"]
    for r in rows:
        bar = "#" * int(r["users"] / top * 40) if top else ""
        mark = "  <- worst drop" if r["step"] == s["worst_drop_step"] else ""
        drop = f" (-{r['drop_pct']}%)" if r["drop_pct"] > 0 else ""
        print(f"  {bar:<40} {r['users']:>7,}  {r['step']}{drop}{mark}")
    print()
    print(f"  {'Step':<30} {'Users':>8} {'From start':>11} {'Drop':>8} {'Lost':>8}")
    print("  " + "-" * 69)
    for r in rows:
        drop = f"-{r['drop_pct']}%" if r["drop_pct"] > 0 else "-"
        lost = f"-{r['lost']:,}" if r["lost"] > 0 else "-"
        print(f"  {r['step'][:30]:<30} {r['users']:>8,} {r['from_start_pct']:>10.1f}% {drop:>8} {lost:>8}")
    p = result["projection"]
    if p:
        print()
        print(f"  WHAT IF: recover {p['recover_share_of_drop']:.0%} of the drop at '{p['step']}'")
        print(f"    Drop at step       : {p['drop_pct_now']}% -> {p['drop_pct_after']}%")
        print(f"    Users regained     : +{p['users_regained_at_step']:,} at the step")
        print(f"    Extra at last step : +{p['extra_users_at_last_step']:,} "
              f"({p['last_step_conversion_pct_now']}% -> {p['last_step_conversion_pct_after']}% of the first step)")
        print(f"    {p['note']}")
    print()


SAMPLE_DATA = {
    "steps": [
        {"name": "Signup completed", "users": 1000},
        {"name": "Email verified", "users": 840},
        {"name": "Profile setup", "users": 580},
        {"name": "First project created", "users": 290},
        {"name": "Invited teammate", "users": 145},
        {"name": "Aha moment (day 3)", "users": 95},
        {"name": "Activated (day 7)", "users": 72},
    ]
}


def main():
    parser = argparse.ArgumentParser(
        description="Find where onboarding loses users and project the gain from fixing the worst step.",
        epilog="With no file, runs on a demo SaaS onboarding funnel.",
    )
    parser.add_argument("file", nargs="?", help="JSON file with the funnel steps")
    parser.add_argument("--recover", type=float, default=0.5, metavar="SHARE",
                        help="share of the worst step's drop-off to recover in the projection, "
                             "between 0 and 1 (default 0.5)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    args = parser.parse_args()

    if not 0 < args.recover <= 1:
        parser.error("--recover must be above 0 and at most 1")
    try:
        if args.file:
            with open(args.file, encoding="utf-8") as fh:
                data = json.load(fh)
        else:
            if not args.json:
                print("Demo mode: sample SaaS onboarding funnel.")
            data = SAMPLE_DATA
        result = analyze(load_steps(data), args.recover)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
