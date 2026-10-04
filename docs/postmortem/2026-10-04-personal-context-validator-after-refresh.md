# Skill validator path unavailable after refresh

This record tracks a validation-tool path change after the required config
refresh. Locate an existing validator or use the repository's reproducible
checks, then keep the chatbot's verification instructions accurate.

## Symptom And Impact

The required `fish -c 'refresh-config'` completed with exit 0. Installed skill
bytes, explicit invocation metadata, Claude linking, canonical instructions,
and the private store then verified successfully. The Second Brain regression
suite also passed 11 tests.

The next chained check could no longer open the previously used
`/home/example/.codex/skills/.system/skill-creator/scripts/quick_validate.py`.
Python exited 2. The remaining README and whitespace checks in that chain did
not execute and must be run separately. The validator had passed before refresh.

## Current Status And Investigation

No skill validation failure was reported; the validator file itself was missing.
Both installed skills roots remained ordinary directories, so inspection did
not establish a symlink replacement as the cause. The lifecycle of the managed
system-skill copy was not diagnosed further; no runtime chatbot file was missing.

## Resolution And Verification

Located an intact copy at
`/home/example/coding/codex-skills/skills/.system/skill-creator/scripts/quick_validate.py`.
Its validation of the final package passed with `Skill is valid!` and exit 0.
README and whitespace checks ran separately and passed. Smoke documentation now
uses this repo's own metadata/link tests, avoiding a dependency on the transient
system-skill installation path. Status: resolved for this task. No private
content or replacement validator was copied into the repository.
