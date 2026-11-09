# Upstream

```upstream
repo: https://github.com/alirezarezvani/claude-skills
path: engineering/skills/skill-security-auditor
commit: 8f082544116fc0d014188e521ca40304cdfc86b0
mode: copy
licence: MIT
extra: LICENSE
```

Vendored unchanged on 2026-11-09 at the owner's request (curate claude-code-skills: take only the
skills in use; this was the only one invoked in 120 days). Upstream name and content kept. Only this
file is ours.
Credit: Alireza Rezvani, claude-skills (`engineering/skills/skill-security-auditor`). Keep `LICENSE` with any copy.
Reviewed 2026-11-09 (read-only): `scripts/skill_security_auditor.py` reads the scanned files and never
imports or runs them. Its only subprocess is `git clone --depth 1` when given a URL; its only deletes
remove its own temp clone. No network otherwise, no writes into the scanned skill.
To update: `bash .claude/scripts/upstream.sh diff skill-security-auditor`, then `pull skill-security-auditor`.

Use in this workspace:
- Scans a skill or plugin before it is installed or vendored. `upstream.sh add` and `upstream.sh pull`
  run it on the new files once this file records a dated review.
- Pass a local path (for example the `.cache/upstream/` copy or the vendored folder), not a URL.
- Not a codebase audit: for that use `security-audit` (Cloudflare) or the `security-auditor` agent.
- Known false positives: regex code that calls `.exec(`, text that forbids prompt injection, and docs
  that describe credentials. Read each FAIL before acting on it.
