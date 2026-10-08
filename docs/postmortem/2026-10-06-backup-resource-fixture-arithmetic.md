# Backup resource fixture arithmetic correction

This report records a mistaken test expectation during the resource-budget extension. The fixture is corrected using a hand-checked conversion while retaining the same memory-ceiling requirement.

- Symptom: the GREEN resource test expected 46500 MiB for 75% of a 65011712 KiB total-memory fixture; implementation returned 49928994816 bytes.
- Impact: defining resource checks and the backup suite had one failure; no production backup was started, stopped or altered.
- Lookup: tracked memory has no specific finding for this fixture arithmetic. This is unrelated to the earlier tool wrapper parser failure.
- Evidence and cause: 65011712 KiB equals 63488 MiB (62 GiB); 75% equals 47616 MiB (46.5 GiB), or 49928994816 bytes. The production min(total,available) ceiling was correct; the independently typed test expectation was wrong.
- Resolution: replace the erroneous literal with 47616 MiB, preserving the intended total-memory upper-bound assertion. Run the defining tests and full backup suite fresh.
- Status: correction implemented; fresh verification recorded in the implementation plan.
- Learning decision: no new reusable finding; basic fixture arithmetic correction with no behavior relaxation.
