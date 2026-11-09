#!/usr/bin/env python3
"""
social_calendar_generator.py: build a social content calendar with a
balanced pillar distribution.

Pillars are spread across post dates with a weighted round-robin, so each
pillar's share of posts tracks its weight. Deterministic: the same config
gives the same calendar.

Usage:
    python3 social_calendar_generator.py                          # demo config
    python3 social_calendar_generator.py --config config.json
    python3 social_calendar_generator.py --config config.json --json
    python3 social_calendar_generator.py --config config.json --markdown
    python3 social_calendar_generator.py --start 2026-04-06 --weeks 4

config.json:
    {
      "pillars": [
        {"name": "Educational", "description": "Tips, tutorials", "weight": 3,
         "formats": ["Carousel", "How-to thread", "Quick tip"]},
        {"name": "Community", "description": "Polls, shoutouts", "weight": 1}
      ],
      "platforms": [
        {"name": "LinkedIn", "posts_per_week": 3, "best_days": ["Monday", "Tuesday", "Wednesday"]},
        {"name": "X", "posts_per_week": 10, "best_days": ["Monday", "Tuesday", "Wednesday",
         "Thursday", "Friday"], "slots_per_day": 2}
      ],
      "start_date": "2026-04-06",
      "weeks": 4
    }
    weight         share of posts for the pillar (default 1)
    formats        optional formats to rotate for the pillar
    slots_per_day  optional posts per day on one platform (default 1)

Stdlib only. Reads the config file; prints to stdout; writes nothing.
"""

import argparse
import json
import sys
from collections import defaultdict
from datetime import date, timedelta


DEMO_CONFIG = {
    "pillars": [
        {"name": "Educational", "description": "Tips, tutorials, how-tos", "weight": 3},
        {"name": "Inspirational", "description": "Success stories and lessons", "weight": 2},
        {"name": "Product", "description": "Feature demos and updates", "weight": 2},
        {"name": "Community", "description": "Polls, questions, shoutouts", "weight": 1},
    ],
    "platforms": [
        {"name": "LinkedIn", "posts_per_week": 3,
         "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday"],
         "content_type_hint": "Long-form insights, carousels, thought leadership"},
        {"name": "X", "posts_per_week": 5,
         "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
         "content_type_hint": "Threads, quick tips, takes, polls"},
    ],
    "start_date": None,  # defaults to next Monday
    "weeks": 4,
}

# Used when a pillar has no "formats" list.
CONTENT_TYPE_HINTS = {
    "Educational": ["How-to thread", "Quick tip", "Carousel: 5 steps", "Tutorial link"],
    "Inspirational": ["Success story", "Before/after", "Lesson learned", "Quote card"],
    "Product": ["Feature demo clip", "Changelog post", "Use-case spotlight", "Behind the scenes"],
    "Community": ["Poll", "User shoutout", "Question post", "Community highlight"],
}

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def build_pillar_sequence(pillars: list, length: int) -> list:
    """Deterministic weighted round-robin: pick the pillar furthest behind its target share."""
    names = [p["name"] for p in pillars]
    weights = [max(0.0, float(p.get("weight", 1))) for p in pillars]
    total_w = sum(weights) or 1.0
    targets = [w / total_w for w in weights]
    sequence, counts = [], [0] * len(pillars)
    for _ in range(length):
        placed = len(sequence)
        scores = [targets[i] - (counts[i] / (placed + 1) if placed else 0) for i in range(len(names))]
        best = scores.index(max(scores))
        sequence.append(names[best])
        counts[best] += 1
    return sequence


def next_monday(from_date: date = None) -> date:
    d = from_date or date.today()
    days_ahead = (0 - d.weekday()) % 7 or 7
    return d + timedelta(days=days_ahead)


