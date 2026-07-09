from __future__ import annotations

import datetime as dt
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents" / "lib"))

from artifact_io import save_dated_markdown


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
            )

            self.assertEqual(path.name, "2099-04-05-issue-42-local-app-test.md")
            self.assertEqual(path.read_text(encoding="utf-8"), "# Report\n")

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


if __name__ == "__main__":
    unittest.main()
