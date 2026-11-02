# Grok CLI Handoff source

This records the reviewed handoff workflow and its portable helper. Fill the
handoff envelope, verify checkout state, and preserve cooperative STOP markers
before delegating or resuming authorized work.

The structured fields identify a public-intake checkpoint, not an upstream-origin claim.
The earlier reviewed import snapshot below remains separate; private source
locations are intentionally not published.

- Source archive: .
- Source commit: 60c6e70f6ba63e6902aa6da76761f0fd550f4e06
- Original source path: dot_agents/skills/grok-cli-handoff/SKILL.md
- Source SHA-256: 49ac15900b4321d96b6a41d657296c53b493079bb9fbadfd8c72a5c3f105755b
- Adapted on: 2026-10-22
- Adaptation basis: accepted public-intake checkpoint of the reviewed workflow; original private locations remain undisclosed.
- Local adaptation: normalize provenance fields while retaining the reviewed privacy, authorization and workflow adaptations below.

- Reviewed import snapshot: `0798ed8553ab5e195ca82d0bd4497de3b19ce930`.
- Imported on: 2026-10-22
- Retained: authorization and untrusted-source boundaries, checkout preflight,
  task/project STOP, explicit resume, evidence and owned-job cancellation rules,
  envelope, disposable smoke helper and full CLI regression tests.
- Public adaptation: replace personal naming with the user, shorten the trigger,
  and route multi-session continuation to the retained `context-handoff` skill.
- Helpers use Python's standard library and Git; no service, remote transport,
  agent launch or paid call is installed or performed by these helpers.
