#!/usr/bin/env python3
"""
funnel_analyzer.py: stage-to-stage conversion, drop-off and bottlenecks for a
funnel, optionally compared across segments (channel, device, cohort, campaign).

Per stage: count, conversion from the previous stage, drop-off, cumulative
conversion from the top, and the relative lift in final conversions that one
extra percentage point at that stage would give (100 / stage rate, all other
rates held constant). Names the largest absolute and the largest relative drop.

Feed it counts from one closed observation window. A cohort still inside its
window is pending, not lost: leave it out (see the analytics skill's principles).

Usage:
  python3 funnel_analyzer.py --file funnel.json [--json]
  python3 funnel_analyzer.py                 # demo funnel

Input, one funnel:
  {"funnel": {"stages": ["Visit", "Signup", "Activated", "Paid"],
              "counts": [10000, 820, 410, 96]}}
Input, segments that share the stages:
  {"stages": ["Visit", "Signup", "Activated", "Paid"],
   "segments": {"paid_search": {"counts": [4000, 380, 190, 51]},
                "paid_social": {"counts": [6000, 440, 220, 45]}}}

Stdlib only. Reads the input file you pass; writes nothing.
"""

import argparse
import json
import sys

DEMO = {"stages": ["Visit", "Signup", "Activated", "Paid"],
        "segments": {"paid_search": {"counts": [4000, 380, 190, 51]},
                     "paid_social": {"counts": [6000, 440, 220, 45]}}}


class InputError(ValueError):
    pass


def counts_of(raw, label, n_stages):
    if not isinstance(raw, list) or len(raw) != n_stages:
        raise InputError(f"{label}: needs {n_stages} counts, one per stage")
    out = []
    for c in raw:
        if isinstance(c, bool) or not isinstance(c, (int, float)) or c < 0:
            raise InputError(f"{label}: counts must be non-negative numbers")
        out.append(c)
    return out


def analyze_funnel(stages, counts):
    metrics, warnings = [], []
    worst_abs, worst_rel = None, None
    for i, (stage, count) in enumerate(zip(stages, counts)):
        row = {"stage": stage, "count": count,
               "cumulative_pct": 100.0 * count / counts[0] if counts[0] else None}
        if i == 0:
            row.update({"conversion_pct": None, "dropoff": None, "dropoff_pct": None,
                        "lift_per_point_pct": None})
        else:
            prev = counts[i - 1]
            rate = 100.0 * count / prev if prev else None
            row["conversion_pct"] = rate
            row["dropoff"] = prev - count
            row["dropoff_pct"] = 100.0 - rate if rate is not None else None
            row["lift_per_point_pct"] = 100.0 / rate if rate else None
            transition = f"{stages[i - 1]} -> {stage}"
            if count > prev:
                warnings.append(f"{transition}: count rises ({prev:g} -> {count:g}); stages may "
                                "not be nested or may come from different windows")
            if worst_abs is None or row["dropoff"] > worst_abs[1]:
                worst_abs = (transition, row["dropoff"])
            if rate is not None and (worst_rel is None or row["dropoff_pct"] > worst_rel[1]):
                worst_rel = (transition, row["dropoff_pct"])
        metrics.append(row)
    return {
        "stages": metrics,
        "entries": counts[0], "completions": counts[-1],
        "overall_conversion_pct": 100.0 * counts[-1] / counts[0] if counts[0] else None,
        "bottleneck_absolute": {"transition": worst_abs[0], "lost": worst_abs[1]} if worst_abs else None,
        "bottleneck_relative": {"transition": worst_rel[0], "dropoff_pct": worst_rel[1]} if worst_rel else None,
        "warnings": warnings,
    }


