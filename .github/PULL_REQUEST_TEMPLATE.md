<!-- Keep PRs small and focused: one concern per PR. -->

## What changed

<!-- A sentence or two. If it changes the model, say what scenario error it prevents. -->

## What it touches

- [ ] Canon model (`/canon`, `structure/`)
- [ ] Schema (`schema/*.json`)
- [ ] Continuity rules (`validation/`)
- [ ] Docs (`README.md`, `CHEATSHEET.md`, etc.)
- [ ] Worked example (`examples/`)
- [ ] Tooling / linter (`tools/`)

## Checklist

- [ ] **Three views stay in sync** — if I changed a `schema/*.json`, I updated the matching
      rule in `validation/continuity-rules.md` and the error code in `CHEATSHEET.md §2`.
- [ ] **IDs stayed stable** — I did not rename or renumber any existing ID.
- [ ] **Canon ≠ narrative** — no scene invents a fact; new facts are defined in canon first.
- [ ] `python tools/lint.py` passes *(if the linter exists)*.
- [ ] Any worked example I touched is still lint-clean against `validation/continuity-rules.md`.
- [ ] Commits use the imperative mood.
