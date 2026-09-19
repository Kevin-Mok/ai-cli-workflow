# YouTube downloader

## Purpose and scope

Create executable `scripts/yt-dl`, offline tests, an opt-in live verification
script, and usage documentation. Download one video with audio from the supplied
URL and verify the resulting media when network/platform access permits.

## Context and decisions

Python 3 standard library wrapper around installed yt-dlp; ffmpeg is required
for merging. Use the exact requested filename rather than the repository's
usual chezmoi `executable_` prefix. No system installs, cookies, commits, or
configuration edits. Default output is `~/Downloads/yt-dl`; live checks use /tmp.
Use stable video-ID filenames and ignore ambient yt-dlp configuration.

## Protected state and risks

Initial dirty files: aliases/key_dirs.tmpl, docs/smoke-tests.md,
dot_config/fish/config.fish.tmpl, dot_config/fish/functions/fn-progress.fish,
tests/test_fn_progress.sh; untracked existing sandbox postmortems, Vesktop
settings, and this task's compiled prompt. Preserve all existing edits; append
only a scoped smoke-test section. YouTube may reject network clients or require
a newer yt-dlp. No mock success may be presented as live verification.

## Checklist

- [x] Inspect rules, dependencies, and upstream CLI documentation.
- [x] Observe defining offline tests RED.
- [x] Implement wrapper and obtain GREEN.
- [x] Add repeatable live verification and attempt supplied URL.
- [x] Update docs, review, and record verification evidence.

## Verification

- `python3 -m unittest discover -s tests -p 'test_yt_dl.py' -v`
- `python3 tests/check_yt_dl_live.py`
- `./scripts/yt-dl --help`
- `git diff --check`

## Progress and review

Dependencies present: yt-dlp 2025.10.22, ffmpeg, ffprobe. The sandbox cannot
initialize loopback; narrowly scoped elevated execution is available. Tests use
an argument-sensitive downloader fixture; live validation checks ID, streams,
duration, and full decode. Rollback removes only new task files and the small
README/smoke-test additions. Keep this plan with implementation in any commit.

RED: unittest command exited 1 with 10 tests / 16 assertions failing because
`scripts/yt-dl is not implemented`, before the implementation was created.

GREEN: the unittest command passes all 13 tests (exit 0), including review-added
empty artifact, ambiguous report, and literal path coverage. CLI help and
`git diff --check` pass. Independent review found no blocking defect; coverage
recommendations were incorporated. No tracked configuration changed, so
refresh-config is not applicable.

Installed yt-dlp 2025.10.22 returned HTTP 403 on the live test; see the
[incident record](../docs/postmortem/2026-09-18-yt-dl-live-download.md).
Created an isolated runtime using `uv venv /tmp/yt-dl-runtime-SkdJyn/venv` and
`uv pip install --python /tmp/yt-dl-runtime-SkdJyn/venv/bin/python 'yt-dlp[default]'`.
Retry: `PATH="/tmp/yt-dl-runtime-SkdJyn/venv/bin:$PATH" python3 tests/check_yt_dl_live.py`.
yt-dlp 2026.8.19 downloaded `/tmp/yt-dl-live-xurxudir/oLOzkH0zVZo.mp4`.
Live checker exited 0 with PASS: ID oLOzkH0zVZo; 1,395,213,482 bytes;
audio and video streams; media duration 6351.238095 seconds versus source
6351 seconds; full ffmpeg decode passed. This verifies the full downloaded
concert, not only an extraction or mock invocation.
Installed user/system packages are unchanged.

## Final review and handoff

### Highest-quality follow-up (2026-09-19)

User now requires highest available quality, superseding the original MP4
preference. Use yt-dlp's unrestricted best-video-plus-audio selection and MKV
merging without transcoding. Preserve existing files; an existing lower-quality
file is not automatically upgraded. Use a fresh output directory for upgrades.
Keep current dependency/runtime requirements; no installed packages change.

- [x] Prove the old selector loses to higher-resolution WebM/better audio.
- [x] Update selector, container, CLI regression contract, and usage/smoke docs.
- [x] Run real yt-dlp selector tests and inspect choices for the supplied video.

Rollback is limited to this follow-up's selector/container and matching docs.
The earlier full-download/decode evidence remains historical, not proof of a
new download with the revised selector.

RED: `/tmp/yt-dl-runtime-SkdJyn/venv/bin/python -m unittest discover -s tests -p 'test_yt_dl_quality.py' -v`
exited 1: actual `mp4-1080 + m4a-128`, expected `webm-2160 + opus-160`.
The combined-only fallback passed. These tests consume the wrapper's actual
subprocess arguments and run yt-dlp's real selector against fixture metadata.

GREEN: `/tmp/yt-dl-runtime-SkdJyn/venv/bin/python -m unittest discover -s tests -p 'test_yt_dl*.py' -v`
passed all 15 tests, no skips (exit 0). `git diff --check` passed.
Live format selection (no media re-download) used:
`/tmp/yt-dl-runtime-SkdJyn/venv/bin/yt-dlp --ignore-config --js-runtimes node --no-playlist --simulate --format 'bv*+ba/b' --dump-single-json 'https://www.youtube.com/watch?v=oLOzkH0zVZo'`.
Exit 0: selected 399+251, AV1 video 1080x1920 at 30 fps plus Opus audio.
Maximum listed height was 1920, matching the selected stream. Node was enabled
only for this current-version diagnostic; the wrapper preserves compatibility
with older CLIs, and users still need a current, fully configured extractor.
No new full download/decode was performed for this selector-only revision;
the previous MP4 is unchanged. Independent review confirmed selector semantics,
MKV merge behavior, and the existing-file caveat, now documented.

