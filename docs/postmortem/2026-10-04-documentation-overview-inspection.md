# Documentation preference inspection

This records a harmless missing-path lookup while locating the configuration
refresh helper, and the corrected source used to finish the instruction update.

## Symptom and impact

A read-only `rg` invocation included an assumed
`dot_config/fish/functions/snapshot-codex-config.fish` path and exited 2.
No configuration was changed by the lookup.

## Cause and resolution

The helper is a Python script at `scripts/executable_snapshot-codex-config`,
not a fish function at the guessed path. The same search located the actual
script and its dry-run interface. Use the discovered source path.

## Verification and follow-up

The actual script source was inspected; configuration refresh results are
recorded below after the requested instruction and preference updates.

`snapshot-codex-config --dry-run` passed. `fish -ic 'refresh-config'`
completed with exit 0 and `REFRESH COMPLETE`. The installed
`~/.codex/AGENTS.md` matches the canonical source byte-for-byte, and
`git diff --check` passed. The instruction, append-only feedback entry,
README summary, manual check and VPS guide overview are updated.
