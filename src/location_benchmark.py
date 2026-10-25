"""Synthetic-only location-token correlation benchmark. No network access."""
import argparse
import json
import random
from collections import defaultdict

def run(seed=101, population=2000, collision_rate=.1, dropout_rate=.15,
        clock_jitter=30, rotation_rate=.1, sensor_error=.05, window=120):
    rng = random.Random(seed)
    n_zones = max(8, population // 80)
    observations, queries = [], []
    for i in range(population):
        zone = f'zone-{rng.randrange(n_zones)}'
        identifier = f'device-{i}'
        if rng.random() < collision_rate:
            identifier = f'shared-gateway-{i // 25}'
        query_id = identifier
        if rng.random() < rotation_rate:
            query_id = f'rotated-{i}'
        queries.append((query_id, zone))
        for s in range(3):
            if rng.random() < dropout_rate:
                continue
            observed_zone = zone
            if rng.random() < sensor_error:
                observed_zone = f'zone-{(int(zone.split("-")[1]) + rng.randrange(1, n_zones)) % n_zones}'
            obs_time = 10000 + rng.randint(-clock_jitter, clock_jitter)
            observations.append((identifier, observed_zone, f'sensor-{i}-{s}', obs_time))
    by_identifier = defaultdict(list)
    for identifier, zone, sensor, t in observations:
        if abs(t - 10000) <= window:
            by_identifier[identifier].append((zone, sensor))
    correct = false = abstained = 0
    for identifier, truth in queries:
        support = defaultdict(set)
        for zone, sensor in by_identifier.get(identifier, []):
            support[zone].add(sensor)
        choice = next(iter(support)) if len(support) == 1 and len(next(iter(support.values()))) >= 2 else None
        if choice is None:
            abstained += 1
        elif choice == truth:
            correct += 1
        else:
            false += 1
    resolved = correct + false
    return {'seed': seed, 'population': population, 'collision_rate': collision_rate,
            'dropout_rate': dropout_rate, 'clock_jitter_seconds': clock_jitter,
            'rotation_rate': rotation_rate, 'sensor_error_rate': sensor_error,
            'correct': correct, 'false': false, 'abstained': abstained,
            'precision_when_resolved': correct/resolved if resolved else None,
            'coverage': resolved/population, 'false_association_rate': false/population,
            'abstention_rate': abstained/population}

def benchmark(population=2000, seeds=(101, 202, 303, 404, 505)):
    scenarios = {
        'clean': dict(collision_rate=0, dropout_rate=0, clock_jitter=0, rotation_rate=0, sensor_error=0),
        'moderate_noise': dict(collision_rate=.1, dropout_rate=.15, clock_jitter=30, rotation_rate=.1, sensor_error=.05),
        'severe_noise': dict(collision_rate=.35, dropout_rate=.4, clock_jitter=180, rotation_rate=.3, sensor_error=.2)}
    results = {}
    for label, options in scenarios.items():
        records = [run(seed=s, population=population, **options) for s in seeds]
        resolved = sum(r['correct']+r['false'] for r in records)
        total = population * len(records)
        results[label] = {'per_seed': records,
            'aggregate': {'population_total': total,
                'correct': sum(r['correct'] for r in records),
                'false': sum(r['false'] for r in records),
                'abstained': sum(r['abstained'] for r in records),
                'precision_when_resolved': sum(r['correct'] for r in records)/resolved if resolved else None,
                'coverage': resolved/total,
                'false_association_rate': sum(r['false'] for r in records)/total}}
    return {'design': 'synthetic only; sensor independence assumed; not geolocation evidence',
            'scenarios': results}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--population', type=int, default=2000)
    parser.add_argument('--output')
    args = parser.parse_args()
    if not 1 <= args.population <= 100000:
        parser.error('population must be 1..100000')
    results = benchmark(population=args.population)
    serialized = json.dumps(results, indent=2) + '\n'
    if args.output:
        with open(args.output, 'w') as stream:
            stream.write(serialized)
    for name, item in results['scenarios'].items():
        a = item['aggregate']
        print(f"{name}: correct={a['correct']}, false={a['false']}, abstain={a['abstained']}, coverage={a['coverage']:.3f}, precision={a['precision_when_resolved']:.3f}")

if __name__ == '__main__':
    main()
