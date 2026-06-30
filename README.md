# Comic Canon

An open, AI-friendly template for writing **long-form comics / manga with no scenario errors.**

It is a *structured story bible*: a single source of truth that an AI (or a human team) reads
before writing any scene, so characters, world rules, power systems and timelines stay
consistent from page 1 to page 1000.

> **Start with [`CHEATSHEET.md`](./CHEATSHEET.md).** This README explains the machinery.
> In a hurry? **[`QUICKSTART.md`](./QUICKSTART.md)** takes you from zero to a linted scene in 5 minutes.

---

## Why this exists

LLMs can write thousands of words but routinely contradict their own facts, characters and
rules — and the errors cluster in the **middle** of long stories. The fix that works in
practice is: **lock the canon as structured, retrievable data, track state with validity
intervals, and reground every scene in canon instead of trusting the model's memory.**

This template encodes that as a folder of plain Markdown + JSON Schema, so it works in any
editor, any git repo, any RAG pipeline, and any AI tool.

---

## Architecture: Canon vs. Narrative

```
comic-canon/
├── CHEATSHEET.md              ← the quality bar + scenario-error rules (read first)
├── QUICKSTART.md              ← zero to your first linted scene in 5 minutes
├── README.md                  ← you are here
│
├── canon/                     ← IMMUTABLE TRUTH. Scenes read this; they never invent it.
│   ├── 00-premise.md          ← logline, theme, moral, hero want vs need, reader promise
│   ├── 01-world.md            ← setting, tone, rules of reality, factions, locations
│   ├── 02-power-system.md     ← the strength system (built to Sanderson's Laws)
│   ├── timeline.md            ← canonical chronology, in-world dates  (EVT-###)
│   ├── items.md               ← plot-relevant objects + their state over time  (ITM-###)
│   ├── glossary.md            ← locked spelling of every proper noun / coined term
│   └── characters/
│       ├── _TEMPLATE.md       ← blank character sheet (copy per character)  CHR-###
│       └── _VISUAL-GUIDE.md   ← how to build a character's visual reference + prompt DNA
│
├── structure/
│   └── arc.md                 ← beat map: Hero's Journey + kishōtenketsu  (ARC-##, beats)
│
├── scenes/                    ← THE STORY. One file per scene.  S{arc}-{seq}
│   └── _TEMPLATE.md           ← blank scene file (the most important template)
│
├── validation/
│   ├── continuity-rules.md    ← the lint rules (human + machine readable)
│   └── payoff-ledger.md       ← setup → payoff tracking (Chekhov's gun)
│
├── schema/
│   ├── scene.schema.json      ← validate scene frontmatter
│   └── character.schema.json  ← validate character frontmatter
│
├── tools/                     ← automation (plain Python, no framework)
│   ├── canonlib.py            ← shared canon-parsing library
│   ├── lint.py                ← the continuity linter (v0.2): schema + R1/R9/R12
│   ├── pack.py                ← context-packer (v0.3): per-scene canon bundle for any AI
│   └── new-story.py           ← scaffold a fresh story from the blank template
│
├── agents/                    ← provider-agnostic agent specs (use with ANY AI)
│   ├── README.md              ← the loop, automated; how the agents chain
│   ├── scene-drafter.md       ← drafts a scene from a pack.py bundle
│   ├── continuity-reviewer.md ← finds errors lint.py can't (R2/R5/R6/R7/R8/R11)
│   └── canon-keeper.md        ← writes a locked scene's state_changes back into canon
│
└── examples/
    └── the-wardens-coin/      ← a complete, lint-clean 6-scene story bible to study
```

---

## The ID scheme (the linchpin)

Every canonical thing gets a **stable ID**. Scenes reference things by ID, never by loose name.
This is what makes the story searchable, RAG-able, and machine-checkable. The **Defined in**
column is the keystone of rule R1: it's where each ID must resolve to, for a human or the
linter to confirm the thing actually exists.

