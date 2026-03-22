#!/bin/bash
# install_tools.sh — Install local development tools for ABPindo.
# Requires: Python 3.12+, Node.js 22+

set -euo pipefail

echo "==> Installing Python tools..."
python -m pip install --upgrade pip
pip install python-abp adblock-decoder

echo "==> Installing Node.js tools..."
# fop-cli: Filter Orderer and Preener (Rust edition, published via npm)
# https://github.com/ryanbr/fop-rs
npm install -g fop-cli

# dead-domains-linter: checks filter lists for dead domains
# https://github.com/AdguardTeam/DeadDomainsLinter
npm install -g @adguard/dead-domains-linter

echo "==> All tools installed."
echo "    Verify: fop --version && flrender --version && dead-domains-linter --version"
