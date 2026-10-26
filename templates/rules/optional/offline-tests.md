## Offline unit tests

- Unit tests never reach a real database, cache, queue or external HTTP service. Mock the
  module that talks to it, or the HTTP client.
- A mock covers every method the code under test calls. An error a test run swallows (`is not a
  function`, a connection refused) means a mock is missing: fix the mock, never ignore the log.
- Where the runner allows it, keep a guard that fails any test reaching a non-local host or
  database, and never disable it inside a test.
- Pin the test time zone so date output matches between machines and CI.
