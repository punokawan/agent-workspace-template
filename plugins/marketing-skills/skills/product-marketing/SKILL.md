---
name: product-marketing
description: "When the user wants to create or update their product marketing context document, or work out positioning before recording it. Also use when the user mentions 'product context,' 'marketing context,' 'set up context,' 'positioning,' 'positioning statement,' 'messaging hierarchy,' 'who is my target audience,' 'describe my product,' 'ICP,' 'ideal customer profile,' 'brand voice,' 'tone of voice,' 'target markets,' 'which language do we write in,' 'what have we learned,' 'log this learning,' or wants to avoid repeating foundational information across marketing tasks. Use this at the start of any new project before using other marketing skills: it creates the context file (one per product) that every other skill reads for product, audience, language, and positioning, and it defines where that file lives. For visual identity and full brand guidelines, see brand-guidelines. For battle cards, see sales-enablement. For a full go-to-market plan, see marketing-plan."
metadata:
  version: 1.0.0
  sources: "corey:product-marketing@96798cf; ali:marketing-context@8f08254; ali:marketing-strategy-pmm@8f08254"
---

# Product Marketing Context

You help users create and maintain a product marketing context document. This captures foundational positioning and messaging information that other marketing skills reference, so users don't repeat themselves.

Every other marketing skill reads this document first, so where it lives follows the rules below.

## Where the Context Lives

Resolve the path before you read or write anything.

1. **Identify the active product.** In a workspace that hosts several products (for example a `projects/<project>/` layout, one folder per product), the active product is the one the task is about: the product the user named, or the product folder that holds the files being worked on. If the active product is unclear, ask which product before reading or writing any context.
2. **Use the path for the layout:**

   | Layout | Context file |
   |--------|--------------|
   | Workspace with several products | `projects/<project>/product-marketing.md`, inside that product's folder: one file per product |
   | Single-product repository | `.agents/product-marketing.md` in the repository root |

3. **Read legacy locations if present:** `.claude/product-marketing.md`, and `product-marketing-context.md` in `.agents/` or `.claude/`. If you find one, use it and offer to move it to the path above. In a multi-product workspace, a legacy file at the shared root belongs to no product by default: confirm which product it describes before you use it, then move it into that product's folder.
4. **Keep products apart.** Write a product's context only at its own path. Never write it where another product's work can read it, such as a shared workspace root, and never copy context, learnings, or voice from one product's file into another's.

Files that support the context, such as personal voice guides, sit next to the context file under the same rules.

## Workflow

### Step 1: Check for Existing Context

First, resolve the context path (see **Where the Context Lives**) and check whether the file exists there or at a legacy location.

**If it exists:**
- Read it and summarize what's captured — note its current **Document version** and the last few **Changelog** entries so the user sees where the doc stands and what's changed recently
- Flag gaps without being asked: no verbatim customer quotes, no named competitors, no brand voice, proof points without numbers, no primary language, or a **Last updated** date more than 6 months old (positioning may have shifted). The completeness check finds these in one run (see **Checking Completeness**).
- Ask which sections they want to update
- Only gather info for those sections
- On any substantive save, bump the version and add a changelog entry (see Step 4). This doc is the shared context every other marketing skill reads, so a dated paper trail of *what changed and why* is worth keeping.

**If it doesn't exist, offer two options:**

1. **Auto-draft from codebase** (recommended): You'll study the repo—README, landing pages, marketing copy, package.json, etc.—and draft a V1 of the context document. The user then reviews, corrects, and fills gaps. This is faster than starting from scratch.

2. **Start from scratch**: Walk through each section conversationally, gathering info one section at a time.

Most users prefer option 1. After presenting the draft, ask: "What needs correcting? What's missing?"

### Step 2: Gather Information

**If auto-drafting:**
1. Read the codebase: README, landing pages, marketing copy, about pages, meta descriptions, package.json, any existing docs
2. Draft all sections based on what you find
3. Present the draft and ask what needs correcting or is missing
4. Iterate until the user is satisfied

**If starting from scratch:**
Walk through each section below conversationally, one at a time. Don't dump all questions at once.

For each section:
1. Briefly explain what you're capturing
2. Ask relevant questions
3. Confirm accuracy
4. Move to the next

Push for verbatim customer language — exact phrases are more valuable than polished descriptions because they reflect how customers actually think and speak, which makes copy more resonant.

### When Positioning Isn't Settled

The context file records positioning; it doesn't invent it. Work positioning out before you fill Competitive Landscape and Differentiation when:
- The user asks for positioning, a positioning statement, an ICP, or a messaging hierarchy
- Differentiation lists features any competitor could claim, or the target audience is "everyone"
- The homepage, sales deck, and ads describe the product differently
- A competitor repositioned, win rates against a named competitor dropped, or the product outgrew its category

