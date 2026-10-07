# Recent recap cache races found during independent review

Concurrent maintenance and interrupted generation exposed cache lifecycle defects. Reproduce them with synthetic fixtures, correct the shared-file boundaries, then rerun the recap and CLI checks.

- Date: 2026-10-07.
- Symptoms/impact: Clearing a cached UUID between exists and read raises FileNotFoundError into picker rendering. A worker losing the generation lock permanently consumes its attempt and displays generating after the other worker exits. An interrupted atomic save leaves a private tmp*.tmp file that maintenance rejects, blocking search/list/clear.
- Lookup: `cache clear race FileNotFoundError generation lock` found no directly applicable reviewed finding; returned MPRIS owner binding and locked authorization guidance concern different state boundaries. Fresh reviewer probes establish applicability locally.
- Evidence: Reviewer synthetic probes reproduced all three without inference or source-session writes. Main suite had passed 75 tests, demonstrating missing concurrency coverage.
- Root cause: Cache existence and read are not atomic; attempt bookkeeping occurs before exclusive ownership; orphan temporary files are not part of maintenance recovery.
- Current status: Fixed and verified. Missing-file races return missing, contention reconciles lock liveness without consuming an attempt, and validated orphan temporary files are removed under the maintenance lock. Unsafe file rejection and stable lock inodes remain intact.
- Verification: All three defining regressions failed for their reported reasons before fixes; 17 recap tests and seven real-fzf/picker tests pass afterward. Actual CLI plus sleeping deterministic recap verifies main index flock is free during inference, and cancellation reaps the leader and stops its descendant. Source immutability checks remain green. Eight integrated recent CLI tests pass.
- Review lookup incident: Read-only reviewer tried nonexistent `scripts/codex_search_picker.py` (exit 1); main explicitly imports `codex_search_recent.py`. Exact existing path then read successfully. No source mutation or implementation defect from this lookup.
- Learning: Reconcile transient cache liveness at the read boundary, count attempts only after generation ownership, and recover safe orphan atomic files under the maintenance lock. Register verified code finding; runtime evidence is synthetic, not a provider availability claim.

## Runtime publication and attempt deadline review

Independent review also reproduced close() observing runtime=None during delayed
construction, then joining while prepare() began after cancellation. The defining
constructor-barrier test observed RED. Publish the runtime under the manager's
condition with a stop check; a cancelled newly constructed runtime never prepares.
A shared monotonic deadline now bounds both configuration probes and inference,
so no process starts after the 120-second attempt expires. Both new deadline
checks observed RED, then GREEN. Full suite89 and Pyright0 errors pass. The actual
CLI index-lock fixture acquires the index flock while inference is sleeping.
