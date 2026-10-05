"""Shared dated Markdown artifact helpers for Builder skills."""

from __future__ import annotations

import datetime as dt
from pathlib import Path
import re

from builder_hub import parse_dated_file, slugify, write_text


def parse_optional_date(value: str | None) -> dt.date:
    if value:
        return dt.date.fromisoformat(value)
    return dt.datetime.now().astimezone().date()


def parse_optional_time(value: str | None) -> dt.time:
    """Clock time from `HH:MM`, defaulting to the current local minute."""
    if value:
        if not re.fullmatch(r"\d{2}:\d{2}", value):
            raise ValueError(f"time must use HH:MM format: {value!r}")
        return dt.time.fromisoformat(value)
    return dt.datetime.now().astimezone().time().replace(second=0, microsecond=0)


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
    artifact_time: dt.time | None = None,
    preserve_truncated_hyphen: bool = False,
) -> Path:
    """Return the path save_dated_markdown would write for title.

    A record already saved on that date with the same slug, timed or not, keeps its path so it can be
    replaced; otherwise the name is date-HH-MM-slug.md. More than one such record raises ValueError.
    """
    artifact_dir = resolve_artifact_dir(root.expanduser().resolve(), directory)
    date = artifact_date or dt.datetime.now().astimezone().date()
    clock_time = artifact_time or parse_optional_time(None)
    clean_title = title.strip()
    filename_slug = slugify(clean_title, fallback_slug)
    if preserve_truncated_hyphen:
        # Five legacy record CLIs truncated after trimming; retain their filenames.
        ascii_title = clean_title.lower().encode("ascii", "ignore").decode("ascii")
        filename_slug = re.sub(r"[^a-z0-9]+", "-", ascii_title).strip("-")[:80] or fallback_slug
    same_day_records = same_day_records_named(artifact_dir, date, filename_slug)
    if len(same_day_records) > 1:
        names = ", ".join(record.name for record in same_day_records)
        raise ValueError(f"several records on {date.isoformat()} are named {filename_slug!r}: {names}")
    if same_day_records:
        return same_day_records[0]
    return artifact_dir / f"{date.isoformat()}-{clock_time.strftime('%H-%M')}-{filename_slug}.md"


def same_day_records_named(artifact_dir: Path, date: dt.date, filename_slug: str) -> list[Path]:
    """Existing records for date whose slug is filename_slug, with or without a time in the name."""
    if not artifact_dir.is_dir():
        return []
    return sorted(
        path for path in artifact_dir.glob(f"{date.isoformat()}-*.md")
        if (dated_file := parse_dated_file(path)) is not None and dated_file.slug == filename_slug)


def save_dated_markdown(
    *,
    root: Path,
    directory: str | Path,
    title: str,
    body: str,
    fallback_slug: str,
    artifact_date: dt.date | None = None,
    artifact_time: dt.time | None = None,
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
        artifact_time=artifact_time,
        preserve_truncated_hyphen=preserve_truncated_hyphen,
    )
    artifact_file.parent.mkdir(parents=True, exist_ok=True)

    if artifact_file.exists() and not overwrite:
        raise FileExistsError(f"{artifact_file} already exists; pass --overwrite to replace it")

    return write_text(artifact_file, clean_body)
