# Concat list-only failure on an existing output

## Symptom and impact

On 2026-09-28, the real-folder list-only check failed while sorting clips: `logic.mp4` has no `creation_time` metadata. This blocks directory-wide listing with the new capture-time ordering. No source video was modified.

## Evidence and current status

`./scripts/executable_concat-timestamped-videos /mnt/usb-8tb/concerts/logic <temporary-output> --list-only` returned 1 with `cannot read capture time for /mnt/usb-8tb/concerts/logic/logic.mp4: Invalid isoformat string: ''`. The directory already contains `logic.mp4` and `logic.ffconcat.txt` from earlier work. The focused Pixel/iPhone ordering test passed, but did not cover an existing unrelated output in the source directory.

## Root cause, resolution, verification, and follow-up

The first ordering implementation tried to read capture metadata from every video, including an unrelated prior output. Generic filenames now keep their prior eligibility and sort after timestamped Pixel/iPhone files. `--clips` selects the intended pair and excludes `logic.mp4`. The new `test_dry_run_keeps_other_video_names_without_capture_metadata` failed before the fallback and passed afterward; the explicit pair-selection test also passed. A fresh full-folder list-only check exited 0, listed 22 top-level videos, and placed `logic.mp4` last. Keep the source and existing output untouched.
