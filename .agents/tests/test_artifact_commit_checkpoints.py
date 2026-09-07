from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents" / "skills"


class ArtifactCommitCheckpointTests(unittest.TestCase):
    def test_develop_loop_has_artifact_commit_checkpoints(self) -> None:
        skill = (SKILLS / "complete-builder-work" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("## Artifact Commit Checkpoints", skill)
        for artifact in (
            "implementation plan",
            "test report",
            "session memory",
        ):
            self.assertIn(
                f"{artifact} must be committed and pushed before the loop continues",
                skill.lower(),
            )

    def test_default_delivery_starts_with_plan_and_spec_is_optional(self) -> None:
        skill = (SKILLS / "complete-builder-work" / "SKILL.md").read_text(encoding="utf-8").lower()
        self.assertIn("start directly with `plan-builder-work` plan and review modes", skill)
        self.assertIn("a separate spec is optional", skill)
        self.assertIn("requirements, acceptance criteria, relevant design decisions", skill)
        self.assertNotIn("project spec must be committed and pushed before the loop continues", skill)
        planning = (SKILLS / "plan-builder-work" / "references" / "review.md").read_text(encoding="utf-8").lower()
        self.assertIn("its absence alone is not a blocker", planning)

    def test_artifact_saving_skills_block_next_step_until_pushed(self) -> None:
        for skill_name in (
            "plan-builder-work",
            "record-runtime-verification",
            "save-session-memory",
        ):
            with self.subTest(skill=skill_name):
                skill = (SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8").lower()

                self.assertIn("must be committed and pushed", skill)
                self.assertIn("before moving to the next", skill)

    def test_orchestrator_covers_review_publish_ci_merge_and_closure(self) -> None:
        skill = (SKILLS / "complete-builder-work" / "SKILL.md").read_text(encoding="utf-8").lower()
        prompt = (
            SKILLS / "complete-builder-work" / "agents" / "openai.yaml"
        ).read_text(encoding="utf-8").lower()

        for required in (
            "`plan-builder-work` plan and review modes",
            "improve the plan until no blockers remain",
            "create a pull request",
            "wait for required ci gates",
            "merge only after required gates pass",
            "close story/issue",
        ):
            self.assertIn(required, skill)

        for required_prompt_text in (
            "implementation plan review",
            "pr creation",
            "ci gates",
            "merge",
            "issue closure",
        ):
            self.assertIn(required_prompt_text, prompt)


if __name__ == "__main__":
    unittest.main()
