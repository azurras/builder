from pathlib import Path
import datetime as dt
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / ".agents/lib"))
from spoke_registry import (SPOKES_ROOT_ENV, ProjectStatus, find_spoke, is_remote_repository, load_spokes,
                            normalize_remote, project_statuses_of, register_spoke, require_active_project,
                            resolve_spoke_location)

SCRIPT = ROOT / ".agents/skills/deliver-change/scripts/manage_spoke_repositories.py"
REPOSITORY = "https://github.com/example/site.dev.git"


def spoke_entry(**overrides):
    entry = {"slug": "site-dev", "name": "site.dev", "repository": REPOSITORY,
             "defaultBranch": "main", "description": "Sample spoke"}
    entry.update(overrides)
    return entry


def project_entry(**overrides):
    entry = {"slug": "home-lab", "name": "Home lab", "status": "active", "description": "Sample standalone project"}
    entry.update(overrides)
    return entry


class SpokeRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.workspace = Path(self.temp.name).resolve()
        self.builder = self.workspace / "builder"
        self.builder.mkdir()

    def write_registry(self, *entries, projects=()):
        document = {"spokes": list(entries)}
        if projects:
            document["projects"] = list(projects)
        (self.builder / "spokes.json").write_text(json.dumps(document), encoding="utf-8")

    def test_repository_registry_is_valid_and_has_no_machine_paths(self):
        spokes = load_spokes(ROOT)
        self.assertIn("christopherbell-dev", [spoke.slug for spoke in spokes])
        statuses = project_statuses_of(ROOT)
        self.assertEqual(statuses["builder"], ProjectStatus.ACTIVE)
        self.assertEqual(statuses["personal-computer-cleanup"], ProjectStatus.ACTIVE)
        self.assertEqual(statuses["software-handoff-kit"], ProjectStatus.RETIRED)
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

    def test_project_slugs_are_the_hub_spokes_and_standalone_projects(self):
        self.write_registry(spoke_entry(), projects=[project_entry(), project_entry(slug="old-shop", status="retired")])
        self.assertEqual(project_statuses_of(self.builder), {
            "builder": ProjectStatus.ACTIVE, "site-dev": ProjectStatus.ACTIVE,
            "home-lab": ProjectStatus.ACTIVE, "old-shop": ProjectStatus.RETIRED})
        for active_slug in ("builder", "site-dev", "home-lab"):
            require_active_project(self.builder, active_slug)
        with self.assertRaisesRegex(ValueError, "retired"):
            require_active_project(self.builder, "old-shop")
        with self.assertRaisesRegex(ValueError, "Unknown project 'missing'.*builder, home-lab, site-dev"):
            require_active_project(self.builder, "missing")

    def test_registry_without_projects_still_loads(self):
        self.write_registry(spoke_entry())
        self.assertEqual(set(project_statuses_of(self.builder)), {"builder", "site-dev"})

    def test_rejects_invalid_projects(self):
        invalid_registries = {
            "reserved for the Builder hub": ([spoke_entry(slug="builder")], []),
            "already used": ([spoke_entry()], [project_entry(slug="site-dev")]),
            "status 'paused'": ([], [project_entry(status="paused")]),
            "missing nonblank description": ([], [project_entry(description=" ")]),
            r"projects\[1\] slug":([], [project_entry(), project_entry(slug="Bad Slug")]),
        }
        for expected_message, (spokes, projects) in invalid_registries.items():
            with self.subTest(expected_message=expected_message):
                self.write_registry(*spokes, projects=projects)
                with self.assertRaisesRegex(ValueError, expected_message):
                    project_statuses_of(self.builder)
        self.write_registry(projects=[project_entry(), project_entry()])
        with self.assertRaisesRegex(ValueError, "already used"):
            project_statuses_of(self.builder)

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

    def test_register_appends_validated_entry_in_registry_format(self):
        self.write_registry(spoke_entry())
        registered = register_spoke(self.builder, slug="blog", name="blog", description="Blog spoke",
                                    repository="git@github.com:example/blog.git", default_branch="trunk")
        self.assertEqual((registered.slug, registered.directory, registered.default_branch), ("blog", "blog", "trunk"))
        registry_text = (self.builder / "spokes.json").read_text(encoding="utf-8")
        self.assertEqual(registry_text, json.dumps({"spokes": [spoke_entry(), {
            "slug": "blog", "name": "blog", "repository": "git@github.com:example/blog.git",
            "defaultBranch": "trunk", "description": "Blog spoke"}]}, indent=2) + "\n")
        self.assertEqual([spoke.slug for spoke in load_spokes(self.builder)], ["site-dev", "blog"])

    def test_register_refuses_conflicts_and_local_paths_without_changing_registry(self):
        self.write_registry(spoke_entry())
        before = (self.builder / "spokes.json").read_bytes()
        refusals = {
            "already registered": dict(slug="site-dev", repository="https://github.com/example/other.git"),
            "already registered as": dict(slug="copy", repository="git@github.com:Example/site.dev.git"),
            "Checkout folder": dict(slug="fork", repository="https://github.com/fork/Site.dev.git"),
            "not a local path": dict(slug="local", repository="C:\\code\\site.dev"),
            "lowercase hyphenated": dict(slug="Bad Slug", repository="https://github.com/example/bad.git"),
        }
        for expected_message, fields in refusals.items():
            with self.subTest(expected_message=expected_message):
                with self.assertRaisesRegex(ValueError, expected_message):
                    register_spoke(self.builder, name="spoke", default_branch="main", description="Spoke", **fields)
                self.assertEqual((self.builder / "spokes.json").read_bytes(), before)

    def test_register_refuses_a_standalone_project_slug_and_keeps_projects(self):
        self.write_registry(spoke_entry(), projects=[project_entry()])
        before = (self.builder / "spokes.json").read_bytes()
        with self.assertRaisesRegex(ValueError, "already registered as a standalone project"):
            register_spoke(self.builder, slug="home-lab", name="home-lab", description="Spoke",
                           repository="https://github.com/example/home-lab.git", default_branch="main")
        self.assertEqual((self.builder / "spokes.json").read_bytes(), before)
        register_spoke(self.builder, slug="blog", name="blog", description="Blog spoke",
                       repository="https://github.com/example/blog.git", default_branch="main")
        self.assertIn("home-lab", project_statuses_of(self.builder))

    def test_remote_forms_exclude_local_paths(self):
        for remote in (REPOSITORY, "ssh://git@github.com/example/site.dev.git", "git@github.com:example/site.dev.git"):
            with self.subTest(remote=remote):
                self.assertTrue(is_remote_repository(remote))
        for local_path in ("C:\\code\\site", "C:/code/site", "/home/me/site", "../site", "file:///srv/site.git"):
            with self.subTest(local_path=local_path):
                self.assertFalse(is_remote_repository(local_path))

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

    def test_register_command_adds_spoke_that_list_then_shows(self):
        registered = self.command("register", "--spoke", "blog", "--name", "blog", "--description", "Blog spoke",
                                  "--repository", "https://github.com/example/blog.git")
        self.assertEqual(registered.returncode, 0, registered.stdout + registered.stderr)
        self.assertIn("clone --spoke blog", registered.stdout)
        self.assertEqual(find_spoke(self.builder, "blog").default_branch, "main")
        self.assertIn("blog", self.command("list").stdout)

    def test_register_command_rejects_missing_fields_and_conflicts(self):
        before = (self.builder / "spokes.json").read_bytes()
        incomplete = self.command("register", "--spoke", "blog", "--repository", "https://github.com/example/blog.git")
        self.assertEqual(incomplete.returncode, 2)
        self.assertIn("register requires", incomplete.stderr)
        duplicate = self.command("register", "--spoke", "site-dev", "--name", "site.dev", "--description", "Again",
                                 "--repository", "https://github.com/example/again.git")
        self.assertEqual(duplicate.returncode, 2)
        self.assertIn("already registered", duplicate.stderr)
        self.assertEqual((self.builder / "spokes.json").read_bytes(), before)

    def test_snapshot_defaults_project_to_spoke_slug(self):
        self.set_origin(REPOSITORY)
        result = self.command("snapshot", "--spoke", "site-dev")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        memory_files = list((self.builder / "docs/session-memory").iterdir())
        self.assertEqual([path.name for path in memory_files], [f"{dt.date.today()}.md"])
        self.assertIn("**Project:** site-dev", memory_files[0].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
