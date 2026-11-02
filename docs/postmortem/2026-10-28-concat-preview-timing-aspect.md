# Joined clip previews and display aspect corrections

Independent review found two defects in the new landscape concat path before delivery. Match previews to actual output timestamps and preserve display aspect before converting to square pixels.

## Symptom and impact

The short real-source sample report sampled its second clip at 0.350s, but the joined file's second segment starts at 0.371029s. Its earlier sample matched the prior segment's last frame. Separately, fitting coded dimensions then forcing square pixels squeezes anamorphic inputs. Both could make the review misleading even while output dimensions pass.

## Evidence and current status

- Reviewer probed output frame timestamps: previous-segment frames at 0.337695/0.354362s, next encoded segment keyframe at 0.371029s. The 0.350000s sample RGB hash matched report `002.png`; the actual 0.371029s sample differed.
- The initial 10fps test masked the AAC-related 21ms shift. The fixture is being raised to 60fps and segments now have distinct colors.
- Scale currently uses coded dimensions and calls `setsar=1` afterward. A SAR 2 fixture displaying square should fit 54x54 within a 96x54 canvas, rather than using the coded 1:2 ratio.
- Lookup: `concat AAC start_time timestamps aspect ratio` returned `local-stream-copy-compatibility-boundary`. Its normalize/verify-boundaries guidance applies; it does not itself establish the AAC preview offset correction. Reviewer packet/frame evidence and defining pixel tests establish the present causes.
- Status: fixed in the initial landscape mode before delivery; no full concert render had been run and originals are unchanged.

## Next steps

The distinct-color 60fps fixture reproduced a prior-segment preview; the SAR 2 fixture reproduced black padding at a pixel that should contain the square picture. Both failed RED before fixes. Previews now add the actual joined video stream start time and seek in absolute timestamp mode. Landscape fitting converts display aspect to square pixels before scaling/padding.

Verification: `python3 -m unittest discover -s tests -p test_concat_timestamped_videos.py -v` passed all 14 tests after the final three-distinct-color fixture. A new short real-source result `/tmp/concat-concert-check-6uemi5nv/joined-fixed.mp4` encoded and decoded with exit 0; both resulting start images were visually inspected and show different, upright iPhone/Pixel scenes. Follow-up resumability/audio work must retain these checks. Full-length playback and later in-clip rotations remain unverified.

## Resume publication follow-up

Independent review of the added resumable mode found two interruption windows: a validated clip was renamed into its final cache name before its fingerprint was persisted, and the review directory was created before its ownership flag was persisted. A crash between each pair of operations would make the identical retry refuse its own valid work. Source/output safety was preserved, but resumability was incomplete.

Lookup `manifest publish before rename resume crash intent` returned no directly applicable finding; unrelated command-handle/pause-intent guidance was not used as a remedy. Two filesystem fault-injection cases reproduced the exact windows RED. The fixes persist validated clip identity and review ownership intent before publication/directory creation. All 19 focused tests passed in 39.940s; a narrow independent review verified both corrected orderings and fault tests. Both real camera-direction samples passed, then the installed helper reused both completed sample jobs to exit 0. The full render started only afterward as `olivia-rodrigo-concat-20261028212506.service`; its completed-output acceptance remains pending.
