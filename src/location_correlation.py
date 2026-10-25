"""Offline fictional location-token correlation. No real addresses or coordinates."""
import json
from collections import defaultdict

WINDOW_SECONDS = 120

def correlate(observations, queries, window=WINDOW_SECONDS):
    """Abstain unless a single location has two independent synthetic sensors."""
    out = []
    for q in queries:
        matches = [r for r in observations if r['identifier'] == q['identifier']
                   and abs(r['timestamp'] - q['timestamp']) <= window]
        supporters = defaultdict(set)
        for m in matches:
            supporters[m['location']].add(m['sensor'])
        candidates = {loc: len(sensors) for loc, sensors in sorted(supporters.items())}
        decision = next(iter(candidates)) if len(candidates) == 1 and next(iter(candidates.values())) >= 2 else None
        out.append({'case': q['case'], 'candidates': candidates,
                    'decision': decision, 'status': 'resolved' if decision else 'abstain'})
    return out

def fixtures():
    q = [{'case': c, 'identifier': i, 'timestamp': t} for c, i, t in [
        ('stable','id-A',1000), ('shared_nat','public-gateway-X',1000),
        ('stale','id-C',1000), ('randomized_mac','new-id-D',1000),
        ('single_sensor','id-E',1000), ('conflicting','id-F',1000)]]
    records = [
        {'identifier': i, 'location': loc, 'timestamp': t, 'sensor': s}
        for i, loc, t, s in [
            ('id-A','zone-alpha',990,'sensor-1'),('id-A','zone-alpha',1010,'sensor-2'),
            ('public-gateway-X','zone-alpha',990,'sensor-1'),('public-gateway-X','zone-beta',1005,'sensor-2'),
            ('id-C','zone-alpha',100,'sensor-1'),('id-C','zone-alpha',110,'sensor-2'),
            ('old-id-D','zone-beta',995,'sensor-1'),('old-id-D','zone-beta',1000,'sensor-2'),
            ('id-E','zone-alpha',1000,'sensor-1'),
            ('id-F','zone-alpha',1000,'sensor-1'),('id-F','zone-beta',1000,'sensor-2')]]
    return records,q

def evaluate():
    observations, queries = fixtures()
    results = correlate(observations, queries)
    expected = {'stable':'zone-alpha'}
    return {'cases':results,
        'correct_resolution':sum(r['decision']==expected[r['case']] for r in results if r['case'] in expected),
        'false_resolution':sum(r['decision'] is not None for r in results if r['case'] not in expected),
        'abstentions':sum(r['decision'] is None for r in results),
        'note':'Hand-constructed fixtures; descriptive checks, not predictive accuracy.'}

if __name__ == '__main__':
    print(json.dumps(evaluate(), indent=2))