| Prefix | Thing | Example | Defined in |
|--------|-------|---------|------------|
| `CHR-###` | Character | `CHR-001` | one file per character in `canon/characters/` |
| `LOC-###` | Location | `LOC-004` | a section in `canon/01-world.md` |
| `FAC-###` | Faction / organization | `FAC-002` | a section in `canon/01-world.md` |
| `PWR-###` | Power / ability | `PWR-007` | a section in `canon/02-power-system.md` |
| `ITM-###` | Item / artifact | `ITM-003` | a section in `canon/items.md` |
| `EVT-###` | Timeline event | `EVT-012` | a row in `canon/timeline.md` |
| `ARC-##`  | Story arc | `ARC-02` | `structure/arc.md` |
| `S{arc}-{seq}` | Scene | `S01-014` | one file per scene in `scenes/` |
| `SP-###`  | Setup→payoff pair | `SP-005` | a row in `validation/payoff-ledger.md` |

---

## Frontmatter conventions (every file)

Each canon/scene file opens with YAML frontmatter so it's queryable and validatable:

```yaml
id: CHR-001
type: character          # premise | world | power | character | location | scene | arc ...
status: canon            # canon | draft | deprecated
version: 3               # bump when you change a locked fact
tags: [protagonist, resonator]
```

**Facts that can change over time** carry a validity interval so the linter doesn't flag
legitimate change (the FACTTRACK idea):

```yaml
- fact: "Sael is an ally of Kai"
  valid_from: S01-004
  valid_until: S02-010    # after this scene the fact is false; he turns
```

---

## The writing loop

1. **Lock canon** (the 6 layers in the cheatsheet). Don't skip.
2. **Map the arc** in `structure/arc.md`.
3. For each scene: copy `scenes/_TEMPLATE.md`, fill frontmatter, **assemble only the relevant
   canon** (see Cheatsheet §7), generate, then **write the `state_changes` back**.
4. **Lint** — run `python tools/lint.py .` (enforces the machine-checkable rules and prints the
   ones a human still has to check) before locking the scene.
5. **Update the ledger + timeline + character state** so the next scene inherits reality.

See [`QUICKSTART.md`](./QUICKSTART.md) for the copy-paste version, and
[`examples/the-wardens-coin/`](./examples/the-wardens-coin/) for the whole loop worked end to end.

---

## Roadmap (open-source)

- v0.1 — the template (manual lint).
- v0.2 — ✅ **shipped:** a CLI linter (`tools/lint.py`) that parses frontmatter and enforces the
  machine-checkable subset of `continuity-rules.md` (schema + R1/R9/R12), with a `new-story.py`
  scaffold and a complete worked example.
- v0.3 — ✅ **shipped:** a context-packer (`tools/pack.py`) that auto-assembles per-scene canon
  from the frontmatter IDs, plus a provider-agnostic `agents/` layer (works with any AI) covering
  the full loop — `scene-drafter`, `continuity-reviewer`, `canon-keeper`.
- v0.3.1 — ✅ **shipped:** linter R3/R4 (interval integrity + appearance/death gating + temporal
  order) and a `tests/` suite (positive + a negative per rule) wired into CI.
- v0.4 — visual-canon pack: reference-image manifest + prompt-DNA injector for panel gen.
- later — the prose half of R3 (does a scene *lean on* a stale fact?) still needs a human.

PRs welcome — see [`CONTRIBUTING.md`](./CONTRIBUTING.md). Keep canon and narrative separate; keep
IDs stable; never let a scene invent a fact.

---

## License

This repository is **dual-licensed** so each part carries the license that fits it:

- **Code** — the JSON Schemas in `schema/` (and any scripts/linter added later) are under the
  **MIT License** ([`LICENSE`](./LICENSE)).
- **Content** — everything else (the Markdown templates, this README, the cheatsheet, the rules,
  and all example prose) is under **CC BY 4.0** ([`LICENSE-CONTENT.md`](./LICENSE-CONTENT.md)).

**The stories you write with it are yours.** The dual license covers *the template*, not the
canon and scenes you author on top of it — those are your own work, licensed however you choose.
