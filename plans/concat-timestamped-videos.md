# Concatenate timestamped videos without transcoding

## Purpose and observable outcome

Provide a reusable command that takes one directory of camera clips, orders top-level files by filename timestamp, writes an FFmpeg concat text file, and creates one output with stream copy.

## Context and scope

No existing concat script was found in `scripts/` or Fish functions. `/mnt/usb-8tb/concerts/logic` contains top-level `PXL_YYYYMMDD_HHMMSSmmm.mp4` files plus a nested `juicy-j` directory. Add one command, focused tests, and usage/smoke documentation. Do not process nested directories or run the 34 GB job during verification.

## Assumptions and decisions

- "Timestamped order" means lexicographic filename order for the camera names shown. Modification times reflect copy timing and are not the source of truth.
- Include `.mp4`, `.mov`, and `.m4v` regular files in the given directory. The user can choose an output path. Stream copy requires compatible input streams.
- Never overwrite an existing output. Keep the generated concat list as a reviewable text file beside the output.

## Checklist

- [x] Capture initial dirty state and identify protected existing README, smoke-test, lessons, and untracked work.
- [x] Audit existing scripts and sample directory.
- [x] Add a defining test and observe RED.
- [x] Implement the command and observe GREEN.
- [x] Update README and smoke checks while preserving existing changes.
- [x] Run focused and proportionate regression checks; record evidence.
- [x] Add a real FFmpeg two-clip integration test that decodes frames on both sides of the join.
- [x] Produce short boundary samples for all adjacent Logic clips and inspect contact sheets.
- [x] Record the follow-up verification in documentation and rerun relevant checks.

## Risks and rollback

Mixed codecs, stream layouts, or formats may make FFmpeg stream copy invalid; FFmpeg's nonzero status is propagated and no transcoding fallback is attempted. A partial new output may remain after FFmpeg failure. The command does not touch source clips. Roll back by removing the new command, test, and its documentation additions. Existing dirty files listed by initial `git status --short` remain protected.

## Verification and review notes

RED: `python3 -m unittest discover -s tests -p test_concat_timestamped_videos.py` exited 1 with three expected failures because the command was absent. GREEN: the same command exited 0 with three tests passing. `./scripts/executable_concat-timestamped-videos /mnt/usb-8tb/concerts/logic /tmp/logic-joined.mp4 --list-only` exited 0 and listed 13 clips. The generated file was inspected: timestamps ascend, with no nested `juicy-j` files. First and last `ffprobe` checks exited 0 and each showed HEVC 3840x2160 video plus AAC 48 kHz audio. `./scripts/executable_readme-recruiter-sync` returned `pass_no_change`; `git diff --check` exited 0. Full `python3 -m unittest discover -s tests` ran 403 tests and exited 1 due to the unrelated extra vault daily note documented in `docs/postmortem/2026-09-28-concat-regression-vault-inventory-failure.md`. The full 34 GB join was not run. The sandbox startup failure is documented in `docs/postmortem/2026-09-28-command-sandbox-loopback-startup.md`.

Follow-up: a real two-clip FFmpeg test generates red and blue videos, runs the concat command, decodes the output, checks duration, and inspects pixels from both sides of the boundary. Directory mode had a deliberate RED failure before `--directory` implementation, then passed. A second deliberate RED exposed the need to honor `logic.ffconcat.txt` rather than include newly present `IMG_*.MOV` files and `logic.mp4`; list-aware directory selection then passed. `python3 tests/check_concat_boundary.py --directory /mnt/usb-8tb/concerts/logic --seconds 2` exited 0 after checking all 12 boundaries from the 13-file list. The overview at `/tmp/concat-boundary-_uia32_i/overview.jpg` was visually inspected and showed no obvious corrupted frames; several boundaries reported non-monotonic DTS warnings. These samples do not prove full-output audio continuity or every frame of the 27 GB `logic.mp4`.

Final follow-up checks: `python3 -m unittest discover -s tests -p test_concat_timestamped_videos.py` exited 0 with six tests. `python3 tests/check_concat_boundary.py --help` exited 0 and lists `--directory`, `--concat-list`, and `--seconds`. `./scripts/executable_readme-recruiter-sync` returned `pass_no_change`; `git diff --check` exited 0. The full unittest discovery rerun executed 406 tests and exited 1 for the same unrelated vault inventory failure. A spot contact sheet taken directly from `logic.mp4` around the first source boundary at `/tmp/concat-boundary-_uia32_i/full-output-first-join.png` was visually inspected and showed no obvious corrupted frames.

