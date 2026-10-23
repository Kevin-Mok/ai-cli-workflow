# Trim baseline validation and path lookup

The trim preflight found inherited validation defects and two stale skill paths.
Record the evidence before remediation, preserve unrelated failures and keep raw
logs outside this public tree.

## Symptom, Impact And Evidence
Two exploratory cat lookups used nonexistent skill paths; exact catalog paths
were then read successfully. No product files changed. Focused baseline tests
had 3 failures/35 passes/33 passing subtests; the full suite failed collection
with 6 SyntaxErrors in sanitized hyphenated test names. This prevents an honest
whole-suite green claim before trim work begins.

## Lookup
Query: `skill path missing file`. Installed read-only helper returned
`local-discover-paths-before-reads` (verified_workaround): use catalog paths and
check optional file existence. Applicable to the read errors; actual paths were
confirmed from the current skill catalog. It does not remedy inherited tests.

## Current Status And Next Steps
Path lookup resolved. Baseline test defects remain documented in the ExecPlan;
fix only requirements within trim scope and report unrelated test limitations.
Raw logs: `/tmp/trim-baseline-tests-focused.log` and
`/tmp/trim-baseline-tests-suite.log`; do not publish diagnostic identifiers.

## Cause, Resolution And Verification
Lookup cause: guessed install paths instead of the supplied skill roots.
Resolution: use full catalog paths; successful subsequent reads verified it.
Tests: inherited source/test drift, not introduced by trim; no resolution claimed.

Two later multi-file patches were rejected because context lines were stale;
no portion applied. Targeted source reads confirmed that state before retry.
Use current file context and separate unrelated hunks; the existing path/source
discovery finding applies. No product regression or new general remedy.

## Learning
Existing path-discovery guidance applies; no new general lesson. The canonical
learning ledger at `/home/kevin/linux-config/dot_agents/skills/postmortem-memory/`
is outside this task's permitted write roots. Its hash/alias update is outstanding;
no installed copy was edited. Record this limitation in the final handoff.

## Additional preparation diagnostics

Trigger-eval test authoring initially rejected a harmless case ID containing
`prompt`; the assertion needed to forbid prompt fields/text, not arbitrary
substrings. The focused suite now passes after that fixture correction.
A mining helper lookup guessed a nested location; the actual helper is
`scripts/codex_search_index.py`. Existing path-discovery guidance applies.
A third no-op patch probe used mismatched capitalization and was rejected
without edits; source reads preceded corrected edits. No new product remedy.
These preparation diagnostics remain separate from inherited baseline failures.

Another plan patch included an unnecessary guessed no-op context hunk and
was rejected atomically. The amendment was appended only after confirming that
no earlier hunk applied. Repeated context-probe failures share the existing
source-verification cause; avoid speculative trailing hunks.

During cull-only verification, a test invocation guessed
`tests/test_commit_plan_push.py`; the actual path is
`tests/test_commit_plan_push_skill.py`. The first run exited 4 without tests;
the corrected focused run passed 72 tests and 34 subtests. A calibration probe
also guessed a nonexistent manifest name; the existing `CULL.json` was then
used. No source change resulted from either probe. Existing path-discovery
guidance applies; no new general learning or false test claim is recorded.

## Cull provenance audit finding

A fresh AI-workflow doctor run (exit 0 without --check, summary status fail)
found one newly introduced finding: context-handoff is marked adapted but lacks
SOURCE.md. Total errors dropped from38 to36, but that does not excuse the new
provenance omission. Current status: investigate the copied source/merge lineage,
add an accurate provenance record, then rerun the doctor and relevant contracts.
No original source, installed copy or machine configuration was changed.

Additional provenance lookup probes assumed an absent brand SOURCE.md and
a split doctor module, and used an unsupported postmortem helper subcommand.
These read-only probes failed without changing product files. The actual
executable doctor and helper usage were then read directly; use discovered
paths and declared subcommands. This repeats the known path-discovery lesson.

Provenance lookup `doctor provenance baseline` matched
`local-doctor-provenance-baseline` (unresolved): compare exact findings, preserve
unrelated lineage and add no new objective failures. Applicable diagnostic, not
an existing repair. SOURCE.md now traces the actual pinned harness input and
the separately hashed installed template without publishing a private archive
path or asserting independently verified earlier lineage. Fresh doctor comparison
is required to establish resolution.

