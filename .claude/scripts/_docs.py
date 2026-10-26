#!/usr/bin/env python3
"""Docs drift check: every fully-qualified code path a doc cites must exist.

Runs per project. Which directories count as source roots, which file extensions are
code, and which docs subtree belongs to which repo all come from the project manifest
and its stack presets — nothing here is hardcoded to one project.

A doc may cite a path that does not exist only when the line is labelled (planned / not
built / not yet written / intended) or the page carries a `**Not built.**` callout.
"""
import collections
import os
import re
import sys

sys.dont_write_bytecode = True   # keep __pycache__ out of the toolkit tree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _project

ROOT = _project.ROOT
C = dict(r="\033[31m", g="\033[32m", y="\033[33m", b="\033[1m", x="\033[0m")

LABELLED = re.compile(r"planned|not built|not yet written|intended", re.I)
UNBUILT_PAGE = re.compile(r"\*\*Not built\.\*\*")


def audit_project(name):
    """Return (checked, {doc_path: [dead paths]}) for one project."""
    man = _project.load_project(name)
    docs_cfg = man.get("docs") or {}
    docs_rel = docs_cfg.get("dir")
    if not docs_rel:
        return 0, {}
    docs_dir = os.path.join(man["_dir"], docs_rel)
    if not os.path.isdir(docs_dir):
        return 0, {}

    repos = man["repos"]
    if not repos:
        return 0, {}

    # Extensions that count as code, and the source roots that make a path "qualified".
    exts = sorted({e.lstrip(".") for r in repos for e in r.get("code_ext", [])})
    if not exts:
        return 0, {}
    pat = re.compile(r"`([A-Za-z0-9_\-./]+\.(?:%s))`" % "|".join(exts))

    qual = []                       # (prefix, [repos that own it])
    owners = collections.defaultdict(list)
    for r in repos:
        for root in r.get("source_roots", []):
            owners[root.rstrip("/") + "/"].append(r)
    qual = sorted(owners, key=len, reverse=True)

    allow = set(docs_cfg.get("allow", []))
    bad, total = collections.defaultdict(list), 0

    for cur, _, files in os.walk(docs_dir):
        for fn in files:
            if not fn.endswith(".md"):
                continue
            path = os.path.join(cur, fn)
            rel = os.path.relpath(path, man["_dir"])          # e.g. docs/web/pages.md
            text = open(path, encoding="utf-8", errors="ignore").read()
            page_unbuilt = UNBUILT_PAGE.search(text) is not None

            # A docs subtree declared by a repo pins every citation on that page to it.
            pinned = [r for r in repos
                      if r.get("docs_prefix") and rel.startswith(r["docs_prefix"])]

            for line in text.splitlines():
                labelled = LABELLED.search(line)
                for m in pat.findall(line):
                    cited = m.lstrip("/")
                    prefix = next((q for q in qual if cited.startswith(q)), None)
                    if not prefix or cited in allow:
                        continue
                    total += 1
                    candidates = pinned or owners[prefix] or repos
                    if any(os.path.exists(os.path.join(r["dir"], cited)) for r in candidates):
                        continue
                    if labelled or page_unbuilt:
                        continue
                    bad[rel].append(cited)
    return total, bad


def main(argv):
    quiet = "--quiet" in argv
    names = [a for a in argv if not a.startswith("--")] or _project.project_names()
    total, findings = 0, {}
    for name in names:
        t, bad = audit_project(name)
        total += t
        for doc, paths in bad.items():
            findings[f"{name}/{doc}"] = paths

    n = sum(len(v) for v in findings.values())
    if quiet:
        return 1 if n else 0
    print(f"{C['b']}DOCS PATH AUDIT{C['x']} — {total} fully-qualified code paths cited "
          f"across {len(names)} project(s)")
    print("=" * 58)
    if not n:
        print(f"  {C['g']}PASS{C['x']}  every cited path exists")
        print(f"\n{C['g']}VERDICT: CONSISTENT{C['x']}")
        return 0
    for doc, paths in sorted(findings.items()):
        print(f"  {C['r']}{doc}{C['x']}")
        for p in paths:
            print(f"      {p}")
    print(f"\n  {n} dead path(s) in {len(findings)} file(s)")
    print(f"{C['r']}VERDICT: DRIFT{C['x']}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
