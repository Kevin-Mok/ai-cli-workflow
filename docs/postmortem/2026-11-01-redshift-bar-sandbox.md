# Redshift bar live inspection sandbox restriction

Live bar inspection needs access to the desktop session. Use the approved elevated route to apply configuration and inspect i3.

- Symptom: ordinary fish startup attempted writes to fnm multishells, universal variables and aliases on a read-only filesystem; i3-msg could not connect to the desktop IPC socket (Operation not permitted).
- Impact: initial live inspection failed; no bar configuration had been edited.
- Lookup: searched `sandbox i3 socket fish read-only`; execution-environments.md#ext-sandbox-loopback recommends scoped approved execution. Applicable to access boundaries, not proof of a bar defect.
- Evidence: fish startup reported read-only filesystem; i3-msg exited 1 on /run/user/1000/i3/ipc-socket.6605.
- Status: live verification pending; use fish --no-config for inspection and request scoped elevated execution for refresh and i3 IPC.
- Next steps: add the existing Redshift block to HDMI-0 main config, refresh, validate and reload, then inspect scheduler output.

- Follow-up evidence: approved refresh-config exited 0, but live wrapper output still lacked Redshift. `chezmoi source-path` reported the bar file not managed; migration-preserved targets exclude it from refresh. Reload retained the existing status-command process.
- Resolution approach: preserve the live file and insert only the same four-line block directly; restart i3 in place so its unchanged status command restarts. Do not alter migration exclusions.

- Resolved: approved direct insertion and i3 in-place restart succeeded. Fresh deployed wrapper emitted Redshift, volume, calendar; target was 1700 K with no error. The right-screen i3blocks process started at 19:01:47 after restart. i3 config validation exited 0 with existing wheel-command deprecation warnings.
- Verification: defining placement assertion observed expected RED before edit and GREEN after edit. Redshift block tests 7/7 and status-wrapper tests 21/21 passed. Refresh exited 0; migrated target requires direct synchronization for persistence in this installation.
- Learning: no new reusable finding; existing permission-boundary and unchanged-status-command activation guidance apply. Register this report with an explicit no-new-learning decision; targeted ledger check follows.
- Limits: physical visual placement and mouse wheel interaction were not observed. Current temperature was preserved; no temperature adjustment was performed.
