"""Vendored skills: where each one came from, and how to update it from its source.

Every vendored skill or plugin keeps an `UPSTREAM.md` with one fenced block per source:

    ```upstream
    repo: https://github.com/<owner>/<repo>
    path: skills/<name>            # comma list allowed (merged mode)
    commit: <40-hex sha>           # the pinned upstream commit
    mode: copy                     # copy = vendored unchanged; merged = adapted (never auto-updated)
    licence: MIT
    extra: LICENSE                 # optional: repo-root files copied next to the skill
    files: SKILL.md                # optional (copy): take only these files from path
    root: marketing-skill          # optional (merged): SOURCES.md paths are relative to this
    key: ali                       # optional (merged): the source key used in SOURCES.md rows
    ref: HEAD                      # optional: branch or ref to follow
    ```

Commands (run through upstream.sh):
    list                    every block, offline
    lint                    validate every block, offline (used by audit.sh)
    check [name...]         newer upstream commits, and local drift from the pinned copy
    diff <name> [--to SHA] [--stat]
                            what changed upstream; for merged mode, which merged skill each file feeds
    pull <name> [--to SHA] [--force]
                            copy mode only: replace the files with a newer commit, bump the pin
    add <repo> <path> [--name N] [--commit SHA] [--extra FILE] [--licence L]
                            vendor a new skill into .claude/skills/<name>, unchanged

Upstream clones live in the main checkout's .cache/upstream/ (bare, blobless). No upstream code runs,
except the vendored skill-security-auditor (a static scanner), and only after its UPSTREAM.md records
a dated review.
"""
import datetime
import os
import re
import shutil
import subprocess
import sys

ROOT = os.environ.get("STUDIO_ROOT") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


def _shared_cache():
    """One clone cache for the main checkout and every worktree of it."""
    if os.environ.get("UPSTREAM_CACHE"):
        return os.environ["UPSTREAM_CACHE"]
    r = subprocess.run(["git", "-C", ROOT, "rev-parse", "--path-format=absolute", "--git-common-dir"],
                       capture_output=True, text=True)
    main = os.path.dirname(r.stdout.strip()) if r.returncode == 0 and r.stdout.strip() else ROOT
    return os.path.join(main, ".cache", "upstream")


CACHE = _shared_cache()
SEARCH = [".claude/skills/*/UPSTREAM.md", "plugins/*/UPSTREAM.md",
          "projects/*/.claude/skills/*/UPSTREAM.md", "projects/*/*/.claude/skills/*/UPSTREAM.md"]
AUDITOR = os.path.join(ROOT, ".claude", "skills", "skill-security-auditor", "scripts", "skill_security_auditor.py")
IGNORED = {"UPSTREAM.md", ".DS_Store"}
BLOCK = re.compile(r"```upstream\n(.*?)```", re.S)
SHA = re.compile(r"^[0-9a-f]{40}$")
KEYS = {"repo", "path", "commit", "mode", "licence", "extra", "files", "root", "key", "ref"}


class Fail(Exception):
    pass


# ---------- blocks ----------

def parse_blocks(text):
    blocks = []
    for m in BLOCK.finditer(text):
        b = {}
        for line in m.group(1).splitlines():
            line = re.sub(r"\s+#.*$", "", line).strip()
            if not line:
                continue
            k, _, v = line.partition(":")
            b[k.strip()] = v.strip()
        blocks.append(b)
    return blocks


def split_list(v):
    return [x.strip().strip("/") for x in (v or "").split(",") if x.strip()]


def discover():
    import glob
    out = []
    for pat in SEARCH:
        for f in sorted(glob.glob(os.path.join(ROOT, pat))):
            text = open(f, encoding="utf-8").read()
            blocks = parse_blocks(text)
            name = os.path.basename(os.path.dirname(f))
            for i, b in enumerate(blocks):
                ident = name if len(blocks) == 1 else f"{name}:{b.get('key') or i + 1}"
                out.append({"id": ident, "name": name, "file": f, "dir": os.path.dirname(f), "index": i, **b})
            if not blocks:
                out.append({"id": name, "name": name, "file": f, "dir": os.path.dirname(f), "index": -1})
    return out


