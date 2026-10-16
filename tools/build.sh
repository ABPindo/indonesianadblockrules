#!/bin/bash
# build.sh — Build all ABPindo subscription files from source filters.
# Usage:
#   bash tools/build.sh          # full build (ABP + DNS)
#   bash tools/build.sh abp      # ABP subscriptions only
#   bash tools/build.sh dns      # DNS filters only (requires ABP hosts files)
#
# Prerequisites: fop, flrender (python-abp), python 3.11+ (override with PYTHON=...).
# Single source of truth for building: used by CI (autobuild.yml) and local dev (npm run build).

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SUBS="$REPO_ROOT/subscriptions"
SRC="$REPO_ROOT/src"
SUBS="$(cygpath -m "$SUBS" 2>/dev/null || echo "$SUBS")"
SRC="$(cygpath -m "$SRC" 2>/dev/null || echo "$SRC")"

PYTHON="${PYTHON:-python3}"
MODE="${1:-all}"

for dep in fop flrender "$PYTHON"; do
    command -v "$dep" >/dev/null 2>&1 || { echo "ERROR: missing dependency: $dep" >&2; exit 1; }
done

mkdir -p "$SUBS"

# ─── ABP subscriptions (via flrender) ───────────────────────────────
build_abp() {
    echo "==> Running FOP..."
    fop -n "$SRC"

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

    # Each job: "format input output" -- later jobs may consume earlier outputs.
    DNS_JOBS=(
        "hosts           abpindo_hosts.txt       hosts.txt"
        "hosts           abpindo_hosts_adult.txt hosts_adult.txt"
        "plain           abpindo_hosts.txt       domain.txt"
        "plain           abpindo_hosts_adult.txt domain_adult.txt"
        "dnsmasq_address hosts.txt               dnsmasq.txt"
        "dnsmasq_address hosts_adult.txt         dnsmasq_adult.txt"
        "dnsmasq_server  hosts.txt               dnsmasq_server.txt"
        "dnsmasq_server  hosts_adult.txt         dnsmasq_adult_server.txt"
        "rpz             hosts.txt               rpz.txt"
        "rpz             hosts_adult.txt         rpz_adult.txt"
        "aghome          hosts.txt               aghome.txt"
        "aghome          hosts_adult.txt         aghome_adult.txt"
        "unbound         hosts.txt               unbound.txt"
        "unbound         hosts_adult.txt         unbound_adult.txt"
    )

    for job in "${DNS_JOBS[@]}"; do
        read -r fmt in out <<<"$job"
        "$PYTHON" tools/dns_converter.py --format "$fmt" "$SUBS/$in" "$SUBS/$out"
    done

    echo "    Built ${#DNS_JOBS[@]} DNS subscription files."
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
