#!/bin/bash
# install_tools.sh — Install local development tools for ABPindo.
# For CI, see .github/actions/setup-tools/action.yml instead.
# Requires: Python 3.11+, Node.js 18+

set -euo pipefail

echo "==> Installing Python tools..."
python -m pip install --upgrade pip
pip install python-abp

echo "==> Installing Node.js tools..."
# Install from package.json (preferred)
if [ -f "package.json" ]; then
    npm install
fi

# fop-cli: Filter Orderer and Preener (Rust edition, published via npm)
# https://github.com/ryanbr/fop-rs
npm install -g fop-cli

# aglint: AdGuard linter for filter lists
# https://github.com/AdguardTeam/AGLint
npm install -g @adguard/aglint

# dead-domains-linter: checks filter lists for dead domains
# https://github.com/AdguardTeam/DeadDomainsLinter
npm install -g @adguard/dead-domains-linter

echo "==> All tools installed."
echo "    Verify: fop --version && aglint --version && dead-domains-linter --version"
