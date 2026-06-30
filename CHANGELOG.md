# Changelog

All notable changes to this template are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Continuity linter** (`tools/lint.py`, v0.2): validates scene/character frontmatter against the
  JSON Schemas and enforces the machine-checkable rules — `R1` (entity existence), `R9`
  (setup/payoff integrity), `R12` (scene earns its place) — plus ID format/uniqueness. Exits
  non-zero on errors (CI-ready) and prints the prose rules a human still has to check.
- **Story scaffold** (`tools/new-story.py`): copy the blank template into a fresh directory.
- **`canon/items.md`**: a home for `ITM-###` items with per-item state logs (FACTTRACK intervals),
  so item state continuity (R10/R11) is trackable. Closes the one entity class that had no home.
- **Worked example** (`examples/the-wardens-coin/`): a complete, lint-clean six-scene story bible
  demonstrating the whole loop. Inline `*_example.md` files were consolidated here so the
  top-level template dirs stay copy-ready.
- **`QUICKSTART.md`** and a **CI workflow** (`.github/workflows/lint.yml`) that lints the example.
- **Community files**: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue/PR templates, `.gitignore`.

### Changed

- Rule `R1` now resolves IDs to a *registered entity* (file **or** registered section/row), with a
  "Defined in" column added to the README ID table — making R1 mechanically enforceable.

## [0.1.0] - 2026-07-01

Initial release of the story-bible template.

### Added

- **Structured canon** (`/canon`) as the single source of truth: premise, world, power system,
  characters, timeline, glossary — each with stable, ID-addressable entities.
- **Narrative layer** (`/scenes`): one file per scene, referencing canon by ID and writing its
  consequences back as state changes.
- **Stable ID scheme** spanning every file (`CHR-`, `LOC-`, `FAC-`, `PWR-`, `ITM-`, `EVT-`,
  `ARC-`, `S{arc}-{seq}`, `SP-`), making the bible searchable, RAG-able, and machine-checkable.
- **Validity intervals** (the FACTTRACK idea): facts are true *between two scene IDs*, so
  legitimate change (ally→enemy, alive→dead) isn't flagged as a contradiction.
- **JSON Schemas** for the two file types that carry frontmatter: `schema/scene.schema.json` and
  `schema/character.schema.json`.
- **Continuity rules** `R1`–`R12` (`validation/continuity-rules.md`), mapped one-to-one to the
  scenario-error taxonomy `E1`–`E12` in `CHEATSHEET.md §2`.
- **Setup→payoff ledger** (`validation/payoff-ledger.md`) for Chekhov's-gun tracking.
- **Templates and worked examples** for characters and scenes, plus a visual-canon guide.
- **Dual license**: MIT for code/schemas, CC BY 4.0 for the templates and documentation.

[Unreleased]: https://github.com/umidjon-2231/comic-canon/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/umidjon-2231/comic-canon/releases/tag/v0.1.0
