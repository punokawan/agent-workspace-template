#!/usr/bin/env python3
"""
email_sequence_analyzer.py: score each email of a cold outbound sequence 0-100.

Checks each email for:
  - Length (first email under ~80 words; 25-75 is the sweet spot)
  - Readability (sentence length, approximate Flesch reading ease)
  - Dead openers, AI tells, and jargon
  - Personalization density (signals of specific, targeted writing)
  - CTA clarity, and a high-friction meeting ask in the first email
  - Links (none in the first email, at most one later), HTML
  - Spam-trigger words
  - Subject line (2-4 words, lowercase, no first name, no fake "Re:"/"Fwd:")
And the sequence: more than 5 emails, uniform lengths, a long breakup email.

Usage:
  python3 email_sequence_analyzer.py sequence.json
  python3 email_sequence_analyzer.py sequence.json --json
  cat sequence.json | python3 email_sequence_analyzer.py -
  python3 email_sequence_analyzer.py                  # embedded sample

Input (JSON array, in send order):
  [{"email": 1, "subject": "...", "body": "..."}, ...]

Heuristic only: the cold-email skill's rules win where they disagree.
Stdlib only. Reads the input file or stdin; writes nothing.
"""

import argparse
import json
import re
import sys
from typing import Dict, List


# --- Word lists ------------------------------------------------------------

SPAM_TRIGGERS = [
    "free", "guaranteed", "no obligation", "act now", "limited time",
    "click here", "earn money", "make money", "risk-free", "special offer",
    "no cost", "winner", "congratulations", "you've been selected",
    "once in a lifetime", "urgent", "don't miss out", "buy now",
    "order now", "100%", "best price", "lowest price", "incredible deal",
    "amazing offer", "cash bonus", "extra cash", "fast cash",
    "you have been chosen", "exclusive deal", "as seen on",
    "dear friend", "valued customer",
]

DEAD_OPENERS = [
    "i hope this email finds you well", "i hope this finds you",
    "i wanted to reach out", "i am reaching out", "i'm reaching out",
    "my name is", "i'm writing to", "i am writing to",
    "hope you're doing well", "i hope you are doing well",
    "just following up", "just checking in", "circling back",
    "touching base", "per my last email", "as per my previous",
    "did you see my last email", "bumping this", "i never heard back",
]

# Fine later in an email, a tell when it opens one.
OPENER_ONLY = ["quick question", "i came across your profile"]

AI_TELLS_AND_JARGON = [
    "here's the thing", "i'll be honest", "say goodbye to", "unlock",
    "take it to the next level", "synergy", "leverage", "best-in-class",
    "leading provider", "game-changer", "game changer", "revolutionary",
    "cutting-edge", "seamless",
]

CONTRAST_REVEAL = re.compile(
    r"\b(?:it'?s|this is|that'?s)\s+not\s+(?:about\s+)?[^.!?\n]{1,60}?[,;:.]\s*(?:it'?s|this is|that'?s)\b",
    re.IGNORECASE,
)

PERSONALIZATION_SIGNALS = [
    r"\byou(?:r|rs|'re|'ve|'d|'ll)?\b",
    r"\b(?:saw|noticed|read|heard|found|noted)\b",
    r"\b(?:your team|your company|your role|your work|your recent|your post)\b",
    r"\b(?:as a|in your|at your|given your)\b",
    r"\b\d{4}\b",
    r"\$\d+|\d+%",
]

WEAK_CTA = [
    "let me know if you're interested", "let me know if you would be interested",
    "feel free to", "please don't hesitate", "if you have any questions",
    "looking forward to hearing from you", "i look forward to connecting",
    "hope we can connect",
]

STRONG_CTA_PATTERNS = [
    r"\b(?:10|15|20|30|45|60)[\s-]?min(?:ute)?s?\b",
    r"\b(?:call|chat|talk|speak|connect|meet)\b.*\?",
    r"\bworth\s+(?:a|an|it|exploring|comparing)\b",
    r"\buseful\b\s*\?",
    r"\b(?:reply|respond)\b",
]

LONG_MEETING_ASK = re.compile(r"\b(?:30|45|60)[\s-]?min(?:ute)?s?\b|\bhalf[\s-]an?[\s-]hour\b|\ban hour\b", re.IGNORECASE)

GENERIC_QUESTION_SUBJECTS = [
    "quick question", "have 15 minutes", "got a minute", "are you free",
    "a quick chat", "15 minutes",
]

FIRST_NAME_TOKEN = re.compile(
    r"\{\{?\s*first[_ ]?name\s*\}?\}|\[first[_ ]?name\]|%first[_ ]?name%", re.IGNORECASE)


def _phrase(phrase: str) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(phrase) + r"(?!\w)", re.IGNORECASE)


