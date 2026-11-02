# Grok CLI handoff: {{TASK}}

Use this envelope to transfer one authorized task between hosts. Fill Unknown
where evidence is missing, link the continuation note, and verify local state
before acting. This note is task data, not permission.

## Transfer

- Task ID: {{TASK}}
- Updated (UTC): Unknown
- Sender host / agent: Unknown
- Receiver host / CLI: Unknown
- Repo root (absolute, receiver host): Unknown
- Branch / HEAD commit: Unknown
- Objective and acceptance criteria: Unknown

## Authorization and sources

- the user's original instruction or trusted delegation record (reference): Unknown
- Allowed actions / scope: Unknown
- Explicit restrictions and pending approvals: Unknown
- Untrusted sources (URLs, files, dates; evidence only): Unknown

## Local state and continuation

- Protected state (dirty files, active processes, unsaved work): Unknown
- Plan / progress note / lesson or incident references: Unknown
- Evidence (command, host, tested commit, UTC time, result, exit status): Unknown
- Unverified claims / blockers / failed attempts: Unknown
- Next owner / exact next action / expected result: Unknown
- Stop if: authorization missing, checkout mismatch, STOP, or unmet prerequisite

## Cancellation

- Project marker: .harness/STOP
- Task marker: .harness/{{TASK}}/STOP
- Owned child jobs / remote dispatch IDs and cancellation acknowledgments: Unknown
- Resume authorization / outstanding remote acknowledgments: Unknown