def analyse(data):
    if not isinstance(data, dict):
        raise InputError("input must be a JSON object")
    if "segments" in data:
        stages = data.get("stages") or (data.get("funnel") or {}).get("stages")
        if not isinstance(stages, list) or len(stages) < 2:
            raise InputError("'stages' needs at least two stage names")
        segments = data["segments"]
        if not isinstance(segments, dict) or not segments:
            raise InputError("'segments' must be a non-empty object")
        results = {}
        for name, seg in segments.items():
            if not isinstance(seg, dict):
                raise InputError(f"segment '{name}' must be an object with 'counts'")
            results[name] = analyze_funnel(stages, counts_of(seg.get("counts"), f"segment '{name}'",
                                                              len(stages)))
        ranking = sorted(results, key=lambda n: results[n]["overall_conversion_pct"] or 0.0,
                         reverse=True)
        return {"mode": "segments", "stage_names": stages, "segments": results, "ranking": ranking}
    funnel = data.get("funnel")
    if not isinstance(funnel, dict):
        raise InputError("input needs 'funnel' (stages + counts) or 'segments'")
    stages = funnel.get("stages")
    if not isinstance(stages, list) or len(stages) < 2:
        raise InputError("'funnel.stages' needs at least two stage names")
    return {"mode": "single", "funnel": analyze_funnel(stages, counts_of(funnel.get("counts"),
                                                                         "funnel", len(stages)))}


def p(value, digits=1):
    return "-" if value is None else f"{value:.{digits}f}%"


def print_funnel(result, title):
    print(title)
    print(f"  Entries {result['entries']:,g} | completions {result['completions']:,g} | "
          f"overall {p(result['overall_conversion_pct'], 2)}")
    print(f"  {'Stage':<18} {'Count':>10} {'Conv':>8} {'Drop-off':>18} {'Cumul':>8} {'+1pt lift':>10}")
    for r in result["stages"]:
        if r["dropoff"] is None:
            drop = "-"
        elif r["dropoff"] < 0:
            drop = f"+{-r['dropoff']:,g} (rise)"
        else:
            drop = f"-{r['dropoff']:,g} ({p(r['dropoff_pct'])})"
        print(f"  {r['stage']:<18} {r['count']:>10,g} {p(r['conversion_pct']):>8} {drop:>18} "
              f"{p(r['cumulative_pct']):>8} {p(r['lift_per_point_pct']):>10}")
    if result["bottleneck_absolute"]:
        b = result["bottleneck_absolute"]
        print(f"  Largest absolute drop: {b['transition']} (lost {b['lost']:,g})")
    if result["bottleneck_relative"]:
        b = result["bottleneck_relative"]
        print(f"  Largest relative drop: {b['transition']} ({p(b['dropoff_pct'])} drop-off)")
    for w in result["warnings"]:
        print(f"  WARNING: {w}")


def print_text(report):
    print("FUNNEL ANALYSIS")
    print("+1pt lift: relative gain in final conversions from one more point at that stage.\n")
    if report["mode"] == "single":
        print_funnel(report["funnel"], "FUNNEL")
        return
    print("SEGMENTS BY OVERALL CONVERSION")
    for rank, name in enumerate(report["ranking"], 1):
        seg = report["segments"][name]
        print(f"  {rank}. {name}: {p(seg['overall_conversion_pct'], 2)} "
              f"({seg['completions']:,g} of {seg['entries']:,g})")
    print()
    for name in report["ranking"]:
        print_funnel(report["segments"][name], f"SEGMENT: {name}")
        print()
    names = report["ranking"]
    print("STAGE CONVERSION BY SEGMENT")
    print(f"  {'Stage':<18}" + "".join(f"{n[:16]:>18}" for n in names))
    for i, stage in enumerate(report["stage_names"]):
        row = f"  {stage:<18}"
        for n in names:
            row += f"{p(report['segments'][n]['stages'][i]['conversion_pct']):>18}"
        print(row)


def rounded(value):
    if isinstance(value, float):
        return round(value, 4)
    if isinstance(value, dict):
        return {k: rounded(v) for k, v in value.items()}
    if isinstance(value, list):
        return [rounded(v) for v in value]
    return value


def main():
    parser = argparse.ArgumentParser(
        description="Funnel conversion, drop-off and bottlenecks, with segment comparison.",
        epilog="No input runs a demo funnel. Reads only --file; writes nothing.")
    parser.add_argument("--file", help="JSON file with 'funnel' or 'stages' + 'segments'")
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
        else:
            data = DEMO
            if not args.json:
                print("No input given: running the demo funnel.\n")
        report = analyse(data)
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(rounded(report), indent=2))
    else:
        print_text(report)


if __name__ == "__main__":
    main()
