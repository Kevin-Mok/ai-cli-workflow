# Fish inspection triggered startup writes

A read-only concat installation inspection invoked Fish with its normal startup configuration. Use a shell without startup configuration for future inspections and preserve existing configuration work.

- Symptom: `fish -c 'functions refresh-config; functions sync-shortcuts'` exited 1. Fish startup attempted fnm multishell links under `/run/user/1000/fnm_multishells`, universal-variable writes, and shortcut generation at `/home/kevin/aliases/.key_aliases`; the sandbox reported read-only filesystem errors.
- Impact: the inspection printed the refresh helper but also ran unrelated startup hooks. No successful home-directory writes were observed. The concat implementation and original concert files were unaffected.
- Lookup: query `fish startup read-only fnm universal variables aliases write` was noisy; the existing October 23 Fish-inspection report directly matched all three startup-write symptoms. `local-fish-function-inspection` and `local-discover-paths-before-reads` also support inspecting known sources in isolation. This applies to inspection, not successful live activation.
- Resolution: `fish --no-config -c 'source dot_config/fish/functions/refresh-config.fish; functions refresh-config'` exited 0 and printed only the requested function, without the startup warnings. Normal startup was not retried.
- Status: inspection resolved; live refresh remains a separate activation step.
- Learning: no new reusable learning; the existing October 23 report and reviewed inspection-isolation guidance already cover the failure. Register this report with that explicit decision.
- Next steps: continue isolated concat verification; use no-config shells for inspection.

## Scoped refresh follow-up

The first no-config refresh attempt scoped `chezmoi apply` to the concat helper and sourced the refresh function, but omitted its `cli-message` dependency. It exited 127 with `cli-message: command not found`; its apply/shortcut steps still ran. Lookup `fish no-config cli-message dependency source` returned path-discovery guidance; source inspection established the concrete dependency. The corrected no-config invocation explicitly sourced `/home/kevin/.config/fish/functions/cli-message.fish`, retained the single-script target restriction, and ran refresh-config to exit 0 with `REFRESH COMPLETE`. The installed CLI's `--help` confirmed the new flags. General startup was never retried. No new learning beyond explicit dependency/isolation guidance; record the updated reviewed hash.
