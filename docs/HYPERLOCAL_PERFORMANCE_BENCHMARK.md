# Hyperlocal inventory performance experiment

The benchmark generates **synthetic** devices in a fictional geographic coordinate patch. It inserts them into an isolated temporary SQLite database and measures the 50-foot R-tree radius query against a full-table scan for identical centers. Every query checks that match counts agree.

Run:
```bash
cd ~/research/Toka_Technical_Footprint
git pull --ff-only
source .venv/bin/activate
python3 -W error::ResourceWarning -m unittest discover -s tests -v
python3 -m src.hyperlocal_performance --sizes 10000 50000 100000 --queries 50 --output results/local/hyperlocal_performance.json
```

Output reports per-population insertion time, inserts/second, indexed and full-scan median and p95 milliseconds, and correctness. The default run performs 50 matching queries for each size, after warming both approaches. Repeat runs to assess thermal or disk caching variability.

**Status:** benchmark code committed; 10k/50k/100k Ubuntu timing measurements pending. No performance claims should be made before examining measurements. No scanning, camera connections, geographic lookup, actual addresses, or LAN access occurs. The service running on port 18765 is unaffected. Data is deleted after each benchmark.

**Limits:** Synthetic distribution, fixed circle, temporary SQLite storage, and local single-thread execution do not capture multi-user contention, disk failure, access-control overhead, real-world location precision, or internet latency.
