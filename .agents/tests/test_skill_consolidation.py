from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents/skills"
OWNERS = {'close-hub-work': 'coordinate-builder-work', 'dispatch-spoke-task': 'coordinate-builder-work', 'ingest-spoke-update': 'coordinate-builder-work', 'start-hub-work': 'coordinate-builder-work', 'save-decision-record': 'plan-builder-work', 'save-project-spec': 'plan-builder-work', 'save-implementation-plan': 'plan-builder-work', 'validate-implementation-plan': 'plan-builder-work', 'save-test-report': 'record-runtime-verification', 'validate-test-report': 'record-runtime-verification', 'register-spoke-repo': 'manage-spoke-repositories', 'sync-spoke-state': 'manage-spoke-repositories', 'update-hub-indexes': 'maintain-builder-hub', 'validate-hub-state': 'maintain-builder-hub'}

WRITERS = {
    "start-hub-work": ("start_hub_work", "work", "hub-work"),
    "dispatch-spoke-task": ("dispatch_spoke_task", "spoke-tasks", "spoke-task"),
    "ingest-spoke-update": ("ingest_spoke_update", "spoke-updates", "spoke-update"),
    "review-spoke-work": ("review_spoke_work", "spoke-reviews", "spoke-review"),
    "close-hub-work": ("close_hub_work", "work-closures", "work-closure"),
    "save-decision-record": ("save_decision_record", "decisions", "decision"),
}


def run(script: Path, *args: str, body: str | None = None):
    return subprocess.run([sys.executable, str(script), *args], input=body,
                          text=True, capture_output=True, timeout=30)


class ArtifactWriterCompatibilityTests(unittest.TestCase):
    def test_legacy_writers_preserve_paths_content_overwrite_and_slug_edges(self):
        for skill, (command, directory, fallback) in WRITERS.items():
            with self.subTest(skill=skill), tempfile.TemporaryDirectory() as temp:
                script = SKILLS / OWNERS.get(skill, skill) / "scripts" / f"{command}.py"
                args = ("--root", temp, "--title", "Example: Record!", "--date", "2099-04-05")
                result = run(script, *args, body="# Example\nEvidence.\n")
                target = Path(temp) / "docs" / directory / "2099-04-05-example-record.md"
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(target.read_text(), "# Example\nEvidence.\n")
                self.assertNotEqual(run(script, *args, body="# Changed").returncode, 0)
                self.assertEqual(target.read_text(), "# Example\nEvidence.\n")
                self.assertEqual(run(script, *args, "--overwrite", body="# Changed").returncode, 0)
                self.assertEqual(target.read_text(), "# Changed\n")
                for title in ("!", "a" * 79 + " b"):
                    result = run(script, "--root", temp, "--title", title, "--date", "2099-04-05", body="# Edge")
                    self.assertEqual(result.returncode, 0, result.stderr)
                    slug = fallback if title == "!" else "a" * 79 + ("" if skill == "start-hub-work" else "-")
                    self.assertEqual(Path(result.stdout.strip()).name, f"2099-04-05-{slug}.md")
                self.assertNotEqual(run(script, "--root", temp, "--title", "Empty", body="").returncode, 0)


class RepositoryInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "spoke"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Test")
        self.git("config", "user.email", "test@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.root / "no-hooks"))
        (self.repo / "file.md").write_text("tracked")
        self.git("add", "file.md")
        self.git("commit", "-m", "Baseline")
        self.git("remote", "add", "origin", "https://example.invalid/spoke.git")
        registry = self.root / "docs/spokes/repos.md"
        registry.parent.mkdir(parents=True)
        registry.write_text(f"<!-- spoke:example -->\n## Example\n- Local path: `{self.repo}`\n<!-- /spoke:example -->\n")
        self.script = SKILLS / "manage-spoke-repositories/scripts/sync_spoke_state.py"

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, check=True,
                              text=True, capture_output=True).stdout

    def test_inspect_is_read_only(self):
        result = run(self.script, "--root", str(self.root), "--inspect")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("clean", result.stdout)
        self.assertFalse((self.root / "docs/spokes/state.md").exists())

    def test_unchanged_snapshot_preserves_bytes_and_mtime(self):
        self.assertEqual(run(self.script, "--root", str(self.root)).returncode, 0)
        snapshot = self.root / "docs/spokes/state.md"
        before = (snapshot.read_bytes(), snapshot.stat().st_mtime_ns)
        self.assertEqual(run(self.script, "--root", str(self.root)).returncode, 0)
        self.assertEqual((snapshot.read_bytes(), snapshot.stat().st_mtime_ns), before)
        (self.repo / "file.md").write_text("modified")
        self.assertEqual(run(self.script, "--root", str(self.root)).returncode, 0)
        self.assertNotEqual(snapshot.read_bytes(), before[0])

    def test_git_failure_is_not_clean(self):
        self.git("config", "core.bare", "true")
        result = run(self.script, "--root", str(self.root))
        self.assertNotEqual(result.returncode, 0)
        snapshot = (self.root / "docs/spokes/state.md").read_text()
        self.assertIn("error", snapshot.lower())
        self.assertNotIn("\nclean\n", snapshot)

    def test_missing_registry_is_an_error_without_writes(self):
        (self.root / "docs/spokes/repos.md").unlink()
        result = run(self.script, "--root", str(self.root), "--inspect")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("registry is missing", result.stderr.lower())
        self.assertFalse((self.root / "docs/spokes/state.md").exists())



