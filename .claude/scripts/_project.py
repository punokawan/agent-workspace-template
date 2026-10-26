#!/usr/bin/env python3
"""Project registry: the single source of truth for what this workspace hosts.

Every script that needs to know "which repos exist, where they live, how to verify
them" asks this module. Nothing else may hardcode a project or repo name.

Layout it assumes:

    <root>/projects/<project>/project.json     the manifest
    <root>/projects/<project>/<repo-id>/       the checkout
    <root>/templates/stacks/<stack>.json       reusable per-stack defaults

A repo entry inherits every key from its stack preset and may override any of them
inline. That is what keeps a new project's manifest to a dozen lines.
"""
import fnmatch
import json
import os
import shutil
import sys

ROOT = os.environ.get("STUDIO_ROOT") or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PROJECTS_DIR = os.path.join(ROOT, "projects")
STACKS_DIR = os.path.join(ROOT, "templates", "stacks")
ACTIVE_PTR = os.path.join(ROOT, ".claude", "agentic-state", "CURRENT_PROJECT")

C = dict(r="\033[31m", g="\033[32m", y="\033[33m", c="\033[36m", b="\033[1m", x="\033[0m")

# Keys a repo entry inherits from its stack preset unless it sets them itself.
INHERITED = ("verify", "shared_artifacts", "local_config", "prune_dirs",
             "code_ext", "source_roots", "generated_markers")


class ManifestError(Exception):
    pass


