#!/usr/bin/env python3
"""
attribution_analyzer.py: score your own journey data under six rule-based models
and compare them side by side.

Models (see references/attribution-models.md):
  first-touch      100% to the first touch
  last-touch       100% to the last touch
  last-non-direct  100% to the last touch that is not direct (direct only if nothing else)
  linear           equal credit to every touch
  time-decay       weight 0.5 ** (days before conversion / half-life), normalised
  position-based   40% first, 40% last, 20% split across the middle
                   (one touch: 100%; two touches: 50/50)

Only converted journeys earn credit. The output is a model of credit, not causality:
read it next to self-reported data and incrementality tests before moving budget.

Usage:
  python3 attribution_analyzer.py --file journeys.json [--model time-decay]
      [--half-life 14] [--credit conversions] [--direct-label direct] [--json]
  python3 attribution_analyzer.py            # demo journeys

Input:
  {"journeys": [
     {"journey_id": "j1", "converted": true, "revenue": 500,
      "conversion_timestamp": "2026-10-09T12:00:00",          optional
      "touchpoints": [
        {"channel": "organic_search", "timestamp": "2026-10-01T10:00:00"},
        {"channel": "paid_search", "timestamp": "2026-10-08T09:15:00Z"}]}]}
  Timestamps are ISO 8601 (date, date-time, optional Z or offset). Time-decay counts
  days back from conversion_timestamp, or from the last touch when it is absent.
  --credit revenue (default) needs revenue on every converted journey;
  --credit conversions gives each converted journey 1.

Stdlib only. Reads the input file you pass; writes nothing.
"""

import argparse
import json
import sys
from datetime import datetime, timezone

MODELS = ["first-touch", "last-touch", "last-non-direct", "linear", "time-decay", "position-based"]
SMALL_SAMPLE = 100

DEMO = {"journeys": [
    {"journey_id": "j1", "converted": True, "revenue": 12000, "touchpoints": [
        {"channel": "paid_social", "timestamp": "2026-09-01"},
        {"channel": "organic_search", "timestamp": "2026-09-06"},
        {"channel": "paid_social", "timestamp": "2026-09-13"},
        {"channel": "paid_search_brand", "timestamp": "2026-10-01"},
        {"channel": "direct", "timestamp": "2026-10-09"}]},
    {"journey_id": "j2", "converted": True, "revenue": 3000, "touchpoints": [
        {"channel": "organic_search", "timestamp": "2026-09-20"},
        {"channel": "email", "timestamp": "2026-09-27"}]},
    {"journey_id": "j3", "converted": False, "touchpoints": [
        {"channel": "paid_social", "timestamp": "2026-09-22"}]},
]}


class InputError(ValueError):
    pass


def parse_timestamp(value, where):
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{where}: timestamp must be an ISO 8601 string")
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        raise InputError(f"{where}: cannot parse timestamp {value!r}")
    if parsed.tzinfo is not None:
        parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed


def prepare(data, credit_mode):
    """Validate input; return (converted journeys with sorted touches, summary)."""
    if not isinstance(data, dict) or not isinstance(data.get("journeys"), list):
        raise InputError("input needs a 'journeys' array")
    journeys = data["journeys"]
    if not journeys:
        raise InputError("'journeys' is empty")
    prepared, channels = [], set()
    converted_total, without_touches, missing_revenue = 0, 0, []
    for i, journey in enumerate(journeys):
        jid = str(journey.get("journey_id", f"journey #{i + 1}")) if isinstance(journey, dict) else str(i + 1)
        if not isinstance(journey, dict):
            raise InputError(f"{jid}: each journey must be an object")
        touches = []
        for t in journey.get("touchpoints") or []:
            if not isinstance(t, dict) or not t.get("channel"):
                raise InputError(f"{jid}: every touchpoint needs a channel")
            channel = str(t["channel"])
            channels.add(channel)
            touches.append((parse_timestamp(t.get("timestamp"), jid), channel))
        if not journey.get("converted", False):
            continue
        converted_total += 1
        if not touches:
            without_touches += 1
            continue
        touches.sort(key=lambda x: x[0])
        if credit_mode == "revenue":
            revenue = journey.get("revenue")
            if isinstance(revenue, bool) or not isinstance(revenue, (int, float)) or revenue < 0:
                missing_revenue.append(jid)
                continue
            value = float(revenue)
        else:
            value = 1.0
        end = journey.get("conversion_timestamp")
        end = parse_timestamp(end, jid) if end else touches[-1][0]
        if end < touches[-1][0]:
            raise InputError(f"{jid}: conversion_timestamp is before the last touch")
        prepared.append({"id": jid, "value": value, "touches": touches, "end": end})
    if missing_revenue:
        shown = ", ".join(missing_revenue[:10]) + (" ..." if len(missing_revenue) > 10 else "")
        raise InputError(f"{len(missing_revenue)} converted journeys have no valid revenue ({shown}); "
                         "add revenue or run with --credit conversions")
    summary = {"journeys": len(journeys), "converted": converted_total,
               "converted_without_touchpoints": without_touches,
               "scored": len(prepared),
               "conversion_rate_pct": round(100.0 * converted_total / len(journeys), 2),
               "credit_unit": credit_mode,
               "total_credit": sum(j["value"] for j in prepared),
               "channels_observed": sorted(channels)}
    return prepared, summary


