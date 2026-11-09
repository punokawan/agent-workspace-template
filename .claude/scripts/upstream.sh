#!/usr/bin/env bash
# Vendored skills: track each one's upstream source and update it from there.
#
#   upstream.sh list                      — every UPSTREAM.md block (offline)
#   upstream.sh lint                      — validate every block (offline; audit.sh runs it)
#   upstream.sh check [name...]           — newer upstream commits + local drift from the pin
#   upstream.sh diff <name> [--to SHA] [--stat]
#                                         — upstream changes; merged plugins also map each file to its skill
#   upstream.sh pull <name> [--to SHA] [--force]
#                                         — copy-mode skills: take a newer commit, bump the pin, scan
#   upstream.sh add <repo> <path> [--name N] [--commit SHA] [--extra FILE] [--licence L]
#                                         — vendor a new skill unchanged into .claude/skills/<name>
#
# Clones are cached in .cache/upstream/. The only upstream code it runs is the vendored
# skill-security-auditor (static scan), and only once its UPSTREAM.md records a dated review.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
STUDIO_ROOT="$ROOT" exec python3 "$SCRIPTS/_upstream.py" "$@"
