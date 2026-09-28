# HDD wizard interactive dry-run prompt failure

## Symptom and impact

The first interactive `--dry-run` reached the USB-disk selection prompt. After
entering `/dev/sdd`, Bash exited 1 with `answer: unbound variable` at line 256.
The wizard stopped before any privileged or write operation.

## Evidence and root cause

The initial non-interactive `--dry-run`, `--help`, and `bash -n` all exited 0.
The interactive reproducer failed specifically after the first input. The
`prompt` helper declares a local `answer` and uses `printf -v` to write to that
name, so the caller's `answer` remains unset under `set -u`.

## Resolution and verification

Renamed the helper's local variable to `input`, leaving the caller's `answer`
available for `printf -v`. The same interactive dry run selected `/dev/sdd`,
confirmed the exact path, declined SMART, accepted default label and mount
path, printed the GPT/ext4/mount/fstab plan, and exited 0 with `No writes were
made.` No destructive operation was invoked.

## Follow-up and rollback

Keep the interactive dry-run path in the smoke checklist. Repository rollback
would revert this script and its related docs; no disk rollback was needed.
