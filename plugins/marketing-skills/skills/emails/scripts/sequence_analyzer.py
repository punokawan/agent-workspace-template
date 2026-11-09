#!/usr/bin/env python3
"""
sequence_analyzer.py: score a lifecycle email sequence (welcome, nurture,
onboarding, re-engagement) 0-100 before it ships.

Per email: subject length (40-60 characters), preview text (90-140
characters, not a repeat of the subject), body length for the email's type,
a call to action, merge fields, pushy or spam-associated phrases, and AI
tells (fake "Re:"/"Fwd:" subjects, em dashes in subject or preview, stock
phrases, "it's not X, it's Y" reveals).
Across the sequence: pacing between sends.

Usage:
  python3 sequence_analyzer.py --file sequence.json
  python3 sequence_analyzer.py --file sequence.json --json
  python3 sequence_analyzer.py                       # demo sequence

Input: a JSON array, one object per email, in send order:
  [
    {"subject": "...", "preview": "...", "body": "...",
     "delay_days": 0, "type": "educational"},
    ...
  ]
  delay_days  day the email sends, counted from sequence entry (0 = immediately)
  type        transactional | educational | story (default: educational)
  preview     optional preview text

Heuristic only: the copy rules in the emails skill win where they disagree.
Stdlib only. Reads the input file; writes nothing.
"""

import argparse
import json
import re
import sys


# ---------------------------------------------------------------------------
# Rules
# ---------------------------------------------------------------------------

SUBJECT_RANGE = (40, 60)
PREVIEW_RANGE = (90, 140)

# Word counts by email type.
LENGTH_RANGES = {
    "transactional": (50, 125),
    "educational": (150, 300),
    "story": (300, 500),
}

# Pushy or spam-associated phrases. Matched as whole words or phrases.
SPAM_PHRASES = [
    "guarantee", "guaranteed", "winner", "prize", "congratulations",
    "earn money", "make money", "extra income", "cash bonus",
    "100% free", "no cost", "risk free", "risk-free", "act now", "limited time",
    "click here", "buy now", "order now", "get it now",
    "as seen on", "dear friend", "you have been selected",
    "this isn't spam", "not spam",
    "special promotion", "amazing offer",
    "increase sales", "double your",
    "lose weight", "weight loss", "viagra", "casino",
]
SPAM_SYMBOLS = ["!!!", "$$$"]

STOCK_PHRASES = [
    "i hope this email finds you well", "just checking in", "great news!",
    "feel free to reach out", "don't hesitate to reach out",
    "say goodbye to", "unlock the power of", "take it to the next level",
    "here's the thing", "reimagined",
]

CONTRAST_REVEAL = re.compile(
    r"\b(?:it'?s|this is|that'?s)\s+not\s+[^.!?\n]{1,60}?[,;:.]\s*(?:it'?s|this is|that'?s)\b",
    re.IGNORECASE,
)

FAKE_REPLY = re.compile(r"^\s*(?:re|fwd?)\s*:", re.IGNORECASE)

CTA_PATTERNS = re.compile(
    r"\b(click|tap|reply|download|sign up|register|buy|purchase|get started|"
    r"learn more|read more|visit|go to|check out|schedule|book|claim|try|"
    r"subscribe|join|start|access|watch|see|grab|discover)\b",
    re.IGNORECASE,
)

PERSONALIZATION_TOKENS = re.compile(
    r"\{\{?\s*\w+\s*\}?\}|%\w+%|\[FIRST_NAME\]|\[NAME\]|\[COMPANY\]|\[FIRSTNAME\]",
    re.IGNORECASE,
)


def _phrase_pattern(phrase: str) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.IGNORECASE)


SPAM_PATTERNS = [(p, _phrase_pattern(p)) for p in SPAM_PHRASES]
STOCK_PATTERNS = [(p, _phrase_pattern(p)) for p in STOCK_PHRASES]


# ---------------------------------------------------------------------------
# Per-email analysis
# ---------------------------------------------------------------------------

def _in_range(value: int, bounds: tuple) -> bool:
    return bounds[0] <= value <= bounds[1]


def _length_verdict(word_count: int, email_type: str) -> str:
    low, high = LENGTH_RANGES[email_type]
    if word_count < low:
        return f"short for {email_type} ({low}-{high} words)"
    if word_count > high:
        return f"long for {email_type} ({low}-{high} words)"
    return "in range"


