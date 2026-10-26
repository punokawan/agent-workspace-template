## Studio defaults

Engineering rules every project follows unless its own guide overrides them.

- **A rule and the code disagree → resolve it.** One of the two is wrong; never work around it.
- **A rule enforced in one place belongs on the server.** A client-side check is a UX
  affordance; delete it and the server must still say no.
- **Money is integer minor units plus a currency code.** Never a float or a formatted string.
- **Timestamps are stored UTC** and shown in a named zone; a time without its zone is a defect.
- **Expected failures are typed results** (permission, validation, conflict, not found). Throw
  only for broken invariants. No raw driver or provider string reaches a user.
- **Uploads are sniffed from their bytes** against a closed allowlist; never trust the declared
  type or extension. SVG is never accepted.
- **Analytics and crash reports carry no personal content** — event names and counts only.
- **Slow work is a job** with retries, an idempotency key and a dead-letter path, never inside a
  request. **Migrations are numbered, forward-only and checked in.**
- **Migrations never risk data that must be kept.** On a database that holds data, never
  reset it, drop and recreate tables, or accept data loss. Back up first, check the migration
  status, read the SQL, then apply.
- **AI output records its provider, model and prompt version**, and prompts live in versioned
  files.
- **Known defects:** a failure that predates your task is recorded in the project's guide, never
  silently absorbed into an unrelated change.
