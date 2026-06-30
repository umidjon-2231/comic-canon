#!/usr/bin/env python3
"""
Scaffold a fresh story from the blank template.

Copies the empty canon/scenes/structure/validation/schema (plus the cheatsheet) into a new
directory, leaving the examples and tooling behind, so you start from clean canon instead of
deleting example files by hand.

Usage:
  python tools/new-story.py ../my-comic
  python tools/new-story.py ../my-comic --force   # allow a non-empty target
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

# Top-level entries that make up the blank template (everything a new story needs, nothing else).
TEMPLATE_ENTRIES = ["canon", "scenes", "structure", "validation", "schema", "CHEATSHEET.md"]

STARTER_README = """# {name}

A story bible built from [Comic Canon](https://github.com/umidjon-2231/comic-canon).

## Start here
1. Read `CHEATSHEET.md` — the quality bar.
2. Lock canon (the 6 layers in `canon/`) before drafting any scene.
3. Copy `scenes/_TEMPLATE.md` per scene; reference canon by ID, never by loose name.
4. Validate: `python <comic-canon>/tools/lint.py .`

Canon is the single source of truth. Scenes consume it; they never invent it.
"""


def main() -> int:
    ap = argparse.ArgumentParser(description="Scaffold a new comic-canon story.")
    ap.add_argument("target", help="directory to create the new story in")
    ap.add_argument("--force", action="store_true", help="proceed even if target exists/non-empty")
    args = ap.parse_args()

    repo = Path(__file__).resolve().parent.parent
    target = Path(args.target).resolve()

    if target.exists() and any(target.iterdir()) and not args.force:
        print(f"error: {target} exists and isn't empty (use --force to override)")
        return 1
    target.mkdir(parents=True, exist_ok=True)

    for entry in TEMPLATE_ENTRIES:
        src = repo / entry
        if not src.exists():
            print(f"warning: template missing {entry}, skipping")
            continue
        dst = target / entry
        if src.is_dir():
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy2(src, dst)

    readme = target / "README.md"
    if not readme.exists() or args.force:
        readme.write_text(STARTER_README.format(name=target.name), encoding="utf-8")

    print(f"created a new story in {target}")
    print("next: read CHEATSHEET.md, lock canon/, then draft scenes/.")
    print(f"lint it with:  python {repo / 'tools' / 'lint.py'} {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
