from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents/lib"))
from spoke_worktrees import (LinkedWorktree, PullRequestHead, github_repository_of, merged_heads_of,  # noqa: E402
                             pull_request_summary, remove_worktree, stale_worktree_decisions)

SCRIPT = ROOT / ".agents/skills/deliver-change/scripts/manage_spoke_repositories.py"
REPOSITORY = "https://github.com/example/site.dev.git"
TEN_DAYS_LATER = time.time() + 10 * 86_400


def git(repo, *args):
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout.strip()


def commit_file(repo, relative_path, text, message):
    (repo / relative_path).write_text(text, encoding="utf-8")
    git(repo, "add", relative_path)
    git(repo, "commit", "-m", message)


class WorktreePruneTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        workspace = Path(self.temp.name).resolve()
        self.checkout = workspace / "site.dev"
        self.worktrees = workspace / "site.dev-worktrees"
        self.checkout.mkdir()
        for args in (("init", "-b", "main"), ("config", "user.name", "Fixture"),
                     ("config", "user.email", "fixture@example.invalid"), ("config", "commit.gpgsign", "false"),
                     ("config", "core.autocrlf", "false"), ("remote", "add", "origin", REPOSITORY)):
            git(self.checkout, *args)
        commit_file(self.checkout, "README.md", "site\n", "Base")
        commit_file(self.checkout, ".gitignore", "build/\n", "Ignore build output")
        self.publish_main()

    def publish_main(self):
        git(self.checkout, "update-ref", "refs/remotes/origin/main", "main")

    def add_worktree(self, name, *, branch=None, folder=None):
        path = (folder or self.worktrees) / name
        branch_args = ["-b", branch] if branch else ["--detach"]
        git(self.checkout, "worktree", "add", *branch_args, str(path), "main")
        return path

    def decisions_by_name(self, now_seconds=TEN_DAYS_LATER):
        return {decision.worktree.path.name: decision
                for decision in stale_worktree_decisions(self.checkout, "main", 7, now_seconds)}

    def test_merged_clean_idle_worktrees_are_stale_including_squash_merges(self):
        fast_forwarded = self.add_worktree("fast-forwarded", branch="work/fast-forwarded")
        squashed = self.add_worktree("squashed", branch="work/squashed")
        commit_file(squashed, "feature.txt", "feature\n", "Feature")
        git(self.checkout, "merge", "--squash", "work/squashed")
        git(self.checkout, "commit", "-m", "Squash feature")
        self.publish_main()
        (fast_forwarded / "build").mkdir()
        (fast_forwarded / "build" / "output.bin").write_text("ignored", encoding="utf-8")

        decisions = self.decisions_by_name()

        self.assertTrue(decisions["fast-forwarded"].is_stale, decisions["fast-forwarded"].reason)
        self.assertTrue(decisions["squashed"].is_stale, decisions["squashed"].reason)

    def test_unmerged_dirty_untracked_locked_recent_and_foreign_worktrees_are_kept(self):
        unmerged = self.add_worktree("unmerged", branch="work/unmerged")
        commit_file(unmerged, "feature.txt", "unpublished\n", "Unpublished")
        dirty = self.add_worktree("dirty", branch="work/dirty")
        (dirty / "README.md").write_text("edited\n", encoding="utf-8")
        untracked = self.add_worktree("untracked", branch="work/untracked")
        (untracked / "notes.txt").write_text("scratch", encoding="utf-8")
        self.add_worktree("locked", branch="work/locked")
        git(self.checkout, "worktree", "lock", str(self.worktrees / "locked"))
        self.add_worktree("elsewhere", folder=self.checkout.parent / "scratch")

        decisions = self.decisions_by_name()
        recent = self.decisions_by_name(now_seconds=time.time())

        expected_reasons = {"unmerged": "is not on origin/main", "dirty": "tracked changes",
                            "untracked": "untracked file", "locked": "locked",
                            "elsewhere": "outside the checkout's worktree folders"}
        for name, reason in expected_reasons.items():
            with self.subTest(name=name):
                self.assertFalse(decisions[name].is_stale)
                self.assertIn(reason, decisions[name].reason)
        self.assertFalse(any(decision.is_stale for decision in recent.values()))

    def test_line_ending_only_changes_do_not_keep_a_worktree(self):
        line_endings = self.add_worktree("line-endings", branch="work/line-endings")
        (line_endings / "README.md").write_bytes(b"site\r\n")

        self.assertTrue(self.decisions_by_name()["line-endings"].is_stale)

    def test_linked_worktree_is_refused_as_the_checkout(self):
        linked = self.add_worktree("linked", branch="work/linked")
        with self.assertRaisesRegex(ValueError, "linked worktree"):
            stale_worktree_decisions(linked, "main", 7)

    def test_removal_deletes_the_folder_and_its_branch(self):
        stale = self.add_worktree("stale", branch="work/stale")
        decision = self.decisions_by_name()["stale"]

        outcome = remove_worktree(self.checkout, decision.worktree, "main")

        self.assertEqual(outcome, "removed worktree and branch work/stale")
        self.assertFalse(stale.exists())
        self.assertEqual(git(self.checkout, "branch", "--list", "work/stale"), "")
        self.assertNotIn("stale", git(self.checkout, "worktree", "list"))

    def test_merged_pull_request_head_counts_as_merged_even_when_main_moved_on(self):
        rewritten = self.add_worktree("rewritten", branch="work/rewritten")
        commit_file(rewritten, "README.md", "site from the branch\n", "Branch edit")
        commit_file(self.checkout, "README.md", "site rewritten on main\n", "Conflicting main edit")
        self.publish_main()
        branch_head = git(rewritten, "rev-parse", "HEAD")

        without_pull_requests = self.decisions_by_name()["rewritten"]
        with_pull_requests = {decision.worktree.path.name: decision for decision in stale_worktree_decisions(
            self.checkout, "main", 7, TEN_DAYS_LATER, merged_pull_request_heads=frozenset({branch_head}))}

        self.assertFalse(without_pull_requests.is_stale)
        self.assertTrue(with_pull_requests["rewritten"].is_stale)
        self.assertIn("by a merged pull request", with_pull_requests["rewritten"].reason)

    def test_pull_request_summary_tells_a_person_what_github_knows(self):
        worktree = LinkedWorktree(self.worktrees / "w", "b" * 40, "work/w", False)
        cases = {
            "no pull request: never published": {},
            "PR #7 closed without merging": {"work/w": [PullRequestHead(7, "CLOSED", "b" * 40, "u")]},
            "PR #8 merged, but the worktree has commits after it":
                {"work/w": [PullRequestHead(8, "MERGED", "a" * 40, "u")]},
            "PR #9 open": {"work/w": [PullRequestHead(9, "OPEN", "b" * 40, "u")]},
        }
        for expected, pull_requests in cases.items():
            with self.subTest(expected=expected):
                self.assertEqual(pull_request_summary(worktree, pull_requests), expected)
        self.assertEqual(merged_heads_of({"x": [PullRequestHead(1, "MERGED", "c" * 40, "u"),
                                                 PullRequestHead(2, "CLOSED", "d" * 40, "u")]}), frozenset({"c" * 40}))

    def test_only_github_repositories_have_pull_requests(self):
        self.assertEqual(github_repository_of("https://github.com/Azurras/christopherbell.dev.git"),
                         "azurras/christopherbell.dev")
        with self.assertRaises(ValueError):
            github_repository_of("https://gitlab.com/example/site.git")

    def test_command_dry_run_reports_without_removing(self):
        stale = self.add_worktree("stale", branch="work/stale")
        builder = self.checkout.parent / "builder"
        builder.mkdir()
        (builder / "spokes.json").write_text(json.dumps({"spokes": [{
            "slug": "site-dev", "name": "site.dev", "repository": REPOSITORY, "defaultBranch": "main",
            "description": "Sample spoke"}]}), encoding="utf-8")
        old_seconds = time.time() - 10 * 86_400
        git_folder = Path(git(stale, "rev-parse", "--absolute-git-dir"))
        for name in ("HEAD", "index", "logs/HEAD"):
            if (git_folder / name).exists():
                os.utime(git_folder / name, (old_seconds, old_seconds))

        result = subprocess.run([sys.executable, "-B", str(SCRIPT), "prune-worktrees", "--spoke", "site-dev",
                                 "--dry-run", "--root", str(builder)],
                                capture_output=True, text=True, encoding="utf-8", timeout=60)

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn(f"[would remove] {stale}", result.stdout)
        self.assertTrue(stale.exists())


if __name__ == "__main__":
    unittest.main()
