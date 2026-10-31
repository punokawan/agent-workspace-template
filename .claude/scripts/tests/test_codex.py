"""codex.sh must never hang on stdin, default to read-only, and turn generated art into a real sprite.

Run: python3 -m unittest discover -s .claude/scripts/tests
"""
import os, shutil, stat, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "_codex.py")
sys.path.insert(0, os.path.join(HERE, ".."))

# Stands in for the codex CLI: records its argv, fails if stdin is open, writes the -o file.
FAKE = """#!/usr/bin/env python3
import os, sys
open(os.environ["FAKE_ARGS"], "w").write("\\n".join(sys.argv[1:]))
if os.environ.get("FAKE_SLEEP"):
    import time; time.sleep(30)
if sys.stdin.read() != "":
    sys.exit(9)
out = sys.argv[sys.argv.index("-o") + 1]
open(out, "w").write("done: " + sys.argv[-1])
"""


class ExecTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.bin = os.path.join(self.d, "codex")
        open(self.bin, "w").write(FAKE)
        os.chmod(self.bin, os.stat(self.bin).st_mode | stat.S_IEXEC)
        self.args = os.path.join(self.d, "args")
        self.env = dict(os.environ, CODEX_BIN=self.bin, FAKE_ARGS=self.args, STUDIO_ROOT=self.d)

    def tearDown(self):
        shutil.rmtree(self.d)

    def run_exec(self, *extra, **env):
        return subprocess.run([sys.executable, SCRIPT, "exec", self.d, *extra],
                              capture_output=True, text=True, env=dict(self.env, **env), timeout=60)

    def argv(self):
        return open(self.args).read().split("\n")

    def test_stdin_closed_and_last_message_printed(self):
        r = self.run_exec("make it")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.strip(), "done: make it")

    def test_read_only_by_default_write_on_request(self):
        self.run_exec("look")
        a = self.argv()
        self.assertEqual(a[a.index("-s") + 1], "read-only")
        self.assertIn("--skip-git-repo-check", a)  # tmp dir is not a git repo
        self.run_exec("--write", "change")
        a = self.argv()
        self.assertEqual(a[a.index("-s") + 1], "workspace-write")

    def test_image_flag_does_not_swallow_the_prompt(self):
        img = os.path.join(self.d, "ref.png")
        open(img, "wb").write(b"x")
        r = self.run_exec("--image", img, "draw it")
        self.assertEqual(r.returncode, 0, r.stderr)
        a = self.argv()
        self.assertEqual(a[-2:], ["--", "draw it"])
        self.assertEqual(a[a.index("-i") + 1], img)

    def test_timeout_kills_and_exits_124(self):
        r = self.run_exec("--timeout", "1", "slow", FAKE_SLEEP="1")
        self.assertEqual(r.returncode, 124)


class SpriteTest(unittest.TestCase):
    def setUp(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not installed")
        self.Image = Image
        self.d = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.d)

    def test_white_background_removed_inner_highlight_kept(self):
        from _codex import to_sprite
        img = self.Image.new("RGBA", (400, 400), (255, 255, 255, 255))
        for x in range(100, 300):          # green 200x200 block, 20px pixel-art cells
            for y in range(150, 350):
                img.putpixel((x, y), (40, 200, 60, 255))
        for x in range(140, 160):          # white highlight inside the subject
            for y in range(190, 210):
                img.putpixel((x, y), (255, 255, 255, 255))
        src = os.path.join(self.d, "in.png")
        img.save(src)
        out = to_sprite(src, os.path.join(self.d, "out.png"), size=10)
        self.assertEqual(out.size, (10, 10))
        self.assertEqual(out.getpixel((0, 0))[3], 255)          # cropped tight: corner is subject
        self.assertEqual(out.getpixel((2, 2)), (255, 255, 255, 255))  # highlight survives
        self.assertEqual(out.getpixel((5, 5)), (40, 200, 60, 255))

    def test_sheet_reports_clipped_share_of_subject_only(self):
        from _codex import contact_sheet
        img = self.Image.new("RGB", (100, 200), (11, 18, 32))   # dark render ground
        for x in range(20, 80):
            for y in range(50, 150):
                img.putpixel((x, y), (255, 255, 255) if x < 50 else (120, 130, 140))
        a, b = os.path.join(self.d, "a.png"), os.path.join(self.d, "b.png")
        img.save(a)
        img.save(b)
        out = os.path.join(self.d, "sheet.png")
        report = contact_sheet(out, [a, b], height=100)
        self.assertEqual(self.Image.open(out).size, (100, 100))   # two 50x100 thumbnails
        self.assertEqual(report[0][1], 6000)                      # ground not counted
        self.assertAlmostEqual(report[0][2], 50.0)                # half the subject clipped

    def test_transparent_input_is_cropped_and_centred(self):
        from _codex import to_sprite
        img = self.Image.new("RGBA", (300, 100), (0, 0, 0, 0))
        for x in range(0, 300):
            for y in range(40, 60):
                img.putpixel((x, y), (200, 0, 0, 255))
        src = os.path.join(self.d, "in.png")
        img.save(src)
        out = to_sprite(src, os.path.join(self.d, "out.png"), size=30)
        self.assertEqual(out.getpixel((15, 0))[3], 0)    # padded above
        self.assertEqual(out.getpixel((15, 15))[3], 255)  # bar centred


if __name__ == "__main__":
    unittest.main()
