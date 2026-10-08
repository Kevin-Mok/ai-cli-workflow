# cto alias sandbox startup failure

The requested fish shortcut was delayed by command-runner startup failure. Scoped approved execution allows the alias workflow to proceed without changing host sandbox policy.

- Symptom/evidence: the initial read-only command exited 1 before execution with `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted`.
- Impact: no requested command or repository write ran in that failed launch.
- Lookup: searched `bwrap loopback Failed RTM_NEWADDR`; matched `local-sandbox-loopback-approved-route` and `ext-sandbox-loopback`, both verified workarounds. Exact startup diagnostic makes that guidance applicable.
- Resolution/status: approved scoped execution successfully read repository status and previewed the alias with exit 0. This verifies a workaround; the default sandbox remains unresolved.
- Root cause: runner cannot initialize its loopback interface; underlying host policy was not investigated.
- Follow-up: host sandbox repair is outside this task. Full refresh-config remains approval-blocked.
- Learning: no new reusable learning; existing approved-route guidance covers the exact symptom and limitation.

- Additional evidence: auto-review rejected broad refresh-config because it synchronizes Git/Codex and all chezmoi targets amid extensive dirty work. A separately reviewed, narrow alternative appended only `abbr cto "codex-time overview"` to the live generated fish file. `fish -n` passed; full refresh did not run.
- Inspection limitations: guessed fish function/config paths were missing; the canonical executable sync-shortcuts was read successfully. No source edits were based on those missing paths.

- Live verification initially found cto missing: regular fish startup regenerated key_abbr.fish from the installed alias input, which had not yet received the mapping. The narrow installation was completed by appending only cto to ~/aliases/key_aliases and regenerating its one live fish definition. `fish --no-config` displayed `abbr -a -- cto 'codex-time overview'`; `fish -n` exited 0. No supplied command executed.
- Final checks: all 19 fish-alias fixture tests passed; targeted ledger check passed. Full refresh remains approval-blocked; narrow live activation is verified.

## Authorized refresh follow-up

Standing rf authorization was saved. Full refresh exited 1 when adopting the intentionally changed live aliases: chezmoi detected a potential generic API key and needed an unavailable TTY. No detected value was printed or adopted. Lookup `chezmoi add template overwrite` matched exact-target captured apply and hidden-prompt guidance. Auto-review then rejected exact-target force apply because it could overwrite unrelated live content. Recovery remains blocked pending safe content comparison or explicit approval.

- Recovery verified: a private rendered/live comparison proved every alias line identical except cto placement (one definition in each). With that new evidence, review approved exact-target apply. The authorized full refresh then exited 0 and printed REFRESH COMPLETE. Fish syntax passed and the live cto expansion is `codex-time overview`. Standing authorization is recorded in the canonical append-only feedback log.
