# Keep Hevin playback visible instead of X11 blanking

Make the idle service own display blanking while it is running, so the five-minute screen/input policy launches Hevin media instead of an older X11 timeout turning displays black. Verify the competing timer under Xvfb, reuse the existing scoped inhibitor, then deploy and check real Hevin playback.

## Context, decisions and scope

User reports a black display instead of the Hevin conveyor. Live settings still enable X11 blanking and DPMS at600s; the newly restarted idle monitor starts its own300-second clocks. Logs show no automatic launch yet and quiet progress only to152s before input. Separate clocks can let the older server timeout blank first; automatic playback also lacks the existing scheduled-only keep_awake scope. Existing media root remains /mnt/linux-files-3/hevin.

Reuse desktop.keep_awake for the idle service lifetime, including quiet waiting and owned playback. This is explicitly for replacing blanking with the requested screensaver. Releasing/stopping service restores prior blanking; do not globally change timeouts, disable locks, change suspend, or weaken i3bar/motion policy. Blackout shortcuts stop the idle service first, so deliberate screens-off behavior remains available. Preserve all prior dirty and staged work; no commit/push.

## Checklist

- [x] Capture dirty state and inspect live status/logs/blanking settings.
- [x] Reproduce blanking during daemon quiet wait with one-second Xvfb timeout; observe RED.
- [x] Reuse scoped inhibitor for daemon lifetime; confirm GREEN/restoration and relevant regression checks.
- [x] Update docs/smoke checks, deploy only changed main module, refresh scoped configuration, restart service and verify actual Hevin preview.

## Verification and rollback

Disposable Xvfb test must prove no black screen during idle wait and original blanking returns after exit. Existing scheduled inhibitor, input/lock policy, media rendering and motion tests remain relevant. Live checks compare installed source bytes, active service, same xset timeouts and Hevin process/logs; no personal screenshots persisted. Full uninterrupted5m acceptance is distinct from immediate playback. Roll back installed main to saved pre-fix copy and restart.

## Review and handoff

Lookup query: screensaver blank automatic XScreenSaver inhibition; matched local-scheduled-screensaver-visibility. Its existing connection-scoped inhibitor and blank-reset behavior applies; extend ownership to the user-requested idle-service lifetime rather than change global timeout configuration. Cursor prompt: Verify Hevin idle service suppresses X11 blanking while waiting/playing and restores it on stop, using disposable Xvfb and no saved personal images. Suggested commit: fix(screensaver): prevent blanking before Hevin playback.

RED: disposableXvfb daemon-wait reproducer failed in2.25s with XScreenSaver state1 instead of0, proving prematureblanking whilewaiting. Source now wraps daemonloop in existingkeep_awake; GREEN/full regressions pending. Updated guide/README/smoke checks to state lifetime ownership and restoration, notglobaltimeoutchanges.

GREEN: daemon-wait Xvfb test passed4.46s, proving unblanked wait and original1s blanking restored afterward. Full4K Xvfbmedia suite68 passed; timer10 passed. Review found no tracked auto-lock wiring conflict; explicitlock checks retained, blackout shortcuts stopservicebeforeforcedoff. No globaltimeouts rewritten. Pending scopedmain deploy and requestedactualHevin playback.

Live delivery: main.py deployed only after confirming installed file differs exactly by this fix; rollback backup `/tmp/hevin-blanking-backup-s_nggbzv/main.py`. Scoped refresh exited0; idle and existing daily playback services active/running. Started requestedHevin preview through existing daily service (schedule unchanged). Journalfound5989 media items and conveyoractive0/10/20s, zero skipped. X11 confirms visible7808x2160 Media conveyor screensaver window acrossallthreeoutputs. xsetstillreports600s screensaver/DPMSsettings and monitoron; no globalsettingrewrite. No saved screenshots, commit orpush. Remaining unobserved: uninterruptedphysical5m automatictrigger and10m realblanking soak; acceleratedXvfb restoration test passed.

## Session commit delivery

Explicit `$commit-session` authorizes the session-owned commit and origin/main push, resolving the earlier automatic-review authorization blocker. Scope helper returned unsafe: no successful repo-writing actions detected because tool-orchestrated Python writes were not attributed. Use the captured initialdirty baseline plus directlyobservedwrites; scope20 files with mixedREADME/aliases/smoke/ledger rebuilt fromHEAD and ourdelimitablechanges. Exclude unrelatedxhpp alias, other-sessionreport andallotherpreexistingwork. Match all implementation/docs/tests/plans/reports in one coherentcommit.

Final validation: fresh fullmedia/timer/JS run requested; previous68media+10timerpassed and actualHevinplaybackverified. Atomicplan andCursorprompt above remainreproducible; rollback scopedcommit andrestoreinstalledmain ifneeded. Intendedsubject: feat(screensaver): add local idle detection and delayed playback. Push once afterverifiedcommit; reportactualhash/outcomeinconversation.

Commit milestone ready: final fresh validation passed 68 media tests under isolated4K Xvfb,10timer tests andbrowserJS. Candidate includes20 directlyattributedfiles, includingonlysofs alias hunk andsessionreportledgerentries. No implementationblockers; nextsteps exactstagedreview, privacygate, focusedcommit andoneorigin/mainpush. Unrelateddirtywork remainsuntouched; commitSHA/pushresult reportedinconversation.
