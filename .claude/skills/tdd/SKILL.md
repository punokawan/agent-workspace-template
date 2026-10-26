---
name: tdd
description: Test-Driven Development for Flutter/BLoC Clean Architecture apps — the TDD cycle, bloc_test patterns, mocking, what to test and why, test layout, and coverage targets per layer. Project facts (mock library, test paths, fixtures, run command) live in the project's app overlay.
license: Proprietary
compatibility: Flutter/Dart with bloc_test, flutter_test, mocktail or mockito
---

# TDD (Flutter + BLoC)

## Source of truth

Before writing tests, read in this order:
1. `projects/<project>/AGENTS.md`, then `projects/<project>/<repo>/AGENTS.md` if it exists
2. `projects/<project>/**/.claude/skills/<project>-app-patterns/references/testing.md` only if it exists — mock library,
   test paths, fixtures, run command, project invariants (example: `example-app-patterns`)
3. One existing test in the same area — match its style and fixtures

Local sources win over this file. Studio default is **mocktail**; some projects use **mockito**
(`@GenerateMocks` + build_runner). Use whatever the repo's `pubspec.yaml` declares.

---

## The TDD cycle

Red → Green → Refactor:

1. **Red**: write a failing test that describes the desired behaviour
2. **Green**: write the minimum implementation that passes
3. **Refactor**: extract, rename, simplify — re-run to stay green

For BLoC work, write the event → state expectation first, then the handler. For use cases, the
delegation assertion first. For mappers, the field-by-field assertion first.

---

## Test layout

Mirror `lib/` under `test/`, one folder per layer: use cases, repositories, mappers, BLoCs, and
(rarely) widgets. Follow the repo's existing layout — the overlay names it when it differs.

---

## BLoC tests (bloc_test) — highest priority

Every async event handler needs: **success** (`[Loading, Success]`), **failure**
(`[Loading, Error]`), and **guard** (nothing emitted when already Loading).

```dart
class MockSaveOrderUseCase extends Mock implements SaveOrderUseCase {}

void main() {
  late MockSaveOrderUseCase useCase;
  final order = Order(id: 'o1', name: 'Test');

  setUpAll(() => registerFallbackValue(SaveOrderParam(order: order)));
  setUp(() => useCase = MockSaveOrderUseCase());

  blocTest<OrderSaveBloc, OrderSaveState>(
    'emits [Loading, Success] when save succeeds',
    build: () {
      when(() => useCase.call(any())).thenAnswer((_) async => Result.success(order));
      return OrderSaveBloc(useCase);
    },
    act: (b) => b.add(SaveOrder(order: order)),
    expect: () => [isA<OrderSaveLoading>(), isA<OrderSaveSuccess>()],
  );

  blocTest<OrderSaveBloc, OrderSaveState>(
    'does not emit when already Loading',
    build: () => OrderSaveBloc(useCase),
    seed: () => const OrderSaveLoading(),
    act: (b) => b.add(SaveOrder(order: order)),
    expect: () => [],
  );
}
```

The failure case is the same with the use case answering a failure result and `isA<...Error>()`.
`blocTest` closes the BLoC itself; a BLoC built in `setUp` needs `tearDown(() => bloc.close())`.

| Parameter | Purpose |
|---|---|
| `build` | construct the BLoC with mocked deps |
| `seed` | initial state before `act` |
| `act` | dispatch events |
| `expect` | ordered emitted states |
| `verify` | side-effect assertions after `act` |
| `errors` | the BLoC threw — rare; prefer an error state |

---

## Use case tests

Use cases are thin delegation wrappers: assert the repository was called with the right argument
**and** the result is propagated, for success and for failure.

## Mapper tests

Pure functions — no mocks, no async. Assert every field, the storage round-trip
(entity → storage → entity), and a maximally sparse input (only required fields) that must not crash.

## Repository tests

Mock the datasource. Assert the happy path maps correctly, and that a throwing datasource yields a
failure result — never a rethrow.

---

## Coverage targets

| Layer | What to cover |
|---|---|
| **BLoC** | Every handler: success + failure + guard (where applicable) |
| **UseCase** | Delegation + error propagation |
| **Mapper** | All fields + round-trip + null safety |
| **Repository impl** | Happy path + exception → failure |
| **Datasource** | Skip unless it has non-trivial filtering |
| **Widget** | Only complex stateful widgets with business-adjacent behaviour |

## What not to test

- Private methods and internal variables
- `verify(...).called(1)` alone — always also assert the result
- Generated code (`*.freezed.dart`, `*.g.dart`)
- Navigation — integration territory
- Third-party SDK internals (Firebase, payments, local DB) — mock at the datasource boundary

---

## Test data

Define fakes at the top of the test file or in a shared fixtures helper; give them obviously fake
IDs (`'test-order-id'`) and fixed dates (`DateTime(2024, 1, 1)`), never `DateTime.now()`.

---

## TDD in practice: a new BLoC event

1. Write the test — which states should be emitted?
2. Run → fails (Red)
3. Add the event class
4. Add the minimal handler
5. Run → passes (Green)
6. Refactor if needed — re-run to confirm still Green