def analyze_email(email: dict, index: int) -> dict:
    subject = email.get("subject", "") or ""
    preview = email.get("preview", "") or ""
    body = email.get("body", "") or ""
    delay = email.get("delay_days", 0)
    email_type = str(email.get("type", "educational")).lower()
    if email_type not in LENGTH_RANGES:
        email_type = "educational"

    # Subject and preview
    subject_len = len(subject)
    subject_ok = _in_range(subject_len, SUBJECT_RANGE)
    preview_notes = []
    if preview:
        if not _in_range(len(preview), PREVIEW_RANGE):
            preview_notes.append(
                f"preview is {len(preview)} chars (aim for {PREVIEW_RANGE[0]}-{PREVIEW_RANGE[1]})")
        if subject and subject.strip().lower() in preview.lower():
            preview_notes.append("preview repeats the subject line")
    preview_ok = not preview_notes

    # Body
    body_word_count = len(re.findall(r"\b\w+\b", body))
    length_verdict = _length_verdict(body_word_count, email_type)
    cta_matches = CTA_PATTERNS.findall(body)
    tokens = PERSONALIZATION_TOKENS.findall(subject) + PERSONALIZATION_TOKENS.findall(body)

    # Spam-associated phrases
    combined = " ".join([subject, preview, body])
    spam_found = [p for p, pat in SPAM_PATTERNS if pat.search(combined)]
    spam_found += [s for s in SPAM_SYMBOLS if s in combined]
    spam_score = min(100, len(spam_found) * 10)

    # AI tells
    tells = []
    if FAKE_REPLY.search(subject):
        tells.append('fake "Re:"/"Fwd:" subject')
    if "—" in subject or "—" in preview:
        tells.append("em dash in subject or preview")
    tells += [f'stock phrase: "{p}"' for p, pat in STOCK_PATTERNS if pat.search(combined)]
    if CONTRAST_REVEAL.search(body):
        tells.append("\"it's not X, it's Y\" reveal")

    return {
        "email_index": index + 1,
        "delay_days": delay,
        "type": email_type,
        "subject": {
            "text": subject,
            "length": subject_len,
            "length_ok": subject_ok,
            "personalized": bool(PERSONALIZATION_TOKENS.findall(subject)),
        },
        "preview": {
            "text": preview,
            "provided": bool(preview),
            "ok": preview_ok,
            "notes": preview_notes,
        },
        "body": {
            "word_count": body_word_count,
            "length_verdict": length_verdict,
            "has_cta": bool(cta_matches),
            "cta_phrases": sorted(set(m.lower() for m in cta_matches))[:5],
            "personalization_tokens": len(tokens),
        },
        "spam": {
            "phrases_found": spam_found[:8],
            "count": len(spam_found),
            "risk_score": spam_score,
            "risk_level": "High" if spam_score >= 40 else "Medium" if spam_score >= 20 else "Low",
        },
        "ai_tells": tells,
    }


# ---------------------------------------------------------------------------
# Sequence-level analysis
# ---------------------------------------------------------------------------

def analyze_pacing(emails: list) -> dict:
    if len(emails) <= 1:
        return {"email_count": len(emails), "note": "Single email, no pacing to analyze", "issues": []}

    delays = [e.get("delay_days", 0) for e in emails]
    gaps = [delays[i] - delays[i - 1] for i in range(1, len(delays))]

    issues = []
    for i, gap in enumerate(gaps):
        email_no = i + 2
        if gap <= 0:
            issues.append(f"Email {email_no}: same day as the previous email or earlier; check delay_days")
        elif gap == 1 and email_no > 3:
            issues.append(f"Email {email_no}: 1-day gap after the early emails; nurture usually runs 2-4 days apart")
        elif gap > 14:
            issues.append(f"Email {email_no}: {gap}-day gap; momentum may drop")

    avg_gap = sum(gaps) / len(gaps)
    if avg_gap <= 2:
        cadence = "Aggressive (avg 2 days or less)"
    elif avg_gap <= 5:
        cadence = "High-frequency (avg 2-5 days)"
    elif avg_gap <= 10:
        cadence = "Standard (avg 5-10 days)"
    else:
        cadence = "Low-frequency (avg 10+ days)"

    return {
        "email_count": len(emails),
        "total_duration_days": max(delays) - min(delays),
        "avg_gap_days": round(avg_gap, 1),
        "cadence_type": cadence,
        "gaps": gaps,
        "issues": issues,
    }


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