Fresh doctor after provenance repair:35 errors/1 warning,0 new finding keys
against the saved pass-0 baseline (38 errors/1 warning). The new context-handoff
missing-provenance finding is resolved; unrelated findings remain. Cause: the
merge copied the adapted marker/template but omitted its lineage record. The
SOURCE.md repair records actual pinned input plus the installed-template hash;
no doctor check was weakened and no full clean audit is claimed.

The first staged whitespace check exposed a trailing blank line in the new
trim-benchmark file, which earlier unstaged diff checks did not inspect. Removed
only the extra EOF whitespace; executable logic is unchanged. Recheck the exact
staged diff before privacy validation and commit.

An intake calibration edit asserted an incorrect heading depth before writing
any file; the authoritative headings were then inspected. Correct the targeted
section match rather than guessing. Existing source/context discovery guidance
applies. The generic skill validator's unsupported disable-model-invocation
error matches the already-reviewed2026-10-21-sire-session-validation incident;
retain valid invocation metadata and use repository contract checks.

Two pass2 benchmark tests initially read budgets before their coordinated update
completed. After the final freeze, the targeted2 and full192-test/231-subtest
run pass. This is preparation ordering, not a product regression. Run budget
checks only after the owned budget snapshot is final.

Staged intake whitespace review found inherited formatting in pinned vendor
reference files (including intentional Markdown hard breaks), plus one extra
EOF blank line in the newly moved shadcn workflow. The authored EOF was removed.
Preserve pinned upstream bytes/hashes and check authored changes separately;
upstream formatting warnings do not establish a runtime or privacy defect.

### Admission candidate size check

The first pass3 staged size check rejected the existing long vetted reference:
resolving its pending intake hash to the real40-character SHA adds20bytes.
No source/calibration content was lost. The user explicitly allows the on-demand
reference to be long; freeze its exact reviewed size as an existing-file ceiling
in file-size-guard.json, then rerun the staged guard and privacy gate. This is
not a wildcard exemption and does not allow a new oversized authored file.

Admission size resolution: exact existing-reference ceiling102,846B accepted
the20-byte real-SHA substitution; staged size and privacy gates passed before
6e9934c7. CASD discovery also passed unmatched test-name globs to rg; no files
changed, and rg --files supplied the actual names. This repeats the known
source-discovery lesson, not a new product failure. Canonical learning-ledger
writes remain outside permitted roots; tracked-source registration outstanding.

CASD source-contract verification: postmortem-memory suite25PASS/1inherited
environment failure at test_actual_ledger_reference_status_and_coverage because
public /home/example fixture roots/ledger reports are unavailable. The changed
relocated-policy assertion passes. Do not repair private fixture availability or
claim the complete suite green; CASD block retention independently checks policy.
The PMlookup query staged-file-size-guard/existing-reference-ceiling returned
no directly applicable remedy; the exact user-authorized long-reference ceiling
was independently reviewed. Canonical helper check still reports this living
report new/unregistered; its external tracked ledger is outside writable roots.

CASD final review added28router bytes after a test worker had already started;
198tests/330subtests passed but2budget assertions saw the old ceiling. Frozen
source now16,127loadedB; root benchmarkPASS. Rerun after confirming that value,
not while its owner is updating it. Same preparation-ordering lesson as pass2.

Fresh post-intake/CASD workflow doctor returns39errors/1warning, with4new
invalid_source_provenance findings: grok-cli-handoff, skill-eval, shadcn and
impeccable. Source text exists, but imported notes lack the doctor's exact
repository/path/revision/basis field names and use punctuated dates. This repeats
the known local-doctor-provenance-baseline issue. Keep body pass focused; correct
structured provenance as a separate follow-up, using true pinned upstream paths
or accepted local intake blobs, without publishing private repo locations.
Do not weaken the doctor or claim zero-new-findings until that rerun passes.

A read-only description preflight assumed report key results instead of the
declared per_case field and raised KeyError. No source changed; inspect the
returned schema before consuming reports. Same source-inspection lesson.

Description preflight also assumed per-case predicted rather than actual;
read the evaluator construction before any further schema use. No source changed.
