# Codex priority refresh: picker identity and input replacement races

This records failures and verified fixes while adding AI priority and Guardian
refresh to the recent-session picker. Source CLI checks now preserve the query
and selected UUID through live updates and uncertain replies; recap tests cover
metadata-only input replacement. Protected installation and the fresh source
suite have passed. Normal sandbox startup remains unresolved outside scope.

## Evidence and impact

- Two initial shell reads failed before running with `bwrap: loopback: Failed
  RTM_NEWADDR: Operation not permitted`; the read-only investigation agent saw
  the same runner failure. Failed launches changed no repository files.
- An optional skill helper was invoked using a guessed nonexistent filename;
  two guessed test filenames also did not exist. These inspection commands
  changed no files. Repository inventory subsequently located the actual helper
  and the picker, recap, and live-fixture tests.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; findings
  `ext-sandbox-loopback` and `local-sandbox-loopback-approved-route` apply to
  the identical runner-startup symptom. Approved scoped repository reads and
  status capture exited 0. This is a verified workaround, not host repair.

## Current resolution and confirmed causes

The source and installed picker fix is **verified_fix**, confirmed cause, runtime scope. fzf
tracks positions during reordered reloads, and mutable shared input plus overlapping
reload/restoration actions could apply a position to the wrong generation. A saved
focus could also override a later visible selection. A lost HTTP reply was wrongly
treated as proof that an already-delivered action had not executed. Defining real-fzf
lost-reply checks reproduced the failure; the specific environmental cause of the
short transport delay remains unestablished.

The picker now serializes immutable row generations. Synchronous capture/load
callbacks publish revision-bound state without making HTTP requests from the
callback; the parent sends the restoration action, and fzf's executed callback
writes its revision acknowledgement. The parent retains that generation until
acknowledged and does not replay uncertain position actions. Enter accepts the
currently visible UUID, and shutdown distinguishes normal process exit from a
live-picker failure before reaping watcher, fzf and workers. The actual source CLI
passed three complete disposable Guardian append/rename, cached-priority and
newest-first repetitions. Real-fzf fixtures also passed deliberately lost reload
and restoration replies with exact UUID/query and cleanup assertions.

The recap replacement fix is **verified_fix**, confirmed cause, code scope. A
metadata/tool-only source refresh can re-extract dialogue into a new filename
without changing its hash, then delete the old file. Retaining an old queued or
lock-waiting entry by generation key kept that deleted filename and consumed its
only attempt. Three defining replacement tests observed unavailable != ready.
Queued entries now receive fresh same-key metadata. Under the index lock, the
worker selects the latest same-key input; before the UI receives a watcher update,
a missing file can recover through the validated canonical manifest only for the
same UUID/hash. Actual SHA256 is checked before inference. All 36 recap tests
passed, including replacement, cancellation and delayed-result checks.

Protected installation and fresh source/runtime verification passed; this does
not establish provider availability. Continue using the
approved scoped execution route and leave host sandbox repair outside this task.
No private session payloads or live provider calls were used.

## Reviewed learning and limits

- Add `local-fzf-serialized-reload-acknowledgement` in API contracts and fixtures
  and `local-recap-same-key-input-replacement` in state and security. Both have
  confirmed causes; the former has source runtime evidence and the latter code
  evidence. The protected installation evidence is recorded separately below.
- Lookup `fzf listener connection refused cancellation reload selection` matched
  the existing stream/headline findings, which cover adjacent identity/cleanup
  checks but not the late listener exit or uncertain delivery. Lookup
  `metadata-only replacement dialogue filename queue index lock` did not identify
  the same-key replacement remedy; the existing cache lifecycle finding covers
  disappearing reads and lock ownership, not refreshed input references.
- No new sandbox or path-lookup learning: the existing approved-route and file
  inventory guidance cover the repeated runner startup failure and guessed
  absent helpers/manifests. Scoped reads worked; the runner was not repaired.
