#!/usr/bin/env python3
"""
social_metrics.py: compute social post metrics from exported numbers.

Per post: engagement rate (by reach, and by followers when given), CTR,
share rate, save rate, reach rate. Overall: totals and the same rates, the
median engagement rate, top and bottom posts, averages by content type,
follower growth, cost metrics (CPE, CPC, CPM, CPA) when spend is given,
ROAS and ROI only from real revenue, a benchmark comparison, and flags.

Usage:
  python3 social_metrics.py posts.json
  python3 social_metrics.py posts.json --json
  python3 social_metrics.py                      # demo data

Input JSON:
  {
    "platform": "instagram",
    "followers": 12000, "followers_start": 11400,              # optional
    "total_spend": 500, "revenue": 1800, "conversions": 12,     # optional
    "benchmarks": {"engagement_rate": 2.5, "ctr": 0.8},         # optional, in percent
    "posts": [
      {"post_id": "p1", "content_type": "carousel", "likes": 342, "comments": 28,
       "shares": 15, "saves": 45, "reach": 5200, "impressions": 8500, "clicks": 120}
    ]
  }
Required per post: likes, comments, reach. Everything else is optional.

The default benchmarks are rough industry figures without a stated basis;
the account's own median is the better baseline.
Stdlib only. Reads the input file; writes nothing.
"""

import argparse
import json
import statistics
import sys

# Average engagement rate and organic CTR by platform, in percent.
DEFAULT_BENCHMARKS = {
    "instagram": {"engagement_rate": 1.22, "ctr": 0.22},
    "facebook": {"engagement_rate": 0.07, "ctr": 0.90},
    "x": {"engagement_rate": 0.05, "ctr": 0.86},
    "twitter": {"engagement_rate": 0.05, "ctr": 0.86},
    "linkedin": {"engagement_rate": 2.0, "ctr": 0.44},
    "tiktok": {"engagement_rate": 5.96, "ctr": 0.30},
}

DEMO = {
    "platform": "instagram",
    "followers": 12000,
    "followers_start": 11400,
    "total_spend": 500,
    "posts": [
        {"post_id": "post_001", "content_type": "image", "likes": 342, "comments": 28, "shares": 15,
         "saves": 45, "reach": 5200, "impressions": 8500, "clicks": 120},
        {"post_id": "post_002", "content_type": "video", "likes": 587, "comments": 42, "shares": 31,
         "saves": 68, "reach": 8900, "impressions": 12400, "clicks": 215},
        {"post_id": "post_003", "content_type": "carousel", "likes": 298, "comments": 19, "shares": 12,
         "saves": 34, "reach": 4100, "impressions": 6800, "clicks": 95},
        {"post_id": "post_004", "content_type": "image", "likes": 120, "comments": 4, "shares": 2,
         "saves": 6, "reach": 9800, "impressions": 15100, "clicks": 40},
    ],
}

COUNT_FIELDS = ("likes", "comments", "shares", "saves", "reach", "impressions", "clicks")


def pct(numerator, denominator):
    """Percentage rounded to 2 places, or None when the denominator is missing or zero."""
    if not denominator:
        return None
    return round(numerator / denominator * 100, 2)


def ratio(numerator, denominator, places=2):
    if not denominator:
        return None
    return round(numerator / denominator, places)


def post_metrics(post: dict, followers) -> dict:
    n = {f: post.get(f, 0) or 0 for f in COUNT_FIELDS}
    engagements = n["likes"] + n["comments"] + n["shares"] + n["saves"]
    return {
        "post_id": post.get("post_id", ""),
        "content_type": post.get("content_type", "unknown"),
        "engagements": engagements,
        "reach": n["reach"],
        "impressions": n["impressions"],
        "engagement_rate": pct(engagements, n["reach"]),
        "engagement_rate_by_followers": pct(engagements, followers),
        "ctr": pct(n["clicks"], n["impressions"]),
        "share_rate": pct(n["shares"], n["impressions"]),
        "save_rate": pct(n["saves"], n["reach"]),
        "reach_rate": pct(n["reach"], followers),
    }


def validate(data: dict) -> list:
    problems = []
    posts = data.get("posts")
    if not isinstance(posts, list) or not posts:
        sys.exit("Error: input needs a non-empty 'posts' array")
    for i, p in enumerate(posts, 1):
        label = p.get("post_id") or f"post {i}"
        for f in ("likes", "comments", "reach"):
            if f not in p:
                problems.append(f"{label}: missing required field '{f}'")
        for f in COUNT_FIELDS:
            v = p.get(f, 0) or 0
            if not isinstance(v, (int, float)) or v < 0:
                problems.append(f"{label}: '{f}' must be a non-negative number")
        if (p.get("reach") or 0) <= 0:
            problems.append(f"{label}: reach is 0, so its rates are skipped")
    spend = data.get("total_spend")
    if spend is not None and (not isinstance(spend, (int, float)) or spend <= 0):
        problems.append("total_spend must be above 0 for cost metrics")
    return problems


