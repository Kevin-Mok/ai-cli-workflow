# Left monitor DND block absent

The left monitor had no notification status control. This report records the
missing bar entry, the minimal configuration repair, and runtime verification.

- Symptom: DND script existed but no indicator appeared on the left monitor.
- Impact: Notification pause state and click control were unavailable there.
- Lookup: postmortem-memory search `dnd` returned no matching learning.
- Evidence: live output DVI-D-0 is at x=0 and uses bar-1 with
  `i3blocks-secondary.conf`; that configuration contains volume and calendar
  but no DND block. Commit eb903a2 added only the DND script.
- Cause: the script was delivered without a bar configuration entry.
- Resolution: added `[dnd]` with `interval=2` immediately before secondary bar volume
  in source and surgically inserted the same entry in the live preserved file.
- Status: verified runtime repair; broad refresh remains blocked by unrelated
  work in `scripts/media-screensaver`. No conflict was overwritten.
- Verification: the executable protocol reproducer first failed with
  `Left bar protocol has no DND block`; after the change it emitted
  `<span color='#6b7a8f'>notif</span>`. `i3-msg reload` returned success, the
  secondary i3blocks process restarted, and `dunstctl is-paused` stayed false.
  No click/toggle or screenshot verification was performed.
- Diagnostic limitations: sandboxed i3 IPC was denied; approved host inspection
  succeeded. An initial source read omitted the `.tmpl` suffix; the exact
  tracked path was then confirmed. The first protocol reader assumed a separate
  array-opening line; the installed i3blocks emits `[[]` on one line, so the
  reader was corrected before recording RED. A refresh invocation also tried
  sourcing a nonexistent sync-shortcuts function; refresh itself subsequently
  stopped at the existing media-screensaver conflict.
- Configuration boundary: chezmoi explicitly preserves this target via
  `migrationPreservedTargets`; refresh cannot deploy this particular entry.
  Live file content was preserved apart from the three-line DND insertion.
- Documentation: updated the existing notification smoke check to cover the
  left bar indicator and restore state after a manual two-click check.
- Follow-up: resolve the unrelated media-screensaver conflict in its owning
  task before rerunning the full refresh. Rollback removes only the DND stanza
  from source/live secondary configuration and reloads i3.
- Learning review: no new general finding; this is a specific omitted bar
  entry repaired with the existing script. Register this report's final hash
  with an explicit no-new-learning decision.

- Placement correction: moved DND immediately left of volume in source and
  live configuration. Fresh protocol output verified adjacent DND then volume;
  i3 reload succeeded. Required refresh again stopped at the same unrelated
  media-screensaver conflict.

- Commit privacy review: the staged ledger alias triggered the home_path
  category. The public candidate uses the repository-standard neutral home
  placeholder; no machine-specific alias will be published. The sanitized candidate was prepared for recheck.
