# Example — project guide

> Applies inside `projects/example/` and its worktrees under `.wt/example/`. The workspace
> guide (`../../AGENTS.md`) applies unchanged except where a line here says `Override`. Each
> repo's own `AGENTS.md` refines this file for that repo.

`project.json` is the source of truth for repos, stacks, branches, deploy targets and verify
commands. Never restate it here.

Read when the task touches them:
- `GLOSSARY.md` — the full vocabulary, when it outgrows the table below.

## What Example is

A booking tool: a customer books a slot on the web, and staff confirm it. **A confirmed
booking is never double-sold** — that outranks every other preference here.

## What each repo owns

- **`web/` is what a customer and staff see** — booking pages and the staff desk.
- **`backend/` is the arbiter** — slots, bookings, payments and the audit log.

## Contracts

- **EX1 — A slot is sold once.** Confirming a booking locks its slot in one transaction; a
  second confirm for the same slot fails with `conflict`, never a second booking.
- **EX2 — A customer sees only their own bookings**, scoped from the authenticated session,
  never from a request body.

## Conventions

- **Override (AGENTS.md §Studio defaults):** times are shown in the venue's zone, not the
  viewer's — a booking is for a place.
- Booking references are `BK-` plus eight base32 characters; never a database id.

## Domain vocabulary

| Term | Means | Not called |
|---|---|---|
| **Slot** | One bookable interval at one venue | session, time, opening |
| **Booking** | One customer's claim on one Slot | reservation, order |

## Security posture

Beyond the workspace rules, which apply unchanged:

- Staff routes require the `staff` role; the role is checked on the backend only.

## Known defects

_None recorded._
