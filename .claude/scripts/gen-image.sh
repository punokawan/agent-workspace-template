#!/usr/bin/env bash
# Generate an image with the Gemini API. The key comes from $GEMINI_API_KEY or the macOS Keychain
# item "gemini-api-key"; it is never printed, logged, or written to disk.
#
#   gen-image.sh "<prompt>" [--out <file.png>] [--ref <image>]... [--aspect 1:1] [--model <id>] [--list-models]
#   --ref sends a reference image to edit or match (repeatable); --aspect sets the output ratio.
#
# Prompts are sent to Google: never include customer data, secrets, or confidential material.
set -euo pipefail

MODEL="gemini-3.1-flash-image"
OUT=""
PROMPT=""
REFS=()
ASPECT=""

die() { echo "gen-image: $*" >&2; exit 1; }

key() {
  local k="${GEMINI_API_KEY:-}"
  [[ -n "$k" ]] || k="$(security find-generic-password -a "$USER" -s gemini-api-key -w 2>/dev/null || true)"
  [[ -n "$k" ]] || die "no key: set GEMINI_API_KEY or add the Keychain item 'gemini-api-key'"
  printf '%s' "$k"
}

list_models() {
  GEMINI_KEY="$(key)" python3 - <<'PY'
import json, os, urllib.request
req = urllib.request.Request(
    "https://generativelanguage.googleapis.com/v1beta/models?pageSize=200",
    headers={"x-goog-api-key": os.environ["GEMINI_KEY"]})
with urllib.request.urlopen(req, timeout=30) as r:
    for m in json.load(r).get("models", []):
        if "image" in m["name"].lower():
            print(m["name"].removeprefix("models/"))
PY
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --out) OUT="${2:?--out needs a path}"; shift 2 ;;
    --model) MODEL="${2:?--model needs an id}"; shift 2 ;;
    --ref) [[ -f "${2:-}" ]] || die "--ref needs an existing image"; REFS+=("$2"); shift 2 ;;
    --aspect) ASPECT="${2:?--aspect needs a ratio}"; shift 2 ;;
    --list-models) list_models; exit 0 ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    -*) die "unknown flag: $1" ;;
    *) [[ -z "$PROMPT" ]] || die "one prompt only (quote it)"; PROMPT="$1"; shift ;;
  esac
done

[[ -n "$PROMPT" ]] || die "usage: gen-image.sh \"<prompt>\" [--out file.png] [--model id]"
[[ -n "$OUT" ]] || OUT="${TMPDIR:-/tmp}/gen-image-$(date +%Y%m%d-%H%M%S).png"
mkdir -p "$(dirname "$OUT")"

REFS_JOINED="$(printf '%s\n' "${REFS[@]+"${REFS[@]}"}")" \
GEMINI_KEY="$(key)" PROMPT="$PROMPT" MODEL="$MODEL" OUT="$OUT" ASPECT="$ASPECT" python3 - <<'PY'
import base64, json, os, sys, urllib.error, urllib.request

import mimetypes
parts = []
for path in filter(None, os.environ.get("REFS_JOINED", "").splitlines()):
    mime = mimetypes.guess_type(path)[0] or "image/png"
    with open(path, "rb") as f:
        parts.append({"inline_data": {"mime_type": mime, "data": base64.b64encode(f.read()).decode()}})
parts.append({"text": os.environ["PROMPT"]})
config = {"responseModalities": ["TEXT", "IMAGE"]}
if os.environ.get("ASPECT"):
    config["imageConfig"] = {"aspectRatio": os.environ["ASPECT"]}
body = json.dumps({"contents": [{"parts": parts}], "generationConfig": config}).encode()
req = urllib.request.Request(
    f"https://generativelanguage.googleapis.com/v1beta/models/{os.environ['MODEL']}:generateContent",
    data=body,
    headers={"x-goog-api-key": os.environ["GEMINI_KEY"], "Content-Type": "application/json"})
try:
    with urllib.request.urlopen(req, timeout=180) as r:
        data = json.load(r)
except urllib.error.HTTPError as e:
    err = json.loads(e.read() or b"{}").get("error", {})
    sys.exit(f"gen-image: HTTP {e.code} {err.get('status', '')}: {err.get('message', '')[:300]}")

out, note = os.environ["OUT"], []
for cand in data.get("candidates", []):
    for part in cand.get("content", {}).get("parts", []):
        blob = part.get("inlineData") or part.get("inline_data")
        if blob:
            ext = {"image/jpeg": ".jpg", "image/png": ".png", "image/webp": ".webp"}.get(blob.get("mimeType", ""), "")
            if ext and not out.lower().endswith(ext) and not (ext == ".jpg" and out.lower().endswith(".jpeg")):
                out = os.path.splitext(out)[0] + ext
            with open(out, "wb") as f:
                f.write(base64.b64decode(blob["data"]))
            print(out)
            if note:
                print("note: " + " ".join(note)[:300], file=sys.stderr)
            sys.exit(0)
        if part.get("text"):
            note.append(part["text"].strip())
reason = (data.get("candidates") or [{}])[0].get("finishReason", "no candidates")
sys.exit(f"gen-image: no image returned ({reason}). {' '.join(note)[:300]}")
PY
