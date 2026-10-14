# Binary Montage Extension Assumption

This report records a failed visual-review montage command caused by assuming
that every extracted large image used the PNG extension.

## Symptom

On 2026-10-13, ImageMagick could not open several requested `IMG-*.png` files
during contact-sheet generation.

## Impact

Only the temporary review montage failed. The extracted assets, private manifest,
rewritten history, and source repository were unchanged.

## Evidence

- The binary inventory contained both PNG and JPEG images.
- The failed command hard-coded `.png` for every review label.
- ImageMagick exited before a valid montage was produced.

## Root Cause

The command used a display label to reconstruct filenames instead of reading the
exact extracted filename recorded in the private binary-review manifest.

## Resolution

Generate the montage from the manifest's exact file paths and validate that each
input exists before invoking ImageMagick.

## Verification

Manifest-driven review successfully opened all six large image candidates and a
contact sheet for 258 small assets. The six large screenshots/mockups were
rejected and removed from every historical path; the 258 retained PNGs are
generic UI/icon assets.

## Follow-up

Use manifests as the source of truth when temporary artifacts can have multiple
extensions. The canonical postmortem-memory ledger is outside the authorized
folder and remains untouched.
