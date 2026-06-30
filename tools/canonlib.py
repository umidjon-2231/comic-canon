"""
canonlib — shared canon-parsing helpers for the comic-canon tooling.

Both tools/lint.py and tools/pack.py import from here so frontmatter parsing and
section slicing have a single source of truth. Pure stdlib + pyyaml; no AI, no
network — provider-agnostic by construction.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    raise SystemExit("error: pyyaml is required — run: pip install -r tools/requirements.txt")

# IDs ending in the placeholder slot are template scaffolding, not real entities.
PLACEHOLDER = re.compile(r"-000$|^S00-000$")

_HEADER = re.compile(r"^(#{1,6})\s+(.*)$")


def use_utf8_io() -> None:
    """Force UTF-8 on stdout/stderr so emoji/arrows in bundles don't crash on
    Windows consoles (cp1251/cp1252) or when piped."""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except (AttributeError, ValueError):
            pass


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def is_template(path: Path) -> bool:
    return path.name.startswith("_")


def parse_frontmatter(path: Path) -> dict | None:
    """Return the YAML frontmatter dict, or None if the file has none."""
    text = read_text(path)
    if not text.startswith("---"):
        return None
    parts = text.split("\n---", 1)
    if len(parts) < 2:
        return None
    try:
        data = yaml.safe_load(parts[0][3:])  # drop the opening '---'
    except yaml.YAMLError as exc:
        raise ValueError(f"invalid YAML frontmatter: {exc}") from exc
    return data if isinstance(data, dict) else None


def body(path: Path) -> str:
    """Return the markdown body (everything after the frontmatter block)."""
    text = read_text(path)
    if text.startswith("---"):
        parts = text.split("\n---", 1)
        if len(parts) == 2:
            return parts[1].lstrip("-").lstrip("\n").rstrip()
    return text.strip()


def slice_id_section(text: str, entity_id: str) -> str | None:
    """Return the markdown block headed `### <entity_id> ...`, up to the next
    header of the same or higher level (fewer/equal '#')."""
    lines = text.splitlines()
    pat = re.compile(rf"^(#{{1,6}})\s+{re.escape(entity_id)}\b")
    start = start_level = None
    for i, line in enumerate(lines):
        m = pat.match(line)
        if m:
            start, start_level = i, len(m.group(1))
            break
    if start is None:
        return None
    out = [lines[start]]
    for line in lines[start + 1:]:
        m = _HEADER.match(line)
        if m and len(m.group(1)) <= start_level:
            break
        out.append(line)
    return "\n".join(out).rstrip()


def slice_title_section(text: str, title_pattern: str) -> str | None:
    """Return the section whose header text matches `title_pattern` (regex),
    up to the next header of the same or higher level."""
    lines = text.splitlines()
    pat = re.compile(title_pattern, re.I)
    start = start_level = None
    for i, line in enumerate(lines):
        m = _HEADER.match(line)
        if m and pat.search(m.group(2)):
            start, start_level = i, len(m.group(1))
            break
    if start is None:
        return None
    out = [lines[start]]
    for line in lines[start + 1:]:
        m = _HEADER.match(line)
        if m and len(m.group(1)) <= start_level:
            break
        out.append(line)
    return "\n".join(out).rstrip()


def character_files(root: Path) -> list[Path]:
    cdir = root / "canon" / "characters"
    return [f for f in sorted(cdir.glob("*.md")) if not is_template(f)] if cdir.exists() else []


def scene_files(root: Path) -> list[Path]:
    sdir = root / "scenes"
    return [f for f in sorted(sdir.glob("*.md")) if not is_template(f)] if sdir.exists() else []


def scene_index(root: Path) -> dict[str, Path]:
    """Map scene id -> file path for every real scene."""
    index: dict[str, Path] = {}
    for f in scene_files(root):
        fm = parse_frontmatter(f)
        if fm and isinstance(fm.get("id"), str):
            index[fm["id"]] = f
    return index


def character_index(root: Path) -> dict[str, Path]:
    index: dict[str, Path] = {}
    for f in character_files(root):
        fm = parse_frontmatter(f)
        if fm and isinstance(fm.get("id"), str):
            index[fm["id"]] = f
    return index
