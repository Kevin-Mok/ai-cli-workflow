# Hevin idle playback loses to X11 blanking — 2026-11-17

Investigate a blank desktop instead of the Hevin screensaver. Reproduce the independent blanking timer, scope the existing display-awake helper to the idle service, then verify restoration and actual playback.

## Symptom and evidence

User reports blank screens instead of Hevin media after inactivity. Live xset reports screensaver600s and DPMS600s, still enabled. New local-motion daemon logs quiet0–152s before physical input reset, without any automatic playback launch. The daemon starts independent clocks on restart and does not hold display-awake inhibition while waiting or during automatic playback. Scheduled playback already has that helper.

## Lookup and hypothesis

Read tracked postmortem-memory before remedy. Query screensaver blank automatic XScreenSaver inhibition matched local-scheduled-screensaver-visibility in operational-drift.md. Existing helper clears an active server blank and holds connection-scoped inhibition without changing configured timeouts. Hypothesis: independent server blanking can win before the restarted daemon's300-second eligibility, and later blank active automatic playback. The user's exact blank event has not been timestamped; reproduce the interference under disposable Xvfb before fixing.

## Status and next steps

No fix claimed yet. Add one-second blanking/daemon-wait reproducer, observe RED, then use scoped keep_awake during daemon lifetime, confirm restoration, deploy and start the requested real Hevin preview. Preserve deliberate screens-off/lock/suspend semantics and all prior staged work. No new generalized learning at this stage; existing inhibitor guidance applies.

## Reproduction, resolution and verification

One-second Xvfb blanking reproduced interference during daemon quiet wait: state1 instead of0 at2.2seconds. Wrapped idle daemon loop in existing connection-scoped keep_awake so it clears an existing server blank and owns automatic blanking while waiting/playing. Green reproducer proves no prematureblackout and original1-second setting returns after exit. Full4K Xvfbmedia suite68 passed; timer10 passed. No tracked XScreenSaver-driven locker startup was found; explicitlock/suspend checks remain. Blackout shortcuts already stopidle beforeforcedoff. Live installation and realHevin playback pending; exact userblank timestamp remainsunknown.

## Installed outcome

Deployed only reviewedmain.py, ran scopedrefresh successfully, restartedidle and startedexistingHevin playbackservice. Both active/running. Journal confirms5989 media items, activeconveyor at0/10/20seconds withzero skipped; X11 confirmsvisible7808x2160 Media conveyor screensaverwindow. Screensaver andDPMSconfiguredtimeouts remain600seconds, monitoron. No personalimages persisted. Scoped live fix andactualHevin playback verified; uninterrupted5-minute autoactivation and10-minute live soak remain separate. Prior main backup is /tmp/hevin-blanking-backup-s_nggbzv/main.py.
