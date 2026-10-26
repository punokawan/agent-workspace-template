---
name: verification
description: Anti-hallucination protocol for all work in every project — evidence grades, the mandatory verification gate before claiming anything is done, and the exact vocabulary for stating uncertainty. Load this before reporting completion, before making any factual claim about the codebase, and before any agent hands off to another.
license: Proprietary
compatibility: bash, fvm, go, npm
---

# Verification — the anti-hallucination gate

The failure mode this prevents: an agent reads three files, infers a fourth, and reports
"implemented and tested" when nothing was run. Everything below exists to make that
impossible to do silently.

## Evidence grades

Every factual claim carries one of these. **State the grade whenever it is not A.**

| Grade | Means | Example |
|---|---|---|
| **A — Executed** | A command ran; you are quoting its real output and exit code | `go vet ./...` exited 1: `middleware.go:132 context leak` |
| **B — Read** | You opened the file and are citing `path:line` | `injector.dart:397` registers `TransactionBloc` |
| **C — Inferred** | Follows from A/B evidence but was not directly observed | "so the DI graph is complete" |
| **D — Assumed** | Not grounded in this repo at all | "the API probably returns 404 here" |

Rules:
- **A and B need a citation.** A `path:line` or the command + exit code. No citation → it is not A or B.
- **C must show its inputs.** "Inferred from `x.dart:12` + `y.go:88`".
- **D must be written `ASSUMPTION: …`** — that exact word. Never let a D-grade claim wear
  a declarative sentence.
- Unknown and uncheckable → write **`unverified`**. Never fill the gap with a plausible guess.
- **Never invent** file paths, function names, package names, versions, CVE IDs, config keys,
  or line numbers. If you need one and don't have it, grep for it or say `unverified`.

## The gate — mandatory before claiming "done"

No agent may report work complete without a Grade-A run:

```bash
V=.claude/scripts/verify.sh
bash $V <repo> --quick     # static: format, analyze/vet/typecheck, lint
bash $V <repo> --full      # adds tests / build. NOT parallel-safe (shared cache)
bash $V all --full         # everything
```

Use a narrow loop while developing: run the affected test directly, then `--quick`; run `--full`
once at the feature or commit boundary. `verify.sh` keeps complete output in its temporary log and
writes a small durable result under `.claude/verify-results/`. Read the result first; open the full
log only for a failed check.

The gate refuses a duplicate run for the same target and mode. Defaults are 45 minutes total and
15 minutes without output; override them only for a known slower suite with
`STUDIO_VERIFY_TIMEOUT_SECONDS` and `STUDIO_VERIFY_STALL_SECONDS`.

Exit codes are the contract:

| Exit | Verdict | What you may say |
|---|---|---|
| `0` | PASSED | "Done — verified" + the checks that passed |
| `1` | FAILED | "Not done" + the real failure output. **Never** report success. |
| `2` | NO EVIDENCE | Nothing ran. You may not claim verification at all. |

**A pre-existing failure does not become your pass.** If `verify.sh` fails on something you
did not touch, say so explicitly and separately: "my change verifies; the repo also has 2
pre-existing failures: …". Do not silently absorb or silently ignore them.

## What each repo actually checks

Checks come from the repo's stack preset, `templates/stacks/<stack>.json` (`quick` and `full`).
Typical:

| Stack | quick | full adds |
|---|---|---|
| `flutter` | `dart format --set-exit-if-changed`, `fvm flutter analyze` | `fvm flutter test` |
| `go` | `go build ./...`, `go vet ./...`, `gofmt -l` | `go test ./...` |
| `nextjs` | `tsc --noEmit`, `next lint` | `next build` |

With no repo argument, `verify.sh` auto-detects repos that have uncommitted changes.

## Reporting format

```
VERIFICATION  <repo> --<mode>
  PASS  go: build
  FAIL  go: vet (exit 1) — pkg/middleware/middleware.go:132 context leak  [PRE-EXISTING]
VERDICT: FAILED
```

Then, separately: what *you* changed, and whether *your* change is implicated.

## Hard prohibitions

- Never write "tests pass" without an exit-0 test run in this session.
- Never write "should work", "this will fix it", or "I've verified" as a substitute for running it.
- Never report a summary of what an agent *said* it did as if you confirmed it — for code
  changes, read the diff (`git diff`) before relaying the claim.
- Never quote a metric (file count, size, coverage, timing) you did not measure this session.
- If the toolchain is missing (`fvm`, `go`, `npm` not found), report `unverified — toolchain
  unavailable`. Do not simulate the result.
