# Example — *The Warden's Coin*

A complete, **lint-clean** mini-story bible: six scenes (ARC-01) on top of a fully locked canon.
It exists so you can see the whole writing loop working end to end — not as a story to publish.

Run the linter against it from the repo root:

```bash
python tools/lint.py examples/the-wardens-coin
```

## What this example is built to demonstrate

| Mechanic | Where to look |
|----------|---------------|
| Canon locked before scenes | everything in `canon/` |
| A power system built to Sanderson's Laws (cost > limit > weakness) | `canon/02-power-system.md` |
| Scenes referencing canon by **ID**, never loose name | every scene's frontmatter |
| **Validity intervals** (a fact true only between two scene IDs) | Kai↔Sael in `characters/CHR-001_Kai.md` |
| A **setup → payoff** opened and closed inside the arc | `SP-002` (planted S01-002, paid S01-005) |
| A **deliberately open** cross-arc thread | `SP-001` (the coin's voice — pays off in ARC-02) |
| A **power-ledger** row justifying a strength increase (anti power-creep) | `canon/02-power-system.md` + `S01-005` |
| **State write-back** (each scene's `state_changes` flowing into canon) | scene frontmatter → `timeline.md`, `items.md`, character logs |
| The **3rd Law** climax (win by combining known rules, not a new power) | `S01-006` |

## The one-paragraph story

Kai, a deaf undercity thief who can hear what objects remember, steals a coin that replays the
voice of the Warden who drowned the lower tiers. Chased by it, she finds a sealed archive, an old
tuner named Vela who teaches her to command without burning out, and — behind the door — the
Warden's name. Cornered, she turns the coin's own memory into a broadcast and makes the whole
city hear the truth it was silenced to forget. The Warden escapes. The reckoning is ARC-02.

> Built with [Comic Canon](https://github.com/umidjon-2231/comic-canon).
