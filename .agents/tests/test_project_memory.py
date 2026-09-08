from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/skills/save-session-memory/scripts/save_session_memory.py"


def run(*args, body="Evidence."):
    return subprocess.run([sys.executable, "-B", str(SCRIPT), *args], input=body,
                          capture_output=True, text=True, timeout=20)


class ProjectMemoryTests(unittest.TestCase):
    def test_same_day_appends_and_different_dates_have_separate_files(self):
        with tempfile.TemporaryDirectory() as temp:
            first = run("--root", temp, "--project", "sample", "--title", "Start",
                        "--date", "2099-01-01", body="First evidence.")
            self.assertEqual(first.returncode, 0, first.stderr)
            path = Path(temp) / "docs/session-memory/2099-01-01-sample.md"
            before = path.read_bytes()
            second = run("--root", temp, "--project", "sample", "--title", "Finish",
                         "--date", "2099-01-01", body="Final evidence.")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertTrue(path.read_bytes().startswith(before))
            text = path.read_text(encoding="utf-8")
            self.assertIn("2099-01-01", text)
            self.assertIn("First evidence.", text)
            self.assertIn("Final evidence.", text)
            self.assertEqual(len(list(path.parent.glob("*.md"))), 1)
            self.assertEqual(run("--root", temp, "--project", "sample", "--title", "Next day",
                                 "--date", "2099-02-01", body="Next day evidence.").returncode, 0)
            self.assertNotIn("Next day evidence.", path.read_text())
            self.assertIn("Next day evidence.", (path.parent / "2099-02-01-sample.md").read_text())
            self.assertEqual(run("--root", temp, "--project", "other", "--title", "Start").returncode, 0)
            self.assertEqual(len(list(path.parent.glob("*.md"))), 3)

    def test_invalid_or_missing_project_and_empty_body_do_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            for project in ("../outside", "index", "", "Project Name"):
                self.assertNotEqual(run("--root", temp, "--project", project, "--title", "Entry").returncode, 0)
            self.assertNotEqual(run("--root", temp, "--title", "Entry").returncode, 0)
            self.assertNotEqual(run("--root", temp, "--project", "sample", "--title", "Entry", body=" ").returncode, 0)
            self.assertNotEqual(run("--root", temp, "--project", "sample", "--title", "Entry",
                                    "--date", "2099-02-30").returncode, 0)
            self.assertFalse((Path(temp) / "docs").exists())


class MigrationTransformTests(unittest.TestCase):
    def test_nested_examples_are_preserved_and_unknown_sources_rejected(self):
        script = ROOT / ".agents/skills/save-session-memory/scripts/consolidate_project_memory.py"
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            def git(*args):
                return subprocess.run(["git", "-C", temp, *args], check=True,
                                      capture_output=True, text=True)
            git("init")
            files = {
                "docs/session-memory/2026-07-04-example.md": "# Builder history\nPreserve me.\n",
                "docs/templates/examples/test-report-example.md": "# Report example\nExample evidence.\n",
                "docs/templates/examples/implementation-plan-example.md": "# Plan example\nExample requirements.\n",
            }
            for name, body in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body, encoding="utf-8")
            git("add", "docs")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "-m", "Fixture")
            command = [sys.executable, "-B", str(script), "--root", temp, "--source-commit", "HEAD"]
            result = subprocess.run(command + ["--apply"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((root / "docs/templates").exists())
            self.assertIn("Preserve me.", (root / "docs/session-memory/2026-07-04-builder.md").read_text())
            for skill, source in (("plan-builder-work", "implementation-plan"),
                                  ("record-runtime-verification", "test-report")):
                self.assertEqual((root / f".agents/skills/{skill}/references/example.md").read_text(),
                                 files[f"docs/templates/examples/{source}-example.md"])
            result = subprocess.run(command + ["--verify"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            unexpected = root / "docs/unclassified.md"
            unexpected.write_text("Unknown history", encoding="utf-8")
            git("add", "docs/unclassified.md")
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                "-c", "commit.gpgsign=false", "commit", "-m", "Unknown source")
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Unaccounted source documents", result.stderr)

    def test_source_anchors_cross_links_and_code_preservation(self):
        sys.path.insert(0, str(ROOT / ".agents/lib"))
        from memory_migration import Destination, heading_ids, source_anchor, source_section, transform
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            source = root / "docs/work/2099-01-01-same.md"
            other = root / "docs/specs/2099-01-01-same.md"
            plan = root / "docs/implementation-plans/2099-01-01-plan.md"
            dest = root / "docs/session-memory/project.md"
            body = "# One\n[other](../specs/2099-01-01-same.md#details)\n[plan](../implementation-plans/2099-01-01-plan.md)\n```md\n# Literal heading\n[untouched](../work/example.md)\n```\n"
            other_body = "# Details\nFirst.\n# Details\nSecond.\n"
            a = source_anchor("docs/work/2099-01-01-same.md")
            b = source_anchor("docs/specs/2099-01-01-same.md")
            self.assertNotEqual(a, b)
            mapping = {source: Destination(dest, a), other: Destination(dest, b), plan: Destination(plan)}
            headings = {source: set(heading_ids(body).values()), other: set(heading_ids(other_body).values())}
            result = transform(body, source, mapping[source], mapping, headings)
            self.assertIn(f"[other](#{b}--details)", result)
            self.assertIn("[plan](../implementation-plans/2099-01-01-plan.md)", result)
            self.assertIn("```md\n# Literal heading\n[untouched](../work/example.md)\n```", result)
            other_result = transform(other_body, other, mapping[other], mapping, headings)
            self.assertIn(b + "--details-1", other_result)
            section = source_section("docs/work/2099-01-01-same.md", body, result, "abc123")
            self.assertIn(result, section)
            self.assertEqual(section.count("<!-- migrated-source:"), 1)
            self.assertIn("abc123", section)
            with self.assertRaises(ValueError):
                transform("[bad](../specs/2099-01-01-same.md#missing)", source, mapping[source], mapping, headings)
