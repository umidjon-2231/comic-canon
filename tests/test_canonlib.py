"""Unit tests for the shared parsing library."""
import canonlib as cl


def test_parse_frontmatter(example_root):
    fm = cl.parse_frontmatter(example_root / "scenes" / "S01-001.md")
    assert fm["id"] == "S01-001"
    assert fm["pov"] == "CHR-001"
    assert fm["present"] == ["CHR-001"]


def test_body_strips_frontmatter(example_root):
    b = cl.body(example_root / "scenes" / "S01-001.md")
    assert not b.lstrip().startswith("---")
    assert "What Walls Remember" in b


def test_slice_id_section_stops_at_next_header(example_root):
    text = cl.read_text(example_root / "canon" / "01-world.md")
    sec = cl.slice_id_section(text, "LOC-003")
    assert sec.startswith("### LOC-003")
    assert "Sealed Archive" in sec
    assert "LOC-004" not in sec  # must stop before the next section


def test_slice_title_section(example_root):
    text = cl.read_text(example_root / "canon" / "02-power-system.md")
    sec = cl.slice_title_section(text, r"Global laws")
    assert sec is not None and "Global laws" in sec


def test_indexes(example_root):
    scenes = cl.scene_index(example_root)
    chars = cl.character_index(example_root)
    assert {f"S01-00{i}" for i in range(1, 7)} <= set(scenes)
    assert {"CHR-001", "CHR-002", "CHR-003"} <= set(chars)
