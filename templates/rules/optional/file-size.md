## File size

- **Keep source files under the stack's soft line limit** (`file_size` in the stack preset; a
  repo entry in `project.json` may override it). Tests, generated code and migrations do not
  count. `/verify` warns, never fails, when a change grows a file past the limit or adds a new
  file over it. Files already over the limit stay as they are until a change adds to them;
  never refactor an untouched file just to get under the limit.
- **When a file you are growing is over the limit, split it along the layers it already
  follows** — no new layer, package or abstraction:
  - Go: same package, sibling files by sub-resource or use case (order.go → order_refund.go,
    order_search.go); a large router gets one route-registration function per resource, each in
    its own file.
  - Flutter: widgets out to the feature's presentation widgets folder, one use case per file, a
    large BLoC split by event group into handler files.
  - Next.js: components into the feature's components folder, data access into its data
    module; a page composes, it does not implement.
- Reviewers report a file-size warning as a should-fix finding with the split to make.
