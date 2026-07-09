from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SAVE_SCRIPT = ROOT / ".agents" / "skills" / "save-test-report" / "scripts" / "save_test_report.py"
INDEX_SCRIPT = ROOT / ".agents" / "skills" / "update-hub-indexes" / "scripts" / "update_hub_indexes.py"
VALIDATE_SCRIPT = ROOT / ".agents" / "skills" / "validate-hub-state" / "scripts" / "validate_hub_state.py"


class TestReportWorkflowTests(unittest.TestCase):
    def test_saves_test_report_with_dated_slug(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            result = subprocess.run(
                [
                    sys.executable,
                    str(SAVE_SCRIPT),
                    "--root",
                    str(root),
                    "--date",
                    "2099-04-05",
                    "--title",
                    "Issue 42 Local App Test",
                ],
                input=(
                    "# Issue 42 Local App Test\n\n"
                    "## Document Status\ncomplete\n\n"
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
                ),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            report = root / "docs" / "test-reports" / "2099-04-05-issue-42-local-app-test.md"
            self.assertEqual(Path(result.stdout.strip()).name, report.name)
            self.assertTrue(report.exists())
            self.assertIn("## Test Cases", report.read_text(encoding="utf-8"))

    def test_indexes_and_validates_test_reports(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            report_dir = root / "docs" / "test-reports"
            report_dir.mkdir(parents=True)
            (report_dir / "2099-04-05-sample-report.md").write_text(
                "# Sample Report\n\n"
                "## Document Status\ncomplete\n\n"
                "## Story/Issue\nIssue 42\n\n"
                "## Branch\n`codex/issue-42`\n\n"
                "## App / Environment\nlocalhost:8080\n\n"
                "## Local Run Details\n`./gradlew bootRun`\n\n"
                "## Test Cases\n- Health endpoint returns OK.\n\n"
                "## Data Sent\nGET /health\n\n"
                "## Response Received\n200 OK\n\n"
                "## Pass / Fail\nPASS\n\n"
                "## Evidence\n`curl http://localhost:8080/health`\n\n"
                "## Bugs / Follow-ups\nNone.\n",
                encoding="utf-8",
            )
            for directory in (
                "docs/session-memory",
                "docs/specs",
                "docs/implementation-plans",
                "docs/spokes",
                "docs/work",
                "docs/spoke-tasks",
                "docs/spoke-updates",
                "docs/spoke-reviews",
                "docs/decisions",
                "docs/work-closures",
                "docs/templates",
            ):
                (root / directory).mkdir(parents=True, exist_ok=True)
            for template in (
                "work-record.md",
                "spoke-task.md",
                "spoke-update.md",
                "spoke-review.md",
                "decision-record.md",
                "work-closure.md",
                "test-report.md",
            ):
                (root / "docs" / "templates" / template).write_text("# Template\n", encoding="utf-8")

            index_result = subprocess.run(
                [sys.executable, str(INDEX_SCRIPT), "--root", str(root)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(index_result.returncode, 0, index_result.stderr)
            self.assertIn("Sample Report", (report_dir / "index.md").read_text(encoding="utf-8"))

            validate_result = subprocess.run(
                [sys.executable, str(VALIDATE_SCRIPT), "--root", str(root)],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            self.assertEqual(validate_result.returncode, 0, validate_result.stdout + validate_result.stderr)


if __name__ == "__main__":
    unittest.main()
