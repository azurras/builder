"""Shared dated Markdown artifact helpers for Builder skills."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import re

from builder_hub import slugify, write_text


def parse_optional_date(value: str | None) -> dt.date:
    if value:
        return dt.date.fromisoformat(value)
    return dt.datetime.now().astimezone().date()


def project_prefixed_title(project: str, title: str) -> str:
    """Title whose filename slug starts with the project, without doubling a prefix the title already has."""
    title_slug = slugify(title.strip(), "")
    if title_slug == project or title_slug.startswith(f"{project}-"):
        return title
    return f"{project} {title}"


def resolve_artifact_dir(root: Path, directory: str | Path) -> Path:
    artifact_dir = Path(directory).expanduser()
    if not artifact_dir.is_absolute():
        artifact_dir = root / artifact_dir
    return artifact_dir


def dated_markdown_file(
    *,
    root: Path,
    directory: str | Path,
    title: str,
    fallback_slug: str,
    artifact_date: dt.date | None = None,
    preserve_truncated_hyphen: bool = False,
) -> Path:
    """Return the dated Markdown path save_dated_markdown would write for title."""
    artifact_dir = resolve_artifact_dir(root.expanduser().resolve(), directory)
    date = artifact_date or dt.datetime.now().astimezone().date()
    clean_title = title.strip()
    filename_slug = slugify(clean_title, fallback_slug)
    if preserve_truncated_hyphen:
        # Five legacy record CLIs truncated after trimming; retain their filenames.
        ascii_title = clean_title.lower().encode("ascii", "ignore").decode("ascii")
        filename_slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")[:80] or fallback_slug
    return artifact_dir / f"{date.isoformat()}-{filename_slug}.md"


def save_dated_markdown(
    *,
    root: Path,
    directory: str | Path,
    title: str,
    body: str,
    fallback_slug: str,
    artifact_date: dt.date | None = None,
    overwrite: bool = False,
    preserve_truncated_hyphen: bool = False,
) -> Path:
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("title must not be blank")

    clean_body = body.strip()
    if not clean_body:
        raise ValueError("body is required")

    artifact_file = dated_markdown_file(
        root=root,
        directory=directory,
        title=clean_title,
        fallback_slug=fallback_slug,
        artifact_date=artifact_date,
        preserve_truncated_hyphen=preserve_truncated_hyphen,
    )
    artifact_file.parent.mkdir(parents=True, exist_ok=True)

    if artifact_file.exists() and not overwrite:
        raise FileExistsError(f"{artifact_file} already exists; pass --overwrite to replace it")

    return write_text(artifact_file, clean_body)
