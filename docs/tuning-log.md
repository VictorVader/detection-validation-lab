# Tuning Log

## FP-001 — Encoded PowerShell rule
Broadened the rule to match any PowerShell process (dropped the `command_contains: -enc` check, left only `process_contains: powershell`).
Caused a false positive on `powershell.exe -Command Get-Service` in datasets/benign/baseline.jsonl.

**Fix:** require `-enc` in the command line, not just the process name.
**Result:** FP was removed, true positive on the encoded-command event remains unchanged.
**Regression test:** tests/cases/encoded_powershell.yml