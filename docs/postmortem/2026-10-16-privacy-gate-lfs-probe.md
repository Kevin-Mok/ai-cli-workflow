# Privacy gate LFS capability probe

A local read-only capability probe found that the installed Git LFS has no
`contentlocation` command. Use supported environment discovery instead, then
validate local payload bytes without downloading anything.

## Symptom and impact

`git lfs contentlocation -h` exited 127 with an unknown-command diagnostic.
No repository content, index, hooks or credentials changed. Gate implementation
was not yet present. No candidate contents were involved or printed.

## Evidence and applicability

Postmortem-memory lookup: `git lfs unknown command contentlocation`; no relevant
prior command capability finding. The probe tested an unsupported command name;
this was not an LFS object-read failure.

## Resolution and verification

Use the supported `git lfs env` LocalMediaDir field, captured privately, to locate
local objects. Gate tests will verify pointer size/hash and missing-object refusal.
Status: resolved. Disposable gate tests pass for safe local LFS payloads,
private payload refusal, and missing-object fail-closed behavior.

## Follow-up

Keep unsupported capability discovery separate from candidate diagnostics.

## Verification discoveries

Repository discovery also encountered absent guessed fixture/ledger filenames;
subsequent inspection used the actual ledger keys and available test files.
No application state changed. Existing checkpoint-journal regression setup fails
before exercising the gate: it copies the public vault placeholder then opens a
removed Decisions.md note. The file was already dirty at the session baseline;
its fixture failure remains outside this task. Other checkpoint tests use private
vault fixtures; their mechanics now mock the new public-policy boundary alongside
the existing doctor/README boundaries. A separate real-tree integration test
checks the public gate itself. This preserves private-repo mechanics without
exempting private vault paths in production.

## Learning decision

No new reusable finding: the unsupported-command probe was a capability
assumption, not a product defect. Existing prerequisite validation guidance
already applies. The existing journal fixture failure is recorded as a residual;
this task does not repair unrelated pre-existing test data.

## Sandbox discovery constraint

A read-only `fish -c 'functions refresh-config'` query triggered normal interactive
configuration startup: fnm symlink and shortcut regeneration writes were refused
by the sandbox's read-only home/runtime mounts. The function query itself exited
0, but startup emitted write errors. Use `fish --no-config` and an explicit
function path for the required refresh, under normal approved workspace
permissions. No config files were adopted to remedy these startup errors.

## Completion title transport

The native completion-title update returned a local HTTP transport error after
verification. The initial objective title had been set successfully. Per the
title policy, keep the existing native name when the tool is unavailable; no
retry or application repair was needed, and gate state was unaffected.
