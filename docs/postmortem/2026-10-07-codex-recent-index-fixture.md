# Recent index reuse fixture compared unstable ctime

The new reuse test treated cache ctime as proof of rewriting. Compare cache content, mtime and inode while keeping full source immutability checks.

- Date: 2026-10-07.
- Symptom/impact: Initial index GREEN run passed seven defining tests and failed the eighth because cache ctime changed; no source data changed.
- Lookup: `cache ctime chmod fixture` found `local-fixture-mtime-after-writes`, but its mtime-after-write cause does not directly apply. Inspection showed only signature element 2 (ctime_ns) differed; size, mtime_ns, device and inode were stable.
- Root cause: Existing `secure_file` permission hardening calls chmod(0600) on cache reuse, which updates ctime without replacing cached content. The assertion was overspecified.
- Resolution: Assert unchanged bytes, size, mtime, device and inode plus private modes for reuse. Preserve full signature/bytes assertions for original sessions. No production behavior was changed for this fixture.
- Verification/current status: All eight defining index tests pass; all 29 prior CLI tests pass through a disposable entrypoint importing the new index module. Runtime cache reuse verified with the corrected observables.
- Follow-up/learning: Cache ctime is not content-reuse evidence when permission hardening calls chmod. Record this distinction as fixture guidance, preserve source immutability checks, and run the targeted learning check.
