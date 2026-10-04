# Personal-context discovery included an absent directory

The initial read-only discovery command included the new skill directory before
it existed. This note records the harmless lookup failure and the corrected
discovery approach.

- **Symptom:** `rg --files` reported that the new personal-context skill
  directory did not exist.
- **Impact:** No files or private context were changed; the remaining requested
  instruction and adjacent-test reads completed.
- **Evidence:** The directory is a planned new deliverable, so its absence at
  the start of implementation was expected even though the search included it.
- **Root cause:** A discovery command mixed existing locations with the future
  skill location without first checking its existence.
- **Resolution:** Subsequent discovery uses existing parent directories.
- **Verification:** Repository status and adjacent tests were read successfully;
  implementation will create only the assigned new paths.
- **Status:** Resolved.
- **Follow-up:** Search existing parents when introducing a new skill.

A later read-only review also guessed two absent installer locations instead
of using the enumerated template path. The command exited 2 while its valid
reads completed. The reviewer switched to existing paths; no files or private
data were changed. This is the same discovery pattern, with the same resolution.
