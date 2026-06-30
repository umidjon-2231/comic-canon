---
id: PAYOFF-LEDGER
type: validation
status: canon
version: 1
tags: [example]
---

# Setup → Payoff Ledger — *The Warden's Coin*

> Open an SP-### when you plant; close it when you cash it. Open rows at the end = dropped
> threads (E9); a payoff with no earlier setup = unearned (E10). The linter checks both (R9).

## Open & closed setups

| ID | Setup (what's planted) | Planted in | Type | Payoff (how it's cashed) | Paid in | Status |
|----|------------------------|-----------|------|--------------------------|---------|--------|
| SP-001 | The coin carries the Warden's recorded voice | S01-001 | mystery | Kai confronts Sael with his own order | — | 🔴 open (→ ARC-02) |
| SP-002 | A sealed archive door the coin's memory points to | S01-002 | object | The archive yields the Sealing order and the Warden's name | S01-005 | ✅ closed |
| SP-003 | Kai is now hunted by name; Vela's Wardenate past stirs | S01-006 | thread | (ARC-02) the deserter and the named thief are run down | — | 🔴 open (→ ARC-02) |

Status key: 🔴 open · 🟡 partially paid · ✅ closed · ⚪ deliberately abandoned (note why)

## Foreshadowing log (softer than setups)
| Hint / motif | First seen | Intended meaning | Payoff scene |
|--------------|-----------|------------------|--------------|
| Kai answers questions with questions | S01-001 | she deflects being known | (ARC-02) she finally answers one straight |
| Vela's torn-off crest | S01-003 | she was Wardenate | S01-006 (she's recognized) |

## End-of-arc audit (ARC-01)
- [x] No 🔴 open rows that were *promised to resolve this arc* (SP-001/SP-003 are intentionally cross-arc)
- [x] Every ✅ payoff this arc (SP-002) has a setup dated earlier (S01-002 < S01-005)
- [x] Abandoned threads (⚪): none
