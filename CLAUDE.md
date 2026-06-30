# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is **primarily not a software project** — it is a **story-bible template**: a folder of plain
Markdown + JSON Schema that acts as a single source of truth an AI (or human team) reads before
writing any scene of a long-form comic/manga, so facts, characters, power rules, and timeline stay
consistent across hundreds of pages. The only code is a small Python helper layer in `tools/`
(`lint.py`, the continuity linter; `pack.py`, the per-scene context-packer; `new-story.py`, the
scaffold; `canonlib.py`, shared parsing) plus provider-agnostic agent specs in `agents/` — no build
system or app runtime.

When asked to "work in this repo," the work is almost always one of: filling in a canon file,
authoring a scene, validating continuity, or extending the template/schema/rules (occasionally the
linter) — **not** writing application code. Read `CHEATSHEET.md` first (the quality bar), then
`README.md` (the machinery). A complete worked story lives in `examples/the-wardens-coin/`.

## The one principle that governs everything

**Canon is the single source of truth. Scenes consume canon; they never invent it.**

- `/canon` = immutable facts (premise, world, power system, characters, timeline, glossary).
  Changed only deliberately, with a `version` bump.
- `/scenes` = the actual story, one file per scene. Scenes *reference* canon by ID and write
  their consequences back into canon.

A "scenario error" is almost always a scene that contradicted canon, or canon that contradicted
itself. Lock canon before drafting scenes.

## The ID scheme (the linchpin — spans every file)

Every canonical thing has a stable ID; scenes reference things by ID, never by loose name. This is
what makes the bible machine-checkable and RAG-able. The schemas enforce these exact patterns:

| Prefix | Thing | Pattern |
|--------|-------|---------|
| `CHR-###` | Character | `^CHR-[0-9]{3}$` |
| `LOC-###` | Location | `^LOC-[0-9]{3}$` |
| `FAC-###` | Faction | `^FAC-[0-9]{3}$` (defined in `canon/01-world.md`) |
| `PWR-###` | Power/ability | `^PWR-[0-9]{3}$` (defined in `canon/02-power-system.md`) |
| `ITM-###` | Item/artifact | `^ITM-[0-9]{3}$` (defined in `canon/items.md`) |
| `EVT-###` | Timeline event | `^EVT-[0-9]{3}$` (defined in `canon/timeline.md`) |
| `ARC-##` | Story arc | `^ARC-[0-9]{2}$` |
| `S{arc}-{seq}` | Scene | `^S[0-9]{2}-[0-9]{3}$` (e.g. `S01-014`) |
| `SP-###` | Setup→payoff pair | `^SP-[0-9]{3}$` |

## Frontmatter & validity intervals (the mechanism that spans files)

Every canon/scene file opens with YAML frontmatter (`id`, `type`, `status`, `version`, `tags`).
The two JSON Schemas in `schema/` define the required fields:

- `schema/scene.schema.json` — requires `id, type, status, arc, scene_type, in_world_time,
  location, present, pov, goal, conflict, outcome, value_turn, state_changes`.
- `schema/character.schema.json` — requires `id, type, status, role, first_appears, alive`.

**Validity intervals are the key trick** (the "FACTTRACK" idea): a fact is not true forever, it is
true *between two scene IDs*. A character's `status_intervals[]` and the relationship tables carry
`valid_from`/`valid_until` (where `null` = still true). This is what lets a fact legitimately
change (ally→enemy, alive→dead) without the linter flagging it as a contradiction — and it is the
single most important concept to preserve when editing canon. Example, from
`examples/the-wardens-coin/canon/characters/CHR-001_Kai.md`: Kai's bond to Sael is
`unknown hunter [valid_from: S01-001, valid_until: S01-005]`; from S01-005 it becomes `named enemy`.

## The writing loop (how scenes get authored)

