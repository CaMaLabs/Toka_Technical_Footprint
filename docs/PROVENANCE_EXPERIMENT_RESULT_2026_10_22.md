# Provenance localization experiment — 2026-10-22

**Status: local execution completed; six tests passed.** This is a controlled, purely synthetic proof of detection logic, **not** a real camera exploit, actual video codec test, or proof about Toka's products.

## Reproduce
```bash
python3 -m unittest discover -s tests -v
python3 -m src.provenance_experiment
```
Uses only Python standard library, eight synthetic records per case and HMAC-SHA256 manifests with a fixed **lab-only** key; not suitable as a production secret.

## Results
| Scenario | Wire matches trusted source | Archive matches source | Cloud matches source | First divergent observation |
|---|---|---|---|---|
| Untouched | Yes | Yes | Yes | None |
| In-transit substitution | No | No | No | Before or at wire observation |
| Recorder-side modification | Yes | No | No | Between wire observation and archive |
| Cloud-side modification | Yes | Yes | No | Between archive and cloud |

All six unit tests passed in a local run (0.001s reported). Raw fixture outcomes: [provenance_four_scenarios.json](../results/provenance_four_scenarios.json).

## The crucial negative finding
**Archive-only inspection cannot distinguish in-transit substitution from recorder-side modification**. A cleanly serialized recording is not evidence of authentic provenance. Localization succeeds here only because we assume an uncompromised source-side signing key and independent, trusted observation points at the wire, archive and cloud boundaries.

We did **not** establish which physical device was compromised: “before or at wire observation” still includes camera endpoint and intermediary paths. We also did not simulate legitimate transcoding, key compromise, signature loss, clock drift, replay protection or network delivery. Those are future controls; do not extrapolate laboratory accuracy to field performance.

## Interpretation
This illustrates how the architecture in patent [US10674118B1](../docs/PATENT_DISCREET_CAMERA_ACCESS_US10674118B1.md) could lead to apparently valid archived footage without rewriting an archive in-place. It does **not** attribute observed attacks or establish that Toka implemented this method.

## Next discriminating controls
1. Signed pre-encoding source evidence vs post-transcode archive: use canonical frame fingerprints to avoid false alerts on legitimate re-encoding.
2. Missing or untrusted intermediate vantage point: quantify localization ambiguity.
3. Independent trusted timestamps and monotonic sequence indices vs benign jitter/clock offsets.
4. Multiple simultaneous modifications and a compromised source signing key, with detection limits stated explicitly.
