# Nominal frame rate falsely rejected

- Symptom: saved 720p at 29.808 average fps rejected against 720p at nominal 30 fps.
- Impact: retained download reported as lower quality despite close frame rates.
- Evidence: user command output; verifier uses a fixed 0.1 fps tolerance.
- Status: Resolved. Actual stream rates are 3726/125 = 29.808 fps, 0.64% below nominal metadata. The fixed absolute threshold was too strict.
- Tooling: first probe assumed an mp4 suffix; listing showed mkv. Corrected the probe path; no media changed.
- Resolution: allow 1% relative FPS timing variation, with unchanged resolution requirements.
- Verification: exact-case test was RED, all 27 tests now pass, including 29/25/24 versus 30 and 30 versus 60 failures. refresh-config exited 0. Installed command verified retained hf163Txt_pg.mkv at 720x1280 / 29.808 fps with audio, exit 0.
- Follow-up: retain actual FPS in messages; verification is bounded metadata comparison, not full integrity proof.
