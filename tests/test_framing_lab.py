import unittest
from src.framing_lab import frame, recover


class FramingTests(unittest.TestCase):
    def test_two_records_with_leading_noise(self):
        self.assertEqual(recover(b"noise" + frame(b"one") + frame(b"two")), [b"one", b"two"])

    def test_truncated_record(self):
        self.assertEqual(recover(frame(b"hello")[:-1]), [])

    def test_empty_payload(self):
        self.assertEqual(recover(frame(b"")), [b""])

    def test_length_limit(self):
        with self.assertRaises(ValueError):
            frame(b"x" * 65536)


if __name__ == "__main__":
    unittest.main()
