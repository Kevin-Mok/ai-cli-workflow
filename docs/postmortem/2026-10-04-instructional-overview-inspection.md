# Instructional overview inventory lookup

This records a missing optional provenance-file lookup during the documentation
sweep. The source inventory established which files exist, and the sweep
continued with the available documentation.

## Symptom and impact

A read-only search included an assumed
`dot_agents/skills/brand-system-designer/SOURCE.md` path. That optional file is
absent; ripgrep reported exit 2 while the other requested sources were readable.
A later command completed, so the compound shell invocation itself exited 0.
No document or runtime behavior changed because of this lookup.

## Cause and resolution

The search assumed every imported skill has a `SOURCE.md`. The earlier file
inventory shows this skill has only its instruction, template, references and
agent metadata. Source-identity checks use those actual files; pinned metaprompt
provenance remains available and is preserved.

## Verification and follow-up

The repository-local and canonical brand files were confirmed to be separate
regular files with identical initial bytes. Locate optional sources with
`rg --files` before reading them, and inspect every batched command's result.
