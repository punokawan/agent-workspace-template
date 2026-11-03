---
name: git-workflow
description: Two-branch development rules for every repo in every project — the production + integration branch model (names from project.json), short-lived working branches merged locally without a PR, commit conventions, hotfix flow, and release hand-off. Load this whenever making commits, cutting or merging branches, or preparing a release in any project.
license: Proprietary
compatibility: git, gh CLI
---

# Git Workflow

Applies to every product checkout `projects/<project>/<repo>/`, addressed as `<project>/<repo>`
(e.g. `example/backend`). Project-specific release steps live in `projects/<project>/AGENTS.md`.

---

## Model: two long-lived branches, nothing else

Every repo has exactly **two** permanent branches. Anything else is temporary by definition.

Both names are declared per repo in `project.json` and differ between repos (`dev`,
`development`, `main`, …). Resolve them, never assume:

```bash
bash .claude/scripts/project.sh show <project>   # INTEGRATION and PROD columns per repo
```

```
<prod> ─────────────────────────────────────────────────► production
       ▲
       │  the user merges, at release time, alone
       │
<integ>┴────────────────────────────────────────────────► integration (everything lands here)
       ▲         ▲          ▲
   feat/x    fix/y      chore/z     ← short-lived; merged locally, deleted the same day
```

**Rules:**

- A working branch exists **only while its work is in flight**. Merge it into the integration
  branch and delete it — local and remote — the same day.
- **No pull request for feature work.** Rebase, fast-forward, push. At this team size a PR costs
  more than it returns.
- **The integration branch → production (`main`) is the user's call, alone.** Never merge into
  it, never push to it, and never open that PR unless the user explicitly asks.
- Rebase onto the integration branch before merging — **fast-forward only**. No merge commits.
- Never leave a branch on the remote after its work has landed. If it has no unmerged commits,
  it should not exist.

## Where work happens — worktrees, not your checkouts

Every `projects/<project>/<repo>/` is **the user's working checkout**. They
often hold uncommitted work and the user may be editing them right now. Never commit, checkout,
branch, rebase, stash, or reset in them.

Every branch is created as a worktree under `.wt/<project>/<repo>/<slug>/`:

```bash
W=.claude/scripts
bash $W/wt.sh start <project>/<repo> <type>/<slug>    # off the integration branch, caches linked, cap enforced
```

Never run `git checkout -b` or `git worktree add` by hand — the first touches the user's checkout,
the second skips cache linking and costs GBs on a tight disk.

**Base branch is always the repo's integration branch** (`origin/<integration>` from
`project.json`). Never branch off production: it may sit behind the integration branch. Use `--from <tag>` only for a
hotfix off a release tag.

See the `worktree-workflow` skill for the full lifecycle.

---

## Branch Naming

```
<type>/<short-slug>
```

| Type | When | Example |
|---|---|---|
| `feat/` | New feature | `feat/wallet-archiving` |
| `fix/` | Bug fix | `fix/balance-zero-after-sync` |
| `refactor/` | Restructure, no behavior change | `refactor/subscription-repo-split` |
| `chore/` | Dependencies, tooling, config | `chore/update-objectbox-4` |
| `hotfix/` | Urgent production fix | `hotfix/crash-on-ipad-ios17` |
| `release/` | Release preparation (rare) | `release/2.1.0` — only if multi-step prep is needed |

Rules:
- `kebab-case` only — no underscores, no uppercase
- ≤ 40 characters
- Slug describes the change, not the ticket number (`feat/wallet-archiving` not `feat/FIN-412`)

---

## Commit Message Format

```
<type>(<optional-scope>): <imperative summary>
```

The subject line becomes the CHANGELOG.md entry — write it as user-facing documentation.

### Types

| Type | Use for |
|---|---|
| `feat` | New feature or capability visible to users |
| `fix` | Bug fix |
| `refactor` | Code restructuring — no behavior change |
| `perf` | Performance improvement |
| `test` | Test additions or corrections |
| `chore` | Dependencies, build scripts, tooling |
| `config` | Version bumps, env, platform config |
| `docs` | Documentation only |
| `style` | Formatting, lint — no logic change |