def lint_block(e):
    errs = []
    if e["index"] < 0:
        return ["no ```upstream block"]
    for k in ("repo", "path", "commit"):
        if not e.get(k):
            errs.append(f"missing {k}")
    if e.get("commit") and not SHA.match(e["commit"]):
        errs.append("commit is not a full 40-character sha")
    mode = e.get("mode", "copy")
    if mode not in ("copy", "merged"):
        errs.append(f"unknown mode {mode}")
    if mode == "copy" and len(split_list(e.get("path"))) > 1:
        errs.append("copy mode takes one path")
    for k in set(e) - KEYS - {"id", "name", "file", "dir", "index"}:
        errs.append(f"unknown key {k}")
    if not e.get("licence"):
        errs.append("missing licence")
    lic = [f for f in os.listdir(e["dir"]) if f.upper().startswith("LICENSE")]
    if not lic:
        errs.append("no LICENSE file next to UPSTREAM.md")
    return errs


def select(entries, names):
    if not names:
        return entries
    picked = [e for e in entries if e["id"] in names or e["name"] in names]
    missing = [n for n in names if not any(n in (e["id"], e["name"]) for e in entries)]
    if missing:
        raise Fail(f"no upstream block for: {', '.join(missing)} (see: upstream.sh list)")
    return picked


def rel(path):
    return os.path.relpath(path, ROOT)


# ---------- git ----------

def git(*args, cwd=None, raw=False, check=True):
    r = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=not raw)
    if check and r.returncode != 0:
        err = r.stderr if not raw else r.stderr.decode(errors="replace")
        raise Fail(f"git {' '.join(args[:3])} failed: {err.strip()[:300]}")
    return r.stdout


def cache_dir(repo):
    slug = re.sub(r"^(https?://|file://)", "", repo.rstrip("/")).removesuffix(".git")
    slug = "__".join(slug.split("/")[-2:])
    return os.path.join(CACHE, re.sub(r"[^A-Za-z0-9_.-]", "_", slug) + ".git")


def ensure(repo, *shas):
    d = cache_dir(repo)
    if not os.path.isdir(d):
        os.makedirs(CACHE, exist_ok=True)
        git("clone", "-q", "--bare", "--filter=blob:none", repo, d)
    else:
        git("fetch", "-q", "--prune", "origin", "+refs/heads/*:refs/heads/*", cwd=d)
    for s in shas:
        if s and subprocess.run(["git", "cat-file", "-e", f"{s}^{{commit}}"], cwd=d,
                                capture_output=True).returncode != 0:
            git("fetch", "-q", "origin", s, cwd=d)
    return d


def remote_head(repo, ref="HEAD"):
    out = git("ls-remote", repo, ref).split()
    if not out:
        raise Fail(f"{repo}: ref {ref} not found")
    return out[0]


def tree_files(d, commit, path):
    out = git("ls-tree", "-r", "--name-only", commit, "--", path, cwd=d).splitlines()
    return [f for f in out if f == path or f.startswith(path + "/")]


def expected_files(d, e, commit):
    """Map of local relative path -> upstream path, for a copy-mode block."""
    path = split_list(e["path"])[0]
    files = tree_files(d, commit, path)
    if not files:
        raise Fail(f"{e['id']}: {path} does not exist at {commit[:10]}")
    want = set(split_list(e.get("files")))
    out = {}
    for f in files:
        local = os.path.basename(f) if f == path else f[len(path) + 1:]
        if want and local not in want:
            continue
        out[local] = f
    for x in split_list(e.get("extra")):
        if x not in out:
            if not tree_files(d, commit, x):
                raise Fail(f"{e['id']}: extra file {x} does not exist at {commit[:10]}")
            out[os.path.basename(x)] = x
    return out


def blob(d, commit, f):
    return git("show", f"{commit}:{f}", cwd=d, raw=True)


def local_files(dirpath):
    out = []
    for base, dirs, files in os.walk(dirpath):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for f in files:
            p = os.path.relpath(os.path.join(base, f), dirpath)
            if f in IGNORED or f.endswith(".pyc"):
                continue
            out.append(p)
    return sorted(out)


def drift(d, e, commit):
    exp = expected_files(d, e, commit)
    have = set(local_files(e["dir"]))
    missing = sorted(set(exp) - have)
    added = sorted(have - set(exp))
    changed = sorted(f for f in set(exp) & have
                     if open(os.path.join(e["dir"], f), "rb").read() != blob(d, commit, exp[f]))
    return missing, added, changed


# ---------- SOURCES.md mapping (merged mode) ----------

def sources_rows(plugin_dir, key):
    rows = []
    for base, _, files in os.walk(plugin_dir):
        if "SOURCES.md" not in files:
            continue
        skill = os.path.basename(base)
        for line in open(os.path.join(base, "SOURCES.md"), encoding="utf-8"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) < 4 or not cells[1].startswith(key + " "):
                continue
            up = re.sub(r" § .*$", "", cells[2])
            up = re.sub(r" \(.*\)$", "", up).strip()
            rows.append((skill, cells[0], up))
    return rows


