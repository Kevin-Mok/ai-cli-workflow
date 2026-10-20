# Preserve newer local configuration

Record the requested local-newer precedence rule and resolve the reported MIME conflict using reviewed source reconciliation.

## Scope and decisions

Update canonical dot_codex/AGENTS.md, append canonical feedback, preserve the two newer local MIME handlers, and retain unforced apply. This changes agent guidance, not refresh helper automation. Protect all pre-existing dirty work, including postmortem memory edits. Commit-session authorized a focused commit and push to origin/main.

## Checklist

- [x] Capture status, inspect log, timestamps and target diff; consult prior incident guidance.
- [x] Record durable rule and preserve newer local MIME changes.
- [x] Confirm target diff empty and whitespace checks pass.
- [x] Run refresh and record actual outcome: REFRESH COMPLETE, exit 0.

## Risks and rollback

Modification time is a precedence signal; review content for secrets, templates and concurrent source edits. Revert only this session’s rule, feedback entry and two MIME additions if necessary. Existing unrelated configuration changes may be applied by refresh as requested by repository policy.

## Verification and review

Observed: chezmoi diff -- ~/.config/mimeapps.list produced no output, exit 0. git diff --check passed. The supplied error log provides the pre-change reproducer; no helper code changed. Manual check: normal refresh, target diff, xdg-mime handler queries. Suggested commit: docs(config): preserve newer local managed files. Cursor handoff: follow the canonical newer-local rule, preserve the two MIME handlers, and verify normal unforced refresh without bundling unrelated edits.

## Delivery milestone

- [x] README gate: pass_no_change; no README edits needed.
- [x] Scope fallback: directly observed session writes only; exclude all unrelated dirty files and ledger records, including incidental JSON formatting.
- [x] Commit candidate prepared: docs(config): preserve newer local managed files. Verified refresh, target diff and handler queries; no implementation work remains. Push follows the focused commit; blockers: none known.

Concurrent shared-index replacement caused the first commit hook to block; retry uses an isolated index, preserves other staging, and retains privacy checks.
