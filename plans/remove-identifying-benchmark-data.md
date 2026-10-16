# Remove identifying benchmark data

This change removes raw benchmark run artifacts from the public repository and its history, keeps the benchmark harness usable with private local output, and records the publication rule. Verification covers current files, rewritten history, pending work, and the remote branch.

## Outcome and scope

- Remove both `benchmarks/metaprompt/runs/` and `benchmarks/metaprompt-selection/runs/` from every public commit and the active source tree. Preserve a private recovery copy.
- Retain benchmark code, fixtures, protocols and aggregate findings in documentation. Update links that previously pointed to raw run artifacts.
- Ignore future raw run output and detect persisted runtime identifiers in the public-history auditor.
- Record the durable rule in `AGENTS.repo.md` and the canonical append-only feedback log.
- Commit this cleanup and plan together, then force-update `origin/main` with an exact lease. Preserve unrelated pending migration work without committing it.

## Context and settled decisions

The starting branch is `main` at `4ee31274b5b68a6db5ddd0fe6acdd429df41bc8a`. Its 683 commits use the explicitly approved public author identity. Initial status has 43 modified and 28 untracked paths, with nothing staged. The private safety review found runtime correlation metadata in 121 tracked benchmark artifacts and historical blobs; no authentication credential was found in the pending content. The requested cleanup removes raw artifacts rather than publishing individual runtime traces with partial redaction.

Recovery contains a verified bundle, original index, status and complete candidate-file archive under a private `~/.local/state/ai-cli-workflow-public-cleanup-<timestamp>/` directory. Original file hashes/modes are recorded there. Existing migration archives remain private and untouched.

## Checklist

- [x] Capture status and verified private recovery before modifying tracked files.
- [x] Map harness callers, tests, docs and runtime metadata boundaries.
- [x] Save the durable publication rule.
- [x] Add defining privacy and ignored-output checks; observe RED, implement GREEN.
- [x] Remove raw run trees and update affected documentation without losing aggregate findings.
- [x] Rewrite in an isolated clean repository; retain author identity, topology, messages and timestamps.
- [x] Prepare a cleanup-only commit/index with this plan; preserve all unrelated dirty work.
- [x] Run focused regressions, boundary scans, README gate and fresh safe refresh.
- [x] Independently review the final result and recovery path; resolve stale smoke and handoff references.
- [ ] Force-push with an exact lease; align the active checkout without resetting dirty files.
- [ ] Verify remote, pending work, absence of identifiers and current/history artifact boundaries.

## Risks and recovery

History rewriting changes descendant commit IDs. An exact force-with-lease must refuse a concurrent remote update. Work occurs in a clean isolated clone because the active checkout has unrelated edits. Never stash, reset, clean or overwrite those edits. Keep the original bundle and working-file archive privately; do not publish backup refs. Removal of raw evidence reduces public reproducibility, so aggregate claims retain their limitations and explicitly describe private raw records. Cached or independently copied GitHub objects cannot be recalled by a force-push alone.

## Verification

Defining tests exercise runtime identifiers in ordinary and nested serialized JSON and ensure findings never echo values. Regression coverage includes the public auditor and benchmark harness/analysis suites using synthetic repositories and temporary run folders. Boundary verification enumerates paths in all rewritten trees, scans for privately retained original identifiers, confirms ignored run roots, and checks the candidate index and working files separately. Generic email findings are classified only for the exact user-approved author headers; other commit, message and file content remains in scope.

Fresh `fish --no-config` must load the current safe refresh helper; scripts, externals and removals stay excluded. Check README usage, local source mapping and protected machine settings. Compare every pre-existing unrelated pending file against its initial recorded bytes and modes. Verify the actual GitHub `main` hash after the leased update.

## Progress and review evidence

Implementation and observed test/review evidence will be recorded here before the cleanup commit. Runtime publication evidence is retained in the private recovery journal and reported in the handoff, so final publication does not require amending the verified commit.

