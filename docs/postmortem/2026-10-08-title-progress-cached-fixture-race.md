# Cached picker fixture overwrote ready state during startup

Record the terminal-fixture failure before retrying it, then preserve cached
state and verify opening titles without launching replacement inference.

## Symptom and impact

Commit verification ran 98 search tests in 25.328 seconds and failed one live
terminal assertion. The cached Guardian fixture expected both cached headlines,
but ID1 was already Guardian review with generating status while ID2 was ready.
Commit and push were deferred; no production module failed this assertion.

## Lookup and evidence

Query: fzf cached fixture startup state async race. The reviewed
local-picker-live-headline-integration guidance requires the actual fzf path;
local-descendant-exit-observation concerns asynchronous child exit and does not
repair cached-state setup. Inspection shows SyntheticManager.start always
queues ID1, and run replaces its preseeded ready state with generating. The
initial cached assertion therefore depended on thread scheduling. Real
SummaryManager preserves usable cached recaps instead of launching this work.

## Resolution and verification

Verified fixture fix. Synthetic automatic startup skips ready entries. The cached
scenario verifies opening headlines, directory query and exact selected UUID,
with zero inference workers. Dedicated uncached modes retain live replacement,
Ctrl-G, refiltering, progress and cancellation checks.

python3 tests/scripts/codex_recent_live_check.py passed both result lines, exit 0.
python3 -m unittest discover -s tests -p 'test_codex_search*.py' passed all
98 tests in 38.034 seconds, exit 0. No provider calls or production changes were
needed for this correction.

## Learning and limits

Update local-picker-live-headline-integration with cache-preserving synthetic
startup and zero-worker cached verification, register this report hash, and run
the targeted ledger check. This proves the fixture and live fzf/cache-title
path; it does not establish provider performance or eliminate all scheduling
variation. Keep the existing uncached runtime coverage.
