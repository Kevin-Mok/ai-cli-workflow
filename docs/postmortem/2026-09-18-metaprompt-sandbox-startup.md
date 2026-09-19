# Metaprompt repository read blocked by sandbox startup

- Date: 2026-09-18.
- Symptom: The initial repository and skill read failed before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` (exit 1).
- Impact: Prompt compilation could not inspect local instructions through the default shell sandbox; no repository files were modified by the failed command.
- Evidence: The same read-only command succeeded with the approved elevated execution fallback (exit 0), including the initial dirty-file inventory.
- Root cause: Sandbox loopback initialization was denied by the execution environment; the underlying host permission cause was not investigated.
- Status: Inspection unblocked; default sandbox startup remains unresolved.
- Resolution: Used the approved fallback for narrowly scoped repository reads. During the requested script-name revision, the patch helper also failed at sandbox startup; reran the same scoped patch through the elevated fallback.
- Verification: Canonical instructions, metaprompt compilation rules, preferences, and target filename availability were read successfully.
- Follow-up: Repair sandbox initialization separately; preserve all pre-existing dirty files. The same startup failure also affected an independent read-only reviewer and implementation-plan patches. Running the installed apply_patch helper explicitly through the elevated shell restored progress.
