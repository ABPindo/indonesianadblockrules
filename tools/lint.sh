#!/bin/bash
# lint.sh — Run AGLint on all source filter files.
# Cross-platform: works on Windows (Git Bash/MSYS2), Linux, and macOS.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/src"

echo "==> Running AGLint on source files..."

# Find all .txt files in src/ and run AGLint
find "$SRC" -name "*.txt" -type f | while read -r file; do
    npx aglint "$file"
done

echo "==> Done. No problems found."
