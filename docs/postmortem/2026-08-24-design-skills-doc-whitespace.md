# Design Skills Documentation Whitespace Failure

- Symptom: `git diff --cached --check` rejected the staged design-skills change.
- Impact: The design-skills commit was paused before creation.
- Evidence: Three new postmortems had trailing whitespace and two new documents had an extra blank line at EOF.
- Root cause: Markdown hard-break spacing and final blank-line residue were not checked before staging.
- Resolution: Remove only the whitespace residue and rerun the staged whitespace check.
- Verification: `git diff --cached --check` passed after the whitespace-only cleanup.
- Follow-up: Include whitespace validation in the final design-skills pre-commit check.
