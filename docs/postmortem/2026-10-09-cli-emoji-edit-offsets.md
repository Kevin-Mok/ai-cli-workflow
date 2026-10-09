# CLI emoji edit helper offset failure

A temporary Python editing helper stopped before writing one remaining script. Preserve completed valid edits and correct the UTF-8 offset conversion before continuing.

## Symptom, impact and evidence

The Python output agent reported `/tmp/decorate_python_outputs.py` raising SyntaxError while preparing `scripts/smoke_redshift_keys.py`. The helper used AST UTF-8 byte offsets as string character offsets near an existing en dash. It parsed the proposed source before writing, so this target was not changed by the failed edit. Earlier completed scripts remain in place and parse-valid according to the agent; root review is pending.

## Lookup and applicability

Consult canonical postmortem-memory and search editing offset symptoms before remedy. A temporary authoring helper failure is distinct from application behavior and expected TDD RED. Current causal evidence is the agent's identified byte/character mismatch; independently verify the corrected output and scripts.

## Current status and next steps

Resolved editing helper. Agent translated AST UTF-8 byte columns to character positions, reran remaining edits and observed seven defining Python tests pass. Root independently parsed all Python sources across scripts, local skill helpers and non-candidate benchmarks and ran a multibyte AST offset probe successfully. The original pre-write parse gate prevented the faulty target from being written.

## Learning decision

Verified editing remedy: convert byte columns before slicing Unicode strings, apply edits from right to left and parse before each write. Add the reviewed finding to tracked editing guidance and run its targeted coverage check. This proves source editing correctness, not live installation by itself.
