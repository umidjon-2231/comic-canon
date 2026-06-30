# Character Visual Guide — *The Warden's Coin*

> Filled example of visual canon. Design-DNA strings are pasted verbatim into every panel prompt
> for that character; the global style token is appended to every prompt, always.

---

## Per-character visual entry

### CHR-001 — Kai

**Design DNA (paste verbatim):**
> `Kai, 17yo girl, lean, short choppy black hair with one silver streak, sharp grey eyes,
> thin scar behind left ear, charcoal hooded coat, fingerless gloves, wary expression`
> *(from S01-005, add: a second white streak in the hair)*

**Reference set:**
- [x] Canonical headshot (identity anchor)
- [x] Turnaround: front / 3/4 / side / back
- [x] Expression sheet: neutral, angry, afraid, determined, hurt, wry
- File paths: `refs/CHR-001/` *(placeholder — generate once, reuse as image refs)*

**Palette lock (hex):**
| Element | Hex | Notes |
|---------|-----|-------|
| Hair | #14151A | black; streaks #C8CDD6 (silver) / #FFFFFF (white, from S01-005) |
| Eyes | #8A93A0 | cold grey |
| Skin | #E9DCCB | pale |
| Primary outfit | #2B2F36 | charcoal coat |
| Accent | #6FB7C4 | resonance glow (cyan) |

**Wardrobe by arc:**
| Arc | Outfit | Reason it changed |
|-----|--------|-------------------|
| ARC-01 | charcoal hooded coat, fingerless gloves | baseline |

**Scale & age lock:** head shorter than CHR-002; apparent age 17, must not drift.

**Do-not-draw list:** no visible hearing aid; no bright colors; both ears intact (scar is subtle).

### CHR-002 — Vela

**Design DNA (paste verbatim):**
> `Vela, late-50s woman, tall and stooped, grey braid, brass-rimmed goggles pushed up on
> forehead, burn-scarred right hand, oilcloth apron over a faded crestless undercoat, dryly kind`

**Palette lock (hex):**
| Element | Hex | Notes |
|---------|-----|-------|
| Hair | #9A968E | grey braid |
| Outfit | #4A4036 | oilcloth / brass |

**Scale & age lock:** a full head taller than CHR-001; late 50s.

**Do-not-draw list:** no Wardenate crest (she tore it off); goggles never over the eyes indoors.

### CHR-003 — Sael

**Design DNA (paste verbatim):**
> `Sael the Warden, 60s man, tall, immaculate, silver hair, slate eyes, dry pale skin,
> grey high-collared coat never wet, brass listener's gorget at the throat, calm certain`

**Palette lock (hex):**
| Element | Hex | Notes |
|---------|-----|-------|
| Hair | #C9CBD0 | silver |
| Coat | #5A5E66 | Warden grey, always dry |
| Gorget | #B08A3E | brass |

**Scale & age lock:** taller than both; 60s. **Do-not-draw list:** never wet, never hurried, no smile that reaches the eyes.

---

## Global style token (append to EVERY panel prompt)
> `black-and-white seinen manga, clean confident linework, screentone shading, high contrast,
> cinematic paneling, rain and reflected neon, no color except a single cyan resonance glow`

## Recurring location references
| LOC-### | Reference image | Lock notes |
|---------|-----------------|------------|
| LOC-002 | `refs/LOC-002/` | flooded market, vertical gangways, neon on black water |
| LOC-003 | `refs/LOC-003/` | half-drowned archive, sealed brass door, resonance-quiet |
| LOC-004 | `refs/LOC-004/` | tuner's nook, brass forks, dead radios above the waterline |

## Panel prompt recipe
```
[global style token] + [shot type & composition] + [LOC reference/desc]
+ [character design DNA for each present character] + [action/expression] + [lighting/mood]
```