### Scope (optional)

Use the feature or layer name when the change is scoped: `feat(goal):`, `fix(wallet):`, `refactor(subscription):`, `fix(api/transaction):`, `feat(dashboard):`.
Omit scope when the change is cross-cutting or infrastructure-level.

### Good vs bad

```
# ✅ Clear, imperative, user-meaningful
feat(wallet): add archive and restore for wallets
fix(sync): prevent duplicate transactions after offline reconnect
refactor(subscription): split SubscriptionRepository into local and remote
fix(api/goal): return 404 when goal not found instead of 500
feat(dashboard): add monthly spending breakdown chart

# ❌ Vague, internal, or past-tense
fixed bug
WIP
update wallet code
refactor(wallet): extract _buildBody method into _WalletContent
chore: run dart format
```

### Body (optional, for non-obvious WHY)

```
fix(goal): recalculate funding when wallet currency changes

The goal funding allocation was computed once at creation time and never
updated when the linked wallet switched currency. Amounts in the goal
detail screen were stale by up to 2 decimal places.
```

Use the body for constraint explanations, non-obvious decisions, or workarounds — not for describing what the diff already shows.

### Atomic commits

One logical change per commit. Never bundle unrelated changes. Multiple commits per PR are fine when each represents a distinct step (entity → use case → BLoC → UI, or migration → DAO → handler → route).

---

## Pre-flight — one gate, not three

`verify.sh` is the single definition of "passes". Its checks come from the stack preset
(`templates/stacks/<stack>.json`); hand-written command lists drift. Run it before every commit and before every PR:

```bash
V=.claude/scripts/verify.sh

bash $V wt:<project>/<repo>/<slug> --quick    # format + analyze/vet/typecheck + lint
bash $V wt:<project>/<repo>/<slug> --full     # adds tests / build  ← required before a PR
```

| Stack | `--quick` runs | `--full` adds |
|---|---|---|
| `flutter` | `dart format --set-exit-if-changed`, `fvm flutter analyze` | `fvm flutter test` |
| `go` | `go build ./...`, `go vet ./...`, `gofmt -l` | `go test ./...` |
| `nextjs` | `npx tsc --noEmit`, `next lint` | `next build` |

Exit 0 → proceed. Exit 1 → the work is not done; report the real failures and whether each is
yours or pre-existing. Exit 2 → nothing ran; you may not claim verification. See the
`verification` skill.

> Do not assume a `type-check` npm script exists; check `package.json`. Typechecking is
> `npx tsc --noEmit`, which `verify.sh` already does.

---

## Integration — merge locally, no PR

Feature work never gets a pull request. When the work is done:

```bash
R=<project>/<repo>                 # e.g. example/backend
B=fix/balance-drift                # the working branch
BASE=<integration>                 # from project.sh show

W=.claude/scripts
bash $W/verify.sh wt:$R/${B#*/} --full   # 1. must exit 0
bash $W/wt.sh push $R ${B#*/}            # 2. rebase onto origin/$BASE — linear history
bash $W/wt.sh land $R ${B#*/}            # 3. fast-forward $BASE, retire the worktree + local branch
git -C projects/$R push origin $BASE     # 4. push the integration branch (confirm first)
git -C projects/$R push origin --delete $B   # 5. delete remote (if it was ever pushed)
```

If `land` refuses to fast-forward, the rebase in step 2 did not take — **do not** fall back to a
merge commit. Re-run the rebase.

### Before you merge

- [ ] `verify.sh --full` exits 0 for the repo
- [ ] Rebased onto the current integration branch
- [ ] Commit subjects follow the convention (each becomes a CHANGELOG entry)
- [ ] No debug prints, commented-out code, or leftover TODOs
- [ ] Project extras below

