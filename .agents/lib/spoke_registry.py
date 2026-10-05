"""Tracked project registry with per-machine spoke path resolution.

spokes.json at the Builder root is the only registry. It declares spokes (the
repositories Builder coordinates) and, under "projects", work that has no
repository. Together with the hub itself ("builder") these are the only project
slugs a plan, test report or memory file may name. A spoke's local checkout
resolves in this order:
1. spokes.local.json at the Builder root (ignored by Git): {"<slug>": "<path>"}
2. BUILDER_SPOKES_ROOT environment variable: <root>/<directory>
3. The Builder checkout's parent directory: <parent>/<directory>
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import json
import os
from pathlib import Path
import re

REGISTRY_FILE = "spokes.json"
LOCAL_OVERRIDES_FILE = "spokes.local.json"
SPOKES_ROOT_ENV = "BUILDER_SPOKES_ROOT"
SLUG_RE = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*")
REQUIRED_FIELDS = ("slug", "name", "repository", "defaultBranch", "description")
PROJECT_REQUIRED_FIELDS = ("slug", "name", "status", "description")
# The hub is a project but not a registry entry: it is the repository holding the registry.
HUB_PROJECT_SLUG = "builder"
REMOTE_REPOSITORY_RE = re.compile(r"(?:https|ssh)://[^\s/]+/\S+|[^@\s/\\]+@[^:\s/\\]+:[^\s\\]+")


@dataclass(frozen=True)
class Spoke:
    slug: str
    name: str
    repository: str
    default_branch: str
    description: str
    directory: str


class ProjectStatus(Enum):
    """Active projects accept new records; retired projects keep their history read-only."""
    ACTIVE = "active"
    RETIRED = "retired"


@dataclass(frozen=True)
class StandaloneProject:
    """Work Builder records that has no repository of its own."""
    slug: str
    name: str
    status: ProjectStatus
    description: str


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
    _require_project_slug(slug, f"spokes[{index}]")
    directory = entry.get("directory") or repository_directory_name(entry["repository"])
    if not isinstance(directory, str) or Path(directory).name != directory or directory in {".", ".."}:
        raise ValueError(f"{REGISTRY_FILE}: spokes[{index}] directory must be a single folder name")
    return Spoke(slug, entry["name"], entry["repository"], entry["defaultBranch"], entry["description"], directory)


def _require_project_slug(slug: str, entry_label: str) -> None:
    if not SLUG_RE.fullmatch(slug) or slug == "index":
        raise ValueError(f"{REGISTRY_FILE}: {entry_label} slug {slug!r} must be a lowercase hyphenated project slug")
    if slug == HUB_PROJECT_SLUG:
        raise ValueError(f"{REGISTRY_FILE}: {entry_label} slug {slug!r} is reserved for the Builder hub")


def _standalone_project_from_entry(entry: object, index: int) -> StandaloneProject:
    entry_label = f"projects[{index}]"
    if not isinstance(entry, dict):
        raise ValueError(f"{REGISTRY_FILE}: {entry_label} must be an object")
    missing = [field for field in PROJECT_REQUIRED_FIELDS
               if not isinstance(entry.get(field), str) or not entry[field].strip()]
    if missing:
        raise ValueError(f"{REGISTRY_FILE}: {entry_label} missing nonblank {', '.join(missing)}")
    _require_project_slug(entry["slug"], entry_label)
    try:
        status = ProjectStatus(entry["status"])
    except ValueError as cause:
        allowed = ", ".join(known_status.value for known_status in ProjectStatus)
        raise ValueError(f"{REGISTRY_FILE}: {entry_label} status {entry['status']!r} must be one of {allowed}") from cause
    return StandaloneProject(entry["slug"], entry["name"], status, entry["description"])


def _read_registry_document(registry_path: Path) -> dict:
    try:
        document = json.loads(registry_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"Spoke registry not found: {registry_path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"{registry_path}: invalid JSON: {error}") from error
    if not isinstance(document, dict) or not isinstance(document.get("spokes"), list):
        raise ValueError(f"{registry_path}: expected an object with a 'spokes' list")
    if not isinstance(document.get("projects", []), list):
        raise ValueError(f"{registry_path}: 'projects' must be a list when present")
    return document


def load_spokes(builder_root: Path) -> list[Spoke]:
    registry_path = builder_root / REGISTRY_FILE
    entries = _read_registry_document(registry_path)["spokes"]
    spokes = [_spoke_from_entry(entry, index) for index, entry in enumerate(entries)]
    slugs = [spoke.slug for spoke in spokes]
    duplicates = sorted({slug for slug in slugs if slugs.count(slug) > 1})
    if duplicates:
        raise ValueError(f"{registry_path}: duplicate spoke slugs {duplicates}")
    return spokes


def load_standalone_projects(builder_root: Path) -> list[StandaloneProject]:
    entries = _read_registry_document(builder_root / REGISTRY_FILE).get("projects", [])
    return [_standalone_project_from_entry(entry, index) for index, entry in enumerate(entries)]


def project_statuses_of(builder_root: Path) -> dict[str, ProjectStatus]:
    """Every valid project slug with its status: the hub, each spoke and each standalone project."""
    registry_path = builder_root / REGISTRY_FILE
    spoke_slugs = [spoke.slug for spoke in load_spokes(builder_root)]
    standalone_projects = load_standalone_projects(builder_root)
    statuses = {HUB_PROJECT_SLUG: ProjectStatus.ACTIVE}
    statuses.update((slug, ProjectStatus.ACTIVE) for slug in spoke_slugs)
    for project in standalone_projects:
        if project.slug in statuses:
            raise ValueError(f"{registry_path}: project slug {project.slug!r} is already used by a spoke or project")
        statuses[project.slug] = project.status
    return statuses


def require_active_project(builder_root: Path, slug: str) -> None:
    """Raise ValueError unless slug names a project that accepts new records."""
    statuses = project_statuses_of(builder_root)
    status = statuses.get(slug)
    if status is ProjectStatus.ACTIVE:
        return
    active = ", ".join(sorted(name for name, value in statuses.items() if value is ProjectStatus.ACTIVE))
    if status is ProjectStatus.RETIRED:
        raise ValueError(f"Project {slug!r} is retired and accepts no new records; active projects: {active}")
    raise ValueError(f"Unknown project {slug!r}; register it in {REGISTRY_FILE} first. Active projects: {active}")


def is_remote_repository(repository: str) -> bool:
    """True for https, ssh and scp-style remotes; False for local paths, which the registry must not hold."""
    return REMOTE_REPOSITORY_RE.fullmatch(repository) is not None


def register_spoke(builder_root: Path, *, slug: str, name: str, repository: str, default_branch: str,
                   description: str) -> Spoke:
    """Append a validated spoke to spokes.json; the file is unchanged when validation fails."""
    registry_path = builder_root / REGISTRY_FILE
    document = _read_registry_document(registry_path)
    registered_spokes = load_spokes(builder_root)
    standalone_project_slugs = {project.slug for project in load_standalone_projects(builder_root)}
    new_entry = {"slug": slug, "name": name, "repository": repository,
                 "defaultBranch": default_branch, "description": description}
    if not is_remote_repository(repository):
        raise ValueError(f"Repository {repository!r} must be an https, ssh or user@host:path remote, not a local path")
    new_spoke = _spoke_from_entry(new_entry, len(registered_spokes))
    if new_spoke.slug in standalone_project_slugs:
        raise ValueError(f"Slug {slug!r} is already registered as a standalone project")
    for registered in registered_spokes:
        if registered.slug == new_spoke.slug:
            raise ValueError(f"Spoke slug {slug!r} is already registered")
        if normalize_remote(registered.repository) == normalize_remote(new_spoke.repository):
            raise ValueError(f"Repository {repository} is already registered as {registered.slug!r}")
        if registered.directory.lower() == new_spoke.directory.lower():
            raise ValueError(f"Checkout folder {new_spoke.directory!r} is already used by {registered.slug!r}")
    document["spokes"].append(new_entry)
    registry_path.write_text(json.dumps(document, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return new_spoke


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