def add(credits, channel, amount):
    credits[channel] = credits.get(channel, 0.0) + amount


def run_model(model, journeys, half_life, direct_labels):
    credits = {}
    for j in journeys:
        touches, value = j["touches"], j["value"]
        channels = [c for _, c in touches]
        if model == "first-touch":
            add(credits, channels[0], value)
        elif model == "last-touch":
            add(credits, channels[-1], value)
        elif model == "last-non-direct":
            chosen = next((c for c in reversed(channels) if c.lower() not in direct_labels),
                          channels[-1])
            add(credits, chosen, value)
        elif model == "linear":
            for c in channels:
                add(credits, c, value / len(channels))
        elif model == "time-decay":
            weights = [0.5 ** (((j["end"] - ts).total_seconds() / 86400.0) / half_life)
                       for ts, _ in touches]
            total = sum(weights)
            for w, c in zip(weights, channels):
                add(credits, c, value * w / total)
        elif model == "position-based":
            if len(channels) == 1:
                add(credits, channels[0], value)
            elif len(channels) == 2:
                add(credits, channels[0], value * 0.5)
                add(credits, channels[1], value * 0.5)
            else:
                add(credits, channels[0], value * 0.4)
                add(credits, channels[-1], value * 0.4)
                for c in channels[1:-1]:
                    add(credits, c, value * 0.2 / (len(channels) - 2))
    return credits


def analyse(data, models, half_life, credit_mode, direct_labels):
    journeys, summary = prepare(data, credit_mode)
    results = {m: run_model(m, journeys, half_life, direct_labels) for m in models}
    notes = []
    if summary["scored"] < SMALL_SAMPLE:
        noun = "journey" if summary["scored"] == 1 else "journeys"
        notes.append(f"{summary['scored']} converted {noun} scored: below {SMALL_SAMPLE}, "
                     "read shares as directional, not as allocation rules")
    if summary["converted_without_touchpoints"]:
        notes.append(f"{summary['converted_without_touchpoints']} converted journeys have no "
                     "touchpoints and earn no credit (an untracked share, often direct or dark social)")
    return {"summary": summary, "half_life_days": half_life, "models": results, "notes": notes}


def print_text(report):
    s = report["summary"]
    unit = "revenue" if s["credit_unit"] == "revenue" else "conversions"
    print("ATTRIBUTION BY MODEL (credit, not causality)")
    print(f"Journeys {s['journeys']} | converted {s['converted']} ({s['conversion_rate_pct']}%) | "
          f"scored {s['scored']} | total credit {s['total_credit']:,.2f} {unit}")
    for note in report["notes"]:
        print(f"NOTE: {note}")
    models = list(report["models"])
    channels = sorted({c for credits in report["models"].values() for c in credits})
    total = s["total_credit"] or 1.0
    header = f"{'Channel':<22}" + "".join(f"{m:>17}" for m in models)
    print("\nShare of credit")
    print(header)
    for c in channels:
        row = f"{c:<22}"
        for m in models:
            row += f"{100.0 * report['models'][m].get(c, 0.0) / total:>16.1f}%"
        print(row)
    print(f"\nCredit in {unit}")
    print(header)
    for c in channels:
        row = f"{c:<22}"
        for m in models:
            row += f"{report['models'][m].get(c, 0.0):>17,.2f}"
        print(row)
    if "time-decay" in models:
        print(f"\nTime-decay half-life: {report['half_life_days']:g} days.")
    if "first-touch" in models and "last-touch" in models:
        print("Read first-touch and last-touch side by side; the gap between them is the insight.")


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
        description="Score journey data under six rule-based attribution models.",
        epilog="No input runs demo journeys. Reads only --file; writes nothing.")
    parser.add_argument("--file", help="JSON file with a 'journeys' array")
    parser.add_argument("--model", choices=MODELS, help="run one model (default: all six)")
    parser.add_argument("--half-life", type=float, default=7.0,
                        help="time-decay half-life in days (default 7; match it to the sales cycle)")
    parser.add_argument("--credit", choices=["revenue", "conversions"], default="revenue",
                        help="credit revenue (default) or one unit per converted journey")
    parser.add_argument("--direct-label", action="append", default=None,
                        help="channel name treated as direct by last-non-direct (repeatable; "
                             "default: direct)")
    parser.add_argument("--json", action="store_true", help="print JSON only")
    args = parser.parse_args()

    if args.half_life <= 0:
        print("Error: --half-life must be above 0", file=sys.stderr)
        sys.exit(2)
    direct_labels = {d.lower() for d in (args.direct_label or ["direct"])}
    models = [args.model] if args.model else MODELS
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
                print("No input given: running the demo journeys.\n")
        report = analyse(data, models, args.half_life, args.credit, direct_labels)
    except InputError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)

    if args.json:
        print(json.dumps(rounded(report), indent=2))
    else:
        print_text(report)


if __name__ == "__main__":
    main()
