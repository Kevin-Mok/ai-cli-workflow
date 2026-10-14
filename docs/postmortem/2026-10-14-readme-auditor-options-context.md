# README Auditor Options Patch Context Failure

This postmortem records why a small README clarification did not apply on its
first attempt.

## Symptom

On 2026-10-14, the patch tool reported that it could not find the expected
history-auditor paragraph even though a subsequent focused read showed the text.

## Impact

The atomic patch made no change. The sanitized history and public-tip worktree
remained intact, and nothing was committed or pushed.

## Evidence

- The failed patch named the README paragraph as its missing context.
- A direct read immediately afterward showed the target command and surrounding
  paragraph unchanged.

## Resolution

Use a smaller hunk anchored only on the command fence and following heading,
then rerun the README gate and worktree scan.

## Current Status

Resolved. The smaller hunk added the documented options, the README gate reports
`pass_no_change`, and the corrected publishable-worktree scan reports zero
findings. The external postmortem-memory ledger remains outside the
user-authorized folder and is intentionally untouched.
