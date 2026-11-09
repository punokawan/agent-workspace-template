#!/usr/bin/env python3
"""Launch readiness scorer: weighted checklist score by category, blockers and a launch decision.

Adapted from alirezarezvani/claude-skills (MIT), marketing-skill/launch-strategy/scripts/launch_readiness_scorer.py.
The default checklist follows this skill: the SLC readiness gate, ORB channel coverage, launch assets and
the operational checks (including references/site-launch-qa.md).
Stdlib only. Reads a JSON file (or stdin with "-") and prints a report to stdout. No network, no file writes.

Usage:
  launch_readiness_scorer.py --export-template > checklist.json   blank checklist to fill in
  launch_readiness_scorer.py --checklist checklist.json            score it
  launch_readiness_scorer.py --sample                              score a built-in example

Checklist JSON: {"<category>": [{"item": "...", "status": "done|partial|not_started", "weight": 1-3}, ...]}
Weight 3 marks a must-have: a weight-3 item that is not started is a blocker.
"""

import argparse
import copy
import json
import sys

TEMPLATE = {
    "product": [
        {"item": "Does one clearly defined thing (Simple)", "weight": 3},
        {"item": "Target users would choose it, not just endure it (Lovable)", "weight": 3},
        {"item": "The one thing is a whole experience with no glaring stubs (Complete)", "weight": 3},
        {"item": "Core user journey tested end to end with real users", "weight": 3},
        {"item": "Known critical bugs fixed", "weight": 3},
        {"item": "Onboarding flow and empty states ready", "weight": 2},
        {"item": "Pricing and plans final and live (if charging)", "weight": 2},
        {"item": "Support briefed with FAQ, known issues and escalation path", "weight": 2},
        {"item": "Getting-started docs published", "weight": 1},
        {"item": "Feedback channel in place", "weight": 1},
    ],
    "channels": [
        {"item": "Owned: email list or waitlist ready for the announcement", "weight": 3},
        {"item": "Owned: blog post or announcement page drafted", "weight": 2},
        {"item": "Owned: in-app announcement for existing users", "weight": 2},
        {"item": "Rented: one or two platforms chosen, posts scheduled", "weight": 2},
        {"item": "Borrowed: partners, newsletters, podcasts or creators confirmed", "weight": 2},
        {"item": "Launch platform or directory listing prepared (if using)", "weight": 1},
        {"item": "Team available to engage and respond on launch day", "weight": 2},
        {"item": "30-day post-launch plan: onboarding emails, roundup, comparison pages", "weight": 2},
    ],
    "assets": [
        {"item": "Landing page with a clear value proposition", "weight": 3},
        {"item": "Launch emails written and scheduled", "weight": 3},
        {"item": "Screenshots, demo video or GIFs", "weight": 2},
        {"item": "Social copy and visuals ready", "weight": 2},
        {"item": "Press or media kit (if pitching)", "weight": 1},
        {"item": "Positioning or comparison page updated", "weight": 1},
    ],
    "operations": [
        {"item": "Analytics and conversion events firing", "weight": 3},
        {"item": "Site QA done for a new site, redesign or migration", "weight": 2},
        {"item": "Monitoring and error alerts active", "weight": 2},
        {"item": "Rollback known and rehearsed once", "weight": 2},
        {"item": "Capacity checked for the expected launch-day peak", "weight": 1},
    ],
}

SAMPLE_STATUS = {
    "product": ["done", "done", "partial", "done", "partial", "done", "done", "not_started", "partial", "done"],
    "channels": ["done", "partial", "not_started", "partial", "not_started", "not_started", "done", "partial"],
    "assets": ["done", "partial", "done", "partial", "not_started", "not_started"],
    "operations": ["done", "partial", "done", "not_started", "partial"],
}

STATUS_VALUE = {"done": 1.0, "partial": 0.5, "not_started": 0.0}


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    sys.exit(2)


def blank_template():
    checklist = copy.deepcopy(TEMPLATE)
    for items in checklist.values():
        for item in items:
            item["status"] = "not_started"
    return checklist


def sample_checklist():
    checklist = copy.deepcopy(TEMPLATE)
    for category, items in checklist.items():
        for item, status in zip(items, SAMPLE_STATUS[category]):
            item["status"] = status
    return checklist


def load_checklist(path):
    try:
        if path == "-":
            return json.load(sys.stdin)
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot read checklist: {exc}")


def label(score):
    if score >= 90:
        return "excellent"
    if score >= 75:
        return "good"
    if score >= 60:
        return "fair"
    if score >= 40:
        return "poor"
    return "critical"


