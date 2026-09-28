# Real-clip sample lost capture metadata

## Symptom and impact

On 2026-09-28, a 0.3-second real-media join probe stopped before encoding because the temporary `IMG_1377.MOV` sample had no `creation_time`. The full source MOV retains that metadata; neither source file was modified.

## Evidence and current status

Both `ffmpeg -c copy -t 0.3` extractions exited 0. The concat command exited 1 with `cannot read capture time for .../IMG_1377.MOV: Invalid isoformat string: ''`. The temporary extraction omitted the creation timestamp needed for capture ordering. The generated fixture integration test passed before this probe.

## Root cause, resolution, verification, and follow-up

`ffmpeg -c copy -t 0.3` did not carry the MOV container's creation timestamp into the temporary sample. The probe was rerun with `-metadata creation_time=2026-09-28T01:21:49Z`; extraction, join, and decoding each exited 0, and decoding emitted no errors. The command continues to reject `IMG_*.MOV` files without usable capture metadata, avoiding silent misordering. Preserve timestamps explicitly in future clipped-media probes.
