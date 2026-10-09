# Task-completion policy edit: sandbox startup failure

Initial repository reads failed before shell execution. Approved scoped execution
unblocked the instruction update; host sandbox repair remains separate work.

- Symptom: four initial read-only commands exited 1 with
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: the command bodies did not execute; no files changed during those calls.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; reviewed
  `ext-sandbox-loopback` and `local-sandbox-loopback-approved-route` in
  the tracked execution-environments reference. Identical startup errors across
  independent commands establish applicability; the existing direct-verification
  policy startup report records the same limitation.
- Cause: denied loopback initialization. The underlying host policy was not investigated.
- Resolution: approved scoped reads, including `git status --short`, exited 0.
- Status: verified workaround; default sandbox startup remains unresolved.
- Next: continue the authorized documentation change through approved scoped
  execution; investigate host startup separately if needed.
- Learning: no new reusable learning; existing sandbox findings cover this exact
  symptom and workaround. Register the reviewed hash and alias with that decision.
