# Upstream

Vendored unchanged from https://github.com/heydamir/unslop (`skills/unslop`, plus `LICENSE`), commit `a6f121eee5f29c2f74976b75456feae8b66afb3a`, CC BY 4.0.
Created by Damir Sokolovsky (@heydamir, https://x.com/heydamir). Keep this credit in any copy or adaptation, and keep the
"unslop by @heydamir" credit in every story video, as the licence asks.
Only this file is ours. Reviewed 2026-11-04 (read-only: content, licence, secret scan, grep of both scripts; scripts not run).
To update: re-download every file at a newer commit, change the SHA here, and review the diff.

Use in this workspace (routed from .claude/agents/ui-designer.md; the skill itself is unchanged):
- Use it only for public, landing and marketing pages, and for new mockups. Never on app screens that already follow a
  design system (for RukunKita: docs/agent/06_design.md); use better-interface and audit-ai-design-slop there.
- Paid image generation (fal, Replicate, OpenAI images, Higgsfield) needs the owner's approval for each generation.
- Installing or connecting an MCP server needs the owner's approval. An agent never does it on its own.
- scripts/snapshot.mjs (fetches a live site with Playwright) and scripts/story.mjs (local server + ffmpeg) get a full line-by-line
  audit before their first run in this workspace. Record the audit date here.
- Its direction step must not override an owner-approved art direction or brand.
