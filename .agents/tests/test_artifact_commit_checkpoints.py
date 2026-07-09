from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents" / "skills"


class ArtifactCommitCheckpointTests(unittest.TestCase):
    def test_develop_loop_has_artifact_commit_checkpoints(self) -> None:
        skill = (SKILLS / "complete-story-issue" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("## Artifact Commit Checkpoints", skill)
        for artifact in (
            "project spec",
            "implementation plan",
            "test report",
            "session memory",
        ):
            self.assertIn(
                f"{artifact} must be committed and pushed before the loop continues",
                skill.lower(),
            )

    def test_artifact_saving_skills_block_next_step_until_pushed(self) -> None:
        for skill_name in (
            "save-project-spec",
            "save-implementation-plan",
            "save-test-report",
            "save-session-memory",
        ):
            with self.subTest(skill=skill_name):
                skill = (SKILLS / skill_name / "SKILL.md").read_text(encoding="utf-8").lower()

                self.assertIn("must be committed and pushed", skill)
                self.assertIn("before moving to the next", skill)


if __name__ == "__main__":
    unittest.main()
