import unittest
from src.location_correlation import correlate, fixtures, evaluate

class Tests(unittest.TestCase):
    def test_all_fixture_outcomes(self):
        rows = {r['case']:r for r in correlate(*fixtures())}
        self.assertEqual(rows['stable']['decision'],'zone-alpha')
        for case in ('shared_nat','stale','randomized_mac','single_sensor','conflicting'):
            self.assertIsNone(rows[case]['decision'],case)
    def test_duplicate_sensor_not_independent(self):
        rows=[{'identifier':'a','location':'one','timestamp':1,'sensor':'same'}]*2
        self.assertIsNone(correlate(rows,[{'case':'dup','identifier':'a','timestamp':1}])[0]['decision'])
    def test_report(self):
        r=evaluate()
        self.assertEqual((r['correct_resolution'],r['false_resolution'],r['abstentions']),(1,0,5))
