#!/usr/bin/env python3
"""Signup funnel drop-off analyzer.

Reads people counts for each step of a signup funnel, in order (for example:
landing visit, signup started, form submitted, email verified, first login),
and reports step conversion, step drop-off, people lost and cumulative
conversion. It names the step with the highest drop-off rate and the step that
loses the most people, and lists likely causes to check for each large drop.

Usage:
  python3 funnel_drop_analyzer.py --steps funnel.json          # text report
  python3 funnel_drop_analyzer.py --steps funnel.json --json   # JSON
  python3 funnel_drop_analyzer.py --stdin < funnel.json
  python3 funnel_drop_analyzer.py                              # demo funnel

Input: a JSON list of steps in funnel order, or {"steps": [...]}. Each step is
{"step": "<name>", "count": <people>}; "name" and "users" are accepted too.
An optional "stage" (landing, cta, form, verify) chooses the cause checklist
when the step name does not make the stage clear. Every step must count the
same cohort, so counts never rise from one step to the next.

Reads only the file or stdin you give it. Writes nothing; prints to stdout.
Adapted from alirezarezvani/claude-skills, marketing-skill/signup-flow-cro (MIT).
"""

import argparse
import json
import sys

HIGH_DROP = 0.50    # step drop-off above this is severity "high"
MEDIUM_DROP = 0.25  # step drop-off above this is severity "medium"; below it, no checklist

# Causes to check, keyed by the stage of the step people failed to reach.
# A step with no recognizable stage gets "other" for high drops and MEDIUM_CAUSES for medium ones.
CAUSES = {
    "landing": [
        "Slow load, redirect chains or broken links between the source and the page.",
        "Tracking gaps: confirm both steps count the same people (consent banners, ad blockers).",
        "Low-quality or accidental clicks from the traffic source.",
    ],
    "cta": [
        "Value proposition unclear: run a 5-second test on the page.",
        "Social proof and trust signals missing near the CTA.",
        "CTA not prominent or not benefit-focused ('Start free' rather than 'Submit').",
        "Long page without a repeated or sticky CTA.",
    ],
    "form": [
        "Too many fields: cut to what account creation needs (often email + password, or SSO).",
        "Collect extra information after signup (progressive profiling).",
        "Errors shown only on submit: add inline validation.",
        "Multi-step flow without a progress indicator.",
    ],
    "verify": [
        "Verification email lands in spam: check SPF, DKIM and DMARC.",
        "No reminder: send a plain follow-up nudge about 30 minutes after signup.",
        "Offer a magic link or code instead of a link-only email.",
        "Let users reach something useful before verification is required.",
    ],
    "other": [
        "Watch session recordings of this step.",
        "Run a one-question exit survey at this step.",
        "Check for UI bugs and broken flows on mobile.",
    ],
}
MEDIUM_CAUSES = [
    "Review the copy and UX at this step.",
    "Test the step on real mobile devices.",
    "Explain why each piece of information is requested.",
]

STAGE_KEYWORDS = (
    ("verify", ("verif", "confirm", "activat")),
    ("form", ("form", "fill", "submit", "detail", "info", "enter", "register", "account created")),
    ("cta", ("cta", "click", "sign up", "signup", "start", "button")),
    ("landing", ("land", "visit", "page", "home", "view")),
)


def guess_stage(name):
    n = name.lower()
    for stage, keys in STAGE_KEYWORDS:
        if any(k in n for k in keys):
            return stage
    return "other"


def load_steps(data):
    """Normalize the input into [{"step", "count", "stage"}] and validate it."""
    if isinstance(data, dict):
        data = data.get("steps")
    if not isinstance(data, list) or len(data) < 2:
        raise ValueError("input must be a list of at least 2 steps (or {\"steps\": [...]})")
    steps = []
    for i, raw in enumerate(data, 1):
        if not isinstance(raw, dict):
            raise ValueError(f"step {i} is not an object")
        name = raw.get("step", raw.get("name"))
        count = raw.get("count", raw.get("users"))
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"step {i} needs a \"step\" (or \"name\") string")
        if isinstance(count, bool) or not isinstance(count, (int, float)) or count < 0:
            raise ValueError(f"step {i} ('{name}') needs a non-negative \"count\" (or \"users\")")
        stage = raw.get("stage") or guess_stage(name)
        if stage not in CAUSES:
            raise ValueError(f"step {i} ('{name}') has unknown stage '{stage}'; "
                             f"use one of: {', '.join(sorted(CAUSES))}")
        steps.append({"step": name.strip(), "count": int(count), "stage": stage})
    if steps[0]["count"] <= 0:
        raise ValueError("the first step must have a count above 0")
    for prev, cur in zip(steps, steps[1:]):
        if cur["count"] > prev["count"]:
            raise ValueError(f"'{cur['step']}' ({cur['count']}) is higher than '{prev['step']}' "
                             f"({prev['count']}): list steps in funnel order and count one cohort")
    return steps


