import unittest
from src.location_benchmark import run, benchmark

class LocationBenchmarkTests(unittest.TestCase):
    def test_clean_data_is_exact(self):
        result = run(seed=101, population=200, collision_rate=0,
                     dropout_rate=0, clock_jitter=0, rotation_rate=0, sensor_error=0)
        self.assertEqual(result['correct'], 200)
        self.assertEqual(result['false'], 0)
        self.assertEqual(result['abstained'], 0)

    def test_accounting_and_determinism(self):
        a=run(seed=505, population=400, collision_rate=.2, sensor_error=.1)
        b=run(seed=505, population=400, collision_rate=.2, sensor_error=.1)
        self.assertEqual(a,b)
        self.assertEqual(a['correct']+a['false']+a['abstained'],400)

    def test_multi_seed_aggregation(self):
        r=benchmark(population=100,seeds=(1,2))
        for scenario in r['scenarios'].values():
            agg=scenario['aggregate']
            self.assertEqual(agg['correct']+agg['false']+agg['abstained'],200)
