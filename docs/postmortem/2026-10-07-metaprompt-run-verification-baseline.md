# Metaprompt runner verification baseline failures

Separate pre-existing legacy hash-test mismatches and a verification-harness API mistake from the fresh-conversation runner update. Record evidence before investigating, then complete unaffected checks.

## Symptoms and impact

The legacy contract suite passed 12 tests. The eight-test integration suite failed four subcases of its legacy byte-identity test; actual SHA-256 values for four metaprompt-alxve references differ from pinned expectations. The runner update did not touch those files. The chained metadata/link checks were skipped, so they need independent execution.

A subsequent functions.exec call used TextEncoder to count handoff UTF-8 bytes. This isolate lacks TextEncoder, producing ReferenceError before create_thread or shell verification ran. No new task was launched by that failed call. The concrete handoff is ASCII, so its JavaScript length is its UTF-8 byte count; arbitrary Unicode handoffs must use a real UTF-8 counter such as Python len(text.encode('utf-8')).

## Evidence and lookup

Integration failure actual/expected digest prefixes: execution-routing 642ebb47/828d0bac; examples bc849a6c/62317639; model-profiles f8b352ab/ea522da5; compilation-rules c02f0210/552e00eb. Postmortem-memory query: metaprompt legacy hash references integration. Prior lookup returned only unrelated fixtures/environment findings, which do not apply to legacy byte pins. HEAD blobs and HEAD test expectations establish the baseline without a remedy; do not rewrite legacy files or weaken tests.

## Current status and next steps

Legacy mismatch status: confirmed pre-existing unresolved baseline. git show HEAD bytes match each of the four working files, and the HEAD test expects different digests for all four; this task altered neither source nor expectations. Harness status: verified_workaround. Retrying the 299-byte ASCII handoff successfully created native task 01a116f0-0303-7101-8a5e-6ef7fabecdc4; a 2,789-byte compiled prompt remained intact on disk. Metadata quick_validate passed and Claude skill-link check exited 0. Record execution completion evidence in the active plan. No authorization to change legacy behavior or pinned test expectations.
