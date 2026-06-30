# Quickstart

From zero to your first lint-clean scene. No prior setup beyond Python 3.9+.

> New here? Read [`CHEATSHEET.md`](./CHEATSHEET.md) first — it's the quality bar. This page is the
> mechanical 5-minute path. To see a finished example, open
> [`examples/the-wardens-coin/`](./examples/the-wardens-coin/).

## 1. Get the tools (once)

```bash
pip install -r tools/requirements.txt
```

## 2. Start your story

```bash
python tools/new-story.py ../my-comic
cd ../my-comic
```

This copies the **blank** template (canon, scenes, structure, validation, schema) — no example
clutter to delete.

## 3. Lock canon before you draft (this is the whole trick)

Fill these six, in `canon/`, in order. Don't skip — drafting before canon is locked is the #1
cause of mid-story contradictions.

1. `00-premise.md` — logline, theme, the hero's want vs. need.
2. `01-world.md` — setting, rules of reality, **locations (`LOC-###`)** and **factions (`FAC-###`)**.
3. `02-power-system.md` — your strength system + each **ability (`PWR-###`)** with its cost/limit/weakness.
4. `characters/` — copy `_TEMPLATE.md` per recurring character (`CHR-###`).
5. `timeline.md` — the chronology (`EVT-###`).
6. `glossary.md` — locked spelling of every name. (`items.md` registers any `ITM-###` as they appear.)

Every canonical thing gets a **stable ID**. Scenes reference things by ID, never by loose name —
that's what makes the bible checkable. See the ID table in [`README.md`](./README.md).

## 4. Write a scene

```bash
cp scenes/_TEMPLATE.md scenes/S01-001.md
```

Fill the frontmatter (`location`, `present`, `pov`, `goal`, `conflict`, `outcome`, `value_turn`).
Then let the tooling assemble *only* the canon this scene needs and hand it to any AI:

```bash
python <path-to>/comic-canon/tools/pack.py S01-001 --root . > bundle.md
```

Pair that bundle with `agents/scene-drafter.md` (a portable spec that works with any AI) to draft
in-canon, then write the `state_changes` — what the next scene inherits.

## 5. Lint before you lock it

```bash
python <path-to>/comic-canon/tools/lint.py .
```

Green means the machine-checkable rules pass (entities exist, setups/payoffs balance, the scene
earns its place). The linter also prints the rules a **human** still has to check (voice, power
costs paid on-page, geography). Fix errors, set `status: locked`, then **write the scene's
`state_changes` back into canon** — stale canon is tomorrow's contradiction.

## 6. Repeat

Loop steps 4–5 per scene. At each arc midpoint, lint the whole arc, not just the latest scene —
errors cluster in the middle of long stories.

---

**Stuck?** Compare against the worked example, which passes the linter cleanly:

```bash
python tools/lint.py examples/the-wardens-coin
```
