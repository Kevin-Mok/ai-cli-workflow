# Mute shortcut desktop access

This report records restricted desktop probes while installing Super+M and the scoped recovery.

## Symptom and impact

Sandboxed xmodmap could not open display :1; pactl reported Operation not permitted and Connection refused. A guessed scripts/executable_refresh-config path did not exist. No desktop state changed.

## Evidence and lookup

Searched postmortem memory for `X11 display pulse Operation not permitted`. Existing execution-environment guidance supports scoped approved host access; it does not establish an audio defect. Approved xmodmap confirmed keycode 133 is Super_L in Mod4; pactl returned Mute: yes. The real refresh helper is a Fish function.

## Resolution and verification

Desktop access recovered through approved execution. Chezmoi reports the live i3 config unmanaged because migrationPreservedTargets excludes it. Updated the tracked binding and only its matching live line, preserving private live content. `fish -c refresh-config` completed successfully; i3 config validation exited 0 with existing wheel_up_cmd/wheel_down_cmd deprecation diagnostics; i3 reload returned success. Two synthetic Super_L+m presses changed `Mute: yes` to `Mute: no` and back to `Mute: yes`, with explicit original-state restoration in a finally block.

## Learning and limits

No new reusable learning: this repeats restricted desktop access and intentionally preserved migration-target behavior. The Bubblewrap startup finding is only analogous: these commands started but desktop sockets were denied. No host security or migration exclusions were changed. Subjective listening and physical keyboard input were not checked. The tracked source is public-safe while the newer live config contains private data; only the requested binding was synchronized, rather than copying private contents into source. No remaining blocker to this shortcut.


## Commit validation warning

`python3 -B tests/test_postmortem_memory.py` completed with 25 passing tests and one failure, `WorkflowTest.test_actual_ledger_reference_status_and_coverage`. The full-corpus check uses placeholder roots `/home/example/coding` and `/home/example/linux-config`, which are absent on this machine. This is an existing corpus-location limitation, not a mute-toggle failure. The earlier targeted check for this report passed. No global path rewrite or unrelated corpus changes were attempted; retain the warning in delivery. No new reusable learning beyond the existing placeholder-root limitation.
