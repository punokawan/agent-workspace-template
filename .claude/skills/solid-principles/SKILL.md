---
name: solid-principles
description: SOLID principles applied to studio Flutter/Dart apps (Clean Architecture + BLoC) — a violation and fix for each principle, common anti-patterns, and a review quick-check.
license: Proprietary
compatibility: Flutter/Dart with freezed, flutter_bloc, get_it
---

# SOLID Principles (studio Flutter)

Every principle below has a concrete Clean Architecture + BLoC violation and its fix. Examples use
neutral names; use the project's own `Result` API and failure type.

Source of truth: `projects/<project>/AGENTS.md`, then `projects/<project>/<repo>/AGENTS.md` if it
exists, then `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and
`projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md` if they exist. They win over this file.

---

## S — Single Responsibility Principle

**A class should have one reason to change.**

### In practice

Each layer artifact has exactly one job:
- **Entity**: represent a domain concept, nothing else
- **UseCase**: orchestrate one operation, nothing else
- **Repository impl**: translate domain calls to storage/network, nothing else
- **BLoC**: manage state for one user operation, nothing else
- **Mapper**: convert between representations, nothing else
- **Datasource**: execute raw IO, nothing else

### Violations to catch

```dart
// ❌ BLoC doing mapping AND business logic AND network calls
class InvoiceAddBloc extends Bloc<...> {
  Future<void> _onAdd(AddInvoice event, Emitter emit) async {
    final db = InvoiceDto(  // mapping belongs in mapper
      id: const Uuid().v4(),
      amount: event.amount,
      ...
    );
    await _storage.write(db);  // direct storage access belongs in datasource
    final response = await _dio.post('/invoices', data: {...});  // network in BLoC
  }
}

// ✅ Each class does one thing
class InvoiceAddLocalBloc extends Bloc<...> {
  Future<void> _onAdd(AddInvoiceLocally event, Emitter emit) async {
    final result = await _saveUseCase.call(SaveInvoiceParam(
      invoice: Invoice(id: _uuid.v4(), amount: event.amount, ...),
    ));
    result.fold(...);  // project Result API
  }
}
```

### Common SRP violations

- Repository impl doing data transformation instead of delegating to mapper
- UseCase containing conditional logic that belongs in the domain entity
- Widget `build()` computing filtered lists or formatting currency
- The DI module doing work beyond wiring (wiring itself importing everything is fine)

---

## O — Open/Closed Principle

**Open for extension, closed for modification.**

### In practice

Use abstractions (repository interfaces, use case base class, sealed classes) so new behavior is added by extension, not by editing existing code.

### Violations to catch

```dart
// ❌ Adding a new payment method requires modifying existing switch
Future<Result<bool>> processPayment(PaymentMethod method) async {
  if (method == PaymentMethod.applePay) { ... }
  else if (method == PaymentMethod.creditCard) { ... }
  // every new method requires editing this method
}

// ✅ Abstract the interface, add new implementations
abstract class PaymentProcessor {
  Future<Result<bool>> process(Invoice t);
}
class ApplePayProcessor implements PaymentProcessor { ... }
class CreditCardProcessor implements PaymentProcessor { ... }
// new method = new class, no existing code touched
```

### OCP with sealed classes + pattern matching

Studio BLoCs use sealed state/event classes. Adding a new state subclass is correct OCP — it extends behavior. But modifying `when`/`switch` exhaustively in every consumer is the cost.

Rule: add new states only when you own all consumers, or use a default branch (`maybeWhen`, `_ =>`) in consumers that don't need the new state.

---

## L — Liskov Substitution Principle

**Subtypes must be substitutable for their base types.**

### In practice

Repository implementations must fully honor their interfaces. A test mock must behave like the real repo from the BLoC's perspective.

### Violations to catch

```dart
// ❌ Implementation throws where interface says it returns Result
abstract class MemberRepository {
  Future<Result<List<Member>>> load();  // contract: never throws
}

class MemberRepositoryImpl extends MemberRepository {
  @override
  Future<Result<List<Member>>> load() async {
    return Result.success(await _datasource.load().map(...).toList());
    // ❌ missing try/catch — can throw, violates the contract
  }
}

// ✅ Implementation honors the contract
@override
Future<Result<List<Member>>> load() async {
  try {
    final dtos = await _datasource.load();
    return Result.success(dtos.map(MemberMapper.toEntity).toList());
  } catch (e, s) {
    return Result.failure(Failure.fromException(e, s));
  }
}
```

LSP is why every repository impl wraps in `try/catch` — it's not defensive programming, it's honoring the `Result<T>` contract.

---

## I — Interface Segregation Principle

**Clients should not depend on interfaces they don't use.**

### In practice

Datasource interfaces should be as narrow as the consumers need. Don't add `loadUnsynced()` to every datasource just because sync needs it somewhere.

```dart
// ❌ Fat interface — every consumer must implement methods they don't use
abstract class InvoiceDatasource {
  Future<List<InvoiceDto>> load();
  Future<List<InvoiceDto>> loadUnsynced();
  Future<List<InvoiceDto>> loadByDateRange(DateTime from, DateTime to);
  Future<List<InvoiceDto>> loadByMember(String memberId);
  Future<int?> save(InvoiceDto t);
  Future<bool> remove(int storageId);
  Future<void> clear();
  // ... 12 more methods
}

// ✅ Narrower contracts when possible — or accept the fat interface is OK
// for data layer where the impl always exists alongside the interface
```

In practice, a datasource whose impl always lives next to its interface may stay wide. The ISP concern rises when you're mocking for tests: if tests must stub 8 methods to test one BLoC, the interface is too fat.

---

## D — Dependency Inversion Principle

**High-level modules should not depend on low-level modules. Both should depend on abstractions.**

### In practice

This is the core of Clean Architecture. Domain is the high-level module. Data is low-level. Domain never imports data.

```dart
// ❌ Domain depending on data (concrete data class)
class LoadInvoicesUseCase {
  final InvoiceLocalDatasourceImpl _datasource;  // concrete data class
  // domain now knows about the database
}

// ✅ Domain depending on abstraction
class LoadInvoicesUseCase extends UseCase<List<Invoice>, NoParams> {
  final InvoiceRepository _repository;  // abstract interface defined in domain
}
```

### GetIt and DIP

The DI module (GetIt) is where DIP is satisfied at runtime. The constructor declares `InvoiceRepository` (abstraction); the injector wires `InvoiceRepositoryImpl` (concrete). The BLoC and use cases never know the concrete type.

### BLoC and DIP

```dart
// ❌ BLoC creating its own dependencies
class InvoiceAddLocalBloc extends Bloc<...> {
  final _useCase = SaveInvoiceUseCase(InvoiceRepositoryImpl(...)); // ❌
}

// ✅ BLoC receiving abstractions via constructor
class InvoiceAddLocalBloc extends Bloc<...> {
  InvoiceAddLocalBloc(this._useCase, this._uuid);
  final SaveInvoiceUseCase _useCase;
  final Uuid _uuid;
}
```

---

## SOLID Quick-Check for Code Reviews

When reviewing any new class, ask:
1. **S**: Could this class change for two different reasons? Split it.
2. **O**: Does adding a new variant require editing this class? Introduce an abstraction.
3. **L**: Does this implementation honor every constraint in its interface? Check `Result<T>` wrapping, null contracts.
4. **I**: Does a test mock require stubbing methods that aren't relevant to the test? Interface too fat.
5. **D**: Does this class import a concrete type it could receive as an abstraction? Invert it.
