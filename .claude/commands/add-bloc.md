---
description: Add a single BLoC triplet (bloc + event + state) to an existing feature in a project's Flutter app. Use when a new operation is needed without scaffolding the full feature stack.
argument-hint: [<project>/app] <feature> <operation> [use_case:UseCaseName] [input:field:Type] [output:Type]  e.g. "wallet transfer use_case:TransferWalletUseCase input:fromId:String input:toId:String input:amount:double output:bool"
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <project>/<repo> <type>/<slug>` first. Never edit a checkout under
   `projects/<project>/<repo>/` directly — those are the user's working checkouts.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log add-bloc "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# Add BLoC

You are adding a single BLoC to an existing feature in the target project's Flutter app.

## Input
`$ARGUMENTS`

## Target

`$ARGUMENTS` may start with a `<project>/app` target (e.g. `example/app`). If it does not, use the
active project (marked `*` in `bash .claude/scripts/project.sh list`) and its `flutter` repo from
`bash .claude/scripts/project.sh show <project>`; if it has none, stop and say so. Then read
`projects/<project>/AGENTS.md`, `projects/<project>/app/AGENTS.md` if present, and — only if they
exist — `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and `projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md`.
Paths, imports, DI calls, and naming below are examples; the project's sources win.

---

## Step 1 — Parse & clarify

Extract from `$ARGUMENTS`:
- **Feature**: snake_case feature name (e.g., `wallet`, `transaction`, `tag`)
- **Operation**: snake_case operation name (e.g., `add_local`, `update_local`, `delete_local`, `list`, `transfer`, `export`)
- **use_case**: the use case class name this BLoC delegates to (e.g., `TransferWalletUseCase`)
- **input fields**: each `input:fieldName:DartType` — these become event fields
- **output**: the success data type (e.g., `Wallet`, `bool`, `List<Transaction>`)

If anything is missing or ambiguous, ask before proceeding:
- Missing operation: "What operation does this BLoC handle?"
- Missing use_case: "Which use case does this BLoC delegate to? (or is it a Cubit with no use case?)"
- Missing output: "What does success return? (entity type, bool, void, etc.)"

---

## Step 2 — Confirm

Show a brief plan:
```
BLoC: {Feature}{Operation}Bloc
Location: <the project's BLoC folder>/{feature}/{operation}/
Files: <the project's BLoC file names>

Operation type: [add_local | update_local | delete_local | list | custom]
Event: {Action}  →  inputs: {field list}
Success output: {OutputType}
Delegates to: {UseCaseName}
```

Ask: `Proceed?`

---

## Step 3 — Detect operation type

Map the operation to the nearest existing BLoC of the same kind in the repo and copy its pattern.
An example mapping (other projects name their operations differently):

| Operation contains | Pattern to use |
|---|---|
| `add_local` or `add` | add_local pattern (UUID + timestamps, sended:false) |
| `update_local` or `update` | update_local pattern (updatedAt: now, carry storageId) |
| `delete_local` or `remove` | delete_local pattern (input: storageId:int, output: bool) |
| `list` or `load` | list pattern (load + in-memory CRUD events) |
| `upsert_remote` | remote upsert (fire-and-forget, delegates to remote repo) |
| `delete_remote` | remote delete (fire-and-forget) |
| anything else | generic async pattern |

---

## Step 4 — Delegate to senior-mobile-engineer

Use the `senior-mobile-engineer` agent (`.claude/agents/senior-mobile-engineer.md`) with the `<project>/app` target and worktree.

Pass:
- Feature name, operation name, operation type
- Input fields and output type
- Use case name and its param class name (infer as `{UseCase}Param` if not specified)
- Whether UUID injection is needed (only for add_local)
- Whether this is app-global (registered in the app-level provider list) or screen-local (`BlocProvider` in the screen)

---

## Step 5 — Write files

Write the BLoC, event, and state files at the project's BLoC path, using its file-naming convention
(for example: `lib/presentations/blocs/{feature}/{operation}/bloc.dart`, `event.dart`, `state.dart`).

---

## Step 6 — Show integration steps

After writing, output what the user needs to wire up, using the project's DI and provider files
(for example, below: `ExampleInjector`, `lib/providers.dart`, `lib/config/injector/injector.dart`):

**Option A — Screen-local BLoC** (most common for add/update/delete):
```dart
// In your screen.dart:
BlocProvider(
  create: (_) => {Feature}{Operation}Bloc(
    ExampleInjector.find(),  // Uuid (if add_local)
    ExampleInjector.find(),  // UseCase
  ),
),
```

**Option B — App-global BLoC** (for list / remote sync):
In `lib/providers.dart`, add to `AppProvider._providers`:
```dart
BlocProvider(
  create: (_) => {Feature}{Operation}Bloc(ExampleInjector.find()),
),
```

**`lib/config/injector/injector.dart`** — only if app-global:
```dart
_container.registerLazySingleton(() => {Feature}{Operation}Bloc(find(), find()));
```

**Usage in content.dart**:
```dart
// Trigger
context.read<{Feature}{Operation}Bloc>().add(const {Action}Event(...));

// Listen
BlocListener<{Feature}{Operation}Bloc, {Feature}{Operation}State>(
  listener: (context, state) {
    if (state is {Feature}{Operation}Success) { ... }
    if (state is {Feature}{Operation}Error) { ... }
  },
),
```

---

## Rules
- All code complete — no `// TODO` or `// ...`
- Use the app's `package:<app>/` imports
- Events and states use `sealed class` + `Equatable`
- Async handlers always guarded: `if (state is ...Loading) return;`
- Never resolve from the DI container inside the BLoC body
