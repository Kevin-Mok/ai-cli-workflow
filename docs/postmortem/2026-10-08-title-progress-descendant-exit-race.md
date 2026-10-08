# Descendant shutdown assertion raced termination during progress verification

Keep the complete regression result visible and inspect signal/reaping evidence.
A bounded observation must reject a surviving child while allowing asynchronous
kernel exit to settle.

## Symptom and impact

The initial full search run had 97 tests in 33.595 seconds with one failure:
test_cancellation_stops_descendants_and_reaps_leader observed child state R
instead of Z immediately after close. Leader absence passed. Other progress,
queue, title and real-fzf checks passed. Installation was deferred for review.

## Root cause and lookup

stop_process sends SIGTERM to its owned process group, waits for the leader,
then sends group SIGKILL and waits for that leader. wait only reaps the leader;
signal delivery and descendant exit are asynchronous. The immediate proc-state
assertion assumed the descendant had already reached Z, creating a race.

Query descendant SIGKILL child zombie still running found no direct prior fix.
Reviewed local-cancellable-terminal-browser-owner applies to owned-group teardown
and real cancellation checks, but does not establish immediate descendant state.
Independent read-only review confirmed the group signalling and observation race.

## Resolution

The fixture retains immediate leader absence and polls the exact child's proc
state for at most one second, accepting only disappearance or Z. It catches
FileNotFoundError around the read to avoid an exists/read race. A genuinely
running child still fails at the deadline with its last state. No production
shutdown changes or extra provider calls were required for this correction.

## Verification and status

Verified fixture fix: the focused cancellation test passes in 0.050 seconds,
exit 0. The full search suite then passed 98 tests in 37.099 seconds, exit 0,
including this descendant test, stopped progress metadata, real-manager queue,
visible timers, AI title adoption and trusted UUID resume. Independent final
review found no blocking issues. git diff --check exited 0.

## Limits and follow-up

Linux proc-state checks use synthetic subprocesses. This fixes a test observation
race; it does not claim the production wait reaps grandchildren or retest live
provider shutdown. Register reviewed local-descendant-exit-observation guidance
and this report hash, then run the targeted coverage check.
