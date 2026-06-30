# Comic Canon — The Cheatsheet

> The single-page bar for **high-quality comics with zero scenario errors**.
> If you only read one file, read this. Everything else is the long form.

---

## 0. The one principle

**Canon is the single source of truth. Scenes consume canon; they never invent it.**

Split everything into two halves:

| | **CANON** (`/canon`) | **NARRATIVE** (`/scenes`) |
|---|---|---|
| What it is | Immutable facts: world, rules, power system, characters, timeline | The actual story, one file per scene |
| Who changes it | You, deliberately, with a version bump | Drafted scene-by-scene |
| The AI's job | **Reads** it as context | **Writes** within it |

A "scenario error" is almost always a scene that contradicted canon, or canon that contradicted itself. Lock canon first. Then every scene is a constrained generation problem, not a free-for-all — which is exactly when AI is reliable.

---

## 1. Lock these 6 canon layers BEFORE drafting any scene

Drafting before canon is locked is the #1 cause of mid-story collapse.

1. **Premise** — logline, theme, moral, the hero's want vs. need, the promise to the reader. (`canon/00-premise.md`)
2. **World** — setting, tone, rules of reality, factions, key locations. (`canon/01-world.md`)
3. **Power system** — the strength system, built to Sanderson's Laws (see §3). (`canon/02-power-system.md`)
4. **Characters** — full sheet + visual canon for every recurring character. (`canon/characters/`)
5. **Timeline** — canonical chronology of events, in-world dates. (`canon/timeline.md`)
6. **Glossary** — locked spelling of every proper noun + coined term. (`canon/glossary.md`)

Plus **structure** (the arc beat map, `structure/arc.md`) and the **setup→payoff ledger** (`validation/payoff-ledger.md`).

---

## 2. The Scenario-Error taxonomy (and the rule that catches each)

Research on long-form AI generation found the dominant failure modes are **factual/detail consistency** and **timeline/plot logic**, and they cluster in the **middle** of the story. Hunt these specifically:

| # | Error | Example | Lint rule that catches it |
|---|-------|---------|---------------------------|
| E1 | **Unknown entity** | A scene names a character/place not in canon | Every `present` / referenced ID must exist in `/canon` |
| E2 | **Fact contradiction** | Eye color, age, name spelling drifts | Field must match canon; spelling must match glossary |
| E3 | **Stale fact** | Treats a dead/changed fact as still true | Check the fact's `valid_from`→`valid_until` window |
| E4 | **Timeline break** | Event B happens before its cause A | Scene `in_world_time` must be ≥ all prerequisite events |
| E5 | **Knowledge leak** | Character acts on info they were never told | Check character `knows` state at that scene |
| E6 | **Power violation** | Ability used ignoring its cost/limit/weakness | Ability use must pay the cost defined in power-system |
| E7 | **Power creep** | Strength jumps with no in-story reason | New capability needs a logged training/event source |
| E8 | **Geography/logistics** | Character is in two places, or travels impossibly fast | Location state + travel time vs. timeline |
| E9 | **Dropped setup** | A gun is shown, never fired | Every `setup` in the ledger needs a `payoff` |
| E10 | **Unearned payoff** | Climax solved by a power/item never set up | Every `payoff` needs a prior `setup` |
| E11 | **Object/status drift** | Item destroyed in S1 reappears intact in S5 | Item state tracked across scenes |
| E12 | **Tone/voice break** | A character suddenly talks unlike themselves | Voice matches character `speech_style` |

> **Validity intervals are the trick.** A fact is not "true forever" — it is true between two scene IDs. `Sael is an ally [valid_from: S01-004, valid_until: S02-010]`. After S02-010 he's an enemy. This lets facts legitimately change without the linter screaming, and stops E3 cold.

---

## 3. Power-system rules (Sanderson's Laws as a checklist)

Whatever your system is (chakra-like, cursed-energy-like, magic, tech), it passes if:

- [ ] **0th — Still awesome.** Rules haven't sanded off the wonder.
- [ ] **1st — Understood before it solves.** Any power that resolves a major conflict was clearly explained to the reader *before* that moment. (Soft/mysterious powers may *create* problems but must never *solve* the climax.)
- [ ] **2nd — Costs > limits > weaknesses > powers.** Every ability has: a **cost** (what you pay to use it), a **limit** (what it physically can't do), and a **weakness** (what defeats it). These are richer than the power itself.
- [ ] **3rd — Depth over breadth.** New plot problems are solved by combining *existing* rules in clever ways, not by introducing a brand-new power.
- [ ] **Power ledger.** Each character's current tier/capability is logged, and every increase points to an in-story cause (training arc, item, event).

If a fight or climax can be won by "remembering" a power we never saw, it fails the 1st Law — that's error E10.

---

## 4. The scene quality bar

A scene **earns its place** only if it passes all of these. Filler that fails should be cut or merged.

- [ ] **POV + goal** — whose scene is it, what do they want *in this scene*?
- [ ] **Conflict** — what opposes the goal?
- [ ] **Outcome** — they get it, fail, or get it at a cost. (No "nothing changed.")
- [ ] **Value turn** — the scene flips a charge: safe→threatened, hope→despair, stranger→ally. If the emotional charge is the same at the end as the start, the scene is inert.
- [ ] **Advances plot OR character** (the best do both).
- [ ] **Canon-clean** — every entity referenced exists and is used per its current valid state.
- [ ] **State delta logged** — what changed (injuries, knowledge, location, relationships, item status) is written to the scene's `state_changes` so the next scene inherits it.

Scene types: `main` (plot spine), `character` (relationship/interiority), `setup` (plants a seed), `payoff` (cashes one), `filler` (breather — allowed, but must still pass the value-turn test or it's cut).

---

## 5. Visual consistency (the image side)

Panel art drifts even faster than prose. Lock these per character in the visual guide:

- [ ] **Identity anchor** — 1 canonical reference image + a one-line "design DNA" string reused in every prompt.
- [ ] **Turnaround + expression sheet** — front/side/back + 4–6 core expressions, so panels stay on-model.
- [ ] **Wardrobe/palette lock** — exact colors (hex) and outfits per arc; note when/why an outfit changes.
- [ ] **Style token** — one fixed style phrase appended to *every* panel prompt (linework, shading, era).
- [ ] **Scale/age lock** — relative heights and ages, so the cast doesn't resize between panels.
- [ ] **Location reference** — a reference image + description for every recurring set.

---

## 6. The pre-flight checklists

**Before drafting (per project):** premise locked · world rules listed · power system passes §3 · every recurring character has a sheet + visual canon · timeline seeded · glossary started · arc beats mapped.

**Per scene:** passes §4 bar · all referenced IDs valid · spelling = glossary · powers pay their cost · timeline order holds · state delta written · any new setup/payoff logged.

**Per arc:** every setup planted this arc has a scheduled payoff · power ledger reviewed for creep · timeline has no gaps/overlaps · theme/moral still being served · relationship graph updated.

---

## 7. How the AI should consume this (context assembly)

Don't paste the whole bible. To generate **scene N**, assemble only:

```
premise.md  +  world.md (relevant sections)  +  power-system.md
+ character sheets for everyone `present` in scene N
+ the previous scene's state_changes
+ any scenes N references (refs:) — summaries, not full text
+ open setups from the payoff-ledger that could pay off here
+ glossary (always)
```

This mirrors the retrieval-augmented approach that pushed state consistency toward 98% in the research: **structured canon + episode summaries + key-item tracking**, retrieved per scene, instead of one giant context blob. It also fights mid-story drift (where errors cluster) because each scene is regrounded in canon rather than relying on the model's fading memory.

---

*v0.1 — living document. Tighten it every story.*
