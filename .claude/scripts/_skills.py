"""Skill authoring: catch collisions early, and keep merged skill libraries credited and checkable.

Commands (run through skills.sh):
    overlap <SKILL.md or folder> | --text "<name and description>"
                        existing skills with the same name (collision) or a similar topic
    new-library <name> --source <key>=<repo-url>[@<sha>][#<root>] [--source ...] [--title "<one line>"]
                        scaffold plugins/<name>/ like marketing-skills, sources and credit filled in
    validate <plugin>   frontmatter, unique names, links, Python and JavaScript syntax (offline)
    sources check <plugin> [--sources DIR]
                        every SKILL.md section and file has a SOURCES.md row; `as is` rows match upstream
    sources generate <plugin> <skill> <key> <upstream-path> [--note TEXT] [--sources DIR]
                        write SOURCES.md for a skill that comes from one source
    snapshot <plugin>   export each source at its pinned commit; prints the folder `sources` uses
    index <plugin>      rebuild the skill table in the plugin README

A merged library names its sources in UPSTREAM.md blocks (`mode: merged`, `key`, `credit`, `root`) and
may keep `library.json` with `categories` (README table) and `context` (a shared context file only its
owner skill may name directly). Nothing here runs upstream code.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _upstream as U  # noqa: E402

ROOT = U.ROOT
DETAIL_DIRS = ("references", "scripts", "assets", "evals")
GROUP_MIN = 6
LINK = re.compile(r"\]\(([^)\s]+)\)")
START, END = "<!-- SKILLS:START -->", "<!-- SKILLS:END -->"
STOP = set("""a an and or the of to for in on at by with from into as is are be this that these those it its use
used using when what which who how your you their them they not no only also any each every than then so if
skill skills user users want wants mentions mention help helps see like etc e.g about across more most""".split())


class Fail(Exception):
    pass


# ---------- shared readers ----------

def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    data, parent = {}, None
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if line.startswith((" ", "\t")) and parent:
            key, _, value = line.strip().partition(":")
            data.setdefault(parent, {})[key.strip()] = value.strip().strip("\"'")
            continue
        key, _, value = line.partition(":")
        key, value = key.strip(), value.strip()
        parent = key if value == "" else None
        data[key] = {} if value == "" else value.strip("\"'")
    return data


def plugin_dir(name):
    d = os.path.join(ROOT, "plugins", name)
    if not os.path.isdir(os.path.join(d, "skills")):
        raise Fail(f"plugins/{name}/skills not found")
    return d


def library(name):
    d = plugin_dir(name)
    up = os.path.join(d, "UPSTREAM.md")
    blocks = U.parse_blocks(open(up, encoding="utf-8").read()) if os.path.isfile(up) else []
    blocks = [b for b in blocks if b.get("key")]
    cfg_path = os.path.join(d, "library.json")
    cfg = json.load(open(cfg_path, encoding="utf-8")) if os.path.isfile(cfg_path) else {}
    return {"name": name, "dir": d, "skills": os.path.join(d, "skills"), "blocks": blocks, "config": cfg}


def all_skills():
    """Every skill in this repository: workspace skills and plugin skills."""
    import glob
    out = []
    for pat in (".claude/skills/*/SKILL.md", "plugins/*/skills/*/SKILL.md"):
        for f in sorted(glob.glob(os.path.join(ROOT, pat))):
            fm = frontmatter(open(f, encoding="utf-8").read()) or {}
            out.append({"name": fm.get("name") or os.path.basename(os.path.dirname(f)),
                        "description": fm.get("description", ""), "file": os.path.relpath(f, ROOT)})
    return out


# ---------- overlap ----------

def tokens(text):
    words = re.findall(r"[a-z][a-z0-9+#.-]*[a-z0-9+#]|[a-z]", text.lower())
    return {w for w in words if w not in STOP and len(w) > 2}


def cmd_overlap(args, quiet=False):
    text = None
    if args and args[0] == "--text":
        name, text = "", " ".join(args[1:])
    elif len(args) == 1:
        p = args[0]
        p = os.path.join(p, "SKILL.md") if os.path.isdir(p) else p
        if not os.path.isfile(p):
            raise Fail(f"{args[0]}: no SKILL.md")
        fm = frontmatter(open(p, encoding="utf-8").read()) or {}
        name = fm.get("name") or os.path.basename(os.path.dirname(os.path.abspath(p)))
        text = f"{name} {name.replace('-', ' ')} {fm.get('description', '')}"
        own = os.path.abspath(p)
    else:
        raise Fail('usage: skills.sh overlap <SKILL.md or folder> | --text "<name and description>"')
    mine = tokens(text)
    rows, clash = [], []
    for s in all_skills():
        if args[0] != "--text" and os.path.abspath(os.path.join(ROOT, s["file"])) == own:
            continue
        if name and s["name"] == name:
            clash.append(s)
        theirs = tokens(f"{s['name']} {s['name'].replace('-', ' ')} {s['description']}")
        shared = mine & theirs
        if len(shared) >= 3:
            score = len(shared) / min(len(mine), len(theirs))
            rows.append((score, s, shared))
    rows.sort(key=lambda r: (-r[0], -len(r[2])))
    def level(score):
        return "high" if score >= 0.5 else "medium" if score >= 0.3 else "low"

    if not quiet or clash or (rows and level(rows[0][0]) != "low"):
        for s in clash:
            print(f"COLLISION  same name `{s['name']}` already at {s['file']}")
        for score, s, shared in rows[:5]:
            if quiet and level(score) == "low":
                continue
            words = ", ".join(sorted(shared)[:6])
            print(f"{level(score):<6} {score:.2f}  {s['name']:<28} {s['file']}\n         shared: {words}")
        if not rows and not clash:
            print("no existing skill shares 3 or more topic words")
        print("Decide per row: same topic -> merge into one skill with a SOURCES.md table; "
              "different job -> keep both and write the boundary in each description.")
    return 1 if clash else 0


# ---------- validate ----------

def cmd_validate(args):
    lib = library(one_arg(args, "validate <plugin>"))
    ctx = lib["config"].get("context") or {}
    errors, warnings, names = [], [], {}
    for entry in sorted(os.listdir(lib["skills"])):
        folder = os.path.join(lib["skills"], entry)
        if not os.path.isdir(folder):
            continue
        skill_md = os.path.join(folder, "SKILL.md")
        if not os.path.isfile(skill_md):
            errors.append(f"{entry}: SKILL.md missing")
            continue
        meta = frontmatter(open(skill_md, encoding="utf-8").read())
        if meta is None:
            errors.append(f"{entry}: frontmatter missing or not closed")
            continue
        name, desc = meta.get("name", ""), meta.get("description", "")
        if name != entry:
            errors.append(f'{entry}: name "{name}" differs from folder')
        if name in names:
            errors.append(f'{entry}: duplicate name "{name}"')
        names[name] = entry
        if not desc:
            errors.append(f"{entry}: description empty")
        elif len(desc) > 1024:
            errors.append(f"{entry}: description {len(desc)} chars (max 1024)")
        md_meta = meta.get("metadata") if isinstance(meta.get("metadata"), dict) else {}
        if not md_meta.get("version"):
            warnings.append(f"{entry}: metadata.version missing")
        if not md_meta.get("sources"):
            warnings.append(f"{entry}: metadata.sources missing")
        lines = sum(1 for _ in open(skill_md, encoding="utf-8"))
        if lines > 600:
            warnings.append(f"{entry}: SKILL.md has {lines} lines")
    owner = os.path.join("skills", ctx["owner"]) + os.sep if ctx.get("owner") else None
    for base, _, files in os.walk(lib["dir"]):
        if os.sep + ".git" in base or os.sep + "node_modules" in base:
            continue
        for fname in files:
            path = os.path.join(base, fname)
            rel = os.path.relpath(path, lib["dir"])
            if fname.endswith(".md"):
                text = open(path, encoding="utf-8", errors="ignore").read()
                for target in LINK.findall(text):
                    if target.startswith(("http://", "https://", "mailto:", "#", "<", "/")) or "{" in target:
                        continue  # web URLs, anchors, templates and example site paths such as /pricing
                    if "." not in target and "/" not in target:
                        continue  # placeholders in examples, such as [text](link)
                    clean = target.split("#")[0].split("?")[0]
                    if clean and not os.path.exists(os.path.normpath(os.path.join(base, clean))):
                        errors.append(f"{rel}: broken link {target}")
                if ctx.get("file") and ctx["file"] in text and rel.startswith("skills" + os.sep) \
                        and not (owner and rel.startswith(owner)):
                    warnings.append(f"{rel}: mentions {ctx['file']} directly")
            elif fname.endswith(".py"):
                try:
                    compile(open(path, encoding="utf-8").read(), path, "exec")
                except SyntaxError as exc:
                    errors.append(f"{rel}: python does not compile (line {exc.lineno}: {exc.msg})")
            elif fname.endswith((".js", ".mjs", ".cjs")) and shutil.which("node"):
                result = subprocess.run(["node", "--check", path], capture_output=True, text=True)
                if result.returncode != 0:
                    errors.append(f"{rel}: node --check failed")
    print(f"skills: {len(names)}  errors: {len(errors)}  warnings: {len(warnings)}")
    for item in errors:
        print("ERROR  ", item)
    for item in warnings:
        print("WARN   ", item)
    return 1 if errors else 0


# ---------- sources ----------

def sections(path):
    text = open(path, encoding="utf-8").read()
    out, current, buf, body = {}, None, [], text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        out["frontmatter"] = text[:end + 4]
        body = text[end + 4:]
    fenced = False
    for line in body.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fenced = not fenced
        if line.startswith("## ") and not fenced:
            if current is not None:
                out[current] = "\n".join(buf).strip()
            current, buf = line[3:].strip(), [line]
        elif current is not None:
            buf.append(line)
    if current is not None:
        out[current] = "\n".join(buf).strip()
    return out


def detail_files(sdir):
    files = []
    for sub in DETAIL_DIRS:
        for base, _, names in os.walk(os.path.join(sdir, sub)):
            files += [os.path.relpath(os.path.join(base, n), sdir) for n in names
                      if not n.startswith(".") and n != "__pycache__" and not n.endswith(".pyc")]
    return sorted(files)


def repos_line(lib):
    parts = []
    for b in lib["blocks"]:
        root = U.split_list(b.get("root"))
        where = f", folder {root[0]}/" if root else ""
        credit = f", {b['credit']}" if b.get("credit") else ""
        parts.append(f"{b['key']} = {b['repo'].removesuffix('.git')}{where} ({b.get('licence', '?')}{credit})")
    return " · ".join(parts)


def prefetch(d, commit, root):
    """A blobless clone fetches each missing file one by one on checkout; fetch them in one batch."""
    out = U.git("rev-list", "--objects", "--missing=print", commit, "--", root or ".", cwd=d)
    oids = [x[1:].strip() for x in out.splitlines() if x.startswith("?")]
    for i in range(0, len(oids), 1000):
        subprocess.run(["git", "-c", "fetch.negotiationAlgorithm=noop", "fetch", "-q", "--no-tags",
                        "--no-write-fetch-head", "--filter=blob:none", "origin", *oids[i:i + 1000]],
                       cwd=d, capture_output=True, text=True)


def snapshot(lib):
    """Export every merged source at its pinned commit; returns {key: folder of its root}."""
    out = {}
    for b in lib["blocks"]:
        root = (U.split_list(b.get("root")) or [""])[0]
        dest = os.path.join(U.CACHE, "snapshots", lib["name"], f"{b['key']}-{b['commit'][:7]}")
        if not os.path.isdir(dest):
            d = U.ensure(b["repo"], b["commit"])
            prefetch(d, b["commit"], root)
            tmp = tempfile.mkdtemp(prefix="snap-", dir=os.path.dirname(U.CACHE))
            env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, ".index"))
            work = os.path.join(tmp, "tree")
            os.makedirs(work)
            r = subprocess.run(["git", "--git-dir", d, "--work-tree", work, "checkout", b["commit"], "--", root or "."],
                               capture_output=True, text=True, env=env)
            if r.returncode != 0:
                shutil.rmtree(tmp, ignore_errors=True)
                raise Fail(f"snapshot of {b['key']} failed: {r.stderr.strip()[:200]}")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(os.path.join(work, root) if root else work, dest)
            shutil.rmtree(tmp, ignore_errors=True)
        out[b["key"]] = dest
    return out


def snap_dirs(lib, given):
    if given:
        return {b["key"]: os.path.join(given, b["key"]) for b in lib["blocks"]}
    return snapshot(lib)


def parse_table(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Part "):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4:
            rows.append(cells[:4])
    return rows


def sources_check(lib, given):
    import filecmp
    snaps = snap_dirs(lib, given) if (given or lib["blocks"]) else {}
    problems, total = [], 0
    for skill in sorted(os.listdir(lib["skills"])):
        sdir = os.path.join(lib["skills"], skill)
        if not os.path.isdir(sdir):
            continue
        total += 1
        src = os.path.join(sdir, "SOURCES.md")
        if not os.path.isfile(src):
            problems.append(f"{skill}: SOURCES.md missing")
            continue
        rows = parse_table(src)
        parts = [r[0] for r in rows]
        skill_md = os.path.join(sdir, "SKILL.md")
        if "Sources and credits: [SOURCES.md](SOURCES.md)" not in open(skill_md, encoding="utf-8").read():
            problems.append(f"{skill}: SKILL.md lacks the SOURCES.md link line")
        mine = sections(skill_md)
        for name in mine:
            label = "frontmatter" if name == "frontmatter" else f"SKILL.md § {name}"
            if not any(p == label or p.startswith(label + " ") for p in parts):
                problems.append(f'{skill}: no row for "{label}"')
        folder_rows = [p.split(" (")[0].rstrip("/") for p in parts if p.endswith("files)")]
        for rel in detail_files(sdir):
            if any(p == rel or p.startswith(rel + " ") for p in parts) or any(rel.startswith(f + os.sep) for f in folder_rows):
                continue
            problems.append(f"{skill}: no row for file {rel}")
        for part, origin, upstream, changed in rows:
            if not changed.startswith(("as is", "edited", "new")):
                problems.append(f'{skill}: "{part}" has an unknown status "{changed}"')
            key = origin.split(" ")[0]
            if not (changed.startswith("as is") and key in snaps and upstream not in ("—", "")):
                continue
            up_path, _, heading = upstream.partition(" § ")
            full = os.path.join(snaps[key], up_path)
            if not os.path.exists(full):
                problems.append(f'{skill}: "{part}" points to missing upstream {upstream}')
            elif heading and part.startswith("SKILL.md § "):
                own = mine.get(part[len("SKILL.md § "):])  # None for a row that covers part of a section
                if own is not None and own != sections(full).get(heading):
                    problems.append(f'{skill}: "{part}" says as is but differs from {upstream}')
            elif os.path.isfile(full) and os.path.isfile(os.path.join(sdir, part)):
                if not filecmp.cmp(os.path.join(sdir, part), full, shallow=False):
                    problems.append(f'{skill}: "{part}" says as is but differs from {upstream}')
    print(f"skills: {total}  problems: {len(problems)}")
    for p in problems:
        print("PROBLEM", p)
    return 1 if problems else 0


def sources_generate(lib, skill, key, upstream, note, given):
    import filecmp
    block = next((b for b in lib["blocks"] if b["key"] == key), None)
    if not block:
        raise Fail(f"no merged source with key `{key}` in plugins/{lib['name']}/UPSTREAM.md")
    sdir = os.path.join(lib["skills"], skill)
    up_dir = os.path.join(snap_dirs(lib, given)[key], upstream)
    if not os.path.isfile(os.path.join(up_dir, "SKILL.md")):
        raise Fail(f"{upstream}/SKILL.md not found in the {key} snapshot")
    tag = f"{key} `{os.path.basename(upstream.rstrip('/'))}` @{block['commit'][:7]}"
    rows = []
    mine, theirs = sections(os.path.join(sdir, "SKILL.md")), sections(os.path.join(up_dir, "SKILL.md"))
    for name, text in mine.items():
        part = "frontmatter" if name == "frontmatter" else f"SKILL.md § {name}"
        if name == "Sources and credits" or text.startswith("Sources and credits:"):
            continue
        if name in theirs:
            where = f"{upstream}/SKILL.md" + ("" if name == "frontmatter" else f" § {name}")
            rows.append((part, tag, where, "as is" if text == theirs[name] else f"edited: {note or 'central pass'}"))
        else:
            rows.append((part, "merge", "—", f"new: {note or 'added in the merge'}"))
    grouped = {}
    for rel in detail_files(sdir):
        top = rel.split(os.sep)[:2]
        k = os.sep.join(top) if len(top) == 2 and os.path.isdir(os.path.join(sdir, *top)) else None
        grouped.setdefault(k, []).append(rel)
    for k, files in sorted(grouped.items(), key=lambda kv: kv[0] or ""):
        if k and len(files) >= GROUP_MIN:
            diff = [f for f in files if not os.path.exists(os.path.join(up_dir, f))
                    or not filecmp.cmp(os.path.join(sdir, f), os.path.join(up_dir, f), shallow=False)]
            rows.append((f"{k}/ ({len(files)} files)", tag, f"{upstream}/{k}/",
                         "as is" if not diff else f"edited: {len(diff)} of {len(files)} files"))
            continue
        for rel in files:
            up = os.path.join(up_dir, rel)
            if not os.path.exists(up):
                rows.append((rel, "merge", "—", f"new: {note or 'added in the merge'}"))
            else:
                same = filecmp.cmp(os.path.join(sdir, rel), up, shallow=False)
                rows.append((rel, tag, f"{upstream}/{rel}", "as is" if same else f"edited: {note or 'central pass'}"))
    lines = [f"# Sources: {skill}", "", "| Part | From | Upstream file | Changed here |", "|---|---|---|---|"]
    lines += [f"| {a} | {b} | {c} | {d} |" for a, b, c, d in rows]
    lines += ["", repos_line(lib), ""]
    open(os.path.join(sdir, "SOURCES.md"), "w", encoding="utf-8").write("\n".join(lines))
    print(f"{skill}: {len(rows)} rows")
    return 0


def take(args, flag, default=None):
    if flag in args:
        i = args.index(flag)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


def one_arg(args, usage):
    if len(args) != 1:
        raise Fail(f"usage: skills.sh {usage}")
    return args[0]


def cmd_sources(args):
    given = take(args, "--sources")
    note = take(args, "--note", "")
    if args[:1] == ["check"] and len(args) == 2:
        return sources_check(library(args[1]), given)
    if args[:1] == ["generate"] and len(args) == 5:
        return sources_generate(library(args[1]), args[2], args[3], args[4], note, given)
    raise Fail("usage: skills.sh sources check <plugin> [--sources DIR] | "
               "sources generate <plugin> <skill> <key> <upstream-path> [--note TEXT] [--sources DIR]")


def cmd_snapshot(args):
    for key, d in snapshot(library(one_arg(args, "snapshot <plugin>"))).items():
        print(f"{key}: {d}")
    return 0


# ---------- index ----------

def cmd_index(args):
    lib = library(one_arg(args, "index <plugin>"))
    keys = [b["key"] for b in lib["blocks"]]
    credit = {b["key"]: b.get("credit") or b["key"] for b in lib["blocks"]}

    def origin(sources):
        have = [k for k in keys if f"{k}:" in sources]
        if len(have) > 1:
            return "Both" if len(keys) == 2 else "Merged"
        return credit[have[0]] if have else "This library"

    skills = {}
    for name in sorted(os.listdir(lib["skills"])):
        path = os.path.join(lib["skills"], name, "SKILL.md")
        if os.path.isfile(path):
            fm = frontmatter(open(path, encoding="utf-8").read()) or {}
            skills[name] = (fm.get("description", ""), (fm.get("metadata") or {}).get("sources", ""))
    cats = [(c[0], c[1]) for c in lib["config"].get("categories", [])]
    rest = sorted(set(skills) - {n for _, ns in cats for n in ns})
    out = []
    for title, names in cats + [("Other" if cats else "Skills", rest)]:
        rows = [n for n in names if n in skills]
        if not rows:
            continue
        out += [f"### {title}", "", "| Skill | What it does | From |", "|---|---|---|"]
        for n in rows:
            desc, src = skills[n]
            first = re.split(r"(?<=[.!?])\s", desc, maxsplit=1)[0]
            first = first if len(first) <= 170 else first[:167].rstrip() + "..."
            out.append(f"| [`{n}`](skills/{n}/SKILL.md) | {first.replace('|', '/')} | {origin(src)} |")
        out.append("")
    merged = sum(1 for _, s in skills.values() if origin(s) in ("Both", "Merged"))
    parts = [f"{merged} merged from {'both libraries' if len(keys) == 2 else 'several sources'}"] if len(keys) > 1 else []
    parts += [f"{sum(1 for _, s in skills.values() if origin(s) == credit[k])} from {credit[k]} only" for k in keys]
    own = sum(1 for _, s in skills.values() if origin(s) == "This library")
    if own:
        parts.append(f"{own} written here")
    header = f"{len(skills)} skills: " + ", ".join(parts) + "."
    block = "\n".join([START, f"<!-- Generated by `bash .claude/scripts/skills.sh index {lib['name']}` from each SKILL.md. "
                       "Do not edit by hand. -->", "", header, ""] + out + [END])
    readme_path = os.path.join(lib["dir"], "README.md")
    readme = open(readme_path, encoding="utf-8").read()
    if START not in readme or END not in readme:
        raise Fail("README.md has no SKILLS markers")
    readme = readme[:readme.index(START)] + block + readme[readme.index(END) + len(END):]
    open(readme_path, "w", encoding="utf-8").write(readme)
    print(header)
    return 0


# ---------- new-library ----------

def parse_source(spec):
    m = re.match(r"^([a-z][a-z0-9-]*)=([^@#]+?)(?:@([0-9a-f]{7,40}))?(?:#(.+))?$", spec)
    if not m:
        raise Fail(f"bad --source {spec!r}; use key=https://github.com/owner/repo[@sha][#folder]")
    return m.group(1), m.group(2), m.group(3), (m.group(4) or "").strip("/")


def cmd_new_library(args):
    title = take(args, "--title", "")
    specs = []
    while "--source" in args:
        specs.append(take(args, "--source"))
    name = one_arg(args, 'new-library <name> --source key=<repo>[@sha][#folder] [...] [--title "..."]')
    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        raise Fail("library name: lowercase letters, digits and hyphens")
    if not specs:
        raise Fail("name at least one --source; a library without an upstream is just .claude/skills")
    dest = os.path.join(ROOT, "plugins", name)
    if os.path.exists(dest):
        raise Fail(f"plugins/{name} already exists")
    blocks, licences, credits = [], [], []
    for spec in specs:
        key, repo, sha, root = parse_source(spec)
        sha = U.git("rev-parse", sha, cwd=U.ensure(repo, sha)).strip() if sha else U.remote_head(repo)
        d = U.ensure(repo, sha)
        lic = next((f for f in U.git("ls-tree", "--name-only", sha, cwd=d).splitlines()
                    if f.upper().startswith("LICENSE")), "")
        if not lic:
            raise Fail(f"{repo} has no LICENSE at its root: do not merge content without a licence")
        text = U.blob(d, sha, lic).decode(errors="replace")
        licence = U.licence_name(text) or "check-by-hand"
        copyright = next((x.strip() for x in text.splitlines() if x.strip().lower().startswith("copyright")), "")
        credit = re.sub(r"^copyright\s*(\(c\)|©)?\s*[\d\s,–-]*", "", copyright, flags=re.I).strip() or key
        blocks.append(["```upstream", f"repo: {repo}", f"path: {root or '.'}"] + ([f"root: {root}"] if root else [])
                      + [f"commit: {sha}", "mode: merged", f"key: {key}", f"credit: {credit}", f"licence: {licence}", "```"])
        licences.append(text)
        credits.append((key, repo, root, sha, licence, credit))
    tpl = os.path.join(ROOT, "templates", "skill-library")
    shutil.copytree(tpl, dest)
    rows = "\n".join(f"| `{k}` | {r} | `{root or '.'}` | `{s[:7]}` | {lic}, {c} |" for k, r, root, s, lic, c in credits)
    fill = {"{{name}}": name, "{{title}}": title or f"Merged skill library: {name}",
            "{{sources_table}}": rows, "{{blocks}}": "\n\n".join("\n".join(b) for b in blocks),
            "{{credits}}": ", ".join(c for *_, c in credits)}
    for base, _, files in os.walk(dest):
        for f in files:
            p = os.path.join(base, f)
            text = open(p, encoding="utf-8").read()
            for k, v in fill.items():
                text = text.replace(k, v)
            open(p, "w", encoding="utf-8").write(text)
    with open(os.path.join(dest, "LICENSE"), "a", encoding="utf-8") as f:
        for (key, repo, *_), text in zip(credits, licences):
            f.write(f"\n\n---- Upstream licence: {key} ({repo}) ----\n\n{text.strip()}\n")
    mp = os.path.join(ROOT, ".claude-plugin", "marketplace.json")
    market = json.load(open(mp, encoding="utf-8"))
    market["plugins"].append({"name": name, "description": title or f"Merged skill library: {name}",
                              "source": f"./plugins/{name}"})
    open(mp, "w", encoding="utf-8").write(json.dumps(market, indent=2, ensure_ascii=False) + "\n")
    print(f"created plugins/{name} with {len(credits)} source(s); registered in .claude-plugin/marketplace.json")
    print("next: read CONTRIBUTING.md (Path C), then fill docs/MAPPING.md before copying any skill")
    return 0


COMMANDS = {"overlap": cmd_overlap, "validate": cmd_validate, "sources": cmd_sources, "snapshot": cmd_snapshot,
            "index": cmd_index, "new-library": cmd_new_library}


def main(argv):
    if not argv or argv[0] not in COMMANDS:
        print(__doc__.split("Commands (run through skills.sh):")[1].split("A merged library")[0])
        return 2
    try:
        return COMMANDS[argv[0]](list(argv[1:]))
    except (Fail, U.Fail) as x:
        print(f"error: {x}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
