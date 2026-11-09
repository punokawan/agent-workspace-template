#!/usr/bin/env python3
"""Form field analyzer for form CRO.

Parses every <form> in an HTML file and flags conversion friction: field
count, required fields, high-friction fields (phone, address, company size),
fields without a visible label, input types that load the wrong mobile
keyboard, missing autocomplete hints, and generic submit-button copy.

Usage:
  python3 form_field_analyzer.py form.html          # text report
  python3 form_field_analyzer.py form.html --json   # JSON for pipelines
  python3 form_field_analyzer.py                    # demo on a sample form

Reads only the HTML file you pass. Writes nothing; prints to stdout.
Exit codes: 0 report printed, 1 no <form> found, 2 bad arguments or unreadable file.

Adapted from alirezarezvani/claude-skills, marketing-skill/form-cro (MIT).
"""

import argparse
import json
import sys
from html.parser import HTMLParser

SKIP_INPUT_TYPES = {"hidden", "submit", "button", "reset", "image"}
GROUPED_INPUT_TYPES = {"checkbox", "radio"}
TEXT_LIKE_TYPES = {"", "text", "search", "number"}
GENERIC_SUBMIT_COPY = {"submit", "send", "go", "ok", "enter"}


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------

class FormParser(HTMLParser):
    """Collects forms, their fields, labels and submit buttons."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.forms = []
        self.current = None
        self.label_stack = []
        self.label_for = {}
        self.fieldsets = []
        self.button = None

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()

        if tag == "form":
            if self.current is not None:
                self.forms.append(self.current)
            self.current = {
                "action": a.get("action", ""),
                "method": (a.get("method") or "GET").upper(),
                "autocomplete_off": a.get("autocomplete", "").lower() == "off",
                "fields": [],
                "buttons": [],
            }
            return

        if tag == "label":
            self.label_stack.append({"for": a.get("for", ""), "text": [], "fields": []})
            return
        if tag == "fieldset":
            self.fieldsets.append({"legend": False, "fields": []})
            return
        if tag == "legend" and self.fieldsets:
            self.fieldsets[-1]["legend"] = True
            return

        if self.current is None:
            return

        if tag == "input":
            itype = a.get("type", "text").lower()
            if itype in ("submit", "image"):
                self.current["buttons"].append(a.get("value") or a.get("alt") or "Submit")
                return
            if itype in SKIP_INPUT_TYPES:
                return
            self._add_field("input", itype, a)
        elif tag in ("select", "textarea"):
            self._add_field(tag, tag, a)
        elif tag == "button":
            btype = a.get("type", "submit").lower()
            self.button = {"text": []} if btype == "submit" else None

    def _add_field(self, tag, ftype, a):
        field = {
            "tag": tag,
            "type": ftype,
            "name": a.get("name", ""),
            "id": a.get("id", ""),
            "placeholder": a.get("placeholder", ""),
            "required": "required" in a or a.get("aria-required", "").lower() == "true",
            "autocomplete": a.get("autocomplete", ""),
            "aria_label": a.get("aria-label", "") or a.get("title", ""),
            "aria_labelledby": a.get("aria-labelledby", ""),
            "wrapped": bool(self.label_stack),
            "label_text": "",
        }
        if self.label_stack:
            self.label_stack[-1]["fields"].append(field)
        if self.fieldsets:
            self.fieldsets[-1]["fields"].append(field)
        self.current["fields"].append(field)

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        if self.label_stack:
            self.label_stack[-1]["text"].append(text)
        if self.button is not None:
            self.button["text"].append(text)

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "label" and self.label_stack:
            label = self.label_stack.pop()
            text = " ".join(label["text"]).strip()
            if label["for"]:
                self.label_for[label["for"]] = text
            for field in label["fields"]:
                field["label_text"] = field["label_text"] or text
        elif tag == "fieldset" and self.fieldsets:
            fieldset = self.fieldsets.pop()
            if fieldset["legend"]:
                # A legend labels a radio or checkbox group; text inputs still need their own label.
                for field in fieldset["fields"]:
                    if field["type"] in GROUPED_INPUT_TYPES:
                        field["wrapped"] = True
        elif tag == "button" and self.button is not None:
            if self.current is not None:
                self.current["buttons"].append(" ".join(self.button["text"]).strip() or "(no text)")
            self.button = None
        elif tag == "form" and self.current is not None:
            self.forms.append(self.current)
            self.current = None

    def finish(self):
        self.close()
        if self.current is not None:
            self.forms.append(self.current)
            self.current = None
        for form in self.forms:
            for field in form["fields"]:
                if field["id"] and field["id"] in self.label_for:
                    field["label_text"] = field["label_text"] or self.label_for[field["id"]]
                    field["wrapped"] = True
        return self.forms


# ---------------------------------------------------------------------------
# Field classification
# ---------------------------------------------------------------------------

def _tokens(*parts):
    tokens, cur = [], []
    for ch in " ".join(parts).lower():
        if ch.isalnum():
            cur.append(ch)
        elif cur:
            tokens.append("".join(cur))
            cur = []
    if cur:
        tokens.append("".join(cur))
    return tokens


def _field_tokens(f):
    return _tokens(f["name"], f["id"], f["autocomplete"], f["label_text"], f["placeholder"])


def _is_email(f, toks):
    return f["type"] == "email" or "email" in toks


def _is_phone(f, toks):
    return (f["type"] == "tel" or "tel" in toks
            or any("phone" in t for t in toks)
            or any(t.startswith("mobile") for t in toks))


def _is_address(f, toks):
    if _is_email(f, toks):
        return False
    return (any("address" in t for t in toks)
            or any(t in ("street", "city", "zip", "zipcode", "postal", "postcode") for t in toks))


def _is_company_size(f, toks):
    if any(t in ("employees", "headcount", "companysize", "teamsize") for t in toks):
        return True
    return "size" in toks and bool({"company", "team", "org", "organization"} & set(toks))


HIGH_FRICTION = (
    ("phone number", _is_phone),
    ("address", _is_address),
    ("company size", _is_company_size),
)


def _display(f):
    return f["name"] or f["id"] or f["label_text"] or f["tag"]


def _group_fields(fields):
    """One logical field per checkbox or radio group; every other control counts once."""
    groups, order = {}, []
    for f in fields:
        key = (f["type"], f["name"]) if f["type"] in GROUPED_INPUT_TYPES and f["name"] else id(f)
        if key not in groups:
            groups[key] = dict(f)
            order.append(key)
        else:
            g = groups[key]
            g["required"] = g["required"] or f["required"]
            g["wrapped"] = g["wrapped"] or f["wrapped"]
            g["label_text"] = g["label_text"] or f["label_text"]
            g["aria_label"] = g["aria_label"] or f["aria_label"]
    return [groups[k] for k in order]


# ---------------------------------------------------------------------------
# Analysis
# ---------------------------------------------------------------------------

def analyze_form(form):
    fields = _group_fields(form["fields"])
    issues, warnings, positives = [], [], []
    n = len(fields)
    required = sum(1 for f in fields if f["required"])

    # Field count (rule of thumb in references/form.md: 3 is baseline, 7+ costs heavily)
    if n == 0:
        warnings.append("No visible input fields found in this form.")
    elif n <= 3:
        positives.append(f"{n} field(s): low friction.")
    elif n <= 6:
        warnings.append(f"{n} fields: every field beyond the first three costs completions; "
                        "keep only fields with a downstream use.")
    else:
        issues.append(f"{n} fields: long for a lead form; cut fields nobody uses after submission, "
                      "or move them to a second step or progressive profiling.")

    if n > 2 and required == n:
        warnings.append(f"All {n} fields are required: mark fields optional unless follow-up needs them.")

    # High-friction fields
    for f in fields:
        toks = _field_tokens(f)
        for kind, test in HIGH_FRICTION:
            if test(f, toks):
                if f["required"]:
                    issues.append(f"Required {kind} field '{_display(f)}': high friction on top-of-funnel "
                                  "forms; make it optional, say why it is needed, or ask for it in a later step.")
                else:
                    warnings.append(f"Optional {kind} field '{_display(f)}': still adds friction; "
                                    "keep it only if follow-up uses it.")
                break

    # Labels
    placeholder_only, hidden_name, unlabeled = [], [], []
    for f in fields:
        if f["wrapped"] or f["aria_labelledby"]:
            continue
        if f["placeholder"]:
            placeholder_only.append(_display(f))
        elif f["aria_label"]:
            hidden_name.append(_display(f))
        else:
            unlabeled.append(_display(f))
    if unlabeled:
        issues.append(f"{len(unlabeled)} field(s) have no label, placeholder or accessible name: "
                      + ", ".join(unlabeled) + ".")
    if placeholder_only:
        warnings.append(f"{len(placeholder_only)} field(s) use placeholder text as the label: "
                        + ", ".join(placeholder_only)
                        + ". Placeholders disappear on input; add visible labels.")
    if hidden_name:
        warnings.append(f"{len(hidden_name)} field(s) have an accessible name but no visible label: "
                        + ", ".join(hidden_name) + ".")

    # Mobile keyboard types
    for f in fields:
        if f["tag"] != "input" or f["type"] not in TEXT_LIKE_TYPES:
            continue
        toks = _field_tokens(f)
        if "email" in toks:
            warnings.append(f"Field '{_display(f)}' looks like an email address but uses type=\"{f['type'] or 'text'}\": "
                            "use type=\"email\" for the email keyboard and built-in validation.")
        elif _is_phone(f, toks):
            warnings.append(f"Field '{_display(f)}' looks like a phone number but uses type=\"{f['type'] or 'text'}\": "
                            "use type=\"tel\" for the phone keypad.")

    # Autocomplete
    if form["autocomplete_off"]:
        warnings.append("The form sets autocomplete=\"off\", which blocks browser autofill.")
    text_fields = [f for f in fields if f["tag"] == "input" and f["type"] in TEXT_LIKE_TYPES | {"email", "tel"}]
    if text_fields and not any(f["autocomplete"] for f in text_fields):
        warnings.append("No autocomplete attributes: add tokens such as name, email, tel and organization "
                        "so browsers can autofill (most useful on mobile).")

    # Submit button
    if not form["buttons"]:
        issues.append("No submit button found; the form may submit through JavaScript only, so check it by hand.")
    for text in form["buttons"]:
        if text.strip().lower() in GENERIC_SUBMIT_COPY:
            warnings.append(f"Submit button says \"{text}\": name the outcome instead, "
                            "for example \"Get my quote\" or \"Send me the guide\".")

    return {
        "action": form["action"],
        "method": form["method"],
        "field_count": n,
        "required_count": required,
        "submit_buttons": form["buttons"],
        "fields": [
            {
                "name": _display(f),
                "type": f["type"],
                "required": f["required"],
                "visible_label": bool(f["wrapped"] or f["aria_labelledby"]),
                "autocomplete": f["autocomplete"],
            }
            for f in fields
        ],
        "issues": issues,
        "warnings": warnings,
        "strengths": positives,
    }


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

def format_report(analyses):
    lines = ["", "FORM CRO - FIELD ANALYSIS", "=" * 60]
    for i, a in enumerate(analyses, 1):
        target = f"action: {a['action'] or '(none)'}, method: {a['method']}"
        buttons = ", ".join(f'"{b}"' for b in a["submit_buttons"]) or "none"
        lines += ["", f"Form {i} ({target})",
                  f"  Fields: {a['field_count']} | Required: {a['required_count']} | Submit: {buttons}", "",
                  "  Fields (* = required):"]
        for f in a["fields"]:
            flags = " *" if f["required"] else ""
            label = "" if f["visible_label"] else "  [no visible label]"
            lines.append(f"    [{f['type']}] {f['name']}{flags}{label}")
        for title, key in (("Issues", "issues"), ("Warnings", "warnings"), ("Strengths", "strengths")):
            if a[key]:
                lines += ["", f"  {title} ({len(a[key])}):"]
                lines += [f"    - {msg}" for msg in a[key]]
    lines.append("")
    return "\n".join(lines)


SAMPLE_HTML = """
<form action="/submit" method="POST">
  <label for="name">Full Name</label>
  <input type="text" name="name" id="name" required placeholder="Jane Smith">

  <label for="email">Work Email</label>
  <input type="email" name="email" id="email" required placeholder="you@company.com">

  <label for="company">Company</label>
  <input type="text" name="company" id="company" required>

  <label for="phone">Phone Number</label>
  <input type="tel" name="phone" id="phone" required>

  <label for="role">Job Title</label>
  <input type="text" name="role" id="role" required>

  <label for="employees">Company Size</label>
  <select name="employees" id="employees" required>
    <option value="">Select...</option>
    <option value="1-10">1-10</option>
    <option value="11-50">11-50</option>
    <option value="51-200">51-200</option>
    <option value="200+">200+</option>
  </select>

  <label for="message">How can we help?</label>
  <textarea name="message" id="message" placeholder="Tell us about your needs..."></textarea>

  <button type="submit">Submit</button>
</form>
"""


def main():
    parser = argparse.ArgumentParser(
        description="Flag conversion friction in the <form> elements of an HTML file.",
        epilog="With no file, analyzes a built-in sample lead form.",
    )
    parser.add_argument("file", nargs="?", help="HTML file that contains the form(s)")
    parser.add_argument("--json", action="store_true", help="print JSON instead of a text report")
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, encoding="utf-8", errors="replace") as fh:
                html = fh.read()
        except OSError as exc:
            parser.error(f"cannot read {args.file}: {exc}")
    else:
        html = SAMPLE_HTML
        if not args.json:
            print("Demo mode: analyzing a sample lead capture form.")

    fp = FormParser()
    fp.feed(html)
    forms = fp.finish()
    if not forms:
        print("No <form> elements found in the HTML.", file=sys.stderr)
        sys.exit(1)

    analyses = [analyze_form(form) for form in forms]
    if args.json:
        print(json.dumps(analyses, indent=2))
    else:
        print(format_report(analyses))


if __name__ == "__main__":
    main()
