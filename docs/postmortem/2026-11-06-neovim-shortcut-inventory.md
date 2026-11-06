# Neovim shortcut validation and scope warnings

This report records an unrelated skill-catalog validation gap found while verifying explicit Neovim file shortcuts.

- Symptom: `scripts/sync-vetted-skills --check` returned exit1 with243 source entries and2 missing calibration entries: installed:agents:no-mistakes and installed:claude:no-mistakes.
- Impact: whole-host inventory cannot claim PASS. The23 shortcut tests,7 admission tests, frozen trigger replay46/51 and generator shell syntax pass.
- Evidence: the warning names installed no-mistakes copies; this task edits only fish-alias and its generator. The prior naming-fix inventory reported241 entries/0 missing. No no-mistakes source, installation or calibration was changed in this task.
- Lookup: queried `skill inventory missing calibration installed only`; no directly applicable incident finding was returned. Existing lean-instructions calibration guidance already requires explicitly recording installed/configured source drift.
- Cause: installed sources are absent from the existing calibration inventory. This is separate from the Neovim editor-selection change.
- Status: unresolved host inventory warning; Neovim implementation verification continues.
- Decision: no new reusable learning; preserve unrelated skill installations and calibration. Do not expand scope or claim an inventory pass.
- Next steps: record this warning in the plan/handoff; reconcile those two installed-source entries in a separately authorized catalog task.

- Delivery scope guard: the feedback log received another concurrent append after the task snapshot. A helper expected exactly one new entry and stopped; the next staging command then could not read its missing feedback snapshot. Initial partial staging contained only explicitly named task files and reviewed README/smoke hunks.
- Scope lookup: queried concurrent append/feedback/staging preservation; existing explicit-path and unrelated-work policies apply. Resolution: construct the feedback index blob from HEAD plus only the exact owned Neovim entry, leaving all concurrent additions in the working tree. Do not include unrelated new log entries.