def map_changes(e, changed):
    root = split_list(e.get("root"))
    root = root[0] + "/" if root else ""
    rows = sources_rows(e["dir"], e.get("key", ""))
    hits, unmapped = {}, []
    for f in changed:
        r = f[len(root):] if root and f.startswith(root) else f
        found = [(s, part) for s, part, up in rows
                 if up == r or (up.endswith("/") and r.startswith(up))]
        if found:
            hits[f] = found
        else:
            unmapped.append(f)
    return hits, unmapped


# ---------- commands ----------

def cmd_list(args):
    for e in discover():
        if e["index"] < 0:
            print(f"{e['id']:<34} (no upstream block)  {rel(e['file'])}")
            continue
        print(f"{e['id']:<34} {e.get('mode', 'copy'):<6} {e['commit'][:10]}  {e['repo']}  {e['path']}")
    return 0


def cmd_lint(args):
    bad = 0
    entries = discover()
    for e in entries:
        for err in lint_block(e):
            print(f"FAIL {rel(e['file'])} [{e['id']}]: {err}")
            bad += 1
    print(f"blocks: {len(entries)}  problems: {bad}")
    return 1 if bad else 0


def cmd_check(args):
    entries = select(discover(), args)
    behind = drifted = 0
    for e in entries:
        if lint_block(e):
            print(f"{e['id']:<34} invalid block (run: upstream.sh lint)")
            continue
        try:
            head = remote_head(e["repo"], e.get("ref", "HEAD"))
            d = ensure(e["repo"], e["commit"], head)
            paths = split_list(e["path"]) + split_list(e.get("extra"))
            if head == e["commit"]:
                state = "up to date"
            else:
                n = len([x for x in git("diff", "--name-only", e["commit"], head, "--", *paths, cwd=d).splitlines() if x])
                ahead = git("rev-list", "--count", f"{e['commit']}..{head}", cwd=d).strip()
                state = f"{ahead} newer commits, " + (f"{n} files changed under path" if n else "nothing changed under path")
                behind += 1 if n else 0
            note = ""
            if e.get("mode", "copy") == "copy":
                missing, added, changed = drift(d, e, e["commit"])
                if missing or added or changed:
                    drifted += 1
                    note = f"  LOCAL DRIFT: {len(changed)} changed, {len(missing)} missing, {len(added)} extra"
            print(f"{e['id']:<34} {state}{note}")
        except Fail as x:
            print(f"{e['id']:<34} error: {x}")
    print(f"checked {len(entries)}: {behind} with upstream changes, {drifted} with local drift")
    return 0


def take(args, flag, default=None):
    if flag in args:
        i = args.index(flag)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


def one(args):
    if len(args) != 1:
        raise Fail("name exactly one skill or block (see: upstream.sh list)")
    picked = select(discover(), args)
    if len(picked) != 1:
        raise Fail(f"{args[0]} has {len(picked)} blocks; name one: " + ", ".join(e["id"] for e in picked))
    e = picked[0]
    errs = lint_block(e)
    if errs:
        raise Fail(f"{e['id']}: " + "; ".join(errs))
    return e


def cmd_diff(args):
    to = take(args, "--to")
    stat = "--stat" in args
    args = [a for a in args if a != "--stat"]
    e = one(args)
    to = to or remote_head(e["repo"], e.get("ref", "HEAD"))
    d = ensure(e["repo"], e["commit"], to)
    paths = split_list(e["path"]) + split_list(e.get("extra"))
    print(f"# {e['id']}: {e['repo']} {e['commit'][:10]}..{to[:10]}")
    if to == e["commit"]:
        print("up to date")
        return 0
    print(git("log", "--oneline", f"{e['commit']}..{to}", "--", *paths, cwd=d) or "(no commits touch the path)")
    changed = [x for x in git("diff", "--name-only", e["commit"], to, "--", *paths, cwd=d).splitlines() if x]
    print(git("diff", "--stat", e["commit"], to, "--", *paths, cwd=d))
    if e.get("mode") == "merged":
        hits, unmapped = map_changes(e, changed)
        print("## Where each change goes (from SOURCES.md rows)")
        for f, found in hits.items():
            print(f"- {f}")
            for skill, part in found:
                print(f"    -> {skill}: {part}")
        if unmapped:
            print("## No SOURCES.md row (new upstream file, or a file copied without a row): decide by hand")
            for f in unmapped:
                print(f"- {f}")
        print(f"\nMerged mode never auto-updates. Carry each change by hand, then set commit: {to}")
    if not stat:
        print(git("diff", e["commit"], to, "--", *paths, cwd=d))
    return 0


