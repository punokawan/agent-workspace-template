---
name: firebase-analytics
description: How to implement Firebase Analytics in a Flutter/BLoC app the right way — where to call it (BLoC success branch, not widgets), one project-wide accessor, screen tracking once at the router, user identity and properties, built-in vs custom events, event naming rules, privacy boundaries, a testable AnalyticsService abstraction, first-use milestones, and DebugView. Project specifics (singleton, event catalog, per-BLoC map) live in the <project>-analytics overlay.
license: MIT
compatibility: firebase_analytics, Flutter/BLoC
---

# Firebase Analytics (Flutter + BLoC)

## Source of truth

Before adding or changing analytics, read in this order:
1. `projects/<project>/AGENTS.md` — privacy rules (many projects forbid content in analytics payloads)
2. `projects/<project>/<repo>/AGENTS.md` if it exists
3. `projects/<project>/**/.claude/skills/<project>-analytics/SKILL.md` only if it exists — the project's accessor, event
   catalog, per-BLoC map, and known anti-patterns (example: `example-analytics`)
4. The nearest existing analytics call in the repo

Local sources win over this file. If the project has no analytics wired, say so before adding it.

---

## Where to call analytics

Analytics calls belong in the **BLoC layer**, in the `success` branch of the result — never in a
widget, never before the result is known, never in the `failure` branch. A widget call logs an
action as done even when the action then fails.

```dart
Future<void> _onSaveOrder(SaveOrder event, Emitter<OrderSaveState> emit) async {
  if (state is OrderSaveLoading) return;
  emit(const OrderSaveLoading());
  try {
    final result = await saveOrderUseCase.call(event.param);
    result.when(
      success: (order) {
        _analytics.logEvent('order_created', parameters: {'type': event.param.type});
        emit(OrderSaveSuccess(order));
      },
      failure: (f) => emit(OrderSaveError(f)),
    );
  } catch (e, s) {
    emit(OrderSaveError(Failure.fromException(e, s)));
  }
}
```

A Cubit with no result wrapper logs right before it emits. The one exception is screen tracking,
which fires on every navigation regardless of outcome.

**One accessor.** The app imports `firebase_analytics` in exactly one place (a singleton or the
service implementation below). Everything else goes through that accessor.

---

## Screen tracking

Track screens once, centrally — in the route generator or a `NavigatorObserver`
(`FirebaseAnalyticsObserver`). Do not add `logScreenView` inside screens; it double-counts. Track
explicitly only surfaces that bypass the router (bottom sheets, dialogs with their own flow).

---

## User identity and properties

- After sign-in: `setUserId` with the **server-assigned opaque ID**. Never email, name, or phone.
- After the profile loads: set user properties that segment behaviour (plan tier, onboarding done).
  Firebase allows **25 user properties** per app; pick few, meaningful ones.
- On sign-out and on account deletion: `setUserId(null)`.

---

## Built-in events — use these, don't reinvent

| Situation | Use |
|---|---|
| Sign in | `logLogin(loginMethod: 'email')` |
| New account | `logSignUp(signUpMethod: 'email')` |
| IAP purchase | `logPurchase(currency:, value:, items:)` |
| App open | `logAppOpen()` — once at startup |
| Screen viewed | `logScreenView(screenName:)` — router only |
| Search | `logSearch(searchTerm:)` — only if the term carries no user content |
| Content selected | `logSelectContent(contentType:, itemId:)` |

Custom events answer "what did the user do?" for actions the built-ins do not cover.

---

## Event naming rules

| Rule | Example |
|---|---|
| `snake_case` only | `order_created` not `orderCreated` |
| verb_noun, past tense | `order_created`, `invoice_deleted`, `goal_completed` |
| Name under 40 characters | Firebase limit |
| Parameter values under 100 characters | Truncate if needed |
| No PII in names or values | See privacy below |
| No reserved prefixes `firebase_`, `google_`, `ga_` | Reserved by Firebase |

---

## Privacy

Analytics data is retained for months and leaves your control. Never log: email, name, phone,
free text the user typed (notes, messages), names of user-created things (use an ID or a type),
or device identifiers beyond what Firebase sets itself. Safe: enum values, booleans (`has_note`),
type strings, plan IDs, status strings, numeric amounts only for `logPurchase`. The project's
`AGENTS.md` may be stricter — it wins.

---

## AnalyticsService — abstraction for testability

`FirebaseAnalytics.instance` is a platform singleton that `bloc_test` cannot mock. Wrap it in a
thin interface with no Firebase import, implement it once with Firebase, register it in DI, and
inject it into BLoCs through the constructor.

```dart
abstract class AnalyticsService {
  Future<void> logEvent(String name, {Map<String, Object>? parameters});
  Future<void> logLogin(String method);
  Future<void> logSignUp(String method);
  Future<void> logPurchase({required String currency, required double value, required String planId, required String planName});
  Future<void> setUserId(String? id);
  Future<void> setUserProperty(String name, String? value);
  Future<void> logScreenView(String screenName);
}
```

In tests, mock `AnalyticsService` with the repo's mocking library, stub `logEvent` to complete, and
assert in `verify:` that the event fired exactly once on success and never on failure.

---

## First-use milestones

High-signal onboarding events (`first_<thing>_created`) fire once per install. Gate them on a
persisted flag: read the flag, return if set, write it, then log. Keep the flag keys with the
project's other storage-key constants.

---

## DebugView

```bash
adb shell setprop debug.firebase.analytics.app <applicationId>   # Android on
adb shell setprop debug.firebase.analytics.app .none.            # Android off
# iOS: add -FIRDebugEnabled to the Xcode scheme's launch arguments
```

Firebase console → Analytics → DebugView shows events within seconds.

---

## Checklist for a new feature

- [ ] `AnalyticsService` injected via the BLoC constructor, not the raw singleton
- [ ] BLoC's DI registration updated with the new dependency
- [ ] Events logged only in the `success` branch
- [ ] `snake_case` verb_noun names; boolean/enum parameters, no free text, no PII
- [ ] IAP purchases use `logPurchase`
- [ ] First-use milestones gated by a persisted flag
- [ ] Project event catalog updated (in the `<project>-analytics` overlay, if it has one)
- [ ] BLoC test mocks `AnalyticsService` and verifies the call
- [ ] Event seen in DebugView before shipping
