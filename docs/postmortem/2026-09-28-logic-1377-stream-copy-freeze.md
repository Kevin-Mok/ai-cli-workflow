# Stream-copy join froze during IMG_1377.MOV

## Symptom and impact

On 2026-09-28, the locally produced `logic-plus-1377.mp4` plays the existing
`logic.mp4` video and then holds its final picture while audio from
`IMG_1377.MOV` continues. The original source files remain intact.

## Evidence and current status

The join list contains `logic.mp4` followed by `IMG_1377.MOV`. `ffprobe` reports
4,689.404 seconds of audio but only 4,332.412 seconds of video in the joined
file. At the boundary, video packet duration changes from roughly 0.01667
seconds to 0.000011 seconds. The source files use different video time bases:
1/90000 and 1/600. They also differ in HEVC profile, bit depth, color transfer,
and display rotation. The failed output has been preserved for comparison.

A four-second boundary sample made with separate decoded inputs and a concat
filter has 4.017 seconds of video, 4.016 seconds of audio, and decodes without
errors. The iPhone image is upright and pillarboxed. The full replacement at
`logic-1377-fixed.mp4` was rendered and verified; the two source files and
failed join remain intact.

## Root cause and resolution

FFmpeg's concat demuxer requires matching stream properties for stream copy.
The second clip's 1/600 video timestamps were interpreted against the first
clip's 1/90000 time base, compressing its roughly 357 seconds of video into
about 0.22 seconds. Copying HEVC packets across the SDR Main and HLG Main 10
streams was also unsafe. A short remux trial changed the iPhone video
time base to 1/90000 and restored roughly four seconds of container duration,
but its decoded second segment emitted HEVC reference and slice errors.
Time-base normalization alone does not make these encoded streams compatible.
The repair decodes both clips, converts the iPhone HLG video to SDR BT.709,
presents it upright inside the 3840x2160 frame, and
encodes one consistent HEVC/AAC output. This loses the iPhone HDR and Dolby
Vision metadata and re-encodes the existing 72-minute video.

## Verification and follow-up

Before the repair, `ffprobe` on `logic-plus-1377.mp4` confirmed the video/audio
duration mismatch and collapsed packet timestamps. The four-second sample was
probed, fully decoded, and visually checked at the iPhone segment. FFmpeg
completed the full render with exit 0. `python3 verify-logic-1377.py` exited 0:
expected 4,689.406 seconds, video 4,689.400 seconds, audio 4,689.410 seconds;
8-second windows around the join and at the end decoded without errors. Frames
extracted at 4,331 and 4,334 seconds show the expected switch to upright,
pillarboxed iPhone footage. Two-second audio windows before and after the cut
had mean levels of -14.9 dB and -26.2 dB, respectively. A person should still
listen to the cut in their preferred player for subjective audio quality. Keep
the originals and failed output until the new file is accepted.
