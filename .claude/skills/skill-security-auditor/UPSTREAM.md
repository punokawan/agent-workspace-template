# Upstream

```upstream
repo: https://github.com/alirezarezvani/claude-skills
path: engineering/skills/skill-security-auditor
commit: 8f082544116fc0d014188e521ca40304cdfc86b0
mode: copy
licence: MIT
extra: LICENSE
```

| | Source |
|---|---|
| Repository | https://github.com/alirezarezvani/claude-skills |
| Path taken | `engineering/skills/skill-security-auditor/`, plus the repository `LICENSE` |
| Commit | see the block above |
| Licence | MIT, Copyright (c) 2025 Alireza Rezvani |

Keep `LICENSE` with any copy.

Vendored on 2026-11-09 at the owner's request: curate claude-code-skills and take only the skills in use (this was the only one invoked in 120 days). Upstream name and content kept. Credit: Alireza Rezvani, claude-skills.

## What changed from upstream

- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.
  `bash .claude/scripts/upstream.sh check skill-security-auditor` proves it (it reports any local drift).
- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here
  one source supplies every file unchanged, so the block above is the whole provenance.

## Review

- 2026-11-09 (read-only): `scripts/skill_security_auditor.py` reads the scanned files and never
  imports or runs them. Its only subprocess is `git clone --depth 1` when given a URL; its only deletes
  remove its own temp clone. No network otherwise, no writes into the scanned skill.

## Limits in this workspace

- Scans a skill or plugin before it is installed or vendored. `upstream.sh add` and `upstream.sh pull`
  run it on the new files once this file records a dated review.
- Pass a local path (for example the `.cache/upstream/` copy or the vendored folder), not a URL.
- Not a codebase audit: for that use `security-audit` (Cloudflare) or the `security-auditor` agent.
- Known false positives: regex code that calls `.exec(`, text that forbids prompt injection, and docs
  that describe credentials. Read each FAIL before acting on it.

## Updating

1. `bash .claude/scripts/upstream.sh diff skill-security-auditor` — read every changed line, scripts in full.
2. `bash .claude/scripts/upstream.sh pull skill-security-auditor` — copies the files, bumps the commit, runs the scan.
3. Add a dated entry under Review: what changed, the scan result, and why each finding is or is
   not real.
