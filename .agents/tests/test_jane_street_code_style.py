from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents" / "skills"
STYLE_SKILL = SKILLS / "write-jane-street-style-code"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class JaneStreetCodeStyleTests(unittest.TestCase):
    def test_skill_package_declares_house_style_contract(self) -> None:
        skill_path = STYLE_SKILL / "SKILL.md"
        metadata_path = STYLE_SKILL / "agents" / "openai.yaml"
        reference_path = STYLE_SKILL / "references" / "language-adaptations.md"

        self.assertTrue(skill_path.is_file())
        self.assertTrue(metadata_path.is_file())
        self.assertTrue(reference_path.is_file())

        skill = read(skill_path)
        skill_lower = skill.lower()
        metadata_lower = read(metadata_path).lower()
        reference_lower = read(reference_path).lower()

        self.assertIn("name: write-jane-street-style-code", skill)
        self.assertIn("description: Use when", skill)
        for required in (
            "before writing or modifying code",
            "encode valid states",
            "narrow and uniform interfaces",
            "mutation, side effects, and failure behavior explicit",
            "property-based",
            "small, cohesive, and reviewable",
            "repository-native",
            "final review",
        ):
            self.assertIn(required, skill_lower)

        self.assertIn("$write-jane-street-style-code", metadata_lower)
        self.assertIn("allow_implicit_invocation: true", metadata_lower)
        for heading in ("### java", "### javascript", "### python", "### templates"):
            self.assertIn(heading, reference_lower)

    def test_repo_and_orchestrator_require_the_style_skill(self) -> None:
        agents = read(ROOT / "AGENTS.md").lower()
        orchestrator = read(SKILLS / "complete-story-issue" / "SKILL.md").lower()
        prompt = read(
            SKILLS / "complete-story-issue" / "agents" / "openai.yaml"
        ).lower()

        for required in (
            "## code-writing standard",
            "before creating or modifying",
            "`write-jane-street-style-code`",
            "read-only inspection",
        ):
            self.assertIn(required, agents)

        self.assertIn(
            "before writing or modifying code, invoke `write-jane-street-style-code`",
            orchestrator,
        )
        self.assertIn("$write-jane-street-style-code", prompt)

    def test_planning_and_dispatch_carry_the_style_skill(self) -> None:
        contracts = {
            "save": SKILLS / "save-implementation-plan",
            "review": SKILLS / "review-implementation-plan",
            "dispatch": SKILLS / "dispatch-spoke-task",
        }

        for name, folder in contracts.items():
            with self.subTest(contract=name):
                skill = read(folder / "SKILL.md").lower()
                prompt = read(folder / "agents" / "openai.yaml").lower()
                self.assertIn("write-jane-street-style-code", skill)
                self.assertIn("$write-jane-street-style-code", prompt)

        save_skill = read(contracts["save"] / "SKILL.md").lower()
        review_skill = read(contracts["review"] / "SKILL.md").lower()
        dispatch_skill = read(contracts["dispatch"] / "SKILL.md").lower()
        self.assertIn("every code-changing task", save_skill)
        self.assertIn("reject the plan", review_skill)
        self.assertIn("before code changes", dispatch_skill)

    def test_spoke_review_checks_house_style_compliance(self) -> None:
        folder = SKILLS / "review-spoke-work"
        skill = read(folder / "SKILL.md").lower()
        prompt = read(folder / "agents" / "openai.yaml").lower()

        self.assertIn("house-style compliance", skill)
        self.assertIn("merge readiness", skill)
        self.assertIn("write-jane-street-style-code", skill)
        self.assertIn("$write-jane-street-style-code", prompt)


if __name__ == "__main__":
    unittest.main()
