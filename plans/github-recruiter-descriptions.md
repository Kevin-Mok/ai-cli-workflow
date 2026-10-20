# Recruiter-focused GitHub descriptions

Improve public repository descriptions using default-branch evidence, preserve original values for rollback, and verify exact GitHub readbacks. Only remote descriptions may change; no commits, pushes, README changes, or other repository settings are authorized.

## Context and scope

- Authorized by `prompts/recruiter-github-descriptions.md`; executor owns all remote writes.
- Initial paginated inventory: 52 Kevin-Mok-owned, public, original, non-archived repositories, observed 2026-10-20T21:41:46.175477+00:00.
- Protected initial dirty state: postmortem-memory references/api-contracts-fixtures.md, references/operational-drift.md, references/state-security.md and sources.json; docs/postmortem/2026-10-20-description-handoff-runtime.md; prompts/monitor-media-screensaver.md, recruiter-github-descriptions.md, tmux-drag-scroll-copy.md. No staging or commits.
- Local scope: this evidence plan and necessary incident records. Research intermediates stay under /tmp.

## Decisions and assumptions

- Use gh-axi CLI/API with full values and base64-encoded JSON transport to avoid display truncation and retain null/empty distinctions.
- Evidence must support user value and each named technology or capability; exercises and prototypes remain labeled honestly.
- Recheck eligibility and original description immediately before each write. Preserve concurrent changes as conflicts.
- Missing or insufficient evidence means preserve the original description, including null.
- Existing user-provided task specification is decision-complete; no additional design or prompt compilation is needed. Current mode remains Default because no mode-switch tool is available.

## Checklist

- [x] Read instructions and capture initial dirty state.
- [x] Discover gh-axi help and enumerate paginated eligible repositories.
- [x] Inspect default-branch README, relevant sources, manifests and deployment evidence in independent batches.
- [x] Independently review all supporting evidence and finalize descriptions below 250 characters.
- [x] Recheck eligibility/current text, apply descriptions only, record per-repository outcomes.
- [x] Read back all descriptions exactly and re-enumerate eligibility.
- [x] Reconcile counts, exceptions, verification and final handoff.

## Risks and rollback

- Repository documentation may overstate maturity: prefer demonstrated features and concrete source evidence.
- Concurrent description/settings changes: compare before writing and skip conflicts.
- API writes can have ambiguous outcomes: read back before any retry.
- Rollback is a description-only PATCH using the exact Original JSON value below; rollback is not requested.
- No automated RED/GREEN applies to editorial metadata updates. Verification uses actual GitHub API readback, inventory reconciliation, claim review and length checks.

## Verification evidence

- `gh-axi --help`, `gh-axi api --help`, `gh-axi repo --help`: exit 0; established PATCH, --input, --paginate, --jq, --full and repo view syntax.
- Initial `gh-axi api '/users/Kevin-Mok/repos?per_page=100&type=owner' --paginate --full`: sandbox network connection error, exit 1. Scoped escalation succeeded, exit 0. See task incident record.
- Inventory command: `gh-axi api '/users/Kevin-Mok/repos?per_page=100&type=owner' --paginate --jq '[.[] | select(.owner.login == "Kevin-Mok" and .fork == false and .archived == false and .private == false) | {full_name,description,default_branch}] | @base64' --full`: exit 0; decoded 52 exact records.

## Review notes and progress

Completed and verified: 52 eligible; 45 updated; 4 unchanged; 3 preserved for insufficient evidence; 52 exact readback matches; 0 conflicts; 0 failures. No outstanding work or blockers. Only descriptions changed remotely; no commits or pushes. Three independent agents own bounded research batches (18/17/17 repositories); executor independently reviews evidence and retains sole write responsibility.

- Evidence collector: empty default branches returned HTTP 409 for ataraxy-codm and scrape-weather-network; preserve their exact originals for insufficient evidence.
- A read-only besu-deploy blob fetch timed out; its research agent is checking via a scoped read. No remote mutation or ambiguous write occurred.
- Targeted postmortem-memory check for the network incident exited 0, one reviewed report, no errors. Existing dirty ledger entries preserved; one no-new-learning report added.

- Pre-write validation: `python3 /tmp/recruiter_review.py` exited 0; all 52 accounted for, 218 supporting evidence entries, all quoted source excerpts matched. 45 updates (maximum 179 characters), 4 unchanged, 3 insufficient-evidence preservations. Executor read representative implementation context for contracts, auth, persistence, lessons, scheduler, infrastructure, OAuth/D3 and weather validation; simplified maturity and integration claims throughout.
- Initial quote check correctly blocked the write manifest for a safe engine-line excerpt missing after credential redaction; the excerpt was recovered and the complete comparison passed. See description-evidence incident.

- Concurrent workspace changes appeared during execution (README, aliases, fish/i3/MIME configuration, other plans/scripts/tests and staged task records). They are unrelated and remain untouched; no staging, refresh-config or commits are part of this metadata-only task.

## Final verification and delivery

- Final observation: 2026-10-20T21:47:40.601211+00:00. Paginated eligible inventory remains 52; additions 0, removals 0, exact-description mismatches 0.
- `python3 /tmp/recruiter_apply.py`: exit 0. All 45 PATCH bodies contained only `description`; every write exited 0. All 52 preflight checks confirmed eligibility and original-description equality. Immediate per-repository GET readbacks matched all intended values.
- Independent final inventory decoding/comparison: exit 0, 52/52 exact matches. All changed descriptions are below 250 characters (maximum 179). All 218 supporting evidence entries were inspected/compared with fetched default-branch content.
- Unchanged because already suitable: ai-cli-workflow, nextjs-chess-analytics, self-hosted-infra-hardening, weather.
- Preserved for insufficient evidence: ataraxy-codm (empty, original null), jenkins-test (title-only README and minimal initialization pipeline, original null), scrape-weather-network (empty, exact existing description preserved). The scraper’s existing claims remain unverified; preservation does not validate them.
- No runtime tests of the 52 projects were performed or needed for metadata-only publication. Source/document review substantiates changed claims; deployed availability is not asserted. No application code, README, topics, visibility, commits or pushes changed.
- Local records: this plan plus two task incident reports and additive postmortem-memory ledger entries. Protected/concurrent dirty work was not staged or changed by this task. No tracked configuration was changed by this task, so refresh-config does not apply.
- Verification commands below all ran after updates and exited 0. Working directory: any; no sudo required; authenticated gh-axi with network access required. Expected examples are abbreviated where indicated; full outputs were read in execution.

### Direct count

gh-axi api '/users/Kevin-Mok/repos?per_page=100&type=owner' --paginate --jq '[.[] | select(.owner.login == "Kevin-Mok" and .fork == false and .archived == false and .private == false)] | length' --full

Expected and observed: `52` (one API page currently contains all 86 owned repositories).

### Representative retained description

gh-axi repo view Kevin-Mok/weather

Expected and observed: weather, public, main, description `Responsive Next.js weather dashboard with 12-hour forecasts, a validated Weather Network feed for Scarborough, Toronto, and Open-Meteo fallback.`

### Complete final description listing

gh-axi api '/users/Kevin-Mok/repos?per_page=100&type=owner' --paginate --jq '[.[] | select(.owner.login == "Kevin-Mok" and .fork == false and .archived == false and .private == false) | {name,description}]' --full

Expected and observed: `[52]{description,name}:` followed by all 52 complete descriptions, including null for ataraxy-codm and jenkins-test.

### Records review

- Both task incident reports are resolved/worked around with verified scope. Their targeted postmortem-memory checks pass (exit 0), with exact reviewed hashes and explicit no-new-learning decisions. Existing ledger changes were preserved.
- Final plan reconciles all 52 original values, intended values, source references, write statuses and readbacks. Rollback remains description-only PATCH to the exact Original JSON values in each entry and was not performed.
- Saved authorized prompt: `prompts/recruiter-github-descriptions.md`; unchanged by executor. No new execution conversation was launched.

## Repository evidence and outcomes

### Kevin-Mok/acanet-voting

