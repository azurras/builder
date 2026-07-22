from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents" / "skills"
STYLE_SKILL = SKILLS / "write-jane-street-style-code"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class JaneStreetCodeStyleTests(unittest.TestCase):
    def test_skill_entrypoint_requires_brief_and_routes_references(self) -> None:
        skill_path = STYLE_SKILL / "SKILL.md"
        metadata_path = STYLE_SKILL / "agents" / "openai.yaml"

        skill = read(skill_path).lower()
        metadata = read(metadata_path).lower()

        self.assertIn("name: write-jane-street-style-code", skill)
        self.assertIn("description: use when", skill)
        for required in (
            "before-edit brief",
            "**behavior:**",
            "**invariants:**",
            "**boundary/api:**",
            "**effects and failures:**",
            "**tests and evidence:**",
            "do not edit code",
            "references/design-and-api.md",
            "references/testing-and-review.md",
            "references/java.md",
            "references/javascript.md",
            "references/python.md",
            "references/templates-and-configuration.md",
        ):
            self.assertIn(required, skill)

        self.assertNotIn("language-adaptations.md", skill)
        self.assertIn("$write-jane-street-style-code", metadata)
        self.assertIn("before-edit brief", metadata)
        self.assertIn("allow_implicit_invocation: true", metadata)

    def test_design_and_testing_references_are_authoritative(self) -> None:
        design_path = STYLE_SKILL / "references" / "design-and-api.md"
        testing_path = STYLE_SKILL / "references" / "testing-and-review.md"

        self.assertTrue(design_path.is_file())
        self.assertTrue(testing_path.is_file())

        design = read(design_path).lower()
        testing = read(testing_path).lower()
        for required in (
            "## table of contents",
            "invalid states",
            "validation boundary",
            "uniform interfaces",
            "absence",
            "expected domain failure",
            "preserve error context",
            "mutation ownership",
            "concurrency",
            "abstraction",
            "dependency direction",
            "performance",
            "compatibility",
            "worked example",
        ):
            self.assertIn(required, design)

        for required in (
            "## table of contents",
            "test-selection matrix",
            "property",
            "scenario",
            "snapshot",
            "integration",
            "concurrency",
            "semantic production change",
            "## blockers",
            "## warnings",
            "finding format",
        ):
            self.assertIn(required, testing)

    def test_language_references_supply_idiomatic_decisions_and_examples(self) -> None:
        references = {
            "java.md": ("sealed", "junit"),
            "javascript.md": ("async", "boundary validation"),
            "python.md": ("dataclass", "pytest"),
            "templates-and-configuration.md": ("escaping", "explicit defaults"),
        }

        for filename, language_terms in references.items():
            with self.subTest(reference=filename):
                path = STYLE_SKILL / "references" / filename
                self.assertTrue(path.is_file())
                content = read(path).lower()
                for required in (
                    "## table of contents",
                    "## decision guide",
                    "## good and bad",
                    "repository-native",
                    *language_terms,
                ):
                    self.assertIn(required, content)

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
        self.assertIn("before-edit brief", save_skill)
        self.assertIn("before-edit brief", review_skill)
        self.assertIn("before-edit brief", dispatch_skill)

    def test_spoke_review_checks_house_style_compliance(self) -> None:
        folder = SKILLS / "review-spoke-work"
        skill = read(folder / "SKILL.md").lower()
        prompt = read(folder / "agents" / "openai.yaml").lower()

        self.assertIn("house-style compliance", skill)
        self.assertIn("merge readiness", skill)
        self.assertIn("write-jane-street-style-code", skill)
        self.assertIn("blockers", skill)
        self.assertIn("warnings", skill)
        self.assertIn("finding format", skill)
        self.assertIn("$write-jane-street-style-code", prompt)


if __name__ == "__main__":
    unittest.main()
