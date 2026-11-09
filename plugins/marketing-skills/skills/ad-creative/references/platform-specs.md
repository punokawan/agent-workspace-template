# Platform Specs Reference

Complete character limits, format requirements, and best practices for each ad platform.

---

## Google Ads

### Responsive Search Ads (RSAs)

| Element | Character Limit | Required | Notes |
|---------|----------------|----------|-------|
| Headline | 30 chars | 3 minimum, 15 max | Any 3 may be shown together |
| Description | 90 chars | 2 minimum, 4 max | Any 2 may be shown together |
| Display path 1 | 15 chars | Optional | Appears after domain in URL |
| Display path 2 | 15 chars | Optional | Appears after path 1 |
| Final URL | No limit | Required | Landing page URL |

**Combination rules:**
- Google selects up to 3 headlines and 2 descriptions to show
- Headlines appear separated by " | " or stacked
- Any headline can appear in any position unless pinned
- Pinning reduces Google's ability to optimize — use sparingly

**Pinning strategy:**
- Pin your brand name to position 1 if brand guidelines require it
- Pin your strongest CTA to position 2 or 3
- Leave most headlines unpinned for machine learning

**Ad Strength** (Poor, Average, Good, Excellent) rates how complete the asset set is. Aim for Good or better: fill all 15 headline slots with unique lines, put the main keyword in at least 3 headlines, and write descriptions that add to the headlines instead of repeating them.

**Headline mix recommendation (15 headlines):**
- 3-4 keyword-focused (match search intent)
- 3-4 benefit-focused (what they get)
- 2-3 social proof (numbers, awards, customers)
- 2-3 CTA-focused (action to take)
- 1-2 differentiators (why you over competitors)
- 1 brand name headline

**Description mix recommendation (4 descriptions):**
- 1 benefit + proof point
- 1 feature + outcome
- 1 social proof + CTA
- 1 urgency/offer + CTA (if applicable)

### Performance Max

| Element | Character Limit | Notes |
|---------|----------------|-------|
| Headline | 30 chars (5 required) | Short headlines for various placements |
| Long headline | 90 chars (5 required) | Used in display, video, discover |
| Description | 90 chars (1 required, 5 max) | Accompany various ad formats |
| Short description | 60 chars | One of the descriptions must fit 60 chars |
| Business name | 25 chars | Required |

### Display Ads

| Element | Character Limit |
|---------|----------------|
| Headline | 30 chars |
| Long headline | 90 chars |
| Description | 90 chars |
| Business name | 25 chars |

---

## Meta Ads (Facebook & Instagram)

### Single Image / Video / Carousel

| Element | Recommended | Maximum | Notes |
|---------|-------------|---------|-------|
| Primary text | 125 chars | 2,200 chars | Text above image; truncated after ~125 |
| Headline | 40 chars | 255 chars | Below image; truncated after ~40 |
| Description | 30 chars | 255 chars | Below headline; may not show |
| URL display link | 40 chars | N/A | Optional custom display URL |

**Placement-specific notes:**
- **Feed**: All elements show; primary text most visible
- **Stories/Reels**: Primary text overlaid; keep under 72 chars
- **Right column**: Only headline visible; skip description
- **Audience Network**: Varies by publisher

**Best practices:**
- Front-load the hook in primary text (first 125 chars)
- Use line breaks for readability in longer primary text
- Emojis: test, but don't overuse — 1-2 per ad max
- Questions in primary text increase engagement
- Headline should be a clear CTA or value statement

### Lead Ads (Instant Form)

| Element | Limit |
|---------|-------|
| Greeting headline | 60 chars |
| Greeting description | 360 chars |
| Privacy policy text | 200 chars |

---

## LinkedIn Ads

### Single Image Ad

| Element | Recommended | Maximum | Notes |
|---------|-------------|---------|-------|
| Intro text | 150 chars | 600 chars | Above the image; truncated after ~150 |
| Headline | 70 chars | 200 chars | Below the image |
| Description | 100 chars | 300 chars | Only shows on Audience Network |

### Carousel Ad

| Element | Limit |
|---------|-------|
| Intro text | 255 chars |
| Card headline | 45 chars |
| Card count | 2-10 cards |

### Message Ad (InMail)

| Element | Limit |
|---------|-------|
| Subject line | 60 chars |
| Message body | 1,500 chars |
| CTA button | 20 chars |

### Conversation Ad

| Element | Limit |
|---------|-------|
| CTA button | 25 chars, up to 5 per message |
| Message | Keep each message short; the **ads** skill's LinkedIn playbook covers length and flow |

