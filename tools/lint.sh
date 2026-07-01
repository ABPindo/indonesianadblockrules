#!/bin/bash
# lint.sh — Run AGLint on all source filter files.
# Cross-platform: works on Windows (Git Bash/MSYS2), Linux, and macOS.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SRC="$REPO_ROOT/src"

echo "==> Running AGLint on source files..."

# Run AGLint on all .txt files in a single invocation for faster, aggregated output.
# Requires bash 4+ for globstar (enabled by default in Git Bash / MSYS2).
shopt -s globstar
aglint "$SRC"/**/*.txt

echo "==> Done. No problems found."
