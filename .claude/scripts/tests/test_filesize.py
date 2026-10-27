"""The file-size warning must fire on growth past the limit and stay silent on legacy files.

Run: python3 -m unittest discover -s .claude/scripts/tests
"""
import os, shutil, subprocess, sys, tempfile, unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from _filesize import oversized

FS = {"limit": 10, "exclude": ["*_test.go", "*/migrations/*"]}


class FileSizeTest(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.git("init", "-q", "-b", "dev")
        self.write("big.go", 20)      # legacy file already over the limit
        self.write("small.go", 5)
        self.git("add", "-A")
        self.git("-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "base")
        self.git("checkout", "-qb", "feat/x")

    def tearDown(self):
        shutil.rmtree(self.d)

    def git(self, *a):
        subprocess.run(["git", "-C", self.d, *a], check=True, capture_output=True)

    def write(self, rel, n):
        p = os.path.join(self.d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w").write("x\n" * n)

    def warns(self):
        return oversized(self.d, FS, [".go"], [".pb.go"], "dev")

    def test_legacy_large_file_untouched_is_silent(self):
        self.assertEqual(self.warns(), [])

    def test_legacy_large_file_shrunk_is_silent(self):
        self.write("big.go", 15)
        self.assertEqual(self.warns(), [])

    def test_growth_and_new_files_warn(self):
        self.write("big.go", 21)
        self.write("small.go", 11)
        self.write("pkg/new.go", 12)
        self.assertEqual(sorted(w.split(":")[0] for w in self.warns()),
                         ["big.go", "pkg/new.go", "small.go"])

    def test_tests_generated_and_migrations_are_ignored(self):
        self.write("a_test.go", 50)
        self.write("api.pb.go", 50)
        self.write("db/migrations/001.go", 50)
        self.write("notes.md", 50)
        self.assertEqual(self.warns(), [])


if __name__ == "__main__":
    unittest.main()
