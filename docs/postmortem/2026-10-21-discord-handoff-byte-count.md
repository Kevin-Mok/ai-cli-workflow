# Discord speech handoff byte-count failure

This report records a compiler-runtime error while preparing a fresh Discord speech implementation task. Check the available JavaScript runtime, count the handoff bytes with Python, then create and inspect exactly one executor.

## Symptom and impact

The initial `functions.exec` handoff preparation failed with `ReferenceError: TextEncoder is not defined`. The exception occurred before `mcp__codex_tui__create_thread` was called. The compiled prompt was already saved and verified; no implementation task was created by the failed call.

## Evidence and current status

- The failed script used `new TextEncoder().encode(handoff).length` before the task-creation call.
- This orchestration environment is a fresh V8 isolate and does not guarantee browser or Node globals.
- The prompt remains intact at `prompts/discord-notification-speech.md`.

## Lookup and applicability

- Queried `TextEncoder not defined UTF-8 handoff byte count`; broad results concerned unrelated Python and byte-offset boundaries. An exact `TextEncoder` query returned no match.
- Read `2026-10-20-redshift-handoff-byte-check.md`: the same missing-global failure had already been diagnosed, with ASCII length validation and scoped Kitty navigation verified. This applies to the compiler runtime, not Discord notification behavior.

## Root cause, resolution and verification

- Cause: assumed the browser/Node `TextEncoder` global existed in the restricted V8 isolate. The exception occurred before any native task creation.
- Python `len(handoff.encode('utf-8'))` verified the exact handoff as 301 bytes, below the 1,000-byte limit (exit 0).
- One native creation returned executor `<redacted-executor-id>`.
- The terminal opener, using normal scoped sandbox escalation, verified that executor in focused Kitty window 2 (exit 0). No duplicate executor was created.
- Native `read_thread` showed an active, in-progress implementation turn without an error. Launch/navigation are verified; completed Discord speech behavior is not established by this compiler check.
- Status: resolved compiler handoff. Implementation and runtime acceptance belong to the executor.

## Learning and follow-up

No new learning: the documented restricted runtime and the reviewed Redshift incident already cover the missing global and scoped socket access. Retain a reviewed source record for this recurrence. Count UTF-8 through an available documented facility and avoid assuming browser globals in `functions.exec`.
