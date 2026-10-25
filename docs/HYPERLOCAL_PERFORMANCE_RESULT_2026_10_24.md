# Hyperlocal geospatial performance — Ubuntu run (2026-10-24)

**Milestone: 100,000 synthetic enrolled devices indexed and queried successfully.** Measurements copied from the researcher's actual Ubuntu run of `src.hyperlocal_performance`; raw JSON remains local at `results/local/hyperlocal_performance.json`.

Command:
```bash
python3 -m src.hyperlocal_performance --sizes 10000 50000 100000 --queries 50 --output results/local/hyperlocal_performance.json
```

| Synthetic devices | Inserts/s | R-tree median (ms) | R-tree p95 (ms) | Full scan median (ms) | Median speedup |
|---:|---:|---:|---:|---:|---:|
| 10,000 | 194,736 | 0.0140 | 0.0268 | 7.6159 | 544× |
| 50,000 | 162,736 | 0.0221 | 0.0293 | 38.1676 | 1,727× |
| 100,000 | 138,458 | 0.0286 | 0.0428 | 76.6641 | 2,680× |

The benchmark asserted that the indexed and full-scan methods returned identical result counts for each of 50 test query centers per population. It uses fictional positions and temporary SQLite storage with warmed-up single-process query paths. Timings exclude address geocoding, network transfer, collectors, and authoritative verification of real device location; they are **not** end-to-end dashboard response latencies.

**Interpretation:** Local R-tree lookups easily support the narrow 50-foot-radius spatial-filter component at these tested dataset sizes. The primary unresolved constraints for real-time intelligence are trustworthy observations, location precision, freshness, provenance, and authorization.
