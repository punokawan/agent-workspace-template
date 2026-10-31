#!/usr/bin/env python3
"""Delegate work to Codex CLI and finish what its sandbox cannot. Used by codex.sh.

    _codex.py exec <dir> [--write] [--timeout s] [--model m] [--image f]... "<prompt>"
    _codex.py blender <script.py> [--timeout s] [-- script args]
    _codex.py sprite <in.png> <out.png> [--size 32] [--tolerance 40] [--preview p.png]
    _codex.py sheet <out.png> <image>... [--height 512]

exec    runs `codex exec` non-interactively: stdin closed (it hangs on an open one), read-only
        unless --write, last message printed, full log kept in .cache/codex/.
blender runs headless Blender outside Codex's sandbox, which blocks the GPU Blender starts on.
sprite  turns a generated "pixel art" image into a real sprite: background flood-filled to
        transparent from the edges, cropped, centred on a square, nearest-neighbour scaled.
sheet   puts renders side by side for review and reports how much of each subject is clipped white.
"""
import os, shutil, signal, subprocess, sys, tempfile, time

ROOT = os.environ.get("STUDIO_ROOT") or os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
LOG_DIR = os.path.join(ROOT, ".cache", "codex")
BLENDER_PATHS = [
    "/Applications/Blender.app/Contents/MacOS/Blender",
    "/usr/bin/blender", "/snap/bin/blender",
    "C:/Program Files/Blender Foundation/Blender/blender.exe",
]


def die(msg, code=1):
    print("codex: " + msg, file=sys.stderr)
    sys.exit(code)


def parse(argv, flags, multi=(), switches=()):
    """Split argv into positionals and options. Everything after `--` is passed through."""
    pos, opts, rest = [], {m: [] for m in multi}, []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--":
            rest = argv[i + 1:]
            break
        if a in switches:
            opts[a] = True
        elif a in flags or a in multi:
            if i + 1 >= len(argv):
                die(a + " needs a value")
            if a in multi:
                opts[a].append(argv[i + 1])
            else:
                opts[a] = argv[i + 1]
            i += 1
        elif a.startswith("--"):
            die("unknown flag: " + a)
        else:
            pos.append(a)
        i += 1
    return pos, opts, rest


def run(cmd, timeout, log_path, cwd=None):
    """Run cmd with stdin closed and output to log_path. Returns exit code, 124 on timeout."""
    with open(log_path, "w") as log:
        p = subprocess.Popen(cmd, cwd=cwd, stdin=subprocess.DEVNULL, stdout=log,
                             stderr=subprocess.STDOUT, start_new_session=True)
        try:
            return p.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            if not hasattr(os, "killpg"):  # Windows: no process groups
                p.kill()
                return 124
            os.killpg(p.pid, signal.SIGTERM)
            try:
                p.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(p.pid, signal.SIGKILL)
            return 124


def tail(path, n):
    with open(path, errors="replace") as f:
        return "".join(f.readlines()[-n:])


