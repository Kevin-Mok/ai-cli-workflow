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

## Chezmoi executable installation repair

Initial dirty state: user moved scripts/yt-dl to scripts/executable-yt-dl,
with byte-identical committed content. Preserve it while correcting chezmoi's
attribute to executable_yt-dl. The installed PATH command is stale and 0644.

- [x] Reproduce with isolated chezmoi apply: expected scripts/yt-dl absent.
- [x] Correct source name, test paths, README, usage, and smoke checks.
- [x] Run downloader tests, refresh-config, and Fish PATH help verification.

Risk: refresh-config snapshots live Codex/Git config and applies all targets;
inspect status afterward and keep unrelated changes out of the repair. No
manual chmod-only workaround. Rollback restores the old source name but also
restores the install bug. Verification uses the real deployment test plus
source/installed byte comparison. See the executable-install postmortem.

Repair verification: all 24 `test_yt_dl*.py` tests passed using the retained
yt-dlp environment. The real isolated chezmoi apply test failed before the
rename and passed after. `fish -c 'refresh-config'` exited 0 with REFRESH
COMPLETE; `fish -c 'command -s yt-dl; yt-dl --help'` resolved
/home/example/scripts/yt-dl and exited 0. Installed mode is 775, and `cmp`
confirmed exact source content. Refresh introduced no unrelated dirty files.
`git diff --check` passed. No new video download was required for this install
repair. Suggested commit: `fix: install yt-dl as executable through chezmoi`.
Cursor review: “Verify scripts/executable_yt-dl deploys as ~/scripts/yt-dl; run
the 24 downloader tests, inspect docs/yt-dl.md and the deployment incident,
and verify Fish yt-dl --help after refresh-config.”

## Live download progress

Preserve the pending chezmoi deployment repair. User reports downloads look
idle; explicit --no-progress suppressed updates. Enable --quiet --progress
to stream percentage/speed/ETA on stderr and preserve stdout's path contract.
Show fetching and checking status; percentage is only meaningful during transfer.

- [x] RED: percentage test failed because no 50.0% progress appeared.
- [x] Enable native progress and document stages.
- [x] Verify regression, real yt-dlp local transfer, and refresh-config deployment.

Risk: unknown total size cannot yield a percentage; separate video/audio
streams have separate progress. Rollback removes these progress/status options.

Verification: all 25 downloader tests passed. Real local HTTP transfer exposed
that native progress uses stdout, so the wrapper now forwards child stdout
directly to parent stderr and collects the final path via --print-to-file in
a cleaned temporary directory. The corrected real transfer reached 100% and
the separate report contained only the final path. Final refresh-config
exited 0 with REFRESH COMPLETE; cmp confirms installed bytes match source.
The already-running download cannot acquire the new code; subsequent launches
show progress. Suggested commit: `fix: stream live video download progress`.
Cursor review: “Run downloader tests and verify percentage output streams to
stderr, path reports remain separate, and chezmoi installs the current source.”

## Nominal FPS tolerance repair

Preserve all pending installation/progress work. User's portrait 720x1280 file
probes at 3726/125 = 29.808 fps versus nominal source 30 fps. Fixed 0.1 fps
tolerance produces a false rejection. Use 1% relative tolerance while requiring
full resolution and retaining actual FPS in output. This accommodates timing
variation, not arbitrary FPS loss; 29/25/24 versus 30 and 30 versus 60 fail.

- [x] Reproduce exact 29.808/30 rejection with a regression test.
- [x] Apply tolerance, update docs, run regressions.
- [x] Refresh chezmoi and recheck the actual retained video.

Risk: verification allows up to 1% FPS shortfall by design; it remains a
metadata quality check, not full frame-by-frame integrity analysis. Rollback
restores 0.1 fps tolerance but reintroduces this false rejection.

Evidence: exact FPS regression failed before implementation, then all 27
downloader tests passed. refresh-config exited 0. Installed command
`~/scripts/yt-dl 'https://www.youtube.com/watch?v=hf163Txt_pg'` exited 0:
VERIFIED 720x1280 at 29.808 fps with audio; 4K not reported. Existing media
was reused. Suggested commit: `fix: tolerate nominal video frame-rate drift`.
Cursor review: “Review the 1% FPS threshold, reproduce the new nominal-30
tests and run all downloader tests; check the retained video and docs.”

## Title filenames without JSON sidecars

User requests lowercase kebab-case video titles and no JSON files. Generate
an ASCII title slug with lowercase video-ID suffix, capped title length and
`video` fallback for titles without ASCII letters/digits. Fetch metadata only
in memory; explicitly disable info sidecars. Preserve existing media/sidecars
without bulk renaming/deletion. The opt-in live test fetches metadata in memory.

- [x] RED: CLI filename expectation rejects old ID-only output template.
- [x] Implement title slug and no-sidecar behavior with regressions.
- [x] Update docs, refresh-config, and verify installed source.

Risk: changing title or naming convention can create a new download; old
files remain untouched. Lowercase ID suffix greatly reduces title collisions
but IDs differing only by case can collide. Rollback returns ID-only naming.

Verification: all 28 downloader tests passed, including real format-selection
and isolated chezmoi deployment tests. Title punctuation/accents, fallback,
length cap, and no-JSON CLI option are covered. refresh-config exited 0 and
cmp confirmed the installed source matches. No additional full YouTube
download was performed for this naming-only change.
Suggested commit: `feat: name videos from titles without JSON sidecars`.
Cursor review: “Run test_yt_dl*.py with yt-dlp installed; inspect title slug
handling and no-write-info-json, and confirm deployed source matches.”

## Title-only filename correction

User explicitly excludes video IDs. Remove the suffix while preserving ASCII
lowercase kebab-case normalization, 160-character cap, no JSON sidecars,
progress, quality checks, and existing-file preservation. Same-title videos
need separate -o directories; no-overwrites prevents replacing existing media
but quality verification cannot establish identity. Earlier ID-suffix design
is superseded. No bulk rename of old files requested.

- [x] RED: title-only CLI test fails against the ID-suffixed implementation.
- [x] Remove suffix and update naming tests/docs.
- [x] Run regressions and refresh-config; compare installed source.

Rollback restores the suffix. Suggested commit: `fix: use title-only video filenames`.

Title-only verification: all 28 downloader tests passed; refresh-config exited
0 and installed/source bytes match. git diff --check passed. No new full
download was needed. Cursor review: “Check title-only output, no JSON sidecars,
existing-file preservation, and run the downloader suite.”

Delivery follow-up: ship installation, progress, FPS tolerance, and title-only
naming together with their tests and documentation as one coherent downloader
commit. Fresh 28-test suite, README gate (`pass_no_change`), diff check, and
installed-source comparison all passed. Real transfer and FPS evidence are
recorded above; no new full decode was performed during delivery.
Push destination: origin/feat/ai-workflow-optimization.
