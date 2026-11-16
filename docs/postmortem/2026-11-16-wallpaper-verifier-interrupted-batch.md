# Interrupted exhaustive wallpaper verification

Finish exhaustive validation without mistaking partial output for a complete pass. Retain the interrupted log and obtain a fresh complete current-software report.

## Symptom and evidence

Sequential667-image exec session78805 exited143 after logentry354 began;353 images completed with no image failure reported. No final JSON was produced. Exact SIGTERM cause remains unknown; there is no evidence tying it to palette behavior or automatic approval. Log /tmp/wallpaper-all-final-2026-11-16.log is retained.

## Resolution

Use four bounded independent workers with separate temporary HOME/cache/GIMP profiles and logs; one main writer emits ordered results and the final exclusive JSON report. Do not splice successful retests into an old failure report. Existing real multi-image CLI/isolation regression passed again after scheduling change. Per-image timeout/progress and source/cache hashing remain unchanged.

## Verification and status

Resolved by verified execution strategy, not a claim that the unknown external termination cause was fixed. Fresh exec session28172 completed exit0:667/667passed,0collisions/0failures, source/cache hashesunchanged. /tmp/wallpaper-all-final-parallel-2026-11-16.json contains complete fresh rows, softwarehashes, per-role contrast/diversity and decoder evidence. Source coverage matches final scan exactly. No images moved or edited.

## Learning

SIGTERM143 long-command lookup returned unrelated environment/interruption guidance; no cause-specific remedy applied. Existing artifact completeness guidance covers not promoting partial output to success. No new generalized finding; final reviewed hash is registered, with runtime-only workaround status and unknown external cause explicitly retained.
