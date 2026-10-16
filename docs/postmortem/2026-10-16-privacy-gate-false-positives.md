# Privacy gate blocked reviewed public source

The newly installed gate refused the repository's existing candidate with 16
findings. Diagnose each finding without exposing values, then approve only exact
reviewed public blobs and resolve Git identity separately in private local policy.

## Symptom and impact

The gate's default check exits 1. Ten findings are reviewed source expressions or
synthetic credential-redaction fixtures, four are public Markdown recovery
runbooks whose names trip the recovery-path rule, and two are effective Git
identity email findings. Normal commits are blocked until these are resolved.
The scanner reports only categories/references; no values or filenames from
sensitive paths were disclosed in the investigation.

## Evidence and lookup

Query: `privacy gate false positive credential fixture`. Returned memory guidance
on unrelated runtime boundaries and fixture validation; no directly applicable
prior gate finding. Do not broaden fixture-directory exemptions or disable checks.
Exact-index triage (object IDs, not working files) reproduced 16 findings.
The source-expression matches occur in request payloads/environment lookups;
fixture matches occur in tests of private-data redaction. Four path-only findings
are tracked Markdown documentation with no content findings. Git identities are
a separate consequential choice; the user was asked about using an existing
published GitHub noreply identity or explicitly approving the current identity.

## Root cause and resolution

The initial gate had no narrow way to retain reviewed legacy fixtures or public
recovery documentation. Generic credential matching also treats code references
as credential literals. Use exact path-reference/content-SHA256/category approvals
owned by the scanner, with public reasons and no private values. A byte edit
invalidates approval; new or changed secrets remain blocking. Retain all other
categories and built-in private-path rules. Installer snapshots the manifest with
the scanner and fails closed if policy is unavailable or malformed.

## Status and verification

Resolved. A defining disposable regression observed an unchanged reviewed
source blob incorrectly blocked (exit 1). Independent review then identified a
private-policy precedence flaw in the first approval implementation; two defining
regressions observed explicit private literal/path rules incorrectly passing.
Private findings are now unioned after public heuristic approvals, including
metadata identity literals, so explicit local prohibitions always win.

`python3 tests/test_pre_commit_privacy_gate.py`: 45 tests pass, including altered
approved blobs, missing/malformed snapshots, private-path/literal precedence and
metadata precedence. Checkpoint privacy integration: 1 pass; history auditor:
14 pass; checkpoint mechanics and real plumbing guard: 24 pass (84 total).
README recruiter check reports pass_no_change; Python compilation and focused
whitespace checks pass. Independent review verified all 14 source hashes, their
reviewed public purposes, category scope and private-rule precedence.

After reinstall and successful refresh-config, the source check, installed status
and actual installed pre-commit hook all exit 0. Before/after HEAD and index-entry
bytes are identical; no real commit, staging or push occurred. The user chose to
keep the existing Git identity and explicitly approve it as public. The exact
name/email pairs are only in private mode-0600 rules outside the checkout; local
Git config points at those rules. Identity settings remain unchanged.

The memory ledger uses the existing neutral public alias prefix; the local alias
mapping warning remains a known separate portability limitation. No actual
identity, private rules path, matched values or sensitive filenames are in this
report.

## Operational constraint

The native title tool is still unavailable through its local HTTP transport;
retain the current conversation title per the documented fallback.
