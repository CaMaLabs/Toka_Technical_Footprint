# Synthetic location-correlation experiment — 2026-10-24

Patent context: [US11212308B1](PATENT_LOCATION_CORRELATION_US11212308B1.md). This is a **conceptual toy model**, not a replication of Toka code or verified deployed architecture.

## Reproduce
```bash
python3 -m unittest discover -s tests -v
python3 -m src.location_correlation
```

## Local results
Three new tests passed. Across six hand-built fictional cases:
- stable identifier supported by two sensors: correctly resolved to zone-alpha (1)
- shared public gateway, stale observations, randomized identifier, single sensor, and conflicting observations: abstained (5)
- false location resolutions: 0 **in these deliberately constructed fixtures**, not a measured field false-positive rate.

Full output: [location_correlation_fixture_results.json](../results/location_correlation_fixture_results.json).

## Interpretation
A gateway's public network identifier does not uniquely identify a device or location. A token changing between observations loses linkage. Stale records and conflicting sources cannot justify a precise location. The synthetic algorithm demands two distinct sensor identifiers before accepting one location, but does **not** prove sensor independence, trustworthy timestamps, or correctness of any source. It does not model physical geography, probability calibration, adversarial manipulation or true device mobility.

No camera IPs, SSIDs, MACs, coordinates or third-party logs were collected.

## Next tests
Use reproducible randomized fictional populations, sensor-error and identifier-collision rates, missing observations, drift, and independent holdout seeds. Report precision and coverage including abstentions, and test how results degrade with noise. Keep discovery/location/access technically separate.