## 2026-09-28 mixed camera follow-up

Purpose: make the command handle the actual `PXL_20260928_011900910.mp4` and `IMG_1377.MOV` pair in capture order and produce a decodable join. The existing command, tests, README, and smoke notes are pre-existing untracked or dirty work and must be preserved. The original large media files are read-only inputs.

Evidence and decisions: the Pixel filename encodes a UTC start time of 01:19:00.910; the iPhone MOV reports `creation_time=2026-09-28T01:21:49Z`. A list-only run put the MOV at position 6 and Pixel clip at position 19. The two sources use HEVC Main and Main 10 respectively, and a one-second stream-copy join emitted non-monotonic DTS and decoder errors. The user chose only this named pair and approved whatever re-encoding is needed for smooth playback. Implement a clean hard cut with continuous audio; the sources were recorded several seconds apart. The re-encode path tone-maps iPhone HLG to SDR H.264/AAC and does not retain Dolby Vision metadata.

- [x] Capture and protect initial dirty state; inspect actual media and source code.
- [x] Add an ordering regression test and observe expected RED (`python3 -m unittest discover -s tests -p test_concat_timestamped_videos.py -k test_dry_run_orders_pixel_and_iphone_clips_by_capture_time`, exit 1, reversed entries).
- [x] Implement capture-time order for the two filename families and observe GREEN.
- [x] Resolve pair selection and mixed-profile join behavior from the user's answers; add defining RED tests before implementation.
- [x] Update README, grouped smoke checks, postmortem, and this plan with the actual behavior.
- [x] Run focused and broader regressions, real short-sample join/decoder checks, and documentation gate; record exact results.

Risks and rollback: metadata can be missing or inconsistent, and re-encoding can alter HDR, audio, duration, or quality. Do not overwrite source clips or the existing `logic.mp4`. Roll back only this follow-up's changes if necessary; preserve the earlier untracked command and associated work.

Verification so far: `test_dry_run_orders_pixel_and_iphone_clips_by_capture_time` failed RED with reversed entries, then passed GREEN. `test_clips_selects_only_named_pair_in_capture_order` failed RED because `--clips` was unavailable, then passed GREEN. `test_reencode_joins_mixed_sdr_and_hlg_clips_without_decode_errors` failed RED because `--reencode` was unavailable, then passed GREEN. `test_dry_run_keeps_other_video_names_without_capture_metadata` failed RED on a prior output and then passed GREEN. `python3 -m unittest discover -s tests -p test_concat_timestamped_videos.py` exited 0 with 10 tests. A fresh list-only check of the real folder selected exactly `PXL_20260928_011900910.mp4`, then `IMG_1377.MOV`; the directory-wide list-only check exited 0 with 22 files, placing `logic.mp4` last. The first short-media probe failed because trimming dropped the MOV creation timestamp (recorded in the linked postmortem); the retry preserved it, then joined two 0.3-second real source samples and decoded the output with exit 0 and empty error output. `./scripts/executable_readme-recruiter-sync` returned `pass_no_change`. The full-size render remains a manual check because it re-encodes several minutes of 4K video.

Broader regression: `python3 -m unittest discover -s tests` ran 410 tests in 67.262 seconds, exit 1, with only `test_second_brain_vault.SecondBrainVaultTest.test_exact_sanitized_tree_exists_without_unapproved_files` failing on the pre-existing extra `05 Daily Notes/2026-07-22.md`. This is recorded in [the vault inventory postmortem](../docs/postmortem/2026-09-28-concat-regression-vault-inventory-failure.md). The focused concat test file remained green with ten tests.

Final checks: `git diff --check` exited 0; `./scripts/executable_concat-timestamped-videos --help` exited 0 and showed `--clips` and `--reencode`; `./scripts/executable_readme-recruiter-sync` returned `pass_no_change`. Both original source files exist, and the documented `logic-pair.mp4` output path does not yet exist. The full-size render was not started.

Review notes: `--clips` accepts two basenames and never selects other files in the directory. Generic video names remain eligible in directory mode and sort after recognized timestamped clips; use `--clips` for this mixed-camera pair. The concat list remains a review artifact even with `--reencode`. The output is a new SDR file, with no source writes. README, grouped smoke checks, postmortems, and the sample-metadata lesson were updated. The requested commit workflow groups this plan with the concat implementation and documentation, after the older daily-size and HDD-wizard commits.
