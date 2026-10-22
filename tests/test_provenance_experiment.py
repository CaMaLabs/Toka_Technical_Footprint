import unittest
from src.provenance_experiment import simulate,infer,seal,validate
class ProvenanceTests(unittest.TestCase):
 def test_baseline(self):self.assertEqual(infer(simulate('baseline')),'no_divergence_observed')
 def test_transit(self):self.assertEqual(infer(simulate('transit')),'before_or_at_wire_observation')
 def test_recorder(self):self.assertEqual(infer(simulate('recorder')),'between_wire_and_archive')
 def test_cloud(self):self.assertEqual(infer(simulate('cloud')),'between_archive_and_cloud')
 def test_tamper(self):self.assertFalse(validate([{'x':2}],seal([{'x':1}])))
 def test_no_anchor_ambiguity(self):
  self.assertFalse(simulate('transit')['archive_matches_origin'])
  self.assertFalse(simulate('recorder')['archive_matches_origin'])
if __name__=='__main__':unittest.main()
