---
name: test-case-design
description: How to derive test cases for Flutter/BLoC Clean Architecture code — equivalence partitioning, boundary analysis, decision tables, state transition testing, and edge case identification per layer. Use before writing test code to ensure nothing important is missed.
license: Proprietary
compatibility: Flutter/Dart
---

# Test Case Design

This skill is about *thinking*, not syntax. Load it before writing tests to systematically identify what cases matter. Load `tdd` for how to write the test code once you know what to test.

Project invariants that need their own cases (sync flags, storage IDs, money rules) live in `projects/<project>/AGENTS.md` and, if it exists, `projects/<project>/**/.claude/skills/<project>-app-patterns/references/testing.md` (example: `example-app-patterns`). Read them first; they add rows to every table below.

---

## Step 1: Identify the Contract

Before listing cases, answer these three questions about the unit under test:

1. **What are the inputs?** (method params, event fields, initial state, injected deps)
2. **What are the outputs?** (return value, emitted states, side effects on mocks)
3. **What invariants must hold?** (Result<T> never throws, loading guard fires, props complete)

Only test against the contract — not the implementation.

---

## Step 2: Equivalence Partitioning

Group inputs into classes where the behavior is identical for all values in the class. Test one representative from each class — testing more is redundant.

### Example: `SaveOrderUseCase`

| Input class | Representative | Expected output |
|---|---|---|
| Valid order | `Order(id: 'x', amount: 100)` | `Result.success(saved)` |
| Repository returns failure | `mockRepo.save` returns `Result.failure(...)` | `Result.failure` propagated |

Two classes → two tests. No need for five "valid" orders.

### Example: `OrderSaveBloc`

| Input class | Representative | Expected output |
|---|---|---|
| BLoC in initial state, use case succeeds | `SaveOrder(...)` + mock success | `[Loading, Success]` |
| BLoC in initial state, use case fails | `SaveOrder(...)` + mock failure | `[Loading, Error]` |
| BLoC already in Loading state (guard) | seed `Loading`, dispatch event | `[]` (nothing emitted) |
| BLoC in Success state, reset | `ResetOrderSave()` | `[Init]` |

Four classes → four tests.

---

## Step 3: Boundary Value Analysis

Test values at and around the edges of valid ranges. Bugs cluster at boundaries.

### Numeric fields

| Boundary | Test case |
|---|---|
| Zero | `amount: 0.0` — should this be valid? |
| Negative | `amount: -1.0` — business rule: is this allowed? |
| Very large | `amount: 999999999.0` — overflow risk? |
| Null | `amount: null` — nullable field, mapper should not crash |

### Collections

| Boundary | Test case |
|---|---|
| Empty list | `load()` returns `[]` → BLoC should emit `ListEmpty`, not `ListLoaded([])` |
| Single item | `load()` returns `[x]` → standard success |
| Large list | Only relevant if there's pagination or slicing logic |

### Strings

| Boundary | Test case |
|---|---|
| Empty string | `name: ''` — valid? or should trigger validation? |
| Null | `name: null` — mapper should handle gracefully |
| Maximum length | Only if there's an enforced limit |

### Dates and time

| Boundary | Test case |
|---|---|
| Past date | `createdAt: DateTime(2000)` — valid |
| Future date | `dueDate: DateTime(2099)` — valid for scheduled items? |
| UTC vs local | Does parsing return local time correctly? Does a UTC RFC3339 string round-trip? |

---

## Step 4: Decision Tables

Use when a unit has multiple independent conditions that combine to produce different outcomes.

### Example: `OrderListBloc.load`

| Condition A: repo result | Condition B: list content | Expected state |
|---|---|---|
| success | non-empty | `OrderListLoaded(items)` |
| success | empty | `OrderListEmpty` |
| failure | — | `OrderListError(failure)` |

Three rows → three tests.

### Example: Repository `save` returning a storage ID

