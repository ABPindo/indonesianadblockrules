#!/usr/bin/env python3
"""
find_duplicates.py — Detect duplicate rules across ABPindo source filter files.

Scans all .txt files under src/ and reports rules that appear in more than one
file (or multiple times within the same file).

Usage:
    python tools/find_duplicates.py              # check all src/**/*.txt
    python tools/find_duplicates.py src/advert/  # check specific directory
    python tools/find_duplicates.py --strict      # exit 1 if any duplicates found

Exit codes:
    0 — no duplicates found
    1 — duplicates found (or --strict and duplicates exist)
"""

import sys
import argparse
from pathlib import Path
from collections import defaultdict


def is_rule(line: str) -> bool:
    """Return True if the line is an actual filter rule (not comment/header/blank)."""
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith(("!", "[", "#")):
        return False
    return True


def find_duplicates(src_dir: Path, strict: bool = False) -> int:
    """
    Scan src_dir for .txt files and report duplicate rules.

    Returns the number of duplicate rules found.
    """
    # rule -> list of (file, line_number)
    rules: dict[str, list[tuple[str, int]]] = defaultdict(list)

    txt_files = sorted(src_dir.rglob("*.txt"))
    if not txt_files:
        print(f"No .txt files found in {src_dir}")
        return 0

    for filepath in txt_files:
        # Use relative path for readable output
        try:
            rel = filepath.relative_to(src_dir.parent)
        except ValueError:
            rel = filepath

        with open(filepath, "r", encoding="utf-8") as f:
            for lineno, line in enumerate(f, start=1):
                if is_rule(line):
                    rule = line.strip()
                    rules[rule].append((str(rel), lineno))

    # Find duplicates
    duplicates = {
        rule: locations
        for rule, locations in rules.items()
        if len(locations) > 1
    }

    if not duplicates:
        print(f"✅ No duplicate rules found across {len(txt_files)} files.")
        return 0

    # Report
    print(f"⚠️  Found {len(duplicates)} duplicate rules across {len(txt_files)} files:\n")

    for rule, locations in sorted(duplicates.items()):
        print(f"  Rule: {rule}")
        for filepath, lineno in locations:
            print(f"    → {filepath}:{lineno}")
        print()

    total_instances = sum(len(locs) for locs in duplicates.values())
    print(f"Summary: {len(duplicates)} rules duplicated across {total_instances} locations.")

    if strict:
        sys.exit(1)

    return len(duplicates)


def main():
    parser = argparse.ArgumentParser(
        description="Detect duplicate rules in ABPindo source filter files."
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=None,
        help="Directory to scan (default: src/ relative to repo root)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with code 1 if duplicates are found",
    )
    args = parser.parse_args()

    if args.path:
        src_dir = Path(args.path)
    else:
        # Default: find src/ relative to this script's location
        script_dir = Path(__file__).resolve().parent
        src_dir = script_dir.parent / "src"

    if not src_dir.is_dir():
        print(f"Error: {src_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    dup_count = find_duplicates(src_dir, strict=args.strict)
    sys.exit(0)


if __name__ == "__main__":
    main()
