# Review refresh controls disappeared from the less prompt

The refresh key worked, but less interpreted punctuation in its help prompt and hid controls. Reproduce the rendered prompt, use text without less control syntax, and verify the visible controls in a real terminal.

## Symptom and impact
Independent real PTY review found the intended `r: refresh recaps | Space: scroll | /: search | q: quit` became `r scroll | / quit`. Users could not see refresh/search help correctly. Source-only change; installed CLI not changed yet.

## Evidence and status
The reviewer reproduced the issue with installed less590; unescaped colon invokes less prompt conditional syntax. CLI tests passed because they do not emulate less's prompt grammar. Status: confirmed renderer integration defect. Next steps: add a real prompt assertion to the disposable PTY smoke, observe RED, change the fixed prompt text, and verify source/installed runtime before completion.

## Lookup and diagnosis
Search `less pager prompt colon syntax` returned no applicable less finding. Reviewed the returned Bash dynamic-output scope finding and rejected it: no Bash variable assignment is involved. The installed less manual's PROMPTS section explicitly reserves question mark, colon, period, percent and backslash, with backslash for literal escaping. Its lesskey manual documents quit's extra-character exit status; independent PTY probes confirmed bat discards that status. These are separate consumer boundaries, not report-renderer errors.

## Resolution and verification
Replaced the fixed help text with punctuation-free `r refresh recaps | Space scroll | / search | q quit`. Added a real PTY assertion for visible refresh, Space and search controls; it failed RED on the original string and passed GREEN after correction. Source and installed smoke both exit 0, verify the prompt, add a session while open, press r to discover it and generate its recap after a zero preview, then Space/q exit normally. All109 session regression tests pass. The changed CLI was installed with byte/hash verification and rollback at /tmp/refresh-key-review-rollback-klom5bng. Status: verified runtime fix using disposable sources and fake inference; no real provider calls were required.

## Follow-up and learning
Treat text passed to a terminal tool's prompt option as that tool's grammar, not inert display text. Escape reserved syntax or use plain fixed text; assert the rendered controls in a real PTY rather than merely checking argv. Maintain this lesson in tracked API-contract/fixture guidance with the reviewed report hash. Runtime evidence does not establish provider availability or regenerate private live recaps.
