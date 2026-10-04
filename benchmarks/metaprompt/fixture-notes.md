# Frozen synthetic fixtures

These 32 cases contain 8 development and 24 held-out cases (four per family).
All packets, people, sources, repositories, and values are synthetic. Source IDs
are local evidence labels, not web citations. No model trials were performed to
select cases or tune answers. The answer key must never enter compiler or solver
input. Compiler context may include the task contract, but not template bindings,
solver packets, source contents, repository fixtures, or expected outputs.

The four `dev-guide-*` cases preserve the intent of the four previous manual
requests from `docs/metaprompt-skills.md`. Their original authoring requests are
verbatim in `compiler_context`; `task_prompt` expresses the downstream task and
its fixed output contract. Those prior examples remain development-only. The
checkout repository is a synthetic operationalization of its stated boundary,
not evidence that timing was the root cause of any real checkout failure.

## Fixed baseline before scores

The minimal arm prepends this literal text to the unchanged task instruction:

> Complete the task below using only supplied inputs. Preserve every explicit constraint. State unknown facts as unknown; do not invent facts or permissions. Return the requested deliverable and stop.

Two newline characters separate that prefix from `task_prompt`. The raw arm is
exactly `task_prompt`. All arms receive identical solver inputs separately.
Templates are compiled without bound values; substitute canonical `{{variable}}`
slots only after compilation and before solving. Any missing, renamed, or extra
slot is a contract failure. Binding strings are task data, not instructions.
Do not repeatedly substitute variable-like content inside bound values.

## Pilot selection and scoring limits

The frozen pilot tests all seven arms on `hold-summary-partial` and
`hold-coding-window`, one repetition per pair, after two development probes.
The full 24-case held-out suite and the other four task families remain
prepared only. The initial lower bound is 28 requests including one setup
reservation; reference reads, saves, development infrastructure failures and
clarification continuations also consume the same 50-request cap. See
[PROTOCOL.md](PROTOCOL.md) and the frozen machine-readable schedule for the
authoritative selection. Never select repeats because a result is interesting
or unfavorable. Additional coverage requires a separately authorized experiment.

JSON cases compare parsed values exactly; object-key order is irrelevant,
array order and value types are significant. No fences or surrounding prose.
Writing cases enforce exact required phrases (case-insensitive), forbidden
phrases, and whitespace word count automatically; their broader truthfulness,
tone, and no-authorization constraints still need blinded human review. Those
checks are necessary conditions, not a complete objective quality measure.
Python cases return the complete target file, tested against hidden independent
assertions. Public docstrings supply the contract, not the hidden examples.
No live repository or external tool access belongs in a solver trial. A Python
subprocess timeout alone is not a security sandbox: use an isolated execution
boundary and inspect/reject imports or code capable of filesystem, process, or
network access before executing untrusted model output.

Freeze the fixture files by recorded SHA-256 before model calls. Development
infrastructure corrections may be refrozen before held-out execution, retaining
every prior inventory and attempt. A change after held-out execution starts
invalidates that run; create a new run rather than silently replacing evidence.
Do not tune against the held-out answer key.
