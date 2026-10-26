"""rules.sh writes the guide every agent reads, so its behaviour is pinned here.

Run: python3 -m unittest discover -s .claude/scripts/tests
Each test builds a throwaway workspace (STUDIO_ROOT) from the real templates/rules.
"""
import json, os, shutil, subprocess, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "..", "_rules.py")
REAL_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


class RulesTest(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp()
        shutil.copytree(os.path.join(REAL_ROOT, "templates"), os.path.join(self.root, "templates"))
        open(self.path("AGENTS.md"), "w").write("# Guide\n\n<!-- BEGIN:rules -->\n<!-- END:rules -->\n\n## Scripts\n")
        self.project("app", rules={"profile": "standard"}, guide="# App\n\n## What it is\n\nA thing.\n")

    def tearDown(self):
        shutil.rmtree(self.root)

    def path(self, *p):
        return os.path.join(self.root, *p)

    def project(self, name, rules=None, guide=None, claude=None):
        d = self.path("projects", name)
        os.makedirs(d, exist_ok=True)
        man = {"name": name, "title": name.title(), "repos": []}
        if rules:
            man["rules"] = rules
        json.dump(man, open(os.path.join(d, "project.json"), "w"))
        if guide is not None:
            open(os.path.join(d, "AGENTS.md"), "w").write(guide)
        if claude is not None:
            open(os.path.join(d, "CLAUDE.md"), "w").write(claude)

    def run_rules(self, *args, ok=True):
        r = subprocess.run(["python3", SCRIPT, *args], capture_output=True, text=True,
                           env={**os.environ, "STUDIO_ROOT": self.root})
        if ok:
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r

    def read(self, *p):
        return open(self.path(*p)).read()

    def test_sync_renders_core_and_profile_and_is_idempotent(self):
        self.run_rules("sync")
        root, app = self.read("AGENTS.md"), self.read("projects", "app", "AGENTS.md")
        self.assertIn("## Instruction precedence", root)
        self.assertIn("## Rules: standard profile", app)
        self.assertIn("## Commit discipline", app)
        self.assertNotIn("## Worktree flow", app)
        self.assertIn("## What it is", app)          # hand-written text survives
        self.assertIn("nothing changed", self.run_rules("sync").stdout)
        self.assertEqual(self.run_rules("check").returncode, 0)

    def test_set_enable_disable_change_only_that_project(self):
        self.project("other", rules={"profile": "light"}, guide="# Other\n\n## Notes\n")
        self.run_rules("sync")
        before = self.read("projects", "other", "AGENTS.md")
        self.run_rules("enable", "app", "offline-tests")
        self.run_rules("disable", "app", "code-style")
        app = self.read("projects", "app", "AGENTS.md")
        self.assertIn("## Offline unit tests", app)
        self.assertNotIn("## How code is written", app)
        self.assertEqual(before, self.read("projects", "other", "AGENTS.md"))

    def test_custom_profile_and_builtins_stay_fixed(self):
        self.run_rules("profile", "new", "team", "from", "light")
        self.run_rules("profile", "add", "team", "capacity-review")
        self.run_rules("set", "app", "team")
        self.assertIn("## Capacity review", self.read("projects", "app", "AGENTS.md"))
        self.assertNotEqual(self.run_rules("profile", "add", "strict", "run-state", ok=False).returncode, 0)
        self.assertNotEqual(self.run_rules("profile", "delete", "team", ok=False).returncode, 0)

    def test_adopt_moves_an_old_claude_guide_verbatim(self):
        self.project("old", claude="# Old\n\n## Conventions\n\nkeep this rule\n")
        self.assertNotEqual(self.run_rules("check", ok=False).returncode, 0)
        self.run_rules("adopt", "old", "light")
        self.assertEqual(self.read("projects", "old", "CLAUDE.md"), "@AGENTS.md\n")
        guide = self.read("projects", "old", "AGENTS.md")
        self.assertIn("keep this rule", guide)
        self.assertIn("## Rules: light profile", guide)

    def test_missing_end_marker_fails_with_a_message(self):
        open(self.path("AGENTS.md"), "w").write("# Guide\n\n<!-- BEGIN:rules -->\nhand edit\n")
        r = self.run_rules("sync", ok=False)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("no '<!-- END:rules -->'", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
