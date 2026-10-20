# Concurrent staging changed a commit candidate

Use a separate Git index when sessions share a checkout so a verified candidate stays scoped through commit hooks.

- Symptom: a commit hook rejected a home_path finding after the explicit candidate gate passed.
- Evidence: the staged candidate changed from six files to nineteen files and its isolated refresh report record was replaced by another session’s redshift report record.
- Impact: the commit did not complete; no history was rewritten.
- Lookup: existing public privacy and scoped Git guidance applies. The safety hook correctly blocked the changed candidate.
- Resolution: prepare a separate temporary index from HEAD containing only directly observed session files and reviewed report records. Keep the shared index and unrelated work intact.
- Status: separate-index retry pending; privacy gate and ordinary hooks remain required.
