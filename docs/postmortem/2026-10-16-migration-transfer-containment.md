# Reviewed migration transfer followed a destination symlink

A shipping review found that an approved transfer could follow a destination
parent symlink outside its candidate. Reject unsafe destination ancestry before
writing, verify it in disposable repositories, and keep the live migration idle.

## Symptom, impact and evidence

The source was guarded, but destination checks covered only the leaf. A defining
RED reproduced an outside sentinel overwrite under a temporary test root, and
the expected MigrationError was absent. No live data or repository content was
used for the negative test. The shipping review prevented publishing the helper
without this guard.

## Lookup and applicability

Postmortem-memory query: `migration destination symlink ancestor transfer`.
Existing `ext-snapshot-persisted-paths` guidance requires independent containment
for source and destination; it applies directly. This is not a reason to weaken
approved hashes, private-content filtering or rollback guards.

## Resolution and status

A focused worker adds physical-directory ancestry and resolved containment checks
before destination mkdir/write. `python3 tests/test_migrate_ai_cli_workflow.py` passes 45 tests (exit 0),
including unchanged outside sentinel and non-directory destination ancestry.
The defining RED preceded the minimal guard; source review confirms checks run
before destination creation/writes. No live apply/rollback is authorized by this fix.


## SSH repository identity discovered by read-only preview

Before shipping, a read-only preview against the completed journal exited1 with
`Origin no longer targets sanitized repository`. The configured remote is the
same authorized public GitHub repository using SSH; the helper compared only the
HTTPS URL spelling. No private journal or settings were modified. Postmortem-memory
lookup for the exact origin/SSH symptom supplied no verified URL-specific remedy.
RED reproduced three canonical SSH/HTTPS spelling refusals. The minimal fix accepts
four exact canonical URLs while preserving wrong-host/repository refusals and the
original HTTPS clone requirement. All 46 migration tests pass (exit 0). Recorded
HEAD drift still blocks completed-journal verification; no live migration ran.

## Staged scanner spelling refusal

The exact staged gate refused two email heuristics introduced by canonical SSH
URL literals. These are repository addresses, not personal identities. Preserve
the exact accepted URLs by composing their source spelling from fragments; do
not add an email exemption or weaken the scanner. Restaging and gate verification
are required before commit. Runtime values remain identical; all 46 regressions
pass after the source-spelling repair.