WEIGHTS = {
    "subject_and_preview": 0.20,
    "cta_presence": 0.20,
    "spam_safety": 0.15,
    "no_ai_tells": 0.15,
    "personalization": 0.10,
    "pacing": 0.10,
    "body_length": 0.10,
}


def compute_sequence_score(analyses: list, pacing: dict) -> dict:
    if not analyses:
        return {"overall": 0, "grade": "F", "breakdown": {}}

    n = len(analyses)

    def share(pred) -> int:
        return round(sum(1 for a in analyses if pred(a)) / n * 100)

    avg_spam = sum(a["spam"]["risk_score"] for a in analyses) / n
    scores = {
        "subject_and_preview": share(lambda a: a["subject"]["length_ok"] and a["preview"]["ok"]),
        "cta_presence": share(lambda a: a["body"]["has_cta"]),
        "spam_safety": max(0, 100 - round(avg_spam)),
        "no_ai_tells": share(lambda a: not a["ai_tells"]),
        "personalization": share(lambda a: a["body"]["personalization_tokens"] > 0),
        "pacing": max(0, 100 - len(pacing.get("issues", [])) * 20),
        "body_length": share(lambda a: a["body"]["length_verdict"] == "in range"),
    }
    overall = round(sum(scores[k] * WEIGHTS[k] for k in WEIGHTS))
    grade = "A" if overall >= 85 else "B" if overall >= 70 else "C" if overall >= 55 else "D" if overall >= 40 else "F"

    return {
        "overall": overall,
        "grade": grade,
        "breakdown": {k: {"score": v, "weight": f"{round(WEIGHTS[k] * 100)}%"} for k, v in scores.items()},
    }


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------

