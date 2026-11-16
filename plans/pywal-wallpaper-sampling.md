# Sample non-editing wallpaper readability

Check a small, varied sample of previously unsuitable wallpapers using the real pywal extractor and corrected exporter. Compare before/after text contrast and rerun the existing regression tests without changing the active theme.

## Scope and assumptions

Read-only wallpaper sources under /home/kevin/Pictures/Backgrounds. Inventory found 53 bright/non-editing and 68 dim/non-editing images. Sample four from each group (eight total), not the entire collection. Use the production --saturate0.8 dark palette and 0.9-opacity sRGB source-over envelope from the original fix. Independent luminance calculation checks all 16 ANSI values plus special foreground/cursor; opaque, black-underlay and worst-case white-underlay backgrounds must each meet4.5:1. This establishes palette contrast, not subjective comfort or arbitrary application-owned colors.

## Protected state and implementation

Initial git status captured; preserve unrelated dirty files and previous commit08b8b66. Do not switch wallpaper, reload terminals, alter audio, or change user palettes. Each sample gets a disposable HOME/cache/config; invoke the readable Python adapter with -n -s -e, not the full desktop-reloading shell wrapper. Keep runner/results/logs under /tmp/pywal-wallpaper-sampling. No implementation change or new dependency planned.

## Checklist

- [x] Inventory non-editing categories and read existing tests/adapter.
- [x] Rerun deterministic regression suite and adjacent consumer checks.
- [x] Select eight representative actual image files.
- [x] Generate actual before/after palettes in isolated homes and check contrast, exports, idempotence and unchanged special background.
- [x] Inspect representative source images; distinguish numerical evidence from live visual validation.
- [x] Record exact results, limitations and reproduction commands.

## Verification and progress

Fresh tests: readable suite6 passed; wrapper passed; i3 suite1 passed; Vim background and actual Nvim live refresh passed. Logs /tmp/pywal-sampling-tests-*.log. These tests use deterministic fixtures; the sampling step adds real image-extraction evidence. Real desktop palette fingerprint captured before/after to verify isolation.

## Risks and review

Sampling cannot prove every image. Bright/busy artwork may remain distracting even with safe text contrast. Custom truecolor, colored selection backgrounds, other compositing/color-management modes and opacity below0.9 are outside coverage. Pywal extraction/backend errors must be reported separately from contrast failures. Temporary artifacts disappear when /tmp is cleared; the committed test suite remains the durable guard. No commit/push implied by this read-only follow-up.

## Sample results — 2026-11-16

All eight real-image samples passed. Each checked all18 text roles (ANSI0–15, foreground and cursor) against opaque background, 90% composition over black, and the worst-case white underlay. Every consumer export contained the corrected colors; all backgrounds and previously readable text were preserved; every cached restore was idempotent. Entire real ~/.cache/wal tree fingerprint was identical before/after sampling. Runner exited0.

Before column excludes ANSI0, which intentionally matched the background in the original palette and would make every original minimum approximately1:1. After column includes all18 text roles, so Japanese Wave's lower after minimum reflects the newly readable ANSI0, not degradation of its already-readable colors.

| Non-editing sample | Worst original ANSI1–15 contrast | Worst corrected text contrast | Slots brightened /18 | Result |
| --- | ---: | ---: | ---: | --- |
| bright/non-editing/ak-vulcan-light.png | 4.47:1 | 4.5003:1 | 2 | PASS |
| bright/non-editing/beach-2.jpg | 2.01:1 | 4.5068:1 | 18 | PASS |
| bright/non-editing/city-park.png | 2.17:1 | 4.5018:1 | 7 | PASS |
| bright/non-editing/japanese-wave.jpg | 5.47:1 | 4.5539:1 | 1 | PASS |
| dim/non-editing/astronaut-2.png | 1.82:1 | 4.5336:1 | 9 | PASS |
| dim/non-editing/blade-runner.jpg | 1.29:1 | 4.5004:1 | 14 | PASS |
| dim/non-editing/forest-fall.jpg | 1.49:1 | 4.5023:1 | 14 | PASS |
| dim/non-editing/japan-street-night.jpg | 1.39:1 | 4.5033:1 | 10 | PASS |

### Interpretation and limits

The biggest improvements came from Blade Runner, Japan Street Night, Forest Fall and Astronaut. Beach needed all18 roles brightened because its extracted teal background is brighter than the other sampled backgrounds. Japanese Wave's chromatic colors already passed; only ANSI0 required repair. Directly inspected the bright beach source and the busy, high-contrast Blade Runner scene to confirm sample variety. These source-image reads are not new live terminal screenshots. No sampled palette failed the supported contrast floor; do not infer all121 wallpapers or every application/color pair has been visually certified.

The existing automated six-test suite passed fresh. It covers near-black/saturated/upper supported backgrounds, all16 ANSI slots plus special text, actual pywal exports, safe-color preservation, generation/cache reuse, both restore spellings, idempotence, invalid-palette rejection and headless Vim background separation. Adjacent wrapper, i3(1 test), Vim background and actual Nvim live-refresh checks also passed. Tests establish numerical/export behavior; they do not judge visual comfort, font rendering, distractions or arbitrary app-owned truecolor/selection backgrounds. The new real-image sampling specifically exercises the real extractor rather than the test's stubbed extraction fixture.

### Reproduction artifacts

Temporary runner: /tmp/pywal-wallpaper-sampling/run.py (supports --plain). JSON containing full before/after palettes and independent numerical evidence: /tmp/pywal-wallpaper-sampling/results.json. Per-image generation/restore logs and exported configs are under sample-1 through sample-8. First run generated real palettes; subsequent runs may reuse those extraction caches, still validating repaired output and restore. The runner always verifies the real active cache is unchanged.

From /home/kevin/linux-config, without sudo: run `python3 /tmp/pywal-wallpaper-sampling/run.py` to repeat, inspect JSON with `python3 -m json.tool /tmp/pywal-wallpaper-sampling/results.json`, and read this report with `cat plans/pywal-wallpaper-sampling.md`. No wallpaper application is needed. Temporary artifacts are not committed. No production changes, no new tests needed, no commit/push for this follow-up; previous fix08b8b66 remains installed.

## Final review

Observed8/8 samples and all focused tests passed. No failures requiring a remedy or living incident. Source images unchanged, real palette unchanged, no GUI/audio changes. Existing unrelated dirty files preserved; only this new plan/report was added. No refresh-config needed because configuration was not changed. No recommended implementation change from this sample. Additional manual check, if desired: apply a chosen sampled image using the existing wrapper and inspect fish, Vim and AlsaMixer at normal0.9 opacity; restore the prior wallpaper afterward. That switching check was deliberately not run here.

## Delivery milestone

The user subsequently authorized commit-session. This sampling record ships with the related verifier/vivid-palette implementation in feat(pywal): verify and diversify wallpaper palettes. Its8/8 results are historical sampling evidence; current exhaustive667/667 evidence and final policy live in plans/verify-wallpaper-merge.md. No images were moved by either task.