- No separate reusable finding for fixture setup/timing mistakes. The wrong
  inherited helper, old provider shape, placeholder hash, startup delay assumption
  and one-shot preview scroll were fixture defects, corrected using real fixture
  contracts and observed control state. They are not evidence of product fixes or
  transport cause. The chronology below retains their verification limits.

The following sections retain the investigation chronology; their pending states
precede the current focused verification above.

## Implementation compatibility investigation

The initial UUID-restoration implementation used generic fzf `transform`, but
installed fzf 0.44.1 rejected its load binding with `unknown action: transform`.
The real terminal fixture failed before listener startup, so priority/reordering
runtime activation is unverified. Lookup for `fzf unknown action transform`
returned no applicable action-compatibility finding. Consult the exact version's
upstream manual and use supported actions; add a regression to the real fixture.
A source lookup also guessed absent optional package/man paths, and the recap
agent guessed absent packaging manifests; no writes or product effects occurred.
Status: compatibility issue under investigation; existing unit priority/watcher
checks pass but do not prove installed fzf behavior.

## Integration review and current evidence

Generic transform was replaced with supported fzf 0.44 capture/load callbacks.
The standalone priority fixture has passed once, but repeated integrated runs
exposed a timing-dependent selected-UUID restoration failure; investigation is
active using control-state diagnostics. fzf filter with with-nth returns display
fields, so restoration retains UUID explicitly in its transformed filter output.
Resume and recap keys are disabled during reordered reloads; Enter always uses
visible UUID after restoration. A reviewer reproduced saved-focus overriding a
later user selection; the defining regression now passes with visible-only
acceptance. Runtime shutdown now stops watcher and fzf before directory cleanup.

Other observed outcomes: extra priority preview lines pushed remaining work below
the narrow preview viewport; the fixture now scrolls to bottom before asserting
visibility. Synthetic legacy provider shape and invalid placeholder input hashes
were corrected to exercise the new production schema. A metadata-only Guardian
refresh also exposed deleted queued dialogue paths; three defining tests failed
unavailable != ready, then passed after same-key snapshots and canonical manifest
fallback were refreshed safely under the index lock.

Independent recap checks: 36 tests passed. One integrated search-suite run passed
118 tests; subsequent source/test updates and a standalone identity race mean that
run is not final completion evidence. Further exact CLI Guardian-refresh checks,
regressions and installation remain required. No live provider/private session
payloads were used.

## Final cancellation regression

The fresh 121-test search suite failed its real-fzf integration case after fzf
closed its listener during cancellation. The parent had entered an iteration
while fzf was alive, then posted the queued restoration action after exit;
connection refused became a SearchError and prevented the fixture result file.
Lookup `fzf listener connection refused cancellation reload selection` matched
the earlier UI-stream/headline findings, which apply to fixture identity and
cleanup but do not cover this late listener-exit race. The failing stack points
to the restoration POST, not source parsing or a provider failure. Preserve
fail-closed behavior for a live picker, and accept the normal closed-process
path when the process has exited. Rerun the executable reproducer and suite.

The first narrow plain-output regression failed at setup because RecentCLITest
reuses selected fixture methods rather than inheriting run_terminal. This is not
the intended RED and proves no product behavior. Inventory the fixture class and
reuse its existing terminal helper explicitly, then observe the decoration RED.

The next 122-test run failed the actual CLI fixture during its third, newest-first
cached opening: query did not match, then its listener refused connections. Live
Guardian append/rename and the second cached opening had passed. The fixture's
final diagnostic GET raised instead of showing its terminal transcript, so the
child exit reason is still unknown. Do not install until the actual CLI fixture
has actionable diagnostics and this intermittent path is reproduced/resolved.

