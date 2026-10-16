# Privacy-gate prompt handoff runtime probe

This report records a compiler-side execution failure before launching the fresh privacy-gate task. It preserves the launch boundary and the correction used to avoid a duplicate task.

## Symptom and impact

The orchestration script used TextEncoder for the native tool handoff byte-count check. That runtime has no TextEncoder global, so it raised ReferenceError before reaching create_thread. No executor was created, no Git index was changed and no secret was exposed. The compiled prompt was already saved and read back successfully.

## Evidence and lookup

The tool returned `ReferenceError: TextEncoder is not defined` at the byte-count line before the native creation call. A lookup for `TextEncoder unavailable JavaScript orchestration handoff` supplied no verified remedy applicable to this orchestration runtime. This is a tool-script compatibility issue, not a privacy scanner failure.

## Resolution and verification

Use an explicitly ASCII handoff and verify its length with string.length, with an ASCII assertion. ASCII characters are one UTF-8 byte each. Only then call create_thread once; inspect its returned task and navigate to that same ID. Observed: the ASCII handoff is 329 UTF-8 bytes; one executor was created, its running turn was inspected, and the terminal opener exited 0 after verifying the focused executor tab. At that handoff boundary gate implementation had started in the separate conversation; later completion evidence is in the privacy-gate plan.

## Follow-up

Use only documented orchestration globals. The separate executor remains responsible for implementing and testing the privacy gate; this compiler incident is not evidence of completed gate behavior.
