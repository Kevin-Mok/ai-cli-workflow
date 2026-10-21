# Discord private D-Bus sandbox check

The notification integration check needed an approved socket-capable execution route. Rerun the isolated Dunst fixture with that route; do not change desktop listeners.

## Symptom and impact

Initial xvfb-run/dbus-run-session invocation exited 1 before tests: dbus-daemon could not bind /tmp/dbus-* (Operation not permitted), then session startup EOF. No notification behavior was exercised and no live daemon was changed.

## Lookup and resolution

Read canonical postmortem-memory; searched D-Bus socket Operation not permitted. Reviewed local-sandbox-loopback-approved-route in references/execution-environments.md: applicable environment-level socket restriction, not product failure. Tests agent reran the same private fixture with approved sandbox escalation. It reached Dunst and produced the expected RED (10 plays instead of 11) for the unimplemented Discord callback. This verifies the execution workaround, not final feature acceptance.

## Cause, verification and follow-up

Confirmed sandbox socket restriction. Approved execution is the workaround; no sandbox configuration changed. Continue feature GREEN checks using the same isolated route. No new learning beyond existing approved-route guidance.

## Fish read probe limitation

A later `fish -c 'functions refresh-config'` returned 0 but startup emitted read-only filesystem diagnostics for fnm multishell links, Fish universal variables and live shortcut generation. Its function text was readable; command exit alone does not prove initialization success. Subsequent deployment uses fish --no-config with only required functions sourced and approved write access. No product-state failure was inferred.
