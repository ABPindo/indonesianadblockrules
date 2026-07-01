# ABPindo Architecture

This document describes the technical architecture, build pipeline, and design decisions behind ABPindo.

---

## Table of Contents

- [Overview](#overview)
- [Repository Structure](#repository-structure)
- [Build Pipeline](#build-pipeline)
- [CI/CD Workflows](#cicd-workflows)
- [Design Decisions](#design-decisions)
- [Adding New Components](#adding-new-components)

---

## Overview

ABPindo is a filter list project that converts source filter rules into multiple distribution formats for different ad-blocking platforms. The architecture is designed for:

- **Simplicity**: Plain text source files, minimal build tooling
- **Portability**: ABP syntax first, uBO extended when needed
- **Automation**: CI/CD handles validation, building, and publishing
- **Multi-format**: Single source → 21 output formats (ABP + DNS variants)

---

## Repository Structure

```
indonesianadblockrules/
├── src/                          # Source filter files (hand-edited)
│   ├── advert/                   # Ad-blocking rules
│   │   ├── adservers.txt         # Third-party ad domains (||domain^$third-party)
│   │   ├── thirdparty.txt        # Third-party resource patterns
│   │   ├── general_block.txt     # Generic network blocks (paths)
│   │   ├── general_hide.txt      # Generic cosmetic filters (##)
│   │   ├── specific_block.txt    # Site-specific network blocks
│   │   ├── specific_hide.txt     # Site-specific cosmetic + extended CSS
│   │   ├── scriptlet_ublock.txt  # uBO-only scriptlet injections (##+js)
│   │   └── allowlist.txt         # Exception rules (@@, #@#)
│   ├── adult/                    # Adult/gambling domain blocks
│   │   ├── adult_general_block.txt
│   │   ├── adult_general_hide.txt
│   │   ├── adult_specific_block.txt
│   │   ├── adult_specific_hide.txt
│   │   ├── adult_thirdparty.txt
│   │   ├── adult_allowlist.txt
│   │   └── adult_prank.txt
│   ├── annoyances.txt            # Non-ad UI annoyances (popups, autoplays)
│   ├── advert_extended.txt       # Experimental/legacy ad rules
│   └── adult_extended.txt        # Experimental/legacy adult rules
│
├── *.template                    # flrender templates (define subscription variants)
│   ├── abpindo.template          # Full list (ads + adult)
│   ├── abpindo_noadult.template  # Ads only
│   ├── abpindo_noelemhide.template # Network blocks only
│   ├── abpindo_annoyances.template # Annoyances only
│   ├── abpindo_extended.template # Experimental rules
│   ├── abpindo_hosts.template    # Hosts format (domain blocks)
│   └── abpindo_hosts_adult.template # Hosts + adult
│
├── subscriptions/                # Build output (generated, committed by CI)
│   ├── abpindo.txt               # 7 ABP-format subscriptions
│   ├── hosts.txt                 # 14 DNS-format subscriptions
│   └── ...
│
├── tools/                        # Build and validation scripts
│   ├── build.sh                  # Main build script (ABP + DNS)
│   ├── lint.sh / lint.ps1        # AGLint runner
│   ├── dns_converter.py          # ABP → DNS format converter
│   ├── find_duplicates.py        # Cross-file duplicate detector
│   └── install_tools.sh          # Dependency installer
│
├── .github/                      # CI/CD and GitHub config
│   ├── workflows/
│   │   ├── validate-filters.yml  # PR validation (lint + duplicates)
│   │   ├── autobuild.yml         # Auto-build on push to master
│   │   ├── dead-domain-*.yml     # Dead domain detection
│   │   └── dependabot-automerge.yml
│   ├── actions/setup-tools/      # Composite action for Python + Node setup
│   └── ISSUE_TEMPLATE/           # Issue forms (bug, false positive)
│
├── wiki/                         # GitHub wiki documentation
├── .aglintrc.yaml                # AGLint config (extends aglint:recommended)
├── .aglintignore                 # Files AGLint skips
├── package.json                  # npm scripts (lint, build, check)
└── README.md / README.en.md      # User documentation
```

---

## Build Pipeline

The build pipeline transforms source filters into multiple distribution formats:

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. SOURCE FILTERS (src/)                                        │
│    Hand-written ABP and uBO filter rules                        │
└───────────────────┬─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. VALIDATION                                                    │
│    • AGLint (syntax check)                                      │
│    • find_duplicates.py (cross-file duplicate detection)        │
│    • FOP (formatter, auto-sorts rules)                          │
└───────────────────┬─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. ABP SUBSCRIPTION BUILD (flrender)                            │
│    • Reads *.template files                                     │
│    • %include abpindo:src/path/file.txt% directive pulls source │
│    • %timestamp% macro replaced with build time                 │
│    • Output: subscriptions/abpindo*.txt (7 variants)            │
└───────────────────┬─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. DNS FORMAT CONVERSION (dns_converter.py)                     │
│    • Parses ABP hosts files (abpindo_hosts*.txt)                │
│    • Extracts domains from ||domain^$third-party patterns       │
│    • Converts to 8 DNS formats:                                 │
│      - hosts (0.0.0.0 domain.com)                               │
│      - plain (domain.com)                                       │
│      - aghome (||domain^)                                       │
│      - dnsmasq_address (address=/domain/0.0.0.0)                │
│      - dnsmasq_server (server=/domain/)                         │
│      - rpz (domain CNAME .)                                     │
│      - unbound (local-zone: "domain" always_nxdomain)           │
│    • Output: subscriptions/*.txt (14 DNS variants)              │
└───────────────────┬─────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. COMMIT & PUSH (CI only)                                      │
│    • github-actions[bot] commits subscriptions/ to master       │
│    • [skip ci] flag prevents infinite loop                      │
│    • Users subscribe to raw GitHub URLs                         │
└─────────────────────────────────────────────────────────────────┘
```

### Local Development Workflow

```bash
# 1. Edit source filters
vim src/advert/specific_hide.txt

# 2. Validate
npm run lint                # AGLint syntax check
npm run check:duplicates    # Duplicate detection

# 3. Build (optional, CI will do this)
npm run build               # Full build (ABP + DNS)
npm run build:abp           # ABP only
npm run build:dns           # DNS only (requires ABP hosts files first)

# 4. Test manually
# Load subscriptions/abpindo.txt in your ad blocker's dev mode

# 5. Commit
git add src/
git commit -m "A: https://example.com — block sidebar ads"
git push
```

---

## CI/CD Workflows

### 1. `validate-filters.yml`
**Trigger**: PR to master, push to master (src/ changes only)  
**Purpose**: Validate filter syntax and detect duplicates before merge

**Steps**:
1. Checkout code
2. Setup tools (Python 3.x, Node 22.x, AGLint)
3. Run `bash tools/lint.sh` (AGLint on all src/**/*.txt)
4. Run `python tools/find_duplicates.py --strict` (exit 1 if duplicates found)
5. Generate report summary

**Exit conditions**:
- ❌ Fail: AGLint errors, duplicates found
- ✅ Pass: All checks green

---

### 2. `autobuild.yml`
**Trigger**: Push to master (src/ changes only), manual dispatch  
**Purpose**: Build all subscription files and commit them back to master

**Steps**:
1. Checkout code
2. Setup tools (Python 3.x, Node 22.x, fop-cli, AGLint, python-abp)
3. Run FOP (auto-format src/)
4. Run AGLint (validation)
5. Build ABP subscriptions via flrender (7 variants)
6. Build DNS subscriptions via dns_converter.py (14 variants)
7. Commit subscriptions/ back to master with `[skip ci]` flag
8. Push to origin/master

**Exit conditions**:
- ❌ Fail: Build errors, flrender errors, python errors
- ✅ Pass: Subscriptions committed successfully

---

### 3. `dead-domain-export.yml` & `dead-domain-import.yml`
**Trigger**: Manual dispatch (weekly cron suggested)  
**Purpose**: Detect and remove dead domains to keep filters lean

**Flow**:
1. Export: Extract domains from ABP hosts files → dead_domains.txt
2. External process (PyFunceble or AdGuard DeadDomainsLinter) checks liveness
3. Import: Read dead_domains.txt, move dead rules to `advert_extended.txt`

**Note**: Currently manual — can be automated with cron.

---

### 4. `dependabot-automerge.yml`
**Trigger**: Dependabot PR created  
**Purpose**: Auto-merge dependency updates after checks pass

---

## Design Decisions

### Why ABP Syntax First, uBO Extended Second?

**Decision**: Use Adblock Plus simple syntax as the default. Use uBlock Origin extended syntax (`##+js()`, `##^`, `:upward()`, etc.) only when ABP cannot express the rule.

**Rationale**:
- **Portability**: ABP syntax works in ABP, uBO, AdGuard, Brave, etc. — widest compatibility
- **Simplicity**: Simpler rules are easier to debug and maintain
- **Avoid vendor lock-in**: uBO-only scriptlets reduce portability to AdGuard users

**Never use**:
- ❌ AdGuard scriptlets (`#%#//scriptlet(...)`) — AdGuard-only
- ❌ ABP snippet syntax (`#%#//snippet(...)`) — limited adoption

**Implementation**:
- uBO-only rules go in `src/advert/scriptlet_ublock.txt`
- ABP users see them as comments (safe to ignore)
- uBO users get full scriptlet support

---

### Why Commit Built Subscriptions to Git?

**Decision**: `subscriptions/` is committed and tracked in git, not gitignored.

**Rationale**:
- **Zero-dependency distribution**: Users subscribe to raw GitHub URLs, no CDN/build server needed
- **Atomic history**: Every source change has corresponding subscription snapshot
- **Rollback safety**: Easy to revert bad builds
- **GitLab mirror works**: GitLab CI doesn't need to rebuild, just mirrors

**Tradeoff**: Larger repo size (21 subscriptions × history), but manageable (<100MB total).

---

### Why Multiple DNS Formats?

**Decision**: Support 8 DNS blocker formats (hosts, plain, dnsmasq, RPZ, etc.) from single source.

**Rationale**:
- **User diversity**: Pi-Hole uses hosts, AdGuard Home uses adblock syntax, Unbound uses RPZ
- **Zero maintenance**: `dns_converter.py` auto-generates from ABP hosts files
- **Single source of truth**: `src/advert/adservers.txt` → all DNS formats stay in sync

---

### Why Split `src/advert/` into Multiple Files?

**Decision**: 8 files (`adservers.txt`, `thirdparty.txt`, `general_block.txt`, etc.) instead of one monolithic file.

**Rationale**:
- **Clarity**: Clear placement rules (see `adblock-filter-dev` skill)
- **Selective inclusion**: Templates can include/exclude categories (e.g., `noelemhide` skips `*_hide.txt`)
- **Merge conflict reduction**: Contributors work on different files
- **Performance**: AGLint runs faster on smaller files

---

## Adding New Components

### Adding a New Subscription Variant

**Example**: Create `abpindo_lite.template` for mobile users (network blocks only, no cosmetic).

**Steps**:
1. Create `abpindo_lite.template` in repo root:
   ```
   [Adblock Plus 2.0]
   ! Title: ABPindo Lite (Network Blocks Only)
   ! Last modified: %timestamp%
   ! Expires: 4 days
   %include abpindo:src/advert/adservers.txt%
   %include abpindo:src/advert/thirdparty.txt%
   %include abpindo:src/advert/general_block.txt%
   %include abpindo:src/advert/specific_block.txt%
   %include abpindo:src/advert/scriptlet_ublock.txt%
   %include abpindo:src/advert/allowlist.txt%
   ```

2. Edit `tools/build.sh`, add line to `build_abp()`:
   ```bash
   flrender -i abpindo=. abpindo_lite.template "subscriptions/abpindo_lite.txt"
   ```

3. Edit `.github/workflows/autobuild.yml`, add line to "Build ABP subscriptions" step:
   ```yaml
   flrender -i abpindo=. abpindo_lite.template subscriptions/abpindo_lite.txt
   ```

4. Update `README.md` subscription table with new variant

5. Test locally: `npm run build:abp`

6. Commit template, build script, workflow, and README together

---

### Adding a New DNS Format

**Example**: Add DNSCrypt blocklist format.

**Steps**:
1. Edit `tools/dns_converter.py`, add format to `FORMATS` dict:
   ```python
   FORMATS = {
       # ... existing formats ...
       "dnscrypt": lambda d: f"*://*.{d}/*",  # DNSCrypt pattern
   }
   ```

2. Edit `tools/build.sh`, add conversion calls to `build_dns()`:
   ```bash
   python tools/dns_converter.py --format dnscrypt subscriptions/hosts.txt subscriptions/dnscrypt.txt
   python tools/dns_converter.py --format dnscrypt subscriptions/hosts_adult.txt subscriptions/dnscrypt_adult.txt
   ```

3. Edit `.github/workflows/autobuild.yml`, add conversion steps:
   ```yaml
   python tools/dns_converter.py --format dnscrypt subscriptions/hosts.txt subscriptions/dnscrypt.txt
   python tools/dns_converter.py --format dnscrypt subscriptions/hosts_adult.txt subscriptions/dnscrypt_adult.txt
   ```

4. Update `README.md` DNS format table

5. Test locally: `npm run build:dns`

---

### Adding a New Source Filter File

**Example**: Add `src/advert/chinese_ads.txt` for Indonesian sites serving Chinese ads.

**Steps**:
1. Create `src/advert/chinese_ads.txt` with rules

2. Edit relevant templates to include it:
   ```
   %include abpindo:src/advert/chinese_ads.txt%
   ```

3. AGLint will auto-discover it (runs on `src/**/*.txt`)

4. `find_duplicates.py` will auto-check it

5. No workflow changes needed

---

## Performance Considerations

### Filter Count vs Execution Speed

- **Network rules** are fast (O(1) hash lookups in most engines)
- **Cosmetic filters** (`##`) are moderate (DOM query on page load)
- **Procedural cosmetic filters** (`#?#`, `:has()`, `:upward()`) are slow (run on every DOM mutation)

**Guidelines**:
- Prefer network blocks over cosmetic filters when possible
- Prefer simple `##` selectors over procedural `#?#`
- Use procedural filters only when static CSS selectors can't express the rule
- Limit per-site procedural filters to <10 (performance impact on slow devices)

### Build Time

Current build takes ~30-60 seconds in CI:
- AGLint: ~5s (18 files, 10k rules)
- flrender: ~10s (7 ABP variants)
- dns_converter.py: ~15s (14 DNS variants)
- Commit + push: ~10s

**Optimization opportunities**:
- Cache `node_modules/` in CI (already done via setup-tools action)
- Parallelize DNS conversions (currently sequential)

---

## Troubleshooting

### "AGLint errors on valid rules"

**Symptom**: PR fails validation, but rules look correct.

**Solution**:
1. Check `.aglintrc.yaml` syntax setting (should be `AdblockPlus`)
2. Verify rule is valid ABP or uBO syntax (not AdGuard-specific)
3. Check for hidden characters (BOM, CRLF on Windows)
4. Run locally: `npm run lint` for full output

---

### "Build succeeds but filters don't work"

**Symptom**: CI green, but ads not blocked in browser.

**Solution**:
1. Check filter is in correct source file (network vs cosmetic)
2. Verify template includes that source file
3. Clear browser's filter cache and force update
4. Check browser console for CSP errors (scriptlets may be blocked)
5. Test in uBO Logger (shows which rules fired)

---

### "Merge conflicts in subscriptions/"

**Symptom**: PR has conflicts in generated `subscriptions/*.txt` files.

**Solution**:
1. **Never manually resolve conflicts in subscriptions/**.
2. Rebase your branch on latest master: `git rebase origin/master`
3. Resolve conflicts in `src/` only
4. Let CI regenerate `subscriptions/` cleanly

---

## References

- [flrender (python-abp)](https://github.com/adblockplus/python-abp) — ABP subscription renderer
- [AGLint](https://github.com/AdguardTeam/AGLint) — Filter list linter
- [FOP (Filter Orderer and Prettifier)](https://github.com/realodix/AdBlockFilterTools) — Filter formatter
- [uBlock Origin filter syntax](https://github.com/gorhill/uBlock/wiki/Static-filter-syntax)
- [Adblock Plus filter syntax](https://help.eyeo.com/en/adblockplus/how-to-write-filters)

---

**Maintained by**: ABPindo contributors  
**Last updated**: 2026-07-01
