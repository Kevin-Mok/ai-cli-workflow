# Installed YouTube downloader still outdated

- Date: 2026-09-19.
- Symptom: The user's quoted URL reached yt-dlp 2025.10.22 but media downloading returned HTTP 403, with outdated-version and SABR warnings.
- Impact: Normal `scripts/yt-dl` use still fails despite the prior successful isolated-runtime test.
- Evidence: `command -v yt-dlp` resolves to `/home/example/.local/bin/yt-dlp`, an official-style Python zip executable; `yt-dlp --version` reports 2025.10.22. See [previous incident](2026-09-18-yt-dl-live-download.md).
- Root cause: The obsolete installed extractor remained in use; the previous fix only updated a temporary environment. Updating the installed executable resolved the same URL with the unchanged wrapper; the precise upstream extraction change was not isolated.
- Status: Resolved. `yt-dlp -U` updated the installed executable to 2026.08.19, and the original wrapper completed the supplied URL with exit 0. Subsequently changed the default destination at the user's request.
- Verification: Download completed with exit 0; video and sidecar moved without overwriting to `/mnt/linux-files-3/yt-vids`. ffprobe exited 0: 3840x2160 video, audio present, duration 3595.248 seconds, 4,522,234,467 bytes. No full decode was performed.
- Follow-up: Keep the installed dependency current; separately address the JavaScript runtime warning for complete format availability.
- Tooling: Initial sandbox reads failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; approved escalated reads succeeded. A discovery command returned 1 because no nested instruction files matched; this was not a downloader failure.

- Runtime check: Node v22.15.0 is installed, but the wrapper ignores ambient configuration and does not explicitly enable Node. Deno is absent. The updated downloader warns that some formats may be missing; this remains a separate limitation.

## Automatic verification follow-up

At the user's request, `scripts/yt-dl` now runs ffprobe and fresh format
extraction before reporting success, including for pre-existing files. Node
is explicitly enabled when installed. The supplied video passed at
3840x2160 / 23.976 fps with audio and no extraction warnings. Selection now
prioritizes resolution and FPS consistently with verification. See the
[implementation plan](../../plans/youtube-downloader.md). No full decode was repeated.
