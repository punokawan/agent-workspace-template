#!/usr/bin/env bash
# Skill authoring: catch collisions early, keep merged libraries credited and checkable.
#
#   skills.sh overlap <SKILL.md|folder> | --text "<name and description>"
#                                         — same name (collision) or similar topic among existing skills
#   skills.sh new-library <name> --source key=<repo>[@sha][#folder] [...] [--title "..."]
#                                         — scaffold plugins/<name>/ like marketing-skills, credit filled in
#   skills.sh validate <plugin>           — frontmatter, names, links, script syntax (offline)
#   skills.sh sources check <plugin>      — every part has a SOURCES.md row; "as is" rows match upstream
#   skills.sh sources generate <plugin> <skill> <key> <upstream-path> [--note TEXT]
#                                         — SOURCES.md for a skill taken from one source
#   skills.sh snapshot <plugin>           — export each source at its pinned commit (used by sources)
#   skills.sh index <plugin>              — rebuild the plugin README skill table
#   skills.sh marketplaces                — every library listed for Claude Code and Codex
#
# Contributor guide: CONTRIBUTING.md. Nothing here runs upstream code.
source "$(dirname "${BASH_SOURCE[0]}")/lib.sh"
STUDIO_ROOT="$ROOT" exec python3 "$SCRIPTS/_skills.py" "$@"
