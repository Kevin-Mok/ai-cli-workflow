# i3 music helper discovery used a nonexistent script path

The lookup assumed refresh-config was a script. The existing fish function
already supplies the implementation; no runtime configuration was affected.

- Symptom/evidence: `rg` reported `scripts/executable_refresh-config` missing.
- Impact: One diagnostic lookup failed; no application behavior or data changed.
- Status/root cause: Resolved discovery mistake; refresh-config is located at
  `dot_config/fish/functions/refresh-config.fish` and was successfully read.
- Resolution/verification: Read the actual function and its apply/sync/source steps.
- Lookup: Prior i3blocks findings concerned rendering and parser behavior, not
  helper discovery. No prior remedy was applied to this failed path lookup.
- Follow-up/learning: No new reusable learning beyond existing repository mapping
  guidance; use the confirmed function for activation.

## Test fixture arithmetic during the same task

The first GREEN run found three incorrect fixture expectations, not production
failures: the fixed blocks total 310 px plus 75 px separators; at workspace
1440 only 167 px remain, while the 25-character smaller song requires 175 px.
At workspace 1580 the 27 px song budget cannot fit the 28 px icon/ellipsis
minimum. Trimming a trailing space can leave up to 13 px unused. Correct the
fixtures from these independent sums and rerun focused/regression checks.
Status: resolved; all 19 focused tests passed after independent fixture corrections. No reusable learning beyond
existing independent expected-value calculation guidance.

## Existing unrelated whitespace

Final global diff checking returned exit 2 for an existing blank line at EOF in
`dot_agents/skills/postmortem-memory/references/api-contracts-fixtures.md:726`.
The file was already dirty before this task and was not edited here. Preserve
it; use a scoped whitespace check for the delivered changes. No new reusable
learning beyond preserving unrelated work. This warning remains outstanding.
