# Dead Domain Management

ABPindo uses [`@adguard/dead-domains-linter`](https://github.com/AdguardTeam/DeadDomainsLinter) for dead domain detection with a **two-phase workflow**.

## How It Works

```
1st of month:   Export dead domains → Review files created
1st-14th:       You review and remove false positives
15th of month:  Auto-import (if not reviewed)
```

## Workflows

| Workflow | Schedule | Action |
|----------|----------|--------|
| `dead-domain-export.yml` | 1st of month | Export dead domains to files |
| `dead-domain-import.yml` | 15th of month | Auto-import (if not reviewed) |

## Export Files

| File | Source |
|------|--------|
| `src/advert/dead_advert.txt` | Dead domains from advert filters |
| `src/adult/dead_adult.txt` | Dead domains from adult filters |

## Manual Review (Optional)

If you want to review before auto-import:

```bash
# 1. Open and review dead_advert.txt
#    - Remove lines that are false positives (domains that are alive)

# 2. Import reviewed list
dead-domains-linter -i "src/advert/*.txt" --import=src/advert/dead_advert.txt --auto

# 3. Open and review dead_adult.txt

# 4. Import reviewed list
dead-domains-linter -i "src/adult/*.txt" --import=src/adult/dead_adult.txt --auto

# 5. Commit
git add src/ && git commit -m "chore: remove reviewed dead domains"
```

## Manual Commands

```bash
# Export dead domains (scan only, no modification)
dead-domains-linter -i "src/advert/*.txt" --export src/advert/dead_advert.txt
dead-domains-linter -i "src/adult/*.txt" --export src/adult/dead_adult.txt

# Import and remove (after review)
dead-domains-linter -i "src/advert/*.txt" --import=src/advert/dead_advert.txt --auto
dead-domains-linter -i "src/adult/*.txt" --import=src/adult/dead_adult.txt --auto
```

## Timeline

| Date | What Happens |
|------|--------------|
| 1st | Export runs, commit created |
| 1st-14th | Review window |
| 15th | Auto-import runs (if files have content) |

## Best Practices

- Review `dead_advert.txt` and `dead_adult.txt` when you see the export commit
- Remove false positives before the 15th
- If you import manually early, the auto-import will find nothing to do
