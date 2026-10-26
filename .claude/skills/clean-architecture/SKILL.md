---
name: clean-architecture
description: Studio Flutter Clean Architecture rules — layer boundaries, dependency direction, what belongs where, and the pattern each layer follows (entities, repositories, use cases, DTOs, mappers, datasources, BLoCs, DI). Load for any implementation, review, or refactor of Flutter/Dart app code in any project.
license: Proprietary
compatibility: Flutter/Dart with flutter_bloc, get_it, equatable, a project Result<T> type
---

# Clean Architecture (studio Flutter house style)

Shared by every Flutter app in the studio. Exact folder
names, the `Result` API, the failure type, DI and storage differ per project — the overlay says which.

## Source of truth

Before writing or reviewing code, read, in this order:
1. `projects/<project>/AGENTS.md` — vocabulary, layering rules, known defects
2. `projects/<project>/<repo>/AGENTS.md` if it exists
3. `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and `projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md`, each only if it exists
4. The nearest existing file of the same kind in the same feature

Where these disagree with this file, they win.

## Layer map

```
Presentation  lib/presentations/   BLoCs, screens, widgets
      ↓ depends on
Domain        lib/domain/          entities, repository interfaces, use cases, pure services
      ↑ implemented by
Data          lib/data/            DTOs, mappers, datasources (local + remote), repository impls

Core          lib/core/            DI, routing, theme, failures, Result, extensions (wires everything)
```

Dependencies point inward only. Domain knows nothing of data or presentation. Data knows domain
contracts. The DI/wiring module is the only place allowed to import broadly. (One project splits core
into `config/` + `commons/`.)

## Boundary rules (violation = Critical)

| Layer | May import |
|---|---|
| Domain | domain, the shared `Result`/`Failure`/`UseCase` primitives, pure Dart packages |
| Data | domain, shared primitives, data itself |
| Presentation | domain, shared primitives, routing/theme, presentation itself |
| Core / wiring | everything (DI only) |

**Domain never imports:** `package:flutter/` (except `foundation.dart` for `@immutable`), Dio or any
HTTP client, the local database package, Firebase, anything under `data/` or `presentations/`.

**BLoCs never import:** HTTP clients, database packages, datasources, or DTOs.

## Domain

- **Entities** — immutable (`freezed` or hand-written `==`/`copyWith`), no JSON, no database
  annotations, no API field names.
- **Repository interfaces** — abstract; every method returns `Future<Result<T>>` (or
  `Stream<Result<T>>`) of domain types. Never throw for an expected failure.
- **Use cases** — one class per operation, extending the project's `UseCase<T, P>`; return
  `Result<T>`; delegate to repository contracts. Param class lives in the same file; `NoParams` when
  none.
- **Domain services** — pure logic with no I/O (rule engines, scoring) when too large for a use case.

```dart
class SaveInvoiceUseCase implements UseCase<Invoice, SaveInvoiceParam> {
  SaveInvoiceUseCase(this._repository);
  final InvoiceRepository _repository;

  @override
  Future<Result<Invoice>> call(SaveInvoiceParam params) => _repository.save(params.invoice);
}

class SaveInvoiceParam {
  const SaveInvoiceParam({required this.invoice});
  final Invoice invoice;
}
```

## Data

- **DTOs** — wire and storage shapes (`fromJson`, database annotations). Dates stay as strings or
  primitives until the mapper converts them.
- **Mappers** — the only place a DTO becomes an entity and back. Pure, static, tested.
- **Datasources** — perform I/O (HTTP, local database) and return DTOs, never entities. Split
  `local/` and `remote/`.
- **Repository impls** — call datasources, map through mappers, catch every exception and return
  a failure `Result`. A raw platform or Dio error never reaches presentation.

```dart
@override
Future<Result<Invoice>> save(Invoice invoice) async {
  try {
    final dto = await _remote.save(InvoiceMapper.toDto(invoice));
    return Result.success(InvoiceMapper.toEntity(dto));   // use the project's Result constructors
  } catch (e, s) {
    return Result.failure(Failure.fromException(e, s));
  }
}
```

## Presentation

- **One BLoC per operation, not per screen** (`InvoiceListBloc`, `InvoicePayBloc`); a screen
  composes several.
- Events and states: `sealed class` + `Equatable`, immutable, `props` lists every field.
- Every async handler: loading guard (`if (state is XLoading) return;`) where double-submit or
  duplicate fetch is possible, then `try/catch`, then emit success or error from the `Result`.
- Dependencies arrive by constructor. No service-locator lookups inside a BLoC.
- A widget never touches a repository or datasource; state reaches it from a BLoC.

```dart
Future<void> _onPay(PayInvoice event, Emitter<InvoicePayState> emit) async {
  if (state is InvoicePayLoading) return;
  emit(const InvoicePayLoading());
  try {
    final result = await _payInvoice(PayInvoiceParam(id: event.id));
    // map with the project's Result API (fold / when / switch on variants)
    result.fold((invoice) => emit(InvoicePaySuccess(invoice)), (f) => emit(InvoicePayError(f)));
  } catch (e, s) {
    emit(InvoicePayError(Failure.fromException(e, s)));
  }
}
```

## DI

Register in dependency order: config/env → logging → network → storage → datasources →
repositories → use cases → global BLoCs. Lazy singletons by default. Screen-scoped BLoCs are created
in the screen's `BlocProvider`, which is the DI boundary for presentation.

## References

- `references/domain-layer.md`
- `references/data-layer.md`
- `references/presentation-layer.md`
- `references/testing.md`
- Project overlay, e.g. `projects/example/.claude/skills/example-app-patterns/references/architecture.md` (an example)
