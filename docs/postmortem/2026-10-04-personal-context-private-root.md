# Private memory initialization rejected its designated root

This record explains an initialization failure caused by an overly broad
repository guard. Verify which directory carries Git metadata, then constrain
the guard to preserve the external private destination and protect this repo.

## Symptom And Impact

On 2026-10-04, initializing source-backed chatbot memory exited 1 with
`Private context cannot be stored inside a Git repository.` The helper rejected
the destination before creating or replacing the store. No personal payload
was printed or copied into this repository, and no source note was changed.

## Evidence And Current Status

The 19 synthetic helper/integration tests and basedpyright passed immediately
before initialization. Tests covered rejecting arbitrary repository test roots,
but not Git metadata in the user's specifically designated external root.
The earlier source plan described that directory as non-Git. The root task's
metadata-only inspection confirmed that the designated private directory now
owns a `.git` directory and that its ancestors do not carry Git markers.

## Root Cause And Resolution

The guard prohibited every Git-marked destination, but the user's requirement
is to keep personal contents outside linux-config. It incorrectly treated the
specifically designated external private repository as an arbitrary destination.

A synthetic regression first reproduced that rejection with the default path
mocked to a temporary directory. The helper now permits an own-root `.git`
marker only at the exact designated default directory. Ancestor repositories,
alternate roots, nested store repositories, installed skill directories, and
symlink/hardlink escapes remain rejected. The helper does not read or modify
the external Git metadata.

## Verification And Next Steps

`python3 -B tests/test_personal_context_store.py` passes all 17 synthetic tests;
the new regression verifies the exact default exception, unchanged Git metadata,
and rejection of ancestor and nested store repositories. `basedpyright` reports
0 errors, 0 warnings, and 0 notes for the helper.

The final combined helper/integration suite passed 22 tests and the type checker
reported zero findings. Retried initialization exited 0, creating revision 1
with nine entries and three questions in the designated external directory.
Existing Markdown source hashes were unchanged. No Git staging, commit, push,
or private-data copy into linux-config occurred. Status: resolved.
