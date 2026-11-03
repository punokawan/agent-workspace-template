---
description: Finish work in a worktree — verify, generate the changelog entry, rebase onto the repo's integration branch, fast-forward it in, push, and delete the branch. No PR: feature work lands directly on the integration branch.
allowed-tools: Bash, Read, Grep, Skill, AskUserQuestion
---

Finish: $ARGUMENTS  (expected `<project>/<repo> <slug>`; empty → the worktree bound to the CURRENT run)

## Procedure — every gate is blocking

```bash
W=.claude/scripts
```

**1. Load skills.** `worktree-workflow`, `git-workflow`, `verification`, `changelog-and-release`.

**2. Resolve the target.**
```bash
bash $W/wt.sh list
bash $W/state.sh show | head -20
```
If several worktrees share the slug (multi-repo work), finish each in turn — backend first,
then the clients that consume its API.

**3. Review the diff yourself.** Do not rely on any earlier agent's report.
```bash
WT=.wt/<project>/<repo>/<slug>
git -C $WT status --short
# resolve the integration branch from project.json
BASE=$(bash -c "source $W/lib.sh; base_ref <project> <repo>")
git -C $WT diff $BASE..HEAD --stat
git -C $WT diff $BASE..HEAD
```
Scan specifically for: secrets or tokens, customer PII, debug prints, commented-out code,
`.env` or key files staged by accident. Any hit → stop and report before going further.

**4. Commit anything uncommitted** using `git-workflow` conventions. Atomic commits, imperative
subjects written as user-facing documentation — they become the changelog.

**5. GATE — verification.** 
```bash
bash $W/verify.sh wt:<project>/<repo>/<slug> --full 2>&1 | tee /tmp/verify-<slug>.txt
```
Exit non-zero → **stop**. Report the real failures and whether each is yours or pre-existing.
Do not push. Do not land. A pre-existing failure does not become your pass.

**6. Changelog.**
```bash
bash $W/changelog.sh add <project>/<repo> <slug>
```
Review the generated `[Unreleased]` entries — they are only as good as the commit subjects.
Fix any that read as internal chatter rather than user-facing change, then commit:
`docs(changelog): record <slug>`.

**7. Rebase and push** — confirm with the user first; this is outward-facing.
```bash
bash $W/wt.sh push <project>/<repo> <slug>
```
Rebase conflicts → resolve in the worktree, re-run step 5, then retry.

**8. Land it** — confirm with the user first; this is outward-facing.
```bash
bash $W/wt.sh land <project>/<repo> <slug>
```
This rebases, fast-forward merges into the integration branch, then retires the worktree
(local-only files archived to `.cache/wt-archive/`, worktree removed, local branch deleted) and
prints the push command. Pass `--keep` only when a follow-up is planned in the worktree. Run on
confirmation:
```bash
git -C projects/<project>/<repo> push origin <base>
git -C projects/<project>/<repo> push origin --delete <branch>   # if it was pushed
```
`land` refuses if it is not a clean fast-forward — re-run the rebase rather than making a merge
commit. **Never** land into production (`main`).

**9. Record.**
```bash
bash $W/state.sh log land "<project>/<repo> <branch> -> <base> @ <sha>; branch deleted"
bash $W/state.sh phase <slug> done
```

## Report

```
FINISHED  <project>/<repo> <branch>
Commits   : <n>
Verified  : <checks + exit codes>
Changelog : <n entries under [Unreleased]>
Landed on : <integration branch> @ <sha>   (pushed: yes/no)
Branch    : deleted local + remote / kept because <reason>
Worktree  : retired (archive: <path or none>) / kept with --keep because <reason>
```

## Rules

- Never push or land on a failed verification, no matter how small the change looks.
- Never merge into `main`, push `main`, or open an integration → `main` PR. That promotion is the
  user's alone — see `/release`.
- Never leave the working branch alive once its commits are on the integration branch.
- Never leave the landed worktree behind: `land` retires it unless `--keep` was passed for a planned follow-up.
- The only write to a user checkout permitted here is the fast-forward of the integration branch
  performed by `wt.sh land`, and only when that checkout is clean.
