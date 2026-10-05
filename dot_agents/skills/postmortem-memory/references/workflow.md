# Retrieval and learning workflow

Use the helper to discover reports, retrieve reviewed guidance and check coverage.
Codex reads and distills the evidence, then edits tracked knowledge directly; the
helper never writes files or executes repairs. Keep updates in the incident's task.

## Commands and locations

The standard-library helper is `scripts/postmortem_memory.py` within the skill.
It runs with Python 3.12+ from any working directory. Each subcommand accepts
`--knowledge DIRECTORY` for an explicit fixture or alternate checkout. Otherwise
it prefers the canonical tracked skill when its SKILL.md exists, then falls back
to the package containing the executing helper. Never maintain installed memory
as an independent writer. An unavailable tracked update remains outstanding.

| Command | Read-only behavior |
| --- | --- |
| `scan [--root DIRECTORY ...]` | Hash discovered reports; show exact-content groups, aliases, new/changed sources, unregistered aliases, missing registered sources and traversal errors. |
| `search QUERY` | Ranked token/phrase retrieval across symptoms and guidance; return reference section, status, confidence, applicability, remedy, scope, limits and source aliases. A miss includes the next diagnostic step. |
| `check [--root DIRECTORY ...]` | Validate ledger shape, reference files/anchors, statuses/evidence scopes, reciprocal finding/source links and coverage in selected roots. |
| `check --postmortem PATH` | Validate all ledger/reference contracts and only the specified source's current hash and registered alias; unrelated unavailable scan roots do not block it. |

Default scan roots are `/home/example/coding` and `/home/example/linux-config`.
Repeatable `--root` flags replace them; Git ignore rules do not affect traversal.
A new alias of reviewed exact content still needs explicit registration. Changed
content needs a fresh full review. Full checks report missing aliases inside the
selected roots, while search can retrieve distilled evidence without originals.
Targeted checks do not prove whole-corpus coverage.

Output is JSON. Exit 0 means the requested operation succeeded (including search
misses); 1 means unreadable/missing sources or incomplete coverage; 2 means invalid
arguments, ledger or reference contracts. Commands require a valid reviewed ledger;
invalid knowledge fails visibly before coverage can be claimed. `scan` reports
new/changed coverage without failing simply because it needs review; `check` fails
until that review is recorded. Read complete errors rather than trusting counts.

## Discovery and privacy boundary

Walk physical paths without following symlink files, directories or root ancestors.
Prune `.git`, dependencies, build output, caches and private directories before
reading. Always exclude `personal-context` directory/filename components plus
`private`, `.private` and `personal` directories. Do not traverse the private store.
This conservative boundary also excludes operational reports named personal-context.

Candidates are `.md`, `.txt` or `.rst` under singular/plural postmortem or incident
folders (including incident-report variants), or explicitly named incident/
postmortem files. Exclude actual template artifacts, index/README navigation, and
named narratives under plans, prompts, skills, tasks and benchmarks. A report
about template failures remains eligible. Include ignored historical repository
copies and `.worktrees` already present; never create a worktree for discovery.
Human review handles narrative candidates explicitly instead of inventing findings.

Exact SHA-256 byte identity forms one report, retaining every physical alias.
Distinct historical versions remain separate evidence units. Alias count is never
incident recurrence. Related reports may describe one incident; the ledger's unique
hash count is a coverage count, not an estimate of independent incidents.

## Authoring contract

[sources.json](../sources.json) has schema_version 1, reports and findings lists.
Metadata records review scope; counts there describe that review date, not a timer.

Each report has `sha256`, all absolute `aliases`, `reviewed_on`, and `findings` IDs.
If it has no reusable learning, give an explicit nonempty `decision` and an empty
findings list. Do not invent a fix for incomplete or physically truncated reports.
When a sole alias changes, update or replace its reviewed record and affected
support links; when copies remain, split the changed alias into a new hash record.
Every finding and report must link reciprocally. Preserve supported historical
claims with their limits; revise or remove claims whose evidence was superseded.

Each finding has `id`, `reference` (`references/topic.md#anchor`), `status`,
`symptoms`, `applicability`, `diagnostics`, `confidence`, `remedy`, `verification`,
`verification_scope`, `limitations`, and `sources` (reviewed hashes). Markdown
sections contain the same fields and links to representative original reports;
the ledger retains all aliases. Keep prose concise, reusable and free of secrets,
contact details, personal discussions and raw report copies. Consult only the
matching reference section rather than loading the full ledger into context.

| Status | Evidence contract |
| --- | --- |
| `verified_fix` | Remedy demonstrably repairs the specified behavior, with code or runtime evidence and supported/confirmed causal confidence. State the scope; code evidence is not live activation. |
| `verified_workaround` | Observed bypass/mitigation; underlying defect or original execution path remains. |
| `unresolved` | Hypothesis, diagnosed but unverified remedy, blocked investigation or baseline issue. State what remains unproved. |
| `activation_pending` | Implemented/checked change still needs live installation, restart, permission or operator acceptance. Scope is code or none. |

Confidence values: confirmed, supported, hypothesis. Verification scopes: code,
runtime, workaround, none. If one report contains multiple states, split findings
instead of promoting all outcomes together. Source and reference claims require
human review; schema validation cannot judge the truth of arbitrary prose.

## Reusable verification

From the linux-config checkout run `python3 -B tests/test_postmortem_memory.py`.
Run `python3 -B scripts/smoke_postmortem_memory.py` for a disposable cross-repository
lookup and synthetic changed-report review. It rejects the stale hash, authors the
fixture update, verifies targeted coverage and preserves activation_pending after
code checks. It writes only a temporary fixture, cleans up, and requires no sudo.
Fresh-agent evaluation evidence and limitations live in the
[implementation plan](../../../../plans/postmortem-memory.md).

See [executed agent evaluations](../../../../docs/troubleshooting-memory-evaluations.md) for the five-repetition comparison, exact scenarios and limits.
