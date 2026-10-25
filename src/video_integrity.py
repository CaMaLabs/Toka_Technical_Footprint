"""Offline, read-only comparison of two local videos using FFmpeg."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile

def command(args):
    return subprocess.run(args, check=True, capture_output=True, text=True, timeout=180)

def hash_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as stream:
        for chunk in iter(lambda: stream.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def probe(path):
    data = json.loads(command(['ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=codec_name,width,height,avg_frame_rate,nb_frames:format=duration',
        '-of', 'json', str(path)]).stdout)
    if not data.get('streams'):
        raise ValueError('No video stream in ' + str(path))
    return data['streams'][0]

def bitstream_hash(path, codec):
    fmt = {'h264': 'h264', 'hevc': 'hevc'}.get(codec)
    if not fmt:
        return None
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-i', str(path), '-map',
        '0:v:0', '-c:v', 'copy', '-f', fmt, '-'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    h = hashlib.sha256()
    for chunk in iter(lambda: proc.stdout.read(1048576), b''):
        h.update(chunk)
    error = proc.stderr.read()
    if proc.wait(timeout=180):
        raise RuntimeError(error.decode(errors='replace'))
    return h.hexdigest()

def metrics(reference, candidate, kind, stats):
    graph = ('[0:v]setpts=PTS-STARTPTS,format=yuv420p[a];'
             '[1:v]setpts=PTS-STARTPTS,format=yuv420p[b];'
             f'[a][b]{kind}=stats_file={stats}')
    command(['ffmpeg', '-nostdin', '-hide_banner', '-v', 'error',
        '-i', str(reference), '-i', str(candidate),
        '-filter_complex', graph, '-an', '-f', 'null', '-'])
    pattern = r'psnr_avg:([^ ]+)' if kind == 'psnr' else r'All:([^ ]+)'
    result = []
    for line in Path(stats).read_text().splitlines():
        match = re.search(pattern, line)
        if match:
            value = float(match.group(1))
            result.append(value if math.isfinite(value) else None)
    return result

def compare(reference, candidate, psnr_warning=35.0, ssim_warning=0.95):
    reference, candidate = Path(reference), Path(candidate)
    if not reference.is_file() or not candidate.is_file():
        raise ValueError('Both inputs must be existing local files')
    a, b = probe(reference), probe(candidate)
    if (a['width'], a['height']) != (b['width'], b['height']):
        raise ValueError('Resolution mismatch: explicitly align before comparison')
    hashes = [bitstream_hash(reference, a['codec_name']),
              bitstream_hash(candidate, b['codec_name'])]
    with tempfile.TemporaryDirectory() as tmp:
        psnr = metrics(reference, candidate, 'psnr', str(Path(tmp) / 'psnr.log'))
        ssim = metrics(reference, candidate, 'ssim', str(Path(tmp) / 'ssim.log'))
    if not psnr or len(psnr) != len(ssim):
        raise ValueError('No comparable frames or inconsistent metric counts')
    flagged = [{'frame_index_1based': i+1, 'psnr_db': p, 'ssim': s}
        for i, (p, s) in enumerate(zip(psnr, ssim))
        if (p is not None and p < psnr_warning) or (s is not None and s < ssim_warning)]
    def average(values):
        values = [v for v in values if v is not None]
        return sum(values)/len(values) if values else None
    exact = hashes[0] is not None and hashes[0] == hashes[1]
    return {
        'sha256': {'reference': hash_file(reference), 'candidate': hash_file(candidate)},
        'encoded_video_sha256': {'reference': hashes[0], 'candidate': hashes[1]},
        'encoded_video_exact_match': exact,
        'video': {'reference': a, 'candidate': b},
        'frames_compared': len(psnr),
        'mean_frame_psnr_db': average(psnr),
        'mean_frame_ssim': average(ssim),
        'warning_thresholds': {'psnr_db': psnr_warning, 'ssim': ssim_warning},
        'flagged_frames': flagged, 'flagged_count': len(flagged),
        'interpretation': 'same extracted encoded video' if exact else
            'differences observed; authenticity indeterminate',
        'limitations': [
            'Frames aligned by index/normalized PTS, not by independently verified time',
            'Missing or extra frames can cause misalignment or silently truncate comparison',
            'Warnings are heuristic, not validated tampering classifications',
            'Metrics cannot establish authenticity without a trusted reference'
        ]
    }

def main():
    parser = argparse.ArgumentParser(description='Compare two authorized local video recordings')
    parser.add_argument('reference'); parser.add_argument('candidate')
    parser.add_argument('--output'); parser.add_argument('--psnr-warning', type=float, default=35)
    parser.add_argument('--ssim-warning', type=float, default=0.95)
    args = parser.parse_args()
    result = json.dumps(compare(args.reference, args.candidate,
        args.psnr_warning, args.ssim_warning), indent=2) + '\n'
    if args.output:
        Path(args.output).write_text(result)
    print(result, end='')

if __name__ == '__main__':
    main()
