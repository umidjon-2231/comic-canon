# Contributing

Thanks for helping make this a better tool for writing long-form stories with zero scenario
errors. This repo is a **template**, not an app — most contributions improve the canon model,
the schemas, the rules, the docs, or add worked examples.

By participating you agree to our [Code of Conduct](./CODE_OF_CONDUCT.md).

## The one principle (don't break it)

**Canon is the single source of truth. Scenes consume canon; they never invent it.**

- Keep canon (`/canon`) and narrative (`/scenes`) separate.
- Keep IDs stable. An ID is a contract — renaming or renumbering one breaks every reference to it.
- Never let a scene invent a fact. If a scene needs a thing, that thing gets defined in canon first.

If your change pressures any of these, it's probably the wrong change.

## The contract that must stay in sync (read this before touching `schema/`)

The ID-pattern regexes, the continuity rules, and the error taxonomy are **three views of the
same contract**. Change one, change all three in the same PR:

| View | Where |
|------|-------|
| Schema — the ID-pattern regexes and required fields | `schema/*.json` |
| Rules — the `R#` checks a reviewer/linter runs | `validation/continuity-rules.md` |
| Errors — the `E#` failure each rule catches | `CHEATSHEET.md §2` |

A PR that adds a regex to a schema but leaves the matching rule and error code untouched will be
asked to fix the drift before merge.

## Validate before you open a PR

1. Install deps once: `pip install -r tools/requirements.txt`.
2. Run the linter on any story you touched — at minimum the worked example:
   `python tools/lint.py examples/the-wardens-coin`. It must exit clean (0 errors).
3. Do a manual pass against `validation/continuity-rules.md` (R1–R12) for the rules the linter
   prints as human-only (R2, R5, R6, R7, R8, R11).

## What a good PR looks like

- **Small and focused** — one concern per PR. A schema tweak and a new example are two PRs.
- Useful kinds of contribution:
  - Template or schema improvements (clearer fields, tighter constraints).
  - New **worked examples** that demonstrate the model end-to-end. Examples live in `examples/`;
    template files live at the top level (e.g. `scenes/_TEMPLATE.md`).
  - Documentation fixes and clarifications.
  - New or sharper **linter rules** (with the matching rule + error-code updates — see above).
- Explain the *why*, not just the *what*. If it changes the model, say what error it prevents.

## Commit & PR style

- Write commit messages in the **imperative mood**: "Add item state log", not "Added" / "Adds".
- Keep the subject line short; put the reasoning in the body.
- Fill out the pull-request template — especially the three-views-in-sync confirmation.

Questions or proposals that aren't ready for a PR? Open an issue at
`https://github.com/umidjon-2231/comic-canon/issues`.
