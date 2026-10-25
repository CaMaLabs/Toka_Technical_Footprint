# Real-video integrity comparison

The read-only offline tool `src/video_integrity.py` compares two **local** authorized recordings using FFmpeg and ffprobe. It reports complete-file SHA-256, extracted H.264/HEVC bitstream SHA-256 when supported, mean frame PSNR, mean frame SSIM, and heuristic per-frame warnings.

## Run on the Ubuntu workstation

```bash
cd ~/research/Toka_Technical_Footprint
git pull --ff-only
python3 -m unittest discover -s tests -v
mkdir -p results/local
python3 -m src.video_integrity local_recordings/main.mkv local_recordings/validation/main_remux.mp4 --output results/local/remux_comparison.json
python3 -m src.video_integrity local_recordings/main.mkv local_recordings/validation/main_transcoded.mp4 --output results/local/transcoded_comparison.json
python3 -m src.video_integrity local_recordings/main.mkv local_recordings/validation/main_modified.mp4 --output results/local/modified_comparison.json
```

A typical exact remux should have different file hashes but identical extracted bitstream hashes, with no flagged frames. Legitimate transcoding generally changes bitstream hashes, while visual similarity may stay high. A large visible alteration should reduce similarity. Results depend on recording content and alignment.

## Important limitations

- Video is aligned approximately by frame index using normalized presentation times. It does **not** establish the original wall-clock timestamp for flagged frames.
- Missing, inserted or duplicated frames can break alignment or silently limit the comparison to overlapping material.
- The PSNR 35 dB and SSIM 0.95 cutoffs are **warning heuristics**, not experimentally calibrated tamper classifiers; independently inspect each result.
- The 'mean' fields average per-frame results, not necessarily FFmpeg's global pooled PSNR.
- Use a trusted independent reference; similarity cannot prove provenance.
- Keep files, results, RTSP URIs and camera metadata local. This public repository must not contain private recordings or inventories.

## Local validation

An offline FFmpeg smoke test on 16 synthetic frames showed a remuxed H.264 stream matched the original extracted bitstream, while a red-box-modified recording differed and produced similarity warnings. The GitHub Actions test suite can repeat this using FFmpeg in its runner environment, if available. Validate on the real camera recordings separately and record actual output before claiming real-camera test results.
