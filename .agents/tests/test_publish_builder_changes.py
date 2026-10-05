from __future__ import annotations

import importlib.util
import contextlib
import io
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents" / "skills" / "publish-builder-changes" / "scripts" / "publish_builder_changes.py"


def load_module():
    spec = importlib.util.spec_from_file_location("publish_builder_changes", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PublishBuilderChangesTests(unittest.TestCase):
    def test_uses_builder_remote(self) -> None:
        module = load_module()

        self.assertEqual(module.EXPECTED_REMOTE, "https://github.com/azurras/builder.git")


class CommitPushBehaviorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve() / "builder"
        self.remote = Path(self.temp.name).resolve() / "origin.git"
        self.root.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Builder Test")
        self.git("config", "user.email", "builder@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(Path(self.temp.name) / "no-hooks"))
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        self.git("remote", "add", "origin", str(self.remote))
        (self.root / "baseline.md").write_text("baseline\n", encoding="utf-8")
        self.git("add", "baseline.md")
        self.git("commit", "-m", "Baseline")
        self.git("push", "-u", "origin", "main")
        self.module = load_module()

    def git(self, *args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=self.root, check=True, capture_output=True, text=True
        ).stdout.strip()

    def invoke(self, *args: str) -> int:
        output = io.StringIO()
        with (
            patch.object(self.module, "EXPECTED_REMOTE", str(self.remote)),
            patch("sys.argv", [str(SCRIPT), "--root", str(self.root), *args]),
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(output),
        ):
            try:
                return self.module.main()
            except SystemExit as error:
                return int(error.code)
            finally:
                self.output = output.getvalue()

    def test_commits_only_selected_literal_file(self) -> None:
        for name in ("chosen[1].md", "chosen1.md", "unrelated.md"):
            (self.root / name).write_text(name, encoding="utf-8")
        result = self.invoke("--message", "Selected", "--path", "chosen[1].md")
        self.assertEqual(result, 0, self.output)
        self.assertEqual(self.git("diff-tree", "--no-commit-id", "--name-only", "-r", "HEAD"), "chosen[1].md")
        self.assertIn("?? unrelated.md", self.git("status", "--short"))
        self.assertIn("?? chosen1.md", self.git("status", "--short"))

    def test_refuses_unrelated_staged_changes_without_mutating_index(self) -> None:
        (self.root / "chosen.md").write_text("selected", encoding="utf-8")
        (self.root / "unrelated.md").write_text("unrelated", encoding="utf-8")
        self.git("add", "unrelated.md")
        before = self.git("write-tree")
        self.assertNotEqual(self.invoke("--message", "Selected", "--path", "chosen.md"), 0)
        self.assertEqual(self.git("write-tree"), before)
        self.assertEqual(self.git("log", "-1", "--format=%s"), "Baseline")

    def test_deleted_directory_cannot_expand_selection_or_mutate_index(self) -> None:
        folder = self.root / "nested"
        folder.mkdir()
        (folder / "one.md").write_text("one", encoding="utf-8")
        (folder / "two.md").write_text("two", encoding="utf-8")
        self.git("add", "nested")
        self.git("commit", "-m", "Nested baseline")
        (folder / "one.md").unlink()
        (folder / "two.md").unlink()
        folder.rmdir()
        before = self.git("write-tree")
        self.assertNotEqual(self.invoke("--message", "Too broad", "--path", "nested"), 0)
        self.assertEqual(self.git("write-tree"), before)

    def test_requires_selection_and_rejects_broad_or_outside_paths(self) -> None:
        (self.root / "chosen.md").write_text("selected", encoding="utf-8")
        self.assertNotEqual(self.invoke("--message", "Missing selection"), 0)
        for selected in (".", "../outside.md", str(self.root / "chosen.md"), ".git/config", "missing.md"):
            with self.subTest(selected=selected):
                self.assertNotEqual(self.invoke("--message", "Invalid", "--path", selected), 0)
                self.assertEqual(self.git("diff", "--cached", "--name-only"), "")

    def test_dry_run_preserves_index_head_and_remote(self) -> None:
        (self.root / "chosen.md").write_text("selected", encoding="utf-8")
        before = (self.git("write-tree"), self.git("rev-parse", "HEAD"), self.git("ls-remote", "origin", "refs/heads/main"))
        self.assertEqual(self.invoke("--message", "Preview", "--path", "chosen.md", "--dry-run"), 0)
        self.assertEqual((self.git("write-tree"), self.git("rev-parse", "HEAD"), self.git("ls-remote", "origin", "refs/heads/main")), before)

    def test_refuses_subdirectory_root(self) -> None:
        (self.root / "nested").mkdir()
        (self.root / "nested" / "chosen.md").write_text("selected", encoding="utf-8")
        output = io.StringIO()
        with (
            patch.object(self.module, "EXPECTED_REMOTE", str(self.remote)),
            patch("sys.argv", [str(SCRIPT), "--root", str(self.root / "nested"), "--message", "Nested", "--path", "chosen.md", "--dry-run"]),
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(output),
        ):
            self.assertNotEqual(self.module.main(), 0)
        self.assertIn("not the repository top level", output.getvalue())

    def test_refuses_linked_worktree(self) -> None:
        linked = Path(self.temp.name).resolve() / "linked"
        self.git("worktree", "add", "-b", "linked", str(linked))
        output = io.StringIO()
        with (
            patch.object(self.module, "EXPECTED_REMOTE", str(self.remote)),
            patch("sys.argv", [str(SCRIPT), "--root", str(linked), "--push-only", "--dry-run"]),
            contextlib.redirect_stdout(output),
            contextlib.redirect_stderr(output),
        ):
            self.assertNotEqual(self.module.main(), 0)
        self.assertIn("linked worktree", output.getvalue())

    def test_selected_deletion_is_committed(self) -> None:
        (self.root / "baseline.md").unlink()
        self.assertEqual(self.invoke("--message", "Delete selected", "--path", "baseline.md"), 0)
        self.assertEqual(self.git("ls-tree", "--name-only", "HEAD"), "")

    def test_push_only_recovers_committed_change_after_failed_push(self) -> None:
        subprocess.run(["git", "--git-dir", str(self.remote), "config", "receive.denyCurrentBranch", "refuse"], check=True)
        subprocess.run(["git", "--git-dir", str(self.remote), "config", "core.bare", "false"], check=True)
        subprocess.run(["git", "--git-dir", str(self.remote), "symbolic-ref", "HEAD", "refs/heads/main"], check=True)
        (self.root / "chosen.md").write_text("selected", encoding="utf-8")
        self.assertNotEqual(self.invoke("--message", "Recoverable", "--path", "chosen.md"), 0)
        committed = self.git("rev-parse", "HEAD")
        self.assertEqual(self.git("log", "-1", "--format=%s"), "Recoverable")
        self.assertEqual(self.git("status", "--short"), "")
        subprocess.run(["git", "--git-dir", str(self.remote), "config", "core.bare", "true"], check=True)
        (self.root / "unrelated.md").write_text("leave alone", encoding="utf-8")
        self.git("add", "unrelated.md")
        before_index = self.git("write-tree")
        self.assertEqual(self.invoke("--push-only"), 0)
        self.assertEqual(self.git("rev-parse", "HEAD"), committed)
        self.assertEqual(self.git("write-tree"), before_index)
        self.assertEqual(self.git("ls-remote", "origin", "refs/heads/main").split()[0], committed)


if __name__ == "__main__":
    unittest.main()
