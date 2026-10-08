# Fish alias completion sandbox startup

The shell sandbox failed before prompt inspection. Reviewed execution permits the authorized skill verification and installation to continue without changing host policy.

- Symptom: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`, exit 1; no command body ran.
- Impact: initial read delayed; no repository mutation occurred.
- Lookup: `bwrap loopback Failed RTM_NEWADDR`; reviewed `local-sandbox-loopback-approved-route` in execution-environments.md. Applicable because startup failed before requested output.
- Resolution and verification: same bounded reads with require_escalated succeeded, exit 0, including Git status before writes.
- Cause: loopback namespace initialization denied; host cause uninvestigated.
- Status: verified workaround; default sandbox unresolved.
- Next steps: continue scoped reviewed execution; host policy repair outside scope.
- Learning: no new learning beyond existing approved-route guidance.
