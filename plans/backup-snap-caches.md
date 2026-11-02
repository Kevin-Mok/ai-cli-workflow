# Exclude Snap caches from backups

Keep disposable Snap application caches out of full and home backups while retaining settings and project data.

## Scope and decisions

Existing backup and home inventory already exclude top-level user caches. The October backup log shows Spotify's Snap cache was copied. Exclude only user Snap app revision/common .cache contents; preserve .config and project caches. Update copy, inventory, preview, documentation, exclusion lists and tests together. Existing dirty postmortem-memory files are unrelated and protected.

## Checklist

- [x] Inspect backup behavior, logs and initial git status.
- [x] Add a real home-copy/inventory test and observe expected failure.
- [x] Align rsync and inventory exclusions; update lists and documentation.
- [x] Run focused and broader checks, check installation and record results.

## Risks and verification

Do not exclude persistent Snap settings, data or project caches. Use fixture rsync plus inventory comparison; verify restore copies with exclusions disabled. Check generated policy, suite, smoke docs and installed deployment. No real backup or source data removal.

RED: unittest failed because alice/snap/spotify/common/.cache/data was copied.

## Evidence and review

RED: real copy retained Snap cache. GREEN: focused test passed. The 69-test host backup suite passed after correcting an existing unrelated fixture's example/alice path mismatch; sandbox ACL/PTY behavior differs from host. Incident: docs/postmortem/2026-10-31-backup-cache-suite.md. Exclusion preview lists the Snap cache rule. Targeted chezmoi apply installed only the backup script and two exclusion lists; compare installed bytes with source. Full refresh-config was not run because its unrestricted apply would also publish unrelated pending skill and documentation changes in this concurrently dirty checkout; targeted apply preserves that work. No live backup or restore boot was performed.
