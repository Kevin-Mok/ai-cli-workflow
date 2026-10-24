# Browser integrations and reference investigation

Use these reviewed incidents to distinguish application state defects from provider and tooling limits. Reproduce the relevant boundary and preserve the stated evidence scope before adopting a remedy.

## ext-browser-sdk-acknowledgements

- Status: verified_fix
- Confidence: confirmed
- Verification scope: code
- Symptoms: Early SDK audio samples erase saved preferences; delayed PLAYING overwrites paused intent; READY arrives before the factory handle.
- Applicability: Browser media adapters using asynchronous iframe SDK setters and sampled state.
- Diagnostics: Reproduce stale samples before setter acknowledgement, event-before-handle ordering, and delayed PLAYING after explicit pause.
- Remedy: Keep desired state separate from observed state; retain pending audio targets until acknowledged; record applied quality only after sending it through a ready handle; never let late PLAYING erase explicit paused intent.
- Verification: Defining regressions failed before correction; final 128 unit/integration and 18 static-browser tests passed with typecheck/build. Real initial volume drift was observed independently.
- Limitations: Native event causes remain ambiguous. Deterministic tests do not establish real Twitch moving video or audible output; pending settings may require an explicit user retry.
- Source: [2026-10-22-interface-validation.md](/home/kevin/coding/viewington-alt/docs/postmortem/2026-10-22-interface-validation.md); reviewed hash retained in sources.json.

## ext-browser-transfer-privacy-gates

- Status: verified_fix
- Confidence: confirmed
- Verification scope: code
- Symptoms: A validated import releases a corrupt-storage write gate; generated public shares copy unrelated page query parameters.
- Applicability: Browser-local apps with protected storage recovery and self-contained public sharing.
- Diagnostics: Import a valid profile over malformed stored bytes and compare the exact bytes.; Generate a share link while a synthetic private query parameter is present.
- Remedy: Keep the persistence gate until a separate explicit recovery action, even after successful imports. Construct shared URLs only from origin/path and the bounded public payload; omit unrelated query data.
- Verification: Both regressions reproduced before correction; the final 128 unit/integration and 18 browser checks passed. Synthetic values only; no private token was used.
- Limitations: A validated payload does not imply consent to overwrite old data. This verifies the tested app boundary, not arbitrary third-party sharing or browser extensions.
- Source: [2026-10-22-interface-validation.md](/home/kevin/coding/viewington-alt/docs/postmortem/2026-10-22-interface-validation.md); reviewed hash retained in sources.json.

## ext-rea-bounded-bundle-analysis

- Status: verified_workaround
- Confidence: confirmed
- Verification scope: workaround
- Symptoms: REA full-site bundle analysis exhausts the Node heap; ASAR extraction fails on missing unpacked companions.
- Applicability: REA 6.7.0 investigation of large web bundles and Electron resources extracted from an installer.
- Diagnostics: Keep passive capture evidence distinct from a failed analyzer result.; Identify the installer format and retain ASAR unpacked companions before analysis.
- Remedy: Use documented bounded app-specific chunk analysis after whole-site exhaustion. Extract required unpacked resources from the same verified installer alongside app.asar before retrying extraction.
- Verification: Bounded web analysis, complete ASAR extraction and selected desktop main/preload analysis returned exit 0 with retained REA evidence IDs.
- Limitations: Full-site/source-map analysis remained incomplete. Selected static resources do not establish Windows runtime behavior. Do not raise resource limits blindly or execute unknown installers for inspection.
- Source: [2026-10-22-reference-tool-contracts.md](/home/kevin/coding/viewington-alt/docs/postmortem/2026-10-22-reference-tool-contracts.md); reviewed hash retained in sources.json.

## ext-twitch-playback-evidence

