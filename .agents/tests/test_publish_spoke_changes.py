from pathlib import Path
import json
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/skills/publish-spoke-changes/scripts/preflight_spoke_pr.py"
SAMPLE_REPORT = ROOT / "docs/test-reports/2026-10-04-software-handoff-removal-runtime-verification.md"
REPORT_PATH = "docs/test-reports/2026-10-04-sample-runtime-verification.md"
SPOKE_REPOSITORY = "https://github.com/example/site.dev.git"


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def init_repository(repo, origin):
    repo.mkdir(parents=True)
    for args in (("init", "-b", "main"), ("config", "user.name", "Fixture"),
                 ("config", "user.email", "fixture@example.invalid"), ("config", "commit.gpgsign", "false"),
                 ("config", "core.autocrlf", "false"), ("remote", "add", "origin", origin)):
        git(repo, *args)


def commit_file(repo, relative_path, text, message):
    file_path = repo / relative_path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(text, encoding="utf-8")
    git(repo, "add", relative_path)
    git(repo, "commit", "-m", message)


def mark_published(repo, branch="main"):
    """Stand in for a push: point origin/<branch> at HEAD without a network remote."""
    git(repo, "update-ref", f"refs/remotes/origin/{branch}", "HEAD")


class PreflightTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        workspace = Path(self.temp.name).resolve()
        self.builder = workspace / "builder"
        self.spoke = workspace / "site.dev"
        init_repository(self.spoke, SPOKE_REPOSITORY)
        commit_file(self.spoke, "README.md", "site\n", "Base")
        mark_published(self.spoke)
        git(self.spoke, "switch", "-c", "codex/footer-20261004")
        commit_file(self.spoke, "README.md", "site with footer\n", "Change footer")
        self.candidate = git(self.spoke, "rev-parse", "HEAD")
        init_repository(self.builder, "git@github.com:example/builder.git")
        registry = {"spokes": [{"slug": "site-dev", "name": "site.dev", "repository": SPOKE_REPOSITORY,
                                "defaultBranch": "main", "description": "Sample spoke"}]}
        commit_file(self.builder, "spokes.json", json.dumps(registry), "Register spoke")

    def publish_report(self, *, candidate_text=None, status="complete"):
        sample_text = SAMPLE_REPORT.read_text(encoding="utf-8")
        status_section = sample_text.split("## Document Status", 1)[1].split("##", 1)[0]
        report_text = sample_text.replace(status_section, f"\n{status}\n\n", 1)
        named_candidate = self.candidate[:7] if candidate_text is None else candidate_text
        commit_file(self.builder, REPORT_PATH, f"{report_text}\nCandidate: {named_candidate}\n", "Report")
        mark_published(self.builder)

    def preflight(self, *extra_args, report=REPORT_PATH):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--spoke", "site-dev", "--path", str(self.spoke),
                               "--report", report, "--root", str(self.builder), *extra_args],
                              capture_output=True, text=True, encoding="utf-8", timeout=30)

    def assert_fails_check(self, check_name, expected_detail):
        result = self.preflight()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertRegex(result.stdout, rf"\[FAIL\] {check_name}: .*{expected_detail}")

    def test_ready_branch_prints_report_link_for_pull_request(self):
        self.publish_report()
        result = self.preflight()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("[FAIL]", result.stdout)
        self.assertIn(f"Candidate {self.candidate} is ready", result.stdout)
        self.assertIn(f"https://github.com/example/builder/blob/main/{REPORT_PATH}", result.stdout)

    def test_origin_mismatch_stops_before_other_checks(self):
        self.publish_report()
        git(self.spoke, "remote", "set-url", "origin", "https://github.com/someone-else/site.dev.git")
        result = self.preflight()
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout.count("[FAIL]"), 1)
        self.assertIn("does not match registered", result.stdout)

    def test_default_branch_and_detached_head_are_refused(self):
        self.publish_report()
        git(self.spoke, "switch", "main")
        self.assert_fails_check("branch", "on default branch main")
        git(self.spoke, "switch", "--detach", self.candidate)
        self.assert_fails_check("branch", "detached")

    def test_modified_tracked_file_is_refused_but_untracked_file_is_not(self):
        self.publish_report()
        (self.spoke / "notes.txt").write_text("scratch", encoding="utf-8")
        self.assertEqual(self.preflight().returncode, 0)
        (self.spoke / "README.md").write_text("edited after verification\n", encoding="utf-8")
        self.assert_fails_check("committed candidate", "not the verified candidate")

    def test_branch_without_new_commits_is_refused(self):
        self.publish_report()
        mark_published(self.spoke)
        self.assert_fails_check("commits ahead", "no commits ahead of origin/main")

    def test_report_must_be_published_and_identical(self):
        self.publish_report()
        git(self.builder, "update-ref", "refs/remotes/origin/main", "HEAD~1")
        self.assert_fails_check("report published", "is not on Builder origin/main")
        mark_published(self.builder)
        with (self.builder / REPORT_PATH).open("a", encoding="utf-8") as report_file:
            report_file.write("Unpublished note.\n")
        self.assert_fails_check("report published", "differs from Builder origin/main")

    def test_report_must_name_candidate_and_be_complete(self):
        self.publish_report(candidate_text="0000000")
        self.assert_fails_check("report names candidate", f"does not name candidate {self.candidate[:7]}")
        self.publish_report(status="draft")
        self.assert_fails_check("report", "Document Status is draft, not complete")

    def test_report_path_outside_test_reports_is_rejected(self):
        result = self.preflight(report="docs/session-memory/2026-10-04-builder.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("docs/test-reports", result.stderr)


if __name__ == "__main__":
    unittest.main()