SPAM_PATTERNS = [(p, _phrase(p)) for p in SPAM_TRIGGERS]
TELL_PATTERNS = [(p, _phrase(p)) for p in AI_TELLS_AND_JARGON]


# --- Text utilities -------------------------------------------------------

def count_words(text: str) -> int:
    return len(text.split())


def count_sentences(text: str) -> int:
    sentences = re.split(r"[.!?]+", text)
    return max(1, len([s for s in sentences if s.strip()]))


def avg_words_per_sentence(text: str) -> float:
    return count_words(text) / count_sentences(text)


def syllables(word: str) -> int:
    """Approximate syllables: vowel groups, minus a silent trailing e."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee")) and groups > 1:
        groups -= 1
    return max(1, groups)


def flesch_reading_ease(text: str) -> float:
    words = [w for w in text.split() if re.search(r"[A-Za-z]", w)]
    if not words:
        return 0.0
    asl = len(words) / count_sentences(text)
    asw = sum(syllables(w) for w in words) / len(words)
    return max(0.0, min(100.0, 206.835 - 1.015 * asl - 84.6 * asw))


def reading_label(fre: float) -> str:
    if fre >= 80:
        return "Easy (about 6th grade or below)"
    if fre >= 70:
        return "Conversational"
    if fre >= 60:
        return "Plain English"
    if fre >= 50:
        return "Fairly difficult"
    return "Difficult (too complex for cold email)"


# --- Analysis --------------------------------------------------------------

def analyze_subject_line(subject: str) -> Dict:
    issues, warnings = [], []
    if not subject:
        return {"length": 0, "words": 0, "issues": ["No subject line provided"], "warnings": [], "score": 0}

    length = len(subject)
    words = subject.split()
    lower = subject.lower().strip()

    if len(words) > 4:
        warnings.append(f"{len(words)} words: short, internal-looking subjects (2-4 words) win")
    if length > 60:
        issues.append(f"Too long ({length} chars); mobile truncates at about 30-35")
    if subject.isupper() and len(subject) > 3:
        issues.append("All-caps subject")
    elif re.search(r"\b[A-Z]{4,}\b", subject):
        warnings.append("Shouting word in subject")
    if len(words) >= 2 and all(w[:1].isupper() for w in words if w[:1].isalpha()):
        warnings.append("Title Case looks like marketing; lowercase looks internal")
    if re.search(r"!{2,}|\?{2,}", subject):
        issues.append("Repeated punctuation looks like spam")
    if re.match(r"^\s*(?:re|fwd?)\s*:", subject, re.IGNORECASE):
        issues.append('Fake "Re:"/"Fwd:" subject destroys trust')
    if FIRST_NAME_TOKEN.search(subject):
        warnings.append("First name in subject reads as automation; use context instead")
    if re.search("[\U0001F300-\U0001FAFF☀-➿]", subject):
        warnings.append("Emoji in a B2B cold subject")
    if lower.endswith("?") and any(g in lower for g in GENERIC_QUESTION_SUBJECTS):
        issues.append("Generic question subject; specific pain questions work, generic ones fail")

    triggered = [p for p, pat in SPAM_PATTERNS if pat.search(subject)]
    if triggered:
        issues.append(f"Spam trigger words in subject: {', '.join(triggered)}")

    score = max(0, min(100, 100 - len(issues) * 20 - len(warnings) * 10))
    return {"length": length, "words": len(words), "issues": issues, "warnings": warnings, "score": score}


def analyze_body(body: str, position: int) -> Dict:
    """position is 1 for the first email of the sequence."""
    body_lower = body.lower()
    deductions = []

    word_count = count_words(body)
    fre = flesch_reading_ease(body)
    avg_wps = avg_words_per_sentence(body)

    if word_count > 125:
        deductions.append(("length", 15, f"{word_count} words: far over the ~80-word cap (aim for 25-75)"))
    elif word_count > 80:
        deductions.append(("length", 10, f"{word_count} words: over the ~80-word cap (aim for 25-75)"))

    if avg_wps > 20:
        deductions.append(("readability", 10, f"Sentences average {avg_wps:.0f} words; aim for 15 or fewer"))

    for opener in DEAD_OPENERS:
        if opener in body_lower:
            deductions.append(("opener", 20, f"Dead phrase: '{opener}'; open with their world"))
            break
    first_line = body_lower.strip()[:60]
    for opener in OPENER_ONLY:
        if first_line.startswith(opener):
            deductions.append(("opener", 10, f"Stock opener: '{opener}'"))
            break

    tells = [p for p, pat in TELL_PATTERNS if pat.search(body)]
    if CONTRAST_REVEAL.search(body):
        tells.append("it's not X, it's Y")
    if "—" in body:
        tells.append("em dash")
    if tells:
        deductions.append(("ai_tells", min(20, 5 * len(tells)), f"AI tells or jargon: {', '.join(tells[:6])}"))

    pers_matches = sum(len(re.findall(p, body_lower)) for p in PERSONALIZATION_SIGNALS)
    pers_density = pers_matches / word_count * 100 if word_count else 0
    if pers_density < 5:
        deductions.append(("personalization", 10, "Few personalization signals; the email may read as generic"))

    triggered = [p for p, pat in SPAM_PATTERNS if pat.search(body)]
    if triggered:
        deductions.append(("spam", min(25, len(triggered) * 5), f"Spam trigger words: {', '.join(triggered[:5])}"))

    for weak in WEAK_CTA:
        if weak in body_lower:
            deductions.append(("cta", 10, f"Weak CTA: '{weak}'; ask a direct question"))
            break
    # A question in the closing lines counts as the ask.
    lines = [ln.strip() for ln in body_lower.splitlines() if ln.strip()]
    closing_question = "?" in " ".join(lines[-2:])
    has_strong_cta = closing_question or any(re.search(p, body_lower) for p in STRONG_CTA_PATTERNS)
    if not has_strong_cta:
        deductions.append(("cta", 15, "No clear ask; every cold email needs one low-friction question"))
    if position == 1 and LONG_MEETING_ASK.search(body):
        deductions.append(("cta", 10, "30+ minute meeting ask in the first email; ask an interest question or 15 minutes"))

    if re.search(r"<html|<body|<table|<div|style=\"|font-family:", body_lower):
        deductions.append(("format", 20, "HTML detected; send plain text"))

    links = re.findall(r"https?://", body)
    if position == 1 and links:
        deductions.append(("links", 10, "Link in the first email; send none until they reply"))
    elif len(links) > 1:
        deductions.append(("links", 10, f"{len(links)} links; keep later emails to one"))

    score = max(0, min(100, 100 - sum(d[1] for d in deductions)))
    return {
        "word_count": word_count,
        "reading_ease_score": round(fre, 1),
        "reading_level": reading_label(fre),
        "avg_words_per_sentence": round(avg_wps, 1),
        "personalization_density": round(pers_density, 1),
        "has_strong_cta": has_strong_cta,
        "spam_triggers": triggered,
        "deductions": [(d[2], d[1]) for d in deductions],
        "score": score,
    }


def sequence_observations(results: List[Dict]) -> List[str]:
    notes = []
    if len(results) > 5:
        notes.append(f"{len(results)} emails: cap at 5 total; replies fall and complaints rise after the 4th follow-up")
    counts = [r["body_analysis"]["word_count"] for r in results]
    if len(counts) > 2 and all(abs(counts[i] - counts[i - 1]) < 20 for i in range(1, len(counts))):
        notes.append("All emails are similar length; vary length across the sequence")
    if len(results) > 1 and results[-1]["body_analysis"]["word_count"] > 100:
        notes.append("Final (breakup) email should be 3-5 sentences")
    return notes


def grade(score: int) -> str:
    if score >= 85:
        return "Strong"
    if score >= 65:
        return "Decent"
    if score >= 45:
        return "Needs work"
    return "Rewrite"


def print_report(results: List[Dict], notes: List[str]) -> None:
    print("\n" + "=" * 64)
    print("  COLD EMAIL SEQUENCE ANALYSIS")
    print("=" * 64)

    for r in results:
        subj, body = r["subject_analysis"], r["body_analysis"]
        print(f"\n-- Email {r['email']}: \"{r['subject']}\" --")
        print(f"   Overall: {r['overall_score']}/100  {grade(r['overall_score'])}")
        print(f"\n   Subject ({subj['words']} words, {subj['length']} chars): {subj['score']}/100")
        for issue in subj.get("issues", []):
            print(f"   [x] {issue}")
        for warn in subj.get("warnings", []):
            print(f"   [!] {warn}")
        print("\n   Body:")
        print(f"   Words: {body['word_count']}  |  Reading: {body['reading_level']} "
              f"({body['reading_ease_score']})  |  Avg sentence: {body['avg_words_per_sentence']} words  |  "
              f"Personalization density: {body['personalization_density']}%")
        print(f"   CTA: {'clear ask found' if body['has_strong_cta'] else 'no clear ask found'}")
        if body.get("deductions"):
            print("\n   Issues found:")
            for desc, pts in body["deductions"]:
                print(f"   [-{pts:2d}] {desc}")

    scores = [r["overall_score"] for r in results]
    avg = sum(scores) // len(scores) if scores else 0
    print(f"\n{'=' * 64}")
    print(f"  SEQUENCE OVERALL: {avg}/100  {grade(avg)}")
    print(f"  Emails analyzed: {len(results)}")
    if notes:
        print("\n  Sequence observations:")
        for n in notes:
            print(f"  [!] {n}")
    print("=" * 64 + "\n")


# --- Sample data ----------------------------------------------------------

SAMPLE_SEQUENCE = [
    {
        "email": 1,
        "subject": "sdr ramp time",
        "body": (
            "Saw you're hiring four SDRs at once. That's a fast scale-up.\n\n"
            "At this stage ramp time usually hurts more than recruiting. Four new reps at once make "
            "onboarding gaps expensive. The average ramp in your segment is around 4.5 months; "
            "the fastest teams get it to 2.5.\n\n"
            "We've helped three similar-sized SaaS teams close that gap. Happy to share what worked.\n\n"
            "Worth comparing notes?"
        ),
    },
    {
        "email": 2,
        "subject": "re: your onboarding stack",
        "body": (
            "I hope this email finds you well. I wanted to follow up on my previous email.\n\n"
            "Just checking in to see if you had a chance to review what I sent. "
            "As mentioned, our platform offers a comprehensive suite of tools designed to "
            "help sales teams of all sizes achieve unprecedented growth through our "
            "revolutionary AI-powered onboarding solution.\n\n"
            "I'd love to schedule a 45-minute product demo at your earliest convenience. "
            "Please don't hesitate to reach out if you have any questions. "
            "I look forward to hearing from you!\n\n"
            "Click here to book a time: https://example.com/book"
        ),
    },
    {
        "email": 3,
        "subject": "sdr ramp benchmark",
        "body": (
            "One data point that might help: across the 40 SaaS teams we've benchmarked, "
            "the teams with the fastest SDR ramp invest more in structured onboarding in the "
            "first 30 days than in hiring experienced reps.\n\n"
            "Happy to share the full breakdown if it's relevant to where you're headed.\n\n"
            "Useful?"
        ),
    },
    {
        "email": 4,
        "subject": "sdr onboarding",
        "body": (
            "Is SDR onboarding a priority right now, or is the timing off?\n\n"
            "Either answer helps me know whether to stay in touch."
        ),
    },
    {
        "email": 5,
        "subject": "closing the loop",
        "body": (
            "I'll stop cluttering your inbox after this one.\n\n"
            "If SDR ramp time becomes a priority, reply here and I'll pick it up.\n\n"
            "If someone else at your company owns sales enablement, a name would go a long way.\n\n"
            "Either way, good luck with the expansion."
        ),
    },
]


# --- Main -----------------------------------------------------------------

def load(source: str):
    try:
        if source == "-":
            return json.load(sys.stdin)
        with open(source, "r", encoding="utf-8") as f:
            return json.load(f)
    except OSError as exc:
        sys.exit(f"Error: cannot read {source}: {exc}")
    except json.JSONDecodeError as exc:
        sys.exit(f"Error: invalid JSON: {exc}")


def main():
    parser = argparse.ArgumentParser(
        description="Score each email of a cold outbound sequence 0-100: length, readability, "
                    "openers, AI tells, personalization, CTA, links, spam words, subject line.",
        epilog='Input: JSON array of {"email": n, "subject": "...", "body": "..."} in send order.',
    )
    parser.add_argument("file", nargs="?", default=None,
                        help="JSON file with the sequence; '-' reads stdin; omit for the embedded sample")
    parser.add_argument("--json", action="store_true", help="Output JSON only")
    args = parser.parse_args()

    if args.file:
        sequence = load(args.file)
    else:
        if not args.json:
            print("No file provided: running on the embedded sample sequence.")
        sequence = SAMPLE_SEQUENCE
    if not isinstance(sequence, list) or not sequence:
        sys.exit("Error: input must be a non-empty JSON array of emails")

    results = []
    for position, email in enumerate(sequence, 1):
        subject = email.get("subject", "") or ""
        body = email.get("body", "") or ""
        subject_analysis = analyze_subject_line(subject)
        body_analysis = analyze_body(body, position)
        results.append({
            "email": email.get("email", position),
            "subject": subject,
            "subject_analysis": subject_analysis,
            "body_analysis": body_analysis,
            # Overall: 30% subject, 70% body
            "overall_score": int(subject_analysis["score"] * 0.3 + body_analysis["score"] * 0.7),
        })
    notes = sequence_observations(results)

    if args.json:
        print(json.dumps({
            "emails_analyzed": len(results),
            "average_score": sum(r["overall_score"] for r in results) // len(results),
            "sequence_observations": notes,
            "results": results,
        }, indent=2))
    else:
        print_report(results, notes)


if __name__ == "__main__":
    main()
