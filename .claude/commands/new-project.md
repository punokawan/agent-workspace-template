---
description: Register a new project in this workspace — scaffolds the manifest, AGENTS.md, planning/ and docs/ from templates, then wires its repos in. Pass a project name, or leave empty to be asked.
---

# /new-project

Add a project to the workspace so the shared harness can work on it. A project is a
manifest plus its checkouts — no script changes, ever.

## Harness contract

- **Where you may write:** `projects/<name>/` (new), and nothing else. Never touch another
  project's files, and never edit anything under `.claude/scripts/` to make a project fit.
- **Evidence required:** grade **A** (real command output) for every claim that a repo was
  cloned, a manifest validates, or a stack verifies. Never report a project as ready on the
  strength of having written the files.
- **Gate:** `bash .claude/scripts/project.sh check` must exit 0, and `/doctor` must still
  exit 0 afterwards.
- **Outward-facing:** cloning a repo reaches the network. Show the URL and confirm before
  cloning anything the user did not name explicitly.

## Steps

**1 — Collect what the manifest needs.** Ask only for what you cannot determine:

- project name (kebab-case — becomes `projects/<name>/`)
- a human title and a one-line description
- for each repo: an id (`app`, `backend`, `web`, `api`, …), a stack, and a clone URL

Available stacks: `bash .claude/scripts/project.sh stacks`. If none fits, say so and stop —
**adding a stack preset is a separate, deliberate change** (`templates/stacks/<stack>.json`),
not something to improvise inside this command.

**2 — Scaffold.**

```bash
bash .claude/scripts/project.sh new <name> --title "<title>" --desc "<one line>" [--rules light|standard|strict]
```

**3 — Add each repo.** Confirm the URL with the user first.

```bash
bash .claude/scripts/project.sh add-repo <name> <repo-id> <stack> --clone <url>
```

`add-repo` reads the real integration branch off the clone rather than assuming `dev`.
Check it landed on the right one: `bash .claude/scripts/project.sh show <name>`.

**4 — Validate against disk.**

```bash
bash .claude/scripts/project.sh check      # must exit 0
```

**5 — Prove the toolchain actually runs.** This is the step that catches a wrong stack:

```bash
bash .claude/scripts/verify.sh <name>/<repo-id> --quick
```

A check that SKIPs because its `requires:` glob found nothing is fine and expected — say so
explicitly. A check that FAILs on a fresh clone is a real finding: report it as a known
defect rather than working around it.

**6 — Write `projects/<name>/AGENTS.md`.** The template marks each section to fill with
`TODO`. Do not guess at them — read the code first, and leave a section empty rather than
inventing content:

- **What each repo owns** — one line per repo; never restate `project.json`
- **Conventions** — only what differs from the Studio defaults module, when the profile turns it on. Each rule concrete
  enough that a reviewer can point at a violation.
- **Domain vocabulary** — the nouns the code and copy use, and what they mean
- **Known defects** — anything already failing on the integration branch, dated, with the
  evidence grade. This is what stops a later agent absorbing someone else's breakage.

Each repo's layering goes in that repo's own `AGENTS.md` (with a `CLAUDE.md` holding
`@AGENTS.md`), committed in that repo. The project folder ships a `.gitignore` that tracks only
its guides; `git init` it if the project's guides should have history.

**7 — Make it active and re-check the workspace.**

```bash
bash .claude/scripts/project.sh use <name>
bash .claude/scripts/audit.sh            # /doctor — must still exit 0
```

## Report

State: the project path, each repo with its stack and integration branch, the real
verification result per repo (with exit codes), and which `AGENTS.md` sections you left for
the user to fill. If any repo failed to clone or verify, say which and why — never round a
partial setup up to "ready".
