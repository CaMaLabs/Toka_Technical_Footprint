# Synthetic location-correlation scaling — 2026-10-24

**Status:** Independently executed locally using Python, 5 seeds × 2,000 fictional device queries × 3 scenarios. No network access, real devices, Wi-Fi scanning, IP geolocation or live people data.

## Reproduce

```bash
python3 -m unittest discover -s tests -v
python3 -m src.location_benchmark --population 2000 --output results/location_benchmark_2026_10_24.json
```

## Results

| Scenario | Queries | Correct | False location | Abstained | Coverage |
| --- | ---: | ---: | ---: | ---: | ---: |
| Clean | 10,000 | 10,000 | 0 | 0 | 100.00% |
| Moderate noise | 10,000 | 6,688 | 1 | 3,311 | 66.89% |
| Severe noise | 10,000 | 1,019 | 7 | 8,974 | 10.26% |

Precision conditional on resolving a device: moderate 6688/6689 = ~99.985%; severe 1019/1026 = ~99.32%. These values are **properties of the toy benchmark** and cannot be extrapolated to real-world systems or Cybertoka's implementation.

## Design

Each fictional device is assigned a synthetic zone token and up to three fictional sensor observations. Scenarios vary shared identifiers (a coarse NAT-like collision), missing observations, clock jitter, rotation of the query identifier, and erroneous zone observations. A matcher accepts a location only when at least two independently named sensors support exactly one candidate zone within a 120-second window; otherwise abstains.

**Limitations:** The model assumes sensor labels represent independent sources and observations are honest; it assigns sensors per device, makes zones uniform, and uses simplistic collision behavior, so realism is limited. Distinct timestamps and sensor IDs do not provide verified independence. It does not simulate IP addressing, physical geographic accuracy, access, camera targeting, adversarial false data, or patent implementation. Noise severities are arbitrary and not empirical.

## Interpretation and next experiment

Low-noise data resolves readily. Under high noise, coverage collapses, while false associations are possible. Next: vary each noise variable independently, measure calibration by source-count, add adversarially correlated sensor errors and cases where a device moves between zones. Quantify whether stronger abstention policies improve errors without making discovery unusable.

Record all real-world measurements separately and never present these results as validation of actual Toka functionality.
