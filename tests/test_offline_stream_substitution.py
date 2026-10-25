import shutil
import subprocess
import tempfile
from pathlib import Path
import unittest
from src.offline_stream_substitution import simulate

class OfflineSubstitutionTests(unittest.TestCase):
    def test_source_required(self):
        with self.assertRaises(ValueError):
            simulate('/does/not/exist.mkv','/tmp/no.mp4')
    @unittest.skipUnless(shutil.which('ffmpeg') and shutil.which('ffprobe'),'FFmpeg required')
    def test_three_modes_and_source_preservation(self):
        with tempfile.TemporaryDirectory() as folder:
            src=Path(folder)/'source.mp4'
            subprocess.run(['ffmpeg','-nostdin','-v','error','-y','-f','lavfi','-i',
                            'testsrc2=size=160x120:rate=25','-t','6','-c:v','mpeg4',
                            str(src)],check=True,timeout=60)
            baseline=src.read_bytes()
            for mode in ('replay','blank','marked_overlay'):
                out=Path(folder)/(mode+'.mp4')
                result=simulate(src,out,mode,seconds=2)
                self.assertTrue(out.is_file())
                self.assertTrue(out.with_suffix('.manifest.json').is_file())
                self.assertEqual(result['segments'][1]['content'],mode)
                self.assertEqual(src.read_bytes(),baseline)
if __name__=='__main__':
    unittest.main()
