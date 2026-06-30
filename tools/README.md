# tools/

Automation for the template. Plain Python, no framework.

## `lint.py` — the continuity linter (v0.2)

Enforces the machine-checkable subset of `validation/continuity-rules.md`.

```bash
pip install -r tools/requirements.txt
python tools/lint.py examples/the-wardens-coin   # lint a story
python tools/lint.py                             # lint the current directory
```

It checks: schema validity of scene/character frontmatter, **R1** (every referenced ID
resolves to a registered entity in `/canon`), **R3** (interval integrity + a character isn't
on-page before `first_appears` or after they die), **R4** (`in_world_time` doesn't move backward
along `follows`), **R9** (setup/payoff integrity), **R12** (the scene earns its place), and
ID/format/uniqueness. It prints — but cannot judge — the prose rules (R2, R5, R6, R7, R8, R11);
those still need a human. Exit code is non-zero on any error, so it drops straight into CI.

Tests live in `tests/` — run `pip install -r tools/requirements-dev.txt && pytest -q`.

## `pack.py` — the context-packer (v0.3)

Assembles the **minimal** canon for one scene into a single bundle you feed to any AI — the
"context assembly" step from `CHEATSHEET.md §7`, as a deterministic tool. No model, no network.

```bash
python tools/pack.py S01-005 --root examples/the-wardens-coin            # to stdout
python tools/pack.py S01-005 --root examples/the-wardens-coin --out b.md # to a file
python tools/pack.py S01-005 --root examples/the-wardens-coin --review   # include the draft
```

It pulls only what scene N needs: the scene's intent, premise, the relevant world/power slices,
full sheets for everyone `present`, the previous scene's `state_changes`, summaries of referenced
scenes, the open setups, and the glossary. The `agents/` specs consume this bundle.

## `canonlib.py` — shared parsing library

Frontmatter parsing and Markdown section-slicing used by both `lint.py` and `pack.py`, so there's
one source of truth. Not run directly.

## `new-story.py` — scaffold a fresh story

Copies the blank template (canon/scenes/structure/validation/schema) into a new directory,
leaving the examples and tooling behind, so you start from clean canon.

```bash
python tools/new-story.py ../my-comic
```
