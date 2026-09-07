from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SKILLS = ROOT / ".agents/skills"


def run(script, *args):
    return subprocess.run([sys.executable, "-B", str(script), *args], capture_output=True, text=True, timeout=30)


class RepositoryInspectionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.git("init", "-b", "main")
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "commit.gpgsign", "false")
        self.git("config", "core.hooksPath", str(self.root / "no-hooks"))
        (self.repo / "file.md").write_text("tracked", encoding="utf-8")
        self.git("add", "file.md")
        self.git("commit", "-m", "Fixture")
        self.script = SKILLS / "manage-spoke-repositories/scripts/manage_spoke_repositories.py"

    def git(self, *args):
        return subprocess.run(["git", *args], cwd=self.repo, text=True, capture_output=True, check=True)

    def command(self, *args):
        return run(self.script, *args, "--root", str(self.root), "--path", str(self.repo))

    def test_default_inspection_is_read_only(self):
        before = {p.relative_to(self.repo): (p.read_bytes(), p.stat().st_mtime_ns)
                  for p in self.repo.rglob("*") if p.is_file()}
        result = self.command()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("clean", result.stdout)
        self.assertFalse((self.root / "docs").exists())
        self.assertEqual(before, {p.relative_to(self.repo): (p.read_bytes(), p.stat().st_mtime_ns)
                                for p in self.repo.rglob("*") if p.is_file()})

    def test_snapshot_appends_to_project_and_unchanged_state_does_not_rewrite(self):
        self.assertEqual(self.command("snapshot", "--project", "sample").returncode, 0)
        memory = self.root / "docs/session-memory/sample.md"
        before = memory.read_bytes(), memory.stat().st_mtime_ns
        self.assertEqual(self.command("snapshot", "--project", "sample").returncode, 0)
        self.assertEqual((memory.read_bytes(), memory.stat().st_mtime_ns), before)
        (self.repo / "file.md").write_text("changed", encoding="utf-8")
        self.assertEqual(self.command("snapshot", "--project", "sample").returncode, 0)
        self.assertTrue(memory.read_bytes().startswith(before[0]))
        self.assertEqual(memory.read_text(encoding="utf-8").count("<!-- git-snapshot:"), 2)
        self.assertEqual({p.name for p in (self.root / "docs").iterdir()}, {"session-memory"})

    def test_git_failure_is_explicit_and_persisted_honestly(self):
        self.git("config", "core.bare", "true")
        result = self.command("snapshot", "--project", "sample")
        self.assertNotEqual(result.returncode, 0)
        text = (self.root / "docs/session-memory/sample.md").read_text(encoding="utf-8")
        self.assertIn("Inspection error", text)
        self.assertNotIn("\nclean\n", text)

    def test_snapshot_requires_project_before_any_write(self):
        self.assertNotEqual(self.command("snapshot").returncode, 0)
        self.assertFalse((self.root / "docs").exists())
        self.assertNotEqual(self.command("register").returncode, 0)


class MaintenanceModeTests(unittest.TestCase):
    def test_check_read_only_and_refresh_only_three_folders(self):
        script = SKILLS / "maintain-builder-hub/scripts/maintain_builder_hub.py"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def snapshot():
                return {p.relative_to(root): (p.read_bytes(), p.stat().st_mtime_ns)
                        for p in root.rglob("*") if p.is_file()}
            self.assertNotEqual(run(script, "--root", temp).returncode, 0)
            self.assertEqual(list(root.iterdir()), [])
            result = run(script, "refresh", "--root", temp)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertEqual({p.name for p in (root / "docs").iterdir()},
                             {"implementation-plans", "test-reports", "session-memory"})
            memory = root / "docs/session-memory/sample.md"
            memory.write_text("# Sample\n\n## 2099-01-01 Progress\nEvidence.\n", encoding="utf-8")
            before = snapshot()
            self.assertNotEqual(run(script, "check", "--root", temp).returncode, 0)
            self.assertEqual(snapshot(), before)
            self.assertEqual(run(script, "refresh", "--root", temp).returncode, 0)
            before = snapshot()
            self.assertEqual(run(script, "check", "--root", temp).returncode, 0)
            self.assertEqual(snapshot(), before)
            self.assertIn("Sample", (memory.parent / "index.md").read_text(encoding="utf-8"))
            (root / "docs/active.md").write_text("# Stale dashboard", encoding="utf-8")
            self.assertNotEqual(run(script, "check", "--root", temp).returncode, 0)


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
