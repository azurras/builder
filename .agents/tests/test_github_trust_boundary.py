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

if __name__ == "__main__":
    unittest.main()
