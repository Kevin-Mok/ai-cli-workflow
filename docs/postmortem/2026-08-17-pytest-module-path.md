# Pytest Console-Script Import Failure

## Symptom

Running `pytest -q` failed during collection with
`ModuleNotFoundError: No module named 'scripts.second_brain'`.

## Impact

The repository-wide Python verification suite could not begin, preventing a
full integration check during the refresh-config repair.

## Evidence

The failure occurred while collecting
`tests/test_second_brain_config_snapshot.py` under the console-script pytest
entrypoint.

## Current Status

The module entrypoint resolves the import path, but the full suite remains red
for an unrelated sanitized-vault contract: it expects the July 14 daily note
while the tracked vault contains a July 22 note.

## Root Cause

The bare `pytest` console script does not place this repository root on Python
module resolution, while `python3 -m pytest` does. The remaining vault failure
is a stale independent fixture expectation, not a refresh-config change.

## Resolution

Use `python3 -m pytest` for repository-wide Python verification. Leave the
vault date mismatch for a separately scoped repair.

## Verification

`python3 -m pytest -q` collected the suite and ran 342 passing tests plus 49
passing subtests. One unrelated vault test failed on the extra July 22 note.

## Follow-up

Update the sanitized-vault fixture date and expected tree only in a dedicated
Second Brain maintenance change.