def set_commit(e, new):
    text = open(e["file"], encoding="utf-8").read()
    blocks = list(BLOCK.finditer(text))
    m = blocks[e["index"]]
    body = re.sub(r"(?m)^(commit:\s*)[0-9a-f]{40}", lambda x: x.group(1) + new, m.group(1), count=1)
    open(e["file"], "w", encoding="utf-8").write(text[:m.start(1)] + body + text[m.end(1):])


def auditor_reviewed():
    """The vendored auditor runs only after its own UPSTREAM.md records a dated review."""
    up = os.path.join(os.path.dirname(os.path.dirname(AUDITOR)), "UPSTREAM.md")
    if not (os.path.isfile(AUDITOR) and os.path.isfile(up)):
        return False
    return has_dated_review(open(up, encoding="utf-8").read())


def has_dated_review(text):
    """A dated entry in `## Review` (or a legacy `Reviewed <date>` line) that is not pending."""
    sec = re.search(r"(?ms)^## Review\b.*?(?=^## |\Z)", text)
    lines = sec.group(0).splitlines() if sec else []
    lines += re.findall(r"(?mi)^Review(?:ed)?\b.*$", text)
    return any(re.search(r"\d{4}-\d{2}-\d{2}", x) and "pending" not in x.lower() for x in lines)


def render_upstream(name, block, licence_line, vendored, intro="", reviews=(), limits=(), update_extra=""):
    """The UPSTREAM.md layout every copy-mode skill shares (same sections as marketing-skills)."""
    b = dict(x.split(": ", 1) for x in block)
    files = f" (only `{b['files']}`)" if b.get("files") else ""
    extra = f", plus the repository `{b['extra']}`" if b.get("extra") else ""
    out = ["# Upstream", "", "```upstream", *block, "```", "",
           "| | Source |", "|---|---|",
           f"| Repository | {b['repo']} |",
           f"| Path taken | `{b['path']}/`{files}{extra} |",
           "| Commit | see the block above |",
           f"| Licence | {licence_line} |", "",
           "Keep `LICENSE` with any copy.", "",
           f"Vendored on {vendored}{intro}", "",
           "## What changed from upstream", "",
           "- **Nothing.** Every file is the upstream file at the pinned commit; only this file is ours.",
           f"  `bash .claude/scripts/upstream.sh check {name}` proves it (it reports any local drift).",
           "- **No SOURCES.md.** That table is for merged skills, where parts come from different sources. Here",
           "  one source supplies every file unchanged, so the block above is the whole provenance.", "",
           "## Review", ""]
    out += [f"- {r}" for r in reviews] or ["- pending: security + fit review (read-only; no scripts run)."]
    out += ["", "## Limits in this workspace", ""]
    out += [f"- {x}" for x in limits] or ["- None recorded yet beyond the workspace rules."]
    out += ["", "## Updating", "",
            f"1. `bash .claude/scripts/upstream.sh diff {name}` — read every changed line, scripts in full.",
            f"2. `bash .claude/scripts/upstream.sh pull {name}` — copies the files, bumps the commit, runs the scan."]
    if update_extra:
        out.append(f"3. {update_extra}")
    out.append(f"{4 if update_extra else 3}. Add a dated entry under Review: what changed, the scan result, and why each finding is or is")
    out.append("   not real.")
    return "\n".join(out) + "\n"


def audit(dirpath):
    if not auditor_reviewed():
        print("security scan: skipped (skill-security-auditor missing or not reviewed yet); scan by hand")
        return
    r = subprocess.run([sys.executable, "-I", AUDITOR, dirpath], capture_output=True, text=True)
    tail = (r.stdout or r.stderr).strip().splitlines()[-12:]
    print("security scan (skill-security-auditor, static, read-only):")
    print("\n".join("  " + x for x in tail))


def write_files(d, e, commit, exp):
    for f, up in exp.items():
        p = os.path.join(e["dir"], f)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(blob(d, commit, up))


def report_scripts(paths):
    code = [p for p in paths if not p.endswith((".md", ".txt", ".json", ".yaml", ".yml", ".png", ".jpg", ".svg"))
            and not os.path.basename(p).upper().startswith("LICENSE")]
    if code:
        print("new or changed code (read every line before its first run):")
        for p in code:
            print(f"  {p}")