Safe diagnostics subsequently exposed the parent message `cannot confirm updated
selection` during an initial visible 2/2 picker. The parent incorrectly treated
an uncertain local HTTP reply as proof that fzf had not applied an action. A
defining real-fzf fixture deliberately delivered startup/reordering restoration
actions and then lost their replies; it failed with the same SearchError before
the fix. Restoration now ends with a private revision acknowledgement written
by fzf's executed callback. The parent waits for that acknowledgement without
replaying positions, retains the immutable active input, and handles normal
process exit separately. The defining fixture passed with both loss kinds, exact
UUID/query and cleanup checks. Repeat actual CLI checks and full suite before
installation. The specific environmental cause of the short transport delay is
not established; the uncertain-delivery handling error is confirmed.

An additional lost-response fixture run selected during a timer-triggered reorder
and then expected that later navigation to be preserved as the captured earlier
focus. The control state showed correct row order but a different current UUID.
Priority fixtures now release their invented inference result only after the
defining UUID selection exists, rather than assuming startup finishes within
600ms. Actual CLI Guardian updates already append evidence after selection and
passed three fresh complete live/cache/recent repetitions with the new handshake.

The next broad run passed the actual CLI case but the 80-column preview check
scrolled once before a final asynchronous preview refresh, which reset the
viewport. Its control state retained the correct UUID/query and ready content.
The defining check now requests bottom while waiting for remaining-work text,
so it verifies the final rendered scroll behavior rather than assuming preview
completion when the row status first changes. No production scroll behavior
was changed.

## Final-suite fixture synchronization and budget

The synthetic active-inference index-lock check attempted its nonblocking .lock
acquisition once after the worker marker. The independent watcher could briefly
own that same lock, so EAGAIN exited the fzf stub with status 1; the picker treated
that as normal cancellation and the fixture's result file was absent. The focused
check alone passed in 0.38 seconds. The fixture now retries acquisition for at
most two seconds while the synthetic inference sleeps for 60 seconds, so a lock
held throughout inference still fails. Missing-artifact diagnostics are explicit.
This changes a fixture synchronization assumption, not production lock isolation.

The expanded all-mode real-fzf fixture also exceeded the original unittest
subprocess budget of 30 seconds. Its parent budget is now 60 seconds for 13
scenarios, each retaining its eight-second phase bound and printing scenario
progress. No owned synthetic processes remained after the timeout. Adjacent
index-lock/cache guidance applies to synchronization and cleanup, but no new
source-isolation finding follows from these fixture repairs. Their specific
no-new-learning decision is to wait for the defining observed state within bounded
phase deadlines, rather than interpreting a marker or aggregate runtime budget
as proof of a production failure. Final full-suite verification remains pending.

## Fresh source verification

The final source command
`python3 -m unittest discover -s tests -p 'test_codex_search*.py'`
passed all 122 tests in 69.796 seconds, exit 0. The shell launcher check and the complete real-fzf all-mode fixture exited 0;
README recruiter validation returned pass_no_change, and diff whitespace checking
passed. Independent acknowledgement review found no lifecycle/generation blocker.
The protected refresh and installed runtime checks below subsequently passed.

Identity evidence uses fixed queries during reordering. Simultaneous user query
editing during the load-time positional restoration interval was not independently
proved. Enter always accepts the visibly supplied UUID, which avoids substituting
saved focus, but that acceptance check does not establish preservation of an
interleaved query-edit/highlight intent. Keep this as an explicit verification
limit rather than claiming universal interaction stability.

## Verified protected installation

`fish /tmp/codex-priority-refresh.fish` called the real refresh-config workflow:
live Codex/Git snapshots, config sync, shortcut generation and fish reload, with
the remaining apply scoped to the six search targets. It reported REFRESH COMPLETE
and exited 0. All 46 guarded workspace hashes remained unchanged during refresh;
all six installed search files matched their source bytes, and codex-search was
executable. Installed help exposed the new sorting options. Fish runtime confirmed
`crg` expands exactly to `codex-search --recent --pick`.

The installed executable then passed this disposable fixture, exit 0:
`python3 tests/scripts/codex_priority_live_check.py --command /home/example/scripts/codex-search --scenario all`.
Guardian append/rename refreshed activity, dialogue digest and title; urgent work
became complete below actionable work. Fixed query and selected UUID survived
reordering; Enter resumed the exact UUID and directory. Cached priority and
newest-first openings reused recaps with zero additional inference calls, and all
workers, watchers and temporary picker directories were removed. Synthetic
inference used no live provider or private history payloads.

