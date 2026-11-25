# Show Redshift first on all monitors

Show the shared thermometer first on every configured bar, including the
laptop and an external display. Preserve existing bar routing, block order
after the thermometer, and the status wrapper that queues wheel events.
The source templates and docs already have local edits. Keep edits scoped to
the Redshift stanzas and their documentation. For rollback, restore those
hunks and the affected installed config backups, then reload i3.

- [x] Reproduce the order failure across the three bar templates.
- [x] Make Redshift unconditional and first, then update the README and smoke checks.
- [x] Verify the rendered configs, run i3blocks and Redshift tests, and check the live bars after reload.

Postmortem lookup for “i3blocks missing Redshift middle bar” found the verified
wheel-queue finding. It applies to interaction through the existing wrapper.
The live 4K config began with volume. The remedy adds the block at the
configuration boundary and retains the existing wrapper.

The pre-change rendered config check exited 1. Both the middle and main
desktop bar configurations started with volume. The secondary started with
Redshift.

- After the change, `chezmoi execute-template` rendered Redshift first and
  exactly once in all three configs. The i3blocks suite passed 80 tests and
  the Redshift suite passed 13.
- The expected `refresh-config` conflict guard stopped on the local 4K
  template target. The scoped live update backed up the two changed files
  to `/tmp/i3-redshift-all-bars-_2kodal4`, then `i3-msg reload` succeeded.
- Live i3 IPC showed bars on HDMI-0, DVI-D-0, and DP-2. Their installed
  status commands each emitted Redshift first at 2300 K. Physical monitor
  inspection and wheel gestures remain manual.

## Commit milestone

`fix(i3): show Redshift first on every monitor` adds the left-bar stanza to
the upstream configuration. The upstream main and 4K templates already
put Redshift first. The commit keeps the session's usage and smoke
documentation, scheduler assertion, and live-verification postmortem
with the change. The previously dirty volume and calendar changes and
the other three local commits stay outside this delivery.

In the isolated delivery checkout, all three rendered configs started with
Redshift, and 79 i3blocks and 13 Redshift tests passed. The linked incident
passed the ledger check at its registered canonical path.
