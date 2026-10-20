# Orientation fixture GTK initialization

The first orientation test could not obtain the GTK sink widget. Initialize GTK before creating a video Card, then repeat the pixel reproducer.

- Symptom: eight fixture subtests failed before pixel assertions because gtksink.widget was None.
- Impact: no production change or original-media write; initial run did not establish RED.
- Evidence: Xvfb orientation suite exited 1 in Card.widget.connect; fixture created Card before any GTK window or init_check.
- Cause: test setup omitted GTK initialization; existing runtime tests create a window first.
- Resolution: initialize GTK explicitly in fixture setUpClass.
- Current status: verification pending; rerun defining pixel tests.
- Follow-up: preserve explicit initialization in new GTK fixtures.
- Other exploratory probes: guessed test filename was absent; unsupported `lookup --help` was replaced with the documented `search` command. These did not mutate state.

## Rotation fixture metadata

After scoped escalation enabled X11, filters still saw no orientation tags. FFprobe confirmed the FFmpeg6.1.1 remux with `-metadata:s:v:0 rotate=90` produced no display matrix. The initial pixel mismatches therefore did not yet prove metadata handling. Use input `-display_rotation` with `-noautorotate` during copy and assert the resulting display matrix before pixel tests. Production filter design is unchanged; repeat RED against the baseline renderer with validated fixtures before accepting GREEN.

## Verified fixture resolution

The corrected FFmpeg command emitted a 90-degree display matrix and GStreamer delivered image-orientation=rotate-270 (opposite sign conventions). A diagnostic pad trace confirmed the automatic filter consumed it and reset the downstream tag to rotate-0 before additional correction. Fresh import of the baseline renderer from HEAD failed all six rotated-metadata pixel cases with verified matrices. The current renderer passed the seven-test focused suite, including saved correction and review controls; this proves the fixture remedy and renderer behavior on synthetic files. No known troublesome personal clip was identified. Broader verification belongs to the orientation ExecPlan.

Status: verified fixture repair, scoped X11 workaround. Limits: Xvfb lacks DRI2; synthetic colors establish pixel rotation but do not identify personal footage content. Explicit Gtk.init_check remains necessary and requires the scoped X11 execution route in this environment.

## Final verification route

The expanded screensaver suite passed54tests under scoped Xvfb (24.565s); browser and display regressions exited0. The final black-letterbox pixel assertion landed while that suite was running, so its metadata matrix was rerun separately and passed. The first focused rerun omitted PYTHONPATH=tests and failed test-module import before execution; adding the existing tests directory to Python's import path repaired only the invocation. This adds no independent production finding. Installed chooser/select/save/reopen/reset/cleanup passed using temporary private records; two sampled original hashes remained unchanged. The task plan records the personal-library visual evidence and native-desktop smoothness limitation without media paths or pixels.
