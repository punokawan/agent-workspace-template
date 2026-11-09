# Internal Linking Playbook

Linking patterns, anchor text, and the orphan-page workflow. Use this for an internal linking plan or audit. The rules and checklist live in SKILL.md; navigation links are in [navigation-patterns.md](navigation-patterns.md).

## Contents
- Linking patterns
- Anchor text
- Finding linking opportunities
- Orphan page recovery
- Patterns that fail

---

## Linking patterns

### Hub and spoke (topic cluster)
For content sites, blogs, and feature or solution pages.

```
Hub (pillar page)
├── Spoke 1 (sub-topic)
│   ├── Deep 1a (specific guide)
│   └── Deep 1b
├── Spoke 2
│   └── Deep 2a
└── Spoke 3
```

- Hub → every spoke, with in-body links, not only a list at the bottom.
- Each spoke → hub, with anchor text that describes the hub's topic.
- Spoke → adjacent spoke only when genuinely relevant.
- Deep page → its spoke and the hub.

The hub earns authority because everything in the cluster links to it. A cluster with no hub, or a hub that misses some spokes, is broken.

### Linear (sequential content)
For courses, multi-part guides, and documentation.

- Each part links to the next and the previous part.
- An index page links to every part.

### Content to conversion
For SaaS and lead-generation sites, where blog posts collect most external links and money pages collect almost none.

```
Blog post (awareness) → Feature page (consideration) → Pricing (decision)
Blog post (awareness) → Case study (proof) → Trial or demo
```

- Every blog post links in context to at least one relevant product or feature page.
- Case studies link to the matching feature or solution page and to pricing.
- Feature pages link to relevant case studies and to pricing.

### Authority distribution from the homepage
The homepage usually holds the most external links. Link it to the 5–8 priority hubs and sections, not to every post; each hub passes authority down to its children.

---

## Anchor text

| Type | Example | Use |
|---|---|---|
| Descriptive partial match | "writing effective cold emails" | Most internal links |
| Exact match | "cold email templates" | Occasionally, where it reads naturally |
| Page title or branded | "our guide to cold outreach" | Fine, adds variety |
| Generic | "click here," "learn more" | Avoid: it says nothing about the target |
| Naked URL | `https://example.com/guide` | Avoid for internal links |

- Vary the wording across the links that point to one page; fifteen identical anchors look manufactured and cover fewer phrasings.
- Write the anchor into the sentence: "For tactical patterns, see our [cold email frameworks](link)."

---

## Finding linking opportunities

1. **New page, old mentions.** Search the site for the topic (`site:example.com "cold email"`). Every page that mentions it without linking to the new page is a candidate for a contextual link.
2. **Crawl export.** Export internal links from a crawler and count inbound links per URL:
   - 0 inbound: orphan, fix now.
   - 1–2 inbound: at risk, add links from related pages.
   - Many outbound, few inbound: a page that gives authority but gets none; link to it from its cluster.
3. **Cluster gaps.** For each hub, list its spokes and check that the hub links to every one.

---

## Orphan page recovery

An orphan has no internal links pointing to it, so crawlers and visitors rarely reach it.

**Find them:** compare the URLs that should be indexed (sitemap or Search Console export) with the URLs that receive internal links (crawl export). The site-architecture `scripts/sitemap_analyzer.py --linked` option does this comparison.

**Classify them:**

| Type | Action |
|---|---|
| Valuable content with no home | Link from relevant pages and add to its hub |
| Campaign landing pages (paid, events) | Often unlinked on purpose; make sure they're `noindex` if they shouldn't rank |
| Duplicate or thin content | Merge into the stronger page with a 301, or `noindex` |
| Outdated content | 301 to the current version, or 410 if nothing replaces it |

**Fix in this order:**
1. Orphans with external backlinks (authority flows in and goes nowhere)
2. Orphans with good content and search demand
3. Thin orphans: fix the content first, then link

---

## Patterns that fail

- **Related-posts widgets as the only links.** Widgets link by tag, not by what you want to rank. Keep them as a supplement to deliberate in-body links.
- **Money pages linked only from navigation.** Add contextual links from relevant posts and case studies to feature and pricing pages.
- **Generic anchors on important pages.** Thirty links that say "our guide" pass authority but no topic. Rewrite the anchors.
- **Never revisiting old posts.** Older posts collect links but rarely point to newer, better pages. When you publish, add links from the older posts on the same topic.

---

*Patterns, anchor guidance, and the orphan workflow are adapted from the ali library's `site-architecture` skill (internal-linking-playbook.md, MIT).*
