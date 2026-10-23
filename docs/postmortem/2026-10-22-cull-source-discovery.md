# Cull Source Discovery Failures

This report records read-only lookup failures during the approved skill cull.
It distinguishes absent repo sources from installed skills and records the
corrected inventory without treating a missing lookup as permission to delete.

## Symptom And Impact

A skill-document lookup used the wrong cache subdirectory. A combined read then
assumed context-handoff already had a repo-local source; it exists only in the
installed catalog. A later reference search named a nonexistent test file. The
repo-local postmortem helper rejected the installed skill's `--compact` option.
All commands were read-only; no user files, Git state or private inputs changed.

## Evidence And Current Status

- The skill cache uses `productivity/writing-for-agents`, not `engineering/`.
  Reading its actual catalog path succeeded.
- `rg --files` and `git ls-files` confirmed context-handoff had no tracked
  source. The parent explicitly authorized adding the installed source and
  merging the approved long-task procedure. Its provenance marker is retained.
- Enumerating test files replaced the guessed test path. No existing test was
  dropped because its path lookup failed.
- The local helper returned argparse exit 2 for `search ... --compact`;
  installed instructions and repo helper interfaces differ. Canonical helper
  help confirmed `search QUERY` without `--compact`; that supported call succeeded.

## Lookup And Learning

Existing `local-discover-paths-before-reads` and `ext-optional-path-discovery`
guidance applies: inventory real roots, use catalog paths and inspect each
batch result. The supported canonical lookup `search "optional path discovery
missing source file"` exited 0 and returned ext-optional-path-discovery as the
top match (verified_workaround); its paths-ownership evidence fits these
read-only inventory mistakes. No new general finding is established by these lookup errors.
Canonical ledger updates are outside this writable worktree and remain for the
parent's verified permission boundary; installed copies are not edited.

## Resolution And Verification

Corrected source reads and file inventories succeeded. Approved directories were
checked clean immediately before removing only their tracked files. The survivor
contract tests first failed for the expected missing behavior and subsequently
passed all four cases. `git diff --check` returned exit 0 after local cleanup.
Whole-suite and trigger evaluation are delegated to the parent and are not
claimed by this report. Canonical targeted `check --postmortem` returned exit 1
with only this new unregistered report; recording its hash/alias and the no-new-
learning decision in the canonical `sources.json` is blocked by the workspace
write boundary and remains outstanding.
