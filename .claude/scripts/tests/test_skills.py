"""skills.sh must catch collisions, scaffold a credited library, and keep SOURCES.md honest.

Run: python3 -m unittest discover -s .claude/scripts/tests
The upstream is a local git repo (file://), so the tests need no network.
"""
import json, os, shutil, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..")
REPO = os.path.abspath(os.path.join(SCRIPTS, "..", ".."))


def git(cwd, *args):
    return subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True, text=True).stdout.strip()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w").write(text)


SKILL = """---
name: seo-check
description: Audit a site for technical SEO problems, crawl errors and indexing issues.
---

# SEO check

## Setup

Collect the URL list.

## Checks

Crawl, then list indexing issues.
"""


class SkillsTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.root = os.path.join(self.d, "ws")
        shutil.copytree(os.path.join(REPO, "templates", "skill-library"),
                        os.path.join(self.root, "templates", "skill-library"))
        write(os.path.join(self.root, ".claude-plugin", "marketplace.json"),
              json.dumps({"name": "t", "plugins": []}))
        write(os.path.join(self.root, ".claude", "skills", "copy-helper", "SKILL.md"),
              "---\nname: copy-helper\ndescription: Write marketing headlines and landing page copy.\n---\n")
        self.up = os.path.join(self.d, "up")
        os.makedirs(self.up)
        git(self.up, "init", "-q", "-b", "main")
        git(self.up, "config", "user.email", "t@example.com")
        git(self.up, "config", "user.name", "t")
        write(os.path.join(self.up, "LICENSE"), "MIT License\n\nCopyright (c) 2026 Test Author\n")
        write(os.path.join(self.up, "skills", "seo-check", "SKILL.md"), SKILL)
        write(os.path.join(self.up, "skills", "seo-check", "references", "notes.md"), "notes\n")
        git(self.up, "add", "-A")
        git(self.up, "commit", "-q", "-m", "v1")
        self.sha = git(self.up, "rev-parse", "HEAD")
        self.env = dict(os.environ, STUDIO_ROOT=self.root, UPSTREAM_CACHE=os.path.join(self.d, "cache"))

    def tearDown(self):
        shutil.rmtree(self.d)

    def run_cmd(self, script, *args):
        return subprocess.run([sys.executable, os.path.join(SCRIPTS, script), *args],
                              capture_output=True, text=True, env=self.env, timeout=120)

    def skills(self, *args):
        return self.run_cmd("_skills.py", *args)

    def new_library(self):
        r = self.skills("new-library", "seo-lib", "--source", f"t=file://{self.up}", "--title", "SEO skills")
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        return os.path.join(self.root, "plugins", "seo-lib")

    # --- overlap ---

    def test_overlap_flags_same_name_and_similar_topic(self):
        cand = os.path.join(self.d, "cand", "copy-helper")
        write(os.path.join(cand, "SKILL.md"),
              "---\nname: copy-helper\ndescription: Landing page copy and marketing headlines.\n---\n")
        r = self.skills("overlap", cand)
        self.assertEqual(r.returncode, 1)
        self.assertIn("COLLISION", r.stdout)
        r = self.skills("overlap", "--text", "write landing page headlines for marketing copy")
        self.assertEqual(r.returncode, 0)
        self.assertIn("copy-helper", r.stdout)
        self.assertIn("shared:", r.stdout)
        r = self.skills("overlap", "--text", "kubernetes helm canary rollout")
        self.assertIn("no existing skill shares", r.stdout)

    # --- new-library ---

    def test_new_library_fills_credit_licence_and_marketplace(self):
        lib = self.new_library()
        up = open(os.path.join(lib, "UPSTREAM.md")).read()
        self.assertIn(f"commit: {self.sha}", up)
        self.assertIn("key: t", up)
        self.assertIn("credit: Test Author", up)
        self.assertIn("mode: merged", up)
        self.assertIn("Copyright (c) 2026 Test Author", open(os.path.join(lib, "LICENSE")).read())
        self.assertIn("| `t` |", open(os.path.join(lib, "README.md")).read())
        self.assertNotIn("{{", "".join(open(os.path.join(b, f)).read() for b, _, fs in os.walk(lib) for f in fs))
        market = json.load(open(os.path.join(self.root, ".claude-plugin", "marketplace.json")))
        self.assertEqual(market["plugins"][-1]["source"], "./plugins/seo-lib")
        codex = json.load(open(os.path.join(self.root, ".agents", "plugins", "marketplace.json")))
        self.assertEqual(codex["plugins"][-1]["source"], {"source": "local", "path": "./plugins/seo-lib"})
        self.assertIn("codex plugin add seo-lib@punokawan", open(os.path.join(lib, "README.md")).read())
        r = self.skills("marketplaces")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertEqual(self.run_cmd("_upstream.py", "lint").returncode, 0)
        r = self.skills("new-library", "seo-lib", "--source", f"t=file://{self.up}")
        self.assertIn("already exists", r.stderr)

    def test_marketplaces_flags_a_library_missing_for_codex(self):
        self.new_library()
        open(os.path.join(self.root, ".agents", "plugins", "marketplace.json"), "w").write('{"plugins": []}')
        r = self.skills("marketplaces")
        self.assertEqual(r.returncode, 1)
        self.assertIn("seo-lib: not listed in .agents/plugins/marketplace.json (Codex)", r.stdout)

    def test_new_library_refuses_a_source_without_licence(self):
        os.remove(os.path.join(self.up, "LICENSE"))
        git(self.up, "commit", "-q", "-am", "drop licence")
        r = self.skills("new-library", "bad-lib", "--source", f"t=file://{self.up}")
        self.assertEqual(r.returncode, 1)
        self.assertIn("no LICENSE", r.stderr)

    # --- sources / validate / index ---

    def test_sources_generate_then_check_catches_a_false_as_is(self):
        lib = self.new_library()
        dest = os.path.join(lib, "skills", "seo-check")
        shutil.copytree(os.path.join(self.up, "skills", "seo-check"), dest)
        with open(os.path.join(dest, "SKILL.md"), "a") as f:
            f.write("\nSources and credits: [SOURCES.md](SOURCES.md)\n")
        r = self.skills("sources", "generate", "seo-lib", "seo-check", "t", "skills/seo-check")
        self.assertEqual(r.returncode, 0, r.stderr)
        table = open(os.path.join(dest, "SOURCES.md")).read()
        self.assertIn("| SKILL.md § Setup | t `seo-check` @" + self.sha[:7] + " | skills/seo-check/SKILL.md § Setup | as is |", table)
        self.assertIn("| SKILL.md § Checks | t `seo-check` @" + self.sha[:7], table)  # edited: the credit line sits in it
        self.assertIn("t = file://", table)
        self.assertEqual(self.skills("sources", "check", "seo-lib").returncode, 0)
        text = open(os.path.join(dest, "SKILL.md")).read().replace("Collect the URL list.", "Collect every URL.")
        open(os.path.join(dest, "SKILL.md"), "w").write(text)
        r = self.skills("sources", "check", "seo-lib")
        self.assertEqual(r.returncode, 1)
        self.assertIn('"SKILL.md § Setup" says as is but differs', r.stdout)

    def test_validate_and_index(self):
        lib = self.new_library()
        dest = os.path.join(lib, "skills", "seo-check")
        shutil.copytree(os.path.join(self.up, "skills", "seo-check"), dest)
        self.assertEqual(self.skills("validate", "seo-lib").returncode, 0)
        r = self.skills("index", "seo-lib")
        self.assertIn("1 skills: 0 from Test Author only, 1 written here.", r.stdout)
        self.assertIn("[`seo-check`](skills/seo-check/SKILL.md)", open(os.path.join(lib, "README.md")).read())
        write(os.path.join(dest, "references", "bad.md"), "[gone](missing.md)\n")
        r = self.skills("validate", "seo-lib")
        self.assertEqual(r.returncode, 1)
        self.assertIn("broken link missing.md", r.stdout)


if __name__ == "__main__":
    unittest.main()
