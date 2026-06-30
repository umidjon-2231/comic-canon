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
resolves to a registered entity in `/canon`), **R9** (setup/payoff integrity), **R12** (the
scene earns its place), and ID/format/uniqueness. It prints — but cannot judge — the prose
rules (R2, R5, R6, R7, R8, R11); those still need a human. Exit code is non-zero on any error,
so it drops straight into CI.

## `new-story.py` — scaffold a fresh story

Copies the blank template (canon/scenes/structure/validation/schema) into a new directory,
leaving the examples and tooling behind, so you start from clean canon.

```bash
python tools/new-story.py ../my-comic
```
