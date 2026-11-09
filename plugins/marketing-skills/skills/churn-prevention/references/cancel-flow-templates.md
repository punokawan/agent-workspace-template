# Cancel Flow Templates

Copy templates for each stage of the cancel flow, post-cancel emails, and a rubric to audit an existing flow. Offer patterns by business type, billing interval and segment are in [cancel-flow-patterns.md](cancel-flow-patterns.md).

---

## Decision Tree

```
Customer clicks "Cancel subscription"
         │
         ▼
   [Exit survey: one required question]
         │
         ▼
   Map reason → one primary offer
   (or skip the offer: business closed, wrong fit,
    feature that does not exist and is not planned,
    competitor decision already made)
         │
   [Accept?] ──Yes──► Apply offer, confirm by email
         │
         No
         │
         ▼
   [Confirm cancellation]
         │
         ▼
   [Post-cancel page + confirmation email]
```

---

## Stage 1: Pre-Cancel Intercept

**When:** the user clicks "Cancel plan" or opens the cancel page.

**Show:** a short "tell us why" framing, not a wall of guilt.

```
Headline: Before you go, we want to understand
Body: Your feedback helps us improve. Take 30 seconds to tell us why
      you're cancelling — we might have a solution you haven't tried.
CTA: Continue to cancellation →
```

**Rules:**
- Never block the cancel path
- Show it at most once per session
- Mobile: one screen, no scrolling

---

## Stage 2: Exit Survey

**Spec:** one required question, radio buttons, 5-8 options, optional free text at the end. Submitting moves to Stage 3; the offer comes after the answer.

```
What's the main reason you're cancelling?

○ It's too expensive for what I get
○ I'm not using it enough to justify the cost
○ It's missing a feature I need
○ I'm switching to a different tool
○ My project or need ended
○ It's too complicated or hard to use
○ I was just testing it out
○ Other: [text field]

[Continue →]
```

Store the reason on the customer record. It is product feedback as well as the offer key.

---

## Stage 3: Save Offer

**Price objection:**
```
Headline: Keep [Product] for less
Body: We'd hate to see you go over price. Here's what we can do:
      [discount]% off your next [n] months — that's [amount] saved.
      After [n] months, your plan returns to [original price].
CTA (accept): Claim my discount →
CTA (decline): No thanks, continue cancelling →
```

**Not using it enough:**
```
Headline: Pause your account — no charge for [n] days
Body: Life gets busy. Put [Product] on hold for up to [n] days.
      Your data stays intact, and you can resume any time.
CTA (accept): Pause my account →
CTA (decline): No thanks, continue cancelling →
```

Track which offer was shown and whether it was accepted.

---

## Stage 4: Confirmation

Include the exact access end date (a date, not "end of billing period"), the data retention period, a support contact and a reactivation path.

```
Your subscription will be cancelled.

Here's what happens next:
• Access continues until [date]
• Your data is kept for [retention period] after cancellation
• After that, your account data is deleted
• You can reactivate any time before [retention end date]

If you change your mind, contact [email] or reactivate at [reactivation URL].

[Confirm cancellation]    [Go back]
```

---

## Stage 5: Post-Cancel Emails

**Immediately — confirmation:**
```
Subject: Your [Product] subscription has been cancelled

Hi [Name],

Your [Product] subscription has been cancelled as requested.

What happens next:
- Access continues until [date]
- Your data is saved until [retention end date]
- To reactivate, visit: [reactivation link]

If this was a mistake or you have questions, reply to this email or visit [support link].

[Product] Team
```

**Day 7 — door open:**
```
Subject: Your [Product] account is still here

Hi [Name],

It's been a week since you cancelled. Your account and data are still intact
until [date].

If anything changed, you can reactivate in one click — no re-setup required.

[Reactivate my account →]

No pressure — just making sure you knew the door's open.

[Product] Team
```

**Day 30 — win-back, only when there is news that answers their cancel reason:**
```
Subject: [Product] update: [feature or fix related to their reason]

Hi [Name],

Since you left, we shipped [update relevant to their cancel reason].
[Two or three sentences on what changed.]

If [their problem] was why you left, it might be worth another look.

[See what's new →]    or    [Reactivate →]

[Product] Team
```

The full post-cancel timing (survey, what's new, final offer) is in [cancel-flow-patterns.md](cancel-flow-patterns.md) § Post-Cancel Sequence; longer win-back sequences belong to the emails skill.

---

## Audit Rubric

Score each dimension 0, 1 or 2. Fix every 0 first, then the 1s with the most revenue behind them.

| Dimension | 0 | 1 | 2 |
|-----------|---|---|---|
| **Access** | Cancel needs a support ticket or call | In settings, but buried | Clearly visible in billing settings |
| **Exit survey** | None | Optional or several questions | One required question that maps to offers |
| **Save offers** | None, or one generic discount | Offers exist but are not mapped to reasons | One primary offer per reason |
| **Confirmation** | Unclear terms | Mentions access end | Exact date, data policy, reactivation path |
| **Post-cancel** | Nothing | One generic email | Confirmation now, re-engagement at day 7, win-back on news |
| **Dunning** | None | Retries only | Retries by decline type, email sequence, card updater |
| **Measurement** | No tracking | Cancellation count only | Reason, offer shown and accepted, save rate, recovery rate |

Report the scores per dimension rather than one total; the dimensions do not carry equal revenue.