def cmd_exec(argv):
    pos, o, _ = parse(argv, {"--timeout", "--model"}, multi=("--image",), switches=("--write",))
    if len(pos) != 2:
        die('usage: codex.sh exec <dir> [--write] [--timeout s] [--model m] [--image f]... "<prompt>"')
    d, prompt = os.path.abspath(pos[0]), pos[1]
    if not os.path.isdir(d):
        die("no such directory: " + d)
    codex = os.environ.get("CODEX_BIN") or shutil.which("codex")
    if not codex:
        die("codex CLI not found — install it and sign in (`codex login`)")
    os.makedirs(LOG_DIR, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    log = os.path.join(LOG_DIR, stamp + ".log")
    last = os.path.join(LOG_DIR, stamp + ".last.txt")
    cmd = [codex, "exec", "-C", d, "-s", "workspace-write" if o.get("--write") else "read-only",
           "--ephemeral", "-o", last]
    if subprocess.run(["git", "-C", d, "rev-parse"], capture_output=True).returncode != 0:
        cmd.append("--skip-git-repo-check")
    if o.get("--model"):
        cmd += ["-m", o["--model"]]
    for img in o["--image"]:
        cmd += ["-i", os.path.abspath(img)]
    code = run(cmd + [prompt], int(o.get("--timeout", 900)), log)
    if os.path.exists(last) and os.path.getsize(last):
        print(open(last, errors="replace").read().rstrip())
    else:
        print(tail(log, 30).rstrip())
    print("codex: log " + log, file=sys.stderr)
    if code == 124:
        die("timed out after %ss — the work may be half done; check the diff" % o.get("--timeout", 900), 124)
    sys.exit(code)


def find_blender():
    for c in [os.environ.get("BLENDER"), shutil.which("blender")] + BLENDER_PATHS:
        if c and os.path.isfile(c):
            return c
    die("Blender not found — install it or set BLENDER=/path/to/blender")


def cmd_blender(argv):
    pos, o, rest = parse(argv, {"--timeout"})
    if len(pos) != 1 or not os.path.isfile(pos[0]):
        die("usage: codex.sh blender <script.py> [--timeout s] [-- script args]")
    script = os.path.abspath(pos[0])
    os.makedirs(LOG_DIR, exist_ok=True)
    log = os.path.join(LOG_DIR, time.strftime("%Y%m%d-%H%M%S") + ".blender.log")
    cmd = [find_blender(), "-b", "--factory-startup", "--python-exit-code", "1",
           "--python", script] + (["--"] + rest if rest else [])
    code = run(cmd, int(o.get("--timeout", 600)), log, cwd=os.path.dirname(script))
    print(tail(log, 25).rstrip())
    print("codex: log " + log, file=sys.stderr)
    sys.exit(code)


def to_sprite(src, dst, size=32, tolerance=40, preview=None):
    try:
        from PIL import Image, ImageChops, ImageDraw
    except ImportError:
        die("sprite needs Pillow: python3 -m pip install Pillow")
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    corners = [img.getpixel(p) for p in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]]
    alpha = img.getchannel("A")
    if sum(c[3] < 128 for c in corners) < 3:
        # Opaque background: mark pixels near the corner colour, then keep only the region
        # connected to the border, so white highlights inside the subject survive.
        bg = tuple(sorted(c[i] for c in corners)[1] for i in range(3))
        diff = ImageChops.difference(img.convert("RGB"), Image.new("RGB", img.size, bg))
        near = diff.convert("L").point(lambda v: 255 if v <= tolerance else 0)
        padded = Image.new("L", (w + 2, h + 2), 255)
        padded.paste(near, (1, 1))
        ImageDraw.floodfill(padded, (0, 0), 128)
        outside = padded.crop((1, 1, w + 1, h + 1)).point(lambda v: 0 if v == 128 else 255)
        alpha = ImageChops.multiply(alpha, outside)
    img.putalpha(alpha.point(lambda v: 255 if v >= 128 else 0))
    box = img.getbbox()
    if not box:
        die("nothing left after removing the background — raise --tolerance or check the image")
    img = img.crop(box)
    side = max(img.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(img, ((side - img.width) // 2, (side - img.height) // 2))
    out = square.resize((size, size), Image.NEAREST)
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    out.save(dst)
    if preview:
        out.resize((size * max(1, 512 // size),) * 2, Image.NEAREST).save(preview)
    return out


def contact_sheet(out, images, height=512, floor=40):
    """Side-by-side sheet for review, plus per-image share of subject pixels clipped to white.
    Subject pixels are those brighter than `floor` (renders sit on a dark ground)."""
    try:
        from PIL import Image
    except ImportError:
        die("sheet needs Pillow: python3 -m pip install Pillow")
    full = [Image.open(p).convert("RGB") for p in images]
    report = []
    for path, im in zip(images, full):
        px = [p for p in im.getdata() if max(p) > floor]
        clipped = sum(1 for p in px if min(p) >= 250)
        report.append((path, len(px), 100.0 * clipped / max(1, len(px))))
    ims = [im.resize((max(1, im.width * height // im.height), height)) for im in full]
    sheet = Image.new("RGB", (sum(im.width for im in ims), height))
    x = 0
    for im in ims:
        sheet.paste(im, (x, 0))
        x += im.width
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out)
    return report


def cmd_sheet(argv):
    pos, o, _ = parse(argv, {"--height"})
    if len(pos) < 2 or not all(os.path.isfile(p) for p in pos[1:]):
        die("usage: codex.sh sheet <out.png> <image>... [--height 512]")
    for path, n, pct in contact_sheet(pos[0], pos[1:], int(o.get("--height", 512))):
        print("%s  subject_px=%d  clipped=%.1f%%" % (os.path.basename(path), n, pct))
    print(pos[0])


def cmd_sprite(argv):
    pos, o, _ = parse(argv, {"--size", "--tolerance", "--preview"})
    if len(pos) != 2 or not os.path.isfile(pos[0]):
        die("usage: codex.sh sprite <in.png> <out.png> [--size 32] [--tolerance 40] [--preview p.png]")
    to_sprite(pos[0], pos[1], int(o.get("--size", 32)), int(o.get("--tolerance", 40)), o.get("--preview"))
    print(pos[1])


if __name__ == "__main__":
    cmds = {"exec": cmd_exec, "blender": cmd_blender, "sprite": cmd_sprite, "sheet": cmd_sheet}
    if len(sys.argv) < 2 or sys.argv[1] not in cmds:
        print(__doc__.strip())
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help") else 1)
    cmds[sys.argv[1]](sys.argv[2:])
