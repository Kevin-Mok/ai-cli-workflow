# VPS prompt commit: session scope attribution unavailable

Date: 2026-10-04

## Symptom and impact

During the requested `commit-session` workflow, the scope helper exited 0 but
reported `status: unsafe` and an empty `commitable` list for session
`01a1086d-ab77-7991-ab48-c505183de525`.

Its reason was: `No successful repo-writing actions were detected in the
current Codex session.` No files were staged by the helper. Automatic
attribution was unavailable, so the commit requires the skill's documented
direct-write fallback.

## Evidence

The executed command was:

```text
python3 dot_agents/skills/commit-session/scripts/session_scope.py --repo-root /home/example/linux-config
```

The active conversation directly records successful creation and read-back
verification of these files:

- `prompts/bootstrap-vps-aws.md`
- `plans/compile-vps-aws-bootstrap-prompt.md`
- `docs/postmortem/2026-10-04-vps-bootstrap-prompt-sandbox-startup.md`

The pre-write Git status and subsequent SHA-256 checks establish that all
13 other dirty files predated these writes and remained unchanged.

## Root cause

The session log records nested command and patch calls as `custom_tool_call`
events named `exec`. The helper recognizes writes only from direct
`exec_command` function calls and direct `apply_patch` custom tool calls.
Its parser therefore misses writes and pre-write status checks inside the
wrapper. Inspection of the parser and session event-name counts confirmed
the mismatch without exposing command contents.

## Resolution and verification

Use the skill's direct-write fallback for the authored documents and their
delivery records. The helper itself was not modified. The original three
documents and this incident record were transferred into
`.worktrees/vps-aws-bootstrap-prompt` on `docs/vps-aws-bootstrap-prompt`.
All four copies were checked byte-for-byte before removing their original
untracked copies. No unrelated files were moved.

- Scope helper: exit 0, with the documented unsafe result.
- Direct edit history and pre-write status establish ownership.
- Transfer verification passed for all four source/destination pairs.
- README gate: `pass_no_change`, exit 0.
- Final scope review found all 13 baseline dirty files unchanged. Two
  concurrently added Kitty-related documents were excluded as unrelated.
- Final commit and push evidence belongs in the session handoff.

## Follow-up

Extend the scope parser for wrapper events in a separate task with session-log
fixtures. Until then, retain direct write evidence and the pre-write baseline.
