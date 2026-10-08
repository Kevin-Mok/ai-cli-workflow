# Push tooling verification sandbox startup

This report records the runner workaround used to verify notification, shortcut, and directory-size changes for authorized delivery.

- Symptom: three initial read commands failed before shell execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` (exit 1). No repository content changed.
- Impact: instruction/status/plan reads required the approved scoped runner.
- Lookup: query `bwrap loopback Failed RTM_NEWADDR`; matched `local-sandbox-loopback-approved-route` and `ext-sandbox-loopback` in execution-environments.md. Their verified-workaround guidance applies because failure occurred before commands executed. Reviewed prior notification-speech-sandbox report and applicable reference.
- Status: verified workaround; escalated skill, git-status, and plan reads all returned exit 0. Host sandbox remains unresolved and outside this delivery scope.
- Verification: notification sound 37 tests/exit 0; speech setup 7 tests/exit 0; real Dust directory-size fixtures 9 tests/exit 0; private Xvfb/D-Bus Dunst check 1 test/exit 0. Fish shortcut 19 tests/exit 0. All five scoped checks passed; no application failure occurred.
- Learning: no new sandbox learning; canonical ledger/hash registration delegated to delivery coordinator to avoid shared-file races.
