---
name: flutter-performance
description: Flutter performance patterns for studio apps — widget rebuild reduction, BlocBuilder optimization, list rendering, compute/isolates for heavy work, local-database query patterns, images, and memory management. Project-specific patterns already in a codebase live in the <project>-app-patterns overlay.
license: Proprietary
compatibility: Flutter/Dart with flutter_bloc
---

# Flutter Performance (studio)

Source of truth: `projects/<project>/AGENTS.md`, then `projects/<project>/<repo>/AGENTS.md` if it
exists, then `projects/<project>/**/.claude/skills/<project>-app-patterns/SKILL.md` and
`projects/<project>/**/.claude/skills/<project>-code-consistency/SKILL.md` if they exist. Reuse a pattern the app already
has before inventing one (for example: pagination, `compute()` suggestion caches, and a
view-data cache are listed in `example-app-patterns/references/ui-and-performance.md`).

Performance work falls into four areas: **rebuild reduction**, **list rendering**, **heavy computation offloading**, and **memory/resource management**. Always profile before optimizing — the Flutter DevTools frame chart identifies the actual bottleneck.

---

## 1. BlocBuilder Rebuild Reduction

### Use `buildWhen` to narrow rebuilds

`BlocBuilder` without `buildWhen` rebuilds on every state emission. Use `buildWhen` to rebuild only when the relevant slice changes:

```dart
// ❌ Rebuilds on every state change — even unrelated ones
BlocBuilder<InvoiceListBloc, InvoiceListState>(
  builder: (context, state) => Text(state.count.toString()),
)

// ✅ Only rebuilds when count actually changes
BlocBuilder<InvoiceListBloc, InvoiceListState>(
  buildWhen: (previous, current) =>
      previous is InvoiceListLoaded && current is InvoiceListLoaded
      ? previous.invoices.length != current.invoices.length
      : previous.runtimeType != current.runtimeType,
  builder: (context, state) => Text(...),
)
```

### Split large `BlocBuilder`s into smaller ones

A single `BlocBuilder` wrapping an entire screen rebuilds the whole tree:

```dart
// ❌ Entire screen rebuilds when any state changes
BlocBuilder<MemberListBloc, MemberListState>(
  builder: (context, state) => Scaffold(
    appBar: _buildAppBar(state),      // only needs member count
    body: _buildBody(state),          // needs full list
    floatingActionButton: _buildFAB(state),  // only needs loading state
  ),
)

// ✅ Each part rebuilds independently
Scaffold(
  appBar: BlocBuilder<MemberListBloc, MemberListState>(
    buildWhen: (p, c) => p is MemberListLoaded != c is MemberListLoaded,
    builder: (_, state) => _buildAppBar(state),
  ),
  body: BlocBuilder<MemberListBloc, MemberListState>(
    builder: (_, state) => _buildBody(state),
  ),
  floatingActionButton: BlocBuilder<MemberListBloc, MemberListState>(
    buildWhen: (p, c) =>
        (p is MemberListLoading) != (c is MemberListLoading),
    builder: (_, state) => state is MemberListLoaded
        ? FloatingActionButton(onPressed: onAdd) : const SizedBox.shrink(),
  ),
)
```

### Use `BlocSelector` for single-value extractions

When only one field from the state drives a widget:

```dart
// ✅ Only rebuilds when members.length changes, not on any field change
BlocSelector<MemberListBloc, MemberListState, int>(
  selector: (state) =>
      state is MemberListLoaded ? state.members.length : 0,
  builder: (context, count) => Text('$count members'),
)
```

---

## 2. Widget `const` and Rebuild Avoidance

### Use `const` constructors everywhere possible

`const` widgets are never rebuilt — Flutter short-circuits the diff entirely:

```dart
// ❌ Rebuilt on every parent build
child: SizedBox.shrink()

// ✅ Never rebuilt
child: const SizedBox.shrink()
```

Every static widget in a `build()` method that takes no dynamic values should be `const`. This includes: `Divider()`, `SizedBox()`, `Padding()` with fixed values, `Icon()` with fixed icons, `Text()` with static strings.