def analyze(data: dict) -> dict:
    platform = str(data.get("platform", "unknown")).lower()
    followers = data.get("followers")
    followers_start = data.get("followers_start")
    spend = data.get("total_spend")
    revenue = data.get("revenue")
    conversions = data.get("conversions")
    warnings = validate(data)

    posts = [post_metrics(p, followers) for p in data["posts"]]
    rated = [p for p in posts if p["engagement_rate"] is not None]

    totals = {f: sum((p.get(f, 0) or 0) for p in data["posts"]) for f in COUNT_FIELDS}
    engagements = totals["likes"] + totals["comments"] + totals["shares"] + totals["saves"]
    overall = {
        "posts": len(posts),
        "engagements": engagements,
        "reach": totals["reach"],
        "impressions": totals["impressions"],
        "clicks": totals["clicks"],
        "engagement_rate": pct(engagements, totals["reach"]),
        "engagement_rate_by_followers_per_post": (
            round(statistics.mean(p["engagement_rate_by_followers"] for p in posts), 2) if followers else None),
        "ctr": pct(totals["clicks"], totals["impressions"]),
        "share_rate": pct(totals["shares"], totals["impressions"]),
        "save_rate": pct(totals["saves"], totals["reach"]),
        "median_engagement_rate": round(statistics.median(p["engagement_rate"] for p in rated), 2) if rated else None,
        "follower_growth": pct((followers or 0) - (followers_start or 0), followers_start) if followers and followers_start else None,
    }

    cost = None
    if isinstance(spend, (int, float)) and spend > 0:
        cost = {
            "spend": spend,
            "cpe": ratio(spend, engagements),
            "cpc": ratio(spend, totals["clicks"]),
            "cpm": ratio(spend * 1000, totals["impressions"]),
            "cpa": ratio(spend, conversions) if conversions else None,
            "roas": ratio(revenue, spend) if revenue is not None else None,
            "roi_percent": pct(revenue - spend, spend) if revenue is not None else None,
        }

    ranked = sorted(rated, key=lambda p: p["engagement_rate"], reverse=True)
    k = 3 if len(ranked) >= 6 else max(1, len(ranked) // 2)
    by_type = {}
    for p in rated:
        by_type.setdefault(p["content_type"], []).append(p["engagement_rate"])
    by_type = {t: {"posts": len(v), "avg_engagement_rate": round(statistics.mean(v), 2)}
               for t, v in sorted(by_type.items(), key=lambda kv: -statistics.mean(kv[1]))}

    # Benchmark comparison: per-follower rate when available (the usual basis), else per reach.
    bench = dict(DEFAULT_BENCHMARKS.get(platform, {}))
    bench_source = "default" if bench else None
    if isinstance(data.get("benchmarks"), dict):
        bench.update({k2: v for k2, v in data["benchmarks"].items() if isinstance(v, (int, float))})
        bench_source = "input"
    comparison = {}
    if bench.get("engagement_rate"):
        basis = "followers" if overall["engagement_rate_by_followers_per_post"] is not None else "reach"
        actual = overall["engagement_rate_by_followers_per_post"] if basis == "followers" else overall["engagement_rate"]
        if actual is not None:
            comparison["engagement_rate"] = {
                "actual": actual, "benchmark": bench["engagement_rate"], "basis": basis,
                "multiple": ratio(actual, bench["engagement_rate"]),
            }
    if bench.get("ctr") and overall["ctr"] is not None:
        comparison["ctr"] = {"actual": overall["ctr"], "benchmark": bench["ctr"],
                             "multiple": ratio(overall["ctr"], bench["ctr"])}

    flags = []
    if len(posts) < 10:
        flags.append(f"Only {len(posts)} posts: too little data to call winners; gather more")
    if any(p["engagement_rate"] is not None and p["engagement_rate"] > 100 for p in posts):
        flags.append("An engagement rate above 100%: check the input (reach versus engagements)")
    med_er = overall["median_engagement_rate"]
    imp_values = [p["impressions"] for p in rated if p["impressions"]]
    if med_er and imp_values:
        med_imp = statistics.median(imp_values)
        weak = [p["post_id"] or "?" for p in rated
                if p["impressions"] > med_imp and p["engagement_rate"] < med_er / 2]
        if weak:
            flags.append(f"High impressions, low engagement (reach without resonance): {', '.join(weak)}")
    if totals["saves"] > 2 * totals["shares"] and totals["saves"] >= 20:
        flags.append("Saves far exceed shares: valuable but not social; add a shareable angle")
    if "ctr" in comparison and comparison["ctr"]["multiple"] is not None and comparison["ctr"]["multiple"] < 1:
        flags.append("CTR below benchmark: tighten the promise and use one CTA")
    if "engagement_rate" in comparison and comparison["engagement_rate"]["multiple"] is not None \
            and comparison["engagement_rate"]["multiple"] < 1:
        flags.append("Engagement below benchmark: audit the last 20 posts by format and topic")
    if overall["follower_growth"] is not None and overall["follower_growth"] <= 0:
        flags.append("Follower growth stalled: check cadence, replies, and collaborations")

    return {
        "platform": platform,
        "warnings": warnings,
        "overall": overall,
        "cost": cost,
        "top_posts": ranked[:k],
        "bottom_posts": list(reversed(ranked[-k:])) if len(ranked) > 1 else [],
        "by_content_type": by_type,
        "benchmark_source": bench_source,
        "benchmark_comparison": comparison,
        "flags": flags,
        "posts": posts,
    }


def fmt(value, suffix="%"):
    return "n/a" if value is None else f"{value}{suffix}"


def print_report(r: dict) -> None:
    o = r["overall"]
    print("=" * 64)
    print(f"  SOCIAL METRICS  platform: {r['platform']}  posts: {o['posts']}")
    print("=" * 64)
    for w in r["warnings"]:
        print(f"  ! {w}")
    print("\n  OVERALL")
    print(f"     Engagements:              {o['engagements']}")
    print(f"     Engagement rate (reach):  {fmt(o['engagement_rate'])}   median per post: {fmt(o['median_engagement_rate'])}")
    print(f"     Engagement rate (follow): {fmt(o['engagement_rate_by_followers_per_post'])} per post")
    print(f"     CTR:                      {fmt(o['ctr'])}")
    print(f"     Share rate / save rate:   {fmt(o['share_rate'])} / {fmt(o['save_rate'])}")
    print(f"     Follower growth:          {fmt(o['follower_growth'])}")
    if r["cost"]:
        c = r["cost"]
        print("\n  COST AND RETURN")
        print(f"     Spend: {c['spend']}   CPE: {fmt(c['cpe'], '')}   CPC: {fmt(c['cpc'], '')}   CPM: {fmt(c['cpm'], '')}")
        print(f"     CPA: {fmt(c['cpa'], '')}   ROAS: {fmt(c['roas'], 'x')}   ROI: {fmt(c['roi_percent'])}")
        if c["roas"] is None:
            print("     (ROAS and ROI need real revenue in the input)")
    print("\n  TOP POSTS (engagement rate by reach)")
    for p in r["top_posts"]:
        print(f"     {p['post_id'] or '?':<14} {p['content_type']:<10} {fmt(p['engagement_rate'])}")
    if r["bottom_posts"]:
        print("  BOTTOM POSTS")
        for p in r["bottom_posts"]:
            print(f"     {p['post_id'] or '?':<14} {p['content_type']:<10} {fmt(p['engagement_rate'])}")
    print("\n  BY CONTENT TYPE")
    for t, v in r["by_content_type"].items():
        print(f"     {t:<14} {v['posts']} posts   avg {v['avg_engagement_rate']}%")
    if r["benchmark_comparison"]:
        print(f"\n  BENCHMARK ({r['benchmark_source']}; your own median is the better baseline)")
        for k, v in r["benchmark_comparison"].items():
            basis = f" by {v['basis']}" if "basis" in v else ""
            print(f"     {k}{basis}: {v['actual']}% vs {v['benchmark']}%  ({fmt(v['multiple'], 'x')})")
    if r["flags"]:
        print("\n  FLAGS")
        for f in r["flags"]:
            print(f"     - {f}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Compute social post metrics: engagement, CTR, share and save rates, top and bottom "
                    "posts, content-type averages, cost and return, benchmark comparison, and flags.",
        epilog="Input: JSON object with 'platform' and a 'posts' array (likes, comments, reach required). "
               "Without a file, runs on demo data.",
    )
    parser.add_argument("file", nargs="?", help="JSON input file; omit for demo data")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except OSError as exc:
            sys.exit(f"Error: cannot read {args.file}: {exc}")
        except json.JSONDecodeError as exc:
            sys.exit(f"Error: invalid JSON: {exc}")
        if not isinstance(data, dict):
            sys.exit("Error: input must be a JSON object with a 'posts' array")
    else:
        data = DEMO
        if not args.json:
            print("No input file: running on demo data.\n")

    result = analyze(data)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
