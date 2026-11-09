# Launching and Measuring a Free Tool

A free tool with no distribution is code on a server. This reference covers the launch sequence, the first 90 days of measurement, what to do when a launch flops, and upkeep. For launch-platform tactics and the general launch framework, see the **launch** skill.

## Contents
- The Launch Mindset
- Pre-Launch Checklist
- Launch Week
- Weeks 2-4: Links and Content
- First 90 Days
- When a Launch Flops
- Maintenance

## The Launch Mindset

Posting once and waiting brings a short spike from existing followers and then nothing. A real launch is about four weeks of sustained distribution: you are seeding, not announcing, and the search value compounds for months.

---

## Pre-Launch Checklist (1-2 weeks before)

### Search foundations
- [ ] Target keyword confirmed (search volume, low-to-medium competition)
- [ ] URL slug fixed, for example `/tools/[keyword-rich-name]`
- [ ] Meta title: "[Free tool name] — [what it does] | [Brand]"
- [ ] Meta description (about 155 characters) with the keyword and what the user gets
- [ ] H1 matches search intent, not just the brand name
- [ ] `SoftwareApplication` markup added (see the **schema** skill)
- [ ] Internal links from related content to the tool, and from the tool to 2-3 related resources

### Tool quality gate
- [ ] Core value in about three inputs
- [ ] Results render on mobile
- [ ] Results are shareable (unique URL, copy button or share)
- [ ] Lead capture in place, after the value, not before
- [ ] Emailed results arrive, if you send them
- [ ] Bad inputs produce helpful errors
- [ ] Fast load: slow tools lose visitors before the first result

### Analytics
- [ ] Analytics installed with events: `tool_started`, `tool_completed`, `lead_captured`, `result_shared`
- [ ] Search console verified
- [ ] Session recordings or heatmaps to watch real use, with consent where required

### Outreach list
- [ ] 20-50 sites that link to similar free tools
- [ ] Newsletters in your category that feature tools
- [ ] Communities where your audience gathers
- [ ] People who regularly share tools in your space

---

## Launch Week

| Day | Focus | Actions |
|-----|-------|---------|
| 1 | Search and directories | Request indexing in the search consoles; submit to relevant directories; publish a 600-900 word post that explains the tool and links to it |
| 2 | Launch platform (optional) | If it fits your audience, launch on a launch platform and answer every comment personally (see the **launch** skill) |
| 3 | Community seeding | Share it as a resource, not a promotion: "I built this free [tool] for [audience] because I couldn't find one — feedback welcome." "Check out our new tool" posts get removed as spam |
| 4 | Your email list | A short dedicated email: what it is, why you built it, one example result, the link. Ask readers to share it with one person who would benefit |
| 5 | Technical communities | For technically interesting or niche tools, a "Show"-style post with an honest builder angle; stay available all day for questions. Generic marketing tools don't land there |
| 6-7 | Social | A walkthrough thread or a short screen recording of you using the tool, posted by a person (the founder) rather than only the company page; personal messages to five people who will love it |

---

## Weeks 2-4: Links and Content

### Backlink outreach

Most of the long-term search value comes from here.

**Find targets:**
1. Search for "best free tools for [your category]" and contact the authors of those lists
2. Use a backlink tool to find pages that link to similar tools; the same pages may link to yours
3. Find bloggers who already write about a competitor's tool

**Outreach template:**
```
Subject: Free [tool name] that might fit your "[resource list title]" post

Hi [Name],

I read your post on the best free tools for [category]. I recently built [tool name]
— it helps [audience] [specific outcome] without [common pain point].

[Direct link to the tool]

Would it fit your list? I'm happy to give you early access or a custom embed if that helps.

[Your name]
```

**Volume:** 50-100 personalized emails in the first 30 days; expect roughly 5-15% positive replies (a rule of thumb). One good resource-page link is worth more than dozens of generic directory listings.

### Content that multiplies
- A guide built around the tool: "How to [goal], with a free calculator to check your numbers"
- A results study: "We analyzed 500 [things] with our [tool]; here's what we found"
- A guest post for a newsletter that features the tool as the main resource

---

## First 90 Days

### Weekly check-ins

| Week | What to look for |
|------|------------------|
| 1 | Traffic from launch channels; completion rate (under ~40% means fix the UX) |
| 2-4 | Launch-channel traffic tails off; the first links arrive |
| 5-8 | First organic impressions; check which queries bring traffic |
| 9-12 | Organic traffic visible; lead capture rate stable |

### Review gates at day 90

These are starting assumptions for a go/fix decision, not benchmarks: no comparable sourced rates exist (see [tool-benchmarks.md](tool-benchmarks.md)). Replace them with your own baseline once you have one. Session thresholds scale with the size of your market and language.

| Metric | Needs work | Good | Great |
|--------|-----------|------|-------|
| Organic sessions per month | <200 | 500-2,000 | >5,000 |
| Tool completion rate | <30% | 40-60% | >70% |
| Lead conversion (completions → email) | <3% | 5-15% | >20% |
| Referring domains | <5 | 10-30 | >50 |

---

## When a Launch Flops

A tool usually fails for one of four reasons:

1. **Wrong keyword** — nobody searches for it. Zero impressions after about 60 days means the target is wrong; move the page copy to a related term with volume.
2. **Wrong problem** — the tool works, but the problem isn't acute enough. Talk to five people who used it once and never returned: what were they hoping for?
3. **Gated too early** — high traffic, low completion. You ask for the email before delivering value; move or remove the gate.
4. **Too little distribution** — the tool is fine, but it was shared once. Run outreach again with a fresh list, submit to more directories, write the guide post.

Many "failed" tools simply never got their 90-day distribution campaign.

---

## Maintenance

A free tool is a multi-year asset, not a three-week campaign.

**Monthly**
- Check the tool still works (APIs, URLs, formulas)
- Review the top search queries and update headings and copy to match
- Ship one improvement from user requests

**Quarterly**
- Refresh any data the tool relies on (benchmarks, averages, rates)
- Refresh the landing page copy
- Find 20 new link targets and run outreach

**Yearly**
- Full UX review on current mobile browsers
- Competitive check: are better free alternatives emerging?
- Decide: invest more, maintain as is, or retire and redirect
