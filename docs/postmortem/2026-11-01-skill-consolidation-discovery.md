# Refresh helper source discovery

Locate the actual Fish function before inspecting or running refresh-config during skill consolidation.

- Symptom: a source lookup used scripts/executable_refresh-config, which does not exist; rg printed an IO error. No apply or configuration change ran.
- Impact: read-only discovery needed correction; no user files changed.
- Lookup: the tracked rebase-permission incident and execution-environment guidance distinguish environment failures from repository defects; neither explains a missing source filename. The failure directly identifies a nonexistent assumed path.
- Cause and resolution: refresh-config is dot_config/fish/functions/refresh-config.fish, not a scripts executable. A successful read confirmed its preserve-local, chezmoi apply and shortcut reload behavior.
- Verification: the actual function was read successfully before activation; this establishes source discovery only, not successful config refresh.
- Status: resolved discovery mistake. Next: inspect live helper and managed-file drift before running it.
- Learning: no new general rule; existing search-before-assuming-path guidance applies. Register this exact report hash with an explicit no-new-learning decision.

## Fish startup permissions

A later `fish -c` read-only helper inspection loaded normal startup hooks, which attempted fnm multishell, universal-variable and shortcut writes outside the sandbox and emitted read-only filesystem errors. The Fish source itself loaded; refresh-config was not invoked. Existing execution-environment guidance distinguishes restricted startup from application failure. Use Fish `--no-config` for inspection, and scoped approved permissions for the required real refresh. This is a command-environment correction, not a product change; refresh-config subsequently completed through approved scoped permissions (exit0), and the installed frontend matches source. The unchanged retired installed skill was hash-verified and removed separately; existing chat context requires a new session.

## Consolidation validation checkpoint

The first GREEN attempt reported four contract failures: deletion left an empty package directory, the edited lean-instructions admission cost needed refreshing, a routing test still matched the old scope label, and an inherited merge test searched only main first-parent history although PR3 is now a merged second-parent branch. Inventory and routing already passed (236 sources/zero drift;46/51). Remove only the empty retired directory, remeasure the edited record, align the scope label, and check the original exact plain-merge parents anywhere in reachable history. No routing labels or prior correct cases are weakened. Focused rerun passed:40 tests/210 subtests; inventory236/zero drift and routing46/51 passed before targeted installed cleanup.

## Post-refresh inventory verification

The exact staged candidate passed the trim budget (14313B,28skills), routing46/51 and README gates. Broader validation then found six installed-catalog drifts after refresh installed the already-admitted skills, one calibration privacy test rejecting home shorthand in the cleanup note, and one old exact14399B/29-skill assertion. Reconcile only the six public installed descriptions against their admitted source descriptions, use logical source labels in calibration, and update the exact consolidation count/budget assertion. No admissions or routing labels change. Fresh verification passed:88 tests/226 subtests, all four CLI gates and staged size guard exit0.

## Delivery checks

A restaging command included already-staged deleted paths; git add rejected the absent pathspec before updating the index. Retain those staged deletions and restage only existing scoped files. The staged file-size guard also rejected bounded growth in five already-grandfathered documentation/ledger files. Preserve its default limit, existing skip rules and installed hook; refresh only the five exact finite ceilings to the reviewed staged sizes required by this task. No wildcard exemption or hook bypass. A reviewer reconstruction probe initially mishandled a quoted YAML name; using the production loader normalization then reproduced every frozen baseline field. No product change was required for that probe. Final source review found no blockers; file-size guard passes, existing hooks remain enabled. Commit/push privacy check is next.

The compact mirror attempt omitted description metadata required by existing overlap tests (five subtest failures). Restore each full public description and description_basis, compact only formatting, retain equality assertions, and bound the calibration record with its exact114123B ceiling. Final rerun passed:88 tests/226 subtests; inventory241/zero drift; routing46/51; trim14313B/28skills; README pass_no_change.
