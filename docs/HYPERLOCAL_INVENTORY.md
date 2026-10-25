# Hyperlocal opt-in device inventory (50-foot radius)

A prototype to study an authorized geographic device inventory, not a camera discovery or access tool. **No scanning, sniffing, geolocation inference, vendor APIs, ONVIF probing, or third-party collection.** All records are synthetic or manually provided by an authorized operator.

## Start (Ubuntu)

```bash
cd ~/research/Toka_Technical_Footprint
git pull --ff-only
source .venv/bin/activate
python3 -m unittest discover -s tests -v

# Make a local token; do not commit it.
export HYPERLOCAL_TOKEN="$(python3 -c 'import secrets;print(secrets.token_urlsafe(24))')"

# Demo uses a synthetic coordinate origin (0,0), NOT a real address.
python3 -m src.hyperlocal_inventory --lat 0 --lon 0 --label "Synthetic lab" --seed
```

Open **http://127.0.0.1:8765** on that Ubuntu machine. Three synthetic records should appear inside the radius; a fourth is intentionally outside. The dashboard polls every two seconds. Stop with Ctrl+C. Data is persisted in `hyperlocal_local.sqlite`. Running `--seed` again upserts the same four records.

### Authorized real-site operation

Supply the precise latitude and longitude of an address **you own or administer**, from an external geocoder or known survey record, e.g. `--lat YOUR_LAT --lon YOUR_LON --label "My authorized site"` (without `--seed`). An address **label alone isn't geocoding**. The system does not infer coordinates for nearby third-party devices. Coordinate accuracy at a 50-foot scale requires trustworthy installation coordinates; GPS and consumer geocoding may not be accurate enough.

### Add an explicitly enrolled device

Use your own coordinates, not the example 0,0, for real installations. Only the client with the token can update records:

```bash
curl -fsS -X POST http://127.0.0.1:8765/api/ingest \
  -H "X-Inventory-Token: $HYPERLOCAL_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"key":"my-test-device","name":"Enrolled device","kind":"camera","lat":0.00001,"lon":0.00001,"source":"manual-consent"}'
```

To list nearby inventory without the dashboard:

```bash
curl -fsS http://127.0.0.1:8765/api/devices
```

## Design and security

- Built-in Python HTTP server, bound **only to 127.0.0.1**. Don't expose this service directly to the internet or forward its port. The dashboard GET endpoint has no authentication (localhost access only); updates need an `X-Inventory-Token` secret. For multi-user/network deployment, add TLS, authorization for both reads and writes, an audit trail, source trust policies, and retention limits before use.
- SQLite R-tree stores a geographic bounding rectangle per record; an exact Haversine distance filter returns only devices within **50 feet of the specified center**. The comparison is approximate due to coordinates and the spherical Earth model.
- Writes use timestamp of receipt; **last seen does not independently prove device online**. Repeated authorized updates can refresh it. There is no auto-discovery.
- Inventory records contain device identifiers and precise locations; keep the database private. `hyperlocal_local.sqlite` is gitignored.
- Sources and location confidence are **self-declared**, not verified. This demonstrates a practical index, **not** Toka's implementation, Sidewalk integration, or Palantir datasets.

## What to measure next

Benchmark 10k–100k synthetic records, index query latency, update rate and cache age; compare bounding-box candidates vs exact circle matches, quantify positional uncertainty, and add expiry/staleness indicators. A separate enrolled agent could push signed observations only from devices explicitly configured by their owners.
