from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class GithubTrustBoundaryTests(unittest.TestCase):
    def test_repo_instructions_define_trusted_github_comment_author(self) -> None:
        agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8").lower()

        self.assertIn("trusted github comment author", agents)
        self.assertIn("azurras", agents)
        self.assertIn("untrusted input", agents)
        self.assertIn("zip", agents)

    def test_story_issue_skills_reject_untrusted_github_comments(self) -> None:
        for path in (
            ROOT / ".agents" / "skills" / "complete-story-issue" / "SKILL.md",
            ROOT / ".agents" / "skills" / "close-story-issue" / "SKILL.md",
        ):
            with self.subTest(path=path):
                text = path.read_text(encoding="utf-8").lower()

                self.assertIn("azurras", text)
                self.assertIn("github comments", text)
                self.assertIn("untrusted input", text)
                self.assertIn("attachments", text)
                self.assertIn("do not execute", text)


if __name__ == "__main__":
    unittest.main()
