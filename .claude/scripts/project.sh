#!/usr/bin/env bash
# Project registry CLI — the only supported way to add a project to this workspace.
#
#   project.sh list                       — every registered project (* = active)
#   project.sh show [<project>]           — repos, stacks, branches, deploy targets
#   project.sh use <project>              — set the project bare repo ids resolve against
#   project.sh check                      — validate every manifest against disk
#   project.sh stacks                     — available stack presets
#   project.sh new <name> [opts]          — scaffold a new project from templates/project
#   project.sh add-repo <project> <id> <stack> [--clone <url>]
#
# `new` options:
#   --title "..."    human name          (default: capitalized <name>)
#   --desc  "..."    one-line summary
#   --rules <p>      rule profile (default: templates/rules/profiles.json "default")
#   --no-docs        skip docs/ + mkdocs.yml
#   --no-planning    skip planning/

source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"

TPL="$TEMPLATES_DIR/project"

# Substitute {{PLACEHOLDER}} tokens without invoking sed on untrusted text.
render() { # render <src> <dest> — never overwrites: a pulled project keeps its own files
  [[ -e "$2" ]] && { warn "kept existing ${2#"$ROOT"/}"; return 0; }
  NAME="$P_NAME" TITLE="$P_TITLE" DESCRIPTION="$P_DESC" \
  DATE="$(date '+%Y-%m-%d')" python3 - "$1" "$2" <<'PY'
import os, sys
src, dest = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
for key in ("NAME", "TITLE", "DESCRIPTION", "DATE"):
    text = text.replace("{{%s}}" % key, os.environ.get(key, ""))
os.makedirs(os.path.dirname(dest), exist_ok=True)
open(dest, "w", encoding="utf-8").write(text)
PY
}

cmd_new() {
  local name="${1:?usage: project.sh new <name> [--title ..] [--desc ..] [--rules ..]}"; shift
  [[ "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "project name must be kebab-case: '$name'"
  # A folder without a manifest (a repo just cloned or pulled here) is adopted, not refused.
  [[ -f "$PROJECTS_DIR/$name/project.json" ]] && die "projects/$name is already registered"

  P_NAME="$name"
  P_TITLE="$(python3 -c 'import sys;print(" ".join(w.capitalize() for w in sys.argv[1].split("-")))' "$name")"
  P_DESC=""
  P_RULES=""
  local want_docs=1 want_planning=1
  while (( $# )); do
    case "$1" in
      --title) P_TITLE="${2:?}"; shift 2 ;;
      --desc)  P_DESC="${2:?}";  shift 2 ;;
      --rules) P_RULES="${2:?}"; shift 2 ;;   # light | standard | strict
      --no-docs)     want_docs=0; shift ;;
      --no-planning) want_planning=0; shift ;;
      *) die "unknown option: $1" ;;
    esac
  done
  [[ -n "$P_DESC" ]] || P_DESC="$P_TITLE."

  local dest="$PROJECTS_DIR/$name"
  mkdir -p "$dest"
  # An older project kept its guide in CLAUDE.md: keep that text as AGENTS.md.
  if [[ ! -f "$dest/AGENTS.md" && -s "$dest/CLAUDE.md" && "$(cat "$dest/CLAUDE.md")" != "@AGENTS.md" ]]; then
    mv "$dest/CLAUDE.md" "$dest/AGENTS.md"; info "moved projects/$name/CLAUDE.md to AGENTS.md"
  fi
  render "$TPL/AGENTS.md.tmpl" "$dest/AGENTS.md"
  if [[ ! -s "$dest/CLAUDE.md" ]]; then printf '@AGENTS.md\n' > "$dest/CLAUDE.md"
  elif [[ "$(cat "$dest/CLAUDE.md")" != "@AGENTS.md" ]]; then
    warn "projects/$name has both AGENTS.md and a CLAUDE.md with its own text — merge them, then make CLAUDE.md '@AGENTS.md'"
  fi
  render "$TPL/gitignore.tmpl" "$dest/.gitignore"

  # A valid manifest with no repos yet, ready for add-repo, which records each repo's stack.
  # json.dump keeps any title or description safe.
  python3 - "$dest/project.json" "$name" "$P_TITLE" "$P_DESC" "$P_RULES" "$TEMPLATES_DIR/rules/profiles.json" <<'PY'
