# Voice audition argument annotation shadowing

This records a new audition helper import failure found by its defining tests and type checker. Rename the argument namespace field, then rerun both checks.

- Symptom: all six audition tests errored during import; `voice: list[str]` raised `TypeError: bool object is not subscriptable`. basedpyright reported Variable not allowed in type expression at the same line.
- Impact: no models downloaded and no audio played; helper could not start.
- Root cause: class attribute `list = False` shadowed the built-in list during evaluation of the following type annotation.
- Lookup: `Python class list bool type annotation shadowing` returned type-related findings, but none matched this exact local name-shadowing cause. Stack trace and class scope establish the cause directly.
- Resolution: rename the namespace field to list_ and use argparse dest=list_, preserving the --list interface.
- Current status: verified fix: six defining tests pass (0.073s), and basedpyright reports 0 errors/warnings; both commands exit 0.
- Learning: record the repo-specific namespace lesson in tasks/lessons.md; no new reusable incident guidance beyond the existing type-check-before-completion contract.
- Next steps: continue real sample synthesis and broader regressions; the import failure is resolved.
