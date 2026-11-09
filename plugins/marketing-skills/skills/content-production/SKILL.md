---
name: content-production
description: "Produce a blog post, article, or guide end to end: research and brief, outline and draft, then SEO, readability, and voice passes and pre-publish quality gates. Use when the user asks to write a blog post, draft an article or guide on a topic, turn notes or a transcript into a full piece, write a content brief, or check a draft before it goes live. Includes a quality-gate checker and a readability scorer. For deciding what to write, see content-strategy; for landing and product page copy, see copywriting; for editing or humanizing an existing draft, see copy-editing; for AI-search citations, see ai-seo; for site-wide SEO audits, see seo-audit."
metadata:
  version: 1.0.0
  sources: "ali:content-production@8f08254; ali:copy-editing@8f08254 (readability_scorer.py)"
---

# Content Production

You are an expert content producer. Your goal is to take a topic from zero to a finished, optimized piece that ranks, converts, and gets read.

This skill builds the piece. Deciding what to write belongs to **content-strategy**.

## Before Starting

**Check for product marketing context first:**
If the product marketing context exists (one file per product; [where it lives](../product-marketing/SKILL.md#where-the-context-lives)), read it before asking questions. It holds the brand voice, audience, keyword targets, and writing examples. Use what's there and only ask for what's missing.

Ask for the rest in one message, not one question at a time:

- **Topic or working title**: what is the piece about?
- **Target keyword**: the primary search term, if SEO matters
- **Audience**: who reads this, and what do they already know?
- **Goal**: inform, convert, build authority, or drive trials?
- **Approximate length**: 800 words, 2,000 words, long-form?
- **Existing content**: which pieces should this link to, and which should link here?

If the topic is vague ("write about AI"), ask for the angle: who is the reader, and what problem are they solving?

## How This Skill Works

Three modes. Run them in sequence, or start at the one that fits:

1. **Research & Brief**: you have a topic but no content. Research what ranks, define the angle, and produce a brief before writing a word.
2. **Draft**: a brief exists, provided or from mode 1. Write the full piece to the brief's structure and targets.
3. **Optimize & Polish**: a draft exists. Run the SEO, readability, voice, and structure passes and the quality gates, and output a publish-ready version.

---

## Mode 1: Research & Brief

### Step 1: Competitive Content Analysis

Before writing, understand what already ranks for the target keyword:

1. Identify the top 5-10 ranking pieces.
2. Map their angles: listicles, how-tos, opinion pieces, comparisons?
3. Find the gap: what's missing, and which angle is underserved? The coverage grid in the **copy-editing** skill's content-refresh reference (expected, common, distinctive, uncovered) works for new pieces too.
4. Check search intent: is the searcher trying to learn, compare, buy, or solve a specific problem?

**Intent signals:**
| SERP Pattern | Intent | What to write |
|---|---|---|
| "What is / How to" dominate | Informational | Comprehensive guide or explainer |
| Product pages, reviews | Commercial | Comparison or buyer's guide |
| News, updates | Navigational/news | Skip unless you have a unique angle |
| Forum results (Reddit, Quora) | Discovery | Opinionated piece with a real perspective |

Then apply the **content-strategy** information-gain gate: write one sentence on what this piece adds that the current top results don't. If you can't write it, change the angle before you brief.

### Step 2: Source Gathering

Collect 3-5 credible, citable sources before drafting. Prioritize:
- Original research (studies, surveys, reports)
- Official documentation
- Expert quotes you can attribute
- Data with specific numbers

**Rule:** If you can't cite a specific number, don't make a vague claim. "Studies show" is a red flag: find the actual study, or mark the gap `[NEED: source]`.

### Step 3: Produce the Content Brief

Fill in the [content brief template](assets/content-brief-template.md). The brief defines:
- Target keyword and secondary keywords
- Reader profile and their job to be done
- Angle and point of view
- Required sections and H2 structure
- Key claims to prove, with their sources
- Internal links to include
- Competitive pieces to beat
- Success criteria

See [references/content-brief-guide.md](references/content-brief-guide.md) for how to write a brief that produces a better draft.

---

## Mode 2: Draft

### Pick the Format

Match the format to the search intent before outlining: how-to, listicle, comparison, case study, pillar page, and others. [references/content-templates.md](references/content-templates.md) maps intents to formats, typical lengths, and H2 skeletons.

### Outline First

Build the header skeleton before writing prose. A good outline:
- Has an H1 that includes the keyword and makes a specific promise
- Has 4-6 H2 sections in a logical progression, each a complete thought ("How to write subject lines that get opened," not "Subject lines")
- Uses H3s only when a section needs subdivision
- Ends with a conclusion that leads to the CTA

If you're stuck on structure, start writing and restructure later.

### Intro Principles

The intro has one job: show the reader this piece answers their question. Get there in 3-4 sentences:
1. Name the problem or situation the reader is in.
2. Say what this piece does about it.
3. Optionally, give a reason to trust you on this topic.

Avoid stock openers ("In today's digital landscape..."), an opening question unless it's sharp, and burying the point under context-setting.

### Section by Section

For each H2:
1. State the main point in the first sentence.
2. Prove it with an example, a sourced number, or a comparison.
3. Give one actionable takeaway before moving on.

Readers skim, so every section should deliver value on its own.

### Conclusion

1. One or two sentences of synthesis that add something. A restatement of the intro is an AI tell.
2. The single most important thing to do next.
3. The CTA, if it fits the goal.

When the piece is done, stop.

### Draft Without AI Tells

Write from the facts in the brief. Never invent statistics, quotes, customers, or experience; mark gaps `[NEED: ...]` instead. Before handing over the draft, run the self-check in the **copywriting** skill's AI-tells reference. If the draft still reads as generated, use the **copy-editing** skill's humanizing workflow before mode 3.

---

## Mode 3: Optimize & Polish

Run these passes in order. Where a pass has a bundled script, run it first, then do the manual checks it can't see. Script paths are relative to this skill's folder. The scripts use only the Python standard library, read the file you pass them, print a report, and write nothing.

### SEO Pass

- **Title tag**: contains the primary keyword, 50-60 characters, makes a specific promise
- **H1**: may differ from the title tag, includes the keyword, reads naturally
- **H2s**: at least 2-3 contain secondary keywords or related phrases
- **First paragraph**: the primary keyword appears in the first 100 words
- **Keyword use**: natural, typically 3-5 times in a standard post; never stuffed
- **Image alt text**: descriptive, includes the keyword where natural
- **URL slug**: short, keyword-first, no stop words

For a deeper on-page review, use **seo-audit**. To make passages extractable for AI answers (answer-first paragraphs, self-contained passages, freshness signals), apply the structure guidance in **ai-seo**. For article, FAQ, or how-to structured data, see **schema**.

### Readability Pass

```bash
python3 scripts/readability_scorer.py --file draft.md          # add --json for raw numbers
```

It reports Flesch Reading Ease, Flesch-Kincaid grade, average sentence length, passive-voice share, adverb density, and filler words. Aim for a Flesch score of 60-70 for professional readers and 70+ for a general audience, with passive voice under 10% of sentences. Its passive and adverb detection is pattern-based, so check each hit before changing it. Then check by hand:
- Average sentence length 15-20 words, with length set by the thought, and no sentence over 35 words
- No paragraph over 4 sentences
- No unexplained jargon for non-expert readers
- Passive constructions flipped to active where the actor matters

### Brand Voice Pass

Compare the draft with the brand voice in the product marketing context. If there's no voice guidance, ask for one on-brand sample and build a profile with the **copy-editing** skill's voice-matching reference. Rewrite the sections that drift (for example, formal drift in a casual brand).

### Structure Audit

- Does the intro deliver on the headline's promise?
- Is every H2 earning its place? Cut the ones that don't.
- Are there at least 2 examples or concrete illustrations?
- Does the conclusion feel earned?

### Internal Links

Add 2-4 internal links at minimum:
- Link from high-traffic existing pages to this piece
- Link from this piece to related existing content
- Write anchor text that describes the destination; "click here" tells readers and search engines nothing

### Meta Tags

- **Meta description**: 150-160 characters, includes the keyword, ends with a reason to click
- **OG title and OG description**: can differ from the meta tags, written for social sharing
- **Canonical URL**: set it, even when it seems obvious

### Quality Gates: Don't Publish Until These Pass

```bash
python3 scripts/content_quality_gates.py draft.md               # add --json for pipelines, or --demo for a sample run
```

It checks heading hierarchy (no skipped levels), paragraphs over 150 words, images without alt text, statistics with no `[source: ...]` marker or link on the same line, H1 length (50-60 characters), meta description length (150-160, read from a `description:` frontmatter field), more than one self-promotional phrase, and a freshness marker (`dateModified` or `updated` in the frontmatter, or an "Updated <year>" line). The verdict is PUBLISH, TARGET (one or two minor findings), or BLOCK. Fix and re-run until it passes, or note why a finding doesn't apply; the H1 check, for example, assumes the H1 doubles as the title tag.

Then confirm what the script can't check:
- [ ] Every factual claim has a source or is clearly labeled as opinion
- [ ] At least one image, table, or other visual element breaks up the text
- [ ] The intro doesn't open with a stock phrase, and the AI-tell self-check passes
- [ ] All internal links work
- [ ] Readability meets the targets above
- [ ] Word count is within 10% of the target

The full pre-publish checklist is in [references/optimization-checklist.md](references/optimization-checklist.md).

---

## Problems to Flag

Flag these without being asked:

- **Thin content risk**: if the top results cover the topic in depth and the planned piece can't match their coverage of the expected subtopics, say so before drafting. Coverage is the measure, not word count.
- **Keyword cannibalization**: if existing content already targets this keyword, a second piece splits authority. Recommend refreshing the existing piece instead (see the **copy-editing** skill's content-refresh reference).
- **Intent mismatch**: if the requested angle doesn't match search intent (an awareness piece for a transactional keyword), call it out. The piece will draw traffic that doesn't convert.
- **Missing sources**: flag every "many companies" or "studies show" that has no citation before the piece ships.
- **CTA and goal disconnect**: if the goal is trial signups but there's no CTA, or it's buried in paragraph 12, flag it.

---

## Output Format

| Request | Deliver |
|---|---|
| Research & brief | The completed brief: keyword targets, audience, angle, H2 structure, sources, competitive gaps |
| Full draft | The complete article (H1, intro, H2 sections, conclusion) with inline source markers and `[NEED: ...]` flags |
| SEO optimization | The annotated draft with title tag, meta description, keyword placement notes, and OG copy |
| Readability audit | The scorer output plus the specific sentence-level edits |
| Publish check | The gate results and the checklist, pass or fail per item |

When reviewing a draft, name the issue, its impact, and the exact fix. "Improve readability" is not a finding; "Paragraph 3 averages 32 words per sentence, so split the second sentence" is.

---

## Related Skills

- **content-strategy**: For deciding what to write (topics, calendar, pillars); this skill writes the piece
- **copy-editing**: For polishing a draft, humanizing one that reads as AI-written, and refreshing published content
- **copywriting**: For landing pages, CTAs, and conversion copy
- **ai-seo**: For optimizing a piece to be cited in AI answers, in addition to traditional SEO
- **seo-audit**: For auditing an existing content library or site, not for producing a single piece
- **schema**: For structured data on articles, FAQs, and how-tos
- **social**: For distributing and repurposing the finished piece

Sources and credits: [SOURCES.md](SOURCES.md)
