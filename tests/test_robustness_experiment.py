import unittest
from src.robustness_experiment import run_cases

class RobustnessTests(unittest.TestCase):
    def setUp(self): self.r=run_cases()
    def test_transcode_raw(self): self.assertFalse(self.r["legitimate_transcode"]["raw_signature_valid"])
    def test_transcode_canonical(self): self.assertTrue(self.r["legitimate_transcode"]["canonical_signature_valid"])
    def test_missing_identical(self): self.assertTrue(self.r["missing_intermediate"]["two_distinct_causes_identical_archive"])
    def test_missing_unlocalizable(self): self.assertFalse(self.r["missing_intermediate"]["location_identifiable_from_archive"])
    def test_clock_raw(self): self.assertFalse(self.r["clock_offset"]["raw_signature_valid"])
    def test_clock_normalized(self): self.assertTrue(self.r["clock_offset"]["calibrated_signature_valid"])
    def test_key_forgery_validates(self): self.assertTrue(self.r["compromised_key"]["forged_record_validates"])
    def test_key_not_assured(self): self.assertFalse(self.r["compromised_key"]["provenance_assured"])
