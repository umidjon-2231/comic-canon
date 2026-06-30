# Character Visual Guide

> How to build the **visual canon** for a character so AI-generated panels stay on-model.
> Panel art drifts faster than prose — this is your defense. One entry per character.

## Why this matters
The #1 reason AI comics look amateur is the protagonist's face changing between panels.
You beat it with three things, reused on *every* prompt: a **design-DNA string**, a **locked
reference set**, and a **global style token**. Lock them once; never paraphrase them later.

---

## Per-character visual entry

### CHR-000 — <name>

**Design DNA (paste verbatim into every prompt for this character):**
> A single dense descriptor string — order matters, keep it identical every time. e.g.:
> `Kai, 17yo girl, lean, short choppy black hair with one silver streak, sharp grey eyes,
> hearing-aid scar behind left ear, charcoal hooded coat, fingerless gloves, wary expression`

**Reference set (generate once, reuse as image refs):**
- [ ] Canonical headshot (the identity anchor)
- [ ] Turnaround: front / 3/4 / side / back
- [ ] Expression sheet: neutral, angry, afraid, determined, hurt, laughing
- [ ] Full-body in default wardrobe
- File paths:

**Palette lock (hex):**
| Element | Hex | Notes |
|---------|-----|-------|
| Hair    |     |       |
| Eyes    |     |       |
| Skin    |     |       |
| Primary outfit |  |   |
| Accent  |     |       |

**Wardrobe by arc (note when/why it changes):**
| Arc | Outfit | Reason it changed |
|-----|--------|-------------------|
| ARC-01 |     |                   |

**Scale & age lock:**
- Height relative to cast: <!-- e.g. "head shorter than CHR-002" -->
- Apparent age (must not drift):

**Do-not-draw list:**
<!-- Things the model keeps adding wrongly — ban them explicitly. -->
-

---

## Global style token (append to EVERY panel prompt, all characters)
> One fixed phrase locking the whole comic's look. e.g.:
> `black-and-white seinen manga, clean confident linework, screentone shading, high contrast,
> cinematic paneling, no color`

## Recurring location references
<!-- Same discipline for sets, so backgrounds stay consistent. -->
| LOC-### | Reference image | Lock notes |
|---------|-----------------|------------|
|         |                 |            |

## Panel prompt recipe
```
[global style token] + [shot type & composition] + [LOC reference/desc]
+ [character design DNA for each present character] + [action/expression] + [lighting/mood]
```
Keep the order fixed. Changing prompt structure between panels is itself a drift source.
