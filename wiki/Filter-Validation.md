# Filter Validation

ABPindo uses [AGLint](https://github.com/AdguardTeam/AGLint) for automated filter syntax validation.

## Overview

AGLint checks for:

- **Invalid modifiers** — Unknown or misplaced filter options
- **Invalid CSS syntax** — Malformed element hiding selectors
- **Invalid domains** — Incorrect domain patterns in rules
- **Duplicated modifiers** — Same modifier used multiple times
- **Unknown preprocessor directives** — Invalid `!#if`, `!#endif` usage

## Usage

### Command Line

```bash
# Install dependencies (pertama kali saja)
npm install

# Validate all filters
npm run lint

# Validate specific directory
npx aglint src/advert/*.txt

# Auto-fix issues (careful: overwrites files)
npx aglint 'src/**/*.txt' --fix
```

### CI/CD

Validation runs automatically:

- **On PR** — Validates all filter files, fails on errors
- **On push to master** — Validates before building

## Configuration

AGLint is configured via `.aglintrc.yaml`:

```yaml
root: true
extends:
  - aglint:recommended
syntax:
  - AdblockPlus
rules:
  invalid-modifiers: error
  no-invalid-css-syntax: error
  invalid-domain-list: warn
```

## Error Severity

| Level | Description | Action Required |
|-------|-------------|-----------------|
| **error** | Syntax error that will break the filter | Must fix before merge |
| **warning** | Potential issue or deprecated syntax | Recommended to fix |

## Inline Configuration

You can disable AGLint for specific rules:

```bash
# Disable for next line
! aglint-disable-next-line
example.com##.ad

# Disable for block
! aglint-disable
example.com##.ad
example.net##.ad
! aglint-enable
```

## CI Pipeline

```
Source Files → FOP → AGLint → Build → Output
```
