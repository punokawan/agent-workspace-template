## What this changes

<!-- One or two lines. -->

## Skills checklist

Delete this section when the pull request adds or changes no skill. Guide: `CONTRIBUTING.md`.

- [ ] Path: A (own skill) / B (vendored unchanged) / C (new merged library) / D (new source for a library)
- [ ] `bash .claude/scripts/skills.sh overlap …` run for every new skill; collisions merged, boundaries written
- [ ] Licence allows copying; upstream `LICENSE` and copyright lines kept
- [ ] Path B: `UPSTREAM.md` has the source block, credit, a dated review and limits; vendored files unedited
- [ ] Path C/D: every skill has `metadata.sources`, the `Sources and credits` line and a complete `SOURCES.md`
- [ ] Path C/D: `docs/MAPPING.md` and `docs/COMPARISON.md` updated; README credits table lists every source
- [ ] Every new or changed script read line by line; security scan result recorded under `## Review`
- [ ] No secrets, customer data or project-specific facts

## Checks

- [ ] `bash .claude/scripts/upstream.sh lint`
- [ ] `bash .claude/scripts/skills.sh validate <library>` and `sources check <library>` (libraries only)
- [ ] `python3 -m unittest discover -s .claude/scripts/tests`
- [ ] `bash .claude/scripts/audit.sh` (no new FAIL)