def build_calendar(config: dict) -> dict:
    pillars = config.get("pillars") or DEMO_CONFIG["pillars"]
    platforms = config.get("platforms") or DEMO_CONFIG["platforms"]
    weeks = int(config.get("weeks") or 4)
    start = date.fromisoformat(config["start_date"]) if config.get("start_date") else next_monday()
    pillar_map = {p["name"]: p for p in pillars}

    calendar_by_platform = {}
    for platform in platforms:
        pname = platform["name"]
        ppw = int(platform.get("posts_per_week", 3))
        best_days = platform.get("best_days") or WEEKDAY_NAMES[:5]
        slots = max(1, int(platform.get("slots_per_day", 1)))

        post_dates = []
        for week in range(weeks):
            week_start = start + timedelta(weeks=week)
            placed = 0
            for day_offset in range(7):
                d = week_start + timedelta(days=day_offset)
                if WEEKDAY_NAMES[d.weekday()] not in best_days:
                    continue
                for _ in range(slots):
                    if placed >= ppw:
                        break
                    post_dates.append(d)
                    placed += 1
        pillar_seq = build_pillar_sequence(pillars, len(post_dates))

        posts, format_idx = [], defaultdict(int)
        for post_date, pillar_name in zip(post_dates, pillar_seq):
            pillar = pillar_map[pillar_name]
            formats = pillar.get("formats") or CONTENT_TYPE_HINTS.get(pillar_name, ["Post"])
            content_type = formats[format_idx[pillar_name] % len(formats)]
            format_idx[pillar_name] += 1
            posts.append({
                "date": post_date.isoformat(),
                "weekday": WEEKDAY_NAMES[post_date.weekday()],
                "week_number": (post_date - start).days // 7 + 1,
                "platform": pname,
                "pillar": pillar_name,
                "description": pillar.get("description", ""),
                "content_type": content_type,
                "content_type_hint": platform.get("content_type_hint", ""),
            })

        dist = defaultdict(int)
        for p in posts:
            dist[p["pillar"]] += 1
        total = len(posts) or 1
        calendar_by_platform[pname] = {
            "platform": pname,
            "posts_per_week": ppw,
            "slots_per_day": slots,
            "total_weeks": weeks,
            "total_posts": len(posts),
            "best_days": best_days,
            "posts": posts,
            "pillar_distribution": dict(dist),
            "pillar_pct": {k: round(v / total * 100) for k, v in dist.items()},
        }

    timeline = sorted((p for pc in calendar_by_platform.values() for p in pc["posts"]),
                      key=lambda p: (p["date"], p["platform"]))
    return {
        "meta": {
            "start_date": start.isoformat(),
            "end_date": (start + timedelta(weeks=weeks) - timedelta(days=1)).isoformat(),
            "weeks": weeks,
            "platforms": [p["name"] for p in platforms],
            "total_posts": len(timeline),
            "pillars": [p["name"] for p in pillars],
            "pillar_descriptions": {p["name"]: p.get("description", "") for p in pillars},
        },
        "platforms": calendar_by_platform,
        "timeline": timeline,
    }


def _group_week(timeline: list, week_num: int) -> dict:
    """date -> platform -> [posts]"""
    grouped = defaultdict(lambda: defaultdict(list))
    for post in timeline:
        if post["week_number"] == week_num:
            grouped[post["date"]][post["platform"]].append(post)
    return grouped


def build_markdown(result: dict) -> str:
    m = result["meta"]
    lines = ["# Social Media Content Calendar",
             f"**Period:** {m['start_date']} to {m['end_date']} | **{m['weeks']} weeks** | "
             f"**{m['total_posts']} total posts**\n"]

    for pname, pc in result["platforms"].items():
        lines.append(f"## {pname} ({pc['total_posts']} posts)\n")
        lines.append("**Pillar distribution:**")
        for pillar, count in pc["pillar_distribution"].items():
            lines.append(f"- {pillar}: {count} posts ({pc['pillar_pct'][pillar]}%)")
        lines.append("")

    for week_num in range(1, m["weeks"] + 1):
        lines.append(f"## Week {week_num}\n")
        lines.append("| Date | Day | " + " | ".join(m["platforms"]) + " |")
        lines.append("|---|---|" + "|".join(["---"] * len(m["platforms"])) + "|")
        grouped = _group_week(result["timeline"], week_num)
        for day in sorted(grouped):
            by_platform = grouped[day]
            weekday = next(iter(by_platform.values()))[0]["weekday"]
            cells = []
            for pname in m["platforms"]:
                posts = by_platform.get(pname, [])
                cells.append("<br/>".join(f"**{p['pillar']}**: {p['content_type']}" for p in posts) or "-")
            lines.append(f"| {day} | {weekday} | " + " | ".join(cells) + " |")
        lines.append("")

    lines.append("## Content Pillars\n")
    lines.append("| Pillar | Description |")
    lines.append("|---|---|")
    for pillar in m["pillars"]:
        lines.append(f"| {pillar} | {m['pillar_descriptions'].get(pillar, '')} |")
    lines.append("")
    return "\n".join(lines)


