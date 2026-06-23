#!/usr/bin/env python3
"""
dns_converter.py — Convert ABP/hosts files to various DNS blocker formats.

Replaces: adblock2hosts, adblock2plain, hosts_to_aghome.py,
          hosts_to_dnsmasq_address.py, hosts_to_dnsmasq_server.py,
          hosts_to_rpz.py, hosts_to_unbound.py

Source: https://gist.github.com/iam-py-test/ba35ce681e195c690ea3590f79479a3b

Usage:
    python3 dns_converter.py --format FORMAT input.txt output.txt
    python3 dns_converter.py --format FORMAT --check input.txt

Formats:
    hosts           0.0.0.0 example.com  (replaces adblock2hosts)
    plain           example.com           (replaces adblock2plain)
    aghome          ||example.com^
    dnsmasq_address address=/example.com/0.0.0.0
    dnsmasq_server  server=/example.com/
    rpz             example.com CNAME .
    unbound         local-zone: "example.com" always_nxdomain
"""

import sys
import re
import argparse

FORMATS = {
    "hosts":           lambda d: f"0.0.0.0 {d}",
    "plain":           lambda d: d,
    "aghome":          lambda d: f"||{d}^",
    "dnsmasq_address": lambda d: f"address=/{d}/0.0.0.0",
    "dnsmasq_server":  lambda d: f"server=/{d}/",
    "rpz":             lambda d: f"{d} CNAME .",
    "unbound":         lambda d: f'local-zone: "{d}" always_nxdomain',
}

# Regex to match ABP network filter rules: ||domain.com^$options
_ABP_NETWORK_RE = re.compile(r"^\|\|([a-zA-Z0-9.-]+)\^")

# Regex to detect lines that look like ABP rules but don't match our parser
_ABP_LIKE_RE = re.compile(r"^\|\|.*\^")


def extract_domain(line: str) -> str | None:
    """Return the domain from a hosts or ABP-format line, or None if not applicable."""
    line = line.strip()
    if not line:
        return None

    # Skip comments and headers
    if line.startswith(("!", "#", "[")):
        return None

    # Hosts format: 0.0.0.0 domain.com or 127.0.0.1 domain.com
    if line.startswith(("0.0.0.0", "127.0.0.1")):
        parts = line.split()
        return parts[1] if len(parts) >= 2 else None

    # ABP network filter: ||domain.com^$options
    match = _ABP_NETWORK_RE.match(line)
    if match:
        return match.group(1)

    return None


def convert(input_path: str, output_path: str | None, fmt: str, check: bool = False) -> bool:
    """
    Convert input file to the specified format.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file (None for --check mode)
        fmt: Output format name
        check: If True, validate without writing output
        
    Returns:
        True if conversion succeeded, False if errors found
    """
    formatter = FORMATS[fmt]
    seen_domains: set[str] = set()
    skipped_lines = 0
    duplicate_count = 0
    unparsed_lines: list[tuple[int, str]] = []
    has_errors = False

    print(f"Converting {input_path} -> {output_path or '(check mode)'} (format: {fmt})")

    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            lines = infile.readlines()
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return False
    except OSError as e:
        print(f"Error: {e}", file=sys.stderr)
        return False

    outfile = None
    if not check and output_path:
        try:
            outfile = open(output_path, "w", encoding="utf-8")
        except OSError as e:
            print(f"Error: {e}", file=sys.stderr)
            return False

    try:
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()

            if not stripped:
                continue

            # Preserve comments and headers, converting ! to # for DNS formats
            if stripped.startswith(("!", "#")):
                if outfile:
                    if stripped.startswith("!"):
                        stripped = "#" + stripped[1:]
                    outfile.write(stripped + "\n")
                continue

            domain = extract_domain(stripped)
            if domain:
                if domain in seen_domains:
                    duplicate_count += 1
                    continue
                seen_domains.add(domain)
                if outfile:
                    outfile.write(formatter(domain) + "\n")
            else:
                skipped_lines += 1
                # Track lines that look like ABP rules but couldn't be parsed
                if _ABP_LIKE_RE.match(stripped):
                    unparsed_lines.append((line_num, stripped))
    finally:
        if outfile:
            outfile.close()

    # Print summary
    print(f"  Domains processed: {len(seen_domains)}")
    if duplicate_count > 0:
        print(f"  Duplicates removed: {duplicate_count}")
    if skipped_lines > 0:
        print(f"  Lines skipped: {skipped_lines}")
    if unparsed_lines:
        print(f"  Warning: {len(unparsed_lines)} line(s) look like ABP rules but couldn't be parsed:")
        for line_num, line_text in unparsed_lines[:10]:  # Show first 10
            print(f"    Line {line_num}: {line_text}")
        if len(unparsed_lines) > 10:
            print(f"    ... and {len(unparsed_lines) - 10} more")

    # Validate output
    if not check and output_path:
        if len(seen_domains) == 0:
            print("Error: No domains found in input file", file=sys.stderr)
            has_errors = True

    if unparsed_lines:
        has_errors = True

    return not has_errors


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert ABP/hosts files to DNS blocker formats."
    )
    parser.add_argument(
        "--format",
        required=True,
        choices=FORMATS.keys(),
        metavar="FORMAT",
        help=f"Output format: {', '.join(FORMATS.keys())}",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate input file without producing output",
    )
    parser.add_argument("input", help="Input file (ABP or hosts format)")
    parser.add_argument("output", nargs="?", help="Output file (not required with --check)")
    args = parser.parse_args()

    if not args.check and not args.output:
        parser.error("output argument is required when --check is not used")

    success = convert(args.input, args.output, args.format, args.check)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
