# Skill reference lookup during tw shortcut setup

This report tracks a failed documentation read while configuring the `tw`
directory shortcut. Discover the actual reference path before retrying the read.

- Symptom: `cat` exited 1 because
  `~/.agents/skills/superpowers/references/codex-tools.md` does not exist.
- Impact: one documentation read failed; no configuration changed.
- Evidence: the other requested skill file was read successfully in the same
  invocation; the error names only the missing Codex reference.
- Lookup: searched postmortem memory for
  `missing skill reference No such file or directory` and found
  `local-discover-paths-before-reads` (search ledger: `verified_fix`; reference:
  `verified_workaround`). Its instruction to
  discover package paths applies directly to this guessed reference path.
- Root cause: resolved a relative reference from the skill collection instead
  of the directory containing `using-superpowers/SKILL.md`.
- Resolution: checked existence and successfully read
  `~/.agents/skills/superpowers/using-superpowers/references/codex-tools.md`.
- Verification: the corrected read exited 0 and returned the Codex platform
  instructions. This verifies documentation access only.
- Status: resolved; no user configuration was affected by the failed read.
- Learning: no new reusable guidance; the existing path-discovery finding
  already covers this error. Register this report's reviewed hash and alias
  in the tracked ledger and run its targeted coverage check.
- Follow-up: resolve references relative to their containing skill directory.
