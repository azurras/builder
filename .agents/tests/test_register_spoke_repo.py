from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents" / "skills" / "register-spoke-repo" / "scripts" / "register_spoke_repo.py"


class RegisterSpokeRepoTests(unittest.TestCase):
    def test_updates_existing_spoke_with_windows_path(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            registry = root / "docs" / "spokes" / "repos.md"
            registry.parent.mkdir(parents=True)
            registry.write_text(
                "# Spoke Repositories\n\n"
                "<!-- spoke:christopherbell-dev -->\n"
                "## christopherbell.dev\n\n"
                "- Local path: `/mnt/c/Users/Christopher/Developer/christopherbell.dev`\n"
                "<!-- /spoke:christopherbell-dev -->\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--root",
                    str(root),
                    "--name",
                    "christopherbell.dev",
                    "--path",
                    r"C:\Users\Christopher\Developer\christopherbell.dev",
                    "--remote",
                    "https://github.com/azurras/christopherbell.dev.git",
                    "--purpose",
                    "Personal website",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            content = registry.read_text(encoding="utf-8")
            self.assertIn(r"- Local path: `C:\Users\Christopher\Developer\christopherbell.dev`", content)
            self.assertIn("- Remote: `https://github.com/azurras/christopherbell.dev.git`", content)


if __name__ == "__main__":
    unittest.main()