Follow [references/positioning.md](references/positioning.md): derive the ICP from best-fit customers, work the positioning chain (alternatives → unique attributes → value → who cares most → market category), validate it with customers, then record the result here and build the messaging hierarchy on it.

---

## Sections to Capture

### 1. Product Overview
- One-line description
- What it does (2-3 sentences)
- Product category (what "shelf" you sit on—how customers search for you)
- Product type (SaaS, marketplace, e-commerce, service, etc.)
- Business model and pricing

### 2. Target Audience
- Target company type (industry, size, stage)
- Target decision-makers (roles, departments)
- Primary use case (the main problem you solve)
- Jobs to be done (2-3 things customers "hire" you for)
- Specific use cases or scenarios

### 3. Languages & Markets
Drafting skills use this to choose the language of audience-facing copy, so record it rather than infer it. There is no default language: if the user hasn't said and the product's own materials don't settle it, ask.
- Primary language and locale (a language tag such as `pt-BR` or `fr-CA`): the language most audience-facing copy is written in
- Other languages or locales, and where each is used (site, app, support, ads, sales)
- Tone per language: formality and form of address (formal or informal "you"), what doesn't carry over (humor, idioms), and brand terms that stay untranslated
- Target markets or regions in priority order, and what differs per market (currency, pricing, regulation, channels, proof that works)

Other skills write in the language the task names. When it names none, they use the primary language recorded here; when nothing is recorded, they ask. The language the user chats in is not evidence of the audience's language. To plan entry into a new market, see **marketing-plan** (international go-to-market).

### 4. Personas (B2B only)
If multiple stakeholders are involved in buying, capture for each:
- User, Champion, Decision Maker, Financial Buyer, Technical Influencer
- What each cares about, their challenge, and the value you promise them

### 5. Problems & Pain Points
- Core challenge customers face before finding you
- Why current solutions fall short
- What it costs them (time, money, opportunities)
- Emotional tension (stress, fear, doubt)

### 6. Competitive Landscape
- **Direct competitors**: Same solution, same problem (e.g., Calendly vs SavvyCal)
- **Secondary competitors**: Different solution, same problem (e.g., Calendly vs Superhuman scheduling)
- **Indirect competitors**: Conflicting approach (e.g., Calendly vs personal assistant)
- How each falls short for customers

### 7. Differentiation
- Key differentiators (capabilities alternatives lack)
- How you solve it differently
- Why that's better (benefits)
- Why customers choose you over alternatives

### 8. Objections & Anti-Personas
- Top 3 objections heard in sales and how to address them
- Who is NOT a good fit (anti-persona)

### 9. Switching Dynamics
The JTBD Four Forces:
- **Push**: What frustrations drive them away from current solution
- **Pull**: What attracts them to you
- **Habit**: What keeps them stuck with current approach
- **Anxiety**: What worries them about switching

### 10. Customer Language
- How customers describe the problem (verbatim)
- How they describe your solution (verbatim)
- Words/phrases to use
- Words/phrases to avoid
- Glossary of product-specific terms

### 11. Brand Voice
- 3-5 voice attributes, each with what it means, what it doesn't mean, and a real line from existing copy
- Tone by context: how the voice shifts for support, launches, errors, sales, and social
- Brand words: terms you own, words you never use (with the reason)
- Style rules: capitalization for headings and buttons, number, date, and currency formats, formatting habits (lists, bold, emoji), and the exact spelling of product names

Build this from copy that already performed and from the founder's own writing, rather than from adjectives picked in a meeting. See [references/brand-voice.md](references/brand-voice.md) for the extraction steps, a worked profile, before/after examples, and per-person voice guides.

### 12. Proof Points
- Key metrics or results to cite
- Notable customers/logos
- Testimonial snippets
- Main value themes and supporting evidence

### 13. Goals
- Primary business goal
- Key conversion action (what you want people to do)
- Current metrics (if known)

### 14. Content & SEO (optional, for content and SEO work)
The content and SEO skills read this so keyword targets and internal links stay consistent from piece to piece.
- Keyword clusters: topic, primary keyword, secondary keywords, search intent (one set per language if you target several)
- Key pages to link to: page, URL, what it's for, preferred anchor text
- Exemplary pieces: 3-5 URLs or files the team considers on-voice and on-strategy, with what makes each good
- Length and format preferences

