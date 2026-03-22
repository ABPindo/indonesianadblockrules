#!/usr/bin/env python3
"""
dns_converter.py — Convert a hosts file to various DNS blocker formats.

Replaces: hosts_to_aghome.py, hosts_to_dnsmasq_address.py,
          hosts_to_dnsmasq_server.py, hosts_to_rpz.py, hosts_to_unbound.py

Source: https://gist.github.com/iam-py-test/ba35ce681e195c690ea3590f79479a3b

Usage:
    python3 dns_converter.py --format FORMAT input.txt output.txt

Formats:
    aghome          ||example.com^
    dnsmasq_address address=/example.com/0.0.0.0
    dnsmasq_server  server=/example.com/
    rpz             example.com CNAME .
    unbound         local-zone: "example.com" always_nxdomain
"""

import sys
import argparse

FORMATS = {
    "aghome":          lambda d: f"||{d}^",
    "dnsmasq_address": lambda d: f"address=/{d}/0.0.0.0",
    "dnsmasq_server":  lambda d: f"server=/{d}/",
    "rpz":             lambda d: f"{d} CNAME .",
    "unbound":         lambda d: f'local-zone: "{d}" always_nxdomain',
}

# Lines starting with these prefixes are not valid hosts entries
_SKIP_PREFIXES = ("#", "!", "[", "|")


def extract_domain(line: str) -> str | None:
    """Return the domain from a hosts-format line, or None if not applicable."""
    line = line.strip()
    if not line or line.startswith(_SKIP_PREFIXES):
        return None
    if line.startswith(("0.0.0.0", "127.0.0.1")):
        parts = line.split()
        return parts[1] if len(parts) >= 2 else None
    return line


def convert(input_path: str, output_path: str, fmt: str) -> None:
    formatter = FORMATS[fmt]
    print(f"Converting {input_path} -> {output_path} (format: {fmt})")

    with open(input_path, "r", encoding="utf-8") as infile, \
         open(output_path, "w", encoding="utf-8") as outfile:

        for line in infile:
            stripped = line.strip()

            if not stripped:
                continue

            if stripped.startswith("#"):
                outfile.write(stripped + "\n")
                continue

            domain = extract_domain(stripped)
            if domain:
                outfile.write(formatter(domain) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert hosts file to DNS blocker formats."
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=FORMATS.keys(),
        metavar="FORMAT",
        help=f"Output format: {', '.join(FORMATS.keys())}",
    )
    parser.add_argument("input", help="Input hosts file")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()

    try:
        convert(args.input, args.output, args.format)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
