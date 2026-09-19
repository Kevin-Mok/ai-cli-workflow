# YouTube live download rejected

- Date: 2026-09-18.
- Symptom: `python3 tests/check_yt_dl_live.py` exited 1: YouTube media request returned HTTP 403 Forbidden.
- Impact: Initial live verification was blocked; final download and full media verification now pass.
- Evidence: yt-dlp 2025.10.22 warned about outdated extraction and missing SABR format URLs; output directory `/tmp/yt-dl-live-b4zas67f`.
- Root cause: The old downloader's media request was refused. Updating the isolated downloader resolved it; the exact upstream extraction difference was not isolated.
- Resolution: Retried with yt-dlp 2026.8.19 in `/tmp/yt-dl-runtime-SkdJyn/venv`, without changing installed user/system packages or using cookies.
- Status: Resolved for this task; the user's older installed version is unchanged.
- Verification: `PATH="/tmp/yt-dl-runtime-SkdJyn/venv/bin:$PATH" python3 tests/check_yt_dl_live.py` exited 0 with PASS. Media `/tmp/yt-dl-live-xurxudir/oLOzkH0zVZo.mp4` is 1,395,213,482 bytes, ID matches, audio/video streams present, duration 6351.238095 seconds versus source 6351 seconds, full decode passed.
- Follow-up: Use a current yt-dlp release for future downloads and follow upstream JavaScript runtime guidance; the successful retry warned that missing runtime support may hide formats.