- Status: unresolved
- Confidence: hypothesis
- Verification scope: runtime
- Symptoms: Twitch embed reports ONLINE and qualities while showing Play preview; style visibility warning despite parent geometry and IntersectionObserver visibility.
- Applicability: Real Twitch integration checks in isolated HeadlessChrome using the supported player SDK.
- Diagnostics: Compare an app player with a bare official SDK embed in the same browser.; Measure current time and frame statistics across an interval; inspect PLAYING separately from ONLINE; verify actual visibility events before claiming background-tab behavior.
- Remedy: No verified remedy. Repeat in a normal visible desktop browser and record advancing frames and human audibility separately before changing application policy or declaring success.
- Verification: Both app and bare SDK attempts had incomplete startup. Bare currentTime stayed at 1.512999 over five seconds with fps 0, bufferSize 0 and no PLAYING; parent geometry was above minimum and visible. Chat loaded public controls.
- Limitations: Exact upstream/browser/application cause unresolved. A bare failure does not establish the app integration correct, and ONLINE, paused=false or a live thumbnail do not prove sustained playback.
- Source: [2026-10-22-interface-validation.md](/home/kevin/coding/viewington-alt/docs/postmortem/2026-10-22-interface-validation.md); reviewed hash retained in sources.json.

- Subsequent desktop occurrence: the user reports that starting a second live stream immediately stops it while the other keeps playing. Read-only app review found no explicit cross-channel pause command; root cause and two-stream playback remain unresolved. Source: [simultaneous playback report](/home/kevin/coding/twitch-grid/docs/postmortem/2026-10-22-simultaneous-playback.md).

## ext-twitch-native-resume-intent

- Status: verified_fix
- Confidence: confirmed
- Verification scope: code
- Symptoms: Native Twitch Play after paused intent starts playback and the app immediately pauses it again.
- Applicability: Media managers that enforce saved playback intent on SDK PLAYING and expose native iframe controls.
- Diagnostics: Replay native PLAY then PLAYING with paused intent and another playing stream; inspect app-issued Pause calls and persisted state after rendering.
- Remedy: Adopt playing intent on PLAY (unpaused, possibly buffering) before PLAYING. Do not issue another Play command; keep PLAYING alone subordinate to explicit pause.
- Verification: Defining manager regression failed paused/paused before correction. Afterwards 129 unit tests, 20 browser tests, typecheck/build and static inspection passed. Browser regression verifies persistence, no corrective commands, other-player isolation and subsequent explicit pause.
- Limitations: Fixture evidence does not establish live two-stream video or audible output. The original desktop symptom still requires retest. SDK events do not distinguish queued programmatic PLAY from a newer native resume; Chrome bridge startup failed and CUA had no browsers.
- Source: [native playback resume incident](/home/kevin/coding/twitch-grid/docs/postmortem/2026-10-22-simultaneous-playback.md); reviewed hash retained in sources.json.

## ext-twitch-fps-presentation-gap

- Status: unresolved (multi-stream lag); diagnostic wording/bitrate boundary verified in code.
- Confidence: confirmed metric-presentation gap; hardware/network cause unknown.
- Applicability: Twitch cross-origin player diagnostics.
- Symptoms: 42–64 reported FPS can accompany visibly choppy multi-stream playback; one stream is smooth.
- Diagnostics: Compare one stream/full lineup and available lower native qualities. Provider frame averages are not evenly presented frames; do not subtract unmatched dropped-frame counters to invent visual FPS.
- Remedy: No verified lag remedy. Show displayed FPS as unavailable when unsupported. Name playbackRate as playback bitrate and label combined partial coverage; never call it actual network download speed.
- Verification: RED→GREEN adapter/manager/browser checks, 136 unit tests/typecheck/build; live 3.11 +3.14 =6.25 Mbps for two advancing videos.
- Limitations: Does not establish user-desktop smoothness, GPU/CPU/network bottleneck or successful real resume.
- Source: [reported FPS and visible stutter](/home/kevin/coding/twitch-grid/docs/postmortem/2026-10-22-reported-fps-visible-stutter.md); reviewed hash retained in sources.json.

