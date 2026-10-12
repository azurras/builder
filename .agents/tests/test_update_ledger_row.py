from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_artifact_quality import LIVING_PLAN  # noqa: E402

SCRIPT = ROOT / ".agents/skills/write-implementation-plan/scripts/update_ledger_row.py"
LEDGER = """
| Slice | Area | State |
|---|---|---|
| 18 | Configuration | done: [plan](a.md), PR #1 `aaaaaaa` |
| 19 | Shared folder | 19a in progress: [plan](b.md); 19b in progress: [plan](c.md) |
| 19x | Notes | in progress: [plan](b.md) |
"""
UMBRELLA_PLAN = LIVING_PLAN.replace("## Goals", LEDGER.lstrip() + "\n## Goals")


class UpdateLedgerRowTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.plan_file = Path(temp.name) / "umbrella.md"

    def run_script(self, *arguments):
        return subprocess.run([sys.executable, str(SCRIPT), "--plan", str(self.plan_file), *arguments],
                              capture_output=True, text=True, encoding="utf-8", timeout=60, check=False)

    def test_replaces_text_only_in_the_named_row_and_keeps_crlf(self):
        self.plan_file.write_bytes(UMBRELLA_PLAN.replace("\n", "\r\n").encode("utf-8"))

        completed = self.run_script("--row", "19", "--replace", "19a in progress: [plan](b.md)",
                                    "--with", "19a done: [plan](b.md), PR #2 `bbbbbbb`")

        self.assertEqual(completed.returncode, 0, completed.stderr)
        expected = UMBRELLA_PLAN.replace("| 19 | Shared folder | 19a in progress: [plan](b.md);",
                                         "| 19 | Shared folder | 19a done: [plan](b.md), PR #2 `bbbbbbb`;")
        self.assertEqual(self.plan_file.read_bytes(), expected.replace("\n", "\r\n").encode("utf-8"))

    def test_missing_or_repeated_text_and_unknown_rows_leave_the_plan_unchanged(self):
        self.plan_file.write_text(UMBRELLA_PLAN, encoding="utf-8", newline="\n")
        original_bytes = self.plan_file.read_bytes()
        cases = (
            (["--row", "20", "--replace", "in progress", "--with", "done"], "found 0"),
            (["--row", "19", "--replace", "in progress", "--with", "done"], "2 times"),
            (["--row", "18", "--replace", "in progress", "--with", "done"], "0 times"),
            (["--row", "19", "--replace", "19a in progress", "--with", "two\nlines"], "one line"),
        )
        for arguments, message in cases:
            with self.subTest(arguments=arguments):
                completed = self.run_script(*arguments)

                self.assertEqual(completed.returncode, 1)
                self.assertIn(message, completed.stderr)
                self.assertEqual(self.plan_file.read_bytes(), original_bytes)

    def test_a_result_that_fails_plan_validation_is_not_written(self):
        broken_plan = UMBRELLA_PLAN.replace("## Outcome\nPending.\n", "")
        self.plan_file.write_text(broken_plan, encoding="utf-8", newline="\n")

        completed = self.run_script("--row", "18", "--replace", "done", "--with", "closed")

        self.assertEqual(completed.returncode, 1)
        self.assertIn("quality checks failed", completed.stderr)
        self.assertEqual(self.plan_file.read_text(encoding="utf-8"), broken_plan)


if __name__ == "__main__":
    unittest.main()
