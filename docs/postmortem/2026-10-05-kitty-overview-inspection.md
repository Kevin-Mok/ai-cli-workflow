# Kitty overview inspection failures

This records the command-runner and diagnostic failures encountered while planning
and implementing live Codex titles. Use the approved scoped execution route, read
the helper schema, and keep the incident ledger aligned with this report.

- Date: 2026-10-05.
- Symptom: Initial planning reads failed before shell startup with
  `bwrap: loopback: Failed RTM_NEWADDR: Operation not permitted` (exit 1).
  A planning search also named nonexistent scripts/executable_refresh-config*;
  the actual helper is dot_config/fish/functions/refresh-config.fish. A later
  diagnostic assumed sources.json contained a top-level sources list and raised
  KeyError: sources after printing the actual top-level reports field.
- Impact: Inspection needed correction. Failed shell starts changed no files;
  diagnostic failures changed no product state. Planning remained read-only.
- Evidence: Approved require_escalated reads exited 0. The read-only ledger helper
  search worked; its workflow specifies schema_version 1 with reports/findings.
  A corrected inspection reports report fields aliases, findings, reviewed_on,
  sha256 (exit 0). Terminal-workflow and dictation baselines both exit 0.
- Root cause: Sandbox wrapper cannot initialize its loopback interface; the host
  policy itself was not diagnosed or changed. The path/schema diagnostics assumed
  names instead of following the inspected repository contracts.
- Resolution/status: Verified workaround for scoped command execution; diagnostic
  assumptions corrected. Default sandbox startup remains unresolved host work.
- Lookup: Query bwrap loopback Failed RTM_NEWADDR matched
  local-sandbox-loopback-approved-route, verified_workaround. Its applicability
  matches this pre-shell error; successful scoped escalations verify only bypass.
  Query KeyError sources ledger schema returned related validation findings but
  no applicable malformed-data defect: this was the caller's wrong field name.
  Read the helper workflow and use reports; no helper implementation change.
- Initial learning decision: The sandbox and schema/path failures duplicate known
  guidance. The later live geometry investigation adds the finding
  local-i3-hidden-workspace-titlebar-probe, recorded below.
- Next steps: Complete feature deployment checks and keep this report/ledger in
  the same eventual commit as the related implementation. No host-security repair.

## Runtime titlebar probe investigation

- Symptom: After successful refresh-config, i3 reload and the Kitty border update,
  all 11 current Kitty windows report border=normal but only 4 report positive
  deco_rect.height. The calling task's positive-height assertion failed (exit 1).
- Impact: Deployment succeeded, but this geometry assertion does not yet establish
  whether the summary bar is visible. No conversations were restarted or closed.
- Evidence: Both i3 IPC commands return success:true. Live/managed title settings
  match [activity, thread-name], and deployed title instructions match source.
- Current status: Investigating geometry semantics, visibility/fullscreen state
  and actual desktop rendering before changing the implementation.
- Next steps: Inspect complete relevant window/layout geometry and current output
  visibility; capture the actual workspace view if needed. Correct the probe or
  implementation only after identifying why normal borders have zero decoration.

- Probe follow-up: A temporary screenshot-selection probe failed before changing
  focus with TypeError: argument of type NoneType is not iterable. Non-window
  i3 tree nodes may have name=null; a default in dict.get does not replace null.
  Normalize with (node.get('name') or '') before matching the calling-task label.
  The lookup found no specific i3 defect; the documented tree contract and null
  input identify this as diagnostic code only. No product change is required.

## Runtime resolution and verification

- Root cause: The tested task was on an inactive workspace. Its title geometry
  retained the earlier pixel-border rendering until the workspace was displayed.
  i3 4.22+ additionally distinguishes actual_deco_rect for normal split leaves.
  This was a diagnostic false negative, not a failed titlebar implementation.
- Resolution: Display only the calling task briefly, allow a compositor frame,
  inspect actual_deco_rect (with deco_rect fallback), capture the result and
  restore original focus. The titlebar then reports 1280x30 and is visibly drawn.
- Screenshot evidence: The first capture occurred before the compositor updated.
  On retry, scrot preserved the existing titlebar.png and wrote titlebar_000.png;
  inspecting the fresh file showed the live titlebar. Use a unique output filename
  and inspect the actual generated artifact rather than an older requested path.
- Reviewer diagnostic: A read-only summary tried sorting mixed int/None heights
  and raised TypeError. This changed no state. Handle missing geometry fields
  explicitly; a hidden/unrendered node is not evidence of a display regression.
- Verification: Scoped focus/capture/restore probe exits 0. A temporary new Codex
  process resumed only this task without sending a model prompt; it displayed the
  persisted task title without the project suffix. Tabbed/narrow/fullscreen checks
  exit 0; a 320x30 titlebar clips safely, and leaving fullscreen restores it.
  Only the temporary view was closed, and the original focus was restored.
- Learning: Register local-i3-hidden-workspace-titlebar-probe as a verified
  diagnostic workaround, with this reviewed report hash. The underlying normal
  rendering behavior is unchanged; this is not a host-sandbox repair.
- Current status: Diagnostic investigation resolved. Sandbox workaround remains
  verified; normal sandbox startup remains external outstanding work.
