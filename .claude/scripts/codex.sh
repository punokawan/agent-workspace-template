#!/usr/bin/env bash
# Delegate work to Codex CLI (signed in with ChatGPT) — the codex-delegate skill's runner.
#   codex.sh exec <dir> [--write] [--timeout s] [--image f]... "<prompt>"   code or images
#   codex.sh blender <script.py> [-- args]                                   run a bpy script
#   codex.sh sprite <in.png> <out.png> [--size 32] [--preview p.png]         pixel-art cleanup
#   codex.sh sheet <out.png> <image>...                                      review sheet + clipping
# Prompts go to OpenAI: never include customer data, secrets, or confidential material.
exec python3 "$(dirname "${BASH_SOURCE[0]}")/_codex.py" "$@"
