---
id: CHR-000          # CHR-001, CHR-002, ...
type: character
status: canon
version: 1
tags: []             # e.g. [protagonist] / [antagonist] / [ally] / [recurring]
role: protagonist    # protagonist | antagonist | ally | mentor | rival | foil | minor
first_appears: S00-000
# Facts that can change over time use validity intervals so legitimate change
# (ally→enemy, alive→dead) isn't flagged as a contradiction:
alive: true
status_intervals:
  - fact: "alive"
    valid_from: S00-000
    valid_until: null   # null = still true
---

# <Character Name>

## Snapshot
- **Role in story:**
- **One-line essence:** <!-- the "who they are" you could tattoo on the reader -->
- **Want (external goal):**
- **Need (internal lesson):**
- **The lie they believe:**
- **Arc (start → end):**

## Appearance (text — visual lock lives in the visual guide)
- Age / apparent age:
- Build / height: <!-- lock relative scale vs other characters -->
- Hair / eyes / skin:
- Distinguishing marks: <!-- scars, tattoos — these are top sources of drift errors -->
- Default wardrobe:
- Visual canon: <!-- link to _VISUAL-GUIDE entry + reference image path -->

## Personality
- Core traits (3–5):
- Strengths:
- Flaws / blind spots:
- Fears:
- Desires (beyond the plot goal):
- Moral line they won't cross (until they do):

## Voice (anti tone-drift)
- Speech style: <!-- terse? formal? slang-heavy? -->
- Verbal tics / catchphrases:
- What they never say:
- Sample line: >

## Backstory (only what the story will reference)
-

## Abilities
- Powers: <!-- PWR-### list -->
- Current tier: <!-- must match power ledger -->
- Signature technique:
- Personal cost/limit/weakness specifics:

## Relationships
<!-- Generalize "relation to hero" into a graph. Use validity intervals for any bond that
     changes — this is how you avoid the "still acting like allies after the betrayal" error. -->
| With | Relationship | valid_from | valid_until |
|------|--------------|------------|-------------|
| CHR-### |           |            |             |

## Knowledge state (anti knowledge-leak, E5)
<!-- What this character KNOWS and from when. A character must not act on info before they
     learn it. Update as the story reveals things. -->
| Knows | Since scene |
|-------|-------------|
|       |             |

## Status log (injuries, possessions, location over time)
<!-- The running state the next scene inherits. -->
| Scene | Change |
|-------|--------|
|       |        |
