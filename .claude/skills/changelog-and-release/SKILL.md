---
name: changelog-and-release
description: How every project manages versioning, changelogs, and releases — the generated Keep a Changelog format via changelog.sh, semver+buildNumber in pubspec.yaml, per-repo release scripts, commit conventions (commit subjects become changelog entries), and the tagging hand-off. Load before cutting a release, writing a changelog entry, or bumping a version.
license: Proprietary
compatibility: scripts/release.sh, pubspec.yaml, CHANGELOG.md, git tags
---

# Changelog and Release

## Version Format

Flutter repos use `semver+buildNumber` in `pubspec.yaml`:

```yaml
version: 1.9.1+42
#        ^ ^ ^  ^
#        | | |  └── buildNumber (auto-incremented, always goes up)
#        | | └───── patch (bug fixes, minor improvements)
#        | └─────── minor (new features, non-breaking changes)
#        └───────── major (breaking changes, large rewrites)
```

**Never** manually edit the version field for a release when the repo has `scripts/release.sh` — use it.

---

## Scope — which repo

Release scripts are per repo. Before releasing `<project>/<repo>`, read, in order:
1. `bash .claude/scripts/project.sh show <project>` — branches and deploy target
2. `projects/<project>/AGENTS.md` and `projects/<project>/<repo>/AGENTS.md` if present
3. `projects/<project>/**/.claude/skills/<project>-release/SKILL.md`, only if it exists (e.g. `example-release`
   documents `example/app`'s `scripts/release.sh`, AAB build, hotfix, and checklist)
4. the repo's own `scripts/release.sh` if present — read it; do not assume what it does

A repo with no release script is released by cutting the changelog (`changelog.sh release`)
and tagging manually — see `git-workflow` → *Release Hand-off*. Hotfixes follow
`git-workflow` → *Hotfix Flow*, then release as a `patch`.

Tagging, pushing a tag, and deploying are outward-facing and hard to reverse: show the command,
get explicit confirmation in the same session, then run it.

---

## CHANGELOG.md — generated, never hand-written

Every repo has a `CHANGELOG.md` in
[Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/) format. **Never edit one by hand** —
entries are generated from conventional commit subjects:

```bash
C=.claude/scripts/changelog.sh

bash $C preview   <repo> <range>        # inspect, write nothing
bash $C add       <repo> <slug>         # fold a worktree branch into [Unreleased]
bash $C add-range <repo> v1.1.0..HEAD   # fold a commit range in the main checkout
bash $C release   <repo> 1.2.0          # cut [Unreleased] into a dated version section
bash $C init      <repo>                # create the file
```

`add` is idempotent — re-running never duplicates an entry.

### Commit type → changelog section

| Commit type | Section |
|---|---|
| `feat` | Added |
| `fix`, `hotfix` | Fixed |
| `perf`, `refactor`, `style` | Changed |
| `revert` | Removed |
| `docs` | Documentation |
| `chore`, `config`, `build`, `ci` | Maintenance |

A commit whose subject is not `<type>(<scope>): <description>` is **silently skipped** and never
reaches the changelog. This is the single strongest reason to write conventional subjects: a
commit written as `fixed bug` is invisible to users forever.

Scoped commits render with the scope in bold: `feat(wallet): add archiving` →
`- **wallet:** add archiving`.

### Resulting shape

```markdown
## [Unreleased]

## [1.1.0] - 2026-06-12

### Added

- **wallet:** add archive and restore
- **transaction_upsert:** add transfer feature

### Fixed

- **sync:** prevent duplicate transactions after offline reconnect
```


---

## Commit Message Conventions

Since `git log --pretty=format:"- %s"` maps each commit subject line to a changelog entry, the subject line IS the user-facing changelog entry. Write it accordingly.

### Format

```
<type>: <imperative short summary>
```

| Type | When to use |
|---|---|
| `feat` | New feature, new screen, new capability |
| `fix` | Bug fix |
| `refactor` | Code restructuring with no behavior change |
| `perf` | Performance improvement |
| `test` | Test additions or fixes |
| `chore` | Dependency updates, tooling, config changes |
| `config` | Version bumps, environment changes |
| `docs` | Documentation only |
| `style` | Formatting, linting, no logic change |

### Good vs Bad commit messages

```
# ✅ Clear to users in a changelog
feat: add wallet archiving with restore option
fix: transaction amount shows zero after offline sync
perf: reduce transaction screen rebuild count by 40%
refactor: migrate wallet BLoC to Result<T> error handling

# ❌ Confuse users or reveal internal details
wip: half done
fix stuff
update code
refactor(wallet): extract _buildBody method into _WalletContent widget
chore: run dart format
```

**Every commit landed since the last tag will appear in the next CHANGELOG.md.** Treat the subject line as user-facing documentation.

---

## Choosing the Bump Type

| Change | Bump type |
|---|---|
| New feature added | `minor` |
| Bug fix only | `patch` |
| Breaking change, major redesign | `major` |
| Dependency update only | `patch` |
| Performance improvement | `patch` |
| Multiple new features in one release | `minor` |

When unsure: `patch` for fixes, `minor` for features. `major` is reserved for app-level breaking changes (auth system rewrite, new onboarding flow, etc.) — not just large refactors.