The wrapper's safe CLI behavior is covered by 13 passing offline tests; failure
coverage includes bad URLs, missing dependencies, download failure, invalid
output, and ambiguous success reports. Live media evidence is above. README,
usage documentation, and grouped smoke checks match the final implementation.
The pre-existing Fish smoke-test edit remains intact. No commits were made.

Remaining limitations: the user's installed yt-dlp is still the older version;
use a current release or the retained temporary runtime to repeat this success.
The current downloader warned about missing supported JavaScript runtime, so
not every available format is guaranteed. No authentication or access controls
were bypassed. The downloaded media and temporary runtime are retained outside
the repository. Follow the [usage/handoff notes](../docs/yt-dl.md) for commands,
the Cursor review prompt, and the proposed Conventional Commit subject.

## 2026-09-19 installed runtime and destination follow-up

Scope: update the obsolete installed executable, verify the user's video, and
change the default to `/mnt/linux-files-3/yt-vids`, retaining `-o` /
`--output-dir`. Preserve the quality selector and existing files. Initial Git
status was clean; the incident document was created during this session.

- [x] Update installed yt-dlp to 2026.08.19.
- [x] Observe default-directory test fail, then change the default and docs.
- [x] Run downloader regression tests and verify downloaded media at destination.

Risk: missing/unwritable storage raises the existing actionable filesystem error;
no fallback to the home drive. Tests must not write fixture media to real storage.
Rollback: revert the default/docs change; previous installed release was
2025.10.22 (known to fail this download). No configuration sync is needed for
Python source and documentation changes. Verify with `python3 -m unittest
discover -s tests -p 'test_yt_dl*.py' -v`, `./scripts/yt-dl --help`, and ffprobe
on the completed file. Runtime warning remains a documented limitation.

Evidence: the focused default test failed with actual `~/Downloads/yt-dl` versus
expected `/mnt/linux-files-3/yt-vids`. After the change,
`/tmp/yt-dl-runtime-SkdJyn/venv/bin/python -m unittest discover -s tests -p 'test_yt_dl*.py' -v`
passed all 15 tests, including both existing override forms and real format
selection. Help displays the new default; `git diff --check` passed. The live
download exited 0 before changing the default; it and its sidecar were moved
without overwriting to the requested directory. ffprobe confirmed 3840x2160
video, audio, 3595.248 seconds, and 4,522,234,467 bytes. No full decode run.
README, usage, smoke checks, and the linked incident record are updated.
Suggested commit: `fix: update YouTube download destination and recovery notes`.
Cursor review prompt: “Review the destination change in scripts/yt-dl and its
default-directory test; run the downloader tests above and check help against
docs/yt-dl.md. Preserve quality selection and both output override flags.”

## Automatic post-download quality check

User requires immediate verification inside the download command. Preserve all
prior uncommitted destination/runtime work. Compare ffprobe's actual video
resolution and FPS with fresh yt-dlp formats after download, require audio,
enable Node when installed, and refuse a success claim if format
extraction warns or fails. Report 4K explicitly. Highest quality here means
highest listed resolution/FPS; codec/bitrate/HDR superiority is not provable
from dimensions. Keep stdout path-only and preserve files on verification failure.

- [x] Observe RED for 4K success reporting, lower resolution/FPS and warnings.
- [x] Implement inline verifier and update usage/README/smoke checks.
- [x] Run offline regression and live command against the existing 4K file.

Verification: downloader unittest suite, existing video rerun without overwrites,
and independent review. Risk: fresh extraction can fail after a valid download;
retain it and return nonzero. Rollback is reverting only this verifier addition.

Review caught a mismatch between default extractor sorting and strict maximum
resolution/FPS verification. A real-selector RED test chose preferred 1080p
over 2160p60; selection now forces `res,fps` ahead of other preferences.
4K classification uses a long edge of at least 3840 pixels so cinematic
widescreen and portrait footage are recognized. Resolution ranking uses the
short edge, consistently with yt-dlp. Any extraction warning is inconclusive.

Initial live run of `./scripts/yt-dl 'https://www.youtube.com/watch?v=kDK8-psUjzY'`
exited 0, reporting VERIFIED 3840x2160 at 23.976 fps with audio and 4K,
against fresh metadata. It reused the existing file. Node is now explicitly
enabled, and this live run emitted no extraction warning. Full decode was not
repeated; this feature checks streams and quality, not every media packet.

Final verification: all 23 downloader tests passed in the retained yt-dlp
Python environment; the final live command again exited 0 with the 4K
verification message above. `git diff --check` passed. Tests cover retained
low-resolution files, stale sidecars, FPS mismatch/tolerance, missing audio,
missing ffprobe, incomplete extraction, non-4K sources, and real selection.
Suggested commit: `feat: verify video quality immediately after download`.
Cursor review prompt: “Review scripts/yt-dl inline verification and both
downloader test files. Run the documented suite and rerun the existing 4K
video without overwriting. Confirm stderr quality reporting, path-only stdout,
and failure when a higher reported resolution/FPS exists.”

Delivery: one coherent downloader commit includes destination, verification,
tests, README, smoke checks, usage, this plan, and the incident record. Before
staging, all 23 downloader tests passed again, CLI help matched the documented
default/override, `git diff --check` passed, and the README gate returned
`pass_no_change`. Push target: `origin/feat/ai-workflow-optimization`.
