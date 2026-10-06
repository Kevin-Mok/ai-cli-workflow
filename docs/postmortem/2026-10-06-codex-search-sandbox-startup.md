# Codex search sandbox startup failure

This report records why repository inspection used approved execution and how that workaround was verified.

## Symptom and impact

On 2026-10-06, four independent initial read-only commands failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. No requested command body ran and no files changed.

## Lookup and evidence

Read the tracked postmortem-memory skill and searched `bwrap loopback Failed RTM_NEWADDR`. The matching `local-sandbox-loopback-approved-route` finding applies: this is runner startup, not a repository or search-tool failure. The required Git status and source reads succeeded through approved execution, exit 0. Status captured before writes protects existing README, aliases, smoke tests, incident knowledge, backup work, lessons, and untracked plans/reports.

## Status, cause, and resolution

Verified workaround; host namespace policy remains unresolved. Approved scoped execution runs the commands; it does not repair the normal sandbox. Continue the authorized implementation through that route without changing host security settings.

## Verification and next steps

Approved `git status --short` and required source reads returned expected output with exit 0. Use approved execution for scoped implementation checks. Host sandbox repair is outside this task. No new reusable learning: existing finding already describes the symptom, scope, and verified workaround.
