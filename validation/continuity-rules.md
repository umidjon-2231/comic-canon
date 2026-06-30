---
id: CONTINUITY-RULES
type: validation
status: canon
version: 1
---

# Continuity Rules (the linter spec)

> The checks that catch scenario errors. Written so a human can run them now and a script
> can enforce them later (v0.2). Each maps to an error code in `CHEATSHEET.md §2`.

## How to run (manually, today)
For each scene, top to bottom, verify every rule. Any failure = fix before `status: locked`.

## Rules

**R1 · Entity existence (E1)**
Every ID in `present`, `mentioned`, `location`, `refs`, and the panel text must resolve to a
**registered entity** in `/canon` — either a file (`CHR-###` in `characters/`, `S##-###` in
`scenes/`) or a registered section/row: `LOC-###`/`FAC-###` in `01-world.md`, `PWR-###` in
`02-power-system.md`, `ITM-###` in `items.md`, `EVT-###` in `timeline.md`, `SP-###` in the
payoff-ledger. (See the "Defined in" column of the ID table in `README.md`.) No loose names for
canonical things.

**R2 · Fact match (E2)**
Any character detail stated in the scene (appearance, age, name) must match the character
sheet exactly. Names must match `glossary.md`. → grep the glossary "forbidden variants" table.

**R3 · Validity window (E3)**
For every fact the scene relies on, the scene's `id` must fall inside that fact's
`valid_from → valid_until` window. (e.g. don't treat Sael as an ally in a scene after
`valid_until: S02-010`.)

**R4 · Temporal order (E4)**
Scene `in_world_time` must be ≥ the `in_world_time` of every event it depends on in
`timeline.md`. No effect before its cause.

**R5 · Knowledge gating (E5)**
A character may only act on information their `knowledge state` says they have *by this scene*.
If they use unknown info, either it's an error or you must add the "how they learned it" beat.

**R6 · Power legality (E6)**
Every ability used must (a) exist in `02-power-system.md`, (b) be one the character actually
has, and (c) pay its defined **cost** and respect its **limit/weakness** on-page.

**R7 · Power ledger (E7)**
If a character does something above their logged tier, there must be a power-ledger row with
an in-story cause dated at/before this scene. No silent power-ups.

**R8 · Geography & logistics (E8)**
A character's `location` must be reachable from their previous location within the elapsed
`in_world_time` (check travel times in `world.md`). No being in two places at once — check
the timeline's parallel-threads table.

**R9 · Setup integrity (E9/E10)**
Every `setups` entry opens an SP-### in the payoff ledger. Every `payoffs` entry must close an
SP-### that was opened in an *earlier* scene. A climax payoff with no prior setup fails.

**R10 · Object/status continuity (E11)**
An item's state (exists / destroyed / who holds it) and a character's status (alive, injured,
possessions) must be consistent with the most recent `state_changes` that touched them.

**R11 · Voice consistency (E12)**
Dialogue must match the character's `speech_style`. Spot-check against their sample line.

**R12 · Scene earns its place (quality, not continuity)**
`goal`, `conflict`, `outcome`, and `value_turn` are all non-empty, and `outcome` is not
"nothing changed." Filler still must turn a value.

## Write-back rule (prevents future errors)
After a scene locks, propagate its `state_changes` into canon **immediately**:
timeline events, character status logs, relationship intervals, item states, ledger entries.
Stale canon is the seed of tomorrow's contradiction.

## Mid-story focus
Errors cluster in the middle of long stories. At each arc midpoint, run a full pass of
R1–R11 across the arc, not just the latest scene.
