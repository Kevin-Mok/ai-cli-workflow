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
