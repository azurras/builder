"""Registry fixture for tests that write records into a temporary Builder root."""
import json
from pathlib import Path


def write_project_registry(builder_root: Path, *, active: tuple[str, ...] = (),
                           retired: tuple[str, ...] = ()) -> None:
    """Write a spokes.json with no spokes and the given standalone projects; builder is always valid."""
    projects = [{"slug": slug, "name": slug, "status": status, "description": "Fixture project"}
                for status, slugs in (("active", active), ("retired", retired)) for slug in slugs]
    builder_root.mkdir(parents=True, exist_ok=True)
    (builder_root / "spokes.json").write_text(json.dumps({"spokes": [], "projects": projects}), encoding="utf-8")
