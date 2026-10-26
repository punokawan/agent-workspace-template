#!/usr/bin/env python3
"""Cross-repo parity checks.

Some facts must be identical in several repos and cannot be shared by any other means, because
each repo is its own git repository: there is no common file to import and no package to depend
on. A log-field allowlist duplicated in Go, TypeScript and Dart is the case this exists for —
adding a key to one and forgetting another is silent, and only the workspace can see all three
checkouts at once.

This script knows no project and no repo. What to compare is declared per project, in
`projects/<name>/project.json`:

    "parity": [
      { "name": "log field allowlist",
        "sources": [
          { "repo": "backend", "file": "...", "between": ["<start>", "<end>"], "extract": "<re>" },
          ...
        ] } ]

`between` bounds the region to read (start marker, end marker); `extract` is a regex whose first
group yields one member of the set. The first source listed is the reference the rest must match.

A source may also declare `verifies`: a list of globs, relative to the repo, whose sha256 sums
must be exactly the extracted set. Without it, a group over CHECKSUM manifests compares the
manifests to each other and nothing to the files — so two manifests left stale in the same way
AGREE, and the check passes while both describe files that have since changed. That happened on
2026-09-23 to the message catalogs: both manifests carried the previous hashes, parity reported
PASS, and the backend was serving copy the web no longer had.
"""
import glob
import hashlib
import json
import os
import re
import sys

ROOT = os.environ.get("STUDIO_ROOT") or os.getcwd()


def members(project_dir, src):
    """The declared set from one source file, or None with a reason if it cannot be read."""
    path = os.path.join(project_dir, src["repo"], src["file"])
    if not os.path.exists(path):
        return None, f"missing file: {os.path.relpath(path, ROOT)}"
    text = open(path, encoding="utf-8").read()
    start_marker, end_marker = src["between"]
    i = text.find(start_marker)
    if i < 0:
        return None, f"start marker not found in {os.path.relpath(path, ROOT)}"
    i += len(start_marker)
    j = text.find(end_marker, i)
    if j < 0:
        return None, f"end marker not found in {os.path.relpath(path, ROOT)}"
    found = set(re.findall(src["extract"], text[i:j]))

    globs = src.get("verifies")
    if globs:
        actual, named = set(), []
        for pattern in globs:
            for f in sorted(glob.glob(os.path.join(project_dir, src["repo"], pattern))):
                actual.add(hashlib.sha256(open(f, "rb").read()).hexdigest())
                named.append(os.path.relpath(f, ROOT))
        if not named:
            return None, f"verifies matched no file: {', '.join(globs)}"
        if actual != found:
            # The manifest describes files that have changed. Saying which side is stale is the
            # useful part: the fix is to regenerate the manifest, never to edit the check.
            return None, (
                f"{os.path.relpath(path, ROOT)} is stale — it does not match "
                f"{len(named)} file(s) it names; regenerate it"
            )
    return found, None


def check_project(name, manifest, project_dir, report):
    ok = True
    for group in manifest.get("parity", []):
        sets, label = [], group.get("name", "unnamed")
        for src in group["sources"]:
            got, err = members(project_dir, src)
            if err:
                report(f"FAIL {name}: {label}: {err}")
                ok = False
                continue
            sets.append((src["repo"], got))
        if len(sets) < 2:
            continue
        ref_repo, ref = sets[0]
        for repo, got in sets[1:]:
            missing, extra = sorted(ref - got), sorted(got - ref)
            if missing or extra:
                ok = False
                report(f"FAIL {name}: {label}: {repo} differs from {ref_repo}")
                if missing:
                    report(f"       missing in {repo}: {', '.join(missing)}")
                if extra:
                    report(f"       only in {repo}: {', '.join(extra)}")
        if ok:
            report(f"PASS {name}: {label} agrees across {len(sets)} repos ({len(ref)} entries)")
    return ok


def main(argv):
    quiet = "--quiet" in argv
    lines = []
    ok = True
    projects_dir = os.path.join(ROOT, "projects")
    for name in sorted(os.listdir(projects_dir)) if os.path.isdir(projects_dir) else []:
        manifest_path = os.path.join(projects_dir, name, "project.json")
        if not os.path.exists(manifest_path):
            continue
        manifest = json.load(open(manifest_path, encoding="utf-8"))
        if not manifest.get("parity"):
            continue
        ok &= check_project(name, manifest, os.path.join(projects_dir, name), lines.append)
    if not quiet:
        print("\n".join(lines) if lines else "no project declares a parity group")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