def pretty_print(result: dict) -> None:
    m = result["meta"]
    print("\n" + "=" * 70)
    print("  SOCIAL MEDIA CONTENT CALENDAR")
    print("=" * 70)
    print(f"\n  Period     : {m['start_date']} to {m['end_date']}  ({m['weeks']} weeks)")
    print(f"  Platforms  : {', '.join(m['platforms'])}")
    print(f"  Total posts: {m['total_posts']}")
    print(f"  Pillars    : {', '.join(m['pillars'])}")

    for pname, pc in result["platforms"].items():
        print(f"\n  {'-' * 60}")
        print(f"  {pname.upper()}: {pc['total_posts']} posts ({pc['posts_per_week']}/week, "
              f"up to {pc['slots_per_day']}/day)")
        print(f"  Best days: {', '.join(pc['best_days'])}")
        print("  Pillar distribution:")
        for pillar, count in pc["pillar_distribution"].items():
            share = pc["pillar_pct"][pillar]
            bar = "#" * (share // 5) + "." * (20 - share // 5)
            print(f"    {pillar:<18} {count:>3} posts  {share:>3}%  {bar}")

    print(f"\n  {'-' * 70}")
    print("  WEEKLY SCHEDULE\n")
    for week_num in range(1, m["weeks"] + 1):
        grouped = _group_week(result["timeline"], week_num)
        if not grouped:
            continue
        print(f"  WEEK {week_num}")
        print(f"  {'Date':<12} {'Day':<11}" + "".join(f" {p:<26}" for p in m["platforms"]))
        print("  " + "-" * (12 + 11 + 27 * len(m["platforms"])))
        for day in sorted(grouped):
            by_platform = grouped[day]
            weekday = next(iter(by_platform.values()))[0]["weekday"]
            row = f"  {day:<12} {weekday:<11}"
            for pname in m["platforms"]:
                posts = by_platform.get(pname, [])
                if posts:
                    cell = f"{posts[0]['pillar'][:12]}/{posts[0]['content_type'][:10]}"
                    if len(posts) > 1:
                        cell += f" (+{len(posts) - 1})"
                else:
                    cell = "-"
                row += f" {cell:<26}"
            print(row)
        print()
    print("  Use --markdown for a copyable table, or --json for every slot.\n")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate a social media content calendar with balanced pillar distribution.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--config", help="Path to JSON config file")
    parser.add_argument("--start", help="Start date YYYY-MM-DD (overrides config)")
    parser.add_argument("--weeks", type=int, help="Number of weeks (overrides config)")
    parser.add_argument("--json", action="store_true", help="Output the calendar as JSON")
    parser.add_argument("--markdown", action="store_true", help="Output the calendar as Markdown")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.config:
        try:
            with open(args.config, encoding="utf-8") as f:
                config = json.load(f)
        except OSError as exc:
            sys.exit(f"Error: cannot read {args.config}: {exc}")
        except json.JSONDecodeError as exc:
            sys.exit(f"Error: invalid JSON in {args.config}: {exc}")
    else:
        print("Demo mode: sample config (4 pillars, 2 platforms)\n", file=sys.stderr)
        config = dict(DEMO_CONFIG)

    if args.start:
        config["start_date"] = args.start
    if args.weeks:
        config["weeks"] = args.weeks
    if int(config.get("weeks") or 4) < 1:
        sys.exit("Error: weeks must be 1 or more")

    try:
        result = build_calendar(config)
    except ValueError as exc:
        sys.exit(f"Error: {exc} (dates use YYYY-MM-DD)")
    except KeyError as exc:
        sys.exit(f"Error: missing field {exc} in a pillar or platform")

    if args.json:
        print(json.dumps(result, indent=2, default=str))
    elif args.markdown:
        print(build_markdown(result))
    else:
        pretty_print(result)


if __name__ == "__main__":
    main()
