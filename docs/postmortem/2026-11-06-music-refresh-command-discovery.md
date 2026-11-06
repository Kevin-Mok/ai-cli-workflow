# Refresh command discovery during music priority change

A guessed executable path for refresh-config was absent. Discover the existing Fish function before applying configuration.

## Symptom and impact

An optional probe of `/home/kevin/.local/bin/refresh-config` reported no such file. No files or runtime state were changed; the task was not blocked.

## Evidence and lookup

`command -v refresh-config` in Bash returned no path; `ls` of the guessed path reported absence. Reviewed lookup `refresh-config command missing path` matched `local-discover-paths-before-reads`: refresh is a Fish function, so this applies directly. Missing optional files are diagnostic outcomes, not runtime defects.

## Resolution and status

Use the tracked/live Fish function discovered from repository evidence. No retry of the guessed executable is needed. Discovery issue resolved; applying configuration is verified separately in the task plan.

## Follow-up and learning

No new learning: the existing path-discovery finding already covers this exact mistake. Discover shell functions before assuming an executable path.

## Fish startup permissions

A subsequent read-only `fish -c 'functions --details refresh-config'` resolved the function but normal interactive startup attempted fnm multishell and generated-alias writes outside the workspace. The sandbox denied these (read-only filesystem); command exit was 0 despite startup diagnostics. No application playback was touched. Lookup `fish startup read-only fnm multishells` did not provide a narrower applicable remedy. Run the authorized refresh through Fish without startup and explicitly source its required functions, requesting normal sandbox escalation for home configuration writes. Do not treat the diagnostic command's exit as proof of clean startup. Existing environment/path-discovery guidance covers this; no new learning.

A later guessed `dot_config/fish/functions/sync-shortcuts.fish` was also absent; no command was executed from that path. Delegate discovery of the existing refresh dependency before invoking it. This repeats the same path-discovery lesson.

## Verification

Scoped `fish --no-config` with the tracked cli-message and refresh-config functions and existing sync-shortcuts script completed successfully (exit 0, REFRESH COMPLETE). Installed now-playing helper is byte-identical to source; a live poll selected Spotify. This verifies configuration deployment without exercising live audio resume.
