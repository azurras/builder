from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from project_registry_fixture import write_project_registry

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents/skills/save-session-memory/scripts/save_session_memory.py"
MIGRATION_SCRIPT = ROOT / ".agents/skills/save-session-memory/scripts/consolidate_project_memory.py"
MIGRATION_SOURCE_COMMIT = "78f0183"


def run(*args, body="Evidence."):
    return subprocess.run([sys.executable, "-B", str(SCRIPT), *args], input=body,
                          capture_output=True, text=True, timeout=20)


class ProjectMemoryTests(unittest.TestCase):
    def test_every_project_on_a_date_appends_to_that_date_file(self):
        with tempfile.TemporaryDirectory() as temp:
            write_project_registry(Path(temp), active=("sample", "other"))
            first = run("--root", temp, "--project", "sample", "--title", "Start",
                        "--date", "2099-01-01", "--time", "09:00", body="First evidence.")
            self.assertEqual(first.returncode, 0, first.stderr)
            path = Path(temp).resolve() / "docs/session-memory/2099-01-01.md"
            self.assertEqual(first.stdout.strip(), str(path))
            before = path.read_bytes()
            second = run("--root", temp, "--project", "other", "--title", "Finish",
                         "--date", "2099-01-01", "--time", "10:30", body="Final evidence.")
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertTrue(path.read_bytes().startswith(before))
            self.assertEqual(path.read_text(encoding="utf-8"),
                             "# 2099-01-01 Session Memory\n\n"
                             "Work, decisions, events, and evidence for every project on this date.\n\n"
                             "## 2099-01-01 09:00 - Start\n\n**Project:** sample\n\nFirst evidence.\n\n"
                             "## 2099-01-01 10:30 - Finish\n\n**Project:** other\n\nFinal evidence.\n")
            self.assertEqual(run("--root", temp, "--project", "sample", "--title", "Next day",
                                 "--date", "2099-02-01", body="Next day evidence.").returncode, 0)
            self.assertNotIn("Next day evidence.", path.read_text(encoding="utf-8"))
            self.assertIn("Next day evidence.", (path.parent / "2099-02-01.md").read_text(encoding="utf-8"))
            self.assertEqual(sorted(p.name for p in path.parent.iterdir()), ["2099-01-01.md", "2099-02-01.md"])

    def test_project_entries_select_only_the_named_project(self):
        sys.path.insert(0, str(ROOT / ".agents/lib"))
        from project_memory import project_entries
        day_text = ("# 2099-01-01 Session Memory\n\nIntro.\n\n"
                    "## 2099-01-01 09:00 - Start\n\n**Project:** sample\n\nOne.\n\n"
                    "## 2099-01-01 10:00 - Other work\n\n**Project:** sample-two\n\nTwo.\n\n"
                    "## 2099-01-01 11:00 - Finish\n\n**Project:** sample\n\nThree.\n")
        self.assertEqual([entry.splitlines()[0] for entry in project_entries(day_text, "sample")],
                         ["## 2099-01-01 09:00 - Start", "## 2099-01-01 11:00 - Finish"])

    def test_merged_memory_links_point_at_the_dated_file(self):
        sys.path.insert(0, str(ROOT / ".agents/lib"))
        from project_memory import retarget_merged_memory_links
        memory_text = ("[a](2099-01-01-sample.md#source-x) [b](../implementation-plans/2099-01-01-sample-plan.md) "
                       "[c](2099-01-01.md) [d](https://example.invalid/2099-01-01-sample.md)\n")
        self.assertEqual(retarget_merged_memory_links(memory_text, "docs/session-memory"),
                         "[a](2099-01-01.md#source-x) [b](../implementation-plans/2099-01-01-sample-plan.md) "
                         "[c](2099-01-01.md) [d](https://example.invalid/2099-01-01-sample.md)\n")
        plan_text = "[m](../session-memory/2099-01-01-sample.md) [p](2099-01-01-sample-plan.md)\n"
        self.assertEqual(retarget_merged_memory_links(plan_text, "docs/implementation-plans"),
                         "[m](../session-memory/2099-01-01.md) [p](2099-01-01-sample-plan.md)\n")

    def test_invalid_or_missing_project_and_empty_body_do_not_write(self):
        with tempfile.TemporaryDirectory() as temp:
            write_project_registry(Path(temp), active=("sample",), retired=("old-shop",))
            for project in ("../outside", "index", "", "Project Name"):
                self.assertNotEqual(run("--root", temp, "--project", project, "--title", "Entry").returncode, 0)
            for project, expected_message in (("stranger", "Unknown project 'stranger'"), ("old-shop", "retired")):
                refused = run("--root", temp, "--project", project, "--title", "Entry")
                self.assertNotEqual(refused.returncode, 0)
                self.assertIn(expected_message, refused.stderr)
            self.assertEqual(run("--root", temp, "--project", "builder", "--title", "Hub entry",
                                 "--date", "2099-01-01").returncode, 0)
            (Path(temp) / "docs/session-memory/2099-01-01.md").unlink()
            (Path(temp) / "docs/session-memory").rmdir()
            (Path(temp) / "docs").rmdir()
            self.assertNotEqual(run("--root", temp, "--title", "Entry").returncode, 0)
            self.assertNotEqual(run("--root", temp, "--project", "sample", "--title", "Entry", body=" ").returncode, 0)
            self.assertNotEqual(run("--root", temp, "--project", "sample", "--title", "Entry",
                                    "--date", "2099-02-30").returncode, 0)
            self.assertFalse((Path(temp) / "docs").exists())


