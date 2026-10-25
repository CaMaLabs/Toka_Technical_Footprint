"""Offline benchmark for a 50-foot synthetic inventory; no network access."""
import argparse
import json
import math
from pathlib import Path
import random
import sqlite3
import statistics
import tempfile
import time
from src.hyperlocal_inventory import connect, nearby

def measure(n=10000, seed=20261024, queries=50):
    rng = random.Random(seed)
    with tempfile.TemporaryDirectory(prefix='hyperlocal-perf-') as directory:
        db = connect(str(Path(directory) / 'data.sqlite'))
        try:
            started = time.perf_counter()
            for start in range(0, n, 5000):
                rows = []
                rectangles = []
                for i in range(start, min(start+5000,n)):
                    lat, lon = rng.uniform(-.027,.027), rng.uniform(-.027,.027)
                    rows.append((i+1,f'synthetic-{i}','Synthetic device','test',lat,lon,'synthetic',0.0))
                    rectangles.append((i+1,lat,lat,lon,lon))
                with db:
                    db.executemany('INSERT INTO devices(id,key,name,kind,lat,lon,source,seen_at) VALUES (?,?,?,?,?,?,?,?)',rows)
                    db.executemany('INSERT INTO geo_index VALUES (?,?,?,?,?)',rectangles)
            insert_seconds = time.perf_counter()-started
            points = [(rng.uniform(-.02,.02),rng.uniform(-.02,.02)) for _ in range(queries)]
            def scan(lat,lon):
                phi = math.radians(lat)
                count = 0
                for a,b in db.execute('SELECT lat,lon FROM devices'):
                    dp,dl=math.radians(a-lat),math.radians(b-lon)
                    h=math.sin(dp/2)**2+math.cos(phi)*math.cos(math.radians(a))*math.sin(dl/2)**2
                    count += 2*6371008.8*math.asin(min(1,math.sqrt(h))) <= 50/3.280839895
                return count
            def benchmark(func):
                samples=[]
                for lat,lon in points:
                    before=time.perf_counter()
                    found=func(lat,lon)
                    samples.append(((time.perf_counter()-before)*1000,found))
                return samples
            benchmark(lambda lat,lon:len(nearby(db,lat,lon)))
            benchmark(scan)
            indexed=benchmark(lambda lat,lon:len(nearby(db,lat,lon)))
            brute=benchmark(scan)
            if [x[1] for x in indexed] != [x[1] for x in brute]:
                raise AssertionError('indexed and full-scan counts differ')
            def summary(rows):
                times=sorted(x[0] for x in rows)
                return {'median_ms':round(statistics.median(times),4),
                        'p95_ms':round(times[math.ceil(.95*len(times))-1],4)}
            return {'devices':n,'queries':queries,'insert_seconds':round(insert_seconds,4),
                    'inserts_per_second':round(n/insert_seconds,1),
                    'indexed':summary(indexed),'full_scan':summary(brute),
                    'match_counts_verified':True}
        finally:
            db.close()

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--sizes',type=int,nargs='+',default=[10000,50000,100000])
    p.add_argument('--queries',type=int,default=50)
    p.add_argument('--output',default='results/local/hyperlocal_performance.json')
    args=p.parse_args()
    if not 2<=args.queries<=500 or any(not 1<=n<=1000000 for n in args.sizes):
        p.error('sizes 1..1000000, queries 2..500')
    rows=[]
    for n in args.sizes:
        r=measure(n,queries=args.queries)
        rows.append(r)
        print(f"{n:,} devices: {r['inserts_per_second']:,.0f} inserts/s; indexed p50={r['indexed']['median_ms']} ms p95={r['indexed']['p95_ms']} ms; full scan p50={r['full_scan']['median_ms']} ms",flush=True)
    path=Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps({'synthetic':True,'radius_feet':50,'runs':rows},indent=2)+'\n')
    print('Saved',path)

if __name__=='__main__':
    main()
