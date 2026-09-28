# Mixed camera concat ordered incorrectly and corrupted a stream-copy join

## Symptom and impact

On 2026-09-28, `concat-timestamped-videos` could not safely join `PXL_20260928_011900910.mp4` with `IMG_1377.MOV`. Directory listing placed the iPhone clip first by lexicographic filename, and stream copy across the two codec profiles produced decoder errors.

## Evidence

A list-only reproducer placed `IMG_1377.MOV` at position 6 and the Pixel clip at position 19. The Pixel filename encodes 01:19:00.910 UTC; the MOV `creation_time` is 01:21:49 UTC. `ffprobe` showed HEVC Main, 8-bit BT.709 in the Pixel clip and HEVC Main 10, 10-bit HLG with Dolby Vision metadata in the MOV. A one-second copy join emitted non-monotonic DTS warnings and HEVC decoding errors.

## Root cause and resolution

The command treated filename order as capture order and assumed all selected streams were copy compatible. It now orders Pixel clips by filename timestamp and iPhone MOV clips by `creation_time`; `--clips` selects exactly two files; `--reencode` normalizes the selected pair to SDR H.264/AAC, tone-mapping HLG while preserving source files. The default stream-copy path remains available for compatible clips.

## Verification and follow-up

The focused regression test failed before the fix with reversed list entries. The mixed SDR/HLG integration test failed before implementation because `--reencode` was unavailable. The final test results and short real-media probe are recorded in [the active plan](../../plans/concat-timestamped-videos.md). A full-length render and playback review remain a manual step; re-encoding discards Dolby Vision/HDR metadata.
