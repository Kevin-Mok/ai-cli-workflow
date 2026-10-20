# Media screensaver runtime and integration probes

This records desktop access during the media conveyor implementation and the scoped workaround used to inspect and verify it.

## Symptom and impact

On 2026-10-20, `xrandr --listmonitors` inside the default command sandbox returned status 1, “Can’t open display :1”. Live geometry could not be verified there. No display configuration was changed.

## Lookup and diagnosis

Read the tracked postmortem-memory skill and searched `X11 cannot open display sandbox unix socket`. Existing execution-environment guidance recommends scoped escalation for sandbox restrictions, but no finding establishes this exact X11 symptom. DISPLAY=:1, the authority file and /tmp/.X11-unix/X1 exist.

## Resolution and verification

The same read-only command with require_escalated exited 0 and reported three enabled monitors: DVI-D-0 2048x1152+0+504; DP-2 3840x2160+2048+0; HDMI-0 1920x1080+5888+540. This is a verified workaround for inspection, not a sandbox repair. The real side-monitor vertical offsets differ from the saved layout script; implementation must consume live geometry.

## Status and next steps

Inspection unblocked. Use scoped escalation for necessary live X11 checks; retain ordinary sandboxing for source and offline checks. Do not run the layout-changing script. No new reusable learning beyond established scoped-escalation guidance; record this report as a no-new-learning source.

## Idle extension probe

An exploratory import of `Xlib.ext.screensaver` failed with ImportError (exit 1): the installed Python Xlib package does not expose this extension. This invalidated that adapter choice before implementation, without changing the desktop. Postmortem search `Xlib screensaver ImportError` had no applicable exact remedy. Use standard-library ctypes with installed libXss instead; runtime verification remains pending. This is a dependency capability finding, not a repaired Python Xlib installation.

## Missing configuration probe

A combined read-only probe confirmed xvfb-run exists, then attempted to read `.chezmoi.toml.tmpl`, which does not exist (sed exit 2). The repository mapper already located the actual chezmoi source/config conventions, so this unnecessary filename assumption was abandoned. No file or configuration changed. No new learning beyond mapping paths before reading guessed filenames.

## Xvfb integration attempt

The first post-implementation Xvfb renderer test run exited 1 with two errors: GTK and libXss could not open the X display even though xvfb-run created the test server. The original X11 sandbox symptom therefore also affects this integration route. Prior lookup and approved live-xrandr evidence apply; rerun the bounded synthetic test outside the sandbox before changing production code. No renderer fix inferred from this environment failure.

## Video widget startup integration failure

Approved Xvfb rerun initialized X11 and passed libXss read-only idle querying, but the real video test had no playback position after 1.2 seconds. GTK warned about a widget without a parent while drawing. The defining playback-continuity test remains red. Investigate GStreamer sink startup versus GTK parenting before changing code; no continuity claim yet.

## Synthetic HEIC encoder capability

Synthetic fixture generation failed before playback: libheif returned “Unsupported file-type: Unspecified” when requesting an HEVC encoder. Installed ImageMagick had already reported HEIC as read-only. This establishes decode-only capability, not a screensaver decoding failure. Search `HEIC encoder unsupported file type` found no exact remedy. Do not make the demo depend on an unavailable encoder; retain generated non-HEIC fixtures and verify HEIC decoding independently with a disposable public fixture or an original opened read-only. No personal media will be committed.

## Isolated browser launcher failure

The first headed chrome-devtools-axi isolated launch with local Chromium and --load-extension returned BRIDGE_NOT_READY because its attached CDP target disappeared. Existing user tabs were not touched. Browser worker is investigating the owned isolated launch; do not infer extension failure from CDP launcher readiness.

## Confirmed decoder checks

Synthetic probe decoded JPG, JPEG, PNG, WebP, MP4, MOV and MKV and skipped one corrupt MP4 without aborting (exit 0). Read-only conversion of one mounted HEIC succeeded (exit 0, decoded PNG 4,824,153 bytes) and SHA-256 of the original was unchanged. HEIC generation is excluded from the demo because this machine has no HEVC encoder plugin; HEIC reading works. Real escalated Xvfb renderer 2/2 passed after delayed startup correction.

## Refresh and repeated dismissal investigation

The required refresh-config was attempted with approval and stopped (exit 1), reporting a chezmoi apply conflict; private log /tmp/refresh-config.m9ZSyZRR.log. Diagnose exact conflict before any retry; preserve unrelated live state. Two bounded real previews exited successfully but dismissed on input at startup (<1 second), so full movement is still unverified. Repeated timing suggests a synthetic/startup idle reset rather than proving user activity; compare idle and pointer state before changing dismissal behavior.

Browser worker also reported an unsupported `search --compact` option (status 2); the tracked helper documents no such flag. Read-only AXI pages repeated BRIDGE_NOT_READY. These do not establish bridge-code failure; use documented helper syntax and inspect direct browser launch stderr.

## Full quiet-window preview interrupted

User confirmed a 35-second quiet window. Preview #3 reached the middle output: settled item #1 at elapsed10.759s with playback10.589s, then dismissed on idle reset at18.226s. No browser worker input was performed. Input identity was not recorded, so user movement versus software XResetScreenSaver is unresolved. XScreenSaver idle can be reset by players and is insufficient to distinguish specifically keyboard/mouse inactivity; inspect raw XInput events before claiming the side-video idle requirement. Full three-output journey remains pending.

A Python Xlib XInput2 capability probe also failed (ModuleNotFoundError for Xlib.ext.xinput); do not assume installed Python adapters exist. libXi ctypes is the proposed narrow alternative, governed by the new executable XResetScreenSaver-vs-raw-keypress reproducer.

