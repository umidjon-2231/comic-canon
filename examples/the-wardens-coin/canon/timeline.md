---
id: TIMELINE
type: timeline
status: canon
version: 1
tags: [example]
---

# Timeline

## Calendar convention
- Format: `Year.Day` — e.g. `003.142` is Year 3, Day 142. Sorts cleanly as a decimal string.
- Day 0 / Year 0 anchor: the founding of the Wardenate (Year 0).

## Backstory events (before the story opens)
| ID | When | Event | Who | Referenced by |
|----|------|-------|-----|---------------|
| EVT-001 | 000.300 | The Sealing — the Warden floods & seals the three lowest tiers | CHR-003 | SP-001, SP-002 |
| EVT-002 | 000.300 | Kai loses hearing in her left ear the night of the Sealing | CHR-001 | CHR-001 backstory |

## Story events (during the narrative)
| ID | In-world time | Event | Scene | Caused by (prior EVT) |
|----|---------------|-------|-------|------------------------|
| EVT-101 | 003.142 | The coin (ITM-001) leaves the market; the plot begins | S01-001 | EVT-001 |
| EVT-102 | 003.144 | The Sealed Archive (LOC-003) is commanded open | S01-005 | EVT-101 |
| EVT-103 | 003.144 | Kai broadcasts the Warden's recorded order to the tier | S01-006 | EVT-102 |

## Causal chain check
- EVT-001 must come before EVT-101 — the coin can't carry the Sealing order before the Sealing.
- EVT-102 must come before EVT-103 — she can't broadcast the archive's proof before opening it.

## Parallel threads (who's where, when)
| In-world time | Thread A (CHR-001 Kai) | Thread B (CHR-003 Sael) |
|---------------|------------------------|-------------------------|
| 003.142 | steals the coin, market (LOC-002) | in the Spire (LOC-001), unaware |
| 003.143 | undercity & Vela (LOC-004) | listeners pick up the coin's hum |
| 003.144 | archive → broadcast (LOC-003) | descends with enforcers |
