# Discord speech optional-path inspection

A read-only inspection queried optional package files and a guessed refresh script. Use the mapped Fish function for subsequent deployment.

## Symptom, impact and evidence

The combined rg inspection exited 2 because package.json, pyproject.toml and scripts/executable_refresh-config were absent (stderr suppressed). Other requested source output was returned. No runtime task or tracked configuration was changed by the probe.

## Lookup and resolution

Read canonical postmortem-memory and searched `missing file probe rg exit`. Finding local-discover-paths-before-reads applies: inventory files and distinguish Fish functions from executables. The mapper located dot_config/fish/functions/refresh-config.fish; reading it exited 0. Root cause confirmed: guessed optional paths. Resolved inspection only; deployment and Discord acceptance are separately tracked in plans/discord-notification-speech.md.

## Follow-up

Use inventoried paths and existence checks. No new reusable learning beyond local-discover-paths-before-reads; no product fix required. A later combined read guessed sync-shortcuts.fish; cat reported it absent while other reads succeeded (overall exit 0). Delegated inventory now resolves the actual executable before deployment.
