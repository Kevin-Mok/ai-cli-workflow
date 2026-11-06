# Firstmate prompt ZIP commit blocked by existing privacy findings

The requested session commit could not include Firstmate's prompt-ZIP ignore rule because the required privacy gate rejects the repository's unchanged HEAD. This report records the safe-subset checks and leaves unrelated content and the privacy gate intact.

## Symptom and impact

- The isolated candidate containing only `.gitignore` and `docs/task-status.md` was rejected with 25 findings. No Firstmate commit or push occurred.
- Findings were classified as credential, email, IP address, and provider token. No raw matched content is copied into this report.
- Linux-config's separately scoped instruction/ignore/admission commit passed exact-candidate and pre-push gates and was pushed as `c184f63`.

## Lookup and applicability

Read the canonical postmortem-memory skill and searched `privacy gate baseline candidate`. Returned broader browser and execution incidents did not establish a remedy for the unchanged Firstmate tree. The applicable existing rule is to preserve the gate, test the exact safe subset, and report the blocking evidence instead of sanitizing unrelated source.

## Evidence

- Exact candidate: the shared privacy scanner with an isolated `GIT_INDEX_FILE`; exit 1, 25 findings.
- Baseline: the same scanner with `--tree` pointing at unchanged `HEAD^{tree}`; exit 1, the same 25 findings.
- Minimum subset: an isolated index containing only the three-line `.gitignore` addition; exit 1, with all 25 hashed location references identical to baseline.
- No introduced source text accounts for these baseline findings. Counts alone were supplemented by exact hashed-location comparison.
- Existing generated ZIPs pass integrity checks and match the scoped ignore pattern. Markdown prompts and archives outside prompts remain visible.

## Current status and next steps

Status: unresolved; baseline rejection confirmed. The scanner's category labels do not establish whether each existing match is a real secret or a false positive. No sanitation, scanner weakening, hook bypass, history rewrite, or unrelated content change was attempted.

The Firstmate ignore rule, status note, upload note, and private archives remain local. Any reviewed remediation or approval-policy change needs its own concrete scope; upstream publication also requires this home's explicit contribution authority. Unrelated parent-thread work remains untouched.

## Learning decision

No new general rule is needed: the existing exact-candidate privacy gate and safe-subset contract already prescribe this outcome. Record this report's reviewed hash/alias with an explicit no-new-learning decision; do not infer or claim a security fix.
