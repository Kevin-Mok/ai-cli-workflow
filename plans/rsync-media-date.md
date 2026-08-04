# Reusable Dated iPad Media Transfer

## Purpose and observable outcome

Add a managed `rsync-media-date` Bash command that accepts an ISO date, a
mounted iPad source, and a destination directory, then overwrites matching
flat media filenames at the destination with that date's original DCIM media.

## Current context, scope, and protected state

- The tracked iPad helpers in `dot_config/fish/functions/ipad/` only transfer
  a single image number and do not provide date selection.
- No tracked `rsync-date-folder.sh` was found in `/home/example` or this repo;
  the new helper will use the managed `scripts/executable_*` convention.
- The user confirmed ISO `YYYY-MM-DD` input, no folder layout preservation,
  immediate transfer (not dry-run), and overwrite behavior.
- Preserve all pre-existing dirty files captured before this task, including
  `README.md`, `docs/smoke-tests.md`, and second-brain changes. Only stage the
  files listed below that this task creates or edits.
- Scope: original `MOV`, `MP4`, and `M4V` files under `SOURCE/DCIM`; no Photos
  metadata, cache files, source deletion, or filename renaming.

## Assumptions and decisions

- File modification times exposed by the mounted iPad identify the requested
  local calendar day. The observed July 28 originals use those timestamps.
- Rsync's default replacement behavior satisfies the requested overwrite
  policy; do not pass `--ignore-existing` or `--update`.
- The helper should create a missing destination directory and show
  `--info=progress2` output during the transfer.
- The 2026-07-28 iPad selection was measured at 45.70 GiB while the HDD had
  49.52 GiB free. The command must not preflight capacity because accurate
  allocation is filesystem-specific, but its documentation will warn about
  the tight margin.

## Implementation checklist

- [x] Capture initial Git status and inspect repository conventions.
- [x] Record confirmed interface and behavior in
  `docs/superpowers/specs/2026-07-29-rsync-media-date-design.md`.
- [x] Add `tests/test_rsync_media_date.sh` with a RED case that expects the
  new helper to select only same-date original media, build a flat rsync file
  list, create the destination, and pass overwrite-capable arguments.
- [x] Run `bash tests/test_rsync_media_date.sh`; it failed with exit status 2
  because `scripts/executable_rsync-media-date` did not exist yet.
- [x] Implement `scripts/executable_rsync-media-date` with `set -euo pipefail`,
  `YYYY-MM-DD SOURCE DESTINATION` validation, DCIM media selection with
  `find -newermt` date bounds, a null-delimited temporary file list, and
  `rsync --archive --info=progress2 --human-readable --no-relative` with the
  selected media paths to produce a flat destination.
- [x] Run the focused tests until GREEN and run `bash -n` on the script.
- [x] Add one `Action`/`Expected` entry to `docs/smoke-tests.md` covering the
  installed command and the requested J. Cole example. Do not touch the
  protected pre-existing smoke-test edits; stage only this entry's hunk.
- [x] Run the focused tests again and inspect the diff. No commit was
  requested, so no staging will occur.
- [x] Run the `snapshot-codex-config --dry-run` preflight; it passed. Run
  `refresh-config`: its snapshot and shortcut steps completed, while
  `chezmoi apply` needs an interactive overwrite response for the separately
  changed live Codex config and was deliberately not forced. Apply the helper
  target alone with chezmoi so `/home/example/scripts/rsync-media-date` is live.
- [x] Record final verification evidence and review notes below.

## Test design

`tests/test_rsync_media_date.sh` will make a temporary source fixture with:

```text
DCIM/100APPLE/IMG_OLD.MOV       2026-07-27
DCIM/101APPLE/IMG_JULY_28.MOV   2026-07-28
DCIM/101APPLE/IMG_JULY_28.MP4   2026-07-28
DCIM/101APPLE/IMG_JULY_29.M4V   2026-07-29
PhotoData/ignored.MOV           2026-07-28
```

It will put a mock `rsync` first in `PATH`, capture its null-delimited argument
list, then assert the two July 28 DCIM paths are selected, `IMG_OLD.MOV`,
`IMG_JULY_29.M4V`, and `PhotoData/ignored.MOV` are not selected, the destination
directory exists, and no `--ignore-existing` or `--update` flags appear. A
malformed date case must fail before the mock is called.

## Risks, rollback, and edge cases

- Same-named source files from different DCIM folders overwrite each other in
  the flat destination; this is intentional per the confirmed overwrite and
  no-layout requirements.
- The current HDD margin is about 3.8 GiB. An `ENOSPC` failure leaves files
  already copied; rerunning resumes/corrects them after space is made.
- Interruptions leave partial output; rerunning uses rsync to continue.
- Rollback is removal or restoration of individual destination filenames from
  a separate backup; the helper never deletes from the iPad.

## Verification evidence

- RED: `bash tests/test_rsync_media_date.sh` exited 2 before the helper
  existed, at its executable-file assertion.
- Initial GREEN: `bash tests/test_rsync_media_date.sh` and
  `bash -n scripts/executable_rsync-media-date` both exited 0.
- Boundary RED: a disposable real-rsync fixture showed a `2026-07-29
  00:00:00` file was incorrectly copied for `2026-07-28`; the new
  `tests/test_rsync_media_date_boundary.sh` then exited 1 reproducing it.
- Boundary GREEN: `bash tests/test_rsync_media_date.sh && bash
  tests/test_rsync_media_date_boundary.sh && bash -n
  scripts/executable_rsync-media-date` exited 0 after the predicate changed
  to explicit start/end second boundaries.
- Refresh preflight: `fish -ic 'snapshot-codex-config --dry-run'` exited 0.
  The first non-TTY `refresh-config` invocation reported that chezmoi could
  not open `/dev/tty`; the TTY retry reached its normal overwrite prompt for
  `.codex/config.toml`. No force overwrite was performed. The waiting
  processes were stopped, then `chezmoi apply /home/example/scripts/rsync-media-date`
  completed and the installed helper rejected a malformed ISO date as expected.

Required manual command, intentionally not run because it would copy about
45.70 GiB to a disk with about 49.52 GiB free:

Manual check:

```text
rsync-media-date 2026-07-28 /mnt/ipad /mnt/linux-files-3/concerts/jcole
```

Expected: the 39 July 28 original videos copy directly into the J. Cole folder
with rsync progress, overwriting any matching names and creating no DCIM
subfolders.

## Review notes

The simplest robust solution is a standalone Bash helper plus hermetic shell
tests and one actual-rsync boundary test; it avoids coupling a one-off transfer
to Fish while remaining managed by the repository's executable convention.
The exact-midnight regression showed that `! -newermt` is inclusive at its
reference timestamp, so the final implementation bounds the requested day as
strictly newer than the preceding second and not newer than the final second.
Rollback is removal or restoration of copied files from the destination.
