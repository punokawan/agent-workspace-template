# Presentation Layer

Screen file layout, widget library, routing, and theme API differ per project — see
`projects/<project>/**/.claude/skills/<project>-app-patterns/` when it exists and the `flutter-ui-patterns` skill.

## Responsibilities

- UI rendering and user interaction.
- BLoC event/state orchestration.
- Navigation through the project's router.
- Formatting display data.
- Local UI state (controllers, selected tab, focus).

## Rules

- BLoCs depend on use cases or domain services — never datasources, DTOs, HTTP clients, Firebase,
  or database boxes.
- Dependencies are injected by constructor; no service-locator lookups inside a BLoC.
- Async handlers guard duplicate loading where double-submit or duplicate fetch can happen.
- Error states carry the project's failure type.
- User-facing text comes from generated l10n.
- Navigation uses the project's router helpers and route constants.
- Styling uses the project's theme tokens and shared widgets, not raw colors.

## BLoC pattern

See `../SKILL.md` "Presentation". One BLoC per operation; sealed `Equatable` events and states;
guard → `try` → emit from `Result`.

## Widget rules

- No business decisions in `build()`.
- Extract repeated UI into feature-local widgets, or shared widgets once reused.
- Match nearby screens for layout, spacing, and accessibility.
- No hardcoded user-facing text where l10n exists.

## Critical violations

- Presentation imports data-layer classes.
- BLoC reaches storage or network directly.
- Widget computes or mutates domain state that belongs in a use case or BLoC.
- Screen bypasses l10n for user-facing text.