The implementation, focused reproductions, final source suite and protected
installed-runtime checks are verified. No further production/test edits are
planned; final diff review and user handoff remain. The unproved simultaneous
query-edit restoration interaction and unknown environmental transport-delay
cause remain the limits stated above, and host sandbox repair remains outside
scope.

## Learning ledger formatting guard

Final learning reconciliation stopped with AssertionError at its byte-preserving
JSON serialization guard after a shared-ledger update. The guard ran before any
ledger/reference writes, so no incident record was overwritten. Product code and
verification are unaffected; inspect the current shared formatting and preserve
all fresh records before reconciling this report's new hash. The formatting cause
is not established yet. Existing shared-file preservation guidance applies; this
is an authoring guard outcome rather than evidence of a new picker failure.

Fresh inspection found that the current ledger again round-tripped with its
existing UTF-8, two-space indentation and insertion order. The earlier mismatch's
precise transient origin remains unestablished. Reconciliation uses fresh parsed
records and narrow object replacements, preserving other records and formatting.
No new reusable learning is claimed beyond the existing shared-file preservation
rule; the targeted check is the evidence that the final authoring update is sound.

## Session-only commit preparation

The user subsequently requested `$commit-session`. Its scope helper returned
`unsafe` with no detected writes because this session's recorded tool calls use
the code-mode `exec` wrapper. This is the documented direct-write fallback:
review the actual successful edits, preserved snapshots and HEAD-based scoped
blobs; do not infer ownership from current dirty paths or timestamps. Shared
README, smoke checks, CLI decoration, incident knowledge and lessons contain
concurrent work that must remain outside this commit.

Two temporary preparation guards stopped before repository/index writes. The
knowledge-blob round-trip assertion used `ensure_ascii=False`; exact HEAD instead
uses ASCII escaping, two-space indentation and insertion order. Using
`ensure_ascii=True` round-tripped all 420,217 HEAD bytes and preserved existing
Unicode escapes. The documentation checker also interpreted status 1 from
`git diff --no-index --check` as whitespace failure although it printed no errors;
`--no-index` implies a difference exit status, so changed clean files return 1.
Check the diagnostic output separately from that difference status.

Lookup query: `shared ledger byte preserving scoped state JSON serialization
guard`. The confirmed `local-skip-worktree-and-scoped-state` workaround applies:
construct HEAD plus directly attributable additions and validate that candidate,
preserving all unrelated working bytes. The serializer equality and absence of
whitespace diagnostics establish these temporary-check causes. The three
candidate knowledge checks and README gate passed before the report hash update;
repeat targeted validation with the final reviewed hash before staging. No new
product failure or reusable finding is established by either tooling mistake.

The reference excerpt helper then raised `ValueError` because it assumed an HTML
anchor; the reference uses a Markdown heading. Reading the matching heading with
`rg -A/-B` confirmed the guidance without changing the file. This is another
read-only inspection mistake, covered by the same explicit no-new-learning
decision. The reviewed hash was reconciled again after recording it.

That hash updater also assumed `reports` was a mapping, but the ledger schema
stores a list. It raised `AttributeError` before a ledger write, and the following
targeted check correctly reported the changed report hash. Reconcile the known
prior hash by guarded text replacement, preserving the validated schema and all
other bytes; do not infer the schema without reading it. No product behavior was
affected. Targeted validation must pass after this correction before delivery.

Candidate copying then encountered a compiled `__pycache__` file beneath the
temporary core-blob directory and raised `FileNotFoundError` for its uncreated
destination. The two intended core source blobs had already copied successfully;
the repository and Git index were untouched. Use the explicit two-file allowlist,
never a recursive glob over scratch outputs, and compare their candidate hashes
with the reviewed blobs. The same scoped-state lookup applies; generated caches
remain excluded and this adds no new product finding.
