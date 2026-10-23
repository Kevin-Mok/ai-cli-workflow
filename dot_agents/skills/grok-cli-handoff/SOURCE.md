# Grok CLI Handoff source

This records the reviewed handoff workflow and its portable helper. Fill the
handoff envelope, verify checkout state, and preserve cooperative STOP markers
before delegating or resuming authorized work.

- Reviewed import snapshot: `0798ed8553ab5e195ca82d0bd4497de3b19ce930`.
- Imported on: `2026-10-22`.
- Retained: authorization and untrusted-source boundaries, checkout preflight,
  task/project STOP, explicit resume, evidence and owned-job cancellation rules,
  envelope, disposable smoke helper and full CLI regression tests.
- Public adaptation: replace personal naming with the user, shorten the trigger,
  and route multi-session continuation to the retained `context-handoff` skill.
- Helpers use Python's standard library and Git; no service, remote transport,
  agent launch or paid call is installed or performed by these helpers.
