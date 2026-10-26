# Data Layer

Project-specific model folders, database, and mapper shapes live in
`projects/<project>/**/.claude/skills/<project>-app-patterns/` when it exists.

## Responsibilities

- API communication and local persistence, through datasources.
- DTOs for wire and storage shapes.
- Mapping DTOs to and from domain entities.
- Repository implementations and error mapping.

## Rules

- DTOs carry `fromJson`/`toJson` or database annotations; entities never do.
- Date fields in DTOs stay in their wire form (RFC 3339 strings, epoch ints); the mapper converts.
- Datasources do I/O and return DTOs, never entities. Keep `local/` and `remote/` apart.
- Repository impls catch every exception and return the project's failure `Result`.
- Mappers are the only place DTO ↔ entity conversion happens. They are pure and tested; a malformed
  payload becomes a failure `Result`, not a throw past the repository.
- Generated files (`*.g.dart`, `*.freezed.dart`) sit beside their source.
- Feature-scoped helper types live next to the repository impl that owns them, not in a shared root.

## Repository pattern

```dart
class InvoiceRepositoryImpl implements InvoiceRepository {
  InvoiceRepositoryImpl(this._remote);
  final InvoiceRemoteDatasource _remote;

  @override
  Future<Result<List<Invoice>>> load() async {
    try {
      final dtos = await _remote.load();
      return Result.success(dtos.map(InvoiceMapper.toEntity).toList());
    } catch (e, s) {
      return Result.failure(Failure.fromException(e, s));
    }
  }
}
```

## Critical violations

- DTO or datasource imported into presentation.
- Repository leaks an uncaught exception.
- Repository builds complex entities by hand when a mapper exists.
- Datasource returns domain entities.
- Database box/query code outside data/storage infrastructure.
- Local and remote impls mixed when the project splits them.
