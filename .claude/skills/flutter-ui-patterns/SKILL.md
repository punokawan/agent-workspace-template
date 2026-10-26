---
name: flutter-ui-patterns
description: Studio Flutter presentation-layer conventions — screen structure, shared widgets, theme tokens, navigation, BlocBuilder/Listener/Consumer choice, loading/empty/error states, constants, l10n, and UI anti-patterns. Project screen layouts, widget libraries, and routers live in the <project>-app-patterns overlay.
license: Proprietary
compatibility: Flutter with flutter_bloc
---

# Flutter UI Patterns (studio)

## Source of truth

Read, in this order: `projects/<project>/AGENTS.md`; `projects/<project>/<repo>/AGENTS.md` if it
exists; `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and
`projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md`, each only if it exists; then the nearest
existing screen in the same feature. They win over this file. For example, one project keeps its
`screen.dart`/`content.dart` split, its `Example*` atoms and `ExampleInjector.navigate` routing in
`example-app-patterns/references/ui-and-performance.md`.

## Screen structure

- Screens live under `lib/presentations/screens/<feature>/`. Follow the project's file split
  (one `<name>_screen.dart`, or a providers file plus a content file).
- The screen's top widget creates screen-scoped BLoCs in `BlocProvider`/`MultiBlocProvider`; that is
  the DI boundary for presentation. The content below it holds the UI.
- Route arguments are typed classes, never raw maps or positional lists.
- A screen composes several operation BLoCs; it does not grow one BLoC per screen.

```dart
class InvoiceListScreen extends StatelessWidget {
  const InvoiceListScreen({super.key});

  @override
  Widget build(BuildContext context) => MultiBlocProvider(
        providers: [
          BlocProvider(create: (_) => injector<InvoiceListBloc>()..add(const LoadInvoices())),
          BlocProvider(create: (_) => injector<InvoicePayBloc>()),
        ],
        child: const _InvoiceListView(),
      );
}
```

## Shared widgets

Use the project's shared widgets (`lib/presentations/widgets/`) for buttons, fields, empty, error,
loading, and money display before writing a new one. Shared widgets hold no business logic. Variants
are named constructors or parameters, not copies.

## Theme

Never hardcode colors, text styles, or spacing that a theme token covers. Use the project's theme
extension; fall back to `Theme.of(context).colorScheme` only when no token exists. Some apps let the
user change the primary color — a literal breaks that.

## Navigation

Use the project's router (`go_router` in most studio apps) and its route constants. No raw path
strings, no ad-hoc `Navigator.of(context).push` unless the surrounding code already does it.

## BlocBuilder vs BlocListener vs BlocConsumer

| Widget | Use when |
|---|---|
| `BlocBuilder` | UI rebuilds from state |
| `BlocListener` | side effects: navigate, snackbar, notify another BLoC |
| `BlocConsumer` | both on the same state change |
| `MultiBlocListener` | several BLoCs producing side effects in one screen |
| `BlocSelector` | one value from the state drives the widget |

BLoC chaining: when one operation succeeds and a list BLoC should reflect it, a `BlocListener` on the
operation BLoC adds an event to the list BLoC — no full reload.

```dart
BlocListener<InvoicePayBloc, InvoicePayState>(
  listener: (context, state) {
    if (state is InvoicePaySuccess) {
      context.read<InvoiceListBloc>().add(InvoiceUpdated(state.invoice));
    }
  },
)
```

## State-driven UI

Every async screen renders loading, empty, error (with retry), and loaded. Disable the submit
control while its BLoC is loading.

```dart
BlocBuilder<InvoicePayBloc, InvoicePayState>(
  builder: (context, state) {
    final isLoading = state is InvoicePayLoading;
    return AppButton(label: context.l10n.invoicePay, isLoading: isLoading, onTap: isLoading ? null : _pay);
  },
)
```

## Constants

Storage keys, route names, and other magic strings are constants owned by the project — never
inline literals.

## Localization

All user-facing text comes from generated l10n (`context.l10n.<key>` or the project accessor). Add
the key to every ARB file immediately — no `TODO: localize`. See the `l10n` skill.

## Anti-patterns to reject

- Business logic in `build()` (filtering, formatting, deriving values) → move to a use case or BLoC.
- `setState` holding app data — `setState` is for purely local UI state.
- `context.read<>()` inside `build()` — only in callbacks.
- `context.watch<>()` where an explicit `BlocBuilder`/`BlocSelector` is clearer.
- Nested `BlocBuilder`s where one with a narrower `buildWhen` suffices.
- Two controls in one section doing the same action.
