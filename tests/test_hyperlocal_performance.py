import unittest
from src.hyperlocal_performance import measure

class HyperlocalPerformanceTests(unittest.TestCase):
    def test_index_matches_full_scan(self):
        result=measure(n=100,seed=11,queries=5)
        self.assertTrue(result['match_counts_verified'])
        self.assertEqual(result['devices'],100)
        self.assertGreater(result['inserts_per_second'],0)
