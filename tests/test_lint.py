"""Positive + negative tests for the linter. Each negative test tampers with a
fresh copy of the worked example and asserts the matching rule fires."""
import lint


# --- positive ---------------------------------------------------------------

def test_example_is_clean(example_root, schema_dir):
    rep = lint.lint(example_root, schema_dir)
    assert rep.errors == [], rep.errors
    assert rep.warnings == [], rep.warnings


# --- negative: each injected error must be caught ---------------------------

def test_r1_unknown_entity(story, schema_dir, edit):
    edit(story / "scenes" / "S01-001.md", "present: [CHR-001]", "present: [CHR-001, CHR-099]")
    rep = lint.lint(story, schema_dir)
    assert any("R1" in e and "CHR-099" in e for e in rep.errors)


def test_r9_unearned_payoff(story, schema_dir, edit):
    edit(story / "scenes" / "S01-003.md", "payoffs: []", "payoffs: [SP-404]")
    rep = lint.lint(story, schema_dir)
    assert any("R9" in e for e in rep.errors)


def test_r12_inert_scene(story, schema_dir, edit):
    edit(story / "scenes" / "S01-005.md",
         'value_turn: "anonymous dread → named enemy"', 'value_turn: ""')
    rep = lint.lint(story, schema_dir)
    assert any("R12" in e for e in rep.errors)


def test_r3_appearance_before_first_appears(story, schema_dir, edit):
    # Sael (first_appears S01-006) shoved on-page in the opener.
    edit(story / "scenes" / "S01-001.md", "present: [CHR-001]", "present: [CHR-001, CHR-003]")
    rep = lint.lint(story, schema_dir)
    assert any("R3" in e and "CHR-003" in e for e in rep.errors)


def test_r3_interval_disorder(story, schema_dir, edit):
    edit(story / "canon" / "characters" / "CHR-001_Kai.md",
         "valid_from: S01-005\n    valid_until: null",
         "valid_from: S01-005\n    valid_until: S01-001")
    rep = lint.lint(story, schema_dir)
    assert any("R3" in e and "valid_from" in e for e in rep.errors)


def test_r3_death_gating_warns(story, schema_dir, edit):
    # Close Kai's "alive" interval at S01-003; she is still present afterwards.
    edit(story / "canon" / "characters" / "CHR-001_Kai.md",
         "valid_from: S01-001\n    valid_until: null",
         "valid_from: S01-001\n    valid_until: S01-003", count=1)
    rep = lint.lint(story, schema_dir)
    assert any("R3" in w and "alive" in w.lower() for w in rep.warnings)


def test_r4_backward_time_warns(story, schema_dir, edit):
    edit(story / "scenes" / "S01-006.md",
         'in_world_time: "003.144"', 'in_world_time: "003.100"')
    rep = lint.lint(story, schema_dir)
    assert any("R4" in w for w in rep.warnings)
