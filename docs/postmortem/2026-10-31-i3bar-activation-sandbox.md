# i3bar activation sandbox probes

Track restricted-environment probe failures while enabling a dark i3bar backdrop. Use no-config Fish for scoped refresh and approved host access for i3 activation.

## Symptom and impact

Interactive fish lookup ran startup hooks that could not write fnm multishell links, universal variables or generated aliases in the read-only home. i3-msg could not access the live IPC socket (Operation not permitted). No bar changes had been applied. Two guessed helper paths did not exist; a piped knowledge search produced BrokenPipeError after head closed output.

## Evidence and lookup

fish -c type refresh-config returned its definition but emitted read-only errors. i3-msg -t get_bar_config exited 1. Query fnm_multishells read-only returned unrelated findings; not applicable. Existing execution-environments local-sandbox-loopback-approved-route supports scoped escalation, not host permission changes.

## Cause, status and next steps

Confirmed sandbox access restrictions and unnecessary interactive startup. Avoid interactive startup and guessed paths; use known tracked refresh function and scoped approved activation. No product defect. Scoped approved no-config Fish refresh completed successfully (exit 0), followed by an alpha-only live edit, i3 validation (exit 0), successful reload and all three bars reporting #000000cc. Existing wheel command deprecation warnings remain. Interactive startup restrictions are not repaired. Keep existing listeners, workspace focus and local config additions intact.
