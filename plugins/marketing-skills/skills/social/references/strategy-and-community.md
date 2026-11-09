# Social Strategy, Audits, and Community Management

For requests beyond a single post: building a presence, fixing an underperforming one, scaling it into a system, and running the community around it.

## Contents
- Three Modes
- Current-State Questions
- Platform Selection
- Pillar Mix for a Company Account
- Weekly Pillar Template
- Calendar Generator Config
- Organic Growth Levers
- Community Management
- Social Media Audit
- Flag Without Being Asked
- Content Angle Bank
- Deliverables

## Three Modes

| Mode | When | Deliver |
|------|------|---------|
| **Build a strategy** | No presence yet, or starting on a new platform | Platform choice, 3-5 pillars, cadence, and a 90-day growth plan |
| **Audit and optimize** | Active presence that underperforms | Profile, content, engagement, and performance findings with ranked actions |
| **Scale and systematize** | Growing presence that needs structure | Calendar, batch workflow, team process, and a measurement routine |

## Current-State Questions

Ask these on top of the SKILL.md context questions when the request is a strategy, an audit, or a system:

- **Current state:** which platforms, follower counts, engagement rates, posting frequency, who manages it, what works and what doesn't
- **Goal:** awareness, lead generation, community, or thought leadership, and what success looks like in 90 days
- **Resources:** who creates content and how many hours a week, paid social budget, scheduling and analytics tools in use

## Platform Selection

Not every platform deserves your time. Choose where the audience already spends time, not where you think you should be, and do one or two platforms exceptionally well before adding a third.

Cadence per platform is in the SKILL.md Platform Quick Reference. YouTube suits education and tutorials at 1-2 videos a week; plan it with the **video** skill.

## Pillar Mix for a Company Account

The SKILL.md example is a founder's personal brand. A company account usually leans harder on education and proof:

| Pillar | Purpose | Share | Examples |
|--------|---------|-------|----------|
| Educational | Teach something useful | 40% | How-tos, tips, frameworks |
| Behind the scenes | Build trust through transparency | 20% | Process, team, journey |
| Social proof | Show results and credibility | 15% | Case studies, testimonials, wins |
| Engagement | Start conversations | 15% | Questions you want answered, polls, debates |
| Promotional | Drive business outcomes | 10% | Features, launches, offers |

The low promotional share is deliberate: a feed that reads like an ad channel loses followers. Engagement posts ask real questions; "Agree?" bait is a tell (see SKILL.md).

## Weekly Pillar Template

The SKILL.md weekly template plans by platform; this one plans by pillar for a single platform.

| Day | Pillar | Format | Notes |
|-----|--------|--------|-------|
| Mon | Educational | Long post or carousel | High-value start to the week |
| Tue | Engagement | Question or poll | Early comments help distribution |
| Wed | Behind the scenes | Photo or short video | Humanize the brand |
| Thu | Educational | Thread or how-to | The deep dive |
| Fri | Social proof or promotional | Case study or launch | End-of-week conversion focus |

## Calendar Generator Config

`scripts/social_calendar_generator.py` spreads pillars across dates with a weighted round-robin, so each pillar's share of posts tracks its weight. Config file:

```json
{
  "pillars": [
    {"name": "Educational", "description": "Tips, tutorials, how-tos", "weight": 4,
     "formats": ["Carousel", "How-to thread", "Quick tip"]},
    {"name": "Behind the scenes", "description": "Process, team, journey", "weight": 2},
    {"name": "Social proof", "description": "Case studies, wins", "weight": 2},
    {"name": "Promotional", "description": "Launches, offers", "weight": 1}
  ],
  "platforms": [
    {"name": "LinkedIn", "posts_per_week": 4, "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday"]},
    {"name": "X", "posts_per_week": 15, "best_days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "slots_per_day": 3}
  ],
  "start_date": "2026-01-05",
  "weeks": 4
}
```

- `weight` sets the pillar's share; `formats` (optional) lists the formats to rotate for that pillar.
- `slots_per_day` (default 1) allows several posts a day on one platform. On X, space them about 60 minutes apart (see [x-algorithm.md](x-algorithm.md)).
- The output is a starting calendar. Override slots by hand when a launch or event needs them, and leave room for real-time posts.

