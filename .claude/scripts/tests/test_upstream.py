"""upstream.sh must pin, detect drift, update copy-mode skills safely and never auto-apply merged ones.

Run: python3 -m unittest discover -s .claude/scripts/tests
Every upstream here is a local git repo (file://), so the tests need no network.
"""
import os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "_upstream.py")


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)


class UpstreamTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.root = os.path.join(self.d, "ws")
        os.makedirs(os.path.join(self.root, ".claude", "skills"))
        self.up = os.path.join(self.d, "up")
        os.makedirs(self.up)
        git(self.up, "init", "-q", "-b", "main")
        git(self.up, "config", "user.email", "t@example.com")
        git(self.up, "config", "user.name", "t")
        write(os.path.join(self.up, "LICENSE"), "MIT License\n\nCopyright (c) 2026 Test\n")
        write(os.path.join(self.up, "skills/demo/SKILL.md"), "---\nname: demo\n---\nv1\n")
        write(os.path.join(self.up, "skills/demo/scripts/run.py"), "print(1)\n")
        write(os.path.join(self.up, "skills/demo/old.md"), "old\n")
        self.c1 = self.commit("v1")
        self.url = "file://" + self.up
        self.env = dict(os.environ, STUDIO_ROOT=self.root, UPSTREAM_CACHE=os.path.join(self.d, "cache"))

    def tearDown(self):
        shutil.rmtree(self.d)

    def commit(self, msg):
        git(self.up, "add", "-A")
        git(self.up, "commit", "-q", "-m", msg)
        return git(self.up, "rev-parse", "HEAD")

    def run_cmd(self, *args):
        return subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True,
                              env=self.env, timeout=120)

    def skill(self, name="demo"):
        return os.path.join(self.root, ".claude", "skills", name)

    def add(self):
        r = self.run_cmd("add", self.url, "skills/demo")
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        return r

    # --- add / lint ---

    def test_add_vendors_files_licence_and_block(self):
        r = self.add()
        s = self.skill()
        self.assertEqual(open(os.path.join(s, "SKILL.md")).read(), "---\nname: demo\n---\nv1\n")
        self.assertTrue(os.path.isfile(os.path.join(s, "LICENSE")))
        up = open(os.path.join(s, "UPSTREAM.md")).read()
        self.assertIn(f"commit: {self.c1}", up)
        self.assertIn("licence: MIT", up)
        self.assertIn("extra: LICENSE", up)
        self.assertIn("scripts/run.py", r.stdout)          # flagged for review
        self.assertNotIn("  LICENSE\n", r.stdout)          # a licence is not code
        self.assertIn("security scan: skipped", r.stdout)  # no reviewed auditor here
        self.assertEqual(self.run_cmd("lint").returncode, 0)

    def test_add_refuses_existing_folder(self):
        self.add()
        r = self.run_cmd("add", self.url, "skills/demo")
        self.assertEqual(r.returncode, 1)
        self.assertIn("already exists", r.stderr)

    def test_lint_flags_missing_commit_and_licence(self):
        write(os.path.join(self.skill("bad"), "UPSTREAM.md"),
              f"# Upstream\n\n```upstream\nrepo: {self.url}\npath: skills/demo\n```\n")
        r = self.run_cmd("lint")
        self.assertEqual(r.returncode, 1)
        self.assertIn("missing commit", r.stdout)
        self.assertIn("missing licence", r.stdout)
        self.assertIn("no LICENSE file", r.stdout)

    # --- check / drift ---

    def test_check_reports_up_to_date_then_behind_then_drift(self):
        self.add()
        self.assertIn("up to date", self.run_cmd("check").stdout)
        write(os.path.join(self.up, "skills/demo/SKILL.md"), "---\nname: demo\n---\nv2\n")
        self.commit("v2")
        out = self.run_cmd("check").stdout
        self.assertIn("1 newer commits, 1 files changed under path", out)
        write(os.path.join(self.skill(), "SKILL.md"), "local edit\n")
        self.assertIn("LOCAL DRIFT: 1 changed", self.run_cmd("check").stdout)

    def test_change_outside_path_is_not_an_update(self):
        self.add()
        write(os.path.join(self.up, "README.md"), "unrelated\n")
        self.commit("readme")
        self.assertIn("nothing changed under path", self.run_cmd("check").stdout)

    # --- pull ---

    def test_pull_updates_removes_and_bumps_pin(self):
        self.add()
        write(os.path.join(self.up, "skills/demo/SKILL.md"), "---\nname: demo\n---\nv2\n")
        os.remove(os.path.join(self.up, "skills/demo/old.md"))
        write(os.path.join(self.up, "skills/demo/new.md"), "new\n")
        c2 = self.commit("v2")
        r = self.run_cmd("pull", "demo")
        self.assertEqual(r.returncode, 0, r.stderr)
        s = self.skill()
        self.assertIn("v2", open(os.path.join(s, "SKILL.md")).read())
        self.assertFalse(os.path.exists(os.path.join(s, "old.md")))
        self.assertTrue(os.path.exists(os.path.join(s, "new.md")))
        self.assertIn(f"commit: {c2}", open(os.path.join(s, "UPSTREAM.md")).read())
        self.assertIn("up to date", self.run_cmd("check").stdout)

    def test_pull_refuses_local_edits_unless_forced(self):
        self.add()
        write(os.path.join(self.skill(), "SKILL.md"), "local edit\n")
        write(os.path.join(self.up, "skills/demo/SKILL.md"), "v2\n")
        self.commit("v2")
        r = self.run_cmd("pull", "demo")
        self.assertEqual(r.returncode, 1)
        self.assertIn("local copy differs", r.stderr)
        self.assertEqual(open(os.path.join(self.skill(), "SKILL.md")).read(), "local edit\n")
        self.assertEqual(self.run_cmd("pull", "demo", "--force").returncode, 0)
        self.assertEqual(open(os.path.join(self.skill(), "SKILL.md")).read(), "v2\n")

    # --- merged mode ---

    def merged_plugin(self):
        p = os.path.join(self.root, "plugins", "mix")
        write(os.path.join(p, "LICENSE"), "MIT License\n")
        write(os.path.join(p, "UPSTREAM.md"),
              f"# Upstream\n\n```upstream\nrepo: {self.url}\npath: skills\ncommit: {self.c1}\n"
              "mode: merged\nkey: up\nlicence: MIT\n```\n")
        write(os.path.join(p, "skills", "merged-demo", "SOURCES.md"),
              "| Part | From | Upstream file | Changed here |\n|---|---|---|---|\n"
              "| SKILL.md § Body | up `demo` @abc | skills/demo/SKILL.md § Body | edited: x |\n")
        return p

    def test_merged_diff_maps_changes_and_pull_refuses(self):
        self.merged_plugin()
        write(os.path.join(self.up, "skills/demo/SKILL.md"), "v2\n")
        write(os.path.join(self.up, "skills/other/SKILL.md"), "brand new\n")
        self.commit("v2")
        out = self.run_cmd("diff", "mix", "--stat").stdout
        self.assertIn("-> merged-demo: SKILL.md § Body", out)
        self.assertIn("skills/other/SKILL.md", out.split("No SOURCES.md row")[1])
        r = self.run_cmd("pull", "mix")
        self.assertEqual(r.returncode, 1)
        self.assertIn("merged", r.stderr)


if __name__ == "__main__":
    unittest.main()
