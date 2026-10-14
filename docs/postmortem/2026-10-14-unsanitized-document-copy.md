# Unsanitized Documentation Copy Reintroduced Findings

This postmortem records why a pre-commit worktree scan found private-context
matches after task documentation was copied onto the sanitized tip.

## Symptom

On 2026-10-14, a direct scan of 1,712 worktree files reported private account,
name, home-path, address, and sensitive-path categories in the newly copied
plan, harness, smoke checklist, lessons, and two intentional placeholder paths.

## Impact

The public-readiness tip was not safe to commit. The already rewritten 688-
commit historical graph remained clean, no remote operation occurred, and the
findings were caught before staging.

## Evidence

- The historical all-object audit had passed immediately before adding the
  public-tip files.
- The copied smoke checklist and lessons came from the original checkout, so
  copying each whole file bypassed the sanitized versions already present in
  the rewrite clone.
- The private vault README and empty feedback log are intentionally public-safe
  placeholders, but broad historical path rules still matched their locations.

## Root Cause

The artifact-copy step treated already tracked documentation like new task
artifacts. That replaced the sanitized historical versions with whole files
from the original checkout. Separately, the path auditor had no way to express
that a specifically reviewed placeholder was safe while its broader directory
remained forbidden.

## Resolution

The smoke checklist and lessons were restored from the sanitized tip and only
their task-specific hunks were reapplied. New plan/harness documents were run
through the deterministic sanitizer before copying. The auditor now supports an
exact `allowed_paths` list; only the public vault README and empty feedback log
are allowed, while their blob contents continue through every detector.

## Verification

- A new allowlist test failed before implementation and passed afterward.
- All 11 auditor/sanitizer behavioral tests passed.
- A fresh direct scan checked 1,711 worktree files with the complete private
  rules and reported zero findings.

## Current Status

Resolved before staging or commit.

## Next Steps

No code follow-up remains. The postmortem-memory ledger update is intentionally
deferred because that canonical ledger is outside the user-authorized folder.
