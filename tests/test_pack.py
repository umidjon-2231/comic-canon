"""Smoke tests for the context-packer."""
import pack
import pytest


def test_pack_pulls_the_right_entities(example_root):
    bundle = pack.pack(example_root, "S01-005", review=False)
    for token in ("LOC-003", "PWR-002", "CHR-001", "CHR-002", "Glossary", "Inherited state"):
        assert token in bundle, f"{token} missing from bundle"


def test_pack_opener_has_no_inherited_state(example_root):
    # S01-001 follows nothing, so there is no prior state to inherit.
    bundle = pack.pack(example_root, "S01-001", review=False)
    assert "Inherited state" not in bundle


def test_pack_review_includes_draft_and_items(example_root):
    bundle = pack.pack(example_root, "S01-006", review=True)
    assert "Current draft of S01-006" in bundle
    assert "ITM-001" in bundle  # mentioned item gets its state slice


def test_pack_unknown_scene_raises(example_root):
    with pytest.raises(SystemExit):
        pack.pack(example_root, "S09-999", review=False)
