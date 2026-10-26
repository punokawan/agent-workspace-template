---
description: Add a single use case to an existing feature in a project's Flutter app — creates the use case class, param class, and shows where to register it in DI.
argument-hint: [<project>/app] <feature> <operation> [return_type:Type] [param:field:Type ...]  e.g. "wallet transfer return_type:bool param:fromStorageId:int param:toStorageId:int param:amount:double"
---

## Harness (applies before anything below)

1. **Work in a worktree.** This command writes repo source. If no worktree is bound to the current
   run, stop and run `/wt-start <project>/<repo> <type>/<slug>` first. Never edit a checkout under
   `projects/<project>/<repo>/` directly — those are the user's working checkouts.
2. **Load** `verification` and `worktree-workflow` before writing code.
3. **Gate before reporting done:**
   `bash .claude/scripts/verify.sh wt:<project>/<repo>/<slug> --full`
   Exit non-zero → not done. Report the real failures; mark pre-existing ones as such.
4. **Record:** `bash .claude/scripts/state.sh log add-usecase "<what changed>"`.
5. Cite `path:line` for every claim about existing code. Never invent a symbol, path, or version —
   grep for it or write `unverified`.

---

# Add Use Case

You are adding a single use case to an existing feature.

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

## Step 1 — Parse

Extract:
- **Feature**: snake_case (e.g., `wallet`, `transaction`)
- **Operation**: snake_case verb (e.g., `transfer`, `export`, `archive`)
- **return_type**: Dart type the use case returns (default: entity name in PascalCase)
- **param fields**: each `param:field:Type` pair

If missing, ask before proceeding.

---

## Step 2 — Generate

Create the use case in the project's use-case folder, named like its neighbours. For example,
`lib/domain/usecases/{feature}/{operation}_{feature}_usecase.dart`:

```dart
import 'package:example/commons/commons.dart';
import 'package:example/domain/domains.dart';

class {Operation}{Feature}UseCase extends UseCase<{ReturnType}, {Operation}{Feature}Param> {
  {Operation}{Feature}UseCase(this._{feature}Repository);
  final {Feature}Repository _{feature}Repository;

  @override
  Future<Result<{ReturnType}>> call({Operation}{Feature}Param params) {
    return _{feature}Repository.{operation}(/* params */);
  }
}

class {Operation}{Feature}Param {
  const {Operation}{Feature}Param({
    required this.field1,
    required this.field2,
  });
  final Type1 field1;
  final Type2 field2;
}
```

Rules:
- Use the project's `NoParams` if no params needed
- Return type is always wrapped: `UseCase<{ReturnType}, {Param}>`
- Use case body is a single `return` — delegate only, no logic

---

## Step 3 — Check if repository method exists

Read the feature's domain repository interface (example: `lib/domain/repositories/local/{feature}_repository.dart`).

If the method called in the use case doesn't exist in the interface:
- Show the method signature to add
- Show the corresponding implementation to add in the repository impl (example: `lib/data/repositories/local/{feature}_repository.dart`)

---

## Step 4 — DI registration

Show the exact line to add in the project's DI file, use-case section (example: `lib/config/injector/injector.dart`):

```dart
_container.registerLazySingleton(() => {Operation}{Feature}UseCase(find()));
```

---

## Step 5 — Architecture check

Verify:
- Use case file is in `domain/` — not `data/` or `presentations/`
- Imports only the app's shared core and domain packages (example: `commons/` and `domain/`)
- Returns `Future<Result<T>>`
- No business logic beyond delegation

Flag any issue immediately.
