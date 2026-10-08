# Guardian title still generic while its recap was running

Inspect the exact row in the live picker before changing code again. Compare
picker start, cache completion and displayed title to distinguish a missed update
from an unfinished background recap.

## Symptom and impact

The user reported another Guardian review row at Toronto 13:44 after the live
update fix. A safe metadata inspection found the corresponding entry with a
ready descriptive headline. Reading the authenticated fzf state confirmed that
same UUID displayed the descriptive headline in the actual running picker.
No selection changes, provider calls or raw dialogue reads were made.

## Evidence and cause

The picker opened at 2026-10-08 13:44:06.647 Toronto time. The exact recap cache
was written at 13:44:34.641, approximately 28 seconds later. The row was second
in discovery order. Installed/source picker bytes matched. The current fzf
state returned the AI headline in title field four and ready/partial status.
The observed remaining generic label was transient while background generation
completed; this row's update path is working. Serial queue and provider latency
mean opening the picker does not immediately provide every missing AI headline.

## Lookup and applicability

Previously reviewed local-picker-live-headline-integration establishes current
headline publication and real fzf checks. SummaryManager inspection confirms one
serial worker and the newest-20 automatic window; no-summaries prohibits manual
and automatic generation. The live-state comparison applies directly here.
Source read found no missed-update defect for the exact reported row.

During investigation, a combined rg command included the guessed nonexistent
path tests/test_codex_search_recent_cli.py. rg reported file absence; later reads
succeeded and the combined shell exit was zero. This did not change files or
invalidate live-state evidence. Use rg --files before further fixture reads.

## Status and next steps

Observed live behavior is correct for this row. Updated the operator guide and
manual smoke check to wait for the preview's ready state before verifying its
AI title. A queued/running recap can retain the generic title temporarily. The
prior live-title fix and batch policy remain unchanged; no extra inference was
triggered. Register the reviewed live timing evidence and check this report.

## Limits

The screenshot capture time is not embedded in the image. Timestamps prove the
28-second completion interval and current descriptive display, not the exact
internal state at capture. Generation can fail or remain outside the automatic
window for other rows; this report only establishes the reported 13:44 entry.
