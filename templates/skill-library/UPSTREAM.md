# Upstream

{{blocks}}

This library merges the sources above. Keep `LICENSE` (every upstream licence) and the Credits section
of `README.md` in any copy.

## What changed from upstream

- **One skill per topic.** When two sources cover the same topic they become one skill, never two.
  This also applies to any source added later.
- **Per-skill provenance.** Every skill has `SOURCES.md`: one row per SKILL.md section and per file,
  with the source key, upstream skill, file and commit, and `as is`, `edited: …` or `new: …`.
  `bash .claude/scripts/skills.sh sources check {{name}}` verifies the rows against the pinned sources.
- **Names.** Record the naming rule here (which source's name wins for a shared topic). Old names map
  to merged names in `docs/MAPPING.md`.
- **Not copied.** List what was left out and why.
- **Added here.** `README.md`, this file, `docs/`, `library.json`, the plugin manifests.

## Review

- pending: security + fit review of every source (read-only; read each script before its first run).

## Limits in this workspace

- None recorded yet beyond the workspace rules.

## Updating

All blocks above are `mode: merged`: the workspace tools report changes but never apply them.

1. `bash .claude/scripts/upstream.sh check {{name}}` shows which source has changes under its path.
2. `bash .claude/scripts/upstream.sh diff {{name}}:<key>` lists the changes and maps each changed file
   to the merged skill and part it feeds (from the `SOURCES.md` rows). Files with no row are new
   upstream files: run them through the same compare-and-merge step, following `docs/COMPARISON.md`.
3. Carry each change by hand. Set the new `commit` in the block, update each touched skill's
   `metadata.sources` and `SOURCES.md` rows, and bump `version` in both plugin manifests.
4. Run `bash .claude/scripts/skills.sh validate {{name}}`, `sources check {{name}}` and
   `index {{name}}`, and re-run the security scan.
5. Installed copies do not follow the repository: `claude plugin marketplace update punokawan`, then
   `claude plugin update {{name}}@punokawan`.