### Extract stateless sub-widgets

Inline widget trees that never change should be extracted into `const`-constructable `StatelessWidget`s:

```dart
// ❌ Rebuilt every time parent rebuilds
Widget build(BuildContext context) {
  return Column(children: [
    Row(children: [Icon(Icons.people), Text('Members')]),  // static
    BlocBuilder<MemberListBloc, ...>(...),                 // dynamic
  ]);
}

// ✅ Header is only built once
class _MemberSectionHeader extends StatelessWidget {
  const _MemberSectionHeader();
  @override
  Widget build(BuildContext context) => Row(
    children: [Icon(Icons.people), Text('Members')],
  );
}
```

### `RepaintBoundary` for expensive isolated subtrees

Wrap charts (`fl_chart`) and complex custom-paint widgets:

```dart
RepaintBoundary(
  child: LineChartCard(data: chartData),
)
```

This prevents chart repaints from propagating to the rest of the screen during scroll or unrelated state changes.

---

## 3. List Rendering

### Always use `ListView.builder` or `SliverList` with a builder

Never use `ListView(children: [...])` for dynamic data — it builds all items upfront:

```dart
// ❌ Builds all 500 invoices at once
ListView(
  children: invoices.map((t) => InvoiceTile(t)).toList(),
)

// ✅ Only builds visible items
ListView.builder(
  itemCount: invoices.length,
  itemBuilder: (context, i) => InvoiceTile(invoices[i]),
)
```

### `itemExtent` for uniform-height lists

When all list items have the same height, set `itemExtent` — Flutter can skip layout measurement:

```dart
ListView.builder(
  itemExtent: 72.0,   // InvoiceTile height
  itemCount: invoices.length,
  itemBuilder: (_, i) => InvoiceTile(invoices[i]),
)
```

### Pagination

Lists that can reach hundreds of items page in memory or from the source (e.g. 20 per page) and
load more near the end. Reuse the app's existing pagination state if it has one.

### `AutomaticKeepAliveClientMixin` for tabs

Tab screens that reload data on every switch should use `AutomaticKeepAliveClientMixin`:

```dart
class _MemberTabState extends State<MemberTab>
    with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true;

  @override
  Widget build(BuildContext context) {
    super.build(context);  // required
    return ...;
  }
}
```

---

## 4. Heavy Computation — compute() and Isolates

### When to use `compute()`

Use `compute()` when a synchronous operation takes >16ms on the main thread (one frame budget). Signs: janky scroll when the operation runs, UI freezes during data processing.

```dart
final cache = await compute(
  _buildCacheInIsolate,      // top-level or static function (required)
  _IsolateParams(            // must be sendable (no closures, no non-primitive types)
    invoices: invoices,
    categories: categories,
  ),
);
```

### `compute()` requirements

- The function must be a **top-level or static function** — closures cannot be sent to isolates
- The parameter must be **sendable**: primitives, lists of primitives, simple value classes. No `Stream`, no `BuildContext`, no `Function`.
- Use a dedicated params class

### What qualifies for `compute()`

| Operation | Use compute()? |
|---|---|
| Filter + sort 1000+ invoices | Yes — can take 20-50ms |
| Build chart data from 500+ data points | Yes |
| Generate PDF/CSV report | Yes — always offload |
| Parse large JSON API response | Yes if >100 items |
| Simple list map/filter (<100 items) | No |
| Single entity mapping | Never |

### PDF and CSV generation — always offload

`pdf` and `csv` style packages do synchronous byte-level work. Always use `compute()`:

```dart
// ❌ Blocks UI for 500ms+ on large reports
final bytes = await _generatePdfReport(invoices);

// ✅ Off main thread
final bytes = await compute(_generatePdfReport, PdfParams(
  invoices: invoices,
  dateRange: dateRange,
));
```

---

## 5. View Data Caching

When a screen filters or sorts a large list in memory, compute the view data once per input set and
cache it, keyed on every input dimension (source list, filters, sort). Any input change invalidates it.

