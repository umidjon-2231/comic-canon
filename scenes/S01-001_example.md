---
id: S01-001
type: scene
status: locked
arc: ARC-01
sequence: 1
scene_type: main
in_world_time: "003.142"        # Year 3, day 142
location: LOC-002               # the flooded market tier
present: [CHR-001]
mentioned: [CHR-003]
refs:
  follows: null                 # opening scene
  callbacks: []
  setups: [SP-001]              # plants: objects remember; the silver coin
  payoffs: []
tags: [opening, theft, rain, undercity]
pov: CHR-001
goal: "Steal the resonant coin before the patrol sweep."
conflict: "The coin's memory screams a warning she can't ignore."
outcome: "Gets the coin, but it marks her — a cost she doesn't yet understand."
value_turn: "safety → exposure"
state_changes:
  - "CHR-001 now carries ITM-001 (the silver coin)"
  - "EVT-101 logged: the coin leaves the market — sets the plot in motion"
---

# S01-001 — What Walls Remember

> EXAMPLE FILE — shows a filled, lint-clean scene. Delete when you start your own story.

## Beat
Kai picks a resonant coin from a drowned market stall. The moment she touches it, it floods
her with a memory that isn't hers — a man's voice ordering the undercity sealed. She takes it
anyway, not knowing the coin will lead the Warden straight to her.

## Panel breakdown

**Panel 1** — wide establishing, rain
- Visual: vertical flooded market, neon bleeding into black water; Kai a small hooded figure on a gangway. *(LOC-002 reference)*
- Caption: "Walls talk. People just lie louder."
- SFX: RAIN — *hssss*

**Panel 2** — close on her gloved hand above a silver coin
- Visual: the coin glows faint as her fingers near it.
- SFX: a low *hummmm*

**Panel 3** — extreme close, her grey eye going wide
- Visual: reflected in her eye, a memory-flash of a man's silhouette. *(SP-001 plant)*
- Dialogue (the coin's memory, jagged bubble): "Seal the lower tiers. Let them drown quiet."

**Panel 4** — she pockets the coin, jaw tight
- Dialogue (Kai): "...Whose voice are you?"

## Continuity notes
- Powers used: PWR-001 (read) — cost: a flash of vertigo, paid (shown panel 3). ✔ within limits.
- Canon updates written back: timeline EVT-101 added; CHR-001 status_log + ITM-001 created;
  payoff-ledger SP-001 opened (the Warden's voice → must pay off when she meets Sael).
