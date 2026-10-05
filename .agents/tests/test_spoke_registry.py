from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents/lib"))
from spoke_registry import (SPOKES_ROOT_ENV, find_spoke, load_spokes, normalize_remote,
                            resolve_spoke_location)

SCRIPT = ROOT / ".agents/skills/deliver-change/scripts/manage_spoke_repositories.py"
REPOSITORY = "https://github.com/example/site.dev.git"


def spoke_entry(**overrides):
    entry = {"slug": "site-dev", "name": "site.dev", "repository": REPOSITORY,
             "defaultBranch": "main", "description": "Sample spoke"}
    entry.update(overrides)
    return entry


class SpokeRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name).resolve()
        self.builder = self.workspace / "builder"
        self.builder.mkdir()

    def write_registry(self, *entries):
        (self.builder / "spokes.json").write_text(json.dumps({"spokes": list(entries)}), encoding="utf-8")

    def test_repository_registry_is_valid_and_has_no_machine_paths(self):
        spokes = load_spokes(ROOT)
        self.assertIn("christopherbell-dev", [spoke.slug for spoke in spokes])
        registry_text = (ROOT / "spokes.json").read_text(encoding="utf-8")
        self.assertNotRegex(registry_text, r"(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/|/home/")

    def test_directory_defaults_to_repository_name(self):
        self.write_registry(spoke_entry())
        self.assertEqual(find_spoke(self.builder, "site-dev").directory, "site.dev")

    def test_rejects_invalid_entries(self):
        invalid_entries = (
            [spoke_entry(slug="Bad Slug")],
            [spoke_entry(repository="")],
            [spoke_entry(directory="../escape")],
            [spoke_entry(), spoke_entry()],
        )
        for entries in invalid_entries:
            with self.subTest(entries=entries):
                self.write_registry(*entries)
                with self.assertRaises(ValueError):
                    load_spokes(self.builder)

    def test_unknown_spoke_names_registered_spokes(self):
        self.write_registry(spoke_entry())
        with self.assertRaisesRegex(ValueError, "site-dev"):
            find_spoke(self.builder, "missing")

    def test_location_precedence_is_override_then_environment_then_sibling(self):
        self.write_registry(spoke_entry())
        spoke = find_spoke(self.builder, "site-dev")
        sibling = resolve_spoke_location(self.builder, spoke, environment={})
        self.assertEqual(sibling.path, self.workspace / "site.dev")

        from_environment = resolve_spoke_location(self.builder, spoke, {SPOKES_ROOT_ENV: str(self.workspace / "code")})
        self.assertEqual(from_environment.path, self.workspace / "code" / "site.dev")

        override = self.workspace / "elsewhere" / "site"
        (self.builder / "spokes.local.json").write_text(json.dumps({"site-dev": str(override)}), encoding="utf-8")
        from_override = resolve_spoke_location(self.builder, spoke, {SPOKES_ROOT_ENV: str(self.workspace / "code")})
        self.assertEqual(from_override.path, override)

    def test_normalize_remote_matches_https_ssh_and_scp_forms(self):
        expected = "github.com/example/site.dev"
        for remote in (REPOSITORY, "https://github.com/Example/site.dev", "git@github.com:example/site.dev.git",
                       "ssh://git@github.com/example/site.dev.git"):
            with self.subTest(remote=remote):
                self.assertEqual(normalize_remote(remote), expected)
        self.assertNotEqual(normalize_remote("https://github.com/other/site.dev.git"), expected)


class SpokeCommandTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name).resolve()
        self.builder = self.workspace / "builder"
        self.builder.mkdir()
        (self.builder / "spokes.json").write_text(json.dumps({"spokes": [spoke_entry()]}), encoding="utf-8")
        self.spoke = self.workspace / "site.dev"
        self.spoke.mkdir()
        for args in (("init", "-b", "main"), ("config", "user.name", "Fixture"),
                     ("config", "user.email", "fixture@example.invalid"), ("config", "commit.gpgsign", "false"),
                     ("commit", "--allow-empty", "-m", "Fixture")):
            subprocess.run(["git", *args], cwd=self.spoke, check=True, capture_output=True)

    def command(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *args, "--root", str(self.builder)],
                              capture_output=True, text=True, timeout=30,
                              env={name: value for name, value in os.environ.items() if name != SPOKES_ROOT_ENV})

    def set_origin(self, remote):
        subprocess.run(["git", "remote", "add", "origin", remote], cwd=self.spoke, check=True, capture_output=True)

    def test_list_shows_resolved_sibling(self):
        result = self.command("list")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("site-dev", result.stdout)
        self.assertIn("present", result.stdout)

    def test_locate_and_inspect_accept_matching_ssh_origin(self):
        self.set_origin("git@github.com:example/site.dev.git")
        located = self.command("locate", "--spoke", "site-dev")
        self.assertEqual(located.returncode, 0, located.stdout + located.stderr)
        self.assertIn("matches registry", located.stdout)
        inspected = self.command("inspect", "--spoke", "site-dev")
        self.assertEqual(inspected.returncode, 0, inspected.stdout + inspected.stderr)
        self.assertFalse((self.builder / "docs").exists())

    def test_origin_mismatch_fails_locate_and_inspect(self):
        self.set_origin("https://github.com/someone-else/site.dev.git")
        self.assertNotEqual(self.command("locate", "--spoke", "site-dev").returncode, 0)
        inspected = self.command("inspect", "--spoke", "site-dev")
        self.assertNotEqual(inspected.returncode, 0)
        self.assertIn("Registry mismatch", inspected.stdout)

    def test_clone_refuses_existing_path(self):
        result = self.command("clone", "--spoke", "site-dev")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("existing path", result.stderr)

    def test_snapshot_defaults_project_to_spoke_slug(self):
        self.set_origin(REPOSITORY)
        result = self.command("snapshot", "--spoke", "site-dev")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual([path.name.endswith("-site-dev.md") for path in (self.builder / "docs/session-memory").iterdir()],
                         [True])


if __name__ == "__main__":
    unittest.main()
