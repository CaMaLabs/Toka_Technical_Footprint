# Camera access and stream-substitution lab

Source: https://patents.google.com/patent/US10674118B1/en

The patent discusses camera feed redirection and delivery of substitute blank, prerecorded, or timestamp-modified streams to the monitoring destination. This is a patented architecture, **not evidence of an actual Toka exploit or deployed code**.

Distinguish: (1) discovery and credentials, (2) obtaining RTSP/ONVIF media, (3) encoded H.264 packet copying, (4) decoded pixel modification, (5) independent recorder/monitor substitution.

## Offline, authorized reproduction

Use only generated test video. The simulation outputs an original/replacement/original recording plus a manifest. It does not intercept camera connections or impersonate a media destination.

```bash
cd ~/research/Toka_Technical_Footprint
git pull --ff-only
source .venv/bin/activate
python3 -W error::ResourceWarning -m unittest discover -s tests -v
mkdir -p results/local
ffmpeg -hide_banner -loglevel error -y -f lavfi -i testsrc2=size=320x240:rate=25 -t 6 -c:v libx264 results/local/synthetic_6s.mp4
for mode in blank replay marked_overlay; do
  python3 -m src.offline_stream_substitution results/local/synthetic_6s.mp4 "results/local/sim_${mode}.mp4" --mode "$mode" --seconds 2
  python3 -m src.video_integrity results/local/synthetic_6s.mp4 "results/local/sim_${mode}.mp4" --output "results/local/comparison_${mode}.json" >/dev/null
done
```

Expected middle intervals: blank = black frames; replay = earlier frames from the same fixture; marked_overlay = red region. Original source is unchanged. Compare output hashes and frame PSNR/SSIM. This is a media-effect demonstration, not a live RTSP attack simulation.

## Passive access-evidence report

```bash
cat > results/local/access_observations.json <<'JSON'
[
 {"operation":"rtsp_options","credential_context":"anonymous","status":"succeeded"},
 {"operation":"onvif_device_info","credential_context":"anonymous","status":"succeeded"},
 {"operation":"onvif_profiles","credential_context":"anonymous","status":"succeeded"},
 {"operation":"onvif_stream_uri","credential_context":"anonymous","status":"succeeded"},
 {"operation":"rtsp_describe","credential_context":"anonymous","status":"not_tested"},
 {"operation":"rtsp_play","credential_context":"anonymous","status":"not_tested"}
]
JSON
python3 -m src.camera_access_audit results/local/access_observations.json --output results/local/access_report.json
```

Review whether every stated credential context actually matches the observed request. The tool only summarizes user-provided observations and never accesses the network. Do not commit sensitive RTSP URIs, credentials or real footage.

## Research gaps

- ONVIF GetStreamUri is not proof a DESCRIBE/PLAY request is authorized.
- Raw encoded bitstreams differ from decoded video pixels. Video replacement can require re-encoding while remux does not.
- Offline editing cannot demonstrate covert live redirection, connection continuity or compromise.
- Future isolated authorized experiments may compare publisher-side captures with viewer-side substitution, keeping independent cryptographic evidence.
