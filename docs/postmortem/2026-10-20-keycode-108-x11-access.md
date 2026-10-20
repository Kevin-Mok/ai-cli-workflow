# Keycode 108 inspection could not reach X11

This records the desktop-access problem encountered while enabling keycode 108
as an Alt modifier, including the evidence and the scoped recovery check.

## Symptom and impact

- Initial restricted-shell `xmodmap -pm` and `xmodmap -pke` both reported
  `unable to open display ':1'` on 2026-10-20. The environment reports X11 and
  `DISPLAY=:1`; no keyboard settings were changed.
- Scoped approved inspection succeeded; repository and live inspection can continue.
- The first shell command used a pipeline without pipefail, so its exit status
  was 0 despite the diagnostic failure. Subsequent probes must preserve status.

## Lookup and applicability

- Read the canonical postmortem-memory skill and searched
  `xmodmap unable open display X11 sandbox` before retrying.
- No reviewed finding specifically covers this X11 error. The reviewed
  `ext-sandbox-loopback` finding describes a different pre-execution failure;
  it supports considering scoped approved execution, not assuming an X11 cause.
- The same read-only inspection succeeds through scoped approved execution.
  This confirms an execution-context access restriction; the exact X11
  namespace or authorization mechanism was not isolated.

## Status and next steps

Verified workaround: approved `xmodmap -pm` and a pipefail-protected
`xmodmap -pke` probe exited 0. Keycode 108 is Alt_R and belongs to Mod1.
The default sandbox was not changed. Use scoped approved execution for the
remaining desktop checks. The X11 access workaround does not prove a particular namespace or
authorization mechanism. The reviewed learning below concerns the probe API
and Unicode command transport, whose correction was exercised directly.

## Desktop probe follow-up

The first raw-key probe passed left Alt+1/2/0 and keycode 108+1, then observed
focused workspace 3 after 108+2 (expected 2). Its cleanup restored the original
focus but the visible-workspace-set assertion failed. This is not yet evidence
of a wrong key mapping: the check samples mutable desktop focus after a delay.
Status at that point: unresolved probe reliability. Inspect current desktop state and
i3 binding events before another test; preserve and restore the visible layout.

The revised diagnostic then timed out waiting for a readiness line from
`i3-msg -m -t subscribe` before injecting any keys. No keyboard or workspace
changes occurred in that attempt. Its subscription setup must move inside
cleanup coverage and use confirmed IPC acknowledgement semantics; consult the
installed i3 documentation before retrying. The monitor subprocess may still
need cleanup; do not kill unrelated i3 or monitor processes.

Documentation review found that i3-msg monitor mode intentionally discards the
subscription acknowledgement and flushes actual events. See the
[i3-msg source](https://github.com/i3/i3/blob/4.23/i3-msg/main.c#L235-L299) and
[i3 IPC subscription contract](https://i3wm.org/docs/ipc.html#_subscribe).
The next probe uses the documented Unix socket framing to receive an explicit
type-2 acknowledgement. Process inspection found no abandoned monitor.

The socket-based probe confirmed all six shortcuts: left Alt and keycode 108,
each with 1/2/0, emitted the expected Mod1 binding and workspace focus event.
Its cleanup still failed: visible workspace numbers were `[3, 3, 2]` instead
of `[10, 3, 1]`. The cleanup serialized Unicode workspace names with JSON
ASCII escapes before sending them as i3 command text, which is not a JSON
parser. Inspect and restore exact original Unicode names using literal UTF-8
and disable workspace auto-back-and-forth during restoration. No key mapping
change is needed on the evidence collected so far.


## Resolution and verification

The final `python3 /tmp/keycode-108-workspace-check.py` run exited 0. All six
left-Alt/keycode-108 combinations with 1/2/0 emitted `['Mod1']` binding events
and focused workspaces 1/2/10. Cleanup restored visible workspaces `[10, 3, 1]`
and focus 3. Literal UTF-8 (`json.dumps(..., ensure_ascii=False)`) plus
`workspace --no-auto-back-and-forth` corrected cleanup; a separate live read
confirmed no temporary escaped-name workspace remained.

No keyboard configuration change was required. The first sampled-focus mismatch
is not isolated to one cause; direct binding and focus-event evidence passes.
Physical keyboard/firmware acceptance remains a manual check. The temporary
probe is diagnostic evidence under `/tmp`, not a new supported repository tool.

Reviewed learning: `local-i3-probe-ipc-unicode` records the verified probe
correction; the report's final hash and alias are registered in the tracked
postmortem ledger. Run the targeted coverage check after updating this report.


## Commit validation note

A preliminary read-only `git show candidate:foo` inspection exited 128 because
`candidate` was an index description, not a Git ref. It made no changes. The
validator corrected the lookup to the manifest's isolated index/blob IDs and
passed ledger/reference, report-hash and reciprocal-link checks. A memory
lookup for `git invalid object name candidate ref` found remote-fetch guidance,
which does not apply to this local invalid-ref typo. No new generalized learning
is needed for this lookup correction; use actual candidate blob IDs.
