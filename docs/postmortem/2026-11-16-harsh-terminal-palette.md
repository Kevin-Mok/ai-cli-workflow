# Harsh terminal palette

Replace the maximum-saturation policy with restrained colors while retaining measured readability and real consumer verification.

## Symptom and impact

User reports that terminal and Vim colors hurt to read. Supplied screenshots show pure red/magenta/yellow/cyan competing across syntax and tinted ordinary text. The existing generator deliberately maximizes HLS saturation and color distance; the verifier rewards those choices. A passing contrast result therefore does not establish comfortable reading.

## Evidence and current status

Investigating. Saved specification: prompts/pywal-comfortable-terminal-palette.md. Initial state and live palette retained under /tmp/pywal-comfort-evidence. Prior decoder and full-library reports are historical. Memory query `pywal vivid harsh saturation palette` returned no applicable remedy (PDF measurement finding only). An exploratory read of a guessed personal-context helper filename failed; actual helper discovery replaces that guess.

## Next steps

Define comfort regressions, replace generator/verifier policy coherently, run fresh full-library checks and inspect actual consumers. Preserve sources and rollback copies. Numerical comfort limits are design judgment, not medical guarantees.

Operational evidence: a live `fish -c` read triggered normal startup hooks, which attempted writes to fnm runtime, universal variables and aliases outside the sandbox. Those writes were denied; the requested highlight values were still returned (normal, blue, cyan, brred). Use `fish --no-config` for isolated checks and normal permission escalation for authorized live activation. No success is inferred from denied startup writes.

First GREEN run: verifier 19/19 passed; readable suite exposed three leftover vivid-policy distance assertions (.04/.08) in sparse/screenshot fixtures. Those contradicted the settled .02 paired-shade policy, so they now use the same defining comfort assertion (chroma, lightness, uniqueness and paired brights remain tested). A log-tail inspection also used an invalid multi-file tail option; it changed no files.

Fresh full-library attempt was interrupted with exit 143 after 396/667 began; no final JSON exists. Retain full-library.log as partial evidence only. Prior interrupted-batch incident documents the same unknown SIGTERM; four-worker scheduling alone does not prevent it in this session. Next attempt uses a continuously polled exec process with normal escalation, while avoiding live palette activation until source/cache fingerprints complete. Full refresh again stops at the pre-existing duplicate MIME targets (`dot_config/mimeapps.list` and `dot_config/private_mimeapps.list`); no unrelated target is removed. Kitty's configured socket base `/tmp/kitty` is PID-suffixed in running instances, so a direct base-socket probe failed; disposable preview uses an explicit known socket. One optional guessed Nord source URL returned 404; published Nord design documentation and the actual Kanagawa source remain the references.

## Resolution and fresh verification

Resolved policy and scoped activation. Defining RED preceded implementation. All32focused regressions pass. Final fresh four-worker run process64970 exited0:667/667images pass,0failures/collisions, exact fresh coverage and source/live-cache fingerprints unchanged. Minimum text4.5000616806:1, reading7.1529518891:1, maximum chroma.0865180103, closest accent pair.0322270627. Source/report software hashes match. Thirteen backgrounds normalized; current #050412 preserved. Full raw report and partial interruption log remain under /tmp/pywal-comfort-evidence. Interrupted execution cause remains unknown; a complete rerun establishes coverage, not a root-cause fix forSIGTERM.

Installed scripts matched HEAD before replacement; backups of both scripts and complete cache are in /tmp/pywal-comfort-evidence/rollback, with executable restore.sh. Scoped current-theme restore exited0 and matched reviewed proposed JSON;15running Kitty sockets updated. Actual Vim highlight query confirms neutral Normal#D8DADF, sage String#99BA82, gold Type#CCA86F, blue Function#82B3E2, lavender Keyword#B8A1DB and gray Comment#A4A6AB, all on unchanged#050412. Real after screenshots show restrained hierarchy without the previous pure red/magenta competition. Opacity remains0.9; fonts unchanged. Full refresh remains separately blocked by unrelated duplicate MIME targets.

## Learning and limitations

The local lesson is to avoid conflating contrast or maximum color distance with comfort; numerical bounds are design judgment informed by primary theme sources. Existing runtime/artifact isolation and incomplete-run learning applies; no additional generalized memory finding. Subjective comfort still needs user feedback. Colored selections, lower opacity, physical calibration and application truecolor are outside guarantees. Rollback and raw evidence under /tmp are temporary.

Final evidence review: all previously pending library/activation/rendering claims verified. The terminal-after screenshot includes a mistyped concatenated `shortclear` automation command before successful listing output; this is input-automation noise, not a palette defect. The separate fresh-window-after.png contains the clean successful lsd rendering. Disposable terminals were closed and original window focus restored. Rollback was syntax-checked but deliberately not executed because doing so would undo the requested activation.
