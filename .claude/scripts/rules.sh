#!/usr/bin/env bash
# Choose which rule modules each project follows, and render them into its AGENTS.md.
#   rules.sh list                              profiles, modules, and each project's choice
#   rules.sh set <project> <profile>           light, standard, strict, or a custom one
#   rules.sh enable|disable <project> <module>  adjust one module on top of the profile
#   rules.sh default <profile>                  profile new projects start on
#   rules.sh profile new <name> [from <p>] | add|remove <name> <module> | delete <name>
#   rules.sh adopt <project> [profile]          bring an existing project in
#   rules.sh sync | check                       re-render the blocks / fail when stale
exec python3 "$(dirname "${BASH_SOURCE[0]}")/_rules.py" "$@"
