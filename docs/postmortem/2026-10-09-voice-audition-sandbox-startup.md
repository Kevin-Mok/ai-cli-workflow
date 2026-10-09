# Voice audition command sandbox startup

This records command-runner startup failures while preparing a local Piper voice audition script. Continue scoped work through the approved runner; host sandbox repair remains separate.

- Symptom/evidence: the first read-only command failed before shell launch with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`. A parallel read-only catalog probe reported the same error.
- Impact: ordinary command execution unavailable; repository and speech runtime were not changed by those launches.
- Lookup: `bwrap loopback Failed RTM_NEWADDR` matched `ext-sandbox-loopback`, verified_workaround. Its pre-shell signature applies; approved scoped status/source reads exited 0.
- Current status: verified workaround; use require_escalated only for authorized scoped operations. The underlying sandbox defect remains unresolved.
- Additional diagnostic: an optional `rg --files ... .codex` operand reported a nonexistent checkout directory; installed configuration lives under the home directory. Other inspected paths were valid; no implementation failure.
- Learning: no new reusable learning; existing environment guidance covers the identical startup symptom and workaround.
- Next steps: implement and verify the voice audition command; retain host sandbox repair outside this task.
