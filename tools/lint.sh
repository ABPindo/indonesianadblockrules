#!/bin/bash
# lint.sh — Run AGLint on all source filter files.
# Cross-platform: works on Windows (Git Bash/MSYS2), Linux, and macOS.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/src"

echo "==> Running AGLint on source files..."

# Run AGLint on all .txt files (except redundant.txt) for faster, aggregated output.
# Requires bash 4+ for globstar (enabled by default in Git Bash / MSYS2).
shopt -s globstar
mapfile -t files < <(find "$SRC" -name '*.txt' ! -name '*redundant*' ! -name '.aglintignore' | sort)
aglint "${files[@]}"

echo "==> Done. No problems found."
