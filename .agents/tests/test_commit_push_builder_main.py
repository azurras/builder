from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".agents" / "skills" / "commit-push-builder-main" / "scripts" / "commit_push_builder_main.py"


def load_module():
    spec = importlib.util.spec_from_file_location("commit_push_builder_main", SCRIPT)
    if spec is None or spec.loader is None:
        raise AssertionError(f"Unable to load {SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CommitPushBuilderMainTests(unittest.TestCase):
    def test_accepts_configured_builder_roots(self) -> None:
        module = load_module()

        roots = {str(path).replace("\\", "/") for path in module.EXPECTED_ROOTS}

        self.assertIn("C:/Users/Christopher/Developer/builder", roots)
        self.assertIn("/Users/cbell/Developer/builder", roots)

    def test_uses_builder_remote(self) -> None:
        module = load_module()

        self.assertEqual(module.EXPECTED_REMOTE, "https://github.com/azurras/builder.git")

    def test_rejects_old_azurras_root(self) -> None:
        module = load_module()

        old_root = Path("/Users/cbell/Developer/builder").resolve()

        self.assertFalse(module.is_expected_root(old_root))


if __name__ == "__main__":
    unittest.main()