DEMO_SEQUENCE = [
    {
        "subject": "{{first_name}}, your free marketing audit is ready",
        "preview": "Three quick wins we found in campaigns like yours, and where to start this week.",
        "body": "Hi {{first_name}},\n\nWe analyzed 500 campaigns like yours and found three quick wins that could double your ROAS in 30 days.\n\nI've put together a custom audit for {{company}}. It takes 10 minutes to review.\n\nClick here to see your results: [LINK]\n\nBest,\nSarah",
        "delay_days": 0,
        "type": "transactional",
    },
    {
        "subject": "Did you see this, {{first_name}}?",
        "body": "Quick follow-up.\n\nMost marketers we talk to are sitting on 2-3 easy optimizations that could add 20-40% more revenue from the same ad spend.\n\nHere's the #1 thing we see: landing pages that don't match the ad promise.\n\nWorth 5 minutes? Review your audit: [LINK]\n\nSarah",
        "delay_days": 3,
        "type": "transactional",
    },
    {
        "subject": "The $50,000 mistake (and how to avoid it)",
        "body": "True story.\n\nOne of our clients was spending $8,500/month on search ads with a 1.8x ROAS. Above break-even, but barely.\n\nWe found that 60% of their budget was going to one keyword that had zero purchase intent.\n\nAfter fixing it: same spend, 4.2x ROAS.\n\nThat's the kind of thing our audit catches. Have you looked at yours yet?\n\nOpen your audit: [LINK]\n\nSarah\n\nP.S. This offer expires Friday.",
        "delay_days": 5,
        "type": "story",
    },
    {
        "subject": "Last call: your audit expires tonight",
        "body": "{{first_name}}, this is the last reminder.\n\nYour personalized audit expires at midnight tonight.\n\nIf growing your ROAS is a priority this quarter, take 10 minutes now.\n\nClaim your audit before it expires: [LINK]\n\nSarah",
        "delay_days": 7,
        "type": "transactional",
    },
    {
        "subject": "New case study: a {{company}}-style win",
        "body": "Since you didn't grab the audit, I wanted to send you something useful anyway.\n\nHere's a 3-minute case study showing how we helped a B2B SaaS company go from 1.9x to 5.4x ROAS in 45 days.\n\nNo audit required, just tactics you can use.\n\nRead the case study: [LINK]\n\nHope it helps,\nSarah",
        "delay_days": 14,
        "type": "transactional",
    },
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _load(path: str) -> list:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except OSError as exc:
        sys.exit(f"Error: cannot read {path}: {exc}")
    except json.JSONDecodeError as exc:
        sys.exit(f"Error: invalid JSON in {path}: {exc}")
    if not isinstance(data, list):
        sys.exit("Error: input must be a JSON array of email objects")
    return data


def main():
    parser = argparse.ArgumentParser(
        description="Score a lifecycle email sequence 0-100: subject and preview, CTA, "
                    "spam-associated phrases, AI tells, merge fields, pacing, body length.",
        epilog="Input: JSON array of {subject, preview?, body, delay_days, type?}. "
               "Without --file, runs on a demo sequence.",
    )
    parser.add_argument("--file", help="JSON file with the email sequence array")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    if args.file:
        emails = _load(args.file)
    else:
        emails = DEMO_SEQUENCE
        if not args.json:
            print("No input provided: running on a demo 5-email nurture sequence.\n")

    analyses = [analyze_email(e, i) for i, e in enumerate(emails)]
    pacing = analyze_pacing(emails)
    scoring = compute_sequence_score(analyses, pacing)

    if args.json:
        print(json.dumps({"sequence_score": scoring, "pacing": pacing, "emails": analyses}, indent=2))
        return

    print("=" * 66)
    print(f"  EMAIL SEQUENCE ANALYSIS   Score: {scoring['overall']}/100  Grade: {scoring['grade']}")
    print("=" * 66)

    print("\n  PACING")
    print(f"     Emails:    {pacing['email_count']}")
    if "cadence_type" in pacing:
        print(f"     Duration:  {pacing['total_duration_days']} days")
        print(f"     Avg gap:   {pacing['avg_gap_days']} days")
        print(f"     Cadence:   {pacing['cadence_type']}")
    for issue in pacing.get("issues", []):
        print(f"     ! {issue}")

    print("\n  PER EMAIL")
    print(f"  {'#':<3} {'Subject':<42} {'Words':<6} {'CTA':<4} {'Tokens':<7} {'Spam'}")
    print("  " + "-" * 64)
    for a in analyses:
        subj = a["subject"]["text"][:38] + ("" if a["subject"]["length_ok"] else " (!)")
        cta = "yes" if a["body"]["has_cta"] else "no"
        print(f"  {a['email_index']:<3} {subj:<42} {a['body']['word_count']:<6} {cta:<4} "
              f"{a['body']['personalization_tokens']:<7} {a['spam']['risk_level']}")

    notes = []
    for a in analyses:
        i = a["email_index"]
        if not a["subject"]["length_ok"]:
            notes.append(f"Email {i}: subject is {a['subject']['length']} chars (aim for {SUBJECT_RANGE[0]}-{SUBJECT_RANGE[1]})")
        for n in a["preview"]["notes"]:
            notes.append(f"Email {i}: {n}")
        if a["body"]["length_verdict"] != "in range":
            notes.append(f"Email {i}: body {a['body']['word_count']} words, {a['body']['length_verdict']}")
        if not a["body"]["has_cta"]:
            notes.append(f"Email {i}: no call to action found")
        if a["spam"]["phrases_found"]:
            notes.append(f"Email {i}: spam-associated phrases: {', '.join(a['spam']['phrases_found'])}")
        for t in a["ai_tells"]:
            notes.append(f"Email {i}: AI tell: {t}")
    if notes:
        print("\n  FIX LIST")
        for n in notes:
            print(f"     - {n}")

    print("\n  SCORE BREAKDOWN")
    for k, v in scoring["breakdown"].items():
        label = k.replace("_", " ").capitalize()
        bar_len = round(v["score"] / 10)
        bar = "#" * bar_len + "." * (10 - bar_len)
        print(f"  {label:<22} [{bar}] {v['score']:>3}/100  (weight {v['weight']})")

    print()
    print("=" * 66)
    print(f"  Overall: {scoring['overall']}/100   Grade: {scoring['grade']}")
    print("=" * 66)


if __name__ == "__main__":
    main()
