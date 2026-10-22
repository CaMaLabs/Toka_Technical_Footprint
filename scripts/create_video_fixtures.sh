#!/usr/bin/env bash
set -euo pipefail
command -v ffmpeg >/dev/null || { echo "ffmpeg required" >&2; exit 1; }
mkdir -p fixtures
ffmpeg -hide_banner -loglevel error -y -f lavfi -i testsrc2=size=320x240:rate=15 -t 3 -c:v mpeg4 -q:v 4 fixtures/lab_original.mp4
ffmpeg -hide_banner -loglevel error -y -i fixtures/lab_original.mp4 -c:v mpeg4 -q:v 7 fixtures/lab_transcoded.mp4
echo "Created local synthetic files under fixtures/"
