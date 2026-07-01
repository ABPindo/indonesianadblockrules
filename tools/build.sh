#!/bin/bash
# build.sh — Build all ABPindo subscription files from source filters.
# Usage:
#   bash tools/build.sh          # full build (ABP + DNS)
#   bash tools/build.sh abp      # ABP subscriptions only
#   bash tools/build.sh dns      # DNS filters only (requires ABP hosts files)
#
# Prerequisites: python-abp (flrender), python 3.11+, Node.js (for npm scripts)
# For CI, this is called by: npm run build
# For local dev, run: npm run build

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SUBS="$REPO_ROOT/subscriptions"
SRC="$REPO_ROOT/src"

MODE="${1:-all}"

mkdir -p "$SUBS"

# ─── ABP subscriptions (via flrender) ───────────────────────────────
build_abp() {
    echo "==> Building ABP subscriptions..."
    cd "$REPO_ROOT"

    flrender -i abpindo=. abpindo.template             "$SUBS/abpindo.txt"
    flrender -i abpindo=. abpindo_noadult.template     "$SUBS/abpindo_noadult.txt"
    flrender -i abpindo=. abpindo_noelemhide.template  "$SUBS/abpindo_noelemhide.txt"
    flrender -i abpindo=. abpindo_annoyances.template  "$SUBS/abpindo_annoyances.txt"
    flrender -i abpindo=. abpindo_extended.template    "$SUBS/abpindo_extended.txt"
    flrender -i abpindo=. abpindo_hosts.template       "$SUBS/abpindo_hosts.txt"
    flrender -i abpindo=. abpindo_hosts_adult.template "$SUBS/abpindo_hosts_adult.txt"

    echo "    Built 7 ABP subscription files."
}

# ─── DNS filters (via dns_converter.py) ─────────────────────────────
build_dns() {
    echo "==> Building DNS filters..."
    cd "$REPO_ROOT"

    DC="python tools/dns_converter.py"

    # hosts format
    $DC --format hosts "$SUBS/abpindo_hosts.txt"       "$SUBS/hosts.txt"
    $DC --format hosts "$SUBS/abpindo_hosts_adult.txt" "$SUBS/hosts_adult.txt"

    # plain domain list
    $DC --format plain "$SUBS/abpindo_hosts.txt"       "$SUBS/domain.txt"
    $DC --format plain "$SUBS/abpindo_hosts_adult.txt" "$SUBS/domain_adult.txt"

    # dnsmasq address
    $DC --format dnsmasq_address "$SUBS/hosts.txt"       "$SUBS/dnsmasq.txt"
    $DC --format dnsmasq_address "$SUBS/hosts_adult.txt" "$SUBS/dnsmasq_adult.txt"

    # dnsmasq server
    $DC --format dnsmasq_server "$SUBS/hosts.txt"       "$SUBS/dnsmasq_server.txt"
    $DC --format dnsmasq_server "$SUBS/hosts_adult.txt" "$SUBS/dnsmasq_adult_server.txt"

    # RPZ
    $DC --format rpz "$SUBS/hosts.txt"       "$SUBS/rpz.txt"
    $DC --format rpz "$SUBS/hosts_adult.txt" "$SUBS/rpz_adult.txt"

    # AdGuard Home
    $DC --format aghome "$SUBS/hosts.txt"       "$SUBS/aghome.txt"
    $DC --format aghome "$SUBS/hosts_adult.txt" "$SUBS/aghome_adult.txt"

    # Unbound
    $DC --format unbound "$SUBS/hosts.txt"       "$SUBS/unbound.txt"
    $DC --format unbound "$SUBS/hosts_adult.txt" "$SUBS/unbound_adult.txt"

    echo "    Built 14 DNS subscription files."
}

# ─── Main ───────────────────────────────────────────────────────────
case "$MODE" in
    abp)
        build_abp
        ;;
    dns)
        build_dns
        ;;
    all)
        build_abp
        build_dns
        ;;
    *)
        echo "Usage: $0 [abp|dns|all]"
        exit 1
        ;;
esac

FILE_COUNT=$(find "$SUBS" -name '*.txt' -not -name 'LICENSE' | wc -l)
echo "==> Done. $FILE_COUNT subscription files in subscriptions/"
