"""Tests for shared spoke repository inspection."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "lib"))

from spoke_state import git


class GitOutputEncodingTest(unittest.TestCase):
    def test_git_preserves_unicode_in_a_committed_report(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            repository_path = Path(temporary_directory)
            report_path = repository_path / "report.md"
            report_text = "✅ PASS\n"

            subprocess.run(
                ["git", "init", "--quiet"],
                cwd=repository_path,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.name", "Test Agent"],
                cwd=repository_path,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "config", "user.email", "test@example.invalid"],
                cwd=repository_path,
                check=True,
                capture_output=True,
            )
            report_path.write_text(report_text, encoding="utf-8")

            git(repository_path, "add", "report.md")
            git(repository_path, "commit", "--quiet", "-m", "Add test report")

            self.assertEqual(git(repository_path, "show", "HEAD:report.md"), "✅ PASS")


if __name__ == "__main__":
    unittest.main()
