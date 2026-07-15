#!/bin/bash
# lint.sh — Run AGLint on all source filter files.
# Cross-platform: works on Windows (Git Bash/MSYS2), Linux, and macOS.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/src"

echo "==> Running AGLint on source files..."

# Run AGLint on all .txt files (except redundant.txt) for faster, aggregated output.
shopt -s globstar
mapfile -t files < <(find "$SRC" -name '*.txt' ! -name '*redundant*' ! -name '.aglintignore' | sort)

# On MSYS/Git Bash, convert POSIX paths to Windows paths for native Windows binaries.
if command -v cygpath &>/dev/null; then
  mapfile -t files < <(for f in "${files[@]}"; do cygpath -w "$f"; done)
fi

if command -v aglint &>/dev/null; then
  aglint "${files[@]}"
else
  npx aglint "${files[@]}"
fi

echo "==> Done. No problems found."
