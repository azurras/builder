"""Shared dated Markdown artifact helpers for Builder skills."""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from builder_hub import slugify, write_text


def parse_optional_date(value: str | None) -> dt.date:
    if value:
        return dt.date.fromisoformat(value)
    return dt.datetime.now().astimezone().date()


def resolve_artifact_dir(root: Path, directory: str | Path) -> Path:
    artifact_dir = Path(directory).expanduser()
    if not artifact_dir.is_absolute():
        artifact_dir = root / artifact_dir
    return artifact_dir


def save_dated_markdown(
    *,
    root: Path,
    directory: str | Path,
    title: str,
    body: str,
    fallback_slug: str,
    artifact_date: dt.date | None = None,
    overwrite: bool = False,
) -> Path:
    clean_title = title.strip()
    if not clean_title:
        raise ValueError("title must not be blank")

    clean_body = body.strip()
    if not clean_body:
        raise ValueError("body is required")

    artifact_dir = resolve_artifact_dir(root.expanduser().resolve(), directory)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    date = artifact_date or dt.datetime.now().astimezone().date()
    artifact_file = artifact_dir / f"{date.isoformat()}-{slugify(clean_title, fallback_slug)}.md"

    if artifact_file.exists() and not overwrite:
        raise FileExistsError(f"{artifact_file} already exists; pass --overwrite to replace it")

    return write_text(artifact_file, clean_body)