### 15. Paid Ads (optional, only if they run ads)
The **ads** skill reads this so the user doesn't re-explain the account every session.
- Margin reality: the target CPA or ROAS that keeps the business profitable, and the hard floor (the ROAS below which, or CPA above which, to flag immediately)
- Budget and pacing: monthly budget and acceptable daily variance
- Conversion truth: which conversion actions count and what each is worth, known tracking weaknesses (lag, double counting, offline gaps), and what separates a good lead from a form fill
- Campaign naming convention and what each campaign is for, one line each
- What the agent may do (read, compare, flag, draft, recommend) and may not do without approval (change budgets or bids, pause or launch, edit tracking, publish ads)

### 16. Learnings
Start this empty. It fills up as work ships (see "Maintaining Learnings" below).

---

## Step 3: Create the Document

After gathering information, create the context file at the path from **Where the Context Lives** with this structure:

```markdown
# Product Marketing Context

**Document version:** v1
**Last updated:** [date]

## Product Overview
**One-liner:**
**What it does:**
**Product category:**
**Product type:**
**Business model:**

## Target Audience
**Target companies:**
**Decision-makers:**
**Primary use case:**
**Jobs to be done:**
-
**Use cases:**
-

## Languages & Markets
**Primary language and locale:**
**Languages:**
| Language / locale | Used for | Tone and form of address |
|-------------------|----------|--------------------------|
| | | |
**Target markets / regions:**
| Market or region | Priority | What differs (currency, pricing, regulation, channels, proof) |
|------------------|----------|----------------------------------------------------------------|
| | | |

## Personas
| Persona | Cares about | Challenge | Value we promise |
|---------|-------------|-----------|------------------|
| | | | |

## Problems & Pain Points
**Core problem:**
**Why alternatives fall short:**
-
**What it costs them:**
**Emotional tension:**

## Competitive Landscape
**Direct:** [Competitor] — falls short because...
**Secondary:** [Approach] — falls short because...
**Indirect:** [Alternative] — falls short because...

## Differentiation
**Key differentiators:**
-
**How we do it differently:**
**Why that's better:**
**Why customers choose us:**

## Objections
| Objection | Response |
|-----------|----------|
| | |

**Anti-persona:**

## Switching Dynamics
**Push:**
**Pull:**
**Habit:**
**Anxiety:**

## Customer Language
**How they describe the problem:**
- "[verbatim]"
**How they describe us:**
- "[verbatim]"
**Words to use:**
**Words to avoid:**
**Glossary:**
| Term | Meaning |
|------|---------|
| | |

## Brand Voice
| Attribute | Means | Doesn't mean | Example line |
|-----------|-------|--------------|--------------|
| | | | |

**Tone by context:**
- Support:
- Launch:
- Errors:
- Sales:
- Social:
**Terms we own:**
**Never use (and why):**
**Style rules:**

## Proof Points
**Metrics:**
**Customers:**
**Testimonials:**
> "[quote]" — [who]
**Value themes:**
| Theme | Proof |
|-------|-------|
| | |

## Goals
**Business goal:**
**Conversion action:**
**Current metrics:**

## Content & SEO (optional)
**Keyword clusters:**
| Cluster | Primary keyword | Secondary keywords | Intent |
|---------|-----------------|--------------------|--------|
| | | | |
**Key pages to link to:**
| Page | URL | Use for | Anchor text |
|------|-----|---------|-------------|
| | | | |
**Exemplary pieces:**
- [URL or file] — [what makes it good]
**Length and format preferences:**

## Paid Ads (optional)
**Target CPA / ROAS:**
**Hard floor:**
**Monthly budget and daily variance:**
**Conversions that count:**
| Action | Means | Value | Feeds bidding? |
|--------|-------|-------|----------------|
| | | | |
**Known tracking weaknesses:**
**Good lead vs. form fill:**
**Campaigns:** [name] — [what it's for]
**Agent may:** read, compare, flag, draft, recommend
**Agent may not (without approval):** change budgets or bids, pause or launch, edit tracking, publish ads

## Learnings
*Decisions and tested lessons. Newest first. Keep it to about 20 active entries.*
| Date | Learning | Evidence | Applies to | Status |
|------|----------|----------|------------|--------|
| | | | | |

## Changelog
*Newest first. One line per revision: what changed and why.*
- v1 ([date]) — Initial context.
```

Delete optional sections the product doesn't use rather than leaving them empty.

---

## Step 4: Confirm, Version, and Save

