# Progress cleanup test patch rejected its context

Record a rejected patch, inspect the exact test location and retry with one
focused hunk. Verify the target before treating rejection as an atomic failure.

## Symptom, impact and cause

While adding a cancellation progress regression, apply_patch rejected an extra
hunk targeting a line earlier than the preceding insertion. The removal was
unintended and unnecessary. Context verification failed and inspection found
that the cancellation test had not been inserted. No product changes from that
invocation were applied. Existing progress checks already passed.

## Lookup and applicability

Query apply patch expected context failed matched local-stale-patch-context.
Read its editing-shell-transport reference: reread exact current lines and apply
only remaining narrow changes. This guidance directly applies to the unnecessary
out-of-order hunk. A fresh source read confirmed the retry insertion point.

## Resolution and verification

Applied only the intended test insertion. Its intentional RED showed generating
status persisted after close. The minimum cleanup now removes active state and
contention timers after the worker is joined. The complete search suite passes
98 tests in 37.099 seconds, exit 0, including close/progress and exact resume.
The patch transport issue is resolved; no permissions or user changes were lost.

## Learning and follow-up

No new reusable learning: the existing scoped patch-context guidance covers the
cause and exact-context retry. Register the current reviewed hash and explicit
no-new-learning decision, then run the targeted postmortem-memory check.
