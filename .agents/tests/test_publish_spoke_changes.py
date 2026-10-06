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

    def publish_report(self, *, candidate_text=None, status="complete", project=None):
        sample_text = SAMPLE_REPORT.read_text(encoding="utf-8")
        status_section = sample_text.split("## Document Status", 1)[1].split("##", 1)[0]
        project_section = f"## Project\n{project}\n\n" if project is not None else ""
        report_text = sample_text.replace(status_section, f"\n{status}\n\n{project_section}", 1)
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

    def test_report_project_must_be_the_spoke(self):
        self.publish_report(project="other-site")
        self.assert_fails_check("report project", "report Project is other-site, not spoke site-dev")
        self.publish_report(project="site-dev")
        result = self.preflight()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[pass] report project: report Project is site-dev", result.stdout)

    def test_fetch_refreshes_origin_refs_before_checking(self):
        self.publish_report()
        spoke_origin = self.spoke.parent / "site-origin.git"
        builder_origin = self.spoke.parent / "builder-origin.git"
        registry = {"spokes": [{"slug": "site-dev", "name": "site.dev", "repository": spoke_origin.as_uri(),
                                "defaultBranch": "main", "description": "Sample spoke"}]}
        commit_file(self.builder, "spokes.json", json.dumps(registry), "Register local origin")
        for bare, repo in ((spoke_origin, self.spoke), (builder_origin, self.builder)):
            git(repo.parent, "init", "--bare", "-b", "main", str(bare))
            git(repo, "push", "--quiet", str(bare), "main:main")
            git(repo, "remote", "set-url", "origin", bare.as_uri())
        # Stale view: origin/main locally claims the candidate is already published.
        git(self.spoke, "update-ref", "refs/remotes/origin/main", self.candidate)

        stale = self.preflight()
        fetched = self.preflight("--fetch")

        self.assertIn("[FAIL] commits ahead", stale.stdout)
        self.assertEqual(fetched.returncode, 0, fetched.stdout + fetched.stderr)

    def test_fetch_failure_stops_before_checks(self):
        self.publish_report()
        missing_origin = (self.spoke.parent / "missing-origin.git").as_uri()
        registry = {"spokes": [{"slug": "site-dev", "name": "site.dev", "repository": missing_origin,
                                "defaultBranch": "main", "description": "Sample spoke"}]}
        commit_file(self.builder, "spokes.json", json.dumps(registry), "Register missing origin")
        git(self.spoke, "remote", "set-url", "origin", missing_origin)

        result = self.preflight("--fetch")

        self.assertEqual(result.returncode, 2)
        self.assertIn("git fetch origin failed", result.stderr)
        self.assertNotIn("[pass]", result.stdout)

    def test_report_path_outside_test_reports_is_rejected(self):
        result = self.preflight(report="docs/session-memory/2026-10-04-builder.md")
        self.assertEqual(result.returncode, 2)
        self.assertIn("docs/test-reports", result.stderr)


PLAN_PATH = "docs/implementation-plans/2026-10-05-09-00-site-dev-workflow-only.md"
NO_RUNTIME_REASON = "Only .github/workflows changes; the application is untouched."


class NoRuntimePreflightTests(unittest.TestCase):
    """A change with nothing runnable records why in its published plan instead of a report."""

    setUp = PreflightTests.setUp
    publish_report = PreflightTests.publish_report

    def publish_plan(self, *, project="site-dev", reason=NO_RUNTIME_REASON):
        reason_line = f"- **Runtime proof not applicable:** {reason}\n" if reason is not None else ""
        plan_text = (
            "# Workflow-only change\n\n## Document Status\nin-progress\n\n## Test Plan\n"
            f"{reason_line}- Contract test covers the workflow.\n\n## Project\n{project}\n"
        )
        commit_file(self.builder, PLAN_PATH, plan_text, "Plan")
        mark_published(self.builder)

    def preflight_without_runtime(self, plan=PLAN_PATH):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), "--spoke", "site-dev", "--path", str(self.spoke),
                               "--no-runtime-plan", plan, "--root", str(self.builder)],
                              capture_output=True, text=True, encoding="utf-8", timeout=30)

    def test_published_plan_reason_replaces_the_report(self):
        self.publish_plan()

        result = self.preflight_without_runtime()

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("[pass] no-runtime plan:", result.stdout)
        self.assertIn(f"Runtime proof not applicable: {NO_RUNTIME_REASON}", result.stdout)
        self.assertIn(f"https://github.com/example/builder/blob/main/{PLAN_PATH}", result.stdout)

    def test_plan_without_a_reason_is_refused(self):
        self.publish_plan(reason=None)

        result = self.preflight_without_runtime()

        self.assertEqual(result.returncode, 1)
        self.assertRegex(result.stdout, r"\[FAIL\] no-runtime plan: .*Runtime proof not applicable")

    def test_unpublished_or_foreign_plan_is_refused(self):
        self.publish_plan()
        with (self.builder / PLAN_PATH).open("a", encoding="utf-8") as plan_file:
            plan_file.write("Unpublished edit.\n")
        self.assertRegex(self.preflight_without_runtime().stdout, r"\[FAIL\] no-runtime plan published: .*differs")

        self.publish_plan(project="other-site")
        self.assertRegex(self.preflight_without_runtime().stdout,
                         r"\[FAIL\] no-runtime plan: .*Project is other-site, not spoke site-dev")

    def test_report_and_no_runtime_plan_are_exclusive(self):
        self.publish_plan()
        self.publish_report()

        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "--spoke", "site-dev", "--path", str(self.spoke),
                                 "--report", REPORT_PATH, "--no-runtime-plan", PLAN_PATH, "--root", str(self.builder)],
                                capture_output=True, text=True, encoding="utf-8", timeout=30)

        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
