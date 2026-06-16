#!/usr/bin/env python3
"""
validate_filters.py — Validate ABP/uBlock filter syntax.

Checks for:
- Invalid characters
- Malformed network filters
- Malformed element hiding rules
- Invalid filter options
- Syntax errors

Usage:
    python3 validate_filters.py src/advert/adservers.txt
    python3 validate_filters.py src/
    python3 validate_filters.py --strict src/
"""

import re
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass
from typing import Optional


@dataclass
class ValidationError:
    file: str
    line: int
    column: int
    severity: str  # error, warning
    message: str
    rule: str


# Valid filter options for network filters
VALID_NETWORK_OPTIONS = {
    # Resource types
    "script", "image", "stylesheet", "object", "subdocument", "xmlhttprequest",
    "font", "media", "websocket", "webtransport", "webrtc", "csp", "ping",
    "other", "document", "elemhide", "generichide", "genericblock",
    # Options
    "third-party", "1p", "3p", "rewrite", "domain", "sitekey",
    "csp", "redirect", "redirect-rule", "empty", "mp4", "object-subrequest",
    "all", "badfilter", "important", "denyallow", "to",
    # Modifiers
    "match-case", "collapse", "donottrack", "nobadfilter",
    # Exceptions
    "~third-party", "~1p", "~3p",
}

# Valid element hiding options
VALID_ELEMENT_OPTIONS = {
    "matches-css", "matches-css-before", "matches-css-after",
    "has", "has-text", "has-text", "not", "not-text",
    "upward", "remove", "replace", "read-text",
    "min-text-length", "max-text-length",
    "matches-attr", "matches-attr-before", "matches-attr-after",
    "xpath", "watch-attr", "is",
}

# Valid scriptlet names
VALID_SCRIPTLETS = {
    "abort-current-inline-script", "abort-current-script",
    "abort-on-property-read", "abort-on-property-write",
    "addEventListener-defuser", "addEventListener-defuser-before",
    "addEventListener-true-defuser", "addEventListener-true-defuser-before",
    "adjust-setTimeout", "adjust-setInterval",
    "call-outpoint", "call-sydney-ufunction",
    "clear-timeout", "clear-interval",
    "define-constant", "define-property-in-iface",
    "json-prune", "json-prune-safe",
    "log", "log-addEventListener",
    "no-alert", "no-eval-if", "no-request-id-if",
    "no-setTimeout-if", "no-setInterval-if",
    "no-window-open-if", "no-xhr-if",
    "object-prune", "prevent-adfly",
    "prevent-addEventListener", "prevent-defusing",
    "prevent-eval-if", "prevent-fetch",
    "prevent-setTimeout", "prevent-setInterval",
    "prevent-window-open", "proxy-replace",
    "read-node", "remove-attr", "remove-class",
    "replace-attr", "set-constant",
    "set-cookie", "set-cookie-reload",
    "spoof-css", "trusted-replace-node",
    "usercall", "userjs",
}

# Valid element hiding extended selectors
VALID_EXTENDED_SELECTORS = {"has", "has-text", "not", "not-text", "upward", "xpath"}


