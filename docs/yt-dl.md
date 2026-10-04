# YouTube downloader

Download one YouTube video with audio and check that its saved resolution
and frame rate match the best formats reported by yt-dlp. Install the
required tools, choose an output folder, run `yt-dl` with the video link,
then read the download and verification result.

Run `yt-dl` after chezmoi apply (Python 3.9+, current yt-dlp, ffmpeg, and ffprobe on
PATH). No sudo is needed.
The wrapper does not install or update dependencies. Follow the
[yt-dlp installation instructions](https://github.com/yt-dlp/yt-dlp#installation)
for your environment, including its current JavaScript runtime requirements.

```bash
yt-dl 'https://www.youtube.com/watch?v=oLOzkH0zVZo'
yt-dl 'https://www.youtube.com/watch?v=oLOzkH0zVZo' --output-dir /tmp/my-videos
yt-dl --help
```

The default directory is `/mnt/linux-files-3/yt-vids`. Override it with
`-o /path/to/videos` or `--output-dir /path/to/videos`. The destination must be
writable; filesystem errors are reported without falling back to another drive.
Watch, youtu.be, shorts, live, and embed video URLs are accepted. Playlist-only
URLs are rejected; playlist and tracking parameters on video links are removed.
Only one video is downloaded. Ambient yt-dlp configuration is ignored; no
browser cookies are read.

The script uses `bv*+ba/b`: yt-dlp's best available video, adding its best
audio-only stream when the video does not already contain audio, with a combined
format fallback. There is no resolution cap or MP4/M4A preference. Quality is
ranked with resolution then frame rate first (`--format-sort res,fps
--format-sort-force`), followed by yt-dlp’s other quality preferences; see the
[upstream selection rules](https://github.com/yt-dlp/yt-dlp#format-selection).
Separate streams merge into MKV without transcoding or quality loss. A combined
download keeps its original container. Files use only the video title in lowercase ASCII kebab-case,
e.g. `my-video-title.mkv`, without a video ID. Spaces and punctuation
become hyphens, accents are normalized, and empty slugs use `video`. Titles
are capped at 160 characters. No JSON sidecar is created: metadata is fetched
in memory for naming and quality verification. Existing media is not overwritten;
older ID-only files and old sidecars are left untouched. A changed YouTube
title or naming convention can produce a new filename on a later run.
Different videos can share a title; use separate `-o` directories in that case.
Existing same-name files are preserved, and the quality check does not prove
the identity of an existing file. Partial
downloads may remain for yt-dlp to resume. Keep output outside the repository.
Use a fresh output directory when upgrading an earlier download's quality:
existing same-name media is preserved, not automatically upgraded.

While downloading, stderr shows live percentage, transfer speed, and ETA
when yt-dlp knows the total size. Video and audio streams have separate progress
updates; fetching and quality verification have status messages.
Success prints one absolute final media path to stdout. Diagnostics go to
stderr. Exit codes: 0 success, 2 argument error, 1 missing dependency/local
error; downloader failures preserve yt-dlp's nonzero code, and interruption
returns 130. Immediately after downloading or reusing an existing file, the command runs
ffprobe and fetches fresh yt-dlp formats. It verifies audio is present and the
saved resolution/frame rate meet the highest reported video format, allowing
1% frame-rate timing variation (for example, 29.808 average fps versus nominal
30 fps). Resolution is not relaxed, and substantial FPS drops still fail. A concise
`VERIFIED` message on stderr explicitly reports 4K dimensions (long edge at least 3840 pixels) or higher, or that
4K was not reported. Portrait videos use their shorter dimension for resolution.

A lower-resolution/FPS file, missing audio, probe failure, extraction warning,
or unavailable metadata returns nonzero and prints no success path. The file
is retained; use `-o` with a fresh directory to replace an older low-quality
download without overwriting it. This check uses fresh metadata, not an old
sidecar, and has 60-second probe and 180-second extraction timeouts.

The script enables Node when installed; Deno remains enabled by yt-dlp by
default. Follow upstream version requirements. Verification means highest
resolution/frame rate **reported by the extractor**, not proof of every format
YouTube could offer, HDR/bitrate superiority, or full media integrity. Use the
live verifier for a full decode. A format-extraction warning deliberately makes
the quality result inconclusive instead of claiming success.

## Verification

```bash
python3 -m unittest discover -s tests -p 'test_yt_dl.py' -v
python3 -m unittest discover -s tests -p 'test_yt_dl_quality.py' -v
python3 tests/check_yt_dl_live.py
```

Offline tests run without network access or installed downloader dependencies.
The additional quality-selection tests require the yt-dlp Python package in the
chosen Python environment (otherwise they explicitly skip). They exercise its
real selector against a 1080p MP4 / 4K WebM ladder with competing audio streams
and a combined-only fallback; no network or media download is involved.
The opt-in live check downloads the supplied video into a fresh `/tmp/yt-dl-live-*`
directory and retains the files. It checks ID, file size, video/audio streams,
duration within two seconds or 1% of source metadata, and a full ffmpeg decode.
The download and decode each have a 15-minute timeout. A platform/network error
fails the check; it is never reported as a passed media verification.

The chezmoi source is `scripts/executable_yt-dl`, installed as executable
`~/scripts/yt-dl` on GUI-enabled hosts. Run `refresh-config` to apply source
changes. For direct checkout execution, use `./scripts/executable_yt-dl`.
The script does not add a shell alias or alter the system PATH.

The installed yt-dlp 2025.10.22 failed the supplied URL with HTTP 403 during
verification. An isolated yt-dlp 2026.8.19 downloaded it successfully; see the
[live-download incident record](postmortem/2026-09-18-yt-dl-live-download.md).
Before the highest-quality selector revision, all live checks passed, including
full decode: 1,395,213,482 bytes, audio and
video streams, and 6351.238095 seconds versus source duration 6351 seconds.
The retained file is `/tmp/yt-dl-live-xurxudir/oLOzkH0zVZo.mp4`.
That version warned that no supported JavaScript runtime was enabled, so some
formats might be unavailable. Install a supported runtime following the upstream
instructions for reliable access to all formats.

After the highest-quality revision, a live format-selection check on the same
URL selected AV1 1080x1920 at 30 fps plus Opus audio (399+251), matching the
highest resolution listed by the extractor. The check used current yt-dlp with
Node enabled and did not download another copy; the prior MP4 remains unchanged.
All 15 CLI and real-selector tests passed in that runtime. See the
[plan](../plans/youtube-downloader.md) for exact commands and evidence.

## Handoff

The [implementation plan](../plans/youtube-downloader.md) records evidence and
remaining live-test limitations. Suggested commit: `feat: add tested YouTube downloader`.
For Cursor review: “Review scripts/executable_yt-dl and tests/test_yt_dl.py against
docs/yt-dl.md; run the offline suite and inspect live verification evidence in
plans/youtube-downloader.md. Preserve unrelated dirty changes and report
concrete correctness issues.”

The installed executable was updated to 2026.08.19 on September 19; see the
[installed-version follow-up](postmortem/2026-09-19-yt-dlp-installed-version.md).
