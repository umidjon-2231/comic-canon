"""Shared fixtures. Puts tools/ on the path so tests import lint/pack/canonlib directly."""
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "tools"))


@pytest.fixture
def repo_root() -> Path:
    return REPO


@pytest.fixture
def example_root() -> Path:
    return REPO / "examples" / "the-wardens-coin"


@pytest.fixture
def schema_dir() -> Path:
    return REPO / "schema"


@pytest.fixture
def story(tmp_path: Path, example_root: Path) -> Path:
    """A mutable copy of the worked example, so negative tests can tamper safely."""
    dst = tmp_path / "story"
    shutil.copytree(example_root, dst)
    return dst


@pytest.fixture
def edit():
    """Returns a helper that replaces a string in a file (for negative fixtures)."""
    def _edit(path: Path, old: str, new: str, count: int = -1) -> None:
        text = path.read_text(encoding="utf-8")
        assert old in text, f"fixture string not found in {path.name}: {old!r}"
        path.write_text(text.replace(old, new, count), encoding="utf-8")
    return _edit
