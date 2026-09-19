# YouTube downloader

Run from the repository checkout (Python 3.9+, current yt-dlp, and ffmpeg on
PATH; ffprobe is also required for the live verification). No sudo is needed.
The wrapper does not install or update dependencies. Follow the
[yt-dlp installation instructions](https://github.com/yt-dlp/yt-dlp#installation)
for your environment, including its current JavaScript runtime requirements.

```bash
./scripts/yt-dl 'https://www.youtube.com/watch?v=oLOzkH0zVZo'
./scripts/yt-dl 'https://www.youtube.com/watch?v=oLOzkH0zVZo' --output-dir /tmp/my-videos
./scripts/yt-dl --help
```

The default directory is `~/Downloads/yt-dl`. `-o` abbreviates `--output-dir`.
Watch, youtu.be, shorts, live, and embed video URLs are accepted. Playlist-only
URLs are rejected; playlist and tracking parameters on video links are removed.
Only one video is downloaded. Ambient yt-dlp configuration is ignored; no
browser cookies are read.

The script uses `bv*+ba/b`: yt-dlp's best available video, adding its best
audio-only stream when the video does not already contain audio, with a combined
format fallback. There is no resolution cap or MP4/M4A preference. Quality is
ranked by yt-dlp across the formats its extractor makes available; see the
[upstream selection rules](https://github.com/yt-dlp/yt-dlp#format-selection).
Separate streams merge into MKV without transcoding or quality loss. A combined
download keeps its original container. Files use the video ID, e.g.
`oLOzkH0zVZo.mkv`, alongside an `.info.json`
metadata sidecar. Existing media and sidecars are not overwritten. Partial
downloads may remain for yt-dlp to resume. Keep output outside the repository.
Use a fresh output directory when upgrading an earlier download's quality:
existing same-name media is preserved, not automatically upgraded.

Success prints one absolute final media path to stdout. Diagnostics go to
stderr. Exit codes: 0 success, 2 argument error, 1 missing dependency/local
error; downloader failures preserve yt-dlp's nonzero code, and interruption
returns 130. Existing files are checked for presence and size, not revalidated
by the normal download command. Use the live verifier for media integrity.

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

The script's exact source filename is `scripts/yt-dl`, as requested; run it from
this checkout. It does not add a shell alias or alter the system PATH.

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
For Cursor review: “Review scripts/yt-dl and tests/test_yt_dl.py against
docs/yt-dl.md; run the offline suite and inspect live verification evidence in
plans/youtube-downloader.md. Preserve unrelated dirty changes and report
concrete correctness issues.”