def analyze(steps):
    top = steps[0]["count"]
    rows = []
    for i, s in enumerate(steps):
        if i == 0:
            rows.append({"step": s["step"], "stage": s["stage"], "count": s["count"],
                         "step_conversion_pct": 100.0, "step_drop_pct": 0.0, "lost": 0,
                         "cumulative_conversion_pct": 100.0, "severity": "entry",
                         "causes_to_check": []})
            continue
        prev = steps[i - 1]["count"]
        conv = s["count"] / prev if prev else 0.0
        drop = 1 - conv
        if drop > HIGH_DROP:
            severity, causes = "high", CAUSES[s["stage"]]
        elif drop > MEDIUM_DROP:
            severity = "medium"
            causes = CAUSES[s["stage"]] if s["stage"] != "other" else MEDIUM_CAUSES
        else:
            severity, causes = "ok", []
        rows.append({"step": s["step"], "stage": s["stage"], "count": s["count"],
                     "step_conversion_pct": round(conv * 100, 1),
                     "step_drop_pct": round(drop * 100, 1),
                     "lost": prev - s["count"],
                     "cumulative_conversion_pct": round(s["count"] / top * 100, 2),
                     "severity": severity,
                     "causes_to_check": causes})

    later = rows[1:]
    worst_rate = max(later, key=lambda r: (r["step_drop_pct"], r["lost"]))
    worst_loss = max(later, key=lambda r: (r["lost"], r["step_drop_pct"]))
    any_loss = worst_loss["lost"] > 0
    return {
        "summary": {
            "steps": len(rows),
            "top_count": top,
            "bottom_count": rows[-1]["count"],
            "overall_conversion_pct": rows[-1]["cumulative_conversion_pct"],
            "highest_drop_rate_step": worst_rate["step"] if any_loss else None,
            "highest_drop_rate_pct": worst_rate["step_drop_pct"],
            "most_people_lost_step": worst_loss["step"] if any_loss else None,
            "most_people_lost": worst_loss["lost"],
        },
        "steps": rows,
        "thresholds": {"high_drop_pct": HIGH_DROP * 100, "medium_drop_pct": MEDIUM_DROP * 100},
    }


def print_report(result):
    s = result["summary"]
    print()
    print("SIGNUP FUNNEL DROP-OFF")
    print("=" * 78)
    print(f"  Entered first step : {s['top_count']:,}")
    print(f"  Reached last step  : {s['bottom_count']:,}  ({s['overall_conversion_pct']}% overall)")
    if s["highest_drop_rate_step"] is None:
        print("  No people lost between steps.")
    else:
        print(f"  Highest drop rate  : {s['highest_drop_rate_step']}  ({s['highest_drop_rate_pct']}% of the step before)")
        print(f"  Most people lost   : {s['most_people_lost_step']}  ({s['most_people_lost']:,} people)")
    print()
    print(f"  {'Step':<28} {'Count':>9} {'Step conv':>10} {'Step drop':>10} {'Lost':>9} {'Cumulative':>11}")
    print("  " + "-" * 81)
    for r in result["steps"]:
        print(f"  {r['step'][:28]:<28} {r['count']:>9,} {r['step_conversion_pct']:>9.1f}% "
              f"{r['step_drop_pct']:>9.1f}% {r['lost']:>9,} {r['cumulative_conversion_pct']:>10.2f}%")
    flagged = [r for r in result["steps"] if r["causes_to_check"]]
    if flagged:
        print()
        print("  Causes to check (drop into the step, so look at what people saw just before it):")
        for r in flagged:
            print(f"\n  [{r['step']}]  {r['step_drop_pct']}% drop ({r['severity']}), stage: {r['stage']}")
            for c in r["causes_to_check"]:
                print(f"    - {c}")
    print()


DEMO_STEPS = [
    {"step": "Landing page visit", "count": 12000},
    {"step": "Clicked sign up CTA", "count": 4560},
    {"step": "Submitted signup form", "count": 2800},
    {"step": "Email verified", "count": 1540},
    {"step": "Completed onboarding", "count": 880},
    {"step": "First core action", "count": 420},
]


def main():
    parser = argparse.ArgumentParser(
        description="Find where a signup funnel loses people (stdlib only).",
        epilog="With neither --steps nor --stdin, runs on a demo funnel.",
    )
    src = parser.add_mutually_exclusive_group()
    src.add_argument("--steps", metavar="FILE", help="JSON file with the funnel steps")
    src.add_argument("--stdin", action="store_true", help="read the steps JSON from stdin")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    args = parser.parse_args()

    try:
        if args.stdin:
            data = json.load(sys.stdin)
        elif args.steps:
            with open(args.steps, encoding="utf-8") as fh:
                data = json.load(fh)
        else:
            if not args.json:
                print("Demo mode: sample SaaS signup funnel.")
            data = DEMO_STEPS
        result = analyze(load_steps(data))
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        parser.error(str(exc))

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
