# Private context helper sibling import failure

This report records and resolves a regression in loading the split storage helper through Python file-based imports.

## Symptom and impact

The focused storage regression suite reported two ModuleNotFoundError errors for knowledge_store. CLI retrieval tests passed, but tests loading context_store directly from its absolute file path could not find the sibling module. No real private data was touched.

## Evidence and lookup

Read canonical postmortem-memory; query `ModuleNotFoundError sibling file import sys.path` returned broad wrapper/path findings but no direct matching remedy. Reproduced and diagnosed the code itself. Existing 19 storage tests reproduced failures in designated-root validation and failed atomic replacement. Root cause: ordinary Python sibling import relies on sys.path containing the skill script directory, which direct file loading does not establish.

## Resolution and verification

Resolved bundled modules relative to __file__ and injected the current storage interface so patched destination policy and exception identity remain consistent. Fresh `python3 -B -m unittest discover -s tests -p 'test_personal_context*.py' -v`: 43 tests passed, exit 0, including both original regression failures and compact retrieval. Status: verified code fix; no real private data or installation checked by this test.

## Follow-up

Keep the direct-import regression tests alongside CLI tests. Installed helper paths must be independent of the active project directory.
