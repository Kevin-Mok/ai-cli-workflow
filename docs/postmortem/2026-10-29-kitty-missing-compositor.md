# Kitty transparency missing compositor

Kitty transparency requires a running X11 compositor. This investigation checked configured opacity, live compositor ownership, and restored the existing Picom configuration.

## Symptom and impact

Kitty appeared opaque in the supplied screenshot. Both tracked and installed kitty.conf specify background_opacity 0.9.

## Lookup and evidence

Searched postmortem memory for kitty transparency opacity compositor. Related wallpaper-startup guidance applies only to distinguishing startup configuration from live activation; no retrieved remedy established this incident. tasks/lessons.md also warns that subtle opacity can be imperceptible.

Sandbox process listings hide host processes and X11 access fails there; host inspection was performed with approved escalation. The inherited KITTY_LISTEN_ON socket was stale, so an existing live socket was used for the color check.

Before restoration, host pgrep found neither Picom nor Compton. XGetSelectionOwner for _NET_WM_CM_S0 returned 0. This is the executable reproducer for missing compositing.

## Resolution and verification

Started picom --daemon --log-file /tmp/kitty-transparency-picom.log. It exited 0; pgrep showed PID 387034 and compositor selection owner became 41943044. The log was empty. A fresh desktop screenshot was captured at /tmp/kitty-transparency-restored.png. Root wallpaper pixmap exists and live Kitty background is #18202a.

## Status and limits

Live compositing restored; no persistent configuration changed. scripts/executable_ubuntu-start already starts Picom when absent. Why the prior compositor exited or did not start remains unresolved. Visual wallpaper visibility at 90 percent opacity requires user acceptance; no opacity adjustment was made. No refresh-config required because configuration was unchanged.

## Follow-up

If recurrence occurs, inspect the Picom log and graphical-login startup path. No new reusable remedy beyond the existing principle of verifying live activation; record this runtime evidence without promoting an unverified startup fix.

## Follow-up: existing windows stayed opaque

User confirmed Picom was running but transparency remained absent. Live remote-control ls showed several older instances at background_opacity 1.0 despite configured 0.9, while others reported 0.9. Reloading one affected instance (socket kitty-4172511), enabling dynamic opacity and explicitly setting 0.8 with --all did not change its reported 1.0. Its X visual depth was 32. Thus restoring the compositor alone did not repair existing opaque windows.

A disposable new Kitty instance launched after Picom with background_opacity=0.7 reported 0.699999988079071. User explicitly confirmed this window worked in transparency. Working new windows versus unchanged old windows supports initialization-time compositor state as the cause; exact Kitty internals were not established. Existing sessions were not terminated. New windows can be opened now; affected sessions require a controlled reopen/resume. The disposable sleep-based probe exits after 120 seconds. No persistent opacity setting was changed.

Additional diagnostics: frozen Kitty Python source cannot be recovered with inspect.getsource; no code remedy inferred from this failed inspection. A guessed filesystem source location was absent. Runtime introspection and native remote-control ls provided the actual evidence instead.
