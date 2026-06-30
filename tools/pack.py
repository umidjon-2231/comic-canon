#!/usr/bin/env python3
"""
context-packer (v0.3) — assemble the minimal canon an AI needs for one scene.

This is the "context assembly" step from CHEATSHEET §7, as a deterministic tool.
Given a scene ID it gathers ONLY the relevant canon — premise + relevant world/power
sections + sheets for everyone `present` + the previous scene's state_changes + brief
summaries of referenced scenes + open setups + the glossary — and prints one self-contained
bundle. Feed that bundle to ANY AI (Claude, GPT, Gemini, a local model, an SDK) to draft or
review the scene. No AI and no network here — just retrieval, so every agent shares one
grounding step instead of re-deriving it.

Usage:
  python tools/pack.py S01-003 --root examples/the-wardens-coin
  python tools/pack.py S01-003 --root examples/the-wardens-coin --review   # include the draft
  python tools/pack.py S01-003 --root examples/the-wardens-coin --out bundle.md

Requires: pyyaml  (see tools/requirements.txt)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import canonlib as cl

PWR_RE = re.compile(r"\bPWR-\d{3}\b")
LEDGER_OPEN = ("🔴", "🟡")


def _section(title: str, content: str | None) -> str:
    return f"## {title}\n\n{content.strip()}\n" if content and content.strip() else ""


def scene_summary(fm: dict, path: Path) -> str:
    """A one-block summary of a referenced scene — not its full text."""
    sid = fm.get("id", path.stem)
    stype = fm.get("scene_type", "")
    goal = fm.get("goal", "")
    outcome = fm.get("outcome", "")
    beat = cl.slice_title_section(cl.body(path), r"^Beat\b")
    beat_line = ""
    if beat:
        rest = beat.split("\n", 1)[1].strip() if "\n" in beat else ""
        beat_line = " ".join(rest.split())[:240]
    line = f"- **{sid}** ({stype}): wants *{goal}* → *{outcome}*"
    return f"{line}\n  {beat_line}" if beat_line else line


def pack(root: Path, sid: str, review: bool) -> str:
    scenes = cl.scene_index(root)
    if sid not in scenes:
        raise SystemExit(f"error: scene {sid} not found under {root}/scenes")
    spath = scenes[sid]
    fm = cl.parse_frontmatter(spath) or {}
    chars = cl.character_index(root)
    canon = root / "canon"

    present = fm.get("present") or []
    mentioned = fm.get("mentioned") or []
    location = fm.get("location")
    refs = fm.get("refs") or {}
    follows = refs.get("follows")
    callbacks = refs.get("callbacks") or []

    out: list[str] = []
    out.append(f"# Context bundle — {sid}")
    out.append(
        "> Assembled by tools/pack.py. This is the ONLY canon you need for this scene. "
        "Honor every ID, the glossary spelling, and each power's cost. Do not invent facts "
        "not present here — if something's missing, it belongs in canon first.\n"
    )

    # --- the target scene's intent (what to write) ---------------------------
    intent = [f"- **{k}:** {fm.get(k)}" for k in
              ("scene_type", "in_world_time", "location", "pov", "goal", "conflict",
               "outcome", "value_turn") if fm.get(k) not in (None, "")]
    intent.append(f"- **present:** {present}")
    if mentioned:
        intent.append(f"- **mentioned:** {mentioned}")
    out.append(_section("Target scene — intent", "\n".join(intent)))

    # --- premise (whole, it's short) ----------------------------------------
    premise = canon / "00-premise.md"
    if premise.exists():
        out.append(_section("Premise", cl.body(premise)))

    # --- world: intro + rules + the referenced LOC/FAC sections -------------
    world = canon / "01-world.md"
    if world.exists():
        wtext = cl.read_text(world)
        parts = [cl.slice_title_section(wtext, r"One-paragraph pitch"),
                 cl.slice_title_section(wtext, r"Rules of reality")]
        for ent in ([location] if location else []) + [m for m in mentioned if m[:3] in ("LOC", "FAC")]:
            parts.append(cl.slice_id_section(wtext, ent) or f"### {ent}\n_(not found in 01-world.md)_")
        out.append(_section("World (relevant slices)", "\n\n".join(p for p in parts if p)))

    # --- power system: laws + one-paragraph + PWRs the cast can use ---------
    power = canon / "02-power-system.md"
    if power.exists():
        ptext = cl.read_text(power)
        pwr_ids: set[str] = {m for m in mentioned if m.startswith("PWR")}
        for cid in present:
            if cid in chars:
                pwr_ids |= set(PWR_RE.findall(cl.read_text(chars[cid])))
        parts = [cl.slice_title_section(ptext, r"system in one paragraph"),
                 cl.slice_title_section(ptext, r"Global laws")]
        for pid in sorted(pwr_ids):
            parts.append(cl.slice_id_section(ptext, pid) or f"### {pid}\n_(not found in 02-power-system.md)_")
        out.append(_section("Power system (relevant)", "\n\n".join(p for p in parts if p)))

    # --- character sheets for everyone present ------------------------------
    sheets = []
    for cid in present:
        if cid in chars:
            sheets.append(cl.body(chars[cid]))
        else:
            sheets.append(f"### {cid}\n_(no character file found)_")
    if sheets:
        out.append(_section("Characters present (full sheets)", "\n\n---\n\n".join(sheets)))

    # --- items referenced on-page (state, holder) ---------------------------
    items_file = canon / "items.md"
    item_ids = [m for m in mentioned if m.startswith("ITM")]
    if items_file.exists() and item_ids:
        itext = cl.read_text(items_file)
        parts = [cl.slice_id_section(itext, i) or f"### {i}\n_(not found in items.md)_" for i in item_ids]
        out.append(_section("Items referenced (current state)", "\n\n".join(parts)))

    # --- what this scene inherits (previous scene's state_changes) ----------
    if follows and follows in scenes:
        pfm = cl.parse_frontmatter(scenes[follows]) or {}
        changes = pfm.get("state_changes") or []
        body = "\n".join(f"- {c}" for c in changes) or "_(none)_"
        out.append(_section(f"Inherited state — from {follows}", body))

    # --- summaries of referenced scenes -------------------------------------
    ref_ids = [r for r in callbacks if r in scenes]
    if ref_ids:
        out.append(_section("Referenced scenes (summaries, not full text)",
                            "\n".join(scene_summary(cl.parse_frontmatter(scenes[r]) or {}, scenes[r])
                                      for r in ref_ids)))

    # --- open setups that could pay off here --------------------------------
    ledger = root / "validation" / "payoff-ledger.md"
    if ledger.exists():
        rows = [ln.strip() for ln in cl.read_text(ledger).splitlines()
                if ln.lstrip().startswith("| SP-") and any(s in ln for s in LEDGER_OPEN)]
        if rows:
            out.append(_section("Open setups (from the payoff ledger)", "\n".join(rows)))

    # --- glossary (always) ---------------------------------------------------
    glossary = canon / "glossary.md"
    if glossary.exists():
        out.append(_section("Glossary (spelling & term lock — always honor)", cl.body(glossary)))

    # --- the current draft, only when reviewing -----------------------------
    if review:
        out.append(_section(f"Current draft of {sid} (for review)", cl.body(spath)))

    return "\n".join(b for b in out if b).rstrip() + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description="Assemble the minimal canon context for one scene.")
    ap.add_argument("scene", help="scene id, e.g. S01-003")
    ap.add_argument("--root", default=".", help="story directory (default: .)")
    ap.add_argument("--review", action="store_true",
                    help="also include the scene's current draft (for continuity review)")
    ap.add_argument("--out", default=None, help="write to a file instead of stdout")
    args = ap.parse_args()

    cl.use_utf8_io()
    bundle = pack(Path(args.root).resolve(), args.scene, args.review)
    words = len(bundle.split())

    if args.out:
        Path(args.out).write_text(bundle, encoding="utf-8")
        print(f"wrote {args.out} — {words} words (~{words * 4 // 3} tokens)", file=sys.stderr)
    else:
        sys.stdout.write(bundle)
        print(f"\n<!-- packed {args.scene}: {words} words (~{words * 4 // 3} tokens) -->",
              file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
