# API contracts and fixtures

Use these reviewed findings to compare a failure with prior evidence. Check applicability and diagnostics before choosing a remedy; keep its verification scope and limits explicit.

## ext-boundary-error-contracts

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Poll.question has no .text; args.port or default accepts explicit zero; missing context returns HTTP 500; integrity-check result ignored
- Applicability: Adapters, HTTP/CLI boundaries and persisted configuration recovery.
- Diagnostic checks: Inspect the installed library property type.; Test omitted versus explicitly invalid values separately.; Inject integrity-check failure, missing resources and invalid saved config.; Verify errors are actionable without exposing private values.
- Remedy: Match installed poll/string contracts, validate explicit ports, honor integrity failures, return JSON 404 for missing context, sanitize translated HTTP errors and preserve invalid configuration privately before offering repair.
- Verification evidence: Defining regressions failed before fixes; full wrapper passed 97 backend tests, lint and mypy; localhost verified JSON 404 and UI paths.
- Limitations: The runtime check covers localhost/synthetic data; live Discord behavior and private data were not exercised.
- Sources:
  - [2026-10-04-review-findings.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-review-findings.md) (SHA-256 `cc3fd381068a`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-calc-style-collision

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: ElementExistException; CellStyles.insertByName; workbook export stops during style definition
- Applicability: LibreOffice UNO workbook builders registering custom styles in the built-in CellStyles namespace.
- Diagnostic checks: List existing style names before insertion.; Inspect the original UNO exception at the boundary, including whether traceback conversion obscures it.
- Remedy: Prefix custom style names with a task-specific namespace; wrap UNO exceptions at the runtime boundary if contextlib conversion masks their traceback.
- Verification evidence: The builder exited 0, all 17 workbook checks passed with zero formula errors, and all three sheets were rendered and inspected.
- Limitations: The report confirms the specific built-in name collision; do not generalize a collision to every UNO exception.
- Sources:
  - [2026-10-05-calc-style-name-collision.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-05-calc-style-name-collision.md) (SHA-256 `9b1dbfd296aa`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-channel-access-onboarding

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: inaccessible channel startup error lacks invite path; optional voice warning obscures channel access problem
- Applicability: Discord bot onboarding with saved token and insufficient/unknown target channel access.
- Diagnostic checks: Separate channel ID/server installation/permissions from optional voice dependencies.; Verify invite URL scopes and minimum required permissions.; Ensure invite mode logs in without opening quota storage or Gateway.
- Remedy: Expose a login-only invite/re-authorization command and actionable startup guidance using only required scopes/permissions.
- Verification evidence: Four defining regressions passed after RED; 55 tests and Pyright passed; a real login-only invite command generated a valid invite URL and exited 0 without revealing the token.
- Limitations: The exact remote channel-access cause remained unknown. Generating a URL does not authorize or prove server installation/channel permissions.
- Sources:
  - [2026-10-02-channel-access-invite.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-channel-access-invite.md) (SHA-256 `d726eefbb45d`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-context-manager-return

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: mypy missing return inside APSW snapshot context; runtime search tests pass but return not exhaustive
- Applicability: Public Python wrappers returning from context managers whose type permits exception suppression.
- Diagnostic checks: Read __exit__ typing and account for suppression paths.; Verify transaction/snapshot lifetime and returned data.
- Remedy: Assign the result within the snapshot context and return after the context closes.
- Verification evidence: Focused mypy and Ruff passed; 27 storage/search tests passed.
- Limitations: Changing return placement must preserve snapshot consistency; it does not establish every context manager is suppression-capable.
- Sources:
  - [2026-10-04-relevance-cursor-type-check.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-relevance-cursor-type-check.md) (SHA-256 `7fe1e07ced67`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-gateway-state-typing-and-swap

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Pyright rejects shared ConnectionState concrete subclass; sync callback parameter name differs; controller construction/save failure leaves mutated scope
- Applicability: Multi-guild controllers sharing one Discord Gateway while switching SQLite-backed scope.
- Diagnostic checks: Preserve the library's Self-parameterized state ownership.; Keep callback signatures matching the public contract.; Inject failure after real scope mutation and confirm rollback plus subsequent counting.
- Remedy: Bind the shared Gateway state narrowly as ConnectionState[Self]; keep controller connection ownership explicit. Snapshot and restore SQLite state on failed construction/save, and retire the previous controller only after success.
- Verification evidence: Ninety-five tests including sixteen guild regressions passed with Pyright; independent injected-failure review verified rollback and later counting.
- Limitations: A narrow cast is justified by explicit shared connection ownership; controllers must never connect independently. Live multi-server verification was not performed.
- Sources:
  - [2026-10-02-guild-router-verification.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-guild-router-verification.md) (SHA-256 `293deda16a75`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-installed-sqlite-types

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: mypy callback signature too narrow; fetchone optional result unguarded; SQL parameters typed object
- Applicability: APSW boundaries using installed SQLiteValue/SQL scalar declarations.
- Diagnostic checks: Compare callbacks and parameter lists against installed stub contracts.; Guard or assert an optional fetchone result under the established invariant.; Run runtime collection after introducing a stub-only type.
- Remedy: Use correct scalar callback/parameter types, explicit result guards, and postponed annotations for runtime-absent declarations.
- Verification evidence: Focused mypy/Ruff and 23 storage/search tests passed.
- Limitations: A justified assertion needs a real invariant; do not use it to suppress unexpected missing rows.
- Sources:
  - [2026-10-04-storage-type-check.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-storage-type-check.md) (SHA-256 `d64256eda23d`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-intent-command-contract-drift

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: exact Gateway intent bitmask stale; registered command count expected 7/8 observed 8/9
- Applicability: Features intentionally adding ordinary Discord intents or public commands.
- Diagnostic checks: Compare the new requirement to exact existing registration and intent assertions.; Assert added command names and preserve unaffected required commands.; Verify privileged intents stay disabled when unnecessary.
- Remedy: Update explicit contract tests alongside authorized feature registration, preserving exact minimal intent/command expectations rather than dropping assertions.
- Verification evidence: Reader suite passed 136 tests with exact intents/eight-command assertions and Pyright; subsequent source-filter suite passed 142 tests with nine commands.
- Limitations: Change expected contracts only after confirming intended product requirements; a count mismatch alone does not justify updating tests.
- Sources:
  - [2026-10-03-reader-gateway-test-contracts.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-reader-gateway-test-contracts.md) (SHA-256 `f8ec5ca40ef9`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-source-command-test-contract.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-source-command-test-contract.md) (SHA-256 `312a843bcc38`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-kitty-release-encoding

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: quick Backspace deletes twice only in Codex; kitty protocol flags 7 emits raw DEL on release; legacy shell Backspace unaffected
- Applicability: Historical combination kitty 0.32.2 and Codex CLI 0.160.0 running directly without tmux/SSH.
- Diagnostic checks: Run the installed encoder at flags 0/5/7/15 and inspect press/release bytes.; Compare the Codex-requested protocol flags and parser behavior.; Require the expected evidence marker as well as intentional reproducer exit status.
- Remedy: Upgrade to a maintained kitty release containing the historical 0.33.0 fix and reopen the terminal, or test the per-launch CODEX_TUI_DISABLE_KEYBOARD_ENHANCEMENT=1 wrapper before relying on it.
- Verification evidence: Installed encoder deterministically emitted identical DEL bytes on press/release at flags 7; wrapper env/argument forwarding and actual --version launch passed.
- Limitations: Neither a terminal upgrade nor a full interactive workaround session was performed. Legacy mode may reduce modified-key distinctions; physical input, Unicode and shortcuts remain manual checks.
- Sources:
  - [2026-10-02-kitty-backspace.md](/home/example/coding/kitty-codex/docs/postmortem/2026-10-02-kitty-backspace.md) (SHA-256 `2ea8d2e3eae4`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-omit-absent-optional-argument

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: TextChannel.send rejects View | None; runtime tests pass but Pyright send signature fails
- Applicability: Library APIs where an optional argument is omitted rather than explicitly set to None.
- Diagnostic checks: Inspect the installed public signature.; Test configured and disabled branches separately.
- Remedy: Call send without view when no reader is configured; pass a concrete View only for the enabled branch.
- Verification evidence: Full 136-test suite and Pyright passed, both exit 0.
- Limitations: Do not generalize omission semantics to every optional API field; read the concrete contract.
- Sources:
  - [2026-10-03-reader-jump-view-type.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-reader-jump-view-type.md) (SHA-256 `30a5fa5f801c`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-realistic-fixture-boundaries

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Discord message has no components attribute; forwarded mention assertion fails; SequenceProxy([]) != []; incremental high_water stays zero; fixture uses removed production constant
- Applicability: Offline fixtures representing installed library objects, protocol request order or independent synthetic identities.
- Diagnostic checks: Exercise real installed message constructors with complete optional payload fields.; Use plausible library-constrained IDs and compare the public sequence contract.; Distinguish snapshot/header requests from data pages when injecting interruptions.; Avoid borrowing unrelated production constants for fixture identity.
- Remedy: Keep fixtures realistic: full-size Discord IDs, optional fields, sequence emptiness checks, interruption after the intended page, and independent synthetic account IDs. Retain behavioral assertions instead of widening production parsing.
- Verification evidence: Discord adapter focused suite passed 24 tests; sync suite passed after request-count correction; bot suites passed 30 and 143 tests after public-sequence and fixture-ID corrections.
- Limitations: Offline fixtures and tests do not establish live Discord behavior. The checksum-fixture report has no completed rerun evidence and is tracked separately.
- Sources:
  - [2026-10-04-discord-adapter-review.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-discord-adapter-review.md) (SHA-256 `5e329a29b1a3`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-review-probes.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-review-probes.md) (SHA-256 `3a811769558f`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-storage-sync-integration.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-storage-sync-integration.md) (SHA-256 `2ddef30312fe`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-02-adapter-verification.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-02-adapter-verification.md) (SHA-256 `7981990b082b`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-reader-cleanup-constant.md](/home/example/coding/twitter-cap-bot/docs/postmortem/2026-10-03-reader-cleanup-constant.md) (SHA-256 `459ecb8778ab`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-recovery-timeout-propagation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: explicit longer restore timeout still expires at manifest timer; source accessor holds old capture timeout
- Applicability: Backup restore APIs whose verified-source accessor and writer both impose deadlines.
- Diagnostic checks: Use an actual protected-file reproducer with a shorter capture bound and explicit longer restore timeout.; Inspect propagation through both local and remote CLI paths.
- Remedy: Accept and pass the explicit restore timeout to the verified-source accessor and local/remote writer.
- Verification evidence: Two real private-fixture regressions failed under the old 0.1-second manifest bound and passed after correction; final CLI 9/9, image 35/35 and full infrastructure/KVM suite passed.
- Limitations: Synthetic/blank-disk verification does not establish a completed real-host backup, bootable restoration or release upgrade.
- Sources:
  - [2026-10-04-vps-recovery-implementation.md](/home/example/coding/example-client-app/docs/postmortem/2026-10-04-vps-recovery-implementation.md) (SHA-256 `db3fcc8d0ae1`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-sha256-fixture-pending

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: shared HTTP fixture rejects sha256='abc'; integration tests fail before requests
- Applicability: Fixtures crossing a storage boundary that requires a full SHA-256 digest.
- Diagnostic checks: Hash the independent fixture bytes with hashlib.; Ensure collection reaches the intended HTTP assertions after fixture correction.
- Remedy: Replace the placeholder checksum with the actual 64-digit SHA-256 and retain storage validation.
- Verification evidence: The report records five fixture failures and the corrective procedure, but no completed rerun result.
- Limitations: Do not label this individual fixture correction verified based only on an instruction to rerun.
- Sources:
  - [2026-10-04-api-fixture.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-api-fixture.md) (SHA-256 `ebf63ddd2ee1`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-type-only-imports

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: circular import from discord.types.message; APSW SQLiteValue missing at runtime; mypy passes but pytest import collection fails
- Applicability: Python libraries whose declarations include typing-only modules or symbols; parallel modules used solely for annotations.
- Diagnostic checks: Read installed runtime source and stubs separately.; Run import/test collection after type checks, not only the type checker.
- Remedy: Put typing-only imports behind TYPE_CHECKING, use forward-reference casts and postponed annotation evaluation, and avoid runtime imports for annotation-only dependencies.
- Verification evidence: The Discord suite passed 24 focused tests with lint/mypy; APSW storage/search passed 23 tests after postponed annotations.
- Limitations: The independent unfinished-storage import report specifies the TYPE_CHECKING correction but lacks its own completed rerun; covered as an unverified case separately.
- Sources:
  - [2026-10-04-discord-adapter-review.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-discord-adapter-review.md) (SHA-256 `5e329a29b1a3`; 1 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-04-storage-type-check.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-storage-type-check.md) (SHA-256 `d64256eda23d`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-typescript-regex-target

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: regex u flag only available targeting es6 or later; Next.js compiles then TypeScript validation fails
- Applicability: Answer normalization using Unicode property escapes with an incompatible TypeScript compiler target.
- Diagnostic checks: Inspect the effective compiler target and actual language requirements.; Run production build as well as unit tests.
- Remedy: For the English-only checker in the report, use the compatible ASCII lowercase matcher; if Unicode support is required, make a deliberate target/support choice instead.
- Verification evidence: Build error and implemented replacement are documented; follow-up commands are listed without observed results.
- Limitations: The ASCII remedy does not preserve all Unicode behavior. No successful deployable build is established by this record.
- Sources:
  - [2026-08-19-unicode-regex-build.md](/home/example/coding/lucas/lucas-java-4/docs/postmortem/2026-08-19-unicode-regex-build.md) (SHA-256 `4f1975fa51c1`; 2 alias(es), all retained in [sources.json](../sources.json)).

## ext-unfinished-annotation-import

- Status: **unresolved**; root-cause confidence: **confirmed**; verification scope: **none**.
- Symptoms: adapter tests cannot collect while storage module unfinished; annotation-only Store imported at runtime
- Applicability: Parallel implementation of boundary modules with unfinished optional integration dependencies.
- Diagnostic checks: Determine whether the dependency is used at runtime or only in type annotations.; Rerun the isolated boundary suite, then the combined suite once the dependency exists.
- Remedy: Move the annotation-only import behind TYPE_CHECKING to let independent adapter tests collect.
- Verification evidence: The report records the collection failure and resolution procedure, but instructs a future rerun rather than recording success.
- Limitations: Do not remove a runtime dependency merely to bypass a collection failure; prove it is annotation-only.
- Sources:
  - [2026-10-04-integration-import.md](/home/example/coding/discord-backup/docs/postmortem/2026-10-04-integration-import.md) (SHA-256 `6975b9209434`; 1 alias(es), all retained in [sources.json](../sources.json)).

## ext-uno-collection-methods

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: AttributeError: addNew; NamedRanges; DatabaseRanges
- Applicability: LibreOffice UNO named-range and database-range collections.
- Diagnostic checks: Inspect the documented or installed collection interface.; Check each collection independently; fixing one assumed method can expose the same mistake on another.
- Remedy: Use addNewByName for these UNO collection interfaces instead of assumed addNew methods.
- Verification evidence: Builder exit 0; exported named range, dropdown reference and table filter verified; 17 workbook tests passed.
- Limitations: Applies to the named collection interfaces in this report; inspect other collection contracts separately.
- Sources:
  - [2026-10-05-named-range-api-mismatch.md](/home/example/coding/codex-usage/docs/postmortem/2026-10-05-named-range-api-mismatch.md) (SHA-256 `a7af82c2d7ca`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-absolute-installed-cli-contract

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: source entrypoint passes but installed command reports unsafe state path; chezmoi source-path relative target returns not managed
- Applicability: Installed fallback resolving a managed source repository through ChezMoi.
- Diagnostic checks: Run the installed command from a neutral directory.; Ask real chezmoi source-path for the absolute applied destination.; Make fake CLI implementations reject unexpected argv.
- Remedy: Resolve the absolute applied front-door target, then retain absolute-path, symlink, Git-root and expected-front-door validation.
- Verification evidence: Strengthened installed-layout test was RED then GREEN; 52 command/path/real-ChezMoi checks passed; installed status and dry-run succeeded from /tmp with matching source bytes.
- Limitations: Source-layout success can hide installed fallback defects. A permissive fake command returning expected output for every argument is insufficient.
- Sources:
  - [2026-07-14-installed-runtime-relative-chezmoi-path.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-07-14-installed-runtime-relative-chezmoi-path.md) (SHA-256 `7856a2cf520f`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-approved-output-contract-fixtures

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: older assertions reject requested state prefixes; playing/paused glyph tests pass but legacy labels fail
- Applicability: Changing a displayed output contract with existing fixtures.
- Diagnostic checks: Compare failed expectations to the authorized new contract.; Test dynamic text escaping and trusted small markup separately.
- Remedy: Update only expectations genuinely superseded by the authorized output change and preserve behavioral assertions; escape dynamic content before assembling trusted markup.
- Verification evidence: All 39 media tests, syntax, desktop regressions and installed comparisons passed; live paused JSON carried the raised compact span.
- Limitations: Visual centering was not re-screenshot-tested and live playing triangle was not present during final observation. Automated markup proof does not establish visual acceptance.
- Sources:
  - [2026-09-24-playback-glyph-test-expectations.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-playback-glyph-test-expectations.md) (SHA-256 `254846844ad9`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-artifact-interface-extraction-contract

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: FileExistsError escapes public ValueError contract; ambiguous prompt fences accepted; saved prompt disagrees with displayed final prompt; variadic repair passes positional tests but breaks public signature
- Applicability: Evaluation tooling exposing confined filesystem and final-artifact contracts.
- Diagnostic checks: Assert boundary exception type while preserving exclusive create.; Validate unique displayed/saved prompt identity and exact callable signature.; Validate frozen inputs before standalone report generation.
- Remedy: Translate collisions to actionable public errors without weakening atomic exclusivity; reject ambiguous/mismatched artifact presentations and compare public parameter names/kinds/defaults.
- Verification evidence: Defining regressions failed before repairs and the complete boundary/focused suites passed after them.
- Limitations: Terminal newline normalization was allowed for prompt agreement. Do not select a preferred conflicting artifact or silently reinterpret a frozen result.
- Sources:
  - [2026-10-03-metaprompt-benchmark-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-benchmark-validation.md) (SHA-256 `95a98d719b14`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-effective-tool-catalog-carriers

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: fixture MCP catalog appears missing while top-level tools is empty; Code Mode unavailable because host disabled; direct-only config fails parsing
- Applicability: Codex Responses Lite isolation harness where tools may be conveyed in developer additional_tools.
- Diagnostic checks: Inspect all known effective tool catalog carriers.; Validate dotted config serialization against actual schema.; Use a no-inference catalog/budget-gate probe before spending permits.
- Remedy: Allow only the intended fixture MCP namespace across known carriers, reject unknown carriers, count combined effective catalog and keep native Code Mode host disabled.
- Verification evidence: Correct catalog probe passed guards with zero upstream calls; synthetic actual-CLI fixture reads/writes and held-out pairs ran successfully.
- Limitations: An empty top-level array alone proves nothing. Do not enable native host tools to work around an unverified catalog problem.
- Sources:
  - [2026-10-03-metaprompt-benchmark-trial-infrastructure.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-benchmark-trial-infrastructure.md) (SHA-256 `8e4453378c36`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-external-prompt-parser-contract

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: chezmoi add receives entire conflict prompt plus EOF instead of target path
- Applicability: Refresh adoption parser consuming ChezMoi human-readable conflict output.
- Diagnostic checks: Capture the exact emitted prompt line including same-line suffix.; Assert only the target path is passed to add.
- Remedy: Extract the first whitespace-delimited field from matching conflict lines rather than trimming a guessed suffix.
- Verification evidence: Fish syntax and focused regression passed; live target adoption and retry reached REFRESH COMPLETE.
- Limitations: This parser is grounded in the reported prompt format; format drift requires a new fixture. Review adopted source diffs.
- Sources:
  - [2026-09-16-refresh-config-conflict-parser.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-16-refresh-config-conflict-parser.md) (SHA-256 `6fa4439c3222`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-external-tool-output-streams

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: download appears idle; mocked progress test passes but real transfer lacks expected stderr percentage
- Applicability: CLI wrappers separating a final machine-readable artifact path from progress.
- Diagnostic checks: Test real local external-tool transfer output channels.; Inspect flags that implicitly suppress or reroute progress.
- Remedy: Forward child progress stdout to wrapper stderr and save the final path through the external tool print-to-file contract; clean temporary reports.
- Verification evidence: Real local transfer progress checker passed after the channel correction; 25 tests passed, refresh succeeded and installed bytes matched.
- Limitations: Mocks cannot establish actual stream behavior. Already running processes retain old code until restarted.
- Sources:
  - [2026-09-19-yt-dl-progress.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-yt-dl-progress.md) (SHA-256 `68b9d00a7eec`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-fixture-mtime-after-writes

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: sparse size fixture reports current date instead of expected historical date
- Applicability: Filesystem tests asserting modification time after writing/truncating files.
- Diagnostic checks: Check operation order: writing after utime changes mtime.
- Remedy: Assign the fixture timestamp after all file writes and sparse truncation.
- Verification evidence: Six focused tests passed after reordering; broader run retained only its known unrelated vault failure.
- Limitations: A sparse fixture verifies size/date logic, not storage consumption or media contents.
- Sources:
  - [2026-09-27-daily-size-sparse-fixture-mtime.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-27-daily-size-sparse-fixture-mtime.md) (SHA-256 `a477a948aec5`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-fixture-stage-preconditions

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: merge test fails ff-only safety stage before reaching intended normal merge; fixture main and remote have one unique commit each
- Applicability: Multi-stage Git workflow tests where a safety prerequisite and intended merge behavior need independent fixtures.
- Diagnostic checks: Inspect disposable branch graph and ahead/behind counts at each helper stage.; Confirm the failure occurred at the intended boundary.
- Remedy: Establish the required fast-forward main update before constructing feature divergence; preserve the separate divergence-refusal safety test.
- Verification evidence: Disposable graph confirmed 1/1 main divergence; corrected defining test and complete 32-test suite passed.
- Limitations: Do not weaken a safety assertion to make a later-stage behavior test pass. All probes used disposable repositories.
- Sources:
  - [2026-10-05-worktree-merge-fixture-divergence.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-05-worktree-merge-fixture-divergence.md) (SHA-256 `111610a2e1bd`; 1 alias(es), all retained in [sources.json](../sources.json)).

## local-generic-artifact-order-fallback

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: concat list-only fails on prior generic output without creation_time
- Applicability: Mixed directory contents where recognized camera names require capture timestamps but older generic files remain eligible.
- Diagnostic checks: Test an existing unrelated output in the source directory.; Use explicit --clips selection for intended inputs.
- Remedy: Keep generic filenames eligible with a deterministic position after recognized timestamped files; apply capture metadata requirements only where the naming contract needs them.
- Verification evidence: New fallback and pair-selection regressions passed; real full directory list-only succeeded with 22 videos and the generic output last.
- Limitations: Do not silently accept malformed recognized camera timestamps. Source and earlier output remain unchanged.
- Sources:
  - [2026-09-28-concat-existing-output-capture-time.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-28-concat-existing-output-capture-time.md) (SHA-256 `f16d8228eb64`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-git-short-revision-arguments

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: git rev-parse --short HEAD @{upstream} says Needed a single revision
- Applicability: Read-only local/upstream SHA verification after delivery.
- Diagnostic checks: Check each command argument against rev-parse single-revision short mode.
- Remedy: Resolve HEAD and quoted upstream separately and compare their outputs.
- Verification evidence: Failed command was read-only and push/status already showed clean tracking; the report records the corrected separate invocation.
- Limitations: This command correction alone is not evidence of fresh remote equality; run both checks and remote comparison when required.
- Sources:
  - [2026-09-28-post-push-rev-parse-arguments.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-28-post-push-rev-parse-arguments.md) (SHA-256 `5a6e510f6ac4`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-media-eligibility-before-selection

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: generic browser title or empty-player placeholder hides valid Spotify fallback; no eligible player leaves stale text/cache
- Applicability: Media status helpers selecting from real tracks and generic dashboard metadata.
- Diagnostic checks: Test structured artist/title and title-only variants.; Test fallback and cache clearing when the first source becomes ineligible.
- Remedy: Apply explicit eligibility at metadata read before selection/control validation. Exclude narrowly known placeholder representations while retaining real title-only tracks and clearing state when nothing qualifies.
- Verification evidence: 29-test filter suite and later 36-test placeholder suite passed; deployed bytes matched source and live Spotify fallback rendered.
- Limitations: The title-format heuristic in the earlier report was deliberately permissive and later superseded by source identity. Placeholder state was fixture-verified, not present in final live observation.
- Sources:
  - [2026-09-19-now-playing-width.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-19-now-playing-width.md) (SHA-256 `949a5aa25daa`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-09-24-flavibot-empty-state.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-24-flavibot-empty-state.md) (SHA-256 `f3ec0efdabe3`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-native-handoff-and-safe-builtins

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: valid final Markdown artifact link triggers redundant continuation; restricted next/iter code raises NameError on StopIteration; serial fixture IO exhausts compiler allowance
- Applicability: Pre-freeze benchmark infrastructure calibration.
- Diagnostic checks: Test explicit native final-link variants and restricted standard Python exception behavior.; Measure request-level IO overhead using development trials.
- Remedy: Provide confined batch IO, recognize calibrated final Markdown links and include safe standard exception classes consistent with allowed iterators. Preserve original attempts/charges and resume only unused stages.
- Verification evidence: Defining regressions and real CLI integration passed before freeze; both development rounds stayed charged and round-two handoffs completed.
- Limitations: Later held-out em-dash/multiline heading variants remained unrecognized and downstream unmeasured. Do not apply pre-freeze fixes retroactively to frozen scored records.
- Sources:
  - [2026-10-03-metaprompt-selection-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-selection-validation.md) (SHA-256 `21607fa9f53f`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-optional-metadata-diagnostics

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: jq Cannot iterate over null; requested_formats absent from sidecar
- Applicability: Ad hoc diagnostics inspecting optional downloader metadata fields.
- Diagnostic checks: Check field presence before iteration.; Identify required top-level fields for the actual verification task.
- Remedy: Query required top-level ID/title/duration or provide a null-safe default for optional arrays.
- Verification evidence: The narrowed jq query avoids requested_formats and the integration checker does not depend on that optional field.
- Limitations: An optional inspection failure is not a failed download or proof of malformed required metadata.
- Sources:
  - [2026-09-18-yt-dl-metadata-inspection.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-09-18-yt-dl-metadata-inspection.md) (SHA-256 `a281ce69cd03`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-renamed-command-identity

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: copied helper help advertises obsolete command name; retained skill metadata test still expects old display identity
- Applicability: Copying or retaining a command/skill under a new authorized identity.
- Diagnostic checks: Assert exact public help name and discovery metadata.; Keep behavioral preservation assertions separate from identity assertions.
- Remedy: Update residual compound command strings and authorized metadata assertions while preserving behavior tests.
- Verification evidence: Installed helper help and exact-name regression passed; retained compiler suite passed 12 tests after identity-only updates with integration/helper checks also green.
- Limitations: Broad token replacement does not guarantee compound command identity. Identity migration alone is not behavior proof.
- Sources:
  - [2026-08-19-design-skills-timer-copy-rename.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-08-19-design-skills-timer-copy-rename.md) (SHA-256 `ff6f1e5780cc`; 2 alias(es), all retained in [sources.json](../sources.json)).
  - [2026-10-03-metaprompt-integration-validation.md](/home/example/linux-config/.worktrees/vps-aws-bootstrap-prompt/docs/postmortem/2026-10-03-metaprompt-integration-validation.md) (SHA-256 `21c81fbdab07`; 2 alias(es), all retained in [sources.json](../sources.json)).

## local-malformed-persistence-fixture

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: schema-drift rejection test fails during fixture setup before the loader assertion; guarded writer correctly rejects a malformed column intended as loader input.
- Applicability: Tests that must manufacture invalid persisted input to exercise a loader or migration rejection boundary.
- Diagnostic checks: Locate the first failing stack frame and check whether fixture setup reaches the intended loader assertion. Separate guarded production writes from isolated test-only invalid-input construction.
- Remedy: Construct deliberately malformed persisted input through a raw serializer in the isolated fixture, then assert that the production loader rejects it; retain the guarded writer for normal use.
- Verification evidence: The corrected schema-drift fixture reaches `Book.load` and its rejection assertion passes; `python3 -m unittest discover -s tests -p test_finance.py -v` passed all 15 tests.
- Limitations: Use a raw serializer only in disposable test fixtures designed to produce invalid persisted data. Do not weaken production writes or loader validation. Unit-test evidence does not establish LibreOffice calculation or live workbook behavior.
- Sources:
  - [2026-10-05-tracker-schema-test.md](/home/example/Documents/expenses/docs/postmortem/2026-10-05-tracker-schema-test.md) (SHA-256 `3c206245e81d`; 1 alias, retained in [sources.json](../sources.json)).

## local-validated-fixture-assignment-order

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Pydantic validate_assignment fixture fails with turn end precedes start before intended DST assertion.
- Applicability: Test fixtures changing interdependent fields on models with assignment-time cross-field validation.
- Diagnostic checks: Check validate_assignment and the first failing fixture assignment.; Evaluate intermediate field combinations against the model invariant.
- Remedy: Keep every intermediate assignment valid: clear an optional end before moving start, then set the new end, or construct a fully validated replacement. Preserve production validators and intended assertions.
- Verification evidence: Corrected DST fixture reaches elapsed-time and Unknown-mix assertions. Final frozen-tree verification: 101 pytest tests, mypy 16 modules, Ruff/build and 47 smoke checks passed.
- Limitations: This verifies fixture construction and the tested report behavior; it does not establish live service activation. Optional-field clearing applies only where the model contract allows None.
- Sources:
  - [2026-10-06-burn-dst-fixture-order.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-burn-dst-fixture-order.md) (SHA-256 `8f9b4252cb91`; 1 alias retained in [sources.json](../sources.json)).

## local-rg-windowed-match-highlighting

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: a bounded highlighted excerpt still takes seconds on a dense single-line match; a matched trailing carriage return disappears from the displayed text.
- Applicability: CLI search renderers consuming ripgrep JSON byte offsets for a clipped decoded excerpt.
- Diagnostic checks: Benchmark a warm 160,000-match synthetic line; inspect which submatches trigger UTF-8 prefix decoding. Exercise a matched trailing CR and a long Unicode prefix in a real PTY.
- Remedy: Calculate the excerpt's byte boundaries once, stop ordered submatch processing past the window and decode only window-relative slices. Remove only the added newline, preserve decoded CR, and remap offsets after escaping controls before adding ANSI.
- Verification evidence: Dense-match defining test timed out at 5s before correction; afterward 160,000 matches took 0.392s (independent review 0.354s). All 29 tests and six installed PTY/option/performance checks pass; real picker Enter/Esc preserve safe selection/cancellation.
- Limitations: This bounds highlight-offset work, not rg scanning/JSON parsing. Terminal emoji-cell widths vary by font; complete resume commands can wrap. Runtime evidence uses synthetic histories.
- Sources:
  - [2026-10-06-codex-search-output-readability.md](/home/example/linux-config/docs/postmortem/2026-10-06-codex-search-output-readability.md) (current reviewed hash retained in [sources.json](../sources.json)).

## local-codex-search-json-boundary

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: malformed payload type causes TypeError; JSON unpaired surrogate causes UnicodeEncodeError; raw cwd terminal controls; BrokenPipeError caught as OSError
- Applicability: Streaming local JSONL search caches and terminal resume commands.
- Diagnostic checks: Inject non-string discriminants and isolated surrogates next to valid records.; Exercise cwd controls and an early-closing output consumer.
- Remedy: Validate discriminant types, skip per-record encoding errors, reject non-printable resume paths, and catch/flush BrokenPipeError before OSError.
- Verification evidence: All four defining regressions observed RED then passed; complete suite 22/22 GREEN.
- Limitations: Synthetic code evidence does not establish support for every historical Codex format.
- Sources:
  - [2026-10-06-codex-search-malformed-records.md](/home/example/linux-config/docs/postmortem/2026-10-06-codex-search-malformed-records.md) (SHA-256 `5d3fefff3238`; reviewed in [sources.json](../sources.json)).

## local-fzf-ui-stream-and-resume-fixture

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: real fzf picker is invisible while selection stubs pass; real-resume fixture wrongly asserts source byte immutability
- Applicability: CLI wrappers capturing a selected row from an interactive fzf subprocess.
- Diagnostic checks: Emit stderr from a defining picker stub.; Run real fzf Escape/Enter on synthetic history and inspect real Codex /status without a prompt.
- Remedy: Capture fzf stdout only; inherit stderr for the UI. Assert source immutability for search, not for the actual resumed application lifecycle.
- Verification evidence: Stderr regression RED/GREEN; 22 tests pass; live fzf cancel/select exit 0; actual saved messages and correct UUID/cwd shown in Codex with zero token use.
- Limitations: Live checks use synthetic logs and temporary fzf, not private history or a permanently installed fzf.
- Sources:
  - [2026-10-06-codex-search-picker-ui.md](/home/example/linux-config/docs/postmortem/2026-10-06-codex-search-picker-ui.md) (SHA-256 `9646e1b4d92a`; reviewed in [sources.json](../sources.json)).

## local-terminal-color-test-environment

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Forced ANSI assertion fails when the test runner inherits NO_COLOR although product correctly suppresses color.
- Applicability: Terminal renderer tests whose output is controlled by inherited color environment variables.
- Diagnostic checks: Inspect NO_COLOR before interpreting an ANSI assertion failure. Exercise forced color and explicit no-color as independently controlled test environments.
- Remedy: Clear NO_COLOR in the color-enabled fixture; retain a separate NO_COLOR suppression test. Do not weaken production environment handling to satisfy a contaminated fixture.
- Verification evidence: The corrected fixture and separate NO_COLOR case passed in 28 focused tests and the 126-test full suite; installed NO_COLOR also suppressed explicit color requests.
- Limitations: A fixture repair does not alone prove terminal readability or live activation; those require separate rendered and installed checks.
- Sources:
  - [2026-10-06-burn-terminal-readability.md](/home/example/coding/track-codex-sessions/docs/postmortem/2026-10-06-burn-terminal-readability.md) (SHA-256 `74fdcb77a95a`; 1 alias, retained in [sources.json](../sources.json)).

## local-codex-effective-isolation-overrides

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: quoted CLI dotted MCP keys report invalid transport; empty MCP table retains inherited servers.
- Applicability: installed Codex CLI 0.160.1 isolated recap and configuration probes.
- Diagnostic checks: inspect effective config/read, hooks/list, per-server enabled flags, and every effective tool-catalog carrier.
- Remedy: use validated plain dotted MCP names, disable each server and all execution/integration features explicitly, then verify before inference. Never assume an empty table replaces inherited configuration.
- Verification evidence: strict no-inference probe exited 0; no hooks; all servers disabled. Synthetic localhost catalog contained no shell/web/MCP tools and made zero upstream requests.
- Limitations: generic Code Mode wrapper remains advertised, but its disabled host reports fail-closed. Existing bubblewrap warning is unresolved; no real generation verified here.
- Sources:
  - [2026-10-07-codex-recap-runtime-probe.md](/home/example/linux-config/docs/postmortem/2026-10-07-codex-recap-runtime-probe.md) (SHA-256 `85c19fb97675`; see [sources.json](../sources.json)).

Codex also requires a regular model instructions file and projects
`tools.update_plan` out of its typed config response. Verify that supplementary
field in the highest-priority raw layer; never replace direct effective
security checks with the arguments you passed.

## local-cache-chmod-ctime-fixture

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **code**.
- Symptoms: Cache reuse assertions fail only on ctime, with bytes, mtime and inode unchanged.
- Applicability: Private caches that call chmod while validating reusable files.
- Diagnostic checks: Compare each stat field and content; inspect permission-hardening calls.
- Remedy: Assert stable bytes, mtime and inode and required permissions for cache reuse; retain full source immutability assertions.
- Verification: Eight new index tests and 29 legacy CLI tests pass after correcting the cache-only assertion.
- Limitations: Does not permit ignoring changed source metadata or skipping permission checks.
- Source: [Recent index fixture](../../../../docs/postmortem/2026-10-07-codex-recent-index-fixture.md).

## local-dunst-stacked-script-state

- Status: **verified_workaround**; root-cause confidence: **confirmed**; verification scope: **workaround**.
- Symptoms: Dunst history recall played after a silent duplicate despite always_run_script=false
- Applicability: Dunst 1.9.2 scripts with native duplicate stacking and notification history.
- Diagnostic checks: Inspect queues_stack_duplicate transfers of script_run. Separate ordinary sounded history from a silently replaced duplicate object.
- Remedy: Preserve native stacking and global false; test/document that silently stacked replacements may sound once on later display instead of promising all history is silent or deduplicating text.
- Verification evidence: Actual private-daemon tests passed completion/approval, immediate duplicate, ordinary history and stacked-history cases with fake mpv.
- Limitations: Native state is unchanged; a previously silent stacked object can sound on history recall or restoration. Audio acceptance remains manual.
- Source: [Dunst fixture startup](/home/example/linux-config/docs/postmortem/2026-10-07-dunst-fixture-startup.md) (SHA-256 `0ecc5a5310ac`).

## local-second-brain-runtime-module-inventory

- Status: **verified_fix**; confidence: **confirmed**; verification scope: **code**.
- Symptoms: `chezmoi runtime package source is incomplete` after extracting a runtime module.
- Applicability: Second Brain Python modules installed through the timer helper.
- Diagnostics: Compare source `.py` filenames to `RUNTIME_MODULE_NAMES` and source directives in `scripts/executable_setup-second-brain-timer`; run timer installation fixtures.
- Remedy: Include the module in the explicit manifest in the same change. Keep strict inventory validation.
- Verification: Four existing installer tests failed before the addition; all 72 session tests passed afterward.
- Limitations: Synthetic installation does not establish live activation.
- Source: [Session review module manifest](/home/example/linux-config/docs/postmortem/2026-10-08-session-review-module-manifest.md).


## local-shortcut-stored-text-verification

- Status: **verified_fix**; confidence: **confirmed**; verification scope: **code**.
- Symptoms: absolute executables with arguments route as file paths; stored fish backticks gain backslashes.
- Applicability: shortcut routing and template/fish string encoding.
- Diagnostics: test absolute executable requests; compare stored `abbr --show` text in isolated fish without executing expansions. Syntax and idempotence alone can conceal changed strings.
- Remedy: multiword values are commands unless the whole value is an existing path; retain backticks without extra escaping inside fish double quotes.
- Verification: defining RED regressions preceded fixes; 19 shortcut tests, syntax and installed-file checks passed.
- Limitations: mapped commands were never executed; conditions remain host-specific and template-delimiter input has its own guard.
- Source: [Fish alias completion checks](/home/example/linux-config/docs/postmortem/2026-10-08-fish-alias-completion-checks.md).

## local-digest-provider-check-contract

- Status: **verified_fix**; confidence: **supported**; verification scope: **runtime**.
- Symptoms: Repeated `invalid_summary` classified as `invalid digest check`, with other recaps succeeding.
- Applicability: Provider schemas that permit values rejected by the local output validator.
- Diagnostics: Inspect safe field types/counts and the local error category. Compare emitted schema constraints with validation; do not log private model text.
- Remedy: Apply the existing lowercase kebab-case check-key pattern and nonblank bounded check-text contract to generation; state key rules in the prompt. Keep local validation strict.
- Verification: The inference-boundary contract test failed before repair; 80 session tests pass afterward. Installed default review exited 0 with five recaps, including the previously failing recap.
- Limitations: The exact earlier private invalid value was not retained, so its field-level cause is supported rather than independently reconstructed; unrelated model failures remain possible.
- Source: [Live session recap validation](/home/example/linux-config/docs/postmortem/2026-10-08-recent-session-review-live-check.md).

## local-picker-live-headline-integration

- Cached-fixture diagnostic: preserve ready cached states during synthetic startup. Verify opening titles and exact resume with zero inference workers; retain uncached live replacement checks separately.
- Cached-fixture evidence: startup previously overwrote ready ID1 and raced the initial assertion. Corrected real-fzf fixture and all 98 search tests pass (38.034s, exit 0).
- Additional source: [Cached fixture startup race](/home/example/linux-config/docs/postmortem/2026-10-08-title-progress-cached-fixture-race.md).

- Additional diagnostic: compare picker start and cache completion time before treating a transient generic label as a missed update.
- Additional runtime evidence: authenticated fzf state confirmed the exact reported row had its AI title after a recap completed 28 seconds from opening. No provider calls or selection changes were made during diagnosis.
- Additional source: [Guardian generation delay](/home/example/linux-config/docs/postmortem/2026-10-08-guardian-title-generation-delay.md).

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Guardian review persists after recap arrives; ready headline exists while live row keeps its fallback; static rendering passes.
- Applicability: Recent-session pickers substituting AI headlines for generic native titles.
- Diagnostic checks: Compare active rows, recap metadata and installed source. Exercise real reloads with synthetic workers. Test stable-directory and old-title-only queries separately.
- Remedy: Publish current headlines on each status update. Retain query text and track selection while matching; allow normal re-filtering and safe zero-match Enter.
- Verification evidence: Defining live replacement RED preceded correction; 93 search tests and source/installed real-fzf fixtures pass, including exact UUID resume and worker cleanup.
- Limitations: Synthetic workers make no provider calls. Already-open processes need one reopen; missing recaps retain native titles.
- Source: [Guardian titles frozen after recap](/home/example/linux-config/docs/postmortem/2026-10-08-guardian-titles-frozen-after-recap.md).

## local-descendant-exit-observation

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: owned descendant remains R immediately after group cancellation while its leader is already reaped.
- Applicability: Linux cancellation fixtures observing process-group signals.
- Diagnostic checks: confirm owned group receives SIGTERM/SIGKILL and the leader is reaped; distinguish an immediate proc-state race from a surviving child; handle disappearance around the direct read.
- Remedy: retain immediate leader absence and bound observation of the owned child disappearing or becoming Z. Fail at the deadline with its last state; leader wait cannot reap grandchildren.
- Verification evidence: focused real subprocess cancellation and all98 search tests pass with a one-second observation bound that still rejects a running child.
- Limitations: synthetic Linux subprocesses; fixture correction does not establish live provider teardown or change production wait semantics.
- Source: [Descendant exit observation race](/home/example/linux-config/docs/postmortem/2026-10-08-title-progress-descendant-exit-race.md).

## local-less-prompt-control-syntax

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: less prompt hides refresh/search labels while the key works and CLI unit tests pass.
- Applicability: custom less prompts, including bat-wrapped viewers.
- Diagnostic checks: inspect the actual rendered PTY prompt; consult the less PROMPTS grammar.
- Remedy: escape reserved prompt characters or use fixed text without question marks, colons, periods, percent signs and backslashes. Assert visible controls in a real PTY.
- Verification evidence: source and installed real bat/less fixture pass after RED prompt assertion; r discovers new work and generates a missing recap after zero preview; Space/q remain normal. All109 session tests pass.
- Limitations: disposable sources and fake inference; provider availability/live recap generation are not claimed.
- Source: [Refresh controls disappeared from less prompt](/home/example/linux-config/docs/postmortem/2026-10-08-review-refresh-less-prompt.md).

## local-fzf-serialized-reload-acknowledgement

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Priority reload restores a different UUID despite a retained query or --track.; A saved focus overrides a later visible selection.; cannot confirm updated selection after an action executed but its HTTP reply was lost.; Late restoration POST raises connection refused during normal cancellation.
- Applicability: Interactive fzf pickers that reload reordered rows and preserve a selected stable UUID, including fzf 0.44 callback contracts.
- Diagnostic checks: Exercise reordered reloads with real fzf and inspect current UUID/query plus capture, load and executed revision acknowledgements.; Deliver reload/restoration actions but deliberately lose their HTTP replies; distinguish uncertain delivery from process exit.; Select a different visible UUID after restoration and confirm Enter accepts that UUID; synchronize synthetic updates to observed selection.
- Remedy: Serialize immutable row generations. Capture UUID before reload, let the synchronous load callback publish its revision-bound restoration action without calling HTTP, and send it from the parent. Wait for an acknowledgement written by the executed fzf callback, retain active input and never replay an uncertain position action. Accept only the visible UUID and reap children after normal cancellation.
- Verification evidence: Defining real-fzf lost reload/restoration reply fixtures observed RED, then passed with exact UUID/query and cleanup. The actual source CLI passed three complete Guardian append/rename, cached-priority and newest-first repetitions. Visible-only acceptance regression passed. Final source suite passed 122 tests in 69.796s; protected refresh completed and the matching installed actual-CLI fixture passed live/cache/recent modes with exact UUID/cwd, zero added cached calls and complete child/temp cleanup.
- Limitations: Runtime evidence uses source and installed CLI with disposable sessions and synthetic inference, not provider/private history. Fixed-query identity is covered; simultaneous query edits during load-time positional restoration were not independently proved. Enter accepts the visibly supplied UUID but does not establish interleaved highlight intent. The environmental cause of short HTTP transport delay is unknown; verify supported actions against the actual fzf version.
- Source: [Codex priority refresh](/home/example/linux-config/docs/postmortem/2026-10-09-codex-priority-inspection.md) (SHA-256 `55a2a381970a`; reviewed in [sources.json](../sources.json)).

## local-picker-metadata-first-readiness

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Recent picker never reaches fzf while scanning old archives; malformed-record warnings repeatedly overwrite its terminal; another indexer holds startup behind its lock.
- Applicability: Recent-session terminal pickers whose first rows need identity metadata while text/AI evidence can arrive later.
- Diagnostic checks: Hold the archive lock on both cold and cached fixtures; delay source extraction; assert the actual listener and usable UUID rows appear before indexing finishes. Test malformed neighbors, absent source directories, pending dialogue and complete-discovery cleanup separately.
- Remedy: Read validated cached metadata without the archive lock or use bounded native headers/title tails. Mark missing dialogue explicitly pending, defer inference/manual requests until indexing, preserve seed rows through bounded background passes, and prune recap caches only after complete discovery. Send diagnostics to private disposable storage; default to concise in-UI progress/accuracy notices and bounded explicit details.
- Verification evidence: Defining startup, pending-recap, unreadable/discovery and title-budget checks observed RED then GREEN. Source and installed actual CLI/real-fzf fixtures open cold/cache/locked/malformed cases within 2s, resume exact UUID/cwd, preserve source bytes and reap children. Native installed history showed 199 usable rows in 1.968s and Escape cleaned up with summaries disabled.
- Limitations: Initial rows/activity/titles are preliminary and capped; budgets are checked between sources, so one large extraction/directory listing can exceed them after startup. Full text search and explicit rebuild retain full scans. Runtime startup checks call no provider. Inference substitution fixtures must keep native inventory, canonical cache and title metadata consistent; retry bounded GET observation, but do not replay uncertain position POSTs.
- Source: [Codex picker archive startup](/home/example/linux-config/docs/postmortem/2026-10-09-codex-picker-archive-startup.md).

## local-dunst-supported-scaled-sizing

- Status: **verified_fix**; root-cause confidence: **confirmed**; verification scope: **runtime**.
- Symptoms: Dunst ignores geometry/notification_height and popup width differs from configuration.
- Applicability: Dunst 1.9.2/X11 with automatic HiDPI scaling.
- Diagnostics: Check installed settings and startup warnings; measure actual drawn window after bounded readiness polling, including DPI and frame pixels.
- Remedy: Use width, height (maximum), origin, offset and notification_limit. Account for desktop scaling rather than treating logical width as physical pixels.
- Verification: Refresh/activation and five focused tests passed. At Xft.dpi=135, supported width 169 rendered 250x270 and width 347 rendered 501x134; removed-sizing warnings absent.
- Limits: Content controls height; fixed ratio is not guaranteed. Values depend on DPI and frame. Other legacy settings remain outside scope.
- Source: [Dunst ignored sizing](../../../../docs/postmortem/2026-10-13-dunst-ignored-sizing.md).