- Default branch: `master`
- Original JSON: `"Voting on the blockchain for academic purposes."`
- Intended JSON: `"Academic e-voting prototype with encrypted Ethereum ballots and multi-party tallying, built with Solidity, React, TypeScript, and Docker."`
- Decision: update; Replace vague academic summary with supported architecture; deliberately avoid README production/security assurances.
- Length: 137
- Evidence commit: [`79433efd505657adf0c518a573bde06eb513d175`](https://github.com/Kevin-Mok/acanet-voting/commit/79433efd505657adf0c518a573bde06eb513d175)
- Evidence: [README.md](https://github.com/Kevin-Mok/acanet-voting/blob/79433efd505657adf0c518a573bde06eb513d175/README.md) — Based on [Provotum]
- Evidence: [contracts/contracts/FiniteField/Ballot.sol](https://github.com/Kevin-Mok/acanet-voting/blob/79433efd505657adf0c518a573bde06eb513d175/contracts/contracts/FiniteField/Ballot.sol) — enum VotingState {KEY_GENERATION, VOTING, TALLYING, RESULT}
- Evidence: [contracts/contracts/FiniteField/Ballot.sol](https://github.com/Kevin-Mok/acanet-voting/blob/79433efd505657adf0c518a573bde06eb513d175/contracts/contracts/FiniteField/Ballot.sol) — // represents the decryption of all vote-ciphers done by one sealer
- Evidence: [README.md](https://github.com/Kevin-Mok/acanet-voting/blob/79433efd505657adf0c518a573bde06eb513d175/README.md) — | **Frontend** | React 16, Material-UI, TypeScript, Zustand |
- Evidence: [README-orig.md](https://github.com/Kevin-Mok/acanet-voting/blob/79433efd505657adf0c518a573bde06eb513d175/README-orig.md) — Use `./docker-up.sh` and `./docker-down.sh` to start/stop all docker containers.
- Status: updated
- Preflight: 2026-10-20T21:46:12.353738+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Academic e-voting prototype with encrypted Ethereum ballots and multi-party tallying, built with Solidity, React, TypeScript, and Docker."`; exact match: True; observed 2026-10-20T21:46:13.442812+00:00

### Kevin-Mok/ai-alpha-build-log

- Default branch: `main`
- Original JSON: `"AI-native full-stack blog and build log showing how I use AI workflows to increase output, ship faster and deliver stronger client-ready product work."`
- Intended JSON: `"Publish an AI engineering build log with Next.js, TypeScript, and MDX, with Supabase-protected admin views and Prisma/Postgres storage for subscribers and inquiries."`
- Decision: update; Concrete publishing, authorization and persistence replace unsupported productivity claims.
- Length: 165
- Evidence commit: [`9c024dc495e2f556d5248cb9e5186f75719dc1a4`](https://github.com/Kevin-Mok/ai-alpha-build-log/commit/9c024dc495e2f556d5248cb9e5186f75719dc1a4)
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/README.md) — MDX content loaded from `content/posts/*.mdx`
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/README.md) — Supabase-authenticated admin routes with role checks
- Evidence: [prisma/schema.prisma](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/prisma/schema.prisma) — provider = "postgresql"
- Evidence: [prisma/schema.prisma](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/prisma/schema.prisma) — model ContactInquiry {
- Evidence: [package.json](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/package.json) — "next": "^15.2.4"
- Evidence: [package.json](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/package.json) — "typescript": "^5.8.2"
- Evidence: [lib/auth/admin.ts](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/lib/auth/admin.ts) — supabase.auth.getUser()
- Evidence: [lib/auth/admin.ts](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/lib/auth/admin.ts) — profile.role !== ProfileRole.ADMIN
- Evidence: [lib/actions/contact.ts](https://github.com/Kevin-Mok/ai-alpha-build-log/blob/9c024dc495e2f556d5248cb9e5186f75719dc1a4/lib/actions/contact.ts) — await createContactInquiry(result.data);
- Status: updated
- Preflight: 2026-10-20T21:46:13.917760+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Publish an AI engineering build log with Next.js, TypeScript, and MDX, with Supabase-protected admin views and Prisma/Postgres storage for subscribers and inquiries."`; exact match: True; observed 2026-10-20T21:46:14.948889+00:00

### Kevin-Mok/ai-chess-coach-llm

- Default branch: `main`
- Original JSON: `"Reproducible chess review core with optional on-device LLM coaching, format-checked outputs, and safe fallback behavior."`
- Intended JSON: `"Turn chess PGNs into reproducible local review reports with Python, Stockfish/Lc0 analysis, optional on-device LLM coaching, and deterministic fallback behavior."`
- Decision: update; Lead with PGN-to-report value and supported local tooling; avoid generic review-core phrasing.
- Length: 161
- Evidence commit: [`a8c025a9cd32c5cd966d7683cd7a050c7518acac`](https://github.com/Kevin-Mok/ai-chess-coach-llm/commit/a8c025a9cd32c5cd966d7683cd7a050c7518acac)
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-chess-coach-llm/blob/a8c025a9cd32c5cd966d7683cd7a050c7518acac/README.md) — a local-first analysis pipeline that turns PGNs into reproducible markdown reports.
- Evidence: [pgn_analyzer/cli.py](https://github.com/Kevin-Mok/ai-chess-coach-llm/blob/a8c025a9cd32c5cd966d7683cd7a050c7518acac/pgn_analyzer/cli.py) — Cause generation mode: heuristic (fast), forensic (Stockfish+Lc0),
- Evidence: [pgn_analyzer/cli.py](https://github.com/Kevin-Mok/ai-chess-coach-llm/blob/a8c025a9cd32c5cd966d7683cd7a050c7518acac/pgn_analyzer/cli.py) — or forensic-llm (forensic + optional local rewrite); default:
- Evidence: [pgn_analyzer/common.py](https://github.com/Kevin-Mok/ai-chess-coach-llm/blob/a8c025a9cd32c5cd966d7683cd7a050c7518acac/pgn_analyzer/common.py) — def enforce_human_field(text, fallback, max_chars=MAX_COACHING_CHARS):
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-chess-coach-llm/blob/a8c025a9cd32c5cd966d7683cd7a050c7518acac/README.md) — Deterministic fallback behavior when optional AI components are unavailable.
- Status: updated
- Preflight: 2026-10-20T21:46:15.367535+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Turn chess PGNs into reproducible local review reports with Python, Stockfish/Lc0 analysis, optional on-device LLM coaching, and deterministic fallback behavior."`; exact match: True; observed 2026-10-20T21:46:16.366076+00:00

### Kevin-Mok/ai-cli-workflow

- Default branch: `main`
- Original JSON: `"A reproducible Linux workspace for AI-assisted engineering: Codex workflows, reusable skills, automation, and dotfiles managed with chezmoi."`
- Intended JSON: `"A reproducible Linux workspace for AI-assisted engineering: Codex workflows, reusable skills, automation, and dotfiles managed with chezmoi."`
- Decision: unchanged; Existing description already states concrete workspace value, supported automation, and chezmoi reproducibility; no useful rewrite needed.
- Length: 140
- Evidence commit: [`cc5f2e379431679b97591567a764d88793b3b38e`](https://github.com/Kevin-Mok/ai-cli-workflow/commit/cc5f2e379431679b97591567a764d88793b3b38e)
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-cli-workflow/blob/cc5f2e379431679b97591567a764d88793b3b38e/README.md) — A reproducible Linux workspace for AI-assisted engineering.
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-cli-workflow/blob/cc5f2e379431679b97591567a764d88793b3b38e/README.md) — preview and apply the configuration with `chezmoi`
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-cli-workflow/blob/cc5f2e379431679b97591567a764d88793b3b38e/README.md) — | Python and Bash automation |
- Evidence: [README.md](https://github.com/Kevin-Mok/ai-cli-workflow/blob/cc5f2e379431679b97591567a764d88793b3b38e/README.md) — | Local skills |
- Status: unchanged
- Preflight: 2026-10-20T21:46:16.785583+00:00; eligibility True; current-description matched original: True
- PATCH exit: not issued; readback JSON: `"A reproducible Linux workspace for AI-assisted engineering: Codex workflows, reusable skills, automation, and dotfiles managed with chezmoi."`; exact match: True; observed 2026-10-20T21:46:17.297603+00:00

### Kevin-Mok/astronofty

- Default branch: `main`
- Original JSON: `"NFT marketplace to create/buy/sell astrophotography. Won 2nd at UofT Hacks X. [React]"`
- Intended JSON: `"Mint, buy, and sell astrophotography NFTs in a React/Solidity hackathon marketplace with IPFS image storage; placed 2nd overall at UofTHacks."`
- Decision: update; Preserve supported award and user value; add contracts/storage and explicit hackathon maturity.
- Length: 141
- Evidence commit: [`b97f1a855d586aca928da59e925b2d79508d67b1`](https://github.com/Kevin-Mok/astronofty/commit/b97f1a855d586aca928da59e925b2d79508d67b1)
- Evidence: [README.md](https://github.com/Kevin-Mok/astronofty/blob/b97f1a855d586aca928da59e925b2d79508d67b1/README.md) — Built for UofTHacks where it placed **2nd overall**.
- Evidence: [README.md](https://github.com/Kevin-Mok/astronofty/blob/b97f1a855d586aca928da59e925b2d79508d67b1/README.md) — | **Frontend** | React 18, React Router 6, Tailwind CSS |
- Evidence: [README.md](https://github.com/Kevin-Mok/astronofty/blob/b97f1a855d586aca928da59e925b2d79508d67b1/README.md) — | **Storage** | IPFS via Estuary/Pinata |
- Evidence: [contracts/NFTMarketplace.sol](https://github.com/Kevin-Mok/astronofty/blob/b97f1a855d586aca928da59e925b2d79508d67b1/contracts/NFTMarketplace.sol) — contract NFTMarketplace is ERC721URIStorage {
- Evidence: [contracts/NFTMarketplace.sol](https://github.com/Kevin-Mok/astronofty/blob/b97f1a855d586aca928da59e925b2d79508d67b1/contracts/NFTMarketplace.sol) — function executeSale(uint256 tokenId) public payable {
- Status: updated
- Preflight: 2026-10-20T21:46:17.695225+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Mint, buy, and sell astrophotography NFTs in a React/Solidity hackathon marketplace with IPFS image storage; placed 2nd overall at UofTHacks."`; exact match: True; observed 2026-10-20T21:46:18.724817+00:00

### Kevin-Mok/ataraxy-codm

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `null`
- Decision: preserve_insufficient; Empty repository (parent verified HTTP 409); no README or source supports a description. Preserve original null.
- Length: null preserved
- Status: preserve_insufficient
- Preflight: 2026-10-20T21:46:19.119025+00:00; eligibility True; current-description matched original: True
- PATCH exit: not issued; readback JSON: `null`; exact match: True; observed 2026-10-20T21:46:19.502736+00:00

### Kevin-Mok/austin

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Introduce students to AI infrastructure and environmental trade-offs through a frontend-only Next.js, React, and TypeScript starter homepage."`
- Decision: update; Accurately describes current starter rather than future curriculum features.
- Length: 141
- Evidence commit: [`57aa18929ccf7b7b6e47d9dfb96a81101cd6a9fa`](https://github.com/Kevin-Mok/austin/commit/57aa18929ccf7b7b6e47d9dfb96a81101cd6a9fa)
- Evidence: [README.md](https://github.com/Kevin-Mok/austin/blob/57aa18929ccf7b7b6e47d9dfb96a81101cd6a9fa/README.md) — The first version is intentionally simple: one homepage with a clear title, mission statement, and three preview cards.
- Evidence: [README.md](https://github.com/Kevin-Mok/austin/blob/57aa18929ccf7b7b6e47d9dfb96a81101cd6a9fa/README.md) — **TypeScript:** checks the code for common mistakes.
- Evidence: [app/page.tsx](https://github.com/Kevin-Mok/austin/blob/57aa18929ccf7b7b6e47d9dfb96a81101cd6a9fa/app/page.tsx) — AI tools feel instant, but they depend on data centers, servers, chips, electricity, cooling, and networks.
- Status: updated
- Preflight: 2026-10-20T21:46:19.933509+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Introduce students to AI infrastructure and environmental trade-offs through a frontend-only Next.js, React, and TypeScript starter homepage."`; exact match: True; observed 2026-10-20T21:46:20.953442+00:00

### Kevin-Mok/aws-minicube

- Default branch: `main`
- Original JSON: `"Kubernetes manifest files to recreate my AWS EC2 server on minikube."`
- Intended JSON: `"Recreate Hemmelig secret sharing and PiGallery photo hosting on local minikube with Kubernetes deployments, services, and persistent-volume manifests."`
- Decision: update; Name actual hosted tools and local Kubernetes scope instead of implying EC2 provisioning.
- Length: 150
- Evidence commit: [`a72a9890f4cb11ed3fa97f8e209d4fcd89568111`](https://github.com/Kevin-Mok/aws-minicube/commit/a72a9890f4cb11ed3fa97f8e209d4fcd89568111)
- Evidence: [README.md](https://github.com/Kevin-Mok/aws-minicube/blob/a72a9890f4cb11ed3fa97f8e209d4fcd89568111/README.md) — # My AWS Server on minikube
- Evidence: [README.md](https://github.com/Kevin-Mok/aws-minicube/blob/a72a9890f4cb11ed3fa97f8e209d4fcd89568111/README.md) — script to apply and delete the applications from your minikube Kubernetes instance.
- Evidence: [hemmelig/deployment.yaml](https://github.com/Kevin-Mok/aws-minicube/blob/a72a9890f4cb11ed3fa97f8e209d4fcd89568111/hemmelig/deployment.yaml) — image: hemmeligapp/hemmelig:v5.19.17
- Evidence: [pigallery/deployment.yaml](https://github.com/Kevin-Mok/aws-minicube/blob/a72a9890f4cb11ed3fa97f8e209d4fcd89568111/pigallery/deployment.yaml) — image: bpatrik/pigallery2:latest
- Evidence: [pigallery/deployment.yaml](https://github.com/Kevin-Mok/aws-minicube/blob/a72a9890f4cb11ed3fa97f8e209d4fcd89568111/pigallery/deployment.yaml) — persistentVolumeClaim:
- Status: updated
- Preflight: 2026-10-20T21:46:21.355567+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Recreate Hemmelig secret sharing and PiGallery photo hosting on local minikube with Kubernetes deployments, services, and persistent-volume manifests."`; exact match: True; observed 2026-10-20T21:46:22.407779+00:00

### Kevin-Mok/besu-deploy

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Explore Solidity compilation and raw Ethereum deployment transactions in a Node.js/Web3.js prototype with ABI-encoded constructor arguments."`
- Decision: update; Deployment code and saved error show exploratory tooling; avoid working-toolkit or arbitrary-network assurances.
- Length: 140
- Evidence commit: [`8c1b3ad699e85b5b348daff0d690d6cf09c0e1e5`](https://github.com/Kevin-Mok/besu-deploy/commit/8c1b3ad699e85b5b348daff0d690d6cf09c0e1e5)
- Evidence: [compile.js](https://github.com/Kevin-Mok/besu-deploy/blob/8c1b3ad699e85b5b348daff0d690d6cf09c0e1e5/compile.js) — const solc = require('solc');
- Evidence: [compile.js](https://github.com/Kevin-Mok/besu-deploy/blob/8c1b3ad699e85b5b348daff0d690d6cf09c0e1e5/compile.js) — await fs.writeFile('SimpleStorage.json', artifact);
- Evidence: [public_tx.js](https://github.com/Kevin-Mok/besu-deploy/blob/8c1b3ad699e85b5b348daff0d690d6cf09c0e1e5/public_tx.js) — const contractConstructorInit = web3.eth.abi.encodeParameters(['uint'], ['47']).slice(2);
- Evidence: [to-buffer-error.txt](https://github.com/Kevin-Mok/besu-deploy/blob/8c1b3ad699e85b5b348daff0d690d6cf09c0e1e5/to-buffer-error.txt) — Error: Cannot convert string to buffer.
- Status: updated
- Preflight: 2026-10-20T21:46:22.856791+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Explore Solidity compilation and raw Ethereum deployment transactions in a Node.js/Web3.js prototype with ABI-encoded constructor arguments."`; exact match: True; observed 2026-10-20T21:46:24.072661+00:00

### Kevin-Mok/difference-array

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Teach difference arrays and prefix sums through an interactive Next.js/TypeScript lesson deck with presenter/student modes, stepwise traces, and Java/Python examples."`
- Decision: update; Describes implemented teaching surface, not merely an algorithm name.
- Length: 166
- Evidence commit: [`43c3c85e692d273c11678b82445acc8efe46f290`](https://github.com/Kevin-Mok/difference-array/commit/43c3c85e692d273c11678b82445acc8efe46f290)
- Evidence: [README.md](https://github.com/Kevin-Mok/difference-array/blob/43c3c85e692d273c11678b82445acc8efe46f290/README.md) — reveal controls, presenter/student modes, language toggles, trace stepping, and live notes.
- Evidence: [components/LessonFlowDeck.tsx](https://github.com/Kevin-Mok/difference-array/blob/43c3c85e692d273c11678b82445acc8efe46f290/components/LessonFlowDeck.tsx) — type AudienceMode = "presenter" | "student";
- Evidence: [components/LessonFlowDeck.tsx](https://github.com/Kevin-Mok/difference-array/blob/43c3c85e692d273c11678b82445acc8efe46f290/components/LessonFlowDeck.tsx) — type SolutionLanguage = "java" | "python";
- Evidence: [README.md](https://github.com/Kevin-Mok/difference-array/blob/43c3c85e692d273c11678b82445acc8efe46f290/README.md) — **Next.js App Router**
- Status: updated
- Preflight: 2026-10-20T21:46:24.502706+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Teach difference arrays and prefix sums through an interactive Next.js/TypeScript lesson deck with presenter/student modes, stepwise traces, and Java/Python examples."`; exact match: True; observed 2026-10-20T21:46:25.705423+00:00

### Kevin-Mok/discord-marketplace-bot

- Default branch: `main`
- Original JSON: `"Custom Discord marketplace system that automates listings, buyer reservations, staff-confirmed fee collection, and real-time lowest-price market boards. "`
- Intended JSON: `"Coordinate Discord item sales with a Python/Red-DiscordBot marketplace featuring listing wizards, buyer reservations, staff-confirmed fees, and automatic lowest-price boards."`
- Decision: update; Retain concrete lifecycle value, make implementation stack explicit and avoid real-time guarantees.
- Length: 174
- Evidence commit: [`8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813`](https://github.com/Kevin-Mok/discord-marketplace-bot/commit/8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813)
- Evidence: [README.md](https://github.com/Kevin-Mok/discord-marketplace-bot/blob/8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813/README.md) — | **Framework** | Red-DiscordBot 3.x |
- Evidence: [README.md](https://github.com/Kevin-Mok/discord-marketplace-bot/blob/8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813/README.md) — | **Language** | Python 3.11+ |
- Evidence: [README.md](https://github.com/Kevin-Mok/discord-marketplace-bot/blob/8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813/README.md) — **Wizard-Based Listing**
- Evidence: [README.md](https://github.com/Kevin-Mok/discord-marketplace-bot/blob/8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813/README.md) — **Auto-Refreshing Embeds** - Show lowest price per mutation
- Evidence: [cogs/stbmarket/cog.py](https://github.com/Kevin-Mok/discord-marketplace-bot/blob/8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813/cogs/stbmarket/cog.py) — # Per-listing locks serialize competing buyer reservations without blocking the whole cog.
- Evidence: [cogs/stbmarket/models.py](https://github.com/Kevin-Mok/discord-marketplace-bot/blob/8ca7a4480fd0a69736d4dcfdeb5c9cbd56335813/cogs/stbmarket/models.py) — fee_confirmed_by: Optional[int] = None
- Status: updated
- Preflight: 2026-10-20T21:46:26.160790+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Coordinate Discord item sales with a Python/Red-DiscordBot marketplace featuring listing wizards, buyer reservations, staff-confirmed fees, and automatic lowest-price boards."`; exact match: True; observed 2026-10-20T21:46:27.145726+00:00

### Kevin-Mok/drag-drop-kanban-scheduler

- Default branch: `main`
- Original JSON: `"Responsive kanban-style calendar app with draggable events, swipe navigation, and smooth Framer Motion transitions, built with Next.js   15, React 19, and TypeScript. "`
- Intended JSON: `"Replan events in a responsive Next.js/React calendar demo with TypeScript, drag-and-drop scheduling, mobile swipes, keyboard navigation, and Framer Motion transitions."`
- Decision: update; Lead with event replanning and acknowledge demo/sample-data scope.
- Length: 167
- Evidence commit: [`32e4af2c2f23c72bbfbc22bb561f092557cf4295`](https://github.com/Kevin-Mok/drag-drop-kanban-scheduler/commit/32e4af2c2f23c72bbfbc22bb561f092557cf4295)
- Evidence: [README.md](https://github.com/Kevin-Mok/drag-drop-kanban-scheduler/blob/32e4af2c2f23c72bbfbc22bb561f092557cf4295/README.md) — **Keyboard Navigation** - Arrow keys to navigate weeks on desktop
- Evidence: [README.md](https://github.com/Kevin-Mok/drag-drop-kanban-scheduler/blob/32e4af2c2f23c72bbfbc22bb561f092557cf4295/README.md) — **Swipe Navigation**
- Evidence: [src/components/Calendar.tsx](https://github.com/Kevin-Mok/drag-drop-kanban-scheduler/blob/32e4af2c2f23c72bbfbc22bb561f092557cf4295/src/components/Calendar.tsx) — import eventsData, { generateEventsForDate } from '@/data/events';
- Evidence: [src/components/Calendar.tsx](https://github.com/Kevin-Mok/drag-drop-kanban-scheduler/blob/32e4af2c2f23c72bbfbc22bb561f092557cf4295/src/components/Calendar.tsx) — newEvents[targetDate] = [...(newEvents[targetDate] || []), movedEvent];
- Evidence: [src/components/Calendar.tsx](https://github.com/Kevin-Mok/drag-drop-kanban-scheduler/blob/32e4af2c2f23c72bbfbc22bb561f092557cf4295/src/components/Calendar.tsx) — import { motion, AnimatePresence } from 'framer-motion';
- Evidence: [package.json](https://github.com/Kevin-Mok/drag-drop-kanban-scheduler/blob/32e4af2c2f23c72bbfbc22bb561f092557cf4295/package.json) — "react": "^19.0.0"
- Status: updated
- Preflight: 2026-10-20T21:46:27.573032+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Replan events in a responsive Next.js/React calendar demo with TypeScript, drag-and-drop scheduling, mobile swipes, keyboard navigation, and Framer Motion transitions."`; exact match: True; observed 2026-10-20T21:46:28.559198+00:00

### Kevin-Mok/easyPokerHUD

- Default branch: `master`
- Original JSON: `"This is the official repository for easyPokerHUD. "`
- Intended JSON: `"Display poker player statistics from PokerStars and 888 Poker hand histories with an open-source C#/.NET HUD and SQLite storage."`
- Decision: update; Replace official-repository boilerplate with supported capability without claiming original authorship.
- Length: 128
- Evidence commit: [`0a06fd7ec3a569ad440ecdf97f8c287f86294472`](https://github.com/Kevin-Mok/easyPokerHUD/commit/0a06fd7ec3a569ad440ecdf97f8c287f86294472)
- Evidence: [README.md](https://github.com/Kevin-Mok/easyPokerHUD/blob/0a06fd7ec3a569ad440ecdf97f8c287f86294472/README.md) — easyPokerHUD is a free and open-source poker HUD for PokerStars and 888 Poker. It is build with C# and SQLite.
- Evidence: [README.md](https://github.com/Kevin-Mok/easyPokerHUD/blob/0a06fd7ec3a569ad440ecdf97f8c287f86294472/README.md) — Set .net framework to 4.6.1
- Evidence: [easyPokerHUD/Source/Global/HandHistoryWatcher.cs](https://github.com/Kevin-Mok/easyPokerHUD/blob/0a06fd7ec3a569ad440ecdf97f8c287f86294472/easyPokerHUD/Source/Global/HandHistoryWatcher.cs) — public class HandHistoryWatcher : FileSystemWatcher
- Evidence: [README.md](https://github.com/Kevin-Mok/easyPokerHUD/blob/0a06fd7ec3a569ad440ecdf97f8c287f86294472/README.md) — positioning the stats windows for each player accordingly.
- Status: updated
- Preflight: 2026-10-20T21:46:28.936065+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Display poker player statistics from PokerStars and 888 Poker hand histories with an open-source C#/.NET HUD and SQLite storage."`; exact match: True; observed 2026-10-20T21:46:30.224203+00:00

### Kevin-Mok/face-tracker

- Default branch: `master`
- Original JSON: `"Track user's face."`
- Intended JSON: `"Explore webcam face and eye tracking with a C++/OpenCV prototype that detects pupils, smooths motion, and moves the Linux mouse through xdotool."`
- Decision: update; Describe actual computer-vision integration with prototype maturity; no accessibility reliability or FPS guarantee.
- Length: 144
- Evidence commit: [`91541f63f3bea77882b179522c080018da00ef1e`](https://github.com/Kevin-Mok/face-tracker/commit/91541f63f3bea77882b179522c080018da00ef1e)
- Evidence: [eye_detector.cpp](https://github.com/Kevin-Mok/face-tracker/blob/91541f63f3bea77882b179522c080018da00ef1e/eye_detector.cpp) — HoughCircles(eye, circles, HOUGH_GRADIENT
- Evidence: [eye_detector.cpp](https://github.com/Kevin-Mok/face-tracker/blob/91541f63f3bea77882b179522c080018da00ef1e/eye_detector.cpp) — center = stabilize(centers, 5);
- Evidence: [eye_detector.cpp](https://github.com/Kevin-Mok/face-tracker/blob/91541f63f3bea77882b179522c080018da00ef1e/eye_detector.cpp) — system(("xdotool mousemove "
- Evidence: [eye_detector.cpp](https://github.com/Kevin-Mok/face-tracker/blob/91541f63f3bea77882b179522c080018da00ef1e/eye_detector.cpp) — VideoCapture cap(0);
- Evidence: [eye_detector.cpp](https://github.com/Kevin-Mok/face-tracker/blob/91541f63f3bea77882b179522c080018da00ef1e/eye_detector.cpp) — #include <opencv2/core.hpp>
- Status: updated
- Preflight: 2026-10-20T21:46:30.682114+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Explore webcam face and eye tracking with a C++/OpenCV prototype that detects pupils, smooths motion, and moves the Linux mouse through xdotool."`; exact match: True; observed 2026-10-20T21:46:31.598297+00:00

### Kevin-Mok/ganache-tx

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Learn raw Ethereum transactions with a Node.js/Web3.js demo that constructs, signs, and broadcasts a transaction to a local Ganache chain."`
- Decision: update; Educational demo is justified by small single-file implementation; no secure-key-handling claim.
- Length: 138
- Evidence commit: [`b2bccf94620ca45f2c7af3bf1d306b13c54c04dd`](https://github.com/Kevin-Mok/ganache-tx/commit/b2bccf94620ca45f2c7af3bf1d306b13c54c04dd)
- Evidence: [README.md](https://github.com/Kevin-Mok/ganache-tx/blob/b2bccf94620ca45f2c7af3bf1d306b13c54c04dd/README.md) — Ethereum transaction demonstration
- Evidence: [index.js](https://github.com/Kevin-Mok/ganache-tx/blob/b2bccf94620ca45f2c7af3bf1d306b13c54c04dd/index.js) — const url = 'http://127.0.0.1:8545'
- Evidence: [index.js](https://github.com/Kevin-Mok/ganache-tx/blob/b2bccf94620ca45f2c7af3bf1d306b13c54c04dd/index.js) — import { Transaction } from 'ethereumjs-tx'
- Evidence: [index.js](https://github.com/Kevin-Mok/ganache-tx/blob/b2bccf94620ca45f2c7af3bf1d306b13c54c04dd/index.js) — tx.sign(Buffer.from(privateKey.slice(2), 'hex'));
- Evidence: [index.js](https://github.com/Kevin-Mok/ganache-tx/blob/b2bccf94620ca45f2c7af3bf1d306b13c54c04dd/index.js) — web3.eth.sendSignedTransaction
- Status: updated
- Preflight: 2026-10-20T21:46:31.974692+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Learn raw Ethereum transactions with a Node.js/Web3.js demo that constructs, signs, and broadcasts a transaction to a local Ganache chain."`; exact match: True; observed 2026-10-20T21:46:32.993590+00:00

### Kevin-Mok/grocery-finder

- Default branch: `master`
- Original JSON: `"Proof of concept for a web app that finds the best supermarket for your needs."`
- Intended JSON: `"Compare grocery stores for a shopping cart in a course-project prototype built with Node.js, Express, and MongoDB, with saved carts and session-based login."`
- Decision: update; Retain proof-of-concept maturity and add supported backend/persistence signals.
- Length: 156
- Evidence commit: [`f3ec4830e3eb160fad4aa4c0e99ad4310f127358`](https://github.com/Kevin-Mok/grocery-finder/commit/f3ec4830e3eb160fad4aa4c0e99ad4310f127358)
- Evidence: [README.md](https://github.com/Kevin-Mok/grocery-finder/blob/f3ec4830e3eb160fad4aa4c0e99ad4310f127358/README.md) — Built as a CSC309 course project at University of Toronto.
- Evidence: [README.md](https://github.com/Kevin-Mok/grocery-finder/blob/f3ec4830e3eb160fad4aa4c0e99ad4310f127358/README.md) — **Store Comparison** - Find best stores by price and distance
- Evidence: [server.js](https://github.com/Kevin-Mok/grocery-finder/blob/f3ec4830e3eb160fad4aa4c0e99ad4310f127358/server.js) — app.get('/get_cart', (req, res) => {
- Evidence: [server.js](https://github.com/Kevin-Mok/grocery-finder/blob/f3ec4830e3eb160fad4aa4c0e99ad4310f127358/server.js) — app.post('/save_cart', (req, res) => {
- Evidence: [package.json](https://github.com/Kevin-Mok/grocery-finder/blob/f3ec4830e3eb160fad4aa4c0e99ad4310f127358/package.json) — "express-session": "^1.15.6"
- Evidence: [package.json](https://github.com/Kevin-Mok/grocery-finder/blob/f3ec4830e3eb160fad4aa4c0e99ad4310f127358/package.json) — "mongoose": "^5.3.14"
- Status: updated
- Preflight: 2026-10-20T21:46:33.411817+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Compare grocery stores for a shopping cart in a course-project prototype built with Node.js, Express, and MongoDB, with saved carts and session-based login."`; exact match: True; observed 2026-10-20T21:46:34.367578+00:00

### Kevin-Mok/image-tagger

- Default branch: `master`
- Original JSON: `"Image-tagging software written in JavaFX."`
- Intended JSON: `"Organize image collections in a JavaFX desktop app with batch tagging, tag-based filenames, rename history, persistent session data, and Imgur uploads."`
- Decision: update; Expand underspecified original with concrete supported organization workflows.
- Length: 151
- Evidence commit: [`ffaaa8c29db0d22b8554c3d5d09c374400803bb0`](https://github.com/Kevin-Mok/image-tagger/commit/ffaaa8c29db0d22b8554c3d5d09c374400803bb0)
- Evidence: [README.md](https://github.com/Kevin-Mok/image-tagger/blob/ffaaa8c29db0d22b8554c3d5d09c374400803bb0/README.md) — **Batch Operations** - Apply tags to multiple images or entire directories
- Evidence: [README.md](https://github.com/Kevin-Mok/image-tagger/blob/ffaaa8c29db0d22b8554c3d5d09c374400803bb0/README.md) — **Name History** - Track all previous filenames with timestamps, revert with one click
- Evidence: [README.md](https://github.com/Kevin-Mok/image-tagger/blob/ffaaa8c29db0d22b8554c3d5d09c374400803bb0/README.md) — **Imgur Upload** - Direct upload to Imgur with API integration
- Evidence: [src/fx/Main.java](https://github.com/Kevin-Mok/image-tagger/blob/ffaaa8c29db0d22b8554c3d5d09c374400803bb0/src/fx/Main.java) — public class Main extends Application {
- Evidence: [src/fx/Main.java](https://github.com/Kevin-Mok/image-tagger/blob/ffaaa8c29db0d22b8554c3d5d09c374400803bb0/src/fx/Main.java) — imageTagManager.saveToFile();
- Status: updated
- Preflight: 2026-10-20T21:46:34.751552+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Organize image collections in a JavaFX desktop app with batch tagging, tag-based filenames, rename history, persistent session data, and Imgur uploads."`; exact match: True; observed 2026-10-20T21:46:35.764849+00:00

### Kevin-Mok/interceptor-kernel

- Default branch: `master`
- Original JSON: `null`
- Intended JSON: `"Monitor per-process Linux system calls in a C kernel-module coursework project using syscall interception, PID tracking, and spinlock synchronization."`
- Decision: update; Truthful coursework context and supported low-level mechanisms; no modern-kernel compatibility or security guarantee.
- Length: 150
- Evidence commit: [`c760d5a0e9023a1f9e15c12a279db6e702f68ac4`](https://github.com/Kevin-Mok/interceptor-kernel/commit/c760d5a0e9023a1f9e15c12a279db6e702f68ac4)
- Evidence: [README.md](https://github.com/Kevin-Mok/interceptor-kernel/blob/c760d5a0e9023a1f9e15c12a279db6e702f68ac4/README.md) — Developed as coursework for operating systems.
- Evidence: [a1/interceptor.c](https://github.com/Kevin-Mok/interceptor-kernel/blob/c760d5a0e9023a1f9e15c12a279db6e702f68ac4/a1/interceptor.c) — extern void* sys_call_table[];
- Evidence: [a1/interceptor.c](https://github.com/Kevin-Mok/interceptor-kernel/blob/c760d5a0e9023a1f9e15c12a279db6e702f68ac4/a1/interceptor.c) — struct pid_list {
- Evidence: [a1/interceptor.c](https://github.com/Kevin-Mok/interceptor-kernel/blob/c760d5a0e9023a1f9e15c12a279db6e702f68ac4/a1/interceptor.c) — spinlock_t my_table_lock = SPIN_LOCK_UNLOCKED;
- Status: updated
- Preflight: 2026-10-20T21:46:36.231205+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Monitor per-process Linux system calls in a C kernel-module coursework project using syscall interception, PID tracking, and spinlock synchronization."`; exact match: True; observed 2026-10-20T21:46:37.219358+00:00

### Kevin-Mok/java-lesson-2

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Teach Java OOP through interactive robot-building exercises in Next.js and TypeScript, with answer feedback, a lesson timer, and browser-saved progress."`
- Decision: update; Replace missing description with classroom value and verified interactivity.
- Length: 152
- Evidence commit: [`ac85ad9287f08318075be751450637002dc25017`](https://github.com/Kevin-Mok/java-lesson-2/commit/ac85ad9287f08318075be751450637002dc25017)
- Evidence: [README.md](https://github.com/Kevin-Mok/java-lesson-2/blob/ac85ad9287f08318075be751450637002dc25017/README.md) — Java objects and constructors
- Evidence: [package.json](https://github.com/Kevin-Mok/java-lesson-2/blob/ac85ad9287f08318075be751450637002dc25017/package.json) — "typescript": "5.6.3"
- Evidence: [src/app/page.tsx](https://github.com/Kevin-Mok/java-lesson-2/blob/ac85ad9287f08318075be751450637002dc25017/src/app/page.tsx) — const result = evalConceptAnswer
- Evidence: [src/lib/persistence.ts](https://github.com/Kevin-Mok/java-lesson-2/blob/ac85ad9287f08318075be751450637002dc25017/src/lib/persistence.ts) — window.localStorage.setItem(LESSON_STORAGE_KEY, payload);
- Status: updated
- Preflight: 2026-10-20T21:46:37.660272+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Teach Java OOP through interactive robot-building exercises in Next.js and TypeScript, with answer feedback, a lesson timer, and browser-saved progress."`; exact match: True; observed 2026-10-20T21:46:38.902663+00:00

### Kevin-Mok/java-lesson-3

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Teach robot composition and safe Java control flow through a Next.js and TypeScript lesson with timed sections, answer checks, hints, and saved learner progress."`
- Decision: update; Replace missing description with distinct lesson outcomes and supported interface features.
- Length: 161
- Evidence commit: [`cdff9bc6f2f47e3171e75710abe7572e31fc7d3a`](https://github.com/Kevin-Mok/java-lesson-3/commit/cdff9bc6f2f47e3171e75710abe7572e31fc7d3a)
- Evidence: [README.md](https://github.com/Kevin-Mok/java-lesson-3/blob/cdff9bc6f2f47e3171e75710abe7572e31fc7d3a/README.md) — LocalStorage persistence
- Evidence: [package.json](https://github.com/Kevin-Mok/java-lesson-3/blob/cdff9bc6f2f47e3171e75710abe7572e31fc7d3a/package.json) — "next"
- Evidence: [data/lesson.ts](https://github.com/Kevin-Mok/java-lesson-3/blob/cdff9bc6f2f47e3171e75710abe7572e31fc7d3a/data/lesson.ts) — Introduce invariants for battery safety
- Evidence: [components/LessonApp.tsx](https://github.com/Kevin-Mok/java-lesson-3/blob/cdff9bc6f2f47e3171e75710abe7572e31fc7d3a/components/LessonApp.tsx) — checkConcept,
- Status: updated
- Preflight: 2026-10-20T21:46:39.295554+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Teach robot composition and safe Java control flow through a Next.js and TypeScript lesson with timed sections, answer checks, hints, and saved learner progress."`; exact match: True; observed 2026-10-20T21:46:40.524096+00:00

### Kevin-Mok/java-lesson-4

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Teach Java robot modes and sensor-based decisions in a Next.js and TypeScript lesson, with deterministic answer feedback, teacher guides, and browser-saved progress."`
- Decision: update; Replace missing description; describe simulated sensors without implying hardware integration.
- Length: 165
- Evidence commit: [`318e99ac66e8123e19e7996485007811e8610181`](https://github.com/Kevin-Mok/java-lesson-4/commit/318e99ac66e8123e19e7996485007811e8610181)
- Evidence: [README.md](https://github.com/Kevin-Mok/java-lesson-4/blob/318e99ac66e8123e19e7996485007811e8610181/README.md) — TypeScript
- Evidence: [README.md](https://github.com/Kevin-Mok/java-lesson-4/blob/318e99ac66e8123e19e7996485007811e8610181/README.md) — LocalStorage
- Evidence: [components/LessonApp.tsx](https://github.com/Kevin-Mok/java-lesson-4/blob/318e99ac66e8123e19e7996485007811e8610181/components/LessonApp.tsx) — Robot Modes: Sensors, Enums, and Safe Decisions
- Evidence: [components/LessonApp.tsx](https://github.com/Kevin-Mok/java-lesson-4/blob/318e99ac66e8123e19e7996485007811e8610181/components/LessonApp.tsx) — feedback.feedback
- Evidence: [data/lesson.ts](https://github.com/Kevin-Mok/java-lesson-4/blob/318e99ac66e8123e19e7996485007811e8610181/data/lesson.ts) — Today we type a distance number ourselves.
- Status: updated
- Preflight: 2026-10-20T21:46:40.939255+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Teach Java robot modes and sensor-based decisions in a Next.js and TypeScript lesson, with deterministic answer feedback, teacher guides, and browser-saved progress."`; exact match: True; observed 2026-10-20T21:46:41.873357+00:00

### Kevin-Mok/java-lesson-5

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Teach Java arrays and event logs through a Next.js and TypeScript robotics lesson, with guided practice, answer feedback, teacher support, and browser-saved progress."`
- Decision: update; Replace missing description with distinct collections curriculum and supported learning flow.
- Length: 166
- Evidence commit: [`afd5d0cb373c5c4188705be8aae0f772be85a2a5`](https://github.com/Kevin-Mok/java-lesson-5/commit/afd5d0cb373c5c4188705be8aae0f772be85a2a5)
- Evidence: [README.md](https://github.com/Kevin-Mok/java-lesson-5/blob/afd5d0cb373c5c4188705be8aae0f772be85a2a5/README.md) — TypeScript
- Evidence: [README.md](https://github.com/Kevin-Mok/java-lesson-5/blob/afd5d0cb373c5c4188705be8aae0f772be85a2a5/README.md) — LocalStorage
- Evidence: [components/LessonApp.tsx](https://github.com/Kevin-Mok/java-lesson-5/blob/afd5d0cb373c5c4188705be8aae0f772be85a2a5/components/LessonApp.tsx) — Robot Logs: Arrays, Lists, and Safe Steps
- Evidence: [components/LessonApp.tsx](https://github.com/Kevin-Mok/java-lesson-5/blob/afd5d0cb373c5c4188705be8aae0f772be85a2a5/components/LessonApp.tsx) — feedback.feedback
- Evidence: [data/lesson.ts](https://github.com/Kevin-Mok/java-lesson-5/blob/afd5d0cb373c5c4188705be8aae0f772be85a2a5/data/lesson.ts) — private final java.util.ArrayList<String> eventLog
- Status: updated
- Preflight: 2026-10-20T21:46:42.272763+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Teach Java arrays and event logs through a Next.js and TypeScript robotics lesson, with guided practice, answer feedback, teacher support, and browser-saved progress."`; exact match: True; observed 2026-10-20T21:46:43.454199+00:00

### Kevin-Mok/jenkins-test

- Default branch: `master`
- Original JSON: `null`
- Intended JSON: `null`
- Decision: preserve_insufficient; Preserve null: README is only a title; sole Jenkinsfile is a minimal initialization experiment with no build/deploy behavior, insufficient useful project evidence.
- Length: null preserved
- Evidence commit: [`17f2ebfa11560ce7fe9271d2cf62d4a2eb4084a9`](https://github.com/Kevin-Mok/jenkins-test/commit/17f2ebfa11560ce7fe9271d2cf62d4a2eb4084a9)
- Evidence: [README.md](https://github.com/Kevin-Mok/jenkins-test/blob/17f2ebfa11560ce7fe9271d2cf62d4a2eb4084a9/README.md) — # jenkins-test
- Evidence: [Jenkinsfile](https://github.com/Kevin-Mok/jenkins-test/blob/17f2ebfa11560ce7fe9271d2cf62d4a2eb4084a9/Jenkinsfile) — stage('Initialize')
- Evidence: [Jenkinsfile](https://github.com/Kevin-Mok/jenkins-test/blob/17f2ebfa11560ce7fe9271d2cf62d4a2eb4084a9/Jenkinsfile) — cleanWs()
- Status: preserve_insufficient
- Preflight: 2026-10-20T21:46:43.884298+00:00; eligibility True; current-description matched original: True
- PATCH exit: not issued; readback JSON: `null`; exact match: True; observed 2026-10-20T21:46:44.264652+00:00

### Kevin-Mok/Kevin-Mok

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Explore Kevin Mok’s development projects and experience through a GitHub profile README with a Python-generated SVG contribution graph."`
- Decision: update; Describe the actual profile artifact rather than treat listed portfolio technologies as this repository implementation.
- Length: 135
- Evidence commit: [`3888f6db0165f0293d6d7017cb9932e787c377ad`](https://github.com/Kevin-Mok/Kevin-Mok/commit/3888f6db0165f0293d6d7017cb9932e787c377ad)
- Evidence: [README.md](https://github.com/Kevin-Mok/Kevin-Mok/blob/3888f6db0165f0293d6d7017cb9932e787c377ad/README.md) — ### Featured Projects
- Evidence: [scripts/generate_contribution_graph.py](https://github.com/Kevin-Mok/Kevin-Mok/blob/3888f6db0165f0293d6d7017cb9932e787c377ad/scripts/generate_contribution_graph.py) — Generate a local SVG contribution graph from GitHub contribution calendar HTML.
- Status: updated
- Preflight: 2026-10-20T21:46:44.678688+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Explore Kevin Mok’s development projects and experience through a GitHub profile README with a Python-generated SVG contribution graph."`; exact match: True; observed 2026-10-20T21:46:45.672403+00:00

### Kevin-Mok/leetcode

- Default branch: `main`
- Original JSON: `"Technical LeetCode repository focused on data structures, algorithmic patterns, optimization strategies, and clean implementations."`
- Intended JSON: `"Practice data structures and algorithms with executable Python solutions, local example runners, regression checks, and an automatically generated problem index."`
- Decision: update; Replace generic positioning with inspectable Python practice and maintenance features.
- Length: 161
- Evidence commit: [`3d9f68d0d9a1bf915572a6ec52a4beb0568b37d1`](https://github.com/Kevin-Mok/leetcode/commit/3d9f68d0d9a1bf915572a6ec52a4beb0568b37d1)
- Evidence: [README.md](https://github.com/Kevin-Mok/leetcode/blob/3d9f68d0d9a1bf915572a6ec52a4beb0568b37d1/README.md) — executable Python solutions, local verification harnesses
- Evidence: [README.md](https://github.com/Kevin-Mok/leetcode/blob/3d9f68d0d9a1bf915572a6ec52a4beb0568b37d1/README.md) — The README is generated from tracked solution files
- Evidence: [stack/71-simplify-path.py](https://github.com/Kevin-Mok/leetcode/blob/3d9f68d0d9a1bf915572a6ec52a4beb0568b37d1/stack/71-simplify-path.py) — if __name__ == "__main__":
- Evidence: [tests/test_update_readme.py](https://github.com/Kevin-Mok/leetcode/blob/3d9f68d0d9a1bf915572a6ec52a4beb0568b37d1/tests/test_update_readme.py) — class ResolveProblemMetadataTests(unittest.TestCase):
- Status: updated
- Preflight: 2026-10-20T21:46:46.055456+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Practice data structures and algorithms with executable Python solutions, local example runners, regression checks, and an automatically generated problem index."`; exact match: True; observed 2026-10-20T21:46:46.988502+00:00

### Kevin-Mok/linux-config-old

- Default branch: `master`
- Original JSON: `"Personal dotfiles for workflow efficiency and ricing."`
- Intended JSON: `"Customize a Linux workspace with chezmoi-managed dotfiles for fish, i3-gaps, Neovim, and ranger, including machine-specific configuration templates."`
- Decision: update; Explain supported tooling and multi-machine configuration without claiming current active status.
- Length: 148
- Evidence commit: [`82018d00a3054b7938b19f586315da8d88808d40`](https://github.com/Kevin-Mok/linux-config-old/commit/82018d00a3054b7938b19f586315da8d88808d40)
- Evidence: [README.md](https://github.com/Kevin-Mok/linux-config-old/blob/82018d00a3054b7938b19f586315da8d88808d40/README.md) — I use [chezmoi]
- Evidence: [README.md](https://github.com/Kevin-Mok/linux-config-old/blob/82018d00a3054b7938b19f586315da8d88808d40/README.md) — configs for different machines with a single branch.
- Evidence: [README.md](https://github.com/Kevin-Mok/linux-config-old/blob/82018d00a3054b7938b19f586315da8d88808d40/README.md) — **Shell**: [Fish]
- Evidence: [README.md](https://github.com/Kevin-Mok/linux-config-old/blob/82018d00a3054b7938b19f586315da8d88808d40/README.md) — **Window Manager**: [i3-gaps]
- Evidence: [README.md](https://github.com/Kevin-Mok/linux-config-old/blob/82018d00a3054b7938b19f586315da8d88808d40/README.md) — **Editor**: [Neovim]
- Evidence: [README.md](https://github.com/Kevin-Mok/linux-config-old/blob/82018d00a3054b7938b19f586315da8d88808d40/README.md) — **File Manager**: [ranger]
- Status: updated
- Preflight: 2026-10-20T21:46:47.411095+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Customize a Linux workspace with chezmoi-managed dotfiles for fish, i3-gaps, Neovim, and ranger, including machine-specific configuration templates."`; exact match: True; observed 2026-10-20T21:46:48.618159+00:00

### Kevin-Mok/maxfield-academy

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Practice sliding-window algorithms with Python exercise scaffolds that bundle prompts, function stubs, example runners, and built-in edge-case tests without external dependencies."`
- Decision: update; Explicitly distinguish unimplemented student scaffolds from completed solutions.
- Length: 179
- Evidence commit: [`1aa1ba5d61cfb0db64b3de18260742135661902b`](https://github.com/Kevin-Mok/maxfield-academy/commit/1aa1ba5d61cfb0db64b3de18260742135661902b)
- Evidence: [README.md](https://github.com/Kevin-Mok/maxfield-academy/blob/1aa1ba5d61cfb0db64b3de18260742135661902b/README.md) — Single-file problem scaffolds
- Evidence: [README.md](https://github.com/Kevin-Mok/maxfield-academy/blob/1aa1ba5d61cfb0db64b3de18260742135661902b/README.md) — There are no external packages
- Evidence: [sliding-window/2-shortest-study-sprint.py](https://github.com/Kevin-Mok/maxfield-academy/blob/1aa1ba5d61cfb0db64b3de18260742135661902b/sliding-window/2-shortest-study-sprint.py) — raise NotImplementedError(
- Evidence: [sliding-window/2-shortest-study-sprint.py](https://github.com/Kevin-Mok/maxfield-academy/blob/1aa1ba5d61cfb0db64b3de18260742135661902b/sliding-window/2-shortest-study-sprint.py) — EDGE_CASES = [
- Status: updated
- Preflight: 2026-10-20T21:46:48.996639+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Practice sliding-window algorithms with Python exercise scaffolds that bundle prompts, function stubs, example runners, and built-in edge-case tests without external dependencies."`; exact match: True; observed 2026-10-20T21:46:50.230509+00:00

### Kevin-Mok/msg-cap-discord-bot

- Default branch: `main`
- Original JSON: `"Lightweight standalone Discord bot with daily message caps, sticky scoreboards, and slash-command moderation."`
- Intended JSON: `"Manage daily Discord message budgets with a Python and SQLite bot featuring persistent counters, server-isolated caps, sticky scoreboards, and slash-command moderation."`
- Decision: update; Retain existing value while adding supported persistence technology and per-server isolation.
- Length: 168
- Evidence commit: [`6908a934f56e194a7080783d21c602aa6a6eefb3`](https://github.com/Kevin-Mok/msg-cap-discord-bot/commit/6908a934f56e194a7080783d21c602aa6a6eefb3)
- Evidence: [README.md](https://github.com/Kevin-Mok/msg-cap-discord-bot/blob/6908a934f56e194a7080783d21c602aa6a6eefb3/README.md) — Python 3.11+
- Evidence: [README.md](https://github.com/Kevin-Mok/msg-cap-discord-bot/blob/6908a934f56e194a7080783d21c602aa6a6eefb3/README.md) — SQLite
- Evidence: [README.md](https://github.com/Kevin-Mok/msg-cap-discord-bot/blob/6908a934f56e194a7080783d21c602aa6a6eefb3/README.md) — Each server has separate daily counts
- Evidence: [README.md](https://github.com/Kevin-Mok/msg-cap-discord-bot/blob/6908a934f56e194a7080783d21c602aa6a6eefb3/README.md) — sticky scoreboard
- Status: updated
- Preflight: 2026-10-20T21:46:50.667388+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Manage daily Discord message budgets with a Python and SQLite bot featuring persistent counters, server-isolated caps, sticky scoreboards, and slash-command moderation."`; exact match: True; observed 2026-10-20T21:46:51.976880+00:00

### Kevin-Mok/my-site

- Default branch: `master`
- Original JSON: `"My personal site."`
- Intended JSON: `"Explore a personal résumé and Linux projects through a Hugo website with custom templates and a GitLab Pages build pipeline."`
- Decision: update; Replace minimal description with site value and supported static-site/deployment implementation.
- Length: 124
- Evidence commit: [`c58d676c8b9151b51de7a08851add024dd5b2847`](https://github.com/Kevin-Mok/my-site/commit/c58d676c8b9151b51de7a08851add024dd5b2847)
- Evidence: [config.yaml](https://github.com/Kevin-Mok/my-site/blob/c58d676c8b9151b51de7a08851add024dd5b2847/config.yaml) — - name: resume
- Evidence: [config.yaml](https://github.com/Kevin-Mok/my-site/blob/c58d676c8b9151b51de7a08851add024dd5b2847/config.yaml) — - name: config
- Evidence: [.gitlab-ci.yml](https://github.com/Kevin-Mok/my-site/blob/c58d676c8b9151b51de7a08851add024dd5b2847/.gitlab-ci.yml) — - hugo
- Evidence: [layouts/index.html](https://github.com/Kevin-Mok/my-site/blob/c58d676c8b9151b51de7a08851add024dd5b2847/layouts/index.html) — {{ partial "home/about.html" . }}
- Status: updated
- Preflight: 2026-10-20T21:46:52.448130+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Explore a personal résumé and Linux projects through a Hugo website with custom templates and a GitLab Pages build pipeline."`; exact match: True; observed 2026-10-20T21:46:53.848907+00:00

### Kevin-Mok/nextjs-chess-analytics

- Default branch: `main`
- Original JSON: `"Next.js portfolio app that turns Chess.com PGN exports into interactive game replays, filters, and performance insights."`
- Intended JSON: `"Next.js portfolio app that turns Chess.com PGN exports into interactive game replays, filters, and performance insights."`
- Decision: unchanged; Existing concise description accurately matches README, parser, and route design.
- Length: 120
- Evidence commit: [`7a236e9df36ea1d61fc98a5d22a855ddc9ab5227`](https://github.com/Kevin-Mok/nextjs-chess-analytics/commit/7a236e9df36ea1d61fc98a5d22a855ddc9ab5227)
- Evidence: [README.md](https://github.com/Kevin-Mok/nextjs-chess-analytics/blob/7a236e9df36ea1d61fc98a5d22a855ddc9ab5227/README.md) — PGN ingest pipeline that normalizes Chess.com games into derived JSON
- Evidence: [README.md](https://github.com/Kevin-Mok/nextjs-chess-analytics/blob/7a236e9df36ea1d61fc98a5d22a855ddc9ab5227/README.md) — searchable and filterable All Games view
- Evidence: [README.md](https://github.com/Kevin-Mok/nextjs-chess-analytics/blob/7a236e9df36ea1d61fc98a5d22a855ddc9ab5227/README.md) — replay/detail page with move navigation and material balance
- Evidence: [lib/pgn.ts](https://github.com/Kevin-Mok/nextjs-chess-analytics/blob/7a236e9df36ea1d61fc98a5d22a855ddc9ab5227/lib/pgn.ts) — function buildFenTimeline
- Status: unchanged
- Preflight: 2026-10-20T21:46:54.281028+00:00; eligibility True; current-description matched original: True
- PATCH exit: not issued; readback JSON: `"Next.js portfolio app that turns Chess.com PGN exports into interactive game replays, filters, and performance insights."`; exact match: True; observed 2026-10-20T21:46:54.669913+00:00

### Kevin-Mok/nextjs-portfolio-showcase

- Default branch: `main`
- Original JSON: `"Personal portfolio site built with Next.js 15 + TypeScript + Tailwind. Showcases projects, resume variants, and production-minded frontend engineering."`
- Intended JSON: `"Explore projects, MDX articles, and role-specific résumés in a Next.js and TypeScript portfolio with a window-manager-inspired UI and a Resend contact form."`
- Decision: update; Replace vague quality claim with distinctive supported content, UI, and email integration.
- Length: 156
- Evidence commit: [`b51faa92494b2d60bbf5751e1a9c4e7f8068805e`](https://github.com/Kevin-Mok/nextjs-portfolio-showcase/commit/b51faa92494b2d60bbf5751e1a9c4e7f8068805e)
- Evidence: [README.md](https://github.com/Kevin-Mok/nextjs-portfolio-showcase/blob/b51faa92494b2d60bbf5751e1a9c4e7f8068805e/README.md) — Hyprland-inspired desktop UI
- Evidence: [README.md](https://github.com/Kevin-Mok/nextjs-portfolio-showcase/blob/b51faa92494b2d60bbf5751e1a9c4e7f8068805e/README.md) — MDX-backed writing
- Evidence: [README.md](https://github.com/Kevin-Mok/nextjs-portfolio-showcase/blob/b51faa92494b2d60bbf5751e1a9c4e7f8068805e/README.md) — role-specific resume links
- Evidence: [package.json](https://github.com/Kevin-Mok/nextjs-portfolio-showcase/blob/b51faa92494b2d60bbf5751e1a9c4e7f8068805e/package.json) — "typescript"
- Evidence: [app/api/contact/route.ts](https://github.com/Kevin-Mok/nextjs-portfolio-showcase/blob/b51faa92494b2d60bbf5751e1a9c4e7f8068805e/app/api/contact/route.ts) — await resend.emails.send({
- Status: updated
- Preflight: 2026-10-20T21:46:55.145055+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Explore projects, MDX articles, and role-specific résumés in a Next.js and TypeScript portfolio with a window-manager-inspired UI and a Resend contact form."`; exact match: True; observed 2026-10-20T21:46:56.564615+00:00

### Kevin-Mok/nomar-trading-club-membership-site

- Default branch: `main`
- Original JSON: `"Hiring a junior web developer? I freelanced this responsive Next.js + TypeScript project, and I'm actively looking for my first full-time web dev role."`
- Intended JSON: `"Compare trading-education memberships and reach Whop checkout through a responsive Next.js and TypeScript site with tiered pricing and dynamic social previews."`
- Decision: update; Remove hiring plea; describe hosted checkout links accurately without claiming local payment processing or Discord automation.
- Length: 159
- Evidence commit: [`b019cb8770f7ee06d404f342edece20b57412541`](https://github.com/Kevin-Mok/nomar-trading-club-membership-site/commit/b019cb8770f7ee06d404f342edece20b57412541)
- Evidence: [README.md](https://github.com/Kevin-Mok/nomar-trading-club-membership-site/blob/b019cb8770f7ee06d404f342edece20b57412541/README.md) — Dynamic OG Images
- Evidence: [package.json](https://github.com/Kevin-Mok/nomar-trading-club-membership-site/blob/b019cb8770f7ee06d404f342edece20b57412541/package.json) — "next": "^16.1.4"
- Evidence: [package.json](https://github.com/Kevin-Mok/nomar-trading-club-membership-site/blob/b019cb8770f7ee06d404f342edece20b57412541/package.json) — "typescript": "^5.3.0"
- Evidence: [components/Pricing.tsx](https://github.com/Kevin-Mok/nomar-trading-club-membership-site/blob/b019cb8770f7ee06d404f342edece20b57412541/components/Pricing.tsx) — return links.whopBasic;
- Evidence: [components/Pricing.tsx](https://github.com/Kevin-Mok/nomar-trading-club-membership-site/blob/b019cb8770f7ee06d404f342edece20b57412541/components/Pricing.tsx) — grid md:grid-cols-3 gap-8
- Status: updated
- Preflight: 2026-10-20T21:46:57.168484+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Compare trading-education memberships and reach Whop checkout through a responsive Next.js and TypeScript site with tiered pricing and dynamic social previews."`; exact match: True; observed 2026-10-20T21:46:58.220760+00:00

### Kevin-Mok/online-ping-cog

- Default branch: `main`
- Original JSON: `"Red cog for pinging when someone goes online."`
- Intended JSON: `"Get Discord presence alerts with a Python Red Bot cog that supports per-server tracking, configurable channels, status filters, and cooldowns."`
- Decision: update; Replace terse description with verified user controls and Python framework.
- Length: 142
- Evidence commit: [`3c991c0dc087e59c8051b26bfd8ab223a0cca740`](https://github.com/Kevin-Mok/online-ping-cog/commit/3c991c0dc087e59c8051b26bfd8ab223a0cca740)
- Evidence: [onlineping/onlineping.py](https://github.com/Kevin-Mok/online-ping-cog/blob/3c991c0dc087e59c8051b26bfd8ab223a0cca740/onlineping/onlineping.py) — from redbot.core import commands, Config, checks
- Evidence: [onlineping/onlineping.py](https://github.com/Kevin-Mok/online-ping-cog/blob/3c991c0dc087e59c8051b26bfd8ab223a0cca740/onlineping/onlineping.py) — self.config.register_guild(targets={}, mode="online_only", prefs={}, cooldown=300)
- Evidence: [README.md](https://github.com/Kevin-Mok/online-ping-cog/blob/3c991c0dc087e59c8051b26bfd8ab223a0cca740/README.md) — Monitor when members come online
- Status: updated
- Preflight: 2026-10-20T21:46:58.635671+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Get Discord presence alerts with a Python Red Bot cog that supports per-server tracking, configurable channels, status filters, and cooldowns."`; exact match: True; observed 2026-10-20T21:46:59.829603+00:00

### Kevin-Mok/openclaw

- Default branch: `main`
- Original JSON: `"End-to-end job application workflow POC with email ingestion, lead scoring, review-thread orchestration, and AI-assisted draft generation in TypeScript. "`
- Intended JSON: `"Review job leads and draft application packets with a fixture-first TypeScript POC using SQLite, lead deduplication, résumé matching, and Discord review plans."`
- Decision: update; Clarify fixture-first maturity and implemented review plans; avoid implying live end-to-end channel deployment.
- Length: 159
- Evidence commit: [`9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba`](https://github.com/Kevin-Mok/openclaw/commit/9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba)
- Evidence: [README.md](https://github.com/Kevin-Mok/openclaw/blob/9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba/README.md) — The POC is intentionally fixture-first.
- Evidence: [README.md](https://github.com/Kevin-Mok/openclaw/blob/9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba/README.md) — normalize and dedupe leads
- Evidence: [README.md](https://github.com/Kevin-Mok/openclaw/blob/9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba/README.md) — choose a resume lane
- Evidence: [src/cli.ts](https://github.com/Kevin-Mok/openclaw/blob/9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba/src/cli.ts) — data/job-ops.sqlite
- Evidence: [src/cli.ts](https://github.com/Kevin-Mok/openclaw/blob/9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba/src/cli.ts) — const board = buildReviewBoard
- Evidence: [package.json](https://github.com/Kevin-Mok/openclaw/blob/9fd443bfbbc1d0b6b2c732a193aa5c49f98008ba/package.json) — "typescript"
- Status: updated
- Preflight: 2026-10-20T21:47:00.329595+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Review job leads and draft application packets with a fixture-first TypeScript POC using SQLite, lead deduplication, résumé matching, and Discord review plans."`; exact match: True; observed 2026-10-20T21:47:01.599319+00:00

### Kevin-Mok/ParsaFood

- Default branch: `master`
- Original JSON: `"Android app to scan ingredients for allergens."`
- Intended JSON: `"Scan ingredient labels for potential allergen and dietary conflicts in an Android hackathon prototype built with Java and Google Mobile Vision OCR."`
- Decision: update; State prototype maturity and potential conflicts; avoid implying clinically reliable allergy detection.
- Length: 147
- Evidence commit: [`3e72898bac3554455984eaf0f0d86e5c2ddd8a83`](https://github.com/Kevin-Mok/ParsaFood/commit/3e72898bac3554455984eaf0f0d86e5c2ddd8a83)
- Evidence: [README.md](https://github.com/Kevin-Mok/ParsaFood/blob/3e72898bac3554455984eaf0f0d86e5c2ddd8a83/README.md) — developed at the Platterz Hackathon
- Evidence: [ocr-reader/app/build.gradle](https://github.com/Kevin-Mok/ParsaFood/blob/3e72898bac3554455984eaf0f0d86e5c2ddd8a83/ocr-reader/app/build.gradle) — com.google.android.gms:play-services-vision:11.0.4
- Evidence: [ocr-reader/app/src/main/java/com/google/android/gms/samples/vision/ocrreader/AfterCaptureActivity.java](https://github.com/Kevin-Mok/ParsaFood/blob/3e72898bac3554455984eaf0f0d86e5c2ddd8a83/ocr-reader/app/src/main/java/com/google/android/gms/samples/vision/ocrreader/AfterCaptureActivity.java) — parser.checkAllergens(itemList)
- Evidence: [ocr-reader/app/src/main/java/com/google/android/gms/samples/vision/ocrreader/TextParser.java](https://github.com/Kevin-Mok/ParsaFood/blob/3e72898bac3554455984eaf0f0d86e5c2ddd8a83/ocr-reader/app/src/main/java/com/google/android/gms/samples/vision/ocrreader/TextParser.java) — public class TextParser
- Status: updated
- Preflight: 2026-10-20T21:47:02.029789+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Scan ingredient labels for potential allergen and dietary conflicts in an Android hackathon prototype built with Java and Google Mobile Vision OCR."`; exact match: True; observed 2026-10-20T21:47:03.009693+00:00

### Kevin-Mok/python-count

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Learn Python string counting with guided lessons, CCC Junior practice, and exact-output checks in a Next.js/TypeScript classroom app running Python in-browser with Pyodide."`
- Decision: update; Explains the teaching workflow and browser execution without backend/security claims.
- Length: 172
- Evidence commit: [`33bc0b6b407de25269b392cdf44cd01c112e146b`](https://github.com/Kevin-Mok/python-count/commit/33bc0b6b407de25269b392cdf44cd01c112e146b)
- Evidence: [README.md](https://github.com/Kevin-Mok/python-count/blob/33bc0b6b407de25269b392cdf44cd01c112e146b/README.md) — Python String Counting Practice is a frontend-only learning site for young beginner Python students learning string traversal, manual counting, `.count(...)`, and two CCC Junior string problems. It starts with `S = input()`, moves through `for letter in S`, counters, and exact character comparisons, then finishes with CCC 2015 J2 Happy or Sad and CCC 2013 J2 Rotating Letters.
- Evidence: [package.json](https://github.com/Kevin-Mok/python-count/blob/33bc0b6b407de25269b392cdf44cd01c112e146b/package.json) — "next": "^16.2.6",     "react": "^18.3.1",     "react-dom": "^18.3.1",     "typescript": "^5.8.3"
- Evidence: [public/pyodide-worker.mjs](https://github.com/Kevin-Mok/python-count/blob/33bc0b6b407de25269b392cdf44cd01c112e146b/public/pyodide-worker.mjs) — await pyodide.runPythonAsync(String(code ?? ""));
- Status: updated
- Preflight: 2026-10-20T21:47:03.440462+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Learn Python string counting with guided lessons, CCC Junior practice, and exact-output checks in a Next.js/TypeScript classroom app running Python in-browser with Pyodide."`; exact match: True; observed 2026-10-20T21:47:04.396149+00:00

### Kevin-Mok/random-color-generator

- Default branch: `master`
- Original JSON: `"Previews a random color on click."`
- Intended JSON: `"Find color inspiration in a JavaScript web tool with random colors, approximate names, hex codes, and navigable color history."`
- Decision: update; Adds supported interaction details to the generic original.
- Length: 126
- Evidence commit: [`599e086022f9bf4d93cfa176a331502cd4091254`](https://github.com/Kevin-Mok/random-color-generator/commit/599e086022f9bf4d93cfa176a331502cd4091254)
- Evidence: [README.md](https://github.com/Kevin-Mok/random-color-generator/blob/599e086022f9bf4d93cfa176a331502cd4091254/README.md) — A simple, elegant web tool for generating random colors on click. Features color name approximation using ntc.js, history navigation, and a clean responsive interface. Great for designers seeking color inspiration.
- Evidence: [js/index.js](https://github.com/Kevin-Mok/random-color-generator/blob/599e086022f9bf4d93cfa176a331502cd4091254/js/index.js) — function getCurrentColorName() {     return ntc.name(getCurrentColor())[1]; }
- Evidence: [js/index.js](https://github.com/Kevin-Mok/random-color-generator/blob/599e086022f9bf4d93cfa176a331502cd4091254/js/index.js) — $("#dir-button-left").on("click", applyPrevColor);     $("#dir-button-right").on("click", applyNextColor);
- Evidence: [js/index.js](https://github.com/Kevin-Mok/random-color-generator/blob/599e086022f9bf4d93cfa176a331502cd4091254/js/index.js) — $("#color-name").html(getCurrentColor());
- Status: updated
- Preflight: 2026-10-20T21:47:04.808177+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Find color inspiration in a JavaScript web tool with random colors, approximate names, hex codes, and navigable color history."`; exact match: True; observed 2026-10-20T21:47:05.788743+00:00

### Kevin-Mok/rarity-surf

- Default branch: `django`
- Original JSON: `"Rare NFT deal finder used to frontrun other competing buyers of top 0.5% of rare NFT's. [Django/React]"`
- Intended JSON: `"Explore NFT rarity and marketplace listings with a Django backend combining trait-based ranking, GraphQL queries, and OpenSea data integration."`
- Decision: update; Replaces unsupported competitive performance wording with implemented data/API capabilities.
- Length: 143
- Evidence commit: [`2d804e045cf897db06da9c7640fb6af9bb9c0b89`](https://github.com/Kevin-Mok/rarity-surf/commit/2d804e045cf897db06da9c7640fb6af9bb9c0b89)
- Evidence: [requirements.txt](https://github.com/Kevin-Mok/rarity-surf/blob/2d804e045cf897db06da9c7640fb6af9bb9c0b89/requirements.txt) — Django==3.2.8
- Evidence: [rarity_check/project/main.py](https://github.com/Kevin-Mok/rarity-surf/blob/2d804e045cf897db06da9c7640fb6af9bb9c0b89/rarity_check/project/main.py) — scores = rarity.calcTraitScores(master_json, trait_counts)     cache.cache_json(scores, constants.SCORES_FILE)      ranks = rarity.calcAllTokenScores(master_json)     cache.cache_json(ranks, constants.RANKS_FILE)
- Evidence: [rarity_check/rarity_check/schema.py](https://github.com/Kevin-Mok/rarity-surf/blob/2d804e045cf897db06da9c7640fb6af9bb9c0b89/rarity_check/rarity_check/schema.py) — token_by_number = graphene.Field(TokenType,             proj_slug=graphene.String(required=True),             number=graphene.Int(required=True))
- Evidence: [rarity_check/project/opensea.py](https://github.com/Kevin-Mok/rarity-surf/blob/2d804e045cf897db06da9c7640fb6af9bb9c0b89/rarity_check/project/opensea.py) — OS_API = "https://api.opensea.io/api/v1" ASSETS_API = f"{OS_API}/assets" EVENTS_API = f"{OS_API}/events"
- Status: updated
- Preflight: 2026-10-20T21:47:06.246938+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Explore NFT rarity and marketplace listings with a Django backend combining trait-based ranking, GraphQL queries, and OpenSea data integration."`; exact match: True; observed 2026-10-20T21:47:07.219393+00:00

### Kevin-Mok/rarity-surf-frontend

- Default branch: `main`
- Original JSON: `"Frontend to my rarity-surf project."`
- Intended JSON: `"Look up NFT rarity ranks, trait scores, and images in a React and Tailwind interface backed by Rarity Surf’s GraphQL API."`
- Decision: update; Uses actual lookup implementation rather than README claims of React 18, REST, or live marketplace filtering.
- Length: 121
- Evidence commit: [`788fac5ab4bc5bc9bcea137b3cc725977e5409b4`](https://github.com/Kevin-Mok/rarity-surf-frontend/commit/788fac5ab4bc5bc9bcea137b3cc725977e5409b4)
- Evidence: [src/App.js](https://github.com/Kevin-Mok/rarity-surf-frontend/blob/788fac5ab4bc5bc9bcea137b3cc725977e5409b4/src/App.js) — tokenByNumber(projSlug: "${projSlug}", number: ${number}) {         tokenType {           name         }         number         imageUrl         rank         traits {           traitType {             name           }           name           rarity           score         }         score       }
- Evidence: [package.json](https://github.com/Kevin-Mok/rarity-surf-frontend/blob/788fac5ab4bc5bc9bcea137b3cc725977e5409b4/package.json) — "react": "^17.0.2"
- Evidence: [package.json](https://github.com/Kevin-Mok/rarity-surf-frontend/blob/788fac5ab4bc5bc9bcea137b3cc725977e5409b4/package.json) — "tailwindcss": "npm:@tailwindcss/postcss7-compat"
- Status: updated
- Preflight: 2026-10-20T21:47:07.599458+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Look up NFT rarity ranks, trait scores, and images in a React and Tailwind interface backed by Rarity Surf’s GraphQL API."`; exact match: True; observed 2026-10-20T21:47:08.585586+00:00

### Kevin-Mok/scrape-weather-network

- Default branch: `main`
- Original JSON: `"Validated hourly forecasts from The Weather Network for Scarborough, Toronto. Browser scraping, a public JSON feed, and automatic refreshes every 30 minutes."`
- Intended JSON: `"Validated hourly forecasts from The Weather Network for Scarborough, Toronto. Browser scraping, a public JSON feed, and automatic refreshes every 30 minutes."`
- Decision: preserve_insufficient; Empty repository: collector observed HTTP 409 on default-branch commit request; no README or source available to justify replacement.
- Length: 157
- Status: preserve_insufficient
- Preflight: 2026-10-20T21:47:08.993741+00:00; eligibility True; current-description matched original: True
- PATCH exit: not issued; readback JSON: `"Validated hourly forecasts from The Weather Network for Scarborough, Toronto. Browser scraping, a public JSON feed, and automatic refreshes every 30 minutes."`; exact match: True; observed 2026-10-20T21:47:09.369296+00:00

### Kevin-Mok/self-hosted-infra-hardening

- Default branch: `main`
- Original JSON: `"Sanitized production configs and incident-driven hardening for a self-hosted Ubuntu VPS running Nginx, Gitea, systemd services, Docker Compose and public-facing domains."`
- Intended JSON: `"Sanitized production configs and incident-driven hardening for a self-hosted Ubuntu VPS running Nginx, Gitea, systemd services, Docker Compose and public-facing domains."`
- Decision: unchanged; Existing description accurately summarizes documented sanitized service configs and incidents.
- Length: 169
- Evidence commit: [`8dc40e32c567b498d3db5e3ea177fc0595b17a83`](https://github.com/Kevin-Mok/self-hosted-infra-hardening/commit/8dc40e32c567b498d3db5e3ea177fc0595b17a83)
- Evidence: [README.md](https://github.com/Kevin-Mok/self-hosted-infra-hardening/blob/8dc40e32c567b498d3db5e3ea177fc0595b17a83/README.md) — This repo documents the live service layout and operational fixes for my personal VPS. It is meant to show real infrastructure work rather than tutorial-only examples: reverse proxying, TLS termination, systemd-managed services, Docker Compose deployment, and incident response for publicly reachable domains.
- Evidence: [README.md](https://github.com/Kevin-Mok/self-hosted-infra-hardening/blob/8dc40e32c567b498d3db5e3ea177fc0595b17a83/README.md) — Files in this repo are sanitized production snapshots, not blind copy-paste deployment artifacts.
- Evidence: [configs/systemd/gitea.service](https://github.com/Kevin-Mok/self-hosted-infra-hardening/blob/8dc40e32c567b498d3db5e3ea177fc0595b17a83/configs/systemd/gitea.service) — ExecStart=/usr/local/bin/gitea -c /etc/gitea/app.ini -w /var/lib/gitea web  Restart=always RestartSec=2s
- Evidence: [configs/docker/zoo-blog/docker-compose.yml](https://github.com/Kevin-Mok/self-hosted-infra-hardening/blob/8dc40e32c567b498d3db5e3ea177fc0595b17a83/configs/docker/zoo-blog/docker-compose.yml) — # Sanitized snapshot of /home/example/zoo-blog/docker-compose.yml # Secret-bearing values are replaced with placeholders for documentation.  services:   postgres:     image: postgres:16-alpine     environment:       POSTGRES_DB: zoo_blog       POSTGRES
- Status: unchanged
- Preflight: 2026-10-20T21:47:09.813308+00:00; eligibility True; current-description matched original: True
- PATCH exit: not issued; readback JSON: `"Sanitized production configs and incident-driven hardening for a self-hosted Ubuntu VPS running Nginx, Gitea, systemd services, Docker Compose and public-facing domains."`; exact match: True; observed 2026-10-20T21:47:10.214592+00:00

### Kevin-Mok/simple-java-app

- Default branch: `master`
- Original JSON: `null`
- Intended JSON: `"Learn Java build and test fundamentals with a minimal Hello World app, Maven packaging, and JUnit tests."`
- Decision: update; Describes the small exercise honestly and omits unverified CI/CD readiness.
- Length: 104
- Evidence commit: [`cf2d37b058dbcfcb22f0b8a1472eaf1247e4ef2d`](https://github.com/Kevin-Mok/simple-java-app/commit/cf2d37b058dbcfcb22f0b8a1472eaf1247e4ef2d)
- Evidence: [src/main/java/com/mycompany/app/App.java](https://github.com/Kevin-Mok/simple-java-app/blob/cf2d37b058dbcfcb22f0b8a1472eaf1247e4ef2d/src/main/java/com/mycompany/app/App.java) — private static final String MESSAGE = "Hello World!";
- Evidence: [pom.xml](https://github.com/Kevin-Mok/simple-java-app/blob/cf2d37b058dbcfcb22f0b8a1472eaf1247e4ef2d/pom.xml) — <artifactId>junit-jupiter-api</artifactId>
- Evidence: [pom.xml](https://github.com/Kevin-Mok/simple-java-app/blob/cf2d37b058dbcfcb22f0b8a1472eaf1247e4ef2d/pom.xml) — <!-- Build an executable JAR -->         <groupId>org.apache.maven.plugins</groupId>         <artifactId>maven-jar-plugin</artifactId>
- Status: updated
- Preflight: 2026-10-20T21:47:10.616541+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Learn Java build and test fundamentals with a minimal Hello World app, Maven packaging, and JUnit tests."`; exact match: True; observed 2026-10-20T21:47:11.557643+00:00

### Kevin-Mok/sliding-window

- Default branch: `main`
- Original JSON: `null`
- Intended JSON: `"Teach sliding-window algorithms with a Next.js/TypeScript lesson deck combining student activities, step-by-step traces, presenter notes, and shareable slide links."`
- Decision: update; Captures classroom value and verified deck modes without implying automatic cross-device synchronization.
- Length: 164
- Evidence commit: [`7b88ba0abc82fbbbc6ad0c57634cf30410025f87`](https://github.com/Kevin-Mok/sliding-window/commit/7b88ba0abc82fbbbc6ad0c57634cf30410025f87)
- Evidence: [README.md](https://github.com/Kevin-Mok/sliding-window/blob/7b88ba0abc82fbbbc6ad0c57634cf30410025f87/README.md) — supports direct slide sharing through the `?slide=` URL parameter
- Evidence: [README.md](https://github.com/Kevin-Mok/sliding-window/blob/7b88ba0abc82fbbbc6ad0c57634cf30410025f87/README.md) — problem slides keep the statement, sample I/O, trace, code, checkpoints, and common mistakes visible throughout the workshop
- Evidence: [components/LessonFlowDeck.tsx](https://github.com/Kevin-Mok/sliding-window/blob/7b88ba0abc82fbbbc6ad0c57634cf30410025f87/components/LessonFlowDeck.tsx) — type AudienceMode = "presenter" | "student";
- Evidence: [package.json](https://github.com/Kevin-Mok/sliding-window/blob/7b88ba0abc82fbbbc6ad0c57634cf30410025f87/package.json) — "next": "^14.2.7",     "react": "^18.3.1",     "react-dom": "^18.3.1",     "typescript": "^5.8.3"
- Status: updated
- Preflight: 2026-10-20T21:47:11.950623+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Teach sliding-window algorithms with a Next.js/TypeScript lesson deck combining student activities, step-by-step traces, presenter notes, and shareable slide links."`; exact match: True; observed 2026-10-20T21:47:13.142442+00:00

### Kevin-Mok/spotify-library-intelligence-dashboard

- Default branch: `master`
- Original JSON: `"Full-stack Spotify analytics app with OAuth2 auth, PostgreSQL storage, and rich D3 visualizations."`
- Intended JSON: `"Explore your Spotify library through D3 artist, genre, and audio-feature charts in a Django app with OAuth2 login and PostgreSQL storage."`
- Decision: update; Leads with listening-library analysis and names the supported stack without a security/production claim.
- Length: 137
- Evidence commit: [`44849406f6896411bab76331209730f32fb83f16`](https://github.com/Kevin-Mok/spotify-library-intelligence-dashboard/commit/44849406f6896411bab76331209730f32fb83f16)
- Evidence: [README.md](https://github.com/Kevin-Mok/spotify-library-intelligence-dashboard/blob/44849406f6896411bab76331209730f32fb83f16/README.md) — A full-stack web application that visualizes and analyzes your Spotify music library with interactive D3.js charts. Discover insights about your listening habits through artist distribution, genre breakdowns, and audio feature analysis.
- Evidence: [login/views.py](https://github.com/Kevin-Mok/spotify-library-intelligence-dashboard/blob/44849406f6896411bab76331209730f32fb83f16/login/views.py) — 'grant_type': 'authorization_code'
- Evidence: [graphs/static/graphs/scripts/artist_graph.js](https://github.com/Kevin-Mok/spotify-library-intelligence-dashboard/blob/44849406f6896411bab76331209730f32fb83f16/graphs/static/graphs/scripts/artist_graph.js) — const root = d3.pack()//{{{     .size([width - 2, height - 2])     .padding(3)     (d3.hierarchy(artistData)       .sum(d => d.num_songs))
- Evidence: [spotifyvis/settings.py](https://github.com/Kevin-Mok/spotify-library-intelligence-dashboard/blob/44849406f6896411bab76331209730f32fb83f16/spotifyvis/settings.py) — 'ENGINE': 'django.db.backends.postgresql_psycopg2'
- Status: updated
- Preflight: 2026-10-20T21:47:13.575319+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Explore your Spotify library through D3 artist, genre, and audio-feature charts in a Django app with OAuth2 login and PostgreSQL storage."`; exact match: True; observed 2026-10-20T21:47:14.509077+00:00

### Kevin-Mok/SuperADABros

- Default branch: `master`
- Original JSON: `"Super Mario Bros if Mario couldn't jump, with head tracking controls."`
- Intended JSON: `"Play a Mario-inspired Godot game that replaces jumping with ramps and supports mouse and head-tracking controls."`
- Decision: update; Highlights the gameplay/input design without claiming verified accessibility for all users.
- Length: 112
- Evidence commit: [`7e7d1b7b534a5e82ca9f165b770c04d927fd8d6b`](https://github.com/Kevin-Mok/SuperADABros/commit/7e7d1b7b534a5e82ca9f165b770c04d927fd8d6b)
- Evidence: [README.md](https://github.com/Kevin-Mok/SuperADABros/blob/7e7d1b7b534a5e82ca9f165b770c04d927fd8d6b/README.md) — **Mario can't jump** - instead, the game uses ramps and lifts to navigate terrain, making it playable for wheelchair users and others facing jumping challenges.
- Evidence: [scripts/Mario.gd](https://github.com/Kevin-Mok/SuperADABros/blob/7e7d1b7b534a5e82ca9f165b770c04d927fd8d6b/scripts/Mario.gd) — extends KinematicBody2D
- Evidence: [scripts/Mario.gd](https://github.com/Kevin-Mok/SuperADABros/blob/7e7d1b7b534a5e82ca9f165b770c04d927fd8d6b/scripts/Mario.gd) — func get_mouse_direction():# {{{ 	cur_mouse_point = Global.view.get_mouse_position() * Global.TEST_WINDOW_SCALE 	if cur_mouse_point.x < Global.TEST_MOVE_LEFT_LINE_X: 		return Vector2(-1,0) 	elif cur_mouse_point.x > Global.TEST_MOVE_RIGHT_LINE_X: 		return Vector2(1,0) 	else: 		return Vector2(0,0)
- Evidence: [scripts/MoveWithHead.gd](https://github.com/Kevin-Mok/SuperADABros/blob/7e7d1b7b534a5e82ca9f165b770c04d927fd8d6b/scripts/MoveWithHead.gd) — Input.warp_mouse_position(mouse_point_set)
- Status: updated
- Preflight: 2026-10-20T21:47:15.010185+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Play a Mario-inspired Godot game that replaces jumping with ramps and supports mouse and head-tracking controls."`; exact match: True; observed 2026-10-20T21:47:16.003445+00:00

### Kevin-Mok/SuperADABros-HTML

- Default branch: `master`
- Original JSON: `"HTML version of my Super ADA Bros game."`
- Intended JSON: `"Play Super ADA Bros in the browser with this Godot HTML5/WebAssembly export of a Mario-inspired game that uses ramps instead of jumping."`
- Decision: update; Explains the playable export and relation to the source game.
- Length: 136
- Evidence commit: [`e4294531e9732695d995e021f721e6c2e1259959`](https://github.com/Kevin-Mok/SuperADABros-HTML/commit/e4294531e9732695d995e021f721e6c2e1259959)
- Evidence: [README.md](https://github.com/Kevin-Mok/SuperADABros-HTML/blob/e4294531e9732695d995e021f721e6c2e1259959/README.md) — The WebAssembly/HTML5 export of [Super ADA Bros](https://github.com/Kevin-Mok/SuperADABros) - an accessible, wheelchair-friendly reimagining of Super Mario Bros designed for players with mobility disabilities.
- Evidence: [README.md](https://github.com/Kevin-Mok/SuperADABros-HTML/blob/e4294531e9732695d995e021f721e6c2e1259959/README.md) — **Mario can't jump**. Instead, the game uses ramps and lifts to navigate terrain, making it playable for wheelchair users and others facing jumping challenges.
- Evidence: [index.html](https://github.com/Kevin-Mok/SuperADABros-HTML/blob/e4294531e9732695d995e021f721e6c2e1259959/index.html) — const MAIN_PACK = 'ada-mario.pck';
- Status: updated
- Preflight: 2026-10-20T21:47:16.436613+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Play Super ADA Bros in the browser with this Godot HTML5/WebAssembly export of a Mario-inspired game that uses ramps instead of jumping."`; exact match: True; observed 2026-10-20T21:47:17.387482+00:00

### Kevin-Mok/terraform-deploys

- Default branch: `main`
- Original JSON: `"Deployments of an AWS EC2 instance and Docker containers."`
- Intended JSON: `"Provision an AWS EC2 instance and photo-gallery or secret-sharing containers with Terraform configurations for Docker ports, persistent volumes, and instance outputs."`
- Decision: update; Connects concrete infrastructure resources to their services without claiming production readiness.
- Length: 166
- Evidence commit: [`7a28e90007c514cbe7a9e6653f04ee951050d4a5`](https://github.com/Kevin-Mok/terraform-deploys/commit/7a28e90007c514cbe7a9e6653f04ee951050d4a5)
- Evidence: [aws/main.tf](https://github.com/Kevin-Mok/terraform-deploys/blob/7a28e90007c514cbe7a9e6653f04ee951050d4a5/aws/main.tf) — resource "aws_instance" "app_server" {   ami           = "ami-08d70e59c07c61a3a"   instance_type = "t2.micro"    tags = {     Name = var.instance_name
- Evidence: [docker/main.tf](https://github.com/Kevin-Mok/terraform-deploys/blob/7a28e90007c514cbe7a9e6653f04ee951050d4a5/docker/main.tf) — name         = "bpatrik/pigallery2"
- Evidence: [docker/main.tf](https://github.com/Kevin-Mok/terraform-deploys/blob/7a28e90007c514cbe7a9e6653f04ee951050d4a5/docker/main.tf) — name         = "hemmeligapp/hemmelig"
- Evidence: [docker/main.tf](https://github.com/Kevin-Mok/terraform-deploys/blob/7a28e90007c514cbe7a9e6653f04ee951050d4a5/docker/main.tf) — container_path  = "/app/data/images"     read_only = true
- Evidence: [aws/outputs.tf](https://github.com/Kevin-Mok/terraform-deploys/blob/7a28e90007c514cbe7a9e6653f04ee951050d4a5/aws/outputs.tf) — output "instance_id" {   description = "ID of the EC2 instance"   value       = aws_instance.app_server.id }
- Status: updated
- Preflight: 2026-10-20T21:47:17.802846+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Provision an AWS EC2 instance and photo-gallery or secret-sharing containers with Terraform configurations for Docker ports, persistent volumes, and instance outputs."`; exact match: True; observed 2026-10-20T21:47:18.771213+00:00

### Kevin-Mok/thread-synchronization

- Default branch: `master`
- Original JSON: `"Use of mutex locks for thread synchronization. [C]"`
- Intended JSON: `"Study concurrent traffic simulation in a C/POSIX threads coursework project using mutexes and condition variables to coordinate cars at intersections."`
- Decision: update; Makes the educational scope explicit and avoids unproven collision/deadlock guarantees.
- Length: 150
- Evidence commit: [`1df55255e49c5e33439c1acc300bd2e2dd22e842`](https://github.com/Kevin-Mok/thread-synchronization/commit/1df55255e49c5e33439c1acc300bd2e2dd22e842)
- Evidence: [README.md](https://github.com/Kevin-Mok/thread-synchronization/blob/1df55255e49c5e33439c1acc300bd2e2dd22e842/README.md) — Developed for CSC369 (Operating Systems) at University of Toronto, demonstrating practical application of OS concepts in thread synchronization.
- Evidence: [a2/safeStopSign.c](https://github.com/Kevin-Mok/thread-synchronization/blob/1df55255e49c5e33439c1acc300bd2e2dd22e842/a2/safeStopSign.c) — sign->quadrants_mutex = (pthread_mutex_t)PTHREAD_MUTEX_INITIALIZER; 	sign->quadrants_turn = (pthread_cond_t)PTHREAD_COND_INITIALIZER;
- Evidence: [a2/safeStopSign.c](https://github.com/Kevin-Mok/thread-synchronization/blob/1df55255e49c5e33439c1acc300bd2e2dd22e842/a2/safeStopSign.c) — pthread_mutex_lock(&sign->lane_mutex[lane_index]);
- Status: updated
- Preflight: 2026-10-20T21:47:19.160552+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Study concurrent traffic simulation in a C/POSIX threads coursework project using mutexes and condition variables to coordinate cars at intersections."`; exact match: True; observed 2026-10-20T21:47:20.368483+00:00

### Kevin-Mok/toronto-zoo-blog

- Default branch: `main`
- Original JSON: `"Production-grade full-stack newsroom for Toronto Zoo reporting, built with Next.js, Directus, Prisma, and automated VPS deployment."`
- Intended JSON: `"Publish Toronto Zoo reporting with a Next.js newsroom combining Directus editorial content, Prisma/PostgreSQL storage, RSS, and Docker Compose deployment."`
- Decision: update; Replaces unsupported production-grade language with verifiable content and deployment features.
- Length: 154
- Evidence commit: [`bdc8df4c3df3264a501af2e7951f23ef67975a06`](https://github.com/Kevin-Mok/toronto-zoo-blog/commit/bdc8df4c3df3264a501af2e7951f23ef67975a06)
- Evidence: [README.md](https://github.com/Kevin-Mok/toronto-zoo-blog/blob/bdc8df4c3df3264a501af2e7951f23ef67975a06/README.md) — The app pairs SSR-first Next.js routes with typed content fetching, Directus-backed editorial data, Prisma operational writes, and an ops path that can run locally in Docker or ship to a small Ubuntu VPS.
- Evidence: [README.md](https://github.com/Kevin-Mok/toronto-zoo-blog/blob/bdc8df4c3df3264a501af2e7951f23ef67975a06/README.md) — `/rss.xml` RSS feed
- Evidence: [package.json](https://github.com/Kevin-Mok/toronto-zoo-blog/blob/bdc8df4c3df3264a501af2e7951f23ef67975a06/package.json) — "@directus/sdk": "^16.1.0",     "@prisma/client": "^6.4.1",     "next": "15.5.9"
- Evidence: [docker-compose.yml](https://github.com/Kevin-Mok/toronto-zoo-blog/blob/bdc8df4c3df3264a501af2e7951f23ef67975a06/docker-compose.yml) — image: postgres:16-alpine
- Evidence: [docker-compose.yml](https://github.com/Kevin-Mok/toronto-zoo-blog/blob/bdc8df4c3df3264a501af2e7951f23ef67975a06/docker-compose.yml) — web:     build:       context: .       dockerfile: Dockerfile
- Status: updated
- Preflight: 2026-10-20T21:47:20.809083+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Publish Toronto Zoo reporting with a Next.js newsroom combining Directus editorial content, Prisma/PostgreSQL storage, RSS, and Docker Compose deployment."`; exact match: True; observed 2026-10-20T21:47:22.048010+00:00

### Kevin-Mok/track-codex-sessions

- Default branch: `main`
- Original JSON: `"Read-only Codex working-time tracking, model usage reports, and allowance burn estimates for Linux."`
- Intended JSON: `"Understand Codex work and usage with a local Python CLI for session time, model/token reports, allowance burn estimates, and searchable session resumption."`
- Decision: update; Adds concrete user purpose, implementation language and existing resume capability.
- Length: 155
- Evidence commit: [`3d8511e3ad7c9ff3336798cde5bb69a58c3360f7`](https://github.com/Kevin-Mok/track-codex-sessions/commit/3d8511e3ad7c9ff3336798cde5bb69a58c3360f7)
- Evidence: [README.md](https://github.com/Kevin-Mok/track-codex-sessions/blob/3d8511e3ad7c9ff3336798cde5bb69a58c3360f7/README.md) — Codex Time is a local time tracker for developers running Codex across projects, models and reasoning levels. It turns session history into a clear picture of how long Codex worked, which models handled that work, how quickly recorded allowance was consumed, and what recorded tokens would cost at today's Standard API rates in USD and CAD—so it helps developers compare workloads with evidence instead of guesswork.
- Evidence: [README.md](https://github.com/Kevin-Mok/track-codex-sessions/blob/3d8511e3ad7c9ff3336798cde5bb69a58c3360f7/README.md) — A searchable terminal picker lets you find and resume sessions.
- Evidence: [src/codex_time/cli.py](https://github.com/Kevin-Mok/track-codex-sessions/blob/3d8511e3ad7c9ff3336798cde5bb69a58c3360f7/src/codex_time/cli.py) — result = argparse.ArgumentParser(description="Read-only Codex session working-time tracker")
- Evidence: [pyproject.toml](https://github.com/Kevin-Mok/track-codex-sessions/blob/3d8511e3ad7c9ff3336798cde5bb69a58c3360f7/pyproject.toml) — requires-python = ">=3.12"
- Status: updated
- Preflight: 2026-10-20T21:47:22.452354+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Understand Codex work and usage with a local Python CLI for session time, model/token reports, allowance burn estimates, and searchable session resumption."`; exact match: True; observed 2026-10-20T21:47:23.648537+00:00

### Kevin-Mok/TrapBot

- Default branch: `master`
- Original JSON: `"reddit bot that looks for comments with song names and responds with their respective SoundCloud links. [Django]"`
- Intended JSON: `"Find SoundCloud links for songs mentioned on Reddit with a Python/PRAW bot that matches track titles and artists; currently on hiatus due to search API issues."`
- Decision: update; Corrects unsupported Django technology and retains documented operational limitation.
- Length: 159
- Evidence commit: [`3af149d2106f0c1bd341b5240587a6ecb12b2bf4`](https://github.com/Kevin-Mok/TrapBot/commit/3af149d2106f0c1bd341b5240587a6ecb12b2bf4)
- Evidence: [README.md](https://github.com/Kevin-Mok/TrapBot/blob/3af149d2106f0c1bd341b5240587a6ecb12b2bf4/README.md) — **Note**: This project is on hiatus due to SoundCloud API returning incorrect search results.
- Evidence: [requirements.txt](https://github.com/Kevin-Mok/TrapBot/blob/3af149d2106f0c1bd341b5240587a6ecb12b2bf4/requirements.txt) — praw==6.2.0
- Evidence: [trapbot/soundcloud_search/find_songs.py](https://github.com/Kevin-Mok/TrapBot/blob/3af149d2106f0c1bd341b5240587a6ecb12b2bf4/trapbot/soundcloud_search/find_songs.py) — found_tracks = soundcloud_service.get('/tracks', q=query, limit=search_query_limit)
- Evidence: [trapbot/reddit/write_post.py](https://github.com/Kevin-Mok/TrapBot/blob/3af149d2106f0c1bd341b5240587a6ecb12b2bf4/trapbot/reddit/write_post.py) — header = '**SoundCloud Links:**\n\n'
- Status: updated
- Preflight: 2026-10-20T21:47:24.088722+00:00; eligibility True; current-description matched original: True
- PATCH exit: 0; readback JSON: `"Find SoundCloud links for songs mentioned on Reddit with a Python/PRAW bot that matches track titles and artists; currently on hiatus due to search API issues."`; exact match: True; observed 2026-10-20T21:47:25.078182+00:00

### Kevin-Mok/weather

- Default branch: `main`
- Original JSON: `"Responsive Next.js weather dashboard with 12-hour forecasts, a validated Weather Network feed for Scarborough, Toronto, and Open-Meteo fallback."`
- Intended JSON: `"Responsive Next.js weather dashboard with 12-hour forecasts, a validated Weather Network feed for Scarborough, Toronto, and Open-Meteo fallback."`
- Decision: unchanged; Existing concise description is supported by README, dashboard defaults, API, and feed validator.
- Length: 144
- Evidence commit: [`468255b50c80667b0b467c2e5bba78e0c344f569`](https://github.com/Kevin-Mok/weather/commit/468255b50c80667b0b467c2e5bba78e0c344f569)
- Evidence: [README.md](https://github.com/Kevin-Mok/weather/blob/468255b50c80667b0b467c2e5bba78e0c344f569/README.md) — A lightweight weather dashboard built for rapid local checks in Toronto and beyond: it opens to Scarborough, Toronto, and shows twelve hourly forecasts with temperature, feels-like temperature, condition and precipitation probability. Scarborough uses a validated browser-scraped The Weather Network feed when available. Other requests and feed failures use Open-Meteo. Current conditions are separately labeled Open-Meteo.
- Evidence: [app/page.tsx](https://github.com/Kevin-Mok/weather/blob/468255b50c80667b0b467c2e5bba78e0c344f569/app/page.tsx) — const DEFAULT_HOURS = 12;
- Evidence: [app/lib/scarborough-feed.ts](https://github.com/Kevin-Mok/weather/blob/468255b50c80667b0b467c2e5bba78e0c344f569/app/lib/scarborough-feed.ts) — if (now - fetchedAt > 90 * 60000) return fail("stale");
- Evidence: [package.json](https://github.com/Kevin-Mok/weather/blob/468255b50c80667b0b467c2e5bba78e0c344f569/package.json) — "next": "14.2.5"
- Status: unchanged
- Preflight: 2026-10-20T21:47:25.479564+00:00; eligibility True; current-description matched original: True
- PATCH exit: not issued; readback JSON: `"Responsive Next.js weather dashboard with 12-hour forecasts, a validated Weather Network feed for Scarborough, Toronto, and Open-Meteo fallback."`; exact match: True; observed 2026-10-20T21:47:25.847637+00:00


## Later commit-delivery readback

During the later authorized commit-plan-push, a fresh public inventory contained53eligible repositories: all52recorded above still matched their intended descriptions exactly, with no removals or mismatches. Kevin-Mok/twitch-following-extension appeared after the historical52-repository audit. No description writes were issued during commit delivery; the new repository is outside that historical audit and is not represented as previously reviewed. This addendum preserves the original observation times and results.