## Review corrections and present status

Independent review found (1) live monitor metadata included `name`, rejected by the strict rectangle validator; defining CLI test failed, then projection fixed it; (2) geometry-only visible-window coverage could alias a hidden covered window with another uncovered profile; matcher now requires equal cardinality across all native/report windows and filters non-viewable matched windows from playback gating; (3) audio-only <video> with zero decoded dimensions was misclassified, now excluded by a tested helper; (4) sufficiently deep JSON escaped as RecursionError. This Python3.12 decoder accepts depth2200 and4000; a depth10000 reproducer failed, then normalization to ValueError fixed the fail-closed path. Browser UI scale measured1.40625 on the actual desktop; physical native geometry confirmed conversion within2px; worker calibrated numerical bounds/rectangles with defining tests.

A separate read-only raw-event observer saw251events in8seconds, dominated by physical Logitech mouse motion, plus wheel-related XTEST events. This supports real activity as a reason for the interrupted previews; no XTEST filtering or arbitrary input-ignore delay was added. Full journey remains pending a quiet desktop. Raw input independently fixes the verified software XResetScreenSaver distinction.

Full refresh stopped specifically because .config/mimeapps.list has local changes and chezmoi could not prompt on EOF. i3 is excluded from this machine’s chezmoi-managed set, so exact chezmoi cat reported not managed. The task installer now appends only its own tested startup line to existing live i3 configuration, preserving all other text. Full refresh remains blocked; no mimeapps overwrite/adoption attempted. Installed status verifies all three monitor names, idle monitor running, automatic activation suppressed for uncovered Chrome windows.

Browsers: downloaded CfT145 could not use the host sandbox; installed Chrome146 works sandboxed, but ignores removed --load-extension flag. Supported Puppeteer enableExtensions with pipe:true successfully loaded the real extension without disabling sandbox or changing normal profiles. Prior AXI readiness failures were launch/control-path issues, not proof of product failure. The isolated browser matrix is underway.

Learning decision: preserve this task-specific evidence, add the raw-input-versus-software-reset and boundary-projection lessons to tasks/lessons.md; no new broad postmortem-memory finding beyond existing strict-contract/environment guidance is needed. Final targeted hash check follows the final evidence update.

## Final resolution and verified scope

Real cross-origin iframe diagnosis found a classic content-script helper named `parent` had replaced the browser’s global parent WindowProxy through Annex B function hoisting. A NodeVM initialization/relay test failed before the helper rename, then passed; actual iframe and closed-shadow playback checks also passed. Unnecessary tabs permission was removed and the real extension remained healthy. A stale owned diagnostic host file after forced supervisor shutdown correctly suppressed activation; only the exact known dead diagnostic record was removed after PID verification. Graceful native cleanup is verified separately. A final X11 cleanup inspection raced a closing owned window (BadWindow); the production inventory already catches this ordinary window-close race, and the diagnostic was repeated with the same guard.

Final automated suite37/37 plus Node browser tests pass, including source-dependent lock-grab behavior (XI2.1), software idle-reset distinction, manual preview with unavailable runtime, browser-start dismissal and a real owned-child lifecycle at the300-second boundary. Actual35-second desktop journey passed with uninterrupted video timestamps, all pipelines released and identical display geometry. Actual mounted MKV/H264, MOV/H264 and MP4/HEVC frames decoded with original metadata unchanged; HEIC decoded read-only with original hash unchanged. Actual isolated sandboxed Chrome146 matrix passed20cases plus unavailable/disconnect/privacy checks. Full global activation correctly remains suppressed because ordinary user profiles were not enabled by this task.

Completed implementation/installation with remaining observational limits: no real five-minute idle wait or suspend/resume; conventional minimize is ignored by this i3 session, while non-viewable scratchpad filtering passed. Full refresh remains blocked by unrelated mimeapps local differences, preserved; scoped installation and i3 startup registration succeeded. All diagnostic content/screenshots are synthetic and temporary; no personal media was committed.

## Final refresh invocation correction

The final refresh invocation used `fish --no-config -c refresh-config` to avoid startup terminal colors. It failed127 because the clean shell does not load this machine’s custom function path. Earlier normal `fish -c refresh-config` resolved the helper successfully and stopped on the protected mimeapps conflict. Lookup `fish no-config refresh-config command not found` was performed before correction; the existing local lesson about callable fish functions/autoload applies. Use the already demonstrated normal invocation; no changes to refresh itself or shell configuration are needed. This invocation failure changed no home files.

The normal final `fish -c refresh-config` resolved the helper and again stopped1 on the exact protected .config/mimeapps.list local-change prompt/EOF (private log /tmp/refresh-config.T86uYBNB.log), confirming the existing blocker without adopting/overwriting that file. Lookup reference local-discover-paths-before-reads explicitly identifies refresh as a Fish function; no duplicate learning entry is needed. Final browser cleanup receipt was independently read: no owned browser processes/windows, all five synthetic HTTP ports closed, and no bridge records remain. Installed launcher plus9 package files match source byte-for-byte; legacy slideshow and display-layout scripts have no diff; git diff --check exits0.

## Session commit validation

The exact staged privacy gate blocked one home_path finding in the memory ledger; staged whitespace validation also found a trailing blank line in desktop.py. Lookup `privacy gate home_path public alias` matched local-privacy-reviewed-content-approvals: public aliases require a separate machine-path mapping. No policy exception is needed. Publish only this report's neutral example-home alias; retain its actual machine alias locally alongside unrelated unstaged ledger work. Remove the extra blank line. These are packaging corrections, with no executable behavior change. The staged privacy and whitespace checks must pass before committing. Existing reviewed guidance covers this outcome; no new general finding.
