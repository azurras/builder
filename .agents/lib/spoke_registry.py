"""Tracked spoke registry with per-machine path resolution.

spokes.json at the Builder root declares spokes without machine paths. A spoke's
local checkout resolves in this order:
1. spokes.local.json at the Builder root (ignored by Git): {"<slug>": "<path>"}
2. BUILDER_SPOKES_ROOT environment variable: <root>/<directory>
3. The Builder checkout's parent directory: <parent>/<directory>
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import os
from pathlib import Path
import re

REGISTRY_FILE = "spokes.json"
LOCAL_OVERRIDES_FILE = "spokes.local.json"
SPOKES_ROOT_ENV = "BUILDER_SPOKES_ROOT"
SLUG_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
REQUIRED_FIELDS = ("slug", "name", "repository", "defaultBranch", "description")


@dataclass(frozen=True)
class Spoke:
    slug: str
    name: str
    repository: str
    default_branch: str
    description: str
    directory: str


@dataclass(frozen=True)
class SpokeLocation:
    path: Path
    source: str


def repository_directory_name(repository: str) -> str:
    name = repository.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
    return name.removesuffix(".git")


def normalize_remote(remote: str) -> str:
    """Reduce https, ssh and scp-style Git remotes to host/owner/repo."""
    value = remote.strip().removesuffix("/").removesuffix(".git")
    scp_match = re.fullmatch(r"[^@/]+@([^:/]+):(.+)", value)
    if scp_match:
        host, path = scp_match.groups()
    else:
        url_match = re.fullmatch(r"[a-z+]+://(?:[^@/]+@)?([^/:]+)(?::\d+)?/(.+)", value)
        if not url_match:
            return value.lower()
        host, path = url_match.groups()
    return f"{host.lower()}/{path.strip('/').lower()}"


def _spoke_from_entry(entry: object, index: int) -> Spoke:
    if not isinstance(entry, dict):
        raise ValueError(f"{REGISTRY_FILE}: spokes[{index}] must be an object")
    missing = [field for field in REQUIRED_FIELDS if not isinstance(entry.get(field), str) or not entry[field].strip()]
    if missing:
        raise ValueError(f"{REGISTRY_FILE}: spokes[{index}] missing nonblank {', '.join(missing)}")
    slug = entry["slug"]
    if not SLUG_RE.fullmatch(slug) or slug == "index":
        raise ValueError(f"{REGISTRY_FILE}: spokes[{index}] slug {slug!r} must be a lowercase hyphenated project slug")
    directory = entry.get("directory") or repository_directory_name(entry["repository"])
    if not isinstance(directory, str) or Path(directory).name != directory or directory in {".", ".."}:
        raise ValueError(f"{REGISTRY_FILE}: spokes[{index}] directory must be a single folder name")
    return Spoke(slug, entry["name"], entry["repository"], entry["defaultBranch"], entry["description"], directory)


def load_spokes(builder_root: Path) -> list[Spoke]:
    registry_path = builder_root / REGISTRY_FILE
    try:
        document = json.loads(registry_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Spoke registry not found: {registry_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"{registry_path}: invalid JSON: {error}") from error
    entries = document.get("spokes") if isinstance(document, dict) else None
    if not isinstance(entries, list):
        raise ValueError(f"{registry_path}: expected an object with a 'spokes' list")
    spokes = [_spoke_from_entry(entry, index) for index, entry in enumerate(entries)]
    slugs = [spoke.slug for spoke in spokes]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicates:
        raise ValueError(f"{registry_path}: duplicate spoke slugs {duplicates}")
    return spokes


def find_spoke(builder_root: Path, slug: str) -> Spoke:
    spokes = load_spokes(builder_root)
    for spoke in spokes:
        if spoke.slug == slug:
            return spoke
    known = ", ".join(spoke.slug for spoke in spokes) or "none"
    raise ValueError(f"Unknown spoke {slug!r}; registered spokes: {known}")


def _local_overrides(builder_root: Path) -> dict[str, str]:
    overrides_path = builder_root / LOCAL_OVERRIDES_FILE
    if not overrides_path.exists():
        return {}
    try:
        overrides = json.loads(overrides_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(f"{overrides_path}: invalid JSON: {error}") from error
    if not isinstance(overrides, dict) or not all(isinstance(value, str) for value in overrides.values()):
        raise ValueError(f"{overrides_path}: expected an object mapping spoke slugs to paths")
    return overrides


def resolve_spoke_location(builder_root: Path, spoke: Spoke, environment: dict[str, str] | None = None) -> SpokeLocation:
    variables = os.environ if environment is None else environment
    override = _local_overrides(builder_root).get(spoke.slug)
    if override:
        return SpokeLocation(Path(override).expanduser().resolve(), LOCAL_OVERRIDES_FILE)
    spokes_root = variables.get(SPOKES_ROOT_ENV)
    if spokes_root:
        return SpokeLocation((Path(spokes_root).expanduser() / spoke.directory).resolve(), SPOKES_ROOT_ENV)
    return SpokeLocation((builder_root.parent / spoke.directory).resolve(), "sibling of Builder")
