---
id: ITEMS
type: items
status: canon
version: 1
tags: []
---

# Items & Artifacts

> The home for every plot-relevant object. Scenes reference items by ID (`ITM-###`) in
> `mentioned` and in `state_changes` (e.g. `"ITM-003 destroyed"`). This file is what those
> IDs resolve to (rule **R1**) and the authority on each item's current state (rules **R10/R11**,
> error **E11** — "item destroyed in S1 reappears intact in S5").
>
> Only register objects the story actually tracks: keys, weapons, artifacts, letters, a
> specific coin. Background props don't need an ID. Coined item names also go in
> `glossary.md` so spelling stays locked.

## How to use this file
1. Give each tracked object an `ITM-###` (next free number).
2. Fill the block below.
3. Every time a scene changes the object's **state, holder, or location**, add a row to that
   item's **State log** with the scene ID — `valid_until: null` means "still true now."
   This is the FACTTRACK pattern: state is true *between two scene IDs*, never "forever," so a
   legitimate change (intact → destroyed) doesn't read as a contradiction.

---

## Registered items

### ITM-001 — the Warden's coin
- **What it is:** a worn brass coin that replays the last voice that held it.
- **Origin / who made it:** struck in the undercity; carries the Warden's recorded command.
- **Significance / why it's tracked:** physical proof the Warden silenced Kai — the story's
  central piece of evidence. <!-- pairs with SP-001 in the payoff-ledger -->
- **Tells / visual signature:** hums faintly when gripped; warm to the touch. <!-- panel lock -->
- **Setups / payoffs:** SP-001 <!-- SP-### it plants or pays off -->
- **First appears:** S01-001

**State log** <!-- holder + condition + location over time -->
| Scene (valid_from) | Holder (CHR-###) | Condition | Location (LOC-###) | valid_until |
|--------------------|------------------|-----------|--------------------|-------------|
| S01-001            | CHR-001          | intact    | LOC-001            | null        |

<!-- ============================================================= -->
<!-- COPY THE BLOCK BELOW PER ITEM. Delete the example above when a real story starts. -->

### ITM-000 — <name>
- **What it is:**
- **Origin / who made it:**
- **Significance / why it's tracked:**
- **Tells / visual signature:**
- **Setups / payoffs:** <!-- SP-### -->
- **First appears:** <!-- scene S##-### -->

**State log**
| Scene (valid_from) | Holder (CHR-###) | Condition | Location (LOC-###) | valid_until |
|--------------------|------------------|-----------|--------------------|-------------|
|                    |                  |           |                    | null        |

> **Condition vocabulary** (keep it consistent so it's greppable):
> `intact` · `damaged` · `destroyed` · `lost` · `sealed` · `consumed` · `transformed`
