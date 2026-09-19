# Download progress hidden

- Symptom: `yt-dl` appeared idle during video downloads.
- Root cause: wrapper explicitly passed `--no-progress`; print mode also implies quiet output.
- Impact: no completion percentage, transfer speed, or ETA visible.
- Resolution plan: explicitly enable progress with quiet mode so stderr streams progress while stdout remains the final path. Add fetching and quality-check status messages.
- Status: Resolved. All 25 downloader tests pass; real local yt-dlp transfer reaches 100%, refresh-config succeeds, and installed bytes match source.
- Verification: run downloader tests, real yt-dlp local-transfer progress check, refresh-config, and installed-source comparison.

- Live validation initially failed: real yt-dlp returned success but stderr lacked the expected progress percentage. Mocked CLI tests alone did not establish the stream behavior. Investigating actual progress output before completion. Refresh completed successfully.

- Final resolution: native progress is stdout, so forward child stdout directly to parent stderr and use --print-to-file for the final path. Temporary reports are automatically cleaned. The corrected real-transfer check passed.
- Follow-up: Preserve realistic external-tool stream behavior in tests; current running processes retain their old code.
