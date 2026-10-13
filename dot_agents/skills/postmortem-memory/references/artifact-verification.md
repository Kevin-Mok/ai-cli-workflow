# Artifact verification and measurement

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## ext-preexisting-truncated-suite

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: Vitest esbuild Unexpected end of file; tracked ad-redirect test ends at line 32; full verification blocked despite partial passing suites
- Applicability: Repositories with an already-truncated required regression file.
- Diagnostic checks: Inspect the complete file and baseline status before assigning ownership.; Separate a transform/collection defect from application failures.; Do not treat the remaining passing suites as a full-suite pass.
- Remedy: Repair only within authorized scope or report the baseline failure with exact partial results. If restored assertions inspect URLSearchParams, compare actual entries rather than object properties.
- Verification evidence: The later gate report records 46 tests in 20 suites passing before one failed suite; another infrastructure report describes fixes underway but no completed aggregate result for those corrections.
- Limitations: No successful final full application suite is established by these records alone; intentional RED is a separate category.
- Sources:
  - [2026-09-22-readme-gate-missing.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-22-readme-gate-missing.md) (SHA-256 `f48da0e0a70d`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-23-infrastructure-patch-failure.md](/home/example/coding/example-client-app/docs/postmortem/2026-09-23-infrastructure-patch-failure.md) (SHA-256 `bc27ed7ce2b0`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-process-memory-accounting

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: ru_maxrss reports over 1 GiB for bounded import; fresh idle Python has high inherited RSS peak; /proc/self/status VmHWM differs sharply
- Applicability: Linux benchmark processes launched through runners that retain pre-exec high-water accounting.
- Diagnostic checks: Compare ru_maxrss with /proc/self/status VmHWM in a fresh no-work interpreter.; Measure startup, import and query stages before rewriting the collector.
- Remedy: Measure the current executable's VmHWM and label the measurement source in benchmark output.
- Verification evidence: An idle interpreter reported about 1.2 GiB ru_maxrss versus about 11 MiB VmHWM; corrected 260,000-message benchmark exited 0 with 26.33 MiB peak RSS.
- Limitations: VmHWM is Linux-specific and measures current-process peak, not child/whole-system memory. Retain the measurement label.
- Sources:
  - [2026-10-04-benchmark-memory.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-benchmark-memory.md) (SHA-256 `f238bb056b66`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-xlsx-export-view-loss

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: freezeAtPosition succeeds but XLSX has no pane element; hidden Calc document loses frozen headers; in-memory view differs from exported artifact
- Applicability: Headless/hidden LibreOffice XLSX export requiring persistent frozen headers and gridline preferences.
- Diagnostic checks: Inspect worksheet sheetViews in the ZIP independently of the builder.; Reload the exported workbook in a real office runtime and inspect frozen-pane and gridline state.
- Remedy: Add standard frozen-pane and active-cell metadata after export while preserving all other archive members, formulas, styles and validation.
- Verification evidence: The missing-pane regression first failed then passed; reload confirmed hasFrozenPanes and hidden gridlines; 17 workbook checks passed.
- Limitations: Archive modification must preserve unrelated entries and be verified by real reload; passing formula checks alone does not prove view preferences.
- Sources:
  - [2026-10-05-freeze-panes-export-loss.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-05-freeze-panes-export-loss.md) (SHA-256 `68398b788f3d`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-xml-boolean-semantics

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: AssertionError requiring showGridLines="0"; export uses showGridLines="false"
- Applicability: Semantic verification of exported XML booleans.
- Diagnostic checks: Parse or normalize valid XML boolean forms rather than matching only one string.; Verify frozen row counts independently of gridline serialization.
- Remedy: Accept both valid false spellings and validate intended pane counts; change the verifier when the export is semantically correct.
- Verification evidence: Corrected archive, frozen-header, gridline, session-validation and original-hash checks passed; 20 workbook tests had passed.
- Limitations: A verifier correction is justified by XML semantics and independent state evidence, not by weakening an assertion to match any output.
- Sources:
  - [2026-10-05-final-view-check-assumption.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-05-final-view-check-assumption.md) (SHA-256 `d7ff5e5b6613`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-authored-markdown-whitespace

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: git diff --cached --check rejects postmortem trailing spaces or EOF residue
- Applicability: Locally authored Markdown incident and documentation changes.
- Diagnostic checks: Check working and staged diffs for whitespace before delivery.
- Remedy: Remove only accidental authored trailing spaces and extra final blank lines; rerun the staged check.
- Verification evidence: Both incidents record staged whitespace checks passing after whitespace-only cleanup.
- Limitations: Do not normalize immutable pinned upstream files merely to clear this check; that separate exception requires integrity evidence.
- Sources:
  - [2026-08-24-design-skills-doc-whitespace.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-24-design-skills-doc-whitespace.md) (SHA-256 `e0d83035b6bc`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-08-24-refresh-config-postmortem-whitespace.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-24-refresh-config-postmortem-whitespace.md) (SHA-256 `3aad855d8fd0`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-deployable-file-set-verification

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: installed byte comparison reports missing __pycache__ file; source/live ledger changes during verification
- Applicability: Package verification with intentionally excluded generated caches and concurrent knowledge writers
- Diagnostic checks: Inspect cache exclusions and exact deployable file sets; Compare the deployment snapshot and current source; preserve concurrent learning entries
- Remedy: Compare deployable artifacts, preserve concurrent reviewed entries, then apply the latest validated knowledge through exact owned targets.
- Verification evidence: Initial generated-cache comparison failed, and later checks identified legitimate concurrent ledger/config changes. Corrected exact verification passed all 13 deployable files, Claude directory link and installed-layout retrieval from /tmp; preserve current unrelated state and verify fresh mutation-boundary hashes.
- Limitations: Established cache exclusions cannot hide real mismatches. Concurrent source revisions require their own review; installed identity does not prove an agent loaded guidance. Do not restore stale protected snapshots.
- Sources:
  - [2026-10-05-postmortem-memory-installed-cache-check.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-installed-cache-check.md) (SHA-256 `9147933e5e04`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-doctor-provenance-baseline

- Status: **unresolved**; root-cause confidence: **supported**; verification scope: **none**.
- Symptoms: doctor invalid_source_provenance for metaprompt SOURCE.md; doctor duplicate_active_skill_slug warning
- Applicability: Existing workflow doctor audit while adding unrelated incident memory.
- Diagnostic checks: Run workflow/doctor tests and the doctor audit before implementation.; Compare exact diagnostic identities after changes and distinguish errors from warnings.
- Remedy: Preserve the unrelated skill policy/provenance; require no additional objective failures and reconcile the doctor schema/text in a separately authorized provenance task.
- Verification evidence: Baseline workflow suite passed 11 of 12, doctor unit suite passed 19, and doctor audit exited 1 with one provenance error plus one duplicate warning.
- Limitations: No provenance remedy is implemented; a green doctor test suite does not make the repository audit green. Fresh postimplementation comparison remains required.
- Sources:
  - [2026-10-05-postmortem-memory-baseline-checks.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-baseline-checks.md) (SHA-256 `0fd87f6f7b04`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-frozen-measurement-defects

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: frozen allocation summary differs from schedule; native matcher rejects FINAL heading suffix; hard failure labels mix format and authorization; held-out compiler handoff has no solver outcome
- Applicability: Already frozen benchmark artifacts with later-discovered adapter, metadata or labeling defects.
- Diagnostic checks: Use actual frozen schedule and durable ledgers for counts.; Separate observed task outcomes from unmeasured downstream stages.; Compare independent derivative aggregation without mutating frozen bytes.
- Remedy: Preserve primary scores, charges and frozen inputs; disclose each specific defect and its measurement limit. Repair schema/parser categories only in a future authorized version.
- Verification evidence: Final independent aggregates reconciled 100 attempts and 754 requests; frozen files matched; adapter limitations and zero observed eligibility effects were disclosed.
- Limitations: No held-out regrading, parser recovery or invented downstream result occurred. Reported native flags may undercount valid human-readable packages.
- Sources:
  - [2026-10-03-metaprompt-selection-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-validation.md) (SHA-256 `21607fa9f53f`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-genuine-template-incident

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: dated template-substitution failure missing from discovery; check incorrectly succeeds with skipped report
- Applicability: Incident scanners that exclude actual template artifacts
- Diagnostic checks: Compare physical report names with discovered hashes; Reproduce using a dated report about template failure
- Remedy: Classify actual template artifact names and template directories instead of excluding every filename containing template.
- Verification evidence: Each defining temporary-fixture regression failed for the expected gap, then all 24 helper tests passed after minimal fixes; corrected discovery found no additional old reports.
- Limitations: Filename heuristics still require human review of narrative candidates; exclusion is not a finding.
- Sources:
  - [2026-10-05-postmortem-memory-coverage-review.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-coverage-review.md) (SHA-256 `65b00c1d9bc4`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-immutable-upstream-whitespace-exception

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: staged whitespace fails on exact pinned upstream LICENSE
- Applicability: Frozen imported evidence with intentional retained upstream bytes.
- Diagnostic checks: Verify pin inventory/hash before classifying whitespace.; Run the same check excluding only the proven immutable file.
- Remedy: Preserve exact pinned bytes and document the narrow whitespace exception instead of trimming frozen input.
- Verification evidence: The report identifies the pinned license residue and corrected snapshot/docs link verification; original frozen evidence remained preserved.
- Limitations: This exception is not permission to skip general whitespace checks or excuse authored whitespace; pin integrity must be established.
- Sources:
  - [2026-10-04-metaprompt-session-scope.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-session-scope.md) (SHA-256 `ac02deccdb08`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-known-unrelated-vault-baseline

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: broad suite fails exact sanitized vault inventory; focused feature tests pass but daily note allowlist disagrees
- Applicability: Repository-wide suites with independently existing vault fixture drift.
- Diagnostic checks: Name the failure and compare actual fixture tree with expected allowlist.; Confirm neither path nor assertion was changed by current task.; Run focused tests separately and retain full suite output.
- Remedy: Preserve unrelated note/expectation during other tasks; reconcile fixture ownership in a separately authorized maintenance change.
- Verification evidence: Multiple full runs reproduce the same inventory failure with otherwise passing task-focused suites.
- Limitations: The broad suite remains red. Do not delete a note merely to clear an unrelated test or report a full green suite from focused checks.
- Sources:
  - [2026-08-17-pytest-module-path.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-17-pytest-module-path.md) (SHA-256 `d27a59d19b24`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-27-daily-size-broad-suite-vault-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-27-daily-size-broad-suite-vault-failure.md) (SHA-256 `22bb6bcbef55`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-28-concat-regression-vault-inventory-failure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-28-concat-regression-vault-inventory-failure.md) (SHA-256 `53e4b0037eb4`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-selection-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-validation.md) (SHA-256 `21607fa9f53f`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-replacement-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-replacement-validation.md) (SHA-256 `0e80df68a1dd`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-ledger-missing-source

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: full source coverage succeeds after a registered source is deleted; zero discovered documents but findings remain
- Applicability: Bidirectional source coverage in selected discovery roots
- Diagnostic checks: Remove a registered fixture source and rerun full check; Compare every selected-root ledger alias with discovery
- Remedy: Report missing registered aliases within selected roots; keep targeted checks scoped and read-only search available without originals.
- Verification evidence: Each defining temporary-fixture regression failed for the expected gap, then all 24 helper tests passed after minimal fixes; corrected discovery found no additional old reports.
- Limitations: A targeted check proves only one report. Root overrides intentionally do not check evidence outside those roots.
- Sources:
  - [2026-10-05-postmortem-memory-coverage-review.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-coverage-review.md) (SHA-256 `65b00c1d9bc4`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-legacy-integrity-baseline

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: four legacy SHA256 assertions fail while behavior passes; git status clean and current files match HEAD
- Applicability: Frozen provenance assertions disagreeing with committed package bytes.
- Diagnostic checks: Compare current files and assertions with HEAD.; Run the committed baseline test independently.; Distinguish behavioral preservation from provenance integrity.
- Remedy: Preserve the disputed historical hashes/package during unrelated work; conduct a separate source provenance review before reconciling either side.
- Verification evidence: Committed baseline independently reproduced identical four subtest failures; 12 behavioral tests passed.
- Limitations: Integrity remains unresolved. Matching current files to HEAD does not establish historical lineage.
- Sources:
  - [2026-10-04-metaprompt-run-legacy-integrity-check.md](/home/example/linux-config/docs/postmortem/2026-10-04-metaprompt-run-legacy-integrity-check.md) (SHA-256 `a4e22afc5d3e`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-media-sample-metadata-preservation

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: trimmed iPhone MOV probe has empty creation_time; source metadata exists but stream-copy sample loses it
- Applicability: Short real-media probes feeding capture-order logic.
- Diagnostic checks: Compare source versus temporary sample container metadata.
- Remedy: Carry the required creation timestamp explicitly when extracting the temporary sample; retain rejection of recognized camera clips without usable capture metadata.
- Verification evidence: Timestamped extraction, short join and full decode all exited 0 with no decode errors.
- Limitations: A sample extraction succeeding does not prove metadata retention. The workaround repairs the probe, not missing real-source evidence.
- Sources:
  - [2026-09-28-concat-sample-metadata-loss.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-28-concat-sample-metadata-loss.md) (SHA-256 `8f044d83e65a`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-push-policy-baseline-contract

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: test_push_policy_is_consistent_in_active_workflows fails; commit-dirty lacks exact expected policy sentence
- Applicability: Workflow-wide policy contract tested while implementing unrelated prompt features.
- Diagnostic checks: Read the named failing assertion and committed skill wording.; Confirm current task does not modify that workflow.
- Remedy: Report the exact existing failure and repair policy/test alignment only with separately authorized scope.
- Verification evidence: Two successive benchmark/migration suites attribute the same push-policy failure while all relevant prompt-focused tests pass.
- Limitations: No remedy was implemented in these reports; the finding is an unresolved baseline diagnosis, not a proven wording fix.
- Sources:
  - [2026-10-03-metaprompt-selection-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-validation.md) (SHA-256 `21607fa9f53f`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-metaprompt-replacement-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-replacement-validation.md) (SHA-256 `0e80df68a1dd`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-05-postmortem-memory-baseline-checks.md](/home/example/linux-config/docs/postmortem/2026-10-05-postmortem-memory-baseline-checks.md) (SHA-256 `0fd87f6f7b04`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-relative-fps-measurement

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: nominal 30 fps rejects retained average 29.808 fps; fixed 0.1 fps tolerance rejects close timing variation
- Applicability: Comparing nominal source FPS to measured average FPS after download.
- Diagnostic checks: Read actual rational stream rate and relative error.; Keep resolution and materially lower rate regressions.
- Remedy: Allow the demonstrated bounded 1% relative FPS variation while preserving resolution requirements and actual-rate output.
- Verification evidence: Exact case was RED then all 27 tests passed; installed command verified the retained 29.808-fps artifact with audio.
- Limitations: This is a metadata quality comparison, not full artifact integrity proof; materially lower rates remain failures.
- Sources:
  - [2026-09-19-yt-dl-fps-tolerance.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-yt-dl-fps-tolerance.md) (SHA-256 `4a1cb1922a22`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-rendered-template-copy-boundaries

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: exact-copy result includes appended punctuation or instructions; multiline template variable merges last fact with following instructions
- Applicability: Line-exact benchmark copy rules and reusable multiline templates.
- Diagnostic checks: Render adversarial multiline bindings before freezing.; Use explicit quoted/bracketed boundaries for copied spans.
- Remedy: For future fixtures delimit input spans before exact-match scoring. For the frozen run preserve results and disclose a clearly labeled equal-arm omission sensitivity only.
- Verification evidence: The derivative analyzer implemented the disclosed omission without changing primary results, charges or recommendation.
- Limitations: Primary ambiguity remains frozen; sensitivity is not a corrected observed outcome or evidence that a control lacked task ability.
- Sources:
  - [2026-10-03-metaprompt-selection-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-validation.md) (SHA-256 `21607fa9f53f`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-renderer-full-short-contract

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: i3blocks hides artist despite helper full label; screenshot shows short_text selected
- Applicability: Status renderers with distinct full and constrained-width text.
- Diagnostic checks: Inspect helper output and live structured renderer JSON, not only one output line.
- Remedy: Emit the required artist-title label in both full and short fields.
- Verification evidence: Focused RED/GREEN and 37 tests passed; fresh live JSON showed artist-title in both fields with source/installed match.
- Limitations: This preserves content in constrained text; it does not guarantee that arbitrarily long labels fit the bar.
- Sources:
  - [2026-09-24-i3blocks-spotify-artist-hidden.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-i3blocks-spotify-artist-hidden.md) (SHA-256 `06d36fb8c5c3`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-stale-preservation-baseline

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: post-push protected-file hash assertion fails after approval wait; config changed by an unidentified intervening writer
- Applicability: Preservation checks across long pauses or concurrent sessions.
- Diagnostic checks: Compare modification timing, current source/live bytes and actual commit path/blob scope.; Refresh baselines immediately before a delivery mutation after a pause.
- Remedy: Preserve current protected content, avoid restoring stale snapshots, and separately verify committed scope and current local state; do not infer writer from changed hashes.
- Verification evidence: Protected configs excluded from commit and unchanged between HEAD and parent; current source/live matched; local/upstream/remote refs matched with zero ahead/behind.
- Limitations: The exact writer was not established. A stale hash warning is not evidence that the delivered commit changed a protected file.
- Sources:
  - [2026-10-04-metaprompt-post-push-verification.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-04-metaprompt-post-push-verification.md) (SHA-256 `2cdff05044ae`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-stream-copy-compatibility-boundary

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: joined video freezes while second audio continues; audio duration exceeds video duration; video packet duration collapses at concat boundary; HEVC decode errors after time-base-only remux
- Applicability: FFmpeg concat demuxer stream copy across mismatched time bases, codec profiles, bit depth, color or rotation.
- Diagnostic checks: Compare all stream properties before copy.; Inspect audio/video durations and boundary packet timestamps.; Decode boundary/end windows and inspect representative frames.
- Remedy: Decode separate inputs, normalize rotation/frame geometry/color, tone-map HDR when needed and encode a consistent output; preserve originals and failed output until accepted.
- Verification evidence: Short boundary sample fully decoded and was visually checked; full replacement duration matched expected within milliseconds; boundary/end windows decoded and frames confirmed the segment switch.
- Limitations: Time-base remux alone still produced codec errors. Re-encoding loses HDR/Dolby Vision metadata; subjective audio cut acceptance remained manual. Window decode is not a full replacement decode.
- Sources:
  - [2026-09-28-logic-1377-stream-copy-freeze.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-28-logic-1377-stream-copy-freeze.md) (SHA-256 `d42e44190bf1`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-ods-view-namespace-preservation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: generated ODS calculates correctly but real reload reports missing frozen headings; headless conversion discards view metadata; hidden controller cannot establish freeze state; oversized inherited page header/footer clips sheet exports.
- Applicability: Generated ODS edited with ElementTree and recalculated through headless LibreOffice, requiring persistent sheet views and readable PDF previews.
- Diagnostic checks: Compare `settings.xml` with Calc-saved view IDs, positions and short-typed split modes. Retain declarations referenced only inside formula/configuration-name strings. Reload with a real controller and assert freezes before manual freeze calls. Inspect exported pages and header/footer dimensions separately from formula checks.
- Remedy: Explicitly retain `of`/`ooo` prefix declarations used in strings; preserve the valid per-workbook view map after calculation; verify `Hidden=False` in an isolated headless process; define disabled bounded page headers/footers for complete exports.
- Verification evidence: `/usr/bin/python3 scripts/verify_tracker.py --render-dir /tmp/finance-tracker-preview` exited 0: all six controllers reported freezes before manual calls, no formula errors, fixed-expense edits changed runway, and all six complete PDF/PNG previews were visually inspected. Original workbook SHA-256 remained unchanged.
- Limitations: `Hidden=True` behavior was observed in the inspected LibreOffice runtime; do not assume every UNO build behaves identically. ODS settings differ from XLSX pane XML. Preserve unrelated ZIP entries, current user view choices and calculated caches; use an isolated profile without changing global settings.
- Sources:
  - [2026-10-05-tracker-frozen-headings.md](/home/example/Documents/expenses/docs/postmortem/2026-10-05-tracker-frozen-headings.md) (SHA-256 `6a91398f4b50`; 1 alias, retained in [sources.json](../sources.json)).

## ext-xlsx-row-offset-scalar-array

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: inserted rows select the wrong latest balance; scalar array formula assignment becomes text; a missing After reading has a misleading range warning.
- Applicability: XLSX ROW-helper/INDEX lookups and Google-exported scalar array formulas edited through UNO.
- Diagnostic checks: compare actual range start with the helper index; inspect UNO's outer `{=...}` wrapper; compare typed inputs before edits and after fresh reload.
- Remedy: use `latestRow-ROW(firstReferencedCell)+1`; strip only the scalar-array wrapper before Formula assignment; name missing fields explicitly. Preserve original views and input data.
- Verification: expected RED tests became GREEN;25 real-spreadsheet tests passed, separate repaired export had no formula errors, original SHA-256 was unchanged, and all five sheetViews fragments matched. Timestamp export rounding was confined to<4microseconds; other inputs matched exactly.
- Limitations: live Google Sheets reimport remains unverified. The requested chronological-row copy is current-week only. Original strict pacing is historical and superseded for the repaired copy by ext-independent-personal-pacing.
- Source: [2026-10-06-google-sheets-budget-withheld.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-06-google-sheets-budget-withheld.md); reviewed hash/alias in sources.json.

## ext-independent-personal-pacing

- Status: **verified_fix**; confidence: **confirmed**; scope: **code**.
- Symptoms: another person's overage or valid unfinished session hides all personal suggestions.
- Applicability: shared allowance spreadsheets with per-person budgets.
- Diagnostic checks: trace personal pacing to the shared readiness guard; test missing After separately from invalid Before with missing After.
- Remedy: retain strict status separately, calculate personal estimates from valid completed data, cap by nonnegative personal entitlement and actual pool, and label unfinished usage as excluded. Unknown attribution, accounting gaps and invalid values still withhold pacing.
- Verification: RED/GREEN regression and25 tests passed; zero exported formula errors; rendered Today shows positive Pistol suggestions and Dom0.
- Limitations: live import remains unverified; current-week repaired copy only. Actual After must update ongoing usage.
- Source: [2026-10-06-personal-suggestions-blocked-by-other-overage.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-06-personal-suggestions-blocked-by-other-overage.md); reviewed hash in sources.json.

## local-duration-microsecond-conservation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Float sums change when a counted interval is partitioned by model.
- Applicability: Working-time reports and display projections using UTC datetime spans.
- Diagnostic checks: Reproduce 0.3 seconds split at 0.1; compare split and unsplit totals and exact exported units.
- Remedy: Aggregate integer elapsed microseconds before converting seconds; expose additive integer fields and keep picker totals on original intervals.
- Verification evidence: Fractional RED→GREEN regressions, native record-byte invariance, full 86-test suite and strict typing passed.
- Limitations: Decimal seconds remain convenience fields; binary float row sums can differ. Human waiting accuracy still depends on evidence.
- Sources: [2026-10-06-model-report-subsecond-conservation.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-model-report-subsecond-conservation.md) (SHA-256 `2335855b28b3`).

## local-pending-context-metadata-join

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Model evidence remains queued when SQLite creates historical timing after rollout scan.
- Applicability: Incremental adapters joining rollout contexts to stable turns supplied by another read-only timing source.
- Diagnostic checks: Fixture rollout context without lifecycle start plus SQLite thread_turns creates a turn with no attached model evidence.
- Remedy: Reconcile pending contexts after metadata refresh and on every scan, using stable session/turn IDs and idempotent timestamp evidence.
- Verification evidence: Actual SQLite fixture import/reimport passed; database bytes unchanged; full 86-test suite passed.
- Limitations: Missing or unresolvable source IDs remain Unknown; never use SQLite current settings to infer history.
- Sources: [2026-10-06-model-report-subsecond-conservation.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-model-report-subsecond-conservation.md) (SHA-256 `2335855b28b3`).

## local-uv-source-tool-reinstall

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: uv tool install --force reinstalls a cached local wheel after source-only edits under the same package version.
- Applicability: Updating a uv-installed local tool whose metadata/version stays unchanged.
- Diagnostic checks: Compare installed source/module behavior against local files; inspect uv reinstall/refresh flags.
- Remedy: Use --reinstall-package for the local tool, then verify the installed entry point and exact deployable source set.
- Verification evidence: Isolated real-uv repeated setup test RED→GREEN; real setup rebuilt package, models help and v2 schema passed, 14 installed source modules matched.
- Limitations: Cache behavior is uv-version dependent; successful package installation does not prove service backfill or live heartbeat health.
- Sources: [2026-10-06-model-report-install-cache.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-model-report-install-cache.md) (SHA-256 `fd015e631db0`).

## local-history-journal-observer-hot-path

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Embedding 268k quota snapshots grows timing ledger to 84.6 MB and burdens observer cadence.; Timing ledger read takes 4.01 seconds with stale-heartbeat and sampling-gap risk.
- Applicability: Observers repeatedly loading/saving timing state while accumulating large append-only historical telemetry.
- Diagnostic checks: Measure real history count and ledger bytes plus read, incremental scan and serialization latency.; Verify installed cadence with multiple heartbeat samples after source tests; audit migration loss and duplicates.
- Remedy: Separate validated append-only history into a journal with cached deduplication and keep history off the hot timing-ledger path. Validate legacy migration, restart, corruption refusal and cached restore behavior.
- Verification evidence: 114 tests, mypy 16 modules, Ruff/build and 60 smoke checks passed. Installed 16 modules matched; journal retained 268,207 old observations plus 6 new, 0 lost/duplicates. Steady scan .691886s and serialization .580391s; 10 heartbeat samples showed 5 distinct, maximum age 2.129663s, no live diagnostic.
- Limitations: Runtime evidence covers the measured installed workload; it does not guarantee all future load. Timing ledger remains 37.7 MB; quota is account-wide and burn comparisons remain uncertain.
- Sources:
  - [2026-10-06-burn-ledger-observation-latency.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-burn-ledger-observation-latency.md) (SHA-256 `5ff8ecec867b`; 1 alias retained in [sources.json](../sources.json)).

## local-terminal-report-readable-projection

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Burn report prints dense unaligned rows, raw epoch resets and quality flags; model mix is hard to scan.
- Applicability: Human terminal reports backed by structured accounting or diagnostic exports.
- Diagnostic checks: Inspect actual rendered output at normal and narrow widths. Distinguish display hierarchy defects from accounting defects; inspect color-free and piped output.
- Remedy: Project the same report data into a responsive summary with aligned model rows, human dates/durations, visible exclusions and progressive technical details. Keep monochrome distinction and an ASCII fallback; separate parallel streams from reset runs.
- Verification evidence: 126 tests, mypy across 16 modules, Ruff/build and 72 smoke checks passed; actual 80-column PTY inspected; installed 40-column ASCII and NO_COLOR checks passed, installed 16 modules matched source and service health was fresh.
- Limitations: Emoji width depends on terminal/font support. Runtime checks prove presentation behavior, not user aesthetic acceptance or quota-rate accuracy.
- Sources:
  - [2026-10-06-burn-terminal-readability.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-burn-terminal-readability.md) (SHA-256 `74fdcb77a95a`; 1 alias, retained in [sources.json](../sources.json)).

## local-backup-best-effort-vanished

- Symptoms: Live home backup exhausts rsync code-24 retries during LevelDB rotation
- Applicability: Opt-in live filesystem backups whose users accept disappearing source files.
- Diagnostic checks: Distinguish rsync vanished-source exit 24 from partial-transfer exit 23. Exercise both progress and direct-copy paths and verify final publication.
- Remedy: Accept live rsync exit 24 after one pass; preserve warning diagnostics and verify the copied inventory before publication. Retain fatal errors and offline strictness.
- Verification evidence: Two defining tests observed RED; all 58 backup tests passed, including fixture publication with injected code 24, warning checksums and tamper rejection. refresh-config succeeded and installed script bytes matched.
- Limitations: Runtime evidence covers installation; no complete machine backup or restored boot was performed. Live application data remains nonatomic.
- Sources:
  - [2026-10-07-backup-vanished-files.md](/home/example/linux-config/docs/postmortem/2026-10-07-backup-vanished-files.md) (SHA-256 `bef0db3a9152`; 1 alias).

## local-xlsx-owned-inputs-and-expiry

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: preservation checks count newly authored helper formulas as altered user input; exported exact deadline creates a tiny positive duration and enormous pacing; an opening-row AND evaluates an invalid prior-row INDEX.
- Applicability: formula-driven XLSX migrations preserving saved raw values and user formulas, with datetime-based pacing.
- Diagnostic checks: compare declared input ownership against expanded used-area snapshots; exercise opening-row and exact-deadline behavior after XLSX export/reload; verify consistent numerator/denominator final-day durations.
- Remedy: snapshot declared input columns, retain their formulas, reject helper collisions, and restrict export tolerance to timestamps. Guard INDEX with IF before eager logical evaluation. Treat positive residue under1e-9 days as expired, while keeping raw positive duration elsewhere for consistent proration.
- Verification evidence: all47 local unittest checks passed; builder export/reload found zero formula errors and preserved saved session inputs/formulas and original workbook hashes.
- Limitations: local LibreOffice evidence does not establish Google Sheets import. The sub0.1ms cutoff is conservative for the inspected serial rounding; it does not change stored observations. Host sandbox startup remains unresolved.
- Source: [History migration input-preservation guard](/home/example/coding/codex-usage/docs/postmortem/2026-10-07-history-input-preservation-guard.md) (SHA-256 `366444a5cf50`; reviewed alias in [sources.json](../sources.json)).

## local-sheets-scalar-latest-observation

- Status: **verified_fix**; confidence: **confirmed**; verification scope: **runtime** (local repaired export/reload).
- Symptoms: Google import selects the first completed row or zero, leaving personal shares correct but shared balances wrong and pacing withheld; a snapshot guard can reject its own normalized clock reference.
- Applicability: spreadsheet history with numeric completed-row helpers and cycle-based latest-reading selection.
- Diagnostic checks: inspect actual imported cached results before another engine recalculates; compare selected rows, shared balance and reconciliation separately from personal shares; check effective clock and normalized formula spelling independently.
- Remedy: use native scalar MAXIFS rather than implicit array arithmetic inside LOOKUP; retain explicit reconciliation on formula failure. Repair a separate snapshot and verify owned inputs, Events, reset evidence, allocation snapshots, Setup and source hash. Refuse custom display content, allowing only equivalent known simple clock references. Show effective clock and exact future-Finished warning while retaining validation.
- Verification: actual Google export cached rows7/0 and shared84/100; repaired local export/reload restored10/11 and51/91, preserved owned inputs/source hash and had zero formula errors. All51 local tests passed; normal/future warning renders were inspected.
- Limitations: native repaired Google reimport/shared editing remain pending; local checks do not establish live activation. Account timezone text does not set application clock. A downloaded snapshot excludes later online edits. No live sheet was written.
- Source: [Imported history pacing incident](/home/example/coding/codex-usage/docs/postmortem/2026-10-07-imported-history-pacing-blank.md) (SHA-256 `4edb2f5d8d82`; reviewed alias in [sources.json](../sources.json)).

## local-workbook-owned-row-formula-loss

- Status: **verified_fix**; confidence: **confirmed**; verification scope: **runtime** (local repair/export/reload).
- Symptoms: completed row shows Used3 but blank Check, counted0/blocking1 and unchanged allowance; older pasted row formulas differ from prepared calculations; migration tests depend on a mutable Drive download.
- Applicability: history workbooks where owned Check formulas govern counted usage; authoritative row order applies only under an explicit user instruction.
- Diagnostics: inspect native cached Check, counted-row/points and blocker values separately from displayed Used; compare owned formulas with prepared rows; establish chronology contract without changing dates or legacy cutoffs; use immutable test sources.
- Remedy: share Used/Check formula generators between fresh builds and snapshot repairs, restore only owned columns, and verify entered formulas/values, Events, reset evidence, allocations, Setup and source hash. Fill declared input columns rather than whole-row pastes. Under explicit row-order authority, remove cross-row time blockers while retaining same-row, future-clock, balance and reset validation. Pin migration fixtures independently of user downloads.
- Verification: actual six-session Google cache reproduced missingJ12/olderG12 exclusion; defining tests failed then passed. Separate repaired export/reload preserved inputs/source, latest10/12 and shared51/88, remaining63.67/24.33 and zero formula errors. All53 local tests passed.
- Limitations: native repaired Google reimport/shared editing remain pending. Explicit row-order authority is task-specific, not a general workaround for ambiguous overlap. Future-clock validation remains; repair is not automatic live restoration. No live sheet or source download was edited.
- Source: [New session formula-loss incident](/home/example/coding/codex-usage/docs/postmortem/2026-10-07-new-session-check-formula-missing.md) (SHA-256 `35b84027c35f`; reviewed alias in [sources.json](../sources.json)).

## local-native-sheet-clock-vs-import-engine

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Native sheet has reconciled balances but blank pacing and a clock hours behind the account timezone; LibreOffice reload turns valid Google cached MAXIFS results into unknown-function error525
- Applicability: Cross-application spreadsheet diagnosis with time-dependent eligibility and native exported formula caches.
- Diagnostics: Read native cached row checks, shared balance, reconciliation, effective clock and future-time count before another engine recalculates.; Compare the sheet clock with the account timezone and confirm any as-of override is blank.; Distinguish native application behavior from imported function parsing failures in the verification engine.
- Remedy: Correct application timezone/recalculation settings; a timezone text label cannot set the clock. For a local probe of Google bare MAXIFS imports, reparse the same function name through Calc with every argument unchanged before comparing clocks. Preserve source hash, inputs and accounting guards; do not create another formula repair when native cached accounting is valid.
- Verification: Native caches showed shared86, remaining61.67/24.33, Reconciled and two future finishes at09:42. After local function-name reparsing, the09:42:38 guard reproduced; changing only effective clock to12:42:38 restored daily9.50/3.75 and rest-of-today4.47/1.76 with balances/input values/source hash unchanged and zero formula errors.
- Limitations: The configured Google timezone was inferred from a three-hour clock difference, not read directly. Actual shared-sheet setting activation remains pending. Local Calc function reparsing is a verification adapter and does not prove an import defect in Google.
- Source: [Sheet clock incident](/home/example/coding/codex-usage/docs/postmortem/2026-10-07-sheet-clock-behind-toronto.md) (SHA-256 `ac8154fdd3d4`; reviewed alias in [sources.json](../sources.json)).

## local-dust-directory-apparent-accounting

- Status: **verified_workaround**; confidence **confirmed**; scope **runtime**.
- Symptom/applicability: Dust v1.2.6 logical totals exceed GNU du 9.4 apparent totals on Linux fixtures.
- Diagnostics: Compare allocated separately; inspect fixture directory st_size and hardlinks.
- Remedy: Document backend semantics. Dust includes directory st_size and logical hardlink names; GNU du --apparent-size --count-links omits directory metadata.
- Verification: Three 4096-byte fixture directories exactly explain a 12,288-byte logical delta; allocated totals match.
- Limits: Fixture evidence only; no atomic snapshot or upgrade guarantee.
- Source: [accounting investigation](../../../../docs/postmortem/2026-10-08-directory-sizes-accounting.md).

## local-backup-vm-stage-sidecars

- Status: **verified_fix**; confidence: **confirmed**; verification scope: **code**.
- Symptoms: disposable VM tools disk stages the backup entrypoint without its required adjacent helpers.
- Applicability: recovery launchers packaging scripts with sidecar dependencies.
- Diagnostics: inspect actual staging output against runtime imports before guest launch.
- Remedy: copy both progress and home-sync helpers beside the entrypoint; exercise real staging while mocking only external image creation.
- Verification: missing-sidecar regression observed RED, then 4 VM tests and all 67 backup tests passed.
- Limitations: guest boot and Secure Boot remain unverified.
- Source: [VM sidecar staging gap](../../../../docs/postmortem/2026-10-08-backup-vm-sidecar-staging.md).

## local-offline-apt-signed-optional-indexes

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Native APT update requests include optional binary-all indexes absent from signed Ubuntu Release metadata; strict offline import refuses them.
- Applicability: Offline package request/bundle workflows using actual APT serialization and authenticated official repository metadata.
- Diagnostic checks: Serialize native update requests rather than only handwritten fixtures. Verify same-suite InRelease with gpgv, then compare every index with its signed SHA256 inventory.
- Remedy: Normalize requests before fetching against authenticated metadata; remove only specifically optional unpublished binary-all Packages variants. Refuse every other unadvertised index and preserve package/hash verification.
- Verification evidence: Defining RED followed by20 package tests; independent native18-row plucky/security request becomes10 authenticated rows after current gpgv verification.
- Limitations: This establishes request normalization with real metadata and synthetic package/media flows, not a complete restored guest GNOME install. Repository availability must be checked freshly without changing releases or weakening authentication.
- Source: [Graphical VPS rehearsal](/home/example/coding/example-client-app/docs/postmortem/2026-10-09-graphical-vps-rehearsal.md) (SHA-256 `0371a96f2aee`; reviewed alias in [sources.json](../sources.json)).

## local-audio-fixture-marker-ordering

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: A child logs synthesis end before clip end despite waiting for the clip-ended marker; notification ordering assertions intermittently fail.
- Applicability: Concurrent subprocess fixtures publishing a completion marker before its observable log event.
- Diagnostic checks: Inspect marker/log order; inject a bounded scheduling gap after marker publication and reproduce the exact assertion.
- Remedy: Log completion before publishing the marker; preserve the behavior assertions.
- Verification evidence: A 50ms injected gap failed the existing assertion before correction and passed afterward; all 67 focused notification/speech tests passed.
- Limitations: Fixture code evidence does not prove hardware timing or live Codex activation. The separately reviewed default-sandbox workaround remains necessary.
- Source: [queued-question task verification incident](/home/example/linux-config/docs/postmortem/2026-10-09-queued-question-sandbox-startup.md).

## local-tmux-history-mouse-ownership

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Dragging in tmux highlights text without moving history like a Kitty scrollbar; Application mouse ownership prevents ordinary wheel from entering tmux history; Early pane output discarded at the default 2000-row history limit
- Applicability: tmux3.4 in Kitty; pane-owned history versus terminal-native scrollbar and mouse-aware applications.
- Diagnostics: Inspect installed version, effective mouse bindings, pane mouse_any_flag and history-limit.; Use a real attached PTY or isolated graphical display and numbered history; distinguish text drag, edge drag, ordinary wheel and modified wheel.; Confirm newly rendered earlier record numbers rather than matching text already visible before the event.
- Remedy: Preserve ordinary application wheel/selection; explicitly bind Alt+wheel to copy-mode history up/down and retain 50000 rows for new panes. tmux3.4 has no native pane scrollbar; native support first appears in3.6.
- Verification: Confirmed RED for absent app Alt-wheel override and lost earliest record, then six emacs/vi PTY tests passed. Installed Kitty on isolated Xvfb showed earlier numbered history, downward exit and INPUT hello in both shell and mouse-aware fixtures; text and edge dragging selected at scroll position0.
- Limitations: This is supported history browsing, not draggable scrollbar parity. Existing pane limits and discarded history remain; app document history is separate. Isolated graphical evidence does not prove physical shared-desktop/imwheel routing. External xclip unchanged/not retested.
- Source: [tmux scrolling diagnosis](../../../../docs/postmortem/2026-10-13-tmux-scrolling.md) (SHA-256 `8a1c8ba042b176a7612ebe0b94a68c6e1c912130bd3a9b11d10b1ae660574484`).

## local-tmux-released-selection-copy-ux

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Shift-wheel does not browse tmux history; Mouse release cancels the blue selection before keyboard copying; Ctrl-Shift-C copies no tmux text or repeat copy leaves another app clipboard value unchanged
- Applicability: Kitty0.49.2/tmux3.4 local terminal scroll/select/copy, including tmux under fish.
- Diagnostics: Use Shift SGR68/69 events and observe release-persistent selection in both key modes.; Verify real X11 clipboard text after release, then replace clipboard data and repeat copy. A buffer or unchanged clipboard alone is insufficient.; Compare the replacement Kitty key mapping fallback flags with the default; inspect actual terminal foreground group if process list is empty.; A transient copy message can suppress subsequent clipboard output even while new tmux buffers are created.
- Remedy: Bind Shift-wheel to pane history, MouseDragEnd to stop-selection, an explicit copy key to copy-selection-no-clear and Escape to cancel. Route Ctrl-Shift-C through a no-UI Kitty adapter that prefers native selection, otherwise resolves the tty foreground group and forwards a dedicated tmux key. Preserve shifted/ASCII fallback and use nonblocking pane status feedback.
- Verification: Defining RED covered Shift/release/OSC52 gaps. Fourteen PTY tests pass including second clipboard output and no-selection input. Actual Kitty/XTest copies exact released shell/app selections, restores selected text after clipboard reseeding, preserves viewport and returns via Escape. Native raw fish Kitty and fish-launched tmux copy checks pass. Independent review finds no important issue.
- Limitations: Isolated graphical display evidence, not physical desktop/imwheel acceptance. tmux3.4 native scrollbar remains absent; prior discarded history remains. Adapter detects local foreground tmux, not arbitrary remote SSH applications.
- Source: [tmux scroll/copy UX](../../../../docs/postmortem/2026-10-13-tmux-scroll-copy-ux.md) (SHA-256 `07ca32cdf9a4f8d1d57f456abe187a2e66f5b8d87640ac592d39fd2354cc88c6`).
