from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

from project_registry_fixture import write_project_registry


ROOT = Path(__file__).resolve().parents[2]
SAVE_SCRIPT = ROOT / ".agents" / "skills" / "write-test-report" / "scripts" / "save_test_report.py"
INDEX_SCRIPT = ROOT / ".agents" / "skills" / "publish-builder-changes" / "scripts" / "update_hub_indexes.py"
VALIDATE_SCRIPT = ROOT / ".agents" / "skills" / "publish-builder-changes" / "scripts" / "validate_hub_state.py"


def report_text(title: str, project: str | None = "builder") -> str:
    project_section = f"## Project\n{project}\n\n" if project is not None else ""
    return (
        f"# {title}\n\n"
        "## Document Status\ncomplete\n\n"
        f"{project_section}"
        "## Story/Issue\nIssue 42\n\n"
        "## Branch\n`codex/issue-42`\n\n"
        "## App / Environment\nlocalhost:8080\n\n"
        "## Local Run Details\n`./gradlew bootRun`\n\n"
        "## Test Cases\n- Health endpoint returns OK.\n\n"
        "## Data Sent\nGET /health\n\n"
        "## Response Received\n200 OK\n\n"
        "## Pass / Fail\nPASS\n\n"
        "## Evidence\n`curl http://localhost:8080/health`\n\n"
        "## Bugs / Follow-ups\nNone.\n"
    )


def run(script: Path, *arguments: str, stdin: str = "") -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-B", str(script), *arguments], input=stdin, text=True,
                          capture_output=True, check=False)