1. **Lock canon** (the 6 layers: premise, world, power-system, characters, timeline, glossary).
2. **Map the arc** in `structure/arc.md` (Hero's Journey for the series spine; kishōtenketsu per chapter).
3. **Per scene:** copy `scenes/_TEMPLATE.md`, fill the frontmatter, **assemble only the relevant
   canon** (see "Context assembly" below — do NOT paste the whole bible), draft, then write the
   `state_changes` array (what the next scene inherits).
4. **Lint** — run `python tools/lint.py <story-dir>` (machine checks) plus a human pass of
   `validation/continuity-rules.md` before setting `status: locked`.
5. **Write-back rule:** the moment a scene locks, propagate its `state_changes` into canon —
   timeline events, character status logs, relationship intervals, item states, payoff-ledger rows.
   *Stale canon is the seed of tomorrow's contradiction.* This step is mandatory, not optional.

## Validation (linter v0.2 + a human pass)

`tools/lint.py` automates the machine-checkable subset: JSON-Schema validation of scene/character
frontmatter, **R1** (entity existence), **R9** (setup/payoff integrity), **R12** (scene earns its
place), and ID format/uniqueness. Run `python tools/lint.py <story-dir>`; it exits non-zero on
errors and **prints the rules it cannot judge** (R2, R5, R6, R7, R8, R11) so you still apply those
by hand. The rules in `validation/continuity-rules.md` (R1–R12) map one-to-one to the error
taxonomy in `CHEATSHEET.md §2` (E1–E12). The high-value checks:

- **R1 entity existence** — every ID in `present`/`mentioned`/`location`/`refs`/panel text must
  resolve to a registered entity in `/canon` (a file, or a registered section/row — see the
  "Defined in" column of the ID table in `README.md`).
- **R3 validity window** — a scene must not rely on a fact outside its `valid_from→valid_until`.
- **R6/R7 power legality & ledger** — every ability used must exist in `02-power-system.md`, be one
  the character has, pay its on-page cost, and not exceed the character's logged tier without a
  ledger row citing an in-story cause.
- **R9 setup/payoff** — every `refs.setups` opens an `SP-###` in `validation/payoff-ledger.md`;
  every `refs.payoffs` closes an `SP-###` opened in an *earlier* scene.
- **R10 object/status continuity** — item and character state must agree with the most recent
  `state_changes` that touched them.

Errors cluster in the **middle** of long stories — at each arc midpoint, re-run R1–R11 across the
whole arc, not just the latest scene.

## Context assembly (how an AI should consume this bible)

To generate scene N, assemble only: `premise.md` + relevant sections of `world.md` +
`power-system.md` + character sheets for everyone `present` in scene N + the previous scene's
`state_changes` + summaries of scenes in `refs` + open setups from the payoff-ledger that could pay
off here + the glossary (always). Regrounding each scene in retrieved canon — instead of trusting
the model's fading memory — is the whole point. **This is automated:** `python tools/pack.py
<scene-id> --root <story>` emits exactly this bundle, and the provider-agnostic specs in `agents/`
(usable with any AI) consume it.

## File-naming conventions

- `_TEMPLATE.md` — blank template; **copy it, never edit it in place**. `scenes/_TEMPLATE.md` is
  the most-used.
- `_VISUAL-GUIDE.md` — visual-canon rules (design-DNA strings, palette locks, style token) to keep
  AI-generated panel art on-model.
- Worked examples live under `examples/` — a complete, lint-clean story bible per folder
  (`examples/the-wardens-coin/`), kept separate from the blank template so the top-level dirs stay
  copy-ready. The template dirs themselves hold only `_TEMPLATE.md` / `_VISUAL-GUIDE.md`.

## When extending the template

Keep canon and narrative separate; keep IDs stable; never let a scene invent a fact. If you change
a schema in `schema/`, keep the ID `pattern` regexes and the `continuity-rules.md` checks in sync —
the rules, the cheatsheet error codes, and the schema constraints are three views of the same
contract and must not drift apart.
