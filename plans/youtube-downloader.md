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
