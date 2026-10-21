# Volume test discovery

An inspection attempted to read a guessed test filename; no runtime configuration was affected.

- Symptom/evidence: `cat tests/test_i3blocks_spotify.py` reported no such file.
- Impact: inspection command exited 1; no files changed by that command.
- Lookup: searched `missing test file`; `local-discover-paths-before-reads` applies because the filename was guessed.
- Resolution: use the search agent inventory, which confirms no volume-specific test exists; add a focused volume regression test.
- Status: resolved inspection error. No new learning beyond the existing path-discovery finding.
- Verification: inspected the actual volume script and identified its shared click dispatch.
- Additional probe limitation: sandboxed Fish startup could not write its runtime aliases/universal variables, and amixer could not attach to the host mixer. Use an authorized host probe and configuration-free Fish for refresh; these diagnostics do not establish a mixer defect.
- Refresh invocation: `fish --no-config -c refresh-config` exited 127 because this function is loaded by normal Fish startup. Next use the normal host Fish environment; no configuration was applied by this attempt.
- Final verification: normal host Fish refresh completed successfully; migration-preserved volume script was installed explicitly. Real mixer checks confirmed off/off/on/on for buttons 3/3/1/1, returning to its original unmuted state. Regression and Bash syntax checks passed.
