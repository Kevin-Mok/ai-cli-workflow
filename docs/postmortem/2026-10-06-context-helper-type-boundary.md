# Context helper typed module boundary

This report records a static-check failure at the new dynamically loaded knowledge-helper boundary and the explicit interface used to resolve it.

## Symptom and evidence

`basedpyright dot_agents/skills/personal-context/scripts/context_store.py` exited 1 with one ModuleType.c attribute error and 27 dynamic-boundary/unused-call warnings. Runtime synthetic tests and private sampled evidence passed, but static verification was incomplete. No private contents were printed.

## Lookup and cause

Reviewed the prior personal-context type-check report and searched `type checker dynamic ModuleType attribute Any boundary`. Broad type-only/path findings do not directly cover this interface. Diagnosis: dynamic module loading lacked a typed callable protocol, CLI extensions lacked declared namespace fields, and new argparse calls left results unused.

## Resolution and status

Declared the validated ProjectEnvelope and helper callable Protocol in context_store, cast through object only at the dynamic module boundary, declared CLI namespace fields and explicitly discarded intentional registration results. Used AbstractContextManager for the current Python interface. Fresh basedpyright: zero errors, warnings and notes, exit 0. Fresh personal-context suite: 59 tests pass; Second Brain routing: 12 tests pass; README gate pass_no_change. Final refresh-config exits 0. Status: verified code/static fix; real sampled foundation evidence predates this typing-only change and remains valid.

## Follow-up

Keep basedpyright on the typed storage helper alongside synthetic runtime tests. Imported modules are runtime-validated; protocol typing must describe the real callable interface.
