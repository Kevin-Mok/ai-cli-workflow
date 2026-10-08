# Dust logical-size comparison assumption

The defining comparison exposed a backend accounting difference. The wrapper retains Dust semantics and documents the difference; allocated fixture equality remains required.

- Symptom: Logical-mode fixture expected GNU du total 33,578,453 bytes but Dust returned 33,590,741, a 12,288-byte difference.
- Impact: Initial defining test failed; no source files were modified by scans.
- Lookup: Query `disk usage apparent size directory accounting` returned no applicable reviewed guidance. Tagged Dust platform.rs and per-inode fixture evidence were examined.
- Root cause: GNU du apparent mode omits directory metadata sizes; Dust sums each directory st_size. Three fixture directories each contributed 4096 bytes. Both tools count all hardlink names under Dust logical mode / GNU du --count-links.
- Resolution: Specify and test this material backend difference rather than change accounting or weaken allocated equality. Tests add exact known directory st_size to logical GNU comparator; documentation labels this mode.
- Verification: Disposable per-inode stat and direct Dust/du probes establish the 12,288-byte delta. Fresh complete contract run recorded in plan.
- Follow-up: Keep allocated and logical comparisons separate; pin backend and retest semantic differences on upgrades.
