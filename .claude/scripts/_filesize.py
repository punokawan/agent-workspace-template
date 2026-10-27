#!/usr/bin/env python3
"""File-size warnings for verify.sh — the `file-size` rule module, never a failure.

    _filesize.py <project> <repo> <dir>

Prints one line per source file that this branch (committed, uncommitted or untracked) made
larger than the stack's `file_size.limit`, or added over it. The base is the merge-base with
the repo's integration branch, else HEAD. A file already over the limit and not grown stays
silent. Silent too when the project's rules do not include `file-size`.
"""
import fnmatch, os, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _project, _rules


def git(d, *args):
    r = subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def lines(text):
    return text.count("\n") + (1 if text and not text.endswith("\n") else 0)


def oversized(d, fs, code_ext, markers, integration):
    limit = fs.get("limit")
    if not limit:
        return []
    base = (git(d, "merge-base", "HEAD", integration) or git(d, "rev-parse", "HEAD") or "").strip()
    pairs = []  # (path at base or None, path now)
    if base:
        for row in (git(d, "diff", "--name-status", "-M", base) or "").splitlines():
            parts = row.split("\t")
            if parts[0].startswith("D"):
                continue
            pairs.append((parts[1], parts[-1]))
    for p in (git(d, "ls-files", "--others", "--exclude-standard") or "").splitlines():
        pairs.append((None, p))
    out = []
    for old, new in pairs:
        if (not any(new.endswith(e) for e in code_ext) or any(m in new for m in markers)
                or any(fnmatch.fnmatch(new, x) or fnmatch.fnmatch("/" + new, x)
                       for x in fs.get("exclude", []))):
            continue
        try:
            now = lines(open(os.path.join(d, new), encoding="utf-8", errors="replace").read())
        except OSError:
            continue
        was = lines(git(d, "show", f"{base}:{old}") or "") if base and old else 0
        if now > limit and now > was:
            how = f"was {was}" if was else "new file"
            out.append(f"{new}: {now} lines ({how}, limit {limit})")
    return out


def main(argv):
    if len(argv) != 3:
        print("usage: _filesize.py <project> <repo> <dir>", file=sys.stderr)
        return 2
    project, repo, d = argv
    if "file-size" not in _rules.chosen(project)[1]:
        return 0
    rec = _project.find_repo(project, repo)
    for w in oversized(d, rec.get("file_size", {}), rec.get("code_ext", []),
                       rec.get("generated_markers", []), rec.get("integration", "dev")):
        print(w)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
