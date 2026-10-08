# Backup compression tool invocation syntax failure

This report records a tool wrapper failure while checking compression options. The retry used valid JavaScript and only a tiny disposable compressor input.

- Symptom: functions.exec rejected one invocation with "SyntaxError: Invalid or unexpected token" before any nested tool executed.
- Impact: no command, file change, backup interruption or disk write occurred; inspection was delayed.
- Evidence: immediate tool result reported a script parser error with zero execution time. The following corrected template-literal invocation completed; local XZ 5.4.5 accepted -9e, --threads=9, --memlimit-compress=30GiB and --no-adjust, reporting 11243 MiB compressor memory.
- Lookup: tracked postmortem-memory search "SyntaxError Invalid or unexpected token" returned broad transport/contract matches; none explained this JavaScript wrapper parser error. Shell interpolation remedies do not apply because the nested shell never started.
- Cause: malformed JavaScript tool wrapper; confidence confirmed at parser boundary, exact offending token not isolated.
- Resolution: use valid JavaScript string transport for the multiline read-only command.
- Status: verified workaround; parser boundary retry passed, no backup runtime behavior changed by this incident.
- Follow-up: verify resource-budget implementation with defining tests and disposable tar fixtures. No new durable engineering finding beyond existing transport guidance; register this scoped evidence with an explicit no-new-learning decision.
