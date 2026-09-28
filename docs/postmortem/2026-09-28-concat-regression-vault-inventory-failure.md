# Broad regression blocked by unrelated vault inventory

Date: 2026-09-28

## Symptom and impact

The full Python unittest discovery run for the video concat change exited 1. The new concat tests passed, but the broader suite could not be reported green.

## Evidence and current status

`python3 -m unittest discover -s tests` ran 403 tests in 54.462 seconds and reported one failure: `test_second_brain_vault.SecondBrainVaultTest.test_exact_sanitized_tree_exists_without_unapproved_files`. Its actual file set contains an extra `05 Daily Notes/2026-07-22.md`. This file and test are outside the concat scope. The focused concat suite exited 0 with three tests.

After the directory-check follow-up, the full suite was rerun: 406 tests in 57.805 seconds, exit 1, with the same sole vault-inventory failure. The expanded focused concat suite exited 0 with six tests.

After the mixed-camera pair follow-up, the full suite ran 410 tests in 67.262 seconds, exit 1, with that same sole vault-inventory failure. The focused concat suite exited 0 with ten tests.

## Root cause and resolution

The vault inventory fixture contains a daily note that the test's fixed allowlist does not expect. No vault file or allowlist was changed for this task. The existing extra file remains for its owner to reconcile; the concat implementation requires no change from this failure.

## Verification and follow-up

Focused command behavior and the actual Logic list-only run passed. Re-run the full suite after the vault inventory owner reconciles the extra file. Do not delete the note merely to clear this unrelated test.
