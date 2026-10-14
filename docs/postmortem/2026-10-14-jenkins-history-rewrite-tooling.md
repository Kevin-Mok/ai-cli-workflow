# Jenkins History Rewrite Tooling Failures

This report records prerequisite and sandbox failures encountered while
removing historical Jenkins and related CI credentials. It keeps the rewrite's
recovery evidence and corrective actions together without reproducing any
credential value.

## Symptoms

1. An isolated `/tmp` installation of `git-filter-repo` generated a launcher
   that could not import its module without an explicit isolated Python path.
2. A disclosure-safe branch-coverage helper exceeded its first 30-second
   command window because it reread identical blobs once per branch.
3. The first real `git-filter-repo --replace-text` attempt could not create a
   lock for a remote-tracking ref because the sandbox mounted `.git` read-only.
4. The first postmortem-memory `scan` command passed the report as a positional
   argument, but the installed helper requires named arguments.
5. The first closeout staging command could not create `.git/index.lock`
   because the default sandbox also mounts the Git index read-only.
6. The post-commit all-object auditor classified the literal SSH remote in the
   plan as an email address, so the first unpushed closeout commit could not be
   retained.

## Impact

The first two failures affected only temporary tooling. The third command
stopped with `git update-ref` failure. Ref/object state must be compared with the
validated 18-ref pre-rewrite manifest and bundle before any retry; no completion
claim is valid until that comparison and the full all-object scan pass.

No credential value was printed or written to tracked files. Raw replacements
remain in a mode-`0600` temporary file.

## Evidence

- `git filter-repo` was absent from the system command path.
- Version verification succeeded after invoking the isolated module with an
  explicit `PYTHONPATH`.
- The optimized coverage helper completed in one cached pass and found three
  confirmed values across the 18 local branch histories.
- A complete 18-branch rollback bundle verified before rewrite, with 691 unique
  reachable commits recorded in the pre-rewrite manifest.
- The sandbox error named a `.git/refs/remotes/origin/...lock` path and reported
  a read-only filesystem.
- The postmortem helper returned an argparse usage error before reading or
  changing its ledger.
- The staging failure occurred before the index changed; the intended four-file
  set remained unstaged.
- Exact-value verification remained clean; the only post-commit finding was the
  auditor's disclosure-safe email category for the newly introduced plan blob.

## Current Status And Next Steps

Resolved. The failed sandboxed attempt left all 18 local refs identical to the
pre-rewrite manifest. The same reviewed command then ran with narrowly
escalated `.git` write access. `git-filter-repo` rewrote the graph and removed
`origin`; the requested SSH URL was restored afterward. Reflogs were expired and
garbage collection pruned unreachable objects without a push.

## Root Cause And Resolution

- The isolated launcher assumed a normal site-package installation. Supplying
  the isolated target through `PYTHONPATH` loaded the installed module without
  modifying the user environment.
- The first coverage helper had an avoidable per-branch/per-path subprocess
  loop. A single historical blob inventory and cache reduced the completed pass
  to a few seconds.
- The default workspace sandbox exposed `.git` read-only. After confirming the
  failed attempt had not moved any ref, the authorized history rewrite used a
  narrow escalation for the same reviewed command.
- The postmortem-memory retry uses the helper's live `scan --help` contract
  rather than assuming the report path is positional.
- Closeout staging uses the same narrow Git-metadata escalation already required
  by the authorized rewrite; staged paths and diff are inspected afterward.
- The single unpushed closeout commit is recreated from the same parent with the
  same message, author, committer, and dates after replacing the plan's literal
  remote URL with a neutral description. The rejected object is then pruned.

## Verification

- All 18 local branch tips equal the old-to-new commit-map targets.
- Of 691 commits, 430 IDs changed, 261 remained identical, and none were
  dropped. Author, committer, timestamp, message, and mapped-parent comparisons
  reported zero mismatches.
- The exact-value verifier scanned 5,883 commit/blob/tag objects and reported
  zero forbidden occurrences before pruning.
- The independent public-history auditor scanned 691 commits and 5,192 unique
  blobs and reported zero findings.
- Reflog inventory and `git fsck --full --unreachable --no-reflogs` both reported
  zero retained entries before the requested immediate prune. Final verification
  is repeated after the documentation commit.

## Remaining Limits

Broad regexes also surfaced 11 reviewed non-credentials: synthetic fixtures,
ordinary prose, and code identifiers. They remain unchanged. The public remote
still contains the old graph until the user runs the force-with-lease commands
in the external report; no rotation or remote push was attempted here.
