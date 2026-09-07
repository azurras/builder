"""Loss-preserving source sections and link relocation for project memory."""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import re
from urllib.parse import unquote


@dataclass(frozen=True)
class Destination:
    path: Path
    anchor: str = ""


def source_anchor(path: str) -> str:
    return "source-" + re.sub(r"[^a-z0-9]+", "-", path.lower()).strip("-")


def outside_fences(text: str):
    fence = None
    for line in text.splitlines(keepends=True):
        match = re.match(r"^\s*(`{3,}|~{3,})", line)
        inside = fence is not None
        if match:
            mark = match.group(1)
            if fence is None:
                fence = mark
            elif mark[0] == fence[0] and len(mark) >= len(fence):
                fence = None
            yield line, False
        else:
            yield line, not inside


def heading_slug(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text).strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def heading_ids(text: str) -> dict[int, str]:
    counts = {}
    result = {}
    for number, (line, active) in enumerate(outside_fences(text)):
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line) if active else None
        if match:
            base = heading_slug(match.group(1))
            count = counts.get(base, 0)
            counts[base] = count + 1
            result[number] = base + (f"-{count}" if count else "")
    return result


def relocate_link(target: str, source: Path, destination: Path,
                  mapping: dict[Path, Destination], headings: dict[Path, set[str]]) -> str:
    raw = target.strip("<>")
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://|^mailto:|^data:", raw):
        return target
    path, sep, fragment = raw.partition("#")
    resolved = (source.parent / unquote(path)).resolve() if path else source.resolve()
    new = mapping.get(resolved)
    if new is None:
        if not resolved.exists():
            return target
        new = Destination(resolved)
    anchor = new.anchor
    if fragment:
        if anchor:
            if unquote(fragment) not in headings.get(resolved, set()):
                raise ValueError(f"Unknown source fragment: {source}: {target}")
            anchor += "--" + unquote(fragment)
        else:
            anchor = fragment
    relative = os.path.relpath(new.path, destination.parent).replace("\\", "/")
    if new.path.resolve() == destination.resolve() and anchor:
        relative = ""
    value = relative + ("#" + anchor if anchor else "")
    return "<" + value + ">" if target.startswith("<") else value


def transform(text: str, source: Path, destination: Destination,
              mapping: dict[Path, Destination], headings: dict[Path, set[str]]) -> str:
    ids = heading_ids(text)
    result = []
    for number, (line, active) in enumerate(outside_fences(text)):
        if not active:
            result.append(line)
            continue
        # Leave inline code and its historical paths intact.
        parts = re.split(r"(`+[^`]*`+)", line)
        for i in range(0, len(parts), 2):
            parts[i] = re.sub(
                r"(!?\[[^\]\n]*\]\()(<[^>]+>|[^\s)]+)([^)]*\))",
                lambda m: m.group(1) + relocate_link(m.group(2), source, destination.path, mapping, headings) + m.group(3),
                parts[i],
            )
        line = "".join(parts)
        reference = re.match(r"^(\s*\[[^\]]+\]:\s*)(<[^>]+>|\S+)(.*)$", line)
        if reference:
            line = reference.group(1) + relocate_link(reference.group(2), source, destination.path, mapping, headings) + reference.group(3) + ("\n" if line.endswith("\n") else "")
        if destination.anchor and number in ids:
            result.append(f'<a id="{destination.anchor}--{ids[number]}"></a>\n')
            line = re.sub(r"^#{1,6}(?=\s)", lambda m: "#" * min(len(m.group()) + 2, 6), line)
        result.append(line)
    return "".join(result)


def source_section(path: str, body: str, transformed: str, commit: str) -> str:
    anchor = source_anchor(path)
    date = re.search(r"\d{4}-\d{2}-\d{2}", path)
    heading = next((line[2:] for line in body.splitlines() if line.startswith("# ")), Path(path).stem)
    stamp = date.group() if date else "Undated archive"
    digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return (f'<a id="{anchor}"></a>\n## {stamp} | {Path(path).parent.name} | {heading}\n\n'
            f'Original source: `{path}` at `{commit}`. SHA-256 (normalized text): `{digest}`.\n\n'
            f'<!-- migrated-source: {path} -->\n{transformed}'
            f'\n<!-- /migrated-source: {path} -->\n')
