# Grok workflow inspection in a restricted checkout

This report records inspection failures while preparing the Grok CLI workflow PR,
the safe workaround, and verification limits. No live configuration was applied.

## Symptom and impact

- Initial `git status --short` exited 128: Git LFS tried to write
  `/home/example/linux-config/.git/lfs/tmp/` in a read-only shared Git directory.
- Some advertised skill paths and `dot_agents/skills/context-handoff` were absent;
  combined reads reported missing files. No source changes resulted.
- The tracked context-handoff copy is absent, but its installed skill exists;
  subsequent inventory located it and the private context helper's real name.
- `gh repo view` was blocked by the sandbox's api.github.com allowlist before
  execution. Approved network access is needed for the authorized PR delivery.
- The README gate was mistakenly invoked with Python; it is a Bash script.
  Python reported SyntaxError without executing or changing repository files.
- The instruction regression found one pre-existing failure:
  `test_push_policy_is_consistent_in_active_workflows` requires a sentence absent
  from `dot_agents/skills/commit-dirty/SKILL.md` in HEAD. That file is unchanged.
  The doctor baseline also has 7 errors and 1 warning, all unchanged after this
  task. They are reported as baseline limitations rather than repaired here.
- Reviewer path inventory guessed two absent paths; actual Claude policy is
  `dot_claude/CLAUDE.md.tmpl`. No remedial source change was needed.
- A lesson append introduced an extra blank line at EOF; diff-check caught it
  and it was removed. One combined patch had a mismatched plan anchor and was
  rejected before changes; a smaller patch applied the intended update.
- The broad memory suite's real-corpus coverage check failed (25/26 pass); it
  scans the dirty canonical checkout and other projects, including unregistered
  or changed reports outside this task. Targeted coverage for this report is
  the relevant completion check, after ledger registration.
- Delivery may require approved writes to the shared Git directory.

## Lookup and evidence

Read the canonical postmortem-memory skill before remediation. Query:
`Git LFS read-only filter-process git status`. Returned sandbox and scoped-state
findings do not directly cover an LFS cache write; no applicable LFS remedy found.
The error names the denied cache location. Disabling the filter produced false
dirty LFS assets, so that output is not the protected baseline.

## Resolution and current status

`git -c lfs.storage=/tmp/grok-workflow-lfs status --short` exited 0 with no output.
The temporary cache retains LFS comparisons without writing the shared Git cache.
The verified pre-write baseline is clean; branch `feat/grok-cli-workflow` already
exists at `eddd552`. Inventory actual repo paths before opening further files.

## Verification and learning

The temporary LFS cache verified a clean baseline and scoped diffs. Approved
GitHub access verified the repo/default branch, fetched main and found no existing
PR. The Bash README gate passed. No signing/identity settings were changed and
no live configuration was applied. The underlying shared-metadata restriction
remains; delivery uses the approved execution path.

Query `api.github.com allowlist` returned unrelated deployment findings; no
applicable access repair. The approved GitHub operation itself is the verification.
The baseline instruction failure was checked directly against its committed
HEAD blob, not attributed to this change. Doctor comparison adds no findings.

Record this report in canonical and task-checkout postmortem ledgers with an
explicit no-new-finding decision: scoped-state and execution-boundary guidance
already covers the permission constraints; the single-environment LFS workaround
is captured in `tasks/lessons.md`. Keep installed copies read-only. Targeted ledger
checks and final delivery evidence belong in the active plan, avoiding a report
hash that changes merely to quote its own coverage check.
