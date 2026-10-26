---
description: Cut a release for one repo — promote the integration branch into production (the user's call), review commits since the last tag, generate the changelog section, bump the version, tag, and hand off to the deploy pipeline
allowed-tools: Bash, Read, Grep, Skill, AskUserQuestion
---

Release: $ARGUMENTS  (expected `<project>/<repo> [patch|minor|major]`)

Releases are outward-facing and hard to reverse. **Every push in this command needs the user's
explicit confirmation in this session.** Approval of one step is not approval of the next.

## Procedure

```bash
W=.claude/scripts
R=projects/<project>/<repo>
BASE=$(bash -c "source $W/lib.sh; proj field <project> <repo> integration")
PROD=$(bash -c "source $W/lib.sh; proj field <project> <repo> production")   # usually main
```

**1. Load** `changelog-and-release`, `git-workflow`, `verification`. Then read
`bash $W/project.sh show <project>`, `projects/<project>/AGENTS.md`, and
`projects/<project>/**/.claude/skills/<project>-release/SKILL.md` if it exists — release script, tags, deploy target.

**1b. The promotion is the user's, not yours.** A release means merging the integration branch
(`$BASE`) into production (`$PROD`). Prepare and verify it, show exactly
what would ship, then **stop and hand the merge to the user**. Never run it yourself.

```bash
git -C $R log --oneline origin/$PROD..origin/$BASE      # what promotion would ship
git -C $R diff --stat origin/$PROD..origin/$BASE
```

**2. Establish the real baseline.**
```bash
git -C $R fetch origin --tags
git -C $R log --oneline origin/$PROD -5
LAST=$(git -C $R describe --tags --abbrev=0 2>/dev/null || echo "")
git -C $R log --no-merges --oneline ${LAST:+$LAST..}origin/$PROD
```
If the repo has no tags yet, the range is the full history and the first tag is a decision to
put to the user.

**3. GATE — verify the branch being released, not your working copy.**
Verify the integration branch *before* promotion, and production *after* the user has merged.
```bash
bash $W/verify.sh <project>/<repo> --full
```
Exit non-zero → **stop**. Do not release a failing trunk. Report the failures.

> Report any pre-existing failure explicitly and say whether it is yours or inherited.
> Releasing over a known-failing gate is the user's call to make explicitly — surface it, do
> not decide for them.

**4. Preview the changelog and fix the input, not the output.**
```bash
bash $W/changelog.sh preview <project>/<repo> ${LAST:+$LAST..}origin/$PROD
```
Read every line as a user would. Vague subjects (`fixed bug`, `WIP`, `update code`) and
non-conventional subjects — which are **silently dropped** — must be corrected by rewording the
commits, not by hand-editing CHANGELOG.md. If rewording is impractical, say which changes will be
missing from the changelog and why.

**5. Choose the bump.** Recommend one from the actual commits and say why:
`feat` present → minor; only `fix`/`chore` → patch; breaking change (`!` or `BREAKING CHANGE`) →
major. Confirm with the user before proceeding.

**6. Write the changelog.**
```bash
bash $W/changelog.sh add-range <project>/<repo> ${LAST:+$LAST..}origin/$PROD
bash $W/changelog.sh release   <project>/<repo> <x.y.z>
```

**7. Bump the version.**
- Repo has `scripts/release.sh` (e.g. example/app) → read it; it typically handles the
  `pubspec.yaml` version+buildNumber and the tag. Show the command, confirm, then run it.
- No release script → commit the changelog, then tag:
  ```bash
  git -C $R tag v<x.y.z> && git -C $R push origin v<x.y.z>    # confirm first
  ```

**8. Record.**
```bash
bash $W/state.sh log release "<project>/<repo> v<x.y.z>: <n changelog entries>"
```

**9. Report** the deploy that this tag or promotion triggers — from the DEPLOY column of
`project.sh show` and the project's release overlay. Say plainly what will now happen
automatically, and mark anything you did not confirm in the workflow files `unverified`.

## Rules

- Never tag, push a tag, or trigger a deploy without confirmation in this session.
- Never hand-edit CHANGELOG.md — regenerate it.
- Never release on a failed `verify.sh` unless the user explicitly overrides, and record that
  override with `state.sh decide`.
- Never bump a version in the user's checkout as a side effect of another task.