def _read_json(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise ManifestError(f"missing: {os.path.relpath(path, ROOT)}")
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid JSON in {os.path.relpath(path, ROOT)}: {exc}")


def load_stack(name):
    return _read_json(os.path.join(STACKS_DIR, f"{name}.json"))


def project_names():
    if not os.path.isdir(PROJECTS_DIR):
        return []
    # A leading "_" marks a reference folder such as _example: shown, never a target.
    return sorted(
        d for d in os.listdir(PROJECTS_DIR)
        if not d.startswith("_") and os.path.isfile(os.path.join(PROJECTS_DIR, d, "project.json")))


def load_project(name):
    """Manifest with every repo fully resolved against its stack preset."""
    man = _read_json(os.path.join(PROJECTS_DIR, name, "project.json"))
    man.setdefault("name", name)
    if man["name"] != name:
        raise ManifestError(
            f"{name}/project.json declares name '{man['name']}' — must match its directory")
    man["_dir"] = os.path.join(PROJECTS_DIR, name)
    resolved = []
    for repo in man.get("repos", []):
        if "id" not in repo:
            raise ManifestError(f"{name}: a repo entry has no 'id'")
        if "stack" not in repo:
            raise ManifestError(f"{name}/{repo['id']}: no 'stack'")
        merged = dict(load_stack(repo["stack"]))
        merged.update(repo)                      # inline keys win over the preset
        for key in INHERITED:
            merged.setdefault(key, [] if key != "verify" else {"quick": [], "full": []})
        merged["project"] = name
        merged["dir"] = os.path.join(PROJECTS_DIR, name, repo["id"])
        merged["reldir"] = os.path.relpath(merged["dir"], ROOT)
        merged.setdefault("integration", "dev")
        merged.setdefault("production", "main")
        resolved.append(merged)
    man["repos"] = resolved
    return man


def active_project():
    names = project_names()
    if os.path.isfile(ACTIVE_PTR):
        cur = open(ACTIVE_PTR, encoding="utf-8").read().strip()
        if cur in names:
            return cur
    if len(names) == 1:
        return names[0]
    return ""


def find_repo(project, repo_id):
    for r in load_project(project)["repos"]:
        if r["id"] == repo_id:
            return r
    return None


def resolve(specs):
    """Expand target specs into concrete (project, repo) records.

    all                  every repo of every project
    <project>            every repo of that project
    <project>/all        same
    <project>/<repo>     one repo
    <repo>               that repo in the active project
    """
    names = project_names()
    out, seen = [], set()

    def add(rec):
        key = (rec["project"], rec["id"])
        if key not in seen:
            seen.add(key)
            out.append(rec)

    for spec in specs:
        if spec == "all":
            for p in names:
                for r in load_project(p)["repos"]:
                    add(r)
            continue
        if "/" in spec:
            proj, _, rid = spec.partition("/")
            if proj not in names:
                raise ManifestError(f"unknown project: {proj} (have: {', '.join(names) or 'none'})")
            if rid in ("all", ""):
                for r in load_project(proj)["repos"]:
                    add(r)
                continue
            rec = find_repo(proj, rid)
            if rec is None:
                have = [r["id"] for r in load_project(proj)["repos"]]
                raise ManifestError(f"unknown repo: {spec} ({proj} has: {', '.join(have)})")
            add(rec)
            continue
        if spec in names:                        # a bare project name
            for r in load_project(spec)["repos"]:
                add(r)
            continue
        act = active_project()                   # a bare repo id in the active project
        if not act:
            raise ManifestError(
                f"'{spec}' is not a project, and no active project is set to resolve it as a "
                f"repo. Run: project.sh use <project>")
        rec = find_repo(act, spec)
        if rec is None:
            have = [r["id"] for r in load_project(act)["repos"]]
            raise ManifestError(
                f"unknown target: {spec} (project '{act}' has: {', '.join(have)}; "
                f"projects: {', '.join(names)})")
        add(rec)
    return out


# ---------------------------------------------------------------- subcommands

def cmd_list(argv):
    for n in project_names():
        man = load_project(n)
        mark = "*" if n == active_project() else " "
        repos = ", ".join(f"{r['id']}:{r['stack']}" for r in man["repos"])
        print(f"{mark} {n:<16} {repos}")
    return 0


def cmd_active(argv):
    a = active_project()
    if a:
        print(a)
        return 0
    return 1


def cmd_use(argv):
    if not argv:
        raise ManifestError("usage: _project.py use <project>")
    name = argv[0]
    if name not in project_names():
        raise ManifestError(f"unknown project: {name}")
    os.makedirs(os.path.dirname(ACTIVE_PTR), exist_ok=True)
    with open(ACTIVE_PTR, "w", encoding="utf-8") as fh:
        fh.write(name + "\n")
    print(name)
    return 0


def cmd_repos(argv):
    proj = argv[0] if argv else active_project()
    if not proj:
        raise ManifestError("no project given and no active project set")
    for r in load_project(proj)["repos"]:
        print(r["id"])
    return 0


def cmd_resolve(argv):
    """Tab-separated: project, repo id, dir relative to root, stack, integration branch."""
    for r in resolve(argv or ["all"]):
        print("\t".join([r["project"], r["id"], r["reldir"], r["stack"], r["integration"]]))
    return 0


def cmd_field(argv):
    """field <project> <repo> <key> — scalars print bare, lists print one per line."""
    if len(argv) < 3:
        raise ManifestError("usage: _project.py field <project> <repo> <key>")
    proj, rid, key = argv[0], argv[1], argv[2]
    rec = find_repo(proj, rid)
    if rec is None:
        raise ManifestError(f"unknown repo: {proj}/{rid}")
    val = rec.get(key)
    if val is None:
        return 0
    if isinstance(val, list):
        for v in val:
            print(v if not isinstance(v, (dict, list)) else json.dumps(v))
    elif isinstance(val, dict):
        print(json.dumps(val))
    else:
        print(val)
    return 0


def cmd_meta(argv):
    """meta <project> [key] — project-level manifest fields."""
    proj = argv[0] if argv else active_project()
    if not proj:
        raise ManifestError("no project given and no active project set")
    man = load_project(proj)
    if len(argv) < 2:
        print(json.dumps({k: v for k, v in man.items() if k != "_dir"}, indent=2))
        return 0
    val = man.get(argv[1], "")
    print(json.dumps(val) if isinstance(val, (dict, list)) else val)
    return 0


def cmd_artifacts(argv):
    """artifacts [spec...] — project, repo, path-in-repo, cache subdir, seed flag."""
    for r in resolve(argv or ["all"]):
        for a in r.get("shared_artifacts", []):
            print("\t".join([r["project"], r["id"], a["path"],
                             f"{r['project']}/{r['id']}/{a['cache']}",
                             "seed" if a.get("seed_from_checkout") else "-"]))
    return 0


def cmd_checks(argv):
    """checks <project> <repo> <quick|full> — one JSON check per line, skips resolved.

    A check whose `requires` globs match nothing in the checkout, or whose
    `requires_tool` is not on PATH, prints as a skip rather than a failure: a gate for a tool that was never configured must never
    report FAIL, and must never silently report PASS either.
    """
    if len(argv) < 3:
        raise ManifestError("usage: _project.py checks <project> <repo> <quick|full>")
    proj, rid, mode = argv[0], argv[1], argv[2]
    rec = find_repo(proj, rid)
    if rec is None:
        raise ManifestError(f"unknown repo: {proj}/{rid}")
    base = os.environ.get("CHECK_DIR") or rec["dir"]
    phases = ["quick"] if mode == "quick" else ["quick", "full"]
    for phase in phases:
        for chk in rec.get("verify", {}).get(phase, []):
            req = chk.get("requires")
            if req and not any(fnmatch.filter(os.listdir(base) if os.path.isdir(base) else [], g)
                               for g in req):
                print(json.dumps({"name": chk["name"], "skip":
                                  chk.get("skip_reason", "required config not present")}))
                continue
            tool = chk.get("requires_tool")
            if tool and shutil.which(tool) is None:
                print(json.dumps({"name": chk["name"], "skip": f"{tool} not installed"}))
                continue
            print(json.dumps({"name": chk["name"], "cmd": chk["cmd"]}))
    return 0


def cmd_check(argv):
    """Validate every manifest against what is actually on disk."""
    quiet = "--quiet" in argv
    problems, names = [], project_names()
    if not names:
        problems.append("no projects registered under projects/*/project.json")
    for n in names:
        try:
            man = load_project(n)
        except ManifestError as exc:
            problems.append(str(exc))
            continue
        if not man["repos"]:
            problems.append(f"{n}: manifest declares no repos")
        for r in man["repos"]:
            if not os.path.isdir(r["dir"]):
                problems.append(f"{n}/{r['id']}: checkout missing at {r['reldir']}")
            elif not os.path.exists(os.path.join(r["dir"], ".git")):
                problems.append(f"{n}/{r['id']}: {r['reldir']} is not a git repository")
            if not os.path.isfile(os.path.join(STACKS_DIR, f"{r['stack']}.json")):
                problems.append(f"{n}/{r['id']}: unknown stack '{r['stack']}'")
        pdir = man.get("planning")
        if pdir and not os.path.isdir(os.path.join(man["_dir"], pdir)):
            problems.append(f"{n}: planning dir '{pdir}' does not exist")
        ddir = (man.get("docs") or {}).get("dir")
        if ddir and not os.path.isdir(os.path.join(man["_dir"], ddir)):
            problems.append(f"{n}: docs dir '{ddir}' does not exist")
    if quiet:
        return 1 if problems else 0
    print(f"{C['b']}PROJECT MANIFEST CHECK{C['x']} — {len(names)} project(s)")
    print("=" * 58)
    if not problems:
        for n in names:
            man = load_project(n)
            print(f"  {C['g']}PASS{C['x']}  {n}: "
                  f"{', '.join(r['id'] for r in man['repos'])}")
        print(f"\n{C['g']}VERDICT: CONSISTENT{C['x']}")
        return 0
    for p in problems:
        print(f"  {C['r']}FAIL{C['x']}  {p}")
    print(f"\n{C['r']}VERDICT: DRIFT{C['x']}")
    return 1


def cmd_show(argv):
    proj = argv[0] if argv else active_project()
    if not proj:
        raise ManifestError("no project given and no active project set")
    man = load_project(proj)
    print(f"{C['b']}{man.get('title', proj)}{C['x']}  ({proj})")
    if man.get("description"):
        print(f"  {man['description']}")
    print(f"  dir      : projects/{proj}")
    print(f"  planning : {man.get('planning', '—')}")
    print(f"  docs     : {(man.get('docs') or {}).get('dir', '—')}")
    print()
    print(f"  {'REPO':<10} {'STACK':<10} {'INTEGRATION':<14} {'PROD':<6} DEPLOY")
    for r in man["repos"]:
        print(f"  {r['id']:<10} {r['stack']:<10} {r['integration']:<14} "
              f"{r['production']:<6} {r.get('deploy', '—')}")
    return 0


COMMANDS = {
    "list": cmd_list, "active": cmd_active, "use": cmd_use, "repos": cmd_repos,
    "resolve": cmd_resolve, "field": cmd_field, "meta": cmd_meta,
    "artifacts": cmd_artifacts, "checks": cmd_checks, "check": cmd_check, "show": cmd_show,
}


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        print(f"usage: _project.py {{{'|'.join(COMMANDS)}}} [args]", file=sys.stderr)
        return 2
    try:
        return COMMANDS[argv[0]](argv[1:])
    except ManifestError as exc:
        print(f"{C['r']}manifest error:{C['x']} {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
