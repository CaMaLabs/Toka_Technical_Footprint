"""Integration tests use locally generated video, never live cameras."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from src.video_integrity import compare

@unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'), 'FFmpeg required')
class VideoIntegrityTests(unittest.TestCase):
    def test_remux_and_modified(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference, remux, modified = (root / name for name in
                ('original.mp4', 'remux.mkv', 'modified.mp4'))
            def ff(*args):
                subprocess.run(['ffmpeg', '-nostdin', '-v', 'error', '-y', *map(str, args)],
                               check=True, capture_output=True, timeout=90)
            ff('-f', 'lavfi', '-i', 'testsrc2=size=160x120:rate=8', '-t', '2',
               '-c:v', 'mpeg4', reference)
            # Use H.264 in a separate pass to test bitstream extraction.
            h264 = root / 'h264.mp4'
            ff('-i', reference, '-c:v', 'libx264', h264)
            ff('-i', h264, '-c:v', 'copy', remux)
            ff('-i', h264, '-vf', 'drawbox=x=10:y=10:w=40:h=40:color=red:t=fill',
               '-c:v', 'libx264', modified)
            same = compare(h264, remux)
            self.assertTrue(same['encoded_video_exact_match'])
            self.assertEqual(same['flagged_count'], 0)
            self.assertEqual(same['frames_compared'], 16)
            changed = compare(h264, modified)
            self.assertFalse(changed['encoded_video_exact_match'])
            self.assertGreater(changed['flagged_count'], 0)
            self.assertLess(changed['mean_frame_psnr_db'], 35)

    def test_missing_file(self):
        with self.assertRaises(ValueError):
            compare('/does/not/exist.mp4', '/does/not/exist2.mp4')

if __name__ == '__main__':
    unittest.main()
