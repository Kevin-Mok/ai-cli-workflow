# Execution Routing

<!-- metaprompt-reference: execution-routing-v1 -->

## Run-signal boundary

Require a fresh standalone `go` for every execution and every high-stakes
pass. A prior signal never carries into a later pass. An original request to
"compile and run" or equivalent still compiles, presents, and waits; it is not
the standalone run signal. A `go` authorizes only the currently gated pass.

Only the exact standalone token `go` authorizes the current gate. Any synonym,
sentence, rider, or embedded run word is a revision: update the compiled
prompt, re-present it, and re-gate. The user may override execution mode by
naming one before authorization, but otherwise choose it for them.

Logistics riders change where or how the accepted prompt runs, such as pulling
an artifact into its slot or changing the destination. Incorporate them into
the run recommendation, then re-gate. Only compile-time assumptions belong in
the Assumptions line.

For Judge -> Rewrite -> Re-check, present all three numbered prompt blocks at
compile time but gate only Judge. After showing Judge's result, ask for a fresh
`go` for Rewrite; repeat after Rewrite for Re-check. Never run two high-stakes
passes from one signal or let an author certify its own work.

## Route order

Decide in this order; first match wins:

1. **Recurring or time-driven:** Polling, scheduled checks, nightly/daily work,
   or run-until-done on a timer belongs in a recurring or scheduled mode. When
   the harness exposes it only as a user-typed command, provide the exact
   command plus one line explaining why; do not claim it was scheduled.
2. **Substantial work with a verifiable end-state:** Tests green, a queue
   emptied, a migration finished, or explicit persistence belongs in a goal or
   until-done mode. If user-triggered only, give the exact command and why.
3. **Research, audit, broad parallel fan-out, multi-perspective verification,
   or a large multi-file migration:** Run an available workflow or parallel
   subagents. Use this only at genuine scale; normal tasks do not need fan-out.
4. **A big new build or anything destructive or hard to reverse:** Recommend
   planning first. If plan mode is user-triggered, say so and wait. Apply a
   reversibility check before any irreversible action.
5. **Otherwise (the common case):** Run the accepted prompt normally here and
   deliver the result. If another role clearly owns it, tailor and hand off the
   self-contained prompt.

Hard accuracy rule: never claim you invoked a user-only command. Give the user
the exact command and one-line reason. Subagents, workflows, and background
tasks are yours to run only when the harness actually exposes them. Name the
chosen mode and brief rationale in the gate so the user only needs to say go.