### Text Ad

| Element | Limit |
|---------|-------|
| Headline | 25 chars |
| Description | 75 chars |

**LinkedIn-specific guidelines:**
- Professional tone, but not boring
- Use job-specific language the audience recognizes
- Statistics and data points perform well
- Avoid consumer-style hype ("Amazing!" "Incredible!")
- First-person testimonials from peers resonate

---

## TikTok Ads

### In-Feed Ads

| Element | Recommended | Maximum | Notes |
|---------|-------------|---------|-------|
| Ad text | 80 chars | 100 chars | Above the video |
| Display name | N/A | 40 chars | Brand name |
| CTA button | Platform options | Predefined | Select from TikTok's options |

### Spark Ads (Boosted Organic)

| Element | Notes |
|---------|-------|
| Caption | Uses original post caption |
| CTA button | Added by advertiser |
| Display name | Original creator's handle |

**TikTok-specific guidelines:**
- Native content outperforms polished ads
- First 2 seconds determine if they watch
- Use trending sounds and formats
- Text overlay is essential (most watch with sound off)
- Vertical video only (9:16)

---

## Twitter/X Ads

### Promoted Tweets

| Element | Limit | Notes |
|---------|-------|-------|
| Tweet text | 280 chars | Full tweet with image/video; each link counts as 23 chars |
| Card headline | 70 chars | Website card |
| Card description | 200 chars | Website card |

### Website Cards

| Element | Limit |
|---------|-------|
| Headline | 70 chars |
| Description | 200 chars |

**Twitter/X-specific guidelines:**
- Conversational, casual tone
- Short sentences work best
- One clear message per tweet
- Hashtags: 1-2 max (0 is often better for ads)
- Threads can work for consideration-stage content

---

## Policy and Rejection Triggers

Limits get an ad truncated; policy gets it disapproved. Check every batch against these before upload. `scripts/ad_copy_validator.py` flags most of them for review; the platform's own policy pages are the final word.

### All platforms

| Trigger | Why it gets flagged | Fix |
|---------|--------------------|-----|
| ALL CAPS words | Reads as shouting; editorial policies | Sentence or title case; keep real acronyms |
| Repeated punctuation (`!!!`, `???`, `...`) | Gimmicky punctuation | One mark at most |
| "#1," "best," other superlatives | Need third-party substantiation | Remove, or cite the verified source on the landing page |
| "Guaranteed" results | Outcome and financial guarantees are restricted | Show evidence of results instead |
| Trademarks: platform names, competitors | Trademark and platform-brand policies | Remove, or get permission; never imply the platform endorses you |
| "Click here" | Low-quality call to action | Name the action and what they get |
| Personal attributes ("Are you depressed?", "Single in [city]?") | Personal-attribute and sensitive-targeting policies | Describe the product, never the reader's traits |
| Discounts without context ("90% off") | Misleading-claims policies | Show the reference price and the terms |
| Health, weight-loss, income, or investment-return claims | Restricted categories | Substantiate, or remove; check the category rules |
| Profanity | Obvious | Remove |

### Platform notes

- **Google Ads:** no exclamation marks in headlines; no gimmicky symbols or repeated punctuation; capitals only for acronyms and trademarks.
- **Meta:** no wording that implies Meta endorses the ad; before/after imagery is restricted for health and beauty; exaggerated health claims and click-bait phrasing ("You won't believe...") get rejected. The old 20% image-text rule no longer limits delivery, but text-light images still tend to perform better.
- **LinkedIn:** no standalone "Click here"; no misleading job or recruitment bait. Generic corporate language is not a policy breach, but it underperforms in a feed full of it.

---

## Character Counting Tips

- **Spaces count** as characters on all platforms
- **Emojis** count as 1-2 characters depending on platform
- **Special characters** (|, &, etc.) count as 1 character
- **URLs** in body text count against limits
- **Dynamic keyword insertion** (`{KeyWord:default}`) can exceed limits — set safe defaults
- Always verify in the platform's ad preview before launching

---

## Multi-Platform Creative Adaptation

When creating for multiple platforms simultaneously, start with the most restrictive format:

1. **Google Search headlines** (30 chars) — forces the tightest messaging
2. **Expand to Meta headlines** (40 chars) — add a word or two
3. **Expand to LinkedIn intro text** (150 chars) — add context and proof
4. **Expand to Meta primary text** (125+ chars) — full hook and value prop

This cascading approach ensures your core message works everywhere, then gets enriched for platforms that allow more space.