Observed evidence: privacy defining tests first failed for three missing runtime detections and the raw-output staging boundary, then all 13 auditor tests passed. The focused nine-module regression passed 97 tests with no failures/errors; two sandbox socket denials were resolved by the scoped loopback-only synthetic runner. Both preview commands exited 0 without model calls after removing 138 raw run files. Source verification exposed pre-existing pin mismatches; the two affected source files and manifests match starting HEAD bytes. These remain documented in `docs/postmortem/2026-10-16-benchmark-source-pins.md`; no frozen input was repinned. The isolated rewrite verified 683 commits and 674 unique tree pairs: only the two run roots changed; all other historical entries, messages, identities, timestamps and parent topology were preserved. Exact original runtime values are retained only as private scan rules.

The tracked rule now explicitly identifies this as a public repository and forbids force-adding sensitive artifacts. A realistic UUID in an existing untracked test fixture was replaced with a clearly synthetic value; the rest of that feature remains pending. A guarded patch check refused an append hunk whose context included unrelated pending smoke notes; applying only the new appended section preserves that work. README gate passes. Fresh safe refresh completed with exit 0 after private live-target backup; installed-inventory formatting and helper-loading probes are recorded in the source-pin incident. Public incident aliases stay neutral; exact source aliases are checked in a private derived ledger overlay.


## Verified cleanup milestone

The final clean candidate passed the nine-module,97-test regression after raw
records were removed (exit 0). Its all-object and current-file scan found no
residual findings after classifying only the 683 explicitly approved author
headers;605 privately retained original runtime values were included as exact
rules. Independent review reproduced all 683 commit and 674 tree comparisons.
It identified stale smoke/handoff references; those now require private record
restoration, remove broken raw links and disclose the existing verify exit 1/2.
The reviewer confirmed the corrected file bytes.1,607 unrelated candidate files
retain their original hashes/modes; the sole intentional unrelated fixture
change is a synthetic replacement for its real-looking runtime UUID.

Delivery uses one focused commit, `security: remove identifying benchmark run
artifacts`, with this plan and related policy, scanner, tests and documentation.
The active repository has no linked worktrees and only main/origin-main refs;
its local Git configuration contains only standard clone/upstream entries.
Prepare independent clean Git metadata from the verified candidate, archive the
complete old `.git` privately, then replace only Git metadata after the exact
remote lease succeeds. The working files are never reset or checked out. The
new index comes from the cleanup commit, preserving the original pending work
without retaining deleted raw objects in the active object database. Recheck
HEAD, index identity and working fingerprints immediately before replacement;
refuse any concurrent change. The private bundle, original index and file
archive remain the rollback boundary. After publication, verify the actual
remote hash and rerun all-object plus pending-content checks; record resulting
commit/hash and publication evidence in the private recovery journal.


Remote inventory discovered 17 public archive branches in addition to main and
no tags. Twelve archive tips still contain raw run records; the complete remote
has 1,371 unique commits. Publication is paused until those references receive
the same removal and an all-ref audit. Preserve all 18 original tips and objects
privately. Keep branch names and safe content, apply the already requested
public author identity to older archive history when needed, and use an atomic
push with exact leases for every changed ref so no partial remote rewrite can
occur. Verify every public ref after publication, not main alone.


All 18 public branch tips now have cleaned counterparts. The original 1,371 commit
objects normalize to 692 distinct safe commits after the two-root removal and
the previously requested author identity; overlapping histories deduplicate.
The all-object audit of the independent candidate passes:692 approved author
headers, zero residual history/current findings, zero raw paths in every
reachable tree, and both output roots ignored. All 1,606 unrelated current files
still match their original bytes/modes after adding the reviewed handoff to
scope. The final fresh-shell refresh exits 0; both actual preview entrypoints
exit 0 with `dry_run_no_model_calls` / `no_model_calls`. The private learning
ledger targeted check reports errors[] with the updated incident hash.


Independent all-ref review passed 1,371 actual commit pairs and 683 unique complete
tree pairs with zero unapproved differences. The author normalization changed
688 older archive headers; committer data, author timestamps, messages, safe
files and branch names remain preserved. All 17 archive heads are included in
the verified candidate. Final publication uses exact leases for all 18 refs.
