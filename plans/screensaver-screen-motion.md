# Screen motion idle detection

Start the existing screensaver after five minutes without physical input or visible changes on the 4K display. Replace automatic Chrome coverage with local screen sampling, mask the live i3 bar, test the policy, then deploy only the relevant package files and restart its idle service.

## Scope and decisions

- User explicitly chose screen observation and exclusion of i3 bar. Motion is an approximation: animations count as activity and still video may not. Nothing is uploaded or saved.
- Monitor the middle 4K output only. Capture errors and lock uncertainty suppress activation. Geometry changes restart the quiet interval.
- Do not sample while owned screensaver preview is active, so its animation cannot dismiss itself. Reset baseline on exit; physical input still dismisses playback. Manual/scheduled commands remain available.
- Scope: new motion module/tests, main integration/CLI tests, README, guide and smoke checks. Existing browser module stays available for legacy/manual behavior; no unrelated removals.
- Initial dirty state captured. Preserve all earlier staged shortcut work, untracked plans/reports and unrelated edits. No commit/push in this task; previous review block remains.

## Checklist

- [x] Read daemon/renderer/status boundaries and capture baseline.
- [x] RED then GREEN: motion/bar masking/quiet threshold/capture failures.
- [x] Finish daemon/status integration GREEN and broader checks.
- [x] Update status/documentation; run focused and broader relevant checks plus review.
- [x] Deploy scoped package changes, run shortcut-scoped refresh, restart idle service and verify live motion/bar geometry/status.

## Verification and rollback

Unit tests use synthetic images/time and fake process boundaries. Xvfb test exercises real capture with a synthetic i3bar. Run relevant CLI, motion, runtime and timer checks without the actual media library; compare live module/source bytes after deployment. Observe live status progressing through quiet/motion and excluded i3bar geometry. Five uninterrupted physical-idle minutes and movie/animation acceptance remain separate manual checks if input prevents observation.

Rollback: restore only previous main.py and remove deployed motion module, restart media-screensaver.service; old browser prerequisite returns. Restore docs in matching change. Do not rewrite earlier staged work.

## Review and handoff

Atomic plan: implement local 4K motion sampler with i3bar exclusion; integrate once in idle supervisor; prevent self-sampling; deploy and verify. Cursor prompt: Verify local 4K motion-based idle activation and i3bar exclusion using Xvfb plus live read-only status, preserve staged work and do not capture/save personal screen images. Suggested commit if separately authorized: `feat(screensaver): detect idle screen motion without i3bar`.

Motion worker evidence: synthetic RED/GREEN and five passing Xvfb tests, including real nested i3-frame bars and cumulative drift. Real live bar metadata: 4K bar is 3840x112 at bottom; mask discovers actual geometry. Integration RED proved automatic preview/daemon still used browser; status RED proved old browser status must be replaced. Preview sampling pauses while owned child runs; motion resets after dismissal.

Full relevant suite under approved disposable Xvfb passed65 tests; timer tests passed10 and browser JS passed. Review corrected stale browser wording in service/README and smoke docs. Live check then exposed slow full4K python-Xlib pixel decode (>2min CPU); stopped owned diagnostic only. Native Pillow probe is0.17s for3840x2160; integrating explicit-display native capture beforedeployment.

Final source evidence: native capture plus actual nested bar exclusion works on real4K in0.278s; final isolated4K motion suite seven pass, CLI eight pass. Fullmedia65 passed before native-capture replacement; finalaffected15 passed afterward. Timer10 and browser JS passed. Captures remain memory-only; explicitXdisplay disables external fallback. Pending scopeddeployment/restart only, no blockers.

Deployment verified: installed only motion.py/main.py atomically after confirming installed main matched pre-task HEAD; backup `/tmp/screensaver-motion-backup-dli93dlm/main.py`. Shortcut-scoped refresh exited0, service restart succeeded, active/running. Fresh installed status reports screen motion quiet14s of300s, i3bar excluded, idle monitor running. Both installed files match tested source bytes. Earlier immediate postrestart status preceded the first sample; subsequent report confirms running. No Chrome bridge requirement remains for automatic playback. No commit/push or changes to existing staged index.

Remaining acceptance: no uninterrupted physical five-minute idle/movie session observed; screenshots stayed in memory. Motion is approximate and non-bar animations count. Final automated15 affected tests, earlier fullmedia65/timer10/JS pass; known Xlib ResourceWarning only. Rollback via backed-up main and restart restores prior browser-gate behavior.

Sessiondelivery: explicitcommit-session authorizes onecoherentcommit andupstreampush includingmotion, timers, blankingfix andallmatchingdocs/plans/tests/reports. Helperattribution unavailable; directlyobservedwrites andinitialbaselineestablishscope. Excludeunrelatedxhpp mapping/preexistingwork. Actualcommit/pushresult reportedinconversation.
