# Model command lookup sandbox startup failure

The model usage command lookup required an approved read-only route after the default runner failed before executing commands.

- Symptom and impact: two independent reads failed with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; shortcut discovery was briefly blocked.
- Lookup: `bwrap loopback Failed RTM_NEWADDR` matched `ext-sandbox-loopback`; the execution-environments reference applies because both errors preceded shell execution.
- Resolution and verification: approved scoped source reads and installed `codex-time models week --help` exited 0. The verified command is `codex-time models week --model-only`.
- Status: verified workaround. The sandbox itself remains unrepaired; no application fix was attempted.
- Learning and follow-up: no new reusable learning beyond the existing sandbox guidance. Continue to scope approved commands; host sandbox repair is separate work.