**Flutter:** l10n strings in every locale ARB file; DI registrations for new use cases /
repositories.
**Backend:** DB migration added if the schema changed; new routes registered in the router.
**Web:** new env vars documented; Supabase types regenerated if the schema changed.

### The only PR that still exists: integration → `main`

Production is `main`. Promoting the integration branch into it is a **release decision that belongs
to the user**. An agent may prepare it — draft the PR body with `pr.sh`, summarise what is about
to ship, confirm the verification gate is green — and then stop and hand it over.

Never merge to `main`. Never push to `main`. Never open that PR unasked.

---

## Hotfix Flow

For an urgent bug already in production:

```bash
R=<project>/<repo>
BASE=<integration>

# 1. Branch from the release tag — not from HEAD, which carries unreleased work
W=.claude/scripts
bash $W/wt.sh start $R hotfix/crash-on-ipad-ios17 --from 1.9.2

# 2. Fix, verify, commit
git commit -m "fix(layout): prevent nil-dereference crash on iPad iOS 17 landscape"

# 3. Merge into the integration branch like any other work
bash $W/wt.sh land $R crash-on-ipad-ios17   # then push $BASE and delete the branch, as above
```

Then **stop and tell the user** the hotfix is on `$BASE` and ready to promote. Shipping it means
merging into `main` and cutting a patch release — both are the user's decisions, not an agent's.

If `$BASE` carries unreleased features that must not ship with the hotfix, say so explicitly and
let the user choose: promote everything, or cherry-pick the fix onto `main` themselves.

---

## Release Hand-off

### Repos with a release script
Some repos ship `scripts/release.sh` (e.g. example/app). Check the repo and
`projects/<project>/AGENTS.md`; see the `changelog-and-release` skill for the full procedure.

```bash
# Review commits since last tag
git log $(git describe --tags --abbrev=0)..HEAD --no-merges --oneline

# Cut the release
bash scripts/release.sh   # choose: patch / minor / major
```

### Repos without one
Tag manually after verifying pre-flight:

```bash
# Review what's going in
git log $(git describe --tags --abbrev=0)..HEAD --no-merges --oneline

# Tag and push
git tag v1.4.0
git push origin v1.4.0
```

### Changelog — generated, never hand-written

```bash
C=.claude/scripts/changelog.sh

bash $C preview <repo> <last-tag>..HEAD      # inspect before writing
bash $C add-range <repo> <last-tag>..HEAD    # fold into [Unreleased]
bash $C release <repo> <x.y.z>               # cut [Unreleased] into a dated section
```

Entries come from conventional commit subjects, so **the commit subject *is* the changelog entry**.
Non-conventional subjects are silently skipped — a commit written as `fixed bug` never reaches the
changelog at all.

**Before any release** — run `preview` and confirm every line reads as user-facing documentation.
Fix vague commit subjects (reword via rebase) *before* tagging, not after.

**Tags and deploys are outward-facing.** Show the command, get the user's confirmation, then run
it. Never push a tag on your own initiative.

---

## Rebase and Conflict Rules

```bash
# Update feature branch
git fetch origin
git rebase origin/<integration>

# Resolve conflicts, then:
git add <resolved-files>
git rebase --continue

# Never git rebase --skip unless the commit is genuinely empty
# Never force-push to production or the integration branch
# Force-push to your own feature branch is fine
git push --force-with-lease origin feat/wallet-archiving
```

Use `--force-with-lease` instead of `--force` — it refuses the push if someone else has pushed to the branch since your last fetch.

---

## What to Avoid

- **Any branch beyond `main` and the integration branch outliving its merge** — this is the rule
  the whole model rests on
- Merging into `main`, pushing to `main`, or opening an integration → `main` PR unasked
- Branching off production instead of the integration branch
- Merge commits — rebase, then fast-forward
- Opening a pull request for feature work
- Vague commit messages (`fix stuff`, `wip`, `update`)
- Bundling unrelated changes in one commit
- Leaving dead code, commented blocks, or TODO comments in merged work
- `--force` push without `--lease` on any shared branch
- Squashing commits that should be individually bisectable