class MigrationTransformTests(unittest.TestCase):
    def test_nested_examples_are_preserved_and_unknown_sources_rejected(self):
        script = MIGRATION_SCRIPT
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
            for skill, source in (("write-implementation-plan", "implementation-plan"),
                                  ("write-test-report", "test-report")):
                self.assertEqual((root / f".agents/skills/{skill}/references/example.md").read_text(),
                                 files[f"docs/templates/examples/{source}-example.md"])
            # The October 2026 merge moved each migrated project file into its date's file.
            memory = root / "docs/session-memory/2026-07-04.md"
            (root / "docs/session-memory/2026-07-04-builder.md").rename(memory)
            result = subprocess.run(command + ["--verify"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            imported_text = memory.read_text(encoding="utf-8")
            memory.write_text(imported_text.replace("Preserve me.", "Rewritten history."), encoding="utf-8")
            result = subprocess.run(command + ["--verify"], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Source preservation failed", result.stderr)
            memory.write_text(imported_text, encoding="utf-8")
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

    def test_link_existence_comes_from_the_supplied_source_tree(self):
        sys.path.insert(0, str(ROOT / ".agents/lib"))
        from memory_migration import Destination, transform
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp).resolve()
            source = root / "docs/old.md"
            destination = Destination(root / "docs/session-memory/project.md", "source-docs-old-md")
            retired_reference = root / ".agents/skills/retired/references/guide.md"
            body = "[guide](../.agents/skills/retired/references/guide.md)\n"
            mapping = {source: destination}
            relocated = transform(body, source, destination, mapping, {},
                                  existing_paths=frozenset({retired_reference}))
            self.assertEqual(relocated, "[guide](../../.agents/skills/retired/references/guide.md)\n")
            unrelocated = transform(body, source, destination, mapping, {})
            self.assertEqual(unrelocated, body)

    def test_stale_link_retarget_is_rejected(self):
        sys.path.insert(0, str(MIGRATION_SCRIPT.parent))
        from consolidate_project_memory import apply_later_link_retargets
        sections = {"docs/old.md": "[guide](../../current/guide.md)\n"}
        sources = {"docs/old.md": "2026-09-06-builder"}
        retargeted = apply_later_link_retargets(
            sections, sources,
            (("docs/session-memory/2026-09-06-builder.md", "../../current/guide.md", "../../renamed/guide.md"),))
        self.assertEqual(retargeted["docs/old.md"], "[guide](../../renamed/guide.md)\n")
        with self.assertRaises(ValueError):
            apply_later_link_retargets(
                sections, sources,
                (("docs/session-memory/2026-09-06-builder.md", "../../missing/guide.md", "../../renamed/guide.md"),))


class MigrationAuditTests(unittest.TestCase):
    def test_real_repository_passes_migration_audit(self):
        has_source_commit = subprocess.run(
            ["git", "-C", str(ROOT), "cat-file", "-e", f"{MIGRATION_SOURCE_COMMIT}^{{commit}}"],
            capture_output=True).returncode == 0
        if not has_source_commit:
            self.skipTest(f"source commit {MIGRATION_SOURCE_COMMIT} is not in this clone")
        result = subprocess.run(
            [sys.executable, "-B", str(MIGRATION_SCRIPT), "--root", str(ROOT),
             "--source-commit", MIGRATION_SOURCE_COMMIT, "--verify"],
            capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Every imported source body matches", result.stdout)
