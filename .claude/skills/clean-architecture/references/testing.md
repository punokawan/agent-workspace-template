# Testing

## Principles

- Prefer behavior tests over implementation-detail tests.
- Use AAA: Arrange, Act, Assert.
- Keep dependencies mockable through constructor injection.
- Every feature change should identify the smallest meaningful test surface.

## Minimum Targets

- Mapper tests for field conversion and null safety.
- Use case tests for delegation and failure propagation.
- Repository tests for datasource success/failure and mapping behavior.
- BLoC tests for loading, success, failure, empty, reset, and duplicate event guard.
- Widget tests only where UI states, validation, or interactions are meaningful.

## BLoC Test Expectations

- Emits loading before success/error for async operations.
- Does not emit duplicate loading for guarded duplicate events.
- Preserves current list state when local add/update/remove events are intended to be in-memory.
- Error state exposes the failure for UI handling.

## Repository Test Expectations

- Datasource exceptions become a failure `Result`.
- Successful datasource responses are mapped through mapper methods.
- Empty local/remote responses produce the intended empty or success result.
- Sync flags, retry timestamps, and local storage IDs are preserved when relevant (project overlay names them).

## Testability Smells

- Widget needs a real network/storage dependency to test.
- BLoC creates dependencies internally.
- Mapper behavior is duplicated in repository or UI.
- Time/UUID/payment/network behavior is not injectable when deterministic tests need it.
