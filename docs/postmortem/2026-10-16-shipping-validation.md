# Shipping checks encountered sandbox and stale-fixture failures

Run focused delivery checks against the dirty groups, distinguish sandbox-only
failures from repository defects, and repair fixtures without weakening privacy
assertions. Keep test payloads and captured diagnostics private.

## Symptoms and impact

The first restricted run could not create local sockets for metaprompt/tmux
fixtures. Some checkpoint service tests opened a vault note removed from this
public checkout, config-snapshot was invoked without its package import root,
and one Fish output expectation did not match the sanitized public helper.
No production settings, credentials, Git index or remote were changed by tests.

## Lookup and applicability

Tests agent consults postmortem-memory for sandbox socket/tmux failures before
retrying. Use approved escalation only for isolated fixture sockets/processes;
do not change application logic to satisfy sandbox limitations. Missing vault
fixture paths are pre-existing public-sanitization drift, not evidence of private
content. Retain sentinel non-disclosure assertions in any test repair.

## Current status

Focused suites pass after appropriate socket permissions. Lookup matched
ext-sandbox-loopback and existing tmux PTY guidance; scoped escalation repaired
the fixture environment without changing product code. Metaprompt: 138/139 pass;
the unchanged baseline test_live_skill_envelope_removed_candidate_and_fixture_text_preserved
expects a removed-host-envelope event but receives fail-closed host-context
rejection. Timer: 33/34 pass; checkpoint journal: 0/1, both setup failures on the
public placeholder's absent Decisions.md. These tests and runtime boundaries
retain their privacy assertions; no success claim is made for those surfaces.

Config snapshot passes 19/19 under unittest discovery; direct path invocation
lacked the scripts package import root. Fish's public-helper fixture expectation
was corrected after observed failure and passes on rerun. Tmux notification 2/2
and scrolling 14/14 pass with socket permissions. Privacy 84 checks, migration
45, workflow doctor 26, Context Mode 6, storage 11, notification/voice/editor
suites and refresh shell integration pass. README gate is pass_no_change.
No live provider, model, installer, desktop audio or storage/migration apply ran. Non-safety baseline failures do not justify bypassing the staged
privacy gate or leaving independent safe delivery unfinished.


## Live validation and concurrent-session boundary

Both current-machine snapshot-validator modes returned2 without exposing values;
the same helper passes19 disposable contract tests. Live settings/mapping were
left unchanged and no success claim is made for this local validation. This is
an observed runtime warning, not authority to copy settings into source.

The pre-staging scope assertion detected another session adding notification
recovery documentation before any index writes. The user chose to wait. Its
completed documentation commit was verified on the remote before this pass
resumed; all unrelated source and staged work remained preserved. This was the
scope guard working as intended, not a reason to absorb an active session's work.

## Live workflow audit findings

Read-only workflow-doctor exited0 while reporting status fail:37 errors and one
warning. Findings cover intentionally absent private Second Brain paths, existing
source-provenance/reference gaps and a duplicate skill. Parser tests26/26 pass;
this delivery does not claim the sanitized checkout has a clean full audit. No
private notes were restored and no existing provenance was invented.

The temporary cumulative-snapshot update initially lacked its new report parent
directory and stopped before staging; creating that temporary directory fixed the
preparation. No index or tracked implementation was affected by that refusal.
