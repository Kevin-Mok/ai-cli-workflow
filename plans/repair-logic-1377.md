# Repair the Logic and IMG_1377 join

## Purpose and observable outcome

Produce one playable MP4 containing `logic.mp4` then `IMG_1377.MOV`, with
continuous picture and audio through the transition, and document the failure.

## Context and scope

The media lives in `/mnt/usb-8tb/concerts/logic`. The canonical repository is
`/home/example/linux-config`; its initial `git status --short` was empty. The
original videos and the failed `logic-plus-1377.mp4` are protected. The tested
repair command is retained at `/mnt/usb-8tb/concerts/logic/repair-logic-1377.sh`
with a `--sample` mode; it refuses to overwrite an existing output. The repo's
concat helper already has a mixed SDR/HLG re-encode path, but its capture-time
sort would place the generic `logic.mp4` after the iPhone clip.

## Assumptions and decisions

- Order is explicit: `logic.mp4` first, `IMG_1377.MOV` second.
- Use a new output path. Keep the originals and failed output for rollback.
- Convert the iPhone HLG portrait clip to BT.709 SDR with pillarboxing.
- Use a decoded concat filter and one HEVC encode across both clips because
  stream-copy input properties are incompatible.

## Checklist and progress

- [x] Capture repo status and source/output media metadata.
- [x] Reproduce the freeze with the failed output's stream and packet timing.
- [x] Investigate source incompatibility independently.
- [x] Render, decode, and inspect a short boundary sample.
- [x] Complete a full-length repair at `logic-1377-fixed.mp4`.
- [x] Verify full duration, boundary decode, final decode, and audio activity.
- [x] Update postmortem with final evidence and review notes.

## Risks, rollback, and verification

The full 72-minute first video must be re-encoded, which takes time and may
alter visual quality. HLG and Dolby Vision metadata are discarded. The
four-second sample ended at 4.017 seconds of video and 4.016 seconds of audio,
decoded with exit 0 and no errors, and showed an upright pillarboxed iPhone
frame. The full render exited 0 and produced an 18,872,920,966-byte MP4.

`python3 verify-logic-1377.py` exited 0: expected 4,689.406 seconds; video
4,689.400 seconds; audio 4,689.410 seconds. FFmpeg decoded eight-second
windows near 4,332 seconds and the end without errors. Frames extracted at
4,331 and 4,334 seconds show the expected camera switch and upright,
pillarboxed iPhone image. Two-second audio windows on each side had mean
levels -14.9 dB and -26.2 dB. Subjective listening in a player remains an
operator check. Roll back by ignoring/removing only the new
`logic-1377-fixed.mp4`; originals remain untouched.

## Review notes

The earlier stream-copy output is a valid RED reproducer.
`python3 verify-logic-1377.py logic-plus-1377.mp4` exited 1 with
`video duration 4332.412s differs from expected 4689.406s`. The verifier is
retained beside the media and checks both stream durations plus decode at the
join and final eight seconds. FFmpeg's documented concat demuxer requires
matching stream properties. The full repair preserves
the requested order and uses a new filename, avoiding overwrite risk.
