# Benchmark source pins after public cleanup

This report records source-verification failures found while removing identifying benchmark artifacts. It separates publication safety from benchmark reproducibility and preserves the original evidence instead of repinning historical inputs to make a check pass.

## Symptom and impact

The pilot `verify` command exits 2 with a candidate integrity mismatch for `candidates/metaprompt-alxve/SOURCE.md`. The selection `verify` command exits 1 with a source integrity failure for `candidates/wshobson-patterns/assets/few-shot-examples.json`. Fresh benchmark execution must remain blocked until the source/provenance mismatch receives its own review. No model requests were made during this investigation.

## Evidence and prior lookup

- Both affected source files and both pin manifests are byte-identical to the starting public HEAD. Removing raw run directories did not change them.
- Both offline `dry-run` commands exit 0 without model calls after raw artifacts are removed.
- The 97 focused auditor/benchmark regressions pass using synthetic inputs; those tests do not certify the real pinned source packages.
- Query: `Candidate integrity mismatch Source integrity failure pinned sanitized benchmark`. Retrieval returned no applicable source-pin remedy; unrelated network and execution findings were rejected as evidence for a fix.
- A separate read-only inventory probe named a nonexistent documentation file. It changed nothing; subsequent reads used inventoried paths. This adds no product defect or reusable learning beyond checking paths before reads.

## Cause, status and resolution boundary

The checked-in package bytes disagree with their stored expected hashes in the starting public revision. The precise earlier modification that created the disagreement was not investigated. The privacy cleanup removes raw public artifacts and prevents their adoption; it does not repair or silently update frozen source pins. Source verification remains unresolved and is documented beside the reusable benchmark commands.

## Follow-up and recovery

Review sanitized package provenance and authorize a new baseline before another inference run. Do not change historical scores, recreate deleted identifying traces, or infer successful source verification from synthetic test results. The privacy cleanup's private bundle and candidate-file archive preserve recovery; these artifacts must never be reintroduced into public Git history.

The public learning ledger uses a neutral checkout alias. Exact local aliases belong in the private verification overlay so maintaining incident knowledge does not publish machine paths.

## Pre-refresh inventory interface

The installed `chezmoi managed` help advertises `--format none|json|yaml`, but `none` is rejected and `json` exits0 while returning non-JSON path text. Both read-only probes stopped before any live apply. A dependent private-ledger check also lacked its not-yet-created input after the first stopped backup. Retrieval matched `local-absolute-installed-cli-contract`; validate the exact installed output contract, use the documented NUL path separator directly, and require success before dependent writes/checks. No installer, external or removal action ran during these probes.

A fresh-fish refresh probe erased the autoload helper before invoking it and exited127 with command-not-found. No apply started. Existing lookup guidance requires a callable function rather than an abbreviation or assumed loaded definition. The next attempt explicitly sources the reviewed function file in a fresh shell before calling it.

Observed recovery: direct NUL-separated managed-path output was validated and1,302live targets were backed up privately. Explicitly sourcing the reviewed helper in `fish --no-config` then completed apply, shortcut generation and reload with exit0; scripts, externals and removals remained excluded. The source-pin mismatch remains unresolved; these inventory/launch issues did not alter source manifests or authorize a benchmark run.


## Final privacy-boundary probe

The private read-only cleanup verifier initially passed multiple paths with
`git check-ignore --quiet`, which accepts only one pathname, and therefore
reported a failed ignore boundary despite zero content findings. No publication
or live apply occurred. Lookup `git check-ignore quiet single pathname` returned
no applicable remedy; unrelated revision/merge findings were rejected. The
verifier now checks each root separately and requires both exit statuses to be
zero. This is a verification-command correction, not a public scanner defect.
Additional missing optional skill/reference probes changed no files; their
fallback paths were located before further reads.


## Pre-publication metadata review

The first unpublished cleanup commit used the approved public author email for
its committer too. The strict verification helper intentionally exempts only
the exact approved author header and therefore rejected that committer email.
No private value was printed or pushed. Lookup `approved author commit metadata
email audit` yielded no applicable remedy; keep the existing strict boundary.
The replacement keeps the requested author identity and uses the established
public noreply committer identity. A typography edit also split the plan's
starting revision; direct review caught it before publication and the literal
revision was restored. Reclone the corrected candidate independently so the
rejected unpublished commit is not retained in the active all-object database.
