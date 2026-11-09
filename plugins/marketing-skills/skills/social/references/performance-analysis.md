# Social Performance Analysis

Turning post data into a verdict: which posts and formats work, how a platform compares with your baseline, and what spend returned. For tracking setup (UTMs, events), see the **analytics** skill.

## Contents
- Workflow
- Input
- Metric Definitions
- Cost and Return
- Benchmarks
- Diagnose
- Comparing Competitors
- Metrics Calculator

## Workflow

1. **Validate the data.** Reach above 0 for every post, counts not negative, dates valid, platform named, spend above 0 if cost metrics are wanted.
2. **Compute per-post metrics**, then campaign totals.
3. **Add cost metrics** if spend is given, and return metrics only if real revenue or conversions are given.
4. **Compare against the account's own median first**, then against published benchmarks.
5. **Rank top and bottom posts** and find what each group shares: format, topic, hook, posting time.
6. **Recommend** the next tests, ranked.

Sanity check before reporting: an engagement rate above 100%, or cost figures that don't reconcile with spend, mean the input is wrong.

## Input

| Field | Required | Notes |
|-------|----------|-------|
| `platform` | Yes | instagram, facebook, x, linkedin, tiktok |
| `posts[].likes`, `posts[].comments` | Yes | Reactions count as likes |
| `posts[].reach` | Yes | Unique accounts reached |
| `posts[].impressions` | No | Total views |
| `posts[].shares`, `posts[].saves`, `posts[].clicks` | No | Reposts count as shares; bookmarks as saves |
| `posts[].content_type`, `posts[].post_id`, `posts[].posted_at` | No | Needed for format and timing patterns |
| `followers`, `followers_start` | No | Reach rate, per-follower engagement, follower growth |
| `total_spend`, `revenue`, `conversions` | No | Cost and return metrics |

## Metric Definitions

| Metric | Formula | Tells you |
|--------|---------|-----------|
| Engagement rate (by reach) | (likes + comments + shares + saves) ÷ reach × 100 | Interaction among the people who saw it |
| Engagement rate (by followers) | (likes + comments + shares + saves) ÷ followers × 100 | The basis most published benchmarks use |
| Click-through rate | clicks ÷ impressions × 100 | Click appeal |
| Reach rate | reach ÷ followers × 100 | Distribution beyond and within the audience |
| Share rate | shares ÷ impressions × 100 | Share-worthiness |
| Save rate | saves ÷ reach × 100 | Lasting value |
| Follower growth | (followers − followers at start) ÷ followers at start × 100 | Audience momentum over the period |

Weigh comments, shares, and saves above likes: they take more effort and carry more signal.

## Cost and Return

| Metric | Formula |
|--------|---------|
| Cost per engagement (CPE) | spend ÷ engagements |
| Cost per click (CPC) | spend ÷ clicks |
| Cost per thousand impressions (CPM) | spend ÷ impressions × 1,000 |
| Cost per acquisition (CPA) | spend ÷ conversions |
| Return on ad spend (ROAS) | revenue ÷ spend |
| ROI | (revenue − spend) ÷ spend × 100 |

Compute ROI only from real revenue. Assigning dollar values to likes or shares produces a made-up ROI. Read ROAS and CPA against the account's margin and target customer acquisition cost (see **attribution** for multi-touch credit).

## Benchmarks

Use the account's own trailing median as the main baseline. Published ranges differ by source, year, and basis (per reach or per follower), and the figures below came without sources. Treat them as rough context for a first read, not as targets.

**Engagement rate by platform (industry figures, 2024-2025)**

| Platform | Average | Good | Excellent |
|----------|---------|------|-----------|
| Instagram | 1.22% | 3-6% | >6% |
| Facebook | 0.07% | 0.5-1% | >1% |
| X | 0.05% | 0.1-0.5% | >0.5% |
| LinkedIn | 2.0% | 3-5% | >5% |
| TikTok | 5.96% | 8-15% | >15% |

**Engagement rate by industry**

| Industry | Instagram | Facebook | LinkedIn |
|----------|-----------|----------|----------|
| Retail | 1.0% | 0.08% | 1.8% |
| Technology | 0.9% | 0.06% | 2.5% |
| Healthcare | 1.5% | 0.12% | 2.2% |
| Finance | 0.8% | 0.05% | 2.8% |
| Food and beverage | 1.8% | 0.15% | 1.5% |
| Travel | 1.4% | 0.10% | 1.9% |
| B2B services | 0.7% | 0.04% | 3.2% |

**Click-through and cost by platform**

| Platform | Organic CTR (avg) | Paid CTR (avg) | CPC (avg) | CPM (avg) | CPE (avg) |
|----------|-------------------|----------------|-----------|-----------|-----------|
| Instagram | 0.22% | 0.58% | $1.20 | $7.91 | $0.15 |
| Facebook | 0.90% | 0.90% | $0.97 | $7.19 | $0.12 |
| X | 0.86% | 1.55% | $0.38 | $6.46 | $0.08 |
| LinkedIn | 0.44% | 0.44% | $5.26 | $33.80 | $0.80 |
| TikTok | 0.30% | 0.84% | $1.00 | $10.00 | $0.10 |

For paid social bidding and creative, see **ads** and **ad-creative**.

**Engagement by content type**

| Platform | Format: average engagement |
|----------|---------------------------|
| Instagram | Reels 1.95% · carousels 1.92% · single image 1.18% · Stories about 0.5% link taps |
| Facebook | Video 0.26% · photo 0.12% · link 0.05% · text status 0.04% |
| LinkedIn | Document (PDF) posts 3.5% · native video 2.8% · image 2.0% · text only 1.8% · link 1.2% |
| TikTok | Trending sound 8-12% · tutorial 6-10% · behind the scenes 5-8% · product demo 4-7% |

## Diagnose

| Pattern | Likely cause | Next step |
|---------|--------------|-----------|
| High impressions, low engagement | Reach without resonance | Rework hooks and topics against your top posts |
| Engagement below your own median | Content isn't landing | Audit the last 20 posts by format and topic |
| Follower growth stalled | Distribution or cadence | Check frequency, reply activity, and collaborations |
| High saves, few shares | Valuable but not social | Add a shareable angle: a take, a story, a number |
| Low CTR | The promise and the CTA don't match | Tighten the promise; one CTA |
| A competitor far ahead | Content gap | Study their top posts with [reverse-engineering.md](reverse-engineering.md) |
| Fewer than 10 posts | Too little data | Gather more before calling winners |

## Comparing Competitors

Compare accounts on the same basis: per-follower engagement rate ((average likes + replies + reposts) ÷ followers × 100), posts per week, format mix, and their most-covered topics. The useful output is the gap: topics and formats your audience engages with that competitors skip. Collect the data with the method in [reverse-engineering.md](reverse-engineering.md).

## Metrics Calculator

`scripts/social_metrics.py` computes everything above from a JSON file in the Input format:

```bash
python3 <skill-dir>/scripts/social_metrics.py posts.json          # report
python3 <skill-dir>/scripts/social_metrics.py posts.json --json   # machine-readable
python3 <skill-dir>/scripts/social_metrics.py                     # demo data
```

It reports per-post and campaign metrics, the account's median engagement rate, top and bottom posts, averages by content type, cost and return metrics when spend, revenue, or conversions are given, a comparison with the engagement benchmark above (or your own, via `"benchmarks": {"engagement_rate": 2.5, "ctr": 0.8}` in the input), and the diagnostic flags from the table above.
