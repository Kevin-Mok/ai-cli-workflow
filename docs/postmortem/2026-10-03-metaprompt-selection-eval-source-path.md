# Public eval source path lookup

Date: 2026-10-03. Status: resolved.

Symptom: a read command requested `selection_lib.py`, which does not exist.
Impact: no benchmark requests, data changes or user work affected.
Evidence: `cat` reported the missing file; file inventory identified
`selection_core.py` as the actual accounting module.
Root cause: reused a guessed library name from the earlier benchmark.
Resolution: read the actual core and its durable budget/fixture contracts.
Verification: the corrected source read exited 0.
Follow-up: inventory new package filenames before requesting source paths.