import json, sys
dest, name, title, desc, rules, profiles = sys.argv[1:7]
rules = rules or json.load(open(profiles, encoding="utf-8"))["default"]
json.dump({"name": name, "title": title, "description": desc,
           "planning": "planning", "docs": {"dir": "docs", "mkdocs": "mkdocs.yml"},
           "repos": [], "rules": {"profile": rules}}, open(dest, "w", encoding="utf-8"), indent=2)
open(dest, "a", encoding="utf-8").write("\n")
PY

  if (( want_planning )); then
    mkdir -p "$dest/planning/features" "$dest/planning/improvements" "$dest/planning/bugs"
    render "$TPL/planning/README.md"      "$dest/planning/README.md"
    render "$TPL/planning/bugs/README.md" "$dest/planning/bugs/README.md"
    [[ -e "$dest/planning/templates" ]] || cp -R "$TPL/planning/templates" "$dest/planning/templates"
    : > "$dest/planning/features/.gitkeep"
    : > "$dest/planning/improvements/.gitkeep"
  fi
  if (( want_docs )); then
    render "$TPL/docs/index.md"    "$dest/docs/index.md"
    render "$TPL/mkdocs.yml.tmpl"  "$dest/mkdocs.yml"
  fi

  bash "$SCRIPTS/rules.sh" sync "$name" >/dev/null || die "rules: could not render the profile into AGENTS.md"
  ok "created projects/$name"
  proj check --quiet || warn "manifest needs a repo before it will validate — see below"
  echo
  echo "Next:"
  echo "  1. add a repo:  bash .claude/scripts/project.sh add-repo $name <id> <stack> --clone <url>"
  echo "  2. make active: bash .claude/scripts/project.sh use $name"
  echo "  3. fill in     projects/$name/AGENTS.md — conventions, vocabulary, known defects"
  echo "  4. verify:      bash .claude/scripts/project.sh check"
}

cmd_add_repo() {
  local project="${1:?project}" id="${2:?repo id}" stack="${3:?stack}"; shift 3
  is_project "$project" || die "unknown project: $project"
  [[ "$id" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || die "repo id must be kebab-case: '$id'"
  [[ -f "$TEMPLATES_DIR/stacks/$stack.json" ]] || \
    die "unknown stack '$stack'. available: $(cmd_stacks | tr '\n' ' ')"

  local url=""
  while (( $# )); do
    case "$1" in
      --clone) url="${2:?}"; shift 2 ;;
      *) die "unknown option: $1" ;;
    esac
  done

  local dest="$PROJECTS_DIR/$project/$id"
  if [[ -n "$url" ]]; then
    [[ -e "$dest" ]] && die "$dest already exists"
    info "cloning into projects/$project/$id"
    git clone "$url" "$dest" || die "clone failed"
  elif [[ ! -d "$dest" ]]; then
    warn "no checkout at projects/$project/$id — clone it there, or re-run with --clone <url>"
  fi

  # Read the real integration branch off the clone rather than assuming one.
  local integration="dev"
  if [[ -d "$dest/.git" ]]; then
    for cand in dev development main; do
      git -C "$dest" rev-parse --verify --quiet "refs/remotes/origin/$cand" >/dev/null 2>&1 \
        && { integration="$cand"; break; }
    done
  fi

  python3 - "$PROJECTS_DIR/$project/project.json" "$id" "$stack" "$integration" <<'PY'
import json, sys
path, rid, stack, integration = sys.argv[1:5]
man = json.load(open(path, encoding="utf-8"))
if any(r["id"] == rid for r in man.get("repos", [])):
    sys.exit(f"repo '{rid}' is already in the manifest")
man.setdefault("repos", []).append({
    "id": rid, "stack": stack, "title": rid,
    "integration": integration, "production": "main", "deploy": "unverified"})
json.dump(man, open(path, "w", encoding="utf-8"), indent=2)
open(path, "a", encoding="utf-8").write("\n")
PY
  ok "registered $project/$id (stack=$stack, integration=$integration)"
  proj show "$project"
}

cmd_stacks() { ls "$TEMPLATES_DIR/stacks"/*.json 2>/dev/null | xargs -n1 basename | sed 's/\.json$//'; }

case "${1:-list}" in
  list)     proj list ;;
  show)     shift; proj show "$@" ;;
  use)      shift; proj use "$@" ;;
  check)    shift; proj check "$@" ;;
  stacks)   cmd_stacks ;;
  new)      shift; cmd_new "$@" ;;
  add-repo) shift; cmd_add_repo "$@" ;;
  *) die "usage: project.sh {list|show|use|check|stacks|new|add-repo}" ;;
esac