def cmd_pull(args):
    to = take(args, "--to")
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    e = one(args)
    if e.get("mode") == "merged":
        raise Fail(f"{e['id']} is merged (adapted): run `upstream.sh diff {e['id']}` and carry changes by hand")
    to = to or remote_head(e["repo"], e.get("ref", "HEAD"))
    d = ensure(e["repo"], e["commit"], to)
    if to == e["commit"]:
        print(f"{e['id']}: up to date ({to[:10]})")
        return 0
    missing, added, changed = drift(d, e, e["commit"])
    if (missing or added or changed) and not force:
        raise Fail(f"{e['id']}: local copy differs from the pinned upstream "
                   f"(changed {changed}, missing {missing}, extra {added}). "
                   "Keep local edits elsewhere, or pass --force to overwrite them.")
    old = expected_files(d, e, e["commit"])
    new = expected_files(d, e, to)
    for f in set(old) - set(new):
        os.remove(os.path.join(e["dir"], f))
    write_files(d, e, to, new)
    set_commit(e, to)
    touched = sorted(f for f in new if f not in old or blob(d, e["commit"], old[f]) != blob(d, to, new[f]))
    print(f"{e['id']}: {e['commit'][:10]} -> {to[:10]}  "
          f"{len(touched)} files added or changed, {len(set(old) - set(new))} removed")
    report_scripts(touched)
    audit(e["dir"])
    print("next: review `git diff`, update the review date in UPSTREAM.md, run the skill's own tests")
    return 0


def licence_name(text):
    head = text[:400].lower()
    for needle, name in (("mit license", "MIT"), ("apache license", "Apache-2.0"),
                         ("attribution 4.0", "CC-BY-4.0"), ("bsd 3-clause", "BSD-3-Clause"),
                         ("isc license", "ISC")):
        if needle in head:
            return name
    return ""


def cmd_add(args):
    name = take(args, "--name")
    commit = take(args, "--commit")
    extra = take(args, "--extra")
    licence = take(args, "--licence")
    if len(args) != 2:
        raise Fail("usage: upstream.sh add <repo-url> <path> [--name N] [--commit SHA] [--extra FILE] [--licence L]")
    repo, path = args[0], args[1].strip("/")
    name = name or os.path.basename(path)
    dest = os.path.join(ROOT, ".claude", "skills", name)
    if os.path.exists(dest):
        raise Fail(f"{rel(dest)} already exists")
    commit = commit or remote_head(repo)
    d = ensure(repo, commit)
    in_path = [f for f in tree_files(d, commit, path) if os.path.basename(f).upper().startswith("LICENSE")]
    if extra is None and not in_path:
        roots = [f for f in git("ls-tree", "--name-only", commit, cwd=d).splitlines()
                 if f.upper().startswith("LICENSE")]
        extra = roots[0] if roots else ""
    lic_src = in_path[0] if in_path else extra
    if not lic_src:
        raise Fail("no LICENSE in the path or the repo root: do not vendor without a licence")
    licence = licence or licence_name(blob(d, commit, lic_src).decode(errors="replace")) or "check-by-hand"
    e = {"id": name, "name": name, "dir": dest, "path": path, "extra": extra or "", "repo": repo}
    exp = expected_files(d, e, commit)
    os.makedirs(dest)
    write_files(d, e, commit, exp)
    lines = [f"repo: {repo}", f"path: {path}", f"commit: {commit}", "mode: copy", f"licence: {licence}"]
    if extra:
        lines.append(f"extra: {extra}")
    today = datetime.date.today().isoformat()
    copyright = next((x.strip() for x in blob(d, commit, lic_src).decode(errors="replace").splitlines()
                      if x.strip().lower().startswith("copyright")), "")
    open(os.path.join(dest, "UPSTREAM.md"), "w", encoding="utf-8").write(render_upstream(
        name, lines, f"{licence}, {copyright}" if copyright else licence, today,
        intro=": upstream name and content kept. Credit: <author>, <repository name>."))
    print(f"vendored {len(exp)} files into {rel(dest)} at {commit[:10]} ({licence})")
    report_scripts(sorted(exp))
    audit(dest)
    print("next: fill Credit and Review in UPSTREAM.md, run roster.sh, add notes on overlaps with existing skills")
    return 0


COMMANDS = {"list": cmd_list, "lint": cmd_lint, "check": cmd_check, "diff": cmd_diff,
            "pull": cmd_pull, "add": cmd_add}


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        print(__doc__.split("Commands (run through upstream.sh):")[1].split("Upstream clones")[0])
        return 2
    try:
        return COMMANDS[argv[0]](list(argv[1:]))
    except Fail as x:
        print(f"error: {x}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
