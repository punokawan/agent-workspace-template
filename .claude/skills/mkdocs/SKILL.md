---
name: mkdocs
description: How every project's engineering docs site works — MkDocs Material, one mkdocs.yml and docs/ tree per project, local dev server, adding a page and registering it in nav, available Markdown extensions, writing style, the mirror rule for cited code paths, and common mistakes. A project's tree and nav live in the <project>-docs overlay.
license: Proprietary
compatibility: MkDocs >= 1.5, mkdocs-material >= 9.5, Python 3.x
---

# MkDocs documentation sites

Each project has its own site: config `projects/<project>/mkdocs.yml`, source
`projects/<project>/docs/` (`docs_dir: docs`). Neither is in git — edits have no undo.

## Source of truth

Before adding or moving a page, read in order:
1. `projects/<project>/mkdocs.yml` — theme, enabled extensions, the real `nav:`
2. `projects/<project>/**/.claude/skills/<project>-docs/SKILL.md` if it exists — the docs tree, content-type locations,
   source files to read per section, and feature → doc maps
3. The existing pages next to the one you are writing

Local sources win over this file.

## Quick start

```bash
# One-time, from the workspace root (requirements.txt lives there):
pip install -r requirements.txt

# Serve with live-reload at http://127.0.0.1:8000
mkdocs serve -f projects/<project>/mkdocs.yml

# Build static site (for deployment):
mkdocs build -f projects/<project>/mkdocs.yml
```

---

## Adding a new page

### Step 1: Create the markdown file in the right location

Follow the existing tree (overlay or `ls projects/<project>/docs`). Pick the section that matches the
content scope: per-repo sections (`app/`, `backend/`, `web/`), cross-stack feature references
(`<feature>/technical-reference.md`), setup guides, shared overviews.

### Step 2: Register the page in `mkdocs.yml`

Add it under the correct nav section. The path in nav is **relative to `docs/`**:

```yaml
nav:
  - App Docs:
    - Flows:
      - app/flows/existing-flow.md
      - app/flows/new-flow.md    # ← add here
```

A page that exists in `docs/` but is NOT in `nav:` will not appear in the sidebar — always register new files.

### Step 3: Verify

```bash
mkdocs serve -f projects/<project>/mkdocs.yml   # open the page and confirm it renders
python3 .claude/scripts/_docs.py                # mirror rule: every cited code path exists
```

**Mirror rule:** every fully-qualified code path a doc cites in backticks must exist. Something not yet
built must be labelled `_(planned)_`, `not yet written`, or with a `**Not built.**` callout.

---

## Theme

Material for MkDocs. Features and palette vary per project — read `theme:` in its `mkdocs.yml` rather
than assuming tabs, footer, or code annotations are on.

---

## Markdown Extensions Available

Check `markdown_extensions:` in the project's `mkdocs.yml` before using one — not every project enables all of these (e.g. tabs and task lists need `pymdownx.tabbed` / `pymdownx.tasklist`).

### Code blocks with syntax highlighting

````markdown
```dart
final result = await useCase.call(param);
```
````

### Admonitions (call-out boxes)

```markdown
!!! note "Title"
    Content here.

!!! warning
    This is important.

!!! tip "Pro tip"
    Prefer the existing helper over a new one.
```

Available types: `note`, `tip`, `warning`, `danger`, `info`, `success`, `question`, `example`, `abstract`

### Collapsible details

```markdown
??? note "Click to expand"
    Hidden content here.
```

### Tabbed content

```markdown
=== "Go"
    ```go
    return nil, err
    ```

=== "Dart"
    ```dart
    return Result.failure(error);
    ```
```

### Task lists

```markdown
- [x] Done
- [ ] Not done
```

### Tables

Standard Markdown tables. The `tables` extension ensures consistent rendering.

---

## Writing style

- **Lead with code, not prose.** Every behavior claim should be backed by a code snippet.
- **Actual field names and types.** Read the source before writing — never guess.
- **One concept per section.** Use `##` headings for major sections, `###` for subsections.
- **No speculative content.** Document what the code does, not what it should do.
- **Link to related pages** using relative paths: `[Sync](../sync/technical-reference.md)`
- **Keep the intro short.** A one-line description + the key facts, then dive in.

---

## Common Mistakes

### File exists but doesn't appear in sidebar
**Cause**: File not registered in `nav:` in `mkdocs.yml`.
**Fix**: Add the path under the correct nav section.

### Nav path is wrong
**Cause**: Path in nav must be relative to `docs/`, not to the repo root.
**Fix**: `app/features/orders.md` not `docs/app/features/orders.md`.

### Broken internal links
**Cause**: Using absolute paths or wrong relative paths.
**Fix**: Use `../` to navigate up. From `app/features/orders.md` to `auth/technical-reference.md` is `../../auth/technical-reference.md` (one `../` only reaches `app/`).
**Rule**: links are relative to the file's location in `docs/`.

### `mkdocs serve` fails with `FileNotFoundError`
**Cause**: A file is listed in `nav:` but doesn't exist on disk.
**Fix**: Either create the file or remove it from nav.

### Font/CSS not loading in serve mode
**Cause**: `mkdocs serve` uses `http://127.0.0.1:8000` — works fine. If accessing from a different host, the base URL changes.
**Fix**: Not a problem for local dev. For production deploy, `mkdocs build` generates a self-contained `site/` directory.
