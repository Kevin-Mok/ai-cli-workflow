# Concat task skill reference lookup

The concat implementation briefly hit a missing documentation path. Resolve relative skill references against their containing skill directory before continuing.

- Symptom: reading `/home/kevin/.agents/skills/superpowers/writing-good-tests.md` exited 1 with `No such file or directory`.
- Impact: one read-only lookup failed; no product files or media were changed by it.
- Lookup: `postmortem_memory.py search 'skill reference relative path missing file'` returned `local-discover-paths-before-reads`. Its guidance applies because this was a guessed parent directory, not a product defect.
- Root cause: `writing-good-tests.md` is relative to `test-driven-development/SKILL.md`, not its parent skill collection.
- Resolution and verification: reading `/home/kevin/.agents/skills/superpowers/test-driven-development/writing-good-tests.md` succeeded with exit 0 and returned the complete reference.
- Status: resolved; no retry or change to the concat script was needed.
- Learning: no new reusable learning; the existing `local-discover-paths-before-reads` guidance already covers this error. Register this report with that explicit decision.
- Next steps: continue the requested concat work; use the containing skill directory for relative references.

## Extensionless inventory import follow-up

The inventory agent attempted `importlib.util.spec_from_file_location` on the extensionless executable Python concat script. It returned a spec without a loader and raised `AttributeError` before probing or modifying media. Reuse the source through `runpy.run_path` rather than duplicating its capture-time parser. Retrieve applicable extensionless-loader guidance before that retry; inventory then completed successfully: all30 clips were probed and capture-ordered using the shared parser. No new loader was added.

## Knowledge edit follow-up

An empty apply_patch used a guessed `# Artifact Verification` heading and was rejected because that exact heading was absent. No content was changed by the rejected patch. The intended new guidance section was appended explicitly without replacing existing text. This is the same already-reviewed exact-path/context discovery lesson; no new general finding.

## Native title availability

The native title update for the capture-order/resumable phase returned a transport error to the local MCP endpoint. It had no product effect. Follow the canonical unavailable-tool fallback: retain the existing native name, record the correct live objective in the plan, and do not repeatedly retry an unavailable metadata service. No new general learning.