## ext-twitch-resolution-quality-ids

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: Sidebar default 360p silently selects Auto while Twitch exposes 360p as group 360p30; 480p likewise uses 480p30.
- Applicability: Twitch iframe integrations that store human-facing bare resolution preferences but send SDK rendition IDs.
- Diagnostics: Compare saved preference with live getQualities name/group pairs, then observe getQuality and fixed-resolution stats. Reproduce at manager and browser boundaries with a saved per-stream override.
- Remedy: Prefer exact available IDs, then the corresponding 30fps ID for a bare resolution, before existing fallback. Do not rewrite explicit 60fps choices or per-stream overrides.
- Verification: Six defining manager regressions and the browser default-quality assertion failed before correction. Afterwards 142 unit tests, 29 browser tests and TypeScript/Vite build passed. Official live SDK selected 360p30 at 640x360 and 480p30 at 852x480; Auto selected auto.
- Limitations: The ID mapping was verified independently, but a later desktop report showed mapping alone was insufficient. See ext-twitch-quality-acknowledgement for ignored requests and older overrides. SDK selection does not establish audibility or sustained visible smoothness.
- Source: [default quality report](/home/kevin/coding/twitch-grid/docs/postmortem/2026-10-22-default-quality.md); reviewed hash retained in sources.json.

## ext-twitch-audience-warning-recovery

- Status: verified_workaround
- Confidence: supported
- Verification scope: runtime
- Symptoms: A live embed stays blurred while the app reports Live; its native frame presents a Gambling warning and Start Watching.
- Applicability: A visible audience-warning interstitial. The informational audience label alone is not conclusive.
- Diagnostics: Inspect the exact native prompt; distinguish ONLINE and cached statistics from moving video.
- Remedy: With explicit viewer approval, use native Start Watching, then native Play if a preview remains. Enlarge the tile to inspect controls. Do not auto-accept warnings or invent force-play loops.
- Verification: Approved acknowledgement removed the warning. Two screenshots show the original app's unblurred advancing video after native Play/startup. A bare official SDK comparison advanced 10.319188 to 16.723766 seconds; its temporary player was removed. No app code changed.
- Limitations: Diagnostic HeadlessChrome only; original desktop lineup and audibility unchecked. Initial post-consent startup delay was not isolated. Repeated cached state messages do not prove motion, and cross-profile acknowledgement persistence is not established.
- Source: [MrSavage blurred playback investigation](/home/kevin/coding/twitch-grid/docs/postmortem/2026-10-22-mrsavage-blurred-playback.md); reviewed hash retained in sources.json.

## ext-twitch-quality-acknowledgement

- Status: verified_fix
- Confidence: confirmed
- Verification scope: runtime
- Symptoms: A default remains at Source after an ignored startup quality setter; a resolved-ID cache suppresses explicit default changes; hidden saved stream overrides bypass the global default.
- Applicability: Twitch iframe managers with asynchronous quality setters, sampled state and persistent per-stream overrides.
- Diagnostics: Drop the first setter and replay mismatching samples; acknowledge then change quality natively; reconnect; change a default while clearing an override that resolves to the same rendition. Inspect actual saved data separately from a fresh browser context.
- Remedy: Send every changed request before accepting an acknowledgement, acknowledge only a later sample, retry pending requests from samples with a three-send budget, and rearm on genuine offline/online recovery. Rearm explicit default changes for default-following channels and changed overrides, even if the rendition ID is unchanged. When the user authorizes all-stream defaults, clear current-lineup overrides at the UI action; retain separately saved profiles.
- Verification: Four defining manager cases and two browser behaviors observed RED, then 146 unit tests, build/typecheck and both focused quality browser tests passed. Independent runtime assertions cover same available/fallback IDs, unchanged overrides and native choices. Real coachboop SDK recovered from a deliberately dropped first setter and the native menu showed360p. Commit-scoped HEAD plus only quality changes independently passed 140 unit tests, build/typecheck and both quality browser cases.
- Limitations: The actual original desktop stored overrides were inaccessible. Native changes before acknowledgement cannot be distinguished from ignored setters; retries are bounded. After three unacknowledged attempts an explicit default change or reload retries. Sustained smoothness/audio not verified. Latest full browser suite had29 passes and2 failures in concurrent bitrate text/video geometry; task quality cases passed.
- Source: [default quality report](/home/kevin/coding/twitch-grid/docs/postmortem/2026-10-22-default-quality.md); reviewed hash retained in sources.json.