def score(checklist, gate_categories, gate_min):
    if not isinstance(checklist, dict) or not checklist:
        fail("checklist must be a JSON object of categories")
    warnings, categories, blockers = [], {}, []
    for category, items in checklist.items():
        if not isinstance(items, list) or not items:
            fail(f"category '{category}' must be a non-empty list of items")
        earned = total = 0.0
        rows = []
        for entry in items:
            if not isinstance(entry, dict) or "item" not in entry:
                fail(f"every entry in '{category}' needs an 'item' field")
            status = str(entry.get("status", "not_started")).strip().lower()
            if status not in STATUS_VALUE:
                warnings.append(f"{category}: unknown status '{status}' for '{entry['item']}', counted as not_started")
                status = "not_started"
            weight = entry.get("weight", 1)
            if not isinstance(weight, (int, float)) or weight <= 0:
                fail(f"weight for '{entry['item']}' must be a positive number")
            earned += STATUS_VALUE[status] * weight
            total += weight
            rows.append({"item": entry["item"], "status": status, "weight": weight})
            if status == "not_started" and weight >= 3:
                blockers.append(f"{category}: {entry['item']}")
        value = round(earned / total * 100)
        categories[category] = {"score": value, "label": label(value), "items": rows}

    overall = round(sum(c["score"] for c in categories.values()) / len(categories))
    gate_failures = [f"{name} ({categories[name]['score']})" for name in gate_categories
                     if name in categories and categories[name]["score"] < gate_min]
    missing_gates = [name for name in gate_categories if name not in categories]
    if missing_gates:
        warnings.append(f"gate categories not in checklist: {', '.join(missing_gates)}")

    if blockers:
        decision = f"NOT READY: resolve {len(blockers)} blocker(s) or move the date"
    elif gate_failures:
        decision = f"SLIP THE DATE: {', '.join(gate_failures)} below {gate_min}"
    elif overall >= 80:
        decision = "READY: launch as planned"
    elif overall >= 60:
        decision = "CONDITIONAL: launch is defensible; finish the partial items"
    elif overall >= 40:
        decision = "CAUTION: consider a soft launch or waitlist"
    else:
        decision = "NOT READY: major preparation needed"

    # Blockers first, then by weight (heaviest first), not-started before partial, weakest category first.
    pending = []
    for name, data in categories.items():
        for row in data["items"]:
            if row["status"] == "done" or (row["status"] == "not_started" and row["weight"] >= 3):
                continue
            tag = "START   " if row["status"] == "not_started" else "FINISH  "
            pending.append((-row["weight"], row["status"] != "not_started", data["score"],
                            f"{tag} {name}: {row['item']}"))
    actions = [f"BLOCKER  {b}" for b in blockers] + [entry[3] for entry in sorted(pending)]

    return {
        "overall": {"score": overall, "label": label(overall), "decision": decision},
        "blockers": blockers,
        "gate": {"categories": gate_categories, "minimum": gate_min, "failures": gate_failures},
        "categories": categories,
        "actions": actions[:15],
        "warnings": warnings,
    }


def print_report(result, sample):
    line = "=" * 66
    print(line)
    print("LAUNCH READINESS" + ("  (SAMPLE DATA)" if sample else ""))
    print(line)
    for warning in result["warnings"]:
        print(f"WARNING: {warning}")
    overall = result["overall"]
    print(f"\nOverall score: {overall['score']}/100 ({overall['label']})")
    print(f"Decision:      {overall['decision']}")
    print(f"\n  {'Category':<14} {'Score':>6}  Status mix (done/partial/not started)")
    for name, data in result["categories"].items():
        counts = [sum(1 for r in data["items"] if r["status"] == s) for s in ("done", "partial", "not_started")]
        print(f"  {name:<14} {data['score']:>5}   {counts[0]}/{counts[1]}/{counts[2]}  ({data['label']})")
    gate = result["gate"]
    print(f"\nGate: {', '.join(gate['categories'])} must score {gate['minimum']} or more"
          + (f"; failing: {', '.join(gate['failures'])}" if gate["failures"] else "; passing"))
    if result["actions"]:
        print("\nNext actions")
        for number, action in enumerate(result["actions"], 1):
            print(f"  {number:>2}. {action}")
    print("\nScore when planning starts and again one week before launch day.")
    print(line)


def main():
    parser = argparse.ArgumentParser(
        description="Score launch readiness from a weighted checklist and return a launch decision.",
        epilog="Checklist format is documented at the top of this file.",
    )
    parser.add_argument("--checklist", help="checklist JSON file, or - to read stdin")
    parser.add_argument("--sample", action="store_true", help="score a built-in example checklist")
    parser.add_argument("--export-template", action="store_true",
                        help="print a blank checklist (all items not_started) to stdout and exit")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    parser.add_argument("--gate-categories", default="channels,assets",
                        help="comma-separated categories that must pass the gate (default: channels,assets)")
    parser.add_argument("--gate-min", type=int, default=60, help="minimum score for gate categories (default: 60)")
    args = parser.parse_args()

    if args.export_template:
        print(json.dumps(blank_template(), indent=2))
        return
    if args.sample:
        checklist = sample_checklist()
    elif args.checklist:
        checklist = load_checklist(args.checklist)
    else:
        parser.print_help()
        sys.exit(1)
    gates = [name.strip() for name in args.gate_categories.split(",") if name.strip()]
    result = score(checklist, gates, args.gate_min)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result, args.sample)


if __name__ == "__main__":
    main()
