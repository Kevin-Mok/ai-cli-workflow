# Restore five-minute idle screensaver

Make automatic playback start after five idle minutes when no video plays on the middle 4K monitor. Inspect the existing service and browser detector, repair activation, then verify gate status without interrupting user media.

## Scope and decisions

Existing code already implements 300 seconds, strict middle 3840x2160 gating, physical-input dismissal and video-only playback blocking. Side-display video and audio do not block. Runtime shows service active and DP-2 at 3840x2160, but automatic activation is suppressed because the browser bridge is unavailable. Preserve the earlier staged delay-shortcut work and all unrelated dirty files. No commit/push authorized by this follow-up; prior automatic-review rejection still applies.

## Checklist

- [x] Capture dirty state; inspect service, monitor geometry, existing behavior and browser/native registration.
- [ ] Reconnect detector in actual desktop Chrome profiles without bypassing unknown-video protection.
- [ ] Verify current gate, idle threshold and persistence; update smoke documentation if activation procedure changes.

## Evidence, risk and rollback

Live `media-screensaver status --plain`: idle monitor running, browser bridge unavailable. systemctl: active/running since 10 AM. xrandr: middle DP-2 3840x2160. Chrome Default registers the correct unpacked extension path; native messaging manifest/host exist and origin matches. No current native-client state is in the user runtime directory. Actual Chrome has no remote-debugging launch flags; attempt native auto-connect via dedicated browser-control session. Do not weaken the fail-closed gate or edit browser preferences while Chrome runs.

Existing postmortem lookup: `screensaver browser bridge unavailable extension Chrome`; scheduled-visibility guidance applies to explicit scheduled playback only, not automatic gate bypass. Discovery guidance applies to a mistaken read of nonexistent install.py; actual installer is in main.py. Before any source behavior change, add and observe defining RED test. Rollback runtime changes by restoring extension state and stopping only this service if needed. Tests and installed GUI acceptance remain pending.

## Handoff

Atomic plan: restore real bridge; verify no video/4K video/side video and 300-second idle matrix; retain existing shortcuts. Cursor prompt: Restore media-screensaver Chrome bridge coverage without weakening uncertainty checks, preserve all staged work, verify status and five-minute behavior. Intended commit if separately authorized: `fix(screensaver): restore idle video detection`.

Live diagnosis: actual desktop Chrome is not attachable through the available browser controls; dedicated auto-connect returned BRIDGE_NOT_READY, and computer-use inventory has no connected surfaces. Opened the detector details in actual Chrome. Asked user to enable/reload the detector in Default, Profile 7 and Profile 15, then reload normal tabs. This required UI step remains pending; do not claim restoration. Headless automation browsers have no native windows needing coverage. Updated existing guide/smoke entry to explain protected active tabs and per-profile setup.

Fresh checks: bridge tests 15 passed; desktop matching tests 3 passed; browser JS tests passed. CLI tests initially hit read-only preview.lock; isolated /tmp XDG_RUNTIME_DIR rerun passed all 6, including 300-second threshold. No source behavior changed, no production runtime state changed, no additional staging/commit/push.

Repeat complaint: fresh journal confirms >5m idle (318 through 409 seconds) with every launch suppressed by unavailable browser bridge; service remains active/running. No source/runtime changes made this turn. Asked user to confirm detector enablement across open profiles; waiting for required UI activation/confirmation before further dependent work. Prior focused tests are previous-turn results.

Superseded by explicit user choice of screen watching with i3bar excluded. See `plans/screensaver-screen-motion.md` for implemented/deployed local motion policy; Chrome bridge remains optional for manual playback. Original user-visible idle block resolved by removing the automatic Chrome prerequisite, not by claiming extension repair.

Sessiondelivery: include this supersededinvestigationrecord alongside theimplementeduserapprovedmotionpolicy under explicitcommit-session authorization. No claim thatoptionalChrome bridge was repaired.