```dart
_ViewData? _cached;
_ViewKey? _cachedKey;

_ViewData _viewData(List<Invoice> invoices) {
  final key = _ViewKey(invoices: invoices, status: status, sortBy: sortBy);
  if (_cachedKey == key && _cached != null) return _cached!;
  _cachedKey = key;
  return _cached = _compute(invoices);
}
```

---

## 6. Local Database Query Performance

### Query in the database, not in Dart

Loading all records and filtering in Dart is O(n) on every access. Database queries (ObjectBox,
drift, sqflite) run natively and return only matching rows. ObjectBox example:

```dart
// ❌ Loads all, filters in Dart
final all = await _storage.readAll<InvoiceDto>();
return all.where((t) => t.memberId == memberId).toList();

// ✅ ObjectBox query — only matching rows loaded
final box = store.box<InvoiceDto>();
final query = box.query(InvoiceDto_.memberId.equals(memberId)).build();
final results = query.find();
query.close();  // always close queries
```

### Add `@Index()` on frequently queried fields

Fields used in filters should be indexed — ids, foreign ids, and date fields first.

### Close queries after use

Every `query.build()` allocates native resources. Always call `query.close()`:

```dart
final query = box.query(...).build();
try {
  return query.find();
} finally {
  query.close();
}
```

---

## 7. Image and Asset Performance

### Cache network images

Prefer `cached_network_image` (or the app's image widget) over bare `Image.network()`:

```dart
// ❌ No caching — re-downloads on every build
Image.network(url)

// ✅ Cached in memory and disk
CachedNetworkImage(
  imageUrl: url,
  placeholder: (_, __) => const AppShimmer(),
  errorWidget: (_, __, ___) => const Icon(Icons.broken_image),
)
```

### SVG icons

With `flutter_svg`, use `SvgPicture.asset()`; never rasterize SVGs by hand.

### Bundle fonts

`google_fonts` fetches fonts at runtime if not bundled. For the fonts the app uses, ensure they're listed in `pubspec.yaml` under `flutter.fonts` to bundle them at build time and avoid network fetches.

---

## 8. Memory Management

### Dispose controllers and subscriptions

Every `TextEditingController`, `ScrollController`, `AnimationController`, `StreamSubscription` opened in a `StatefulWidget` must be disposed:

```dart
class _ContentState extends State<Content> {
  late final TextEditingController _nameController;
  StreamSubscription? _sub;

  @override
  void initState() {
    super.initState();
    _nameController = TextEditingController();
  }

  @override
  void dispose() {
    _nameController.dispose();
    _sub?.cancel();
    super.dispose();
  }
}
```

The `cancel_subscriptions` lint rule catches forgotten subscription cancellations, but does not catch `TextEditingController` or `AnimationController` — those must be audited manually.

### Chart data — don't rebuild chart models on every build

Chart data construction (iterating invoices to build `FlSpot` lists) should happen in the BLoC or be memoized — not inside `build()`:

```dart
// ❌ Chart data rebuilt every frame
Widget build(BuildContext context) {
  final spots = invoices.map((t) =>
    FlSpot(t.date.millisecondsSinceEpoch.toDouble(), t.amount ?? 0)
  ).toList();
  return LineChart(LineChartData(lineBarsData: [LineChartBarData(spots: spots)]));
}

// ✅ Pre-computed in BLoC or cached
// BLoC computes List<FlSpot> in the success state, widget just renders it
```

---

## Performance Profiling Checklist

Before declaring a performance fix done:

- [ ] Open Flutter DevTools → Performance tab
- [ ] Record while reproducing the slow interaction
- [ ] Check for frames exceeding 16ms (red in the timeline)
- [ ] Identify whether the jank is in **build**, **layout**, or **paint**
- [ ] Build jank → reduce rebuilds (BlocBuilder, const, extract widgets)
- [ ] Layout jank → simplify widget tree depth, use `itemExtent`
- [ ] Paint jank → add `RepaintBoundary`, reduce overdraw
- [ ] Memory growth → check DevTools Memory tab for retained objects

Never optimize without measuring. A perceived lag is often network latency, not render performance.