- Show the completed document
- Ask if anything needs adjustment
- **Set the version and changelog** — this is the paper trail for a doc every other skill reads:
  - **New document:** set `Document version: v1` and a single Changelog entry — `- v1 ([today]) — Initial context.`
  - **Updating an existing document:** increment the version (v2 → v3 …), update `Last updated` to today, and **prepend a new Changelog entry** at the top of the list (newest first) summarizing *what changed and why* in one line. Never rewrite or reorder past entries.
  - A good entry names the sections touched and the reason, not "updated the doc." Examples:
    - `- v3 (2026-07-16) — Repositioned from "email tool" to "deliverability platform"; added RevOps to the ICP.`
    - `- v2 (2026-06-02) — Rewrote value prop and objections after 5 customer interviews; added competitor Acme.`
  - Use today's date in ISO form (YYYY-MM-DD) for the entry and `Last updated`.
  - **Pure typo-only fix:** don't bump the version or add a changelog entry — just save the correction. Every other change bumps the version and gets an entry. When the change is a real repositioning, say so plainly — downstream skills will now generate against the new context.
- Run the completeness check (see **Checking Completeness**) and fill any required section the user can answer now
- Save to the context path from **Where the Context Lives**
- Tell them: "Other marketing skills will now use this context automatically. The Changelog at the bottom tracks every revision — check it to see how your positioning has evolved. Run `/product-marketing` anytime to update it."

---

## Checking Completeness

Score the file after you write or update it, and when you review an existing one:

```bash
python3 scripts/context_validator.py <context-file>          # readable report
python3 scripts/context_validator.py <context-file> --json   # for other tools
python3 scripts/context_validator.py --demo                  # built-in sample
```

The script only reads the file you pass (no writes, no network). It expects the section headings from Step 3. A field counts only when it holds real content: `[placeholders]`, empty table rows, and bare bullets don't count. Optional sections the product doesn't use (Personas, Content & SEO, Paid Ads) are skipped when absent or empty. It scores 0-100 and warns about missing verbatim quotes, proof points without numbers, no primary language, no version line or Changelog, and a **Last updated** date older than 180 days (`--max-age-days` changes it).

- **Score below 70, or a required section missing:** go back to the interview and fill those sections before calling the context done. Sibling skills quietly turn generic when the file is thin.
- **Score 70 or above:** the file is usable. The score measures coverage, not quality: a full file can still hold weak positioning.

---

## Maintaining Learnings

The Changelog records how the document changed. **Learnings** records what the team found out by shipping: which angles won, which offers flopped, which decisions were made and why. Drafting skills (copywriting, emails, ads, ad-creative, social) read it before writing so the next brief starts from what's already known.

**Entry format:** one row per learning.
- **Learning:** one sentence, specific enough to change a draft. "Price-anchored headlines beat outcome headlines on the pricing page" works. "Be clearer" doesn't.
- **Evidence:** the test, campaign, or source, with the number and sample size. "Variant B +18% trial starts, 2,400 visitors per arm, 3 weeks."
- **Applies to:** the channels, segments, or skills it affects.
- **Status:** `active`, `watch` (one data point, worth retesting), or `retired`.

**What earns a place:**
- A test result that reached its planned sample, or the same pattern seen in two or more campaigns
- A decision the user made with a reason (positioning, pricing, a channel cut) that future drafts must respect
- A correction the user gave more than once ("never call it a platform")

**What doesn't:** single-run anecdotes (log those as `watch` or leave them out), task notes, and anything that belongs in another section. A new objection goes in Objections; a new customer phrase goes in Customer Language.

**When to retire an entry:** a later test contradicts it, the product or market changed underneath it (new pricing, new ICP), or it hasn't been relevant for two quarters. Change the status to `retired` and add a line saying why, rather than deleting it, so nobody re-tests a settled question. Move retired rows to the bottom, and archive them once the table passes about 20 active rows.

**Who writes it:** any skill that finishes a test, campaign, or postmortem may propose a row. Show the proposed row to the user and add it on approval, with a version bump and a Changelog line like any other substantive change. Loops that run on a schedule do this through their session-end step (see **marketing-loops**).

---

## Tips

- **Be specific**: Ask "What's the #1 frustration that brings them to you?" not "What problem do they solve?"
- **Capture exact words**: Customer language beats polished descriptions
- **Ask for examples**: "Can you give me an example?" unlocks better answers
- **Validate as you go**: Summarize each section and confirm before moving on
- **Skip what doesn't apply**: Not every product needs all sections (e.g., Personas for B2C, Paid Ads if they don't run ads)

## Related Skills

- **customer-research**: For the interviews and review mining that feed Customer Language, Switching Dynamics, and the ICP
- **competitor-profiling**: For researching competitors before you fill Competitive Landscape
- **sales-enablement**: For battle cards, persona cards, and win-loss analysis built on this positioning
- **copywriting**: For turning the messaging hierarchy into page copy
- **launch**: For launch plans that start from this positioning
- **marketing-plan**: For a full go-to-market plan, including entry into new markets
- **brand-guidelines**: For visual identity and a complete brand guideline document

Sources and credits: [SOURCES.md](SOURCES.md)
