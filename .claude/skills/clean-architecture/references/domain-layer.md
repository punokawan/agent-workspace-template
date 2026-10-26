# Domain Layer

Project-specific layouts (barrels, enum folders, local/remote split) live in
`projects/<project>/**/.claude/skills/<project>-app-patterns/` when it exists.

## Responsibilities

- Business entities and value objects.
- Repository contracts.
- Use cases — one per operation.
- Domain services — pure business logic with no I/O (rule engines, scoring, projections).
- Framework-agnostic code only.

## Rules

- Entities are immutable; changes go through `copyWith`.
- Entities have no `fromJson`/`toJson`, database annotations, API field names, Dio/Firebase imports,
  or UI imports.
- Use cases implement the project's `UseCase<ReturnType, ParamsType>` and return `Result<T>`
  (or a `Stream<Result<T>>` for watches).
- Use cases delegate to repository contracts; any validation or branching they hold is intentional
  and unit-tested.
- Params classes live in the same file as the use case.
- Enums live in their own files, not inline in an entity file.
- A `repositories/` folder holds repository interfaces only — no helpers, DTOs, or rule engines.
  Logic goes to a domain service.

## Domain service pattern

```dart
abstract final class LateFeeRules {
  static int feeFor(Invoice invoice, DateTime today) {
    // pure computation — no await, no repository calls
  }
}
```

Called by a use case or a repository impl that already holds the inputs.

## Critical violations

- Domain imports `data/`, `presentations/`, or the DI/wiring module.
- Entity exposes JSON or database concerns.
- Use case talks to datasources, storage, network clients, or a service locator.
- Use case returns raw data instead of `Result<T>`.
- Helper, DTO, or rule engine placed in `repositories/`.