| Condition A: datasource save | Condition B: storageId returned | Expected |
|---|---|---|
| success | non-null | `Result.success(entity.copyWith(storageId: id))` |
| success | null | `Result.success(entity.copyWith(storageId: null))` — edge case |
| throws | — | `Result.failure(Failure.fromException(...))` |

---

## Step 5: State Transition Testing

For stateful classes (BLoCs), map all valid state transitions and test each one.

### State machine diagram (OrderSaveBloc)

```
Init ──SaveOrder──> Loading ──success──> Success
                                    └──failure──> Error
Success ──ResetOrderSave──> Init
Error   ──ResetOrderSave──> Init
Loading ──SaveOrder──> Loading (guard — no transition)
```

Each arrow is one test case. Don't skip the "guard" edges — they're the most commonly missed.

### Test case derivation from state machine

| From state | Event | To state | Notes |
|---|---|---|---|
| `Init` | `SaveOrder` (success) | `Success` | via `Loading` |
| `Init` | `SaveOrder` (failure) | `Error` | via `Loading` |
| `Loading` | `SaveOrder` | `Loading` | guard fires, no emission |
| `Success` | `ResetOrderSave` | `Init` | |
| `Error` | `ResetOrderSave` | `Init` | |

---

## Step 6: Recurring Edge Cases

These recur across features. Always check them explicitly.

Project sync invariants (offline flags, local storage IDs) belong here too — take them from the overlay.

### Mapper null safety

Every mapper method should be tested with a maximally-sparse input — all nullable fields null except the minimum required to construct the type. This catches null-dereference crashes before production.

```dart
test('responseToEntity handles all-null optional fields', () {
  final sparse = OrderResponse(id: 'o1');  // only id set
  expect(() => OrderMapper.responseToEntity(sparse), returnsNormally);
});
```

### Result<T> contract

| Scenario | Test |
|---|---|
| Repository method when datasource throws | Returns `FailureResult`, does not rethrow |
| BLoC catch block | Emits error state, does not crash stream |

### List BLoC in-memory mutations

`Add`, `Update`, `Remove`, `Set` events are synchronous and don't call the use case. Test that they mutate the in-memory list correctly without async.

| Event | Precondition | Expected |
|---|---|---|
| `AddOrderToList` | List has 2 items | List has 3 items |
| `UpdateOrderInList` | List has item with `storageId: 5` | Item with `storageId: 5` is replaced |
| `RemoveOrderFromList` | List has 1 item | `ListEmpty` state |
| `RemoveOrderFromList` | List has 2 items | `ListLoaded` with 1 item |

---

## Step 7: Test Case Checklist

Before writing any test code, run through this checklist for the unit under test:

**BLoC**
- [ ] Happy path for each async event
- [ ] Failure path for each async event
- [ ] Guard path (already Loading) for each async event
- [ ] Reset event (if present)
- [ ] Each synchronous in-memory event (List BLoC: Add, Update, Remove, Set)
- [ ] Empty list edge case (ListLoaded vs ListEmpty boundary)

**UseCase**
- [ ] Successful delegation — repo called with correct param
- [ ] Failure propagation — repo failure returned as-is

**Mapper**
- [ ] All fields populated (full input)
- [ ] All nullable fields null (sparse input — no crash)
- [ ] Round-trip: entity → storage → entity preserves all fields
- [ ] Date parsing: String → DateTime and back
- [ ] Project sync/storage invariants handled (see the overlay)

**Repository impl**
- [ ] Happy path: datasource success → mapped entity returned
- [ ] Datasource throws → `Result.failure` returned (not rethrown)
- [ ] Project save invariants hold (see the overlay)

---

## Naming Test Cases

Test names should read as specifications:

```dart
// ✅ Reads as a spec
'emits [Loading, Success] when save succeeds'
'returns failure when datasource throws'
'does not emit when already Loading'
'handles null name field without crashing'

// ❌ Too vague
'test save'
'error case'
'works correctly'
```

Pattern: `'{verb} {what} when {condition}'`
