---
id: TIMELINE
type: timeline
status: canon
version: 1
tags: []
---

# Timeline

> The canonical chronology. Timeline/plot-logic errors are one of the two dominant AI failure
> modes — this file is the fix. Every scene's `in_world_time` must be consistent with this.

## Calendar convention
<!-- Define how in-world time is expressed so it sorts cleanly. Pick one and stick to it. -->
- Format: <!-- e.g. "Year.Day" (003.142) or absolute dates or "Arc-relative day" -->
- Day 0 / Year 0 anchor:

## Backstory events (before the story opens)
| ID | When | Event | Who | Referenced by |
|----|------|-------|-----|---------------|
| EVT-001 |  |      |     |               |

## Story events (during the narrative)
<!-- Add a row as each scene establishes a dated event. Keep it sorted. -->
| ID | In-world time | Event | Scene | Caused by (prior EVT) |
|----|---------------|-------|-------|------------------------|
| EVT-101 |          |       | S01-001 |                     |

## Causal chain check
<!-- For any event, its causes must precede it. List the must-hold orderings so the linter
     (or you) can verify no scene violates them. -->
- EVT-### must come before EVT-###  because:

## Parallel threads (who's where, when)
<!-- If multiple plotlines run at once, track them side by side so a character can't be in
     two places at the same in-world time (error E8). -->
| In-world time | Thread A (CHR-001) | Thread B (CHR-003) |
|---------------|--------------------|--------------------|
|               |                    |                    |
