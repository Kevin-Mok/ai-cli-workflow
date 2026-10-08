# Codex picker temporary-file lookup crossed permission boundaries

## Symptom and impact

A read-only rg --files /tmp search for an existing refresh wrapper returned exit 2
because unrelated private systemd/snap directories deny access. Matching wrapper
paths were still returned. No repository or live files were changed by the search.

## Evidence and cause

Observed Permission denied for unrelated private directories. The search root was
broader than necessary. Timestamp regressions passed independently (90 tests).

## Lookup and resolution

Read postmortem-memory before remediation. Query: rg permission denied broad tmp
search. Existing lookup guidance and environment findings establish explicit paths
as the safe boundary; unrelated service/build findings do not apply. Read the
returned exact /tmp/codex-recent-refresh.fish path instead of retrying recursion.
Exact file read passed, exit 0. No permission changes required.

## Status and follow-up

Verified workaround: exact-path read succeeds; private directories remain protected.
Keep future temporary-wrapper lookups bounded. No new learning beyond existing
narrow-discovery guidance; register this report with that explicit decision.

## Ledger inspection correction

A diagnostic assumed a top-level sources key and raised KeyError; sources are
actually indexed under reports. A subsequent read-only key inspection confirmed
the schema. The installation/verification commands still completed, exit 0;
no ledger write occurred before inspecting the actual schema. Register under
reports and run the targeted checker. This is an existing schema-inspection
lesson, with no new reusable finding.
