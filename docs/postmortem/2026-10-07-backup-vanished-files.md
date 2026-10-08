# Live backup aborts on vanished home files

Record why a running-system backup aborts on normal file rotation and verify the best-effort behavior requested by the user.

## Symptom and impact

The supplied backup log shows Spotify/Chrome LevelDB files disappearing, rsync code 24, three retries, and an incomplete bundle. User explicitly accepts these missing files. Root cause is the bounded-retry failure policy in copy_command, rather than a copy I/O error.

## Lookup and evidence

Postmortem search `backup rsync vanished code 24` found topology/other backup guidance but no applicable vanished-file remedy. Existing swap-alias finding is unrelated. Source and tests explicitly require failure after three code-24 attempts. Plan: defining RED test, accept live code 24 once, preserve warnings and fatal errors, verify publication.

## Current status

Resolved in repository code: accept live rsync exit 24 once, retain diagnostics, continue copied-home verification and publication. Other copy errors and offline changed-source rejection remain. Defining tests observed RED (2 calls instead of 1; retry exhaustion). GREEN: python3 -B -m unittest discover -s tests -p 'test_backup_pc*.py' passed all 58 tests, exit 0; bash -n scripts/executable_backup-pc passed, exit 0. Publication test uses a real fixture copy with injected code 24 and verifies warning checksums and tamper rejection. Activation verified: fish -c refresh-config completed with REFRESH COMPLETE (exit 0); cmp scripts/executable_backup-pc /home/example/scripts/backup-pc exited 0. git diff --check exited 0. No full backup or disk restore performed.
