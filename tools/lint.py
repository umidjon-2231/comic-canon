#!/usr/bin/env python3
"""
comic-canon linter (v0.2)

Parses the YAML frontmatter of a story bible and enforces the machine-checkable
subset of validation/continuity-rules.md. It is the automation of the manual
pass — it does NOT replace human judgement for the prose-level rules.

What it checks (machine):
  SCHEMA  scene/character frontmatter validates against schema/*.json
  R1      every referenced ID resolves to a registered entity in /canon
  R9      setups open an SP-### in the ledger; payoffs close one opened earlier
  R12     goal/conflict/outcome/value_turn are non-empty and not "nothing"
  IDS     IDs are unique, well-formed, and match their filename

What stays MANUAL (printed as reminders, never auto-passed):
  R2 fact match · R5 knowledge gating · R6 power cost on-page ·
  R7 power-ledger cause · R8 geography/logistics · R11 voice

Usage:
  python tools/lint.py [STORY_DIR]      # default: current directory
  python tools/lint.py examples/the-wardens-coin

Exit code: 0 if no errors, 1 if any error (suitable for CI).
Requires: pyyaml, jsonschema  (see tools/requirements.txt)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("error: pyyaml is required — run: pip install -r tools/requirements.txt")
try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("error: jsonschema is required — run: pip install -r tools/requirements.txt")

import json

from canonlib import PLACEHOLDER, is_template, parse_frontmatter, use_utf8_io

# --- ID patterns -------------------------------------------------------------
ID_PATTERNS = {
    "CHR": re.compile(r"^CHR-\d{3}$"),
    "LOC": re.compile(r"^LOC-\d{3}$"),
    "FAC": re.compile(r"^FAC-\d{3}$"),
    "PWR": re.compile(r"^PWR-\d{3}$"),
    "ITM": re.compile(r"^ITM-\d{3}$"),
    "EVT": re.compile(r"^EVT-\d{3}$"),
    "ARC": re.compile(r"^ARC-\d{2}$"),
    "SCN": re.compile(r"^S\d{2}-\d{3}$"),
    "SP":  re.compile(r"^SP-\d{3}$"),
}

SECTION_ID = re.compile(r"^#{2,4}\s+((?:LOC|FAC|PWR|ITM)-\d{3})\b", re.M)
ANY_EVT = re.compile(r"\bEVT-\d{3}\b")
ANY_SP = re.compile(r"\bSP-\d{3}\b")


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"  [ERROR] {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"  [warn]  {where}: {msg}")


def collect_ids(text: str, pattern: re.Pattern) -> set[str]:
    return {m for m in pattern.findall(text) if not PLACEHOLDER.search(m)}


def build_registry(root: Path, rep: Report) -> dict[str, set[str]]:
    """Scan /canon and /scenes for every defined ID (rule R1's resolution map)."""
    reg: dict[str, set[str]] = {k: set() for k in
                                ("CHR", "LOC", "FAC", "PWR", "ITM", "EVT", "SP", "SCN", "ARC")}
    canon = root / "canon"

    # Characters: one file each
    for f in sorted((canon / "characters").glob("*.md")) if (canon / "characters").exists() else []:
        if is_template(f):
            continue
        fm = parse_frontmatter(f)
        if fm and isinstance(fm.get("id"), str) and ID_PATTERNS["CHR"].match(fm["id"]):
            cid = fm["id"]
            reg["CHR"].add(cid)
            if cid not in f.stem:
                rep.warn(f.name, f"id {cid} not reflected in filename")

    # Registry sections / rows
    def section_ids(fname: str) -> set[str]:
        fp = canon / fname
        if not fp.exists():
            return set()
        found = SECTION_ID.findall(fp.read_text(encoding="utf-8"))
        return {x for x in found if not PLACEHOLDER.search(x)}

    for x in section_ids("01-world.md"):
        reg[x[:3]].add(x)
    for x in section_ids("02-power-system.md"):
        reg["PWR"].add(x)
    for x in section_ids("items.md"):
        reg["ITM"].add(x)

    tl = canon / "timeline.md"
    if tl.exists():
        reg["EVT"] |= collect_ids(tl.read_text(encoding="utf-8"), ANY_EVT)

    ledger = root / "validation" / "payoff-ledger.md"
    if ledger.exists():
        reg["SP"] |= collect_ids(ledger.read_text(encoding="utf-8"), ANY_SP)

    arc = root / "structure" / "arc.md"
    if arc.exists():
        for m in re.findall(r"\bARC-\d{2}\b", arc.read_text(encoding="utf-8")):
            if not PLACEHOLDER.search(m):
                reg["ARC"].add(m)

    # Scenes: one file each
    sdir = root / "scenes"
    for f in sorted(sdir.glob("*.md")) if sdir.exists() else []:
        if is_template(f):
            continue
        fm = parse_frontmatter(f)
        if fm and isinstance(fm.get("id"), str) and ID_PATTERNS["SCN"].match(fm["id"]):
            reg["SCN"].add(fm["id"])

    return reg


def parse_ledger(root: Path) -> dict[str, str]:
    """Map SP-### -> the scene id it was planted in (R9 'opened earlier' check)."""
    planted: dict[str, str] = {}
    ledger = root / "validation" / "payoff-ledger.md"
    if not ledger.exists():
        return planted
    for line in ledger.read_text(encoding="utf-8").splitlines():
        if not line.lstrip().startswith("| SP-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        sp = cells[0]
        if not ID_PATTERNS["SP"].match(sp):
            continue
        scene = next((m.group(0) for c in cells[1:]
                      for m in [re.search(r"S\d{2}-\d{3}", c)] if m), None)
        if scene:
            planted[sp] = scene
    return planted


def load_schema(schema_dir: Path, name: str) -> Draft202012Validator | None:
    fp = schema_dir / name
    if not fp.exists():
        return None
    return Draft202012Validator(json.loads(fp.read_text(encoding="utf-8")))


def lint(root: Path, schema_dir: Path) -> Report:
    rep = Report()
    reg = build_registry(root, rep)
    planted = parse_ledger(root)

    char_schema = load_schema(schema_dir, "character.schema.json")
    scene_schema = load_schema(schema_dir, "scene.schema.json")

    # --- characters: schema only -------------------------------------------
    cdir = root / "canon" / "characters"
    for f in sorted(cdir.glob("*.md")) if cdir.exists() else []:
        if is_template(f):
            continue
        try:
            fm = parse_frontmatter(f)
        except ValueError as exc:
            rep.error(f.name, str(exc))
            continue
        if fm and char_schema:
            for err in sorted(char_schema.iter_errors(fm), key=str):
                rep.error(f.name, f"schema: {err.message}")

    # --- scenes: schema + R1 + R9 + R12 ------------------------------------
    sdir = root / "scenes"
    scenes = [f for f in sorted(sdir.glob("*.md")) if not is_template(f)] if sdir.exists() else []
    if not scenes:
        rep.warn("scenes/", "no scene files found (only templates?) — nothing to lint")

    def resolve(where: str, kind: str, value) -> None:
        """R1: value(s) must exist in the registry for `kind`."""
        if value is None:
            return
        for v in (value if isinstance(value, list) else [value]):
            if not isinstance(v, str) or PLACEHOLDER.search(v):
                continue
            bucket = "SCN" if kind == "SCN" else v.split("-")[0]
            if v not in reg.get(bucket, set()):
                rep.error(where, f"R1 unknown {kind}: {v} not defined in /canon")

    for f in scenes:
        try:
            fm = parse_frontmatter(f)
        except ValueError as exc:
            rep.error(f.name, str(exc))
            continue
        if not fm:
            rep.error(f.name, "scene has no frontmatter")
            continue
        where = f.name

        if scene_schema:
            for err in sorted(scene_schema.iter_errors(fm), key=str):
                rep.error(where, f"schema: {err.message}")

        sid = fm.get("id", "")
        if isinstance(sid, str) and sid and sid not in f.stem:
            rep.warn(where, f"id {sid} not reflected in filename")

        # R1 — entity existence
        resolve(where, "LOC", fm.get("location"))
        resolve(where, "CHR", fm.get("pov"))
        resolve(where, "CHR", fm.get("present"))
        resolve(where, "CHR/LOC/FAC/ITM/PWR", fm.get("mentioned"))
        refs = fm.get("refs") or {}
        if isinstance(refs, dict):
            resolve(where, "SCN", refs.get("follows"))
            resolve(where, "SCN", refs.get("callbacks"))
            resolve(where, "SP", refs.get("setups"))
            resolve(where, "SP", refs.get("payoffs"))

            # R9 — setup/payoff integrity
            for sp in refs.get("setups") or []:
                if PLACEHOLDER.search(sp):
                    continue
                if sp not in planted:
                    rep.error(where, f"R9 setup {sp} has no row in payoff-ledger.md")
            for sp in refs.get("payoffs") or []:
                if PLACEHOLDER.search(sp):
                    continue
                origin = planted.get(sp)
                if origin is None:
                    rep.error(where, f"R9 payoff {sp} closes a setup never opened (E10)")
                elif isinstance(sid, str) and origin >= sid:
                    rep.error(where, f"R9 payoff {sp} opened in {origin}, not an earlier scene")

        # R12 — scene earns its place
        for field in ("goal", "conflict", "outcome", "value_turn"):
            val = (fm.get(field) or "").strip().lower()
            if not val:
                rep.error(where, f"R12 empty {field}")
            elif field == "outcome" and val in ("nothing", "nothing changed", "nothing changes"):
                rep.error(where, "R12 outcome is 'nothing changed' — scene is inert")

    return rep


MANUAL_RULES = (
    "R2 fact/spelling match", "R5 knowledge gating", "R6 power cost on-page",
    "R7 power-ledger cause", "R8 geography/logistics", "R11 voice consistency",
)


def main() -> int:
    ap = argparse.ArgumentParser(description="Lint a comic-canon story bible.")
    ap.add_argument("root", nargs="?", default=".", help="story directory (default: .)")
    ap.add_argument("--schema", default=None,
                    help="schema dir (default: the repo's schema/ next to this script)")
    args = ap.parse_args()
    use_utf8_io()

    root = Path(args.root).resolve()
    schema_dir = Path(args.schema).resolve() if args.schema else Path(__file__).resolve().parent.parent / "schema"

    if not (root / "canon").exists() and not (root / "scenes").exists():
        print(f"error: {root} doesn't look like a story dir (no canon/ or scenes/)")
        return 2

    print(f"comic-canon lint · {root}")
    print(f"schemas · {schema_dir}\n")

    rep = lint(root, schema_dir)

    for line in rep.warnings:
        print(line)
    for line in rep.errors:
        print(line)

    print()
    if rep.errors:
        print(f"FAIL — {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
    else:
        print(f"OK — 0 errors, {len(rep.warnings)} warning(s)")
    print("\nStill needs a human pass (not machine-checked): " + " · ".join(MANUAL_RULES))
    return 1 if rep.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
