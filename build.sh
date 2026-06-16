#!/bin/bash
# build.sh — Local development build script.
# For CI/CD, use .github/workflows/autobuild.yml instead.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUBSCRIPTIONS="$REPO_ROOT/subscriptions"
TOOLS="$REPO_ROOT/tools"

mkdir -p "$SUBSCRIPTIONS"

echo "==> Running FOP..."
fop -n "$REPO_ROOT/src/"

echo "==> Building ABP subscriptions..."
flrender -i abpindo="$REPO_ROOT" "$REPO_ROOT/abpindo.template"             "$SUBSCRIPTIONS/abpindo.txt"
flrender -i abpindo="$REPO_ROOT" "$REPO_ROOT/abpindo_noadult.template"     "$SUBSCRIPTIONS/abpindo_noadult.txt"
flrender -i abpindo="$REPO_ROOT" "$REPO_ROOT/abpindo_noelemhide.template"  "$SUBSCRIPTIONS/abpindo_noelemhide.txt"
flrender -i abpindo="$REPO_ROOT" "$REPO_ROOT/abpindo_annoyances.template"  "$SUBSCRIPTIONS/abpindo_annoyances.txt"
flrender -i abpindo="$REPO_ROOT" "$REPO_ROOT/abpindo_extended.template"    "$SUBSCRIPTIONS/abpindo_extended.txt"
flrender -i abpindo="$REPO_ROOT" "$REPO_ROOT/abpindo_hosts.template"       "$SUBSCRIPTIONS/abpindo_hosts.txt"
flrender -i abpindo="$REPO_ROOT" "$REPO_ROOT/abpindo_hosts_adult.template" "$SUBSCRIPTIONS/abpindo_hosts_adult.txt"

echo "==> Building DNS filters..."
adblock2hosts --ip 0.0.0.0 -o "$SUBSCRIPTIONS/hosts.txt"       "$SUBSCRIPTIONS/abpindo_hosts.txt"
adblock2hosts --ip 0.0.0.0 -o "$SUBSCRIPTIONS/hosts_adult.txt" "$SUBSCRIPTIONS/abpindo_hosts_adult.txt"

adblock2plain -o "$SUBSCRIPTIONS/domain.txt"       "$SUBSCRIPTIONS/abpindo_hosts.txt"
adblock2plain -o "$SUBSCRIPTIONS/domain_adult.txt" "$SUBSCRIPTIONS/abpindo_hosts_adult.txt"

python3 "$TOOLS/dns_converter.py" --format dnsmasq_address "$SUBSCRIPTIONS/hosts.txt"       "$SUBSCRIPTIONS/dnsmasq.txt"
python3 "$TOOLS/dns_converter.py" --format dnsmasq_address "$SUBSCRIPTIONS/hosts_adult.txt" "$SUBSCRIPTIONS/dnsmasq_adult.txt"
python3 "$TOOLS/dns_converter.py" --format dnsmasq_server  "$SUBSCRIPTIONS/hosts.txt"       "$SUBSCRIPTIONS/dnsmasq_server.txt"
python3 "$TOOLS/dns_converter.py" --format dnsmasq_server  "$SUBSCRIPTIONS/hosts_adult.txt" "$SUBSCRIPTIONS/dnsmasq_adult_server.txt"
python3 "$TOOLS/dns_converter.py" --format rpz             "$SUBSCRIPTIONS/hosts.txt"       "$SUBSCRIPTIONS/rpz.txt"
python3 "$TOOLS/dns_converter.py" --format rpz             "$SUBSCRIPTIONS/hosts_adult.txt" "$SUBSCRIPTIONS/rpz_adult.txt"
python3 "$TOOLS/dns_converter.py" --format aghome          "$SUBSCRIPTIONS/hosts.txt"       "$SUBSCRIPTIONS/aghome.txt"
python3 "$TOOLS/dns_converter.py" --format aghome          "$SUBSCRIPTIONS/hosts_adult.txt" "$SUBSCRIPTIONS/aghome_adult.txt"
python3 "$TOOLS/dns_converter.py" --format unbound         "$SUBSCRIPTIONS/hosts.txt"       "$SUBSCRIPTIONS/unbound.txt"
python3 "$TOOLS/dns_converter.py" --format unbound         "$SUBSCRIPTIONS/hosts_adult.txt" "$SUBSCRIPTIONS/unbound_adult.txt"

echo "==> Done. Output: $SUBSCRIPTIONS/"
