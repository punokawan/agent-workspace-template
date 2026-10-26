---
name: dart-style
description: Studio Dart style — naming, file layout, immutability, null-safety, freezed and sealed-class usage, Equatable events and states. Project naming tables and model shapes live in the <project>-app-patterns overlay.
license: Proprietary
compatibility: Flutter/Dart with freezed, equatable
---

# Dart Style (studio)

## Source of truth

Read, in this order: `projects/<project>/AGENTS.md`; `projects/<project>/<repo>/AGENTS.md` if it
exists; `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and
`projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md`, each only if it exists; then the nearest file
of the same kind. They win over this file. For example, a project's class-suffix table and
one-class-per-folder layout are in `example-app-patterns/references/style-and-lint.md`.

## Naming

### Files
- `snake_case.dart`; one primary type per file (one class or one enum — never mixed).
- `part` files match their owner (`invoice_list_event.dart` is `part of 'invoice_list_bloc.dart'`).
- Generated `*.g.dart` / `*.freezed.dart` sit beside their source, never in a `generated/` folder.
- Enums get their own file; group them where the project groups them.

### Classes
| Type | Convention | Example |
|---|---|---|
| Domain entity | PascalCase, no suffix | `Invoice`, `Member` |
| DTO | project suffix (`*Dto`, `*Response`, `*DB`) | `InvoiceDto` |
| Mapper | `*Mapper`, static-only | `InvoiceMapper` |
| Repository interface / impl | `*Repository` / `*RepositoryImpl` | `InvoiceRepositoryImpl` |
| Datasource | `*LocalDatasource` / `*RemoteDatasource` | `InvoiceRemoteDatasource` |
| Use case + param | `*UseCase` + `*Param` | `PayInvoiceUseCase`, `PayInvoiceParam` |
| BLoC | `<Feature><Operation>Bloc` | `InvoicePayBloc` |
| Event | action verb, no suffix | `PayInvoice`, `LoadInvoices` |
| State | BLoC prefix + noun | `InvoicePayLoading`, `InvoicePaySuccess` |

### Variables, fields, methods
- `camelCase`; private fields prefixed `_`: `final InvoiceRepository _repository;`
- Booleans: `is*`, `has*`, `can*`, `should*`.
- Collections: plural nouns (`invoices`, not `invoiceList`).
- Methods verb-first (`save`, `load`, `findById`); BLoC handlers `_on{EventName}`; mapper statics
  `{source}To{target}` or `toEntity`/`toDto` — match the project.

## Immutability

Domain and presentation data is immutable. Change with `copyWith`, never mutation.

```dart
@freezed
abstract class Invoice with _$Invoice {
  const factory Invoice({required String id, required int amountMinor, required InvoiceStatus status}) = _Invoice;
}
final paid = invoice.copyWith(status: InvoiceStatus.paid);
```

BLoC events and states are `sealed class` + `Equatable` with `const` constructors and `final`
fields. Never a mutable field in an event or state.

## Null safety

- Prefer non-nullable when the value is always present — a success state carries a non-null
  payload.
- Entity nullability follows the project: some keep all-nullable entities for partially populated
  sync data. Do not change the convention in a local edit.
- Prefer `??` for defaults and `?.` for navigation.

```dart
class InvoicePaySuccess extends InvoicePayState {
  const InvoicePaySuccess(this.invoice);
  final Invoice invoice;  // non-null: it just succeeded
  @override
  List<Object?> get props => [invoice];
}
```

## freezed

- Domain entity: `@freezed`, no `fromJson`, no database annotations, no Flutter import.
- DTO: `@freezed` + `fromJson` (or the project's JSON reader); wire-format dates as strings.
- Local-database rows follow the database package (e.g. ObjectBox `@Entity` classes are mutable and
  not freezed).

## sealed classes

Use `sealed` for BLoC events and states (exhaustive `switch`), for `Result`/`Failure` hierarchies,
and — where the project does — for datasource interfaces. Static-only namespaces (mappers, rule
engines) are `abstract final class` or `sealed class`, per the project.

## Equatable

Every event and state subclass implements `props` with **all** fields. A missing field makes two
different values compare equal and breaks `blocTest` expectations.

## Avoid

- `dynamic` — use `Object?` or a real type.
- `var` for class fields — declare types.
- `print()` — use the project logger.
- `assert()` as production validation — validate at boundaries.
- `late` on nullable fields — use `?`.
- `!` without a null check in the same scope.
- `as` without a prior `is` — prefer pattern matching.