## Organic Growth Levers

1. **Consistency.** A schedule you can keep beats bursts.
2. **Questions that invite replies.** Real questions, polls, and defensible takes; never "like if you agree."
3. **Collaboration.** Co-create with complementary accounts.
4. **Repurposing.** One long piece becomes 5-10 posts (see the SKILL.md repurposing system).
5. **Trends.** Join relevant ones fast, only when they fit the brand.
6. **Community spaces.** Groups or chats you host, not only an audience (see **community-marketing**).

## Community Management

The response framework is in SKILL.md (Engagement Strategy). A community plan adds:

- **Response times.** Product questions within 2 hours during business hours; check comments within the first hour after each post.
- **Daily workflow.** Reply to every comment on your posts, then the outbound routine in SKILL.md.
- **Escalation.** Hand to a named owner, and take it out of public replies, for legal threats, safety or security issues, press inquiries, and complaints a public reply can't resolve.

## Social Media Audit

**Profile**
- [ ] Photo recognizable and consistent across platforms
- [ ] Bio states the value you offer, not a list of job titles
- [ ] Link goes to a relevant page, not just the homepage
- [ ] Pinned post is your best-performing or most important content

**Content**
- [ ] Regular cadence, not sporadic
- [ ] Mix balanced across pillars, not all promotional
- [ ] Format variety: text, images, video, carousels
- [ ] Voice consistent with the brand across posts

**Engagement**
- [ ] Response time within 2 hours, not days
- [ ] Replies are genuine, not "thanks!"
- [ ] Outbound engagement with others' content every day
- [ ] Present in relevant groups and conversations

**Performance:** top and bottom posts of the last 20-30, against the account's own median. See [performance-analysis.md](performance-analysis.md). For an X profile, add the checks in [x-growth.md](x-growth.md).

## Flag Without Being Asked

Raise these when you see them in the user's plan or data:

- **The same post planned for every platform**: adapt format, length, and tone per platform before writing.
- **No hook**: write the hook first. Nothing else matters if the first line doesn't land.
- **Unsustainable frequency** (for example, 3 posts a day on 4 platforms): narrow to 1-2 platforms and batch.
- **Promotional content above about 20% of the calendar**: rebalance toward educational and story pillars.
- **No engagement plan**: posting without engaging is broadcasting. Offer the daily routine.
- **The same format every post**: mix text, carousel, video, and polls.
- **Engagement below the account's own baseline**: audit the last 20 posts for what the winners share.
- **High impressions, low engagement**: reach without resonance, a content problem.
- **Follower growth stalled**: check distribution, cadence, and reply activity.
- **A competitor far ahead**: study their top posts with [reverse-engineering.md](reverse-engineering.md).

## Content Angle Bank

Fourteen angles to rotate when ideas run dry, on any platform:

1. Lesson learned from your own experience
2. Framework or system breakdown
3. Tool recommendation, with an honest take
4. Myth busting
5. Behind the scenes of a process or workflow
6. Industry trend analysis
7. Beginner guide
8. Comparison (X vs. Y, and which fits whom)
9. Prediction
10. Case study with real numbers
11. A mistake you made and what changed
12. Quick tactical tip
13. Contrarian take you can defend
14. Curated list of resources, tools, or accounts

## Deliverables

Lead with the deliverable, then the reasoning. Write the hook first, every time.

| Request | Deliver |
|---------|---------|
| A post | Platform-native post: hook, body, CTA, and hashtags within [platform-limits.md](platform-limits.md) |
| Hook options | 5 hooks across curiosity, story, value, contrarian, and data |
| A thread | Hook post, 5-8 body posts, CTA post, with formatting notes |
| A repurposing plan | The source mapped to 5-8 derivative formats across platforms |
| A content calendar | 4-week table of date, platform, pillar, format, and topic, with evergreen and timely posts marked |
| A strategy | Platform choice, pillars, cadence, and a 90-day growth plan |
| An audit | The audit above with prioritized actions |
| A community plan | Response framework, daily workflow, and escalation rules |
| A performance analysis | Metrics per post and overall, top and bottom posts, benchmark context, and ranked actions |
