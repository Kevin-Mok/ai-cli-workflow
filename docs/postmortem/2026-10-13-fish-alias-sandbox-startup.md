# Fish alias sandbox startup failure

The default shell runner failed before shortcut inspection. Approved scoped execution lets this task proceed; the host sandbox remains unresolved.

- Symptom: `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`; initial read-only command exited 1 before execution.
- Impact: No files changed and no mapped command ran during the failed invocation.
- Lookup: Query `bwrap loopback Failed RTM_NEWADDR` matched `local-sandbox-loopback-approved-route` in `references/execution-environments.md`; the startup failure matches its applicability.
- Evidence: Approved scoped execution returned repository status and instruction files with exit 0; mapping previews also exited 0.
- Cause: Sandbox loopback initialization denied; underlying host policy cause remains unverified.
- Resolution/status: Verified workaround using scoped approved execution. Default sandbox remains unresolved.
- Next steps: Mappings deployed successfully through refresh-config; repeat previews returned changed=false and generated syntax passed. Host sandbox repair is separate work.
- Learning: No new reusable learning; existing approved-route guidance covers this exact symptom and limitation.

## Verification command correction

- Symptom/evidence: Fish rejected a double-quoted regex ending in a literal dollar sign with `Expected a variable name after this $`. No app launched and no process was killed.
- Impact: That invocation did not inspect the abbreviations; earlier refresh succeeded.
- Lookup: Queried `fish dollar double quoted regex`; the Fish diagnostic directly identified expansion syntax.
- Cause/resolution: An unnecessary regex end anchor was interpreted as Fish variable syntax. Remove the anchor and inspect the complete matching lines.
- Status: Corrected inspection commands exited 0 and printed `v vesktop`, `kav killall vesktop`, and `kad killall discord`; generated syntax passed `fish -n`. No product behavior changed.
- Learning: Existing shell transport/quoting guidance applies; no new reusable learning.