class FilterValidator:
    def __init__(self, strict: bool = False):
        self.strict = strict
        self.errors: list[ValidationError] = []
        self.stats = {
            "files": 0,
            "lines": 0,
            "comments": 0,
            "empty": 0,
            "network_filters": 0,
            "element_hiding": 0,
            "scriptlet_injection": 0,
            "extended_css": 0,
            "errors": 0,
            "warnings": 0,
        }

    def add_error(self, file: str, line: int, column: int, severity: str, message: str, rule: str):
        self.errors.append(ValidationError(file, line, column, severity, message, rule))
        if severity == "error":
            self.stats["errors"] += 1
        else:
            self.stats["warnings"] += 1

    def validate_file(self, filepath: Path) -> list[ValidationError]:
        """Validate a single filter file."""
        self.stats["files"] += 1
        file_errors = []

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
        except UnicodeDecodeError as e:
            self.add_error(str(filepath), 0, 0, "error", f"File encoding error: {e}", "")
            return self.errors

        lines = content.splitlines()
        for line_num, line in enumerate(lines, 1):
            self.stats["lines"] += 1
            stripped = line.strip()

            # Empty line
            if not stripped:
                self.stats["empty"] += 1
                continue

            # Comment
            if stripped.startswith("!") or stripped.startswith("["):
                self.stats["comments"] += 1
                continue

            # Validate the rule
            errors = self.validate_rule(stripped, str(filepath), line_num)
            file_errors.extend(errors)

        return file_errors

    def validate_rule(self, rule: str, file: str, line: int) -> list[ValidationError]:
        """Validate a single filter rule."""
        errors = []

        # Check for invalid characters
        invalid_chars = set()
        for i, char in enumerate(rule):
            if ord(char) < 32 and char not in ('\t', '\n', '\r'):
                invalid_chars.add((i, char))
            elif char in '\u200b\u200c\u200d\ufeff':
                invalid_chars.add((i, char))

        if invalid_chars:
            for col, char in invalid_chars:
                self.add_error(file, line, col, "error",
                    f"Invalid character: U+{ord(char):04X}", rule)

        # Skip if already has errors from invalid characters
        if any(e.line == line and e.severity == "error" for e in self.errors):
            return errors

        # Determine filter type and validate
        if rule.startswith("@@"):
            # Allowlist filter
            self.stats["network_filters"] += 1
            errors.extend(self.validate_network_filter(rule[2:], file, line, is_allowlist=True))
        elif rule.startswith("##"):
            # Element hiding (global)
            self.stats["element_hiding"] += 1
            errors.extend(self.validate_element_hiding(rule, file, line))
        elif rule.startswith("#@#"):
            # Element hiding exception (global)
            self.stats["element_hiding"] += 1
            errors.extend(self.validate_element_hiding_exception(rule, file, line))
        elif re.match(r"^[a-zA-Z0-9._-]+##", rule):
            # Site-specific element hiding
            self.stats["element_hiding"] += 1
            errors.extend(self.validate_site_specific_hiding(rule, file, line))
        elif re.match(r"^[a-zA-Z0-9._-]+#@#", rule):
            # Site-specific element hiding exception
            self.stats["element_hiding"] += 1
            errors.extend(self.validate_site_specific_exception(rule, file, line))
        elif re.match(r"^[a-zA-Z0-9._-]+##\+js\(", rule):
            # Scriptlet injection
            self.stats["scriptlet_injection"] += 1
            errors.extend(self.validate_scriptlet_injection(rule, file, line))
        elif re.match(r"^[a-zA-Z0-9._-]+##\^", rule):
            # HTML filtering (uBlock)
            self.stats["element_hiding"] += 1
            errors.extend(self.validate_html_filter(rule, file, line))
        else:
            # Network filter
            self.stats["network_filters"] += 1
            errors.extend(self.validate_network_filter(rule, file, line))

        return errors

    def validate_network_filter(self, rule: str, file: str, line: int, is_allowlist: bool = False) -> list[ValidationError]:
        """Validate a network filter rule."""
        errors = []
        prefix = "@@" if is_allowlist else ""

        # Find options separator
        options_start = -1
        in_domain = False
        i = 0
        while i < len(rule):
            if rule[i] == '$':
                # Check if this $ is inside a domain option
                options_part = rule[i+1:]
                if options_part.startswith("domain="):
                    in_domain = True
                    i += 8
                    continue
                elif in_domain and rule[i-1] != '|':
                    i += 1
                    continue
                else:
                    options_start = i
                    break
            i += 1

        if options_start > 0:
            options_str = rule[options_start+1:]
            pattern = rule[:options_start]
        else:
            options_str = ""
            pattern = rule

        # Validate pattern
        if not pattern:
            self.add_error(file, line, 1, "error", f"{prefix}Empty filter pattern", rule)
            return errors

        # Check for valid pattern syntax
        if pattern.startswith("||"):
            # Domain anchor
            domain = pattern[2:]
            if not domain:
                self.add_error(file, line, 3, "error", f"{prefix}Empty domain after ||", rule)
            elif not self.is_valid_domain_pattern(domain):
                self.add_error(file, line, 3, "warning", f"{prefix}Potentially invalid domain pattern", rule)
        elif pattern.startswith("|"):
            # Start anchor
            if len(pattern) < 2:
                self.add_error(file, line, 2, "error", f"{prefix}Empty pattern after |", rule)
        elif pattern.endswith("|"):
            # End anchor
            if len(pattern) < 2:
                self.add_error(file, line, len(pattern), "error", f"{prefix}Empty pattern before |", rule)
        elif pattern.startswith("/") and pattern.endswith("/"):
            # Regex
            try:
                re.compile(pattern[1:-1])
            except re.error as e:
                self.add_error(file, line, 1, "error", f"{prefix}Invalid regex: {e}", rule)
        elif not self.is_valid_url_pattern(pattern):
            self.add_error(file, line, 1, "warning", f"{prefix}Potentially invalid URL pattern", rule)

        # Validate options
        if options_str:
            errors.extend(self.validate_options(options_str, file, line, prefix))

        return errors

    def validate_options(self, options_str: str, file: str, line: int, prefix: str = "") -> list[ValidationError]:
        """Validate filter options."""
        errors = []
        options = self.parse_options(options_str)

        for opt_name, opt_value in options.items():
            if opt_name not in VALID_NETWORK_OPTIONS:
                if self.strict:
                    self.add_error(file, line, options_str.find(opt_name) + 1, "error",
                        f"{prefix}Unknown option: {opt_name}", options_str)
                else:
                    self.add_error(file, line, options_str.find(opt_name) + 1, "warning",
                        f"{prefix}Unknown or deprecated option: {opt_name}", options_str)

            # Validate specific options
            if opt_name == "domain" and opt_value:
                domains = opt_value.split("|")
                for domain in domains:
                    domain = domain.lstrip("~")
                    if domain and not self.is_valid_domain(domain):
                        self.add_error(file, line, options_str.find(domain) + 1, "warning",
                            f"{prefix}Invalid domain in option: {domain}", options_str)

            if opt_name == "redirect" and opt_value:
                # Redirect resource names should be valid
                if not re.match(r'^[a-zA-Z0-9_-]+$', opt_value):
                    self.add_error(file, line, options_str.find(opt_value) + 1, "warning",
                        f"{prefix}Invalid redirect resource name: {opt_value}", options_str)

        return errors

    def parse_options(self, options_str: str) -> dict:
        """Parse filter options string."""
        options = {}
        # Simple parser - handle domain= specially
        parts = options_str.split(",")
        domain_value = None
        i = 0
        while i < len(parts):
            part = parts[i].strip()
            if part.startswith("domain="):
                domain_value = part[8:]
                # Check for continuation in next parts
                while i + 1 < len(parts) and not parts[i+1].strip().split("=")[0] in VALID_NETWORK_OPTIONS:
                    i += 1
                    domain_value += "," + parts[i]
                options["domain"] = domain_value
            elif "=" in part:
                key, value = part.split("=", 1)
                options[key.strip()] = value.strip()
            elif part:
                options[part] = None
            i += 1
        return options

    def validate_element_hiding(self, rule: str, file: str, line: int) -> list[ValidationError]:
        """Validate global element hiding rule."""
        errors = []
        selector = rule[2:]  # Remove ##

        if not selector:
            self.add_error(file, line, 3, "error", "Empty element hiding selector", rule)
            return errors

        # Check for invalid characters in selector
        if re.search(r'[!@#$%^&*()=+\[\]{};:"\'\\|<>?]', selector):
            # Some characters are valid in CSS selectors but might be issues
            pass

        # Validate CSS selector (basic check)
        if selector.startswith(".") or selector.startswith("#") or selector.startswith("["):
            # Valid CSS selector start
            pass
        elif re.match(r'^[a-zA-Z]', selector):
            # Tag name
            pass
        else:
            self.add_error(file, line, 3, "warning", "Selector may not be valid CSS", rule)

        return errors

    def validate_element_hiding_exception(self, rule: str, file: str, line: int) -> list[ValidationError]:
        """Validate global element hiding exception rule."""
        errors = []
        selector = rule[3:]  # Remove #@

        if not selector:
            self.add_error(file, line, 4, "error", "Empty element hiding exception selector", rule)

        return errors

    def validate_site_specific_hiding(self, rule: str, file: str, line: int) -> list[ValidationError]:
        """Validate site-specific element hiding rule."""
        errors = []

        # Extract domain and selector
        match = re.match(r'^([a-zA-Z0-9._-]+)(##|#@\?#|#@#)(.*)', rule)
        if not match:
            self.add_error(file, line, 1, "error", "Invalid site-specific hiding syntax", rule)
            return errors

        domain, operator, selector = match.groups()

        if not self.is_valid_domain(domain):
            self.add_error(file, line, 1, "warning", f"Invalid domain: {domain}", rule)

        if operator == "##":
            # Check for extended CSS selectors
            if ":has(" in selector or ":has-text(" in selector or ":not(" in selector:
                self.stats["extended_css"] += 1
                errors.extend(self.validate_extended_css(selector, file, line, rule))
            elif "#?#" in rule:
                self.stats["extended_css"] += 1
                errors.extend(self.validate_extended_css(selector, file, line, rule))
        elif operator == "#@?#":
            self.stats["extended_css"] += 1
            errors.extend(self.validate_extended_css(selector, file, line, rule))

        return errors

    def validate_site_specific_exception(self, rule: str, file: str, line: int) -> list[ValidationError]:
        """Validate site-specific element hiding exception rule."""
        errors = []

        match = re.match(r'^([a-zA-Z0-9._-]+)#@#(.*)', rule)
        if not match:
            self.add_error(file, line, 1, "error", "Invalid site-specific exception syntax", rule)
            return errors

        domain, selector = match.groups()

        if not self.is_valid_domain(domain):
            self.add_error(file, line, 1, "warning", f"Invalid domain: {domain}", rule)

        return errors

    def validate_scriptlet_injection(self, rule: str, file: str, line: int) -> list[ValidationError]:
        """Validate scriptlet injection rule."""
        errors = []

        match = re.match(r'^([a-zA-Z0-9._-]+)##\+js\((.+)\)$', rule)
        if not match:
            self.add_error(file, line, 1, "error", "Invalid scriptlet injection syntax", rule)
            return errors

        domain, scriptlet_part = match.groups()

        if not self.is_valid_domain(domain):
            self.add_error(file, line, 1, "warning", f"Invalid domain: {domain}", rule)

        # Parse scriptlet
        parts = self.parse_scriptlet_args(scriptlet_part)
        if not parts:
            self.add_error(file, line, rule.find("##") + 5, "error", "Empty scriptlet", rule)
            return errors

        scriptlet_name = parts[0]
        if scriptlet_name not in VALID_SCRIPTLETS:
            if self.strict:
                self.add_error(file, line, rule.find(scriptlet_name) + 1, "error",
                    f"Unknown scriptlet: {scriptlet_name}", rule)
            else:
                self.add_error(file, line, rule.find(scriptlet_name) + 1, "warning",
                    f"Unknown or custom scriptlet: {scriptlet_name}", rule)

        return errors

    def parse_scriptlet_args(self, scriptlet_str: str) -> list[str]:
        """Parse scriptlet arguments, handling commas inside quotes."""
        parts = []
        current = []
        in_single_quote = False
        in_double_quote = False
        escape_next = False

        for char in scriptlet_str:
            if escape_next:
                current.append(char)
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                current.append(char)
                continue
            if char == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
                current.append(char)
            elif char == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
                current.append(char)
            elif char == ',' and not in_single_quote and not in_double_quote:
                parts.append(''.join(current).strip())
                current = []
            else:
                current.append(char)

        if current:
            parts.append(''.join(current).strip())

        return parts

    def validate_extended_css(self, selector: str, file: str, line: int, rule: str) -> list[ValidationError]:
        """Validate extended CSS selector."""
        errors = []

        # Check for proper nesting of pseudo-selectors
        depth = 0
        for i, char in enumerate(selector):
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
                if depth < 0:
                    self.add_error(file, line, i + 1, "error", "Unmatched closing parenthesis", rule)
                    break
        if depth > 0:
            self.add_error(file, line, len(selector), "error", "Unmatched opening parenthesis", rule)

        return errors

    def validate_html_filter(self, rule: str, file: str, line: int) -> list[ValidationError]:
        """Validate HTML filtering rule (uBlock-specific)."""
        errors = []

        match = re.match(r'^([a-zA-Z0-9._-]+)##\^(.+)$', rule)
        if not match:
            self.add_error(file, line, 1, "error", "Invalid HTML filter syntax", rule)
            return errors

        domain, pattern = match.groups()

        if not self.is_valid_domain(domain):
            self.add_error(file, line, 1, "warning", f"Invalid domain: {domain}", rule)

        return errors

    def is_valid_domain_pattern(self, pattern: str) -> bool:
        """Check if domain pattern is valid."""
        # Remove wildcards
        clean = pattern.replace("*", "")
        if clean.startswith("."):
            clean = clean[1:]
        return self.is_valid_domain(clean) or clean == ""

    def is_valid_domain(self, domain: str) -> bool:
        """Check if domain is valid."""
        if not domain:
            return False
        # Basic domain validation
        domain_regex = re.compile(
            r'^([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)*[a-zA-Z]{2,}$'
        )
        return bool(domain_regex.match(domain))

    def is_valid_url_pattern(self, pattern: str) -> bool:
        """Check if URL pattern is valid."""
        # Very basic check - just ensure it's not obviously broken
        if not pattern:
            return False
        # Check for balanced parentheses
        depth = 0
        for char in pattern:
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            if depth < 0:
                return False
        return depth == 0

    def validate_directory(self, dirpath: Path) -> list[ValidationError]:
        """Validate all filter files in a directory."""
        errors = []

        for file in sorted(dirpath.rglob("*.txt")):
            file_errors = self.validate_file(file)
            errors.extend(file_errors)

        return errors

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Files scanned:    {self.stats['files']}")
        print(f"Total lines:      {self.stats['lines']}")
        print(f"Comments:         {self.stats['comments']}")
        print(f"Empty lines:      {self.stats['empty']}")
        print(f"Network filters:  {self.stats['network_filters']}")
        print(f"Element hiding:   {self.stats['element_hiding']}")
        print(f"Scriptlet inject: {self.stats['scriptlet_injection']}")
        print(f"Extended CSS:     {self.stats['extended_css']}")
        print("-" * 60)
        print(f"Errors:           {self.stats['errors']}")
        print(f"Warnings:         {self.stats['warnings']}")
        print("=" * 60)

    def print_errors(self, errors: list[ValidationError]):
        """Print validation errors."""
        if not errors:
            print("\n[OK] No errors found!")
            return

        print(f"\nFound {len(errors)} issue(s):\n")

        for error in errors:
            severity_color = "\033[91m" if error.severity == "error" else "\033[93m"
            reset = "\033[0m"
            print(f"{severity_color}{error.severity.upper()}{reset}")
            print(f"  File:     {error.file}")
            print(f"  Line:     {error.line}:{error.column}")
            print(f"  Message:  {error.message}")
            print(f"  Rule:     {error.rule[:80]}{'...' if len(error.rule) > 80 else ''}")
            print()


def main():
    parser = argparse.ArgumentParser(
        description="Validate ABP/uBlock filter syntax."
    )
    parser.add_argument(
        "path",
        help="File or directory to validate"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON"
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )

    args = parser.parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"Error: Path not found: {path}", file=sys.stderr)
        sys.exit(1)

    validator = FilterValidator(strict=args.strict)

    if path.is_file():
        errors = validator.validate_file(path)
    elif path.is_dir():
        errors = validator.validate_directory(path)
    else:
        print(f"Error: Invalid path: {path}", file=sys.stderr)
        sys.exit(1)

    if args.json:
        import json
        output = {
            "stats": validator.stats,
            "errors": [
                {
                    "file": e.file,
                    "line": e.line,
                    "column": e.column,
                    "severity": e.severity,
                    "message": e.message,
                    "rule": e.rule[:100]
                }
                for e in errors
            ]
        }
        print(json.dumps(output, indent=2))
    else:
        validator.print_errors(errors)
        validator.print_summary()

    # Exit with error code if there are errors
    if validator.stats["errors"] > 0:
        sys.exit(1)
    elif args.strict and validator.stats["warnings"] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
