# Dual-jack diagnostic access and path assumptions

Desktop audio inspection required access outside the command sandbox. Read-only diagnostics recovered with scoped desktop access; the user subsequently confirmed both physical outputs worked.

## Symptom and impact

Sandboxed `wpctl status` returned exit 2, `Could not connect to PipeWire`. `amixer -c 2/3` could not access the cards; sandboxed `aplay -l` reported no soundcards. These were diagnostic-access failures, not evidence that desktop audio was broken. Initial file reads also guessed nonexistent `dot_config/fish/functions/ubuntu-startup.fish` and `scripts/executable_refresh-config` paths. No audio or files were changed by those probes.

## Lookup and root cause

Query: `Could not connect to PipeWire sandbox audio`. Existing `ext-sandbox-loopback` guidance applies to restricted desktop/socket access; `local-audio-sink-mute` is not a remedy here because the live default sink and both hardware paths were already unmuted. Scoped unsandboxed inspection showed healthy PipeWire, ALC897 analog output, and matching front/rear stereo converter streams. Repository mapping identified `scripts/executable_ubuntu-start` and `dot_config/fish/functions/refresh-config.fish`; subsequent reads used those exact paths.

## Resolution and verification

Scoped desktop commands succeeded. Three left/right `paplay` tests completed with exit 0, and the user confirmed `works`. Existing HDA retask boot firmware associates front/top and rear green pins; this task saves that mapping and adds a mixer-only restore helper. No driver reload, audio-service restart, or volume increase was used to resolve the reported silence.

## Status and follow-up

Targeted `chezmoi apply` refused `~/scripts/ubuntu-start` as not managed (exit 1), so the chained refresh did not run. The installed script was older and its reviewed diff only contained the superseded redshift command. Scoped direct installation of the two reviewed scripts succeeded, followed by `fish -c refresh-config` (exit 0, `REFRESH COMPLETE`). Installed/source comparisons and the live helper passed; no migration exclusions were removed. Master remained 70%, Front/Surround 100%, PipeWire 46%, with all outputs unmuted. Existing migration-preserved-target guidance covers the direct-install fallback.

Diagnostic access: verified workaround, confirmed cause. Physical playback: user-confirmed before persistence changes. New-session/reboot activation remains a separate manual check. No new reusable learning: existing sandbox-access guidance and exact-path discovery cover these failures; keep privileged audio probes scoped, and do not interpret sandbox device absence as hardware failure.
