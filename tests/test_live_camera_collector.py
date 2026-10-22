import unittest
from unittest.mock import patch
from src.live_camera_collector import validate_target, collect

class CollectorTests(unittest.TestCase):
    def test_private_host(self):
        self.assertEqual(validate_target("192.168.10.4"), "192.168.10.4/32")
    def test_small_subnet(self):
        self.assertEqual(validate_target("10.0.0.0/28"), "10.0.0.0/28")
    def test_public_denied(self):
        with self.assertRaises(ValueError):
            validate_target("8.8.8.8")
    def test_large_subnet_denied(self):
        with self.assertRaises(ValueError):
            validate_target("192.168.1.0/24")
    def test_loopback_denied(self):
        with self.assertRaises(ValueError):
            validate_target("127.0.0.1")
    @patch("src.live_camera_collector.subprocess.run")
    def test_dry_run_never_executes(self, run):
        result = collect("192.168.10.4", "unused.sqlite")
        self.assertTrue(result["dry_run"])
        run.assert_not_called()
