# yt-dl installed without execute permission

- Symptom: Fish found `~/scripts/yt-dl` but refused to execute it.
- Impact: The normal PATH command failed and the installed copy was stale.
- Evidence: Installed mode 0644; tracked source mode 100755. At diagnosis, a user rename left `scripts/yt-dl` deleted and identical content at `scripts/executable-yt-dl` (hyphen).
- Root cause: chezmoi requires the `executable_` source attribute; Git execute bits alone do not express the installed mode. The hyphen spelling is not that attribute. Prior tests only exercised the checkout.
- Status: Resolved. Preserved source content and renamed it to `scripts/executable_yt-dl`; updated test and documentation references.
- Verification: Isolated chezmoi apply failed before the rename and passed afterward; all 24 downloader tests pass. `refresh-config` exited 0. Fish resolves `~/scripts/yt-dl` and `yt-dl --help` exits 0. Installed mode 775 and bytes match source. No unrelated refresh changes.
- Follow-up: Keep the real deployment regression test. See the [plan](../../plans/youtube-downloader.md).
- Tooling: Initial reads assumed nonexistent paths and returned errors; subsequent file discovery found the actual refresh function. `chezmoi source-path` confirmed the original target was unmanaged after the pending rename.