class TestReportWorkflowTests(unittest.TestCase):
    def test_saves_test_report_with_project_prefixed_dated_slug(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_project_registry(root)
            result = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05", "--time", "14:07",
                         "--title", "Issue 42 Local App Test", stdin=report_text("Issue 42 Local App Test"))

            self.assertEqual(result.returncode, 0, result.stderr)
            report = root / "docs" / "test-reports" / "2099-04-05-14-07-builder-issue-42-local-app-test.md"
            self.assertEqual(Path(result.stdout.strip()).name, report.name)
            self.assertIn("## Test Cases", report.read_text(encoding="utf-8"))

    def test_saving_without_a_time_names_the_report_with_the_current_minute(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_project_registry(root)
            result = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05",
                         "--title", "Clock", stdin=report_text("Clock"))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertRegex(Path(result.stdout.strip()).name, r"^2099-04-05-([01]\d|2[0-3])-[0-5]\d-builder-clock\.md$")

    def test_overwrite_replaces_the_same_day_report_whatever_its_time(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_project_registry(root)
            first = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05", "--time", "09:30",
                        "--title", "Rerun", stdin=report_text("Rerun"))
            self.assertEqual(first.returncode, 0, first.stderr)

            refused = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05", "--time", "16:45",
                          "--title", "Rerun", stdin=report_text("Rerun"))
            replaced = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05", "--time", "16:45",
                           "--title", "Rerun", "--overwrite", stdin=report_text("Rerun").replace("PASS", "PASS again"))

            self.assertEqual(refused.returncode, 1, refused.stdout + refused.stderr)
            self.assertIn("already exists", refused.stderr)
            self.assertEqual(replaced.returncode, 0, replaced.stdout + replaced.stderr)
            report_dir = root / "docs" / "test-reports"
            self.assertEqual([path.name for path in report_dir.glob("*.md")], ["2099-04-05-09-30-builder-rerun.md"])
            self.assertIn("PASS again", (report_dir / "2099-04-05-09-30-builder-rerun.md").read_text(encoding="utf-8"))

    def test_save_refuses_a_malformed_time_and_an_ambiguous_same_day_report(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_project_registry(root)
            report_dir = root / "docs" / "test-reports"
            report_dir.mkdir(parents=True)
            for name in ("2099-04-05-builder-twin.md", "2099-04-05-10-00-builder-twin.md"):
                (report_dir / name).write_text(report_text("Twin"), encoding="utf-8")

            malformed = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05", "--time", "9:30",
                            "--title", "Other", stdin=report_text("Other"))
            ambiguous = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05",
                            "--title", "Twin", "--overwrite", stdin=report_text("Twin"))

            self.assertEqual(malformed.returncode, 2, malformed.stdout + malformed.stderr)
            self.assertIn("--time must use HH:MM format", malformed.stderr)
            self.assertEqual(ambiguous.returncode, 2, ambiguous.stdout + ambiguous.stderr)
            self.assertIn("several records on 2099-04-05 are named 'builder-twin': "
                          "2099-04-05-10-00-builder-twin.md, 2099-04-05-builder-twin.md", ambiguous.stderr)

    def test_new_report_must_name_an_active_project(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_project_registry(root, retired=("old-shop",))
            refusals = {
                "need a Project section": None,
                "Unknown project": "stranger",
                "retired": "old-shop",
            }
            for expected_message, project in refusals.items():
                with self.subTest(project=project):
                    result = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05",
                                 "--title", "Health check", stdin=report_text("Health check", project))
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(expected_message, result.stderr)
            self.assertFalse((root / "docs").exists())

            historical_report = root / "docs" / "test-reports" / "2099-04-05-health-check.md"
            historical_report.parent.mkdir(parents=True)
            historical_report.write_text(report_text("Health check", None), encoding="utf-8")
            replaced = run(SAVE_SCRIPT, "--root", str(root), "--date", "2099-04-05", "--title", "Health check",
                           "--overwrite", stdin=report_text("Health check", None).replace("PASS", "PASS again"))
            self.assertEqual(replaced.returncode, 0, replaced.stdout + replaced.stderr)
            self.assertIn("PASS again", historical_report.read_text(encoding="utf-8"))

    def test_indexes_group_reports_by_project_and_validate_them(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_project_registry(root, active=("home-lab",))
            report_dir = root / "docs" / "test-reports"
            report_dir.mkdir(parents=True)
            (report_dir / "2099-04-05-sample-report.md").write_text(report_text("Sample Report", None), encoding="utf-8")
            (report_dir / "2099-04-06-home-lab-router-report.md").write_text(
                report_text("Router Report", "home-lab"), encoding="utf-8")
            (report_dir / "2099-04-07-builder-hub-report.md").write_text(report_text("Hub Report"), encoding="utf-8")
            (report_dir / "2099-04-08-09-30-builder-timed-report.md").write_text(
                report_text("Timed Report"), encoding="utf-8")
            for directory in ("docs/session-memory", "docs/implementation-plans"):
                (root / directory).mkdir(parents=True, exist_ok=True)

            index_result = run(INDEX_SCRIPT, "--root", str(root))
            self.assertEqual(index_result.returncode, 0, index_result.stderr)
            index_text = (report_dir / "index.md").read_text(encoding="utf-8")
            group_positions = [index_text.index(heading) for heading in
                               ("## builder\n\n- 2099-04-07: [Hub Report]",
                                "- 2099-04-08 09:30: [Timed Report]",
                                "## home-lab\n\n- 2099-04-06: [Router Report]",
                                "## Before the Project field\n\n- 2099-04-05: [Sample Report]")]
            self.assertEqual(group_positions, sorted(group_positions))

            validate_result = run(VALIDATE_SCRIPT, "--root", str(root))
            self.assertEqual(validate_result.returncode, 0, validate_result.stdout + validate_result.stderr)

    def test_hub_rejects_unregistered_or_mismatched_report_projects(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            write_project_registry(root)
            report_dir = root / "docs" / "test-reports"
            report_dir.mkdir(parents=True)
            cases = {
                "2099-04-05-stranger-report.md": ("stranger", "is not builder, a registered spoke"),
                "2099-04-05-health-report.md": ("builder", "filename must start with YYYY-MM-DD-HH-MM-builder-"),
                "2099-04-05-09-30-timed-report.md": ("builder", "filename must start with YYYY-MM-DD-HH-MM-builder-"),
            }
            for filename, (project, expected_error) in cases.items():
                with self.subTest(filename=filename):
                    report = report_dir / filename
                    report.write_text(report_text("Report", project), encoding="utf-8")
                    run(INDEX_SCRIPT, "--root", str(root))
                    result = run(VALIDATE_SCRIPT, "--root", str(root))
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(expected_error, result.stdout)
                    report.unlink()


if __name__ == "__main__":
    unittest.main()
