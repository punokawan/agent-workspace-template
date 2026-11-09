# Contributing skills

This repository is public. Every skill in it keeps its credit, and no topic has two skills. This
guide shows how to add a skill so that both stay true. Run every command from the repository root.

## Rules that never change

1. **Credit stays.** Never remove an upstream `LICENSE`, copyright line or credit. Every part of an
   adapted skill names its source in a table.
2. **One skill per topic.** When two sources cover the same topic, they become one skill with a
   `SOURCES.md` table that shows which part came from which source. Two skills for one topic are not
   accepted.
3. **Licence first.** Copy content only when its licence allows it (table below). No licence means no
   copy.
4. **Nothing private.** No secrets, keys, customer data or project-specific facts. Project rules live
   in each project's own guide, never in a shared skill.
5. **Read code before it runs.** A vendored script is read line by line before its first run, and the
   review is recorded with its date.

| Licence of the source | You may | You must |
|---|---|---|
| MIT, BSD, ISC | copy, adapt | keep the licence text and copyright line |
| Apache-2.0 | copy, adapt | keep the licence and any `NOTICE`, mark changed files |
| CC BY 4.0 | copy, adapt | credit the author as the licence asks, say what changed |
| CC BY-NC, CC BY-ND, "all rights reserved", none | nothing | link to it instead of copying |
| GPL, AGPL | ask the maintainer first | (copyleft would cover the whole library) |

## Pick your path

| You have | Path | Result |
|---|---|---|
| A skill you wrote yourself | A | `.claude/skills/<name>/` |
| One upstream skill you want unchanged | B | `.claude/skills/<name>/` + `UPSTREAM.md` |
| Several upstream libraries on one domain (like `marketing-skills`) | C | `plugins/<name>/` |
| A new source for a library that exists | D | new block + new `SOURCES.md` rows |

Before any path, check for collisions:

```bash
bash .claude/scripts/skills.sh overlap path/to/candidate/SKILL.md     # a folder or SKILL.md
bash .claude/scripts/skills.sh overlap --text "name and one-line description"
```

`COLLISION` means a skill with the same name exists. `high` and `medium` rows share topic words; read
them and decide with the table in [When skills collide](#when-skills-collide).

### A. Your own skill

1. Create `.claude/skills/<name>/SKILL.md` with frontmatter `name` (equal to the folder), a
   `description` under 1024 characters that says when to use it and when not to, and `license: MIT`.
2. Run `bash .claude/scripts/roster.sh`, then `bash .claude/scripts/audit.sh`.

### B. Vendor one upstream skill unchanged

1. Ask the maintainer before you add a new source.
2. Run:

   ```bash
   bash .claude/scripts/upstream.sh add https://github.com/<owner>/<repo> <path/to/skill>
   ```

   It copies the skill at a pinned commit with the upstream `LICENSE`, writes `UPSTREAM.md` with a
   source block, runs the collision check (it stops on a name collision) and lists every script for
   review.
3. Fill in `UPSTREAM.md`: the credit line, a dated entry under `## Review` (what you read, what each
   script does), and `## Limits in this workspace` (boundaries with skills that exist here).
4. Never edit the vendored files. To change behaviour, write the boundary in `UPSTREAM.md`, or take
   path C.
5. Run `bash .claude/scripts/upstream.sh lint`, `bash .claude/scripts/roster.sh` and
   `bash .claude/scripts/audit.sh`.

### C. Merge several upstream libraries into one

`plugins/marketing-skills/` is the reference: 61 skills from two libraries, each with a `SOURCES.md`.

1. Ask the maintainer, then scaffold the library. Each `--source` gets a short key; the tool pins the
   commit, reads the licence and copyright, and writes the credit everywhere:

   ```bash
   bash .claude/scripts/skills.sh new-library <name> \
     --source a=https://github.com/<owner>/<repo-a> \
     --source b=https://github.com/<owner>/<repo-b>@<sha>#<folder> \
     --title "One line on what the library is for"
   ```

2. **Plan before you copy.** For every upstream skill, run `skills.sh overlap` and fill
   `docs/MAPPING.md`: one row per topic, the base source, what is folded in, and keep or fold. Write
   the naming rule in `UPSTREAM.md` (which source's name wins for a shared topic).
3. **Build each skill.** Start from the base source's skill. Fold in only what the base lacks. Every
   skill gets:
   - frontmatter `metadata.version` and `metadata.sources: "a:<skill>@<sha7>; b:<skill>@<sha7>"`;
   - a last line `Sources and credits: [SOURCES.md](SOURCES.md)`;
   - a `SOURCES.md` table, one row per SKILL.md section and per file:

     | Part | From | Upstream file | Changed here |
     |---|---|---|---|
     | SKILL.md § Setup | a `seo-audit` @1234abc | skills/seo-audit/SKILL.md § Setup | as is |
     | SKILL.md § Checks | b `seo-audit` @5678def | skills/seo-audit/SKILL.md § Audit | edited: steps renumbered |
     | references/local.md | merge | — | new: written for the merged skill |

   For a skill taken from one source, generate the table and then add notes:
   `bash .claude/scripts/skills.sh sources generate <name> <skill> <key> <upstream/path>`.
4. Record per topic in `docs/COMPARISON.md` what was taken, what was dropped and why. Facts that
   change (laws, platform limits, prices) need a source and a date.
5. Check, and repeat until clean:

   ```bash
   bash .claude/scripts/skills.sh validate <name>       # frontmatter, names, links, script syntax
   bash .claude/scripts/skills.sh sources check <name>  # every part has a row; "as is" really is
   bash .claude/scripts/skills.sh index <name>          # README skill table
   bash .claude/scripts/upstream.sh lint
   ```

   Then scan with the `skill-security-auditor` skill and record the result under `## Review`.

### D. Add a source to an existing library

1. Add one `upstream` block to the library's `UPSTREAM.md` (`mode: merged`, a new `key`, `credit`,
   `licence`, `commit`, and `root` when the skills sit in a sub-folder).
2. Append the source's licence in full to the library's `LICENSE`, and add a row to the Credits table
   in its `README.md`.
3. Continue with path C from step 2. Existing skills that gain material get new `SOURCES.md` rows;
   their `metadata.sources` lists the new key.

## When skills collide

| What you found | Do this |
|---|---|
| Same name (`COLLISION`) | Merge into one skill (path C or D). Never add a second skill with that name. |
| Same job, different names | Merge into one skill; keep the name the library's naming rule picks; list the old name in `docs/MAPPING.md`. |
| Neighbouring jobs (for example SEO audit and AI search) | Keep both. Write the boundary in both descriptions ("For X, see Y"), and in a router skill if the library has one. |
| A vendored skill (path B) overlaps | Do not edit it. Write the boundary under `## Limits in this workspace` in its `UPSTREAM.md`. |

## Updating from upstream

```bash
bash .claude/scripts/upstream.sh check          # which sources moved, and any local drift
bash .claude/scripts/upstream.sh diff <name>    # what changed; libraries also map files to skills
bash .claude/scripts/upstream.sh pull <name>    # path B only: take the new commit, then review
```

Merged libraries (`mode: merged`) are never updated automatically. Follow the `## Updating` steps in
the library's `UPSTREAM.md`.

## Before you open a pull request

- `python3 -m unittest discover -s .claude/scripts/tests` passes.
- `bash .claude/scripts/audit.sh` shows no new FAIL.
- The pull request template checklist is complete.
