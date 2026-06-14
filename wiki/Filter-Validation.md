# Filter Validation

ABPindo includes automated filter syntax validation to catch errors before they reach production.

## Overview

The validation tool checks for:

- **Invalid characters** — Non-printable characters, zero-width spaces, BOM markers
- **Malformed network filters** — Broken domain anchors, invalid patterns, unclosed regex
- **Invalid element hiding rules** — Unclosed parentheses, invalid CSS selectors
- **Unknown filter options** — Deprecated or misspelled options
- **Scriptlet injection errors** — Invalid scriptlet names, malformed arguments
- **Extended CSS issues** — Unmatched parentheses, invalid pseudo-selectors

## Usage

### Command Line

```bash
# Validate a single file
python tools/validate_filters.py src/advert/adservers.txt

# Validate all filters
python tools/validate_filters.py src/

# Strict mode (warnings become errors)
python tools/validate_filters.py --strict src/

# JSON output
python tools/validate_filters.py --json src/
```

### Pre-commit Hook

Install the pre-commit hook to validate automatically before each commit:

```bash
cp tools/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

### CI/CD

Validation runs automatically:

- **On PR** — Validates all changed filter files
- **On push to master** — Validates before building
- **Weekly** — Full validation of all filters

## Error Severity

| Level | Description | Action Required |
|-------|-------------|-----------------|
| **error** | Syntax error that will break the filter | Must fix before merge |
| **warning** | Potential issue or deprecated syntax | Recommended to fix |

## Common Errors

### Invalid Domain Pattern
```
Error: Invalid domain pattern
Rule: ||^$third-party
Fix:  ||example.com^$third-party
```

### Unmatched Parentheses
```
Error: Unmatched opening parenthesis
Rule: example.com##+js(set, timeout, 1000
Fix:  example.com##+js(set, timeout, 1000)
```

### Unknown Scriptlet
```
Warning: Unknown scriptlet: invalid-scriptlet
Rule: example.com##+js(invalid-scriptlet)
Fix:  Use a valid scriptlet name from the documentation
```

## Integration with Tools

### FOP (Filter Orderer and Preener)
FOP runs before validation to sort and clean filter files. The validator then checks the cleaned output.

### CI Pipeline
```
Source Files → FOP → Validator → Build → Output
```

## Adding Custom Checks

To add new validation rules, edit `tools/validate_filters.py`:

1. Add the check to the appropriate `validate_*` method
2. Use `self.add_error()` to report issues
3. Update `VALID_*` constants for new options/selectors