class PublicModeTests(unittest.TestCase):
    setUp = RepositoryInspectionTests.setUp
    git = RepositoryInspectionTests.git
    def test_manage_defaults_to_inspect_and_requires_explicit_snapshot(self):
        script = SKILLS / "manage-spoke-repositories/scripts/manage_spoke_repositories.py"
        before = {p.relative_to(self.repo): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.repo.rglob("*") if p.is_file()}
        result = run(script, "--root", str(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("clean", result.stdout)
        self.assertFalse((self.root / "docs/spokes/state.md").exists())
        after = {p.relative_to(self.repo): (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in self.repo.rglob("*") if p.is_file()}
        self.assertEqual(after, before)
        result = run(script, "snapshot", "--root", str(self.root))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.root / "docs/spokes/state.md").is_file())

    def test_management_rejects_unknown_mode_and_registers_explicitly(self):
        script = SKILLS / "manage-spoke-repositories/scripts/manage_spoke_repositories.py"
        self.assertNotEqual(run(script, "snapshott", "--root", str(self.root)).returncode, 0)
        result = run(script, "register", "--root", str(self.root), "--name", "Second",
                     "--path", str(self.repo), "--remote", "https://example.invalid/second.git",
                     "--purpose", "Fixture repository")
        self.assertEqual(result.returncode, 0, result.stderr)
        content = (self.root / "docs/spokes/repos.md").read_text(encoding="utf-8")
        self.assertIn("## Example", content)
        self.assertIn("## Second", content)
        self.assertFalse((self.root / "docs/spokes/state.md").exists())


class MaintenanceModeTests(unittest.TestCase):
    def test_check_is_read_only_and_refresh_is_explicit(self):
        script = SKILLS / "maintain-builder-hub/scripts/maintain_builder_hub.py"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            templates = root / "docs/templates"
            templates.mkdir(parents=True)
            for name in ("work-record", "spoke-task", "spoke-update", "spoke-review",
                         "decision-record", "work-closure", "test-report"):
                (templates / f"{name}.md").write_text("# Template\n", encoding="utf-8")
            def snapshot():
                return {p.relative_to(root): (p.read_bytes(), p.stat().st_mtime_ns)
                        for p in root.rglob("*") if p.is_file()}
            before = snapshot()
            result = run(script, "--root", temp)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(snapshot(), before)
            result = run(script, "refresh", "--root", temp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((root / "docs/active.md").is_file())
            for optional in ("specs", "decisions"):
                self.assertFalse((root / "docs" / optional).exists())
            self.assertNotIn("Missing artifact directory: docs/specs", result.stdout)
            self.assertNotIn("Missing artifact directory: docs/decisions", result.stdout)
            self.assertEqual({p.name for p in (root / "docs/session-memory").iterdir()}, {"index.md"})
            self.assertFalse((root / ".git").exists())
            refreshed = snapshot()
            self.assertEqual(run(script, "check", "--root", temp).returncode, 0)
            self.assertEqual(snapshot(), refreshed)
            (root / "docs/specs").mkdir()
            (root / "docs/specs/2099-04-05-new.md").write_text("# New Spec\n", encoding="utf-8")
            stale = snapshot()
            self.assertNotEqual(run(script, "check", "--root", temp).returncode, 0)
            self.assertEqual(snapshot(), stale)
            self.assertEqual(run(script, "refresh", "--root", temp).returncode, 0)
            self.assertIn("New Spec", (root / "docs/specs/index.md").read_text(encoding="utf-8"))
            decision = root / "docs/decisions/2099-04-05-choice.md"
            decision.parent.mkdir()
            decision.write_text("# Choice\n", encoding="utf-8")
            validator = SKILLS / "maintain-builder-hub/scripts/validate_hub_state.py"
            self.assertNotEqual(run(validator, "--root", temp).returncode, 0)
            self.assertEqual(run(script, "refresh", "--root", temp).returncode, 0)
            self.assertIn("Choice", (decision.parent / "index.md").read_text(encoding="utf-8"))
            self.assertEqual(run(script, "check", "--root", temp).returncode, 0)
            (templates / "work-record.md").unlink()
            self.assertNotEqual(run(script, "refresh", "--root", temp).returncode, 0)


class SkillDiscoveryTests(unittest.TestCase):
    def test_discovery_is_exact_and_active_links_resolve(self):
        expected = {"complete-builder-work", "plan-builder-work", "coordinate-builder-work",
                    "record-runtime-verification", "manage-spoke-repositories", "maintain-builder-hub",
                    "commit-push-builder-main", "verify-local-spring-app", "write-jane-street-style-code",
                    "review-spoke-work", "save-session-memory"}
        self.assertEqual({p.name for p in SKILLS.iterdir() if p.is_dir()}, expected)
        self.assertEqual({p.parent.name for p in SKILLS.glob("*/SKILL.md")}, expected)
        self.assertEqual({p.parents[1].name for p in SKILLS.glob("*/agents/openai.yaml")}, expected)
        for name in expected:
            folder = SKILLS / name
            for path in folder.rglob("*.md"):
                content = path.read_text(encoding="utf-8")
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", content):
                    if "://" not in target and not target.startswith("#"):
                        self.assertTrue((path.parent / target.split("#", 1)[0]).exists(), f"{path}: {target}")
                for command in re.findall(r"\.agents/skills/[a-z0-9-]+/scripts/[a-z0-9_]+\.py", content):
                    self.assertTrue((ROOT / command).is_file(), f"{path}: {command}")


if __name__ == "__main__":
    unittest.main()
