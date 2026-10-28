# Trim commit blocked by read-only Git metadata

The prepared trim work and approved cull can be reviewed in this worktree, but
Git cannot stage them.
Restore ordinary write access to this worktree's Git metadata, then rerun the
documented checks, stage the listed files and commit before starting pass 1.

## Symptom And Impact
`git add` exited 128: it could not create
`/home/kevin/ai-cli-dotfiles-public/.git/worktrees/skills-efficiency/index.lock`
because the filesystem is read-only. No staging, privacy check or commit ran.
The requested one-commit-per-pass sequence cannot advance under this mount.

## Evidence And Lookup
`findmnt -T /home/kevin/ai-cli-dotfiles-public/.git/worktrees/skills-efficiency`
reported `/home` mounted `ro`. The worktree itself is a permitted writable root;
the shared Git metadata lies outside it. `git diff --cached --stat` was empty.
Lookup query: `git index.lock read-only file system worktree`.
The existing `local-git-owned-index-lock-check` and
`local-git-index-same-filesystem-publish` findings cover lock probes and index
publication, but do not remedy a read-only mount. No stale-lock deletion,
alternate Git directory, history rewrite or permission bypass was attempted.

## Current Status And Next Steps
Unresolved external permission boundary. Preserve the prepared pass and initial
untracked input files. Resume only after normal Git metadata writes are allowed;
rerun focused tests/benchmark and README gate, inspect the staged diff, run the
privacy gate and finish the current dedicated cull commit,
`refactor(skills): cull approved overlaps`, following the latest user priority.
Keep later admission and intake changes out; do not start the next pass. No push/config sync is authorized.

## Learning
Known mount-boundary limitation, no new remedy established. Required canonical
ledger update at `/home/kevin/linux-config/dot_agents/skills/postmortem-memory/`
is also outside permitted writes; hash/alias review remains outstanding. No
installed knowledge copy was changed. This report is a handoff, not a fix claim.

## Latest cull checkpoint

The most recent normal staging attempt still exited 128 creating the same
index.lock; findmnt still reports /home read-only. The host fetched approved
private branch refs, but that does not grant this task metadata write access.
No current-session file is staged and HEAD remains the original start commit.
The cull is being finished with its required calibration maintenance; no private
PR file is imported, no config is activated, and no workaround is attempted.

## Resolution

The host restarted the task with the main repository .git as a writable root.
A normal git add now exits0 and stages the intended config file. findmnt still
displays a protected read-only metadata mount, so it is not sufficient evidence
of effective sandbox write authorization. Use the actual authorized operation
as the decisive probe. No permission bypass or alternate Git directory used.
Staged privacy review and the cull commit now proceed normally.

Direct Git commands now stage the complete reviewed scope successfully. A
Python-spawned git add still received a read-only index-lock error in this
execution environment; use the normal direct Git tool invocation. This was
verified by two successful direct staging operations and an exact234-path
staged-manifest comparison. No alternate index or permission bypass was used.
