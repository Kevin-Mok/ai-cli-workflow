# Delivery command invocation

Record a delivery verification invocation mistake and its bounded correction.

## Symptom and impact

The backup exclusion preview was invoked with Python, but its entry point is a Bash script embedding Python. It failed at set -euo pipefail with SyntaxError before executing any backup operation. No data changed. A newly written delivery plan also reused an existing historical plan filename; the historical bytes were immediately restored from HEAD and the new plan moved to a dated path.

## Lookup and resolution

Read postmortem-memory and searched command interpreter and existing path discovery guidance. Matches ext-explicit-wrapper-shell and ext-optional-path-discovery apply to interpreter and destination ownership; script shebang and git show established the diagnostic evidence. The script shebang confirms Bash ownership. Invoke the executable directly. Existing discovery guidance covers checking file ownership and existing destinations before writing; no new general finding is established.

## Verification and limits

The direct excludes invocation prints the embedded policy including Snap caches and exits 0. Historical plan bytes match HEAD. This verifies preview only; no backup or restore ran.

## Candidate-ledger validation follow-up

The first public-candidate projection excluded every expenses-directory record, which also removed two historical sources still used by existing findings. The schema check rejected missing reciprocal links; the diagnostic formatter then assumed a success-only missing_sources key and raised KeyError. The candidate was not committed. Preserve historical sources and exclude only the newly introduced private preflight report. Read the error-shaped result before summarizing it. These are delivery-projection mistakes, not defects in the shared validator. Fresh exact-candidate schema validation passed with zero errors and missing sources after preserving historical entries; no reports were scanned in this schema-only check.
