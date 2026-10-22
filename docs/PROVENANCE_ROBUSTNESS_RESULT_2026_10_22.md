# Provenance robustness experiment — 2026-10-22

**Executed locally:** `python3 -m unittest discover -s tests -v` — 8 tests passed. `python3 -m src.robustness_experiment` produced [results JSON](../results/provenance_robustness.json).

## Outcomes
- **Legitimate transcoding (synthetic encoding-label change):** raw serialized HMAC fails; HMAC over normalized logical records succeeds. This is not real codec transcoding or perceptual hashing.
- **Missing intermediate observation:** distinct simulated transit and recorder interventions yield identical final archives; precise localization is impossible from the archive alone.
- **Clock offset:** a known constant +1-hour offset invalidates raw serialized signature; correcting the known offset restores it. Unknown drift, jitter, time-zone ambiguities and malicious shifts remain untested.
- **Compromised signing key:** synthetic altered content accompanied by a signature generated with the stolen/shared key verifies; provenance is no longer assured.

## Interpretation
Passing assertions confirm the expected behavior of this *toy synthetic model*, **not** tamper detection on real surveillance footage or a validated claim about Toka. A signature over a canonical representation is only useful if the canonicalization is robust against meaningful image changes and the signer is independently trusted. Neither property is established here.

## Next controls
Use real, locally generated video fixtures; test benign H.264/H.265 transcoding and timestamp changes with false-positive rates; use frame-level perceptual metrics as secondary signals; introduce missing observation points and unknown clock drift; test protected keys and externally anchored logs.
