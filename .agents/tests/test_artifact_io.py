from __future__ import annotations

import datetime as dt
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents" / "lib"))

from artifact_io import save_dated_markdown
from builder_hub import DatedFile, parse_dated_file


class ArtifactIoTests(unittest.TestCase):
    def test_save_dated_markdown_writes_slugged_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            path = save_dated_markdown(
                root=root,
                directory="docs/test-reports",
                title="Issue 42: Local App Test!",
                body="# Report\n",
                fallback_slug="test-report",
                artifact_date=dt.date(2099, 4, 5),
                artifact_time=dt.time(9, 5),
            )

            self.assertEqual(path.name, "2099-04-05-09-05-issue-42-local-app-test.md")
            self.assertEqual(path.read_text(encoding="utf-8"), "# Report\n")

    def test_save_dated_markdown_writes_lf_line_endings_for_any_body(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)

            path = save_dated_markdown(
                root=root,
                directory="docs/test-reports",
                title="Line endings",
                body="# Report\r\n\r\nWindows line.\r\nOld Mac line.\rUnix line.\n",
                fallback_slug="test-report",
                artifact_date=dt.date(2099, 4, 5),
                artifact_time=dt.time(9, 5),
            )

            self.assertEqual(
                path.read_bytes(),
                b"# Report\n\nWindows line.\nOld Mac line.\nUnix line.\n")

    def test_save_dated_markdown_refuses_overwrite_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            kwargs = {
                "root": root,
                "directory": "docs/specs",
                "title": "Same",
                "body": "# First\n",
                "fallback_slug": "spec",
                "artifact_date": dt.date(2099, 4, 5),
            }
            save_dated_markdown(**kwargs)

            with self.assertRaises(FileExistsError):
                save_dated_markdown(**{**kwargs, "body": "# Second\n"})

    def test_overwrite_replaces_an_older_record_named_without_a_time(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            older_record = root / "docs/test-reports/2099-04-05-same.md"
            older_record.parent.mkdir(parents=True)
            older_record.write_text("# First\n", encoding="utf-8")

            path = save_dated_markdown(root=root, directory="docs/test-reports", title="Same", body="# Second\n",
                                       fallback_slug="test-report", artifact_date=dt.date(2099, 4, 5),
                                       artifact_time=dt.time(18, 0), overwrite=True)

            self.assertEqual(path.name, older_record.name)
            self.assertEqual(older_record.read_text(encoding="utf-8"), "# Second\n")
            self.assertEqual([entry.name for entry in older_record.parent.iterdir()], ["2099-04-05-same.md"])

    def test_parse_dated_file_reads_an_optional_time(self) -> None:
        cases = {
            "2099-04-05-09-30-builder-plan.md": DatedFile("2099-04-05", "09:30", "builder-plan"),
            "2099-04-05-builder-plan.md": DatedFile("2099-04-05", None, "builder-plan"),
            "2099-04-05-24-00-builder-plan.md": DatedFile("2099-04-05", None, "24-00-builder-plan"),
            "2026-09-23-2026-09-23-site-audit.md": DatedFile("2026-09-23", None, "2026-09-23-site-audit"),
            "notes.md": None,
        }
        for name, expected in cases.items():
            with self.subTest(name=name):
                self.assertEqual(parse_dated_file(Path(name)), expected)


if __name__ == "__main__":
    unittest.main()
