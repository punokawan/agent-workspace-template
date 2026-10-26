#!/usr/bin/env bash
# Planning index + drift detection. Frontmatter is the single source of truth.
#
#   plan.sh index [--project <p>]          — regenerate <project>/planning/INDEX.md
#   plan.sh index --check                  — exit 1 if any INDEX.md is stale
#   plan.sh audit [--project <p>]          — cross-check declared status against real code
#   plan.sh list [status|area=x] [--project <p>]
#   plan.sh set <id> <status> [note]       — update one plan's status
#
# With no --project, every registered project that has a planning/ directory is covered.
# Statuses: draft scoped in-progress partial shipped dropped needs-review
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
PY="$SCRIPTS/_plan.py"

case "${1:-index}" in
  index)  shift; STUDIO_ROOT="$ROOT" python3 "$PY" index "$@" ;;
  audit)  shift; STUDIO_ROOT="$ROOT" python3 "$PY" audit "$@" ;;
  list)   shift; STUDIO_ROOT="$ROOT" python3 "$PY" list  "$@" ;;
  set)    shift; STUDIO_ROOT="$ROOT" python3 "$PY" set   "$@" ;;
  *) die "usage: plan.sh {index|audit|list|set}" ;;
esac
