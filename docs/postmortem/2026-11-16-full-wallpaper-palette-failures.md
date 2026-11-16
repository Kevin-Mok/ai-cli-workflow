# Full-library wallpaper palette failures

Use complete isolated extraction and actionable image diagnostics to fix every actual palette failure while preserving source images and proving the final readable, vivid output.

## Symptom and initial evidence

First actual full-root run:662/667pass,5fail,0collisions, source/live hashes unchanged. Report /tmp/wallpaper-all-backgrounds-2026-11-16.json retains exact image paths, commands, environment and stdout/stderr.

Three extracted backgrounds were too light for the old dark envelope: calvin-hobbes/HUJQM.png (#11820f), calvin-hobbes/f0KXF.png (#078504), root jonesy-cool.png (#079F08). calvin-hobbes/ji77X.jpeg decoded but quantization returned9/11/46colors forrequested16/35/256, so upstream16–35retrylimit could not provide16colors. Root fn-squid-game-bar.xcf produced ImageMagick EOF/not-enough-pixels errors.

## Root cause and resolution

White text cannot meet the original floor against those light composite backgrounds. Latest user preference also requires vivid, diverse editing colors: cap insufficient backgrounds to7:1white headroom through hue-preserving black mix; bodycolor7/foreground/cursor require7:1, otherroles4.5:1. Choose12distinct maximum-HLS-saturation accents using72 five-degree candidates and greedy perceptual OKLab spacing. Candidate4.55target gives roundingroom; quantized wallpaper anchor gives idempotence. Alreadydark backgrounds remainunchanged.

Valid1–15color extraction now repeats actual colors. If the original generator exhausts its retry limit despite a richer256-quantization palette, sample16real colors including endpoints; successful original generation remains unchanged. The first sparse-only fix missed this richer underquantized case; a second batch reported666/667 and the remaining case was fixed after exact9/11/46reproduction. No decoder failure becomes invented success.

Independent GIMP2.10.36 loaded the XCF and exported a visible1920x1080 composite with192209colors: ImageMagick limitation, not source corruption. Fallback runs an isolated new headless GIMP instance, merges visible layers, atomically caches a source-hash PNG, and lets actual wallpaper application use that persistent render. The original XCF hash is unchanged. Missing GIMP produces an actionable error rather than silent exclusion.

Vim's legacy strongest-three remapping collapsed some new readable lanes. A defining headless RED proved this; valid six-color palettes now retain their function/keyword/special assignments, with legacy fallback for weak palettes.

## Verification and final status

Resolved. Defining palette/low-color/normalization/vivid/72anchor/Vim REDs preceded fixes; the actual initial full batch was the XCF decoder executable RED. Focused current suite:11 palette +19verifier +1actual XCF +1i3tests and wrapper/Vim/background/live-refresh/syntax checks pass. Fresh complete report /tmp/wallpaper-all-final-parallel-2026-11-16.json:667/667passed,0failures,0collisions, all source/cache hashes unchanged, exact fresh scan coverage and matching verifier/adapter hashes. Minimum alltext4.5000657676:1; reading7.0018504426:1; HLS saturation1.0; closestpair OKLab0.0544158774. Six backgrounds normalized. Fifteen non-image/metadata files remainuntouched. Subsequent live restore of reviewed current theme exited0; original image sources remainunchanged.

## Learning and limits

Memory lookup pywal low colors light background truncated XCF returned no applicable remedy. Existing artifact verification guidance requires independent runtime evidence before diagnosing source corruption; specific quantizer/decoder/isolation lessons are recorded in tasks/lessons.md. Register final reviewed hash with no new generalized finding. Guarantees cover documented0.9sRGB composite, not arbitrary colored selections/truecolor, physical calibration or future undecodable files. New files are discovered and diagnosed on every run; no hard-coded exclusions were added.
