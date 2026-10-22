# Owned-Camera Research Toolkit

**Purpose:** assemble verifiable open-source components to examine **owned or explicitly authorized** cameras and isolated surveillance pipelines. This is a hypothesis-driven functional toolkit, **not a list of tools confirmed to be used by Toka**. No exploit chain, stealth access, or live-path interception is bundled.

## Tool catalog and relevance
| Component | Public source | Function | Toka relationship |
|---|---|---|---|
| Nmap | https://nmap.org/book/man-version-detection.html | Inventory/services on an authorized LAN | Conceptually adjacent to US10523549B1; reuse unverified |
| Wireshark / tshark | https://www.wireshark.org/ | Inspect *authorized* saved packet captures, RTP timing and RTSP metadata | Network-analysis analogy only |
| FFmpeg / ffprobe | https://ffmpeg.org/ffprobe.html | Decode, transcode, examine metadata/streams from local recordings or authorized media URLs | Media-processing analogy only |
| MediaMTX | https://github.com/bluenviron/mediamtx | Standalone lab RTSP publisher/reader/recorder | Demonstrates legitimate video routing; no Toka attribution |
| GStreamer | https://gstreamer.freedesktop.org/ | Controlled local media pipelines and format experiments | Functional alternative |
| ONVIF reference/specifications | https://www.onvif.org/profiles/ | Standards-oriented camera capability and interoperability research | Useful for device family mapping |
| OpenDHFS | https://github.com/OpenDHFS/OpenDHFS | Proprietary DVR footage analysis (verify formats supported per revision) | Candidate format-analysis analogy |
| Untrunc | https://github.com/anthwlock/untrunc | Recovery of damaged MP4 containers | Adjacent forensic capability only |

**Caution:** tool selection follows publicly documented features, not direct evidence of Toka's stack. Camera firmware and OEM attribution must be backed by vendor publications or firmware analyses.

## Quick local test — no camera needed
Requires `ffmpeg`, `ffprobe`, Python 3. Produces three seconds of synthetic test-pattern footage and a transcoded copy:
```bash
bash scripts/create_video_fixtures.sh
python3 scripts/inspect_recording.py fixtures/lab_original.mp4 fixtures/lab_transcoded.mp4
python3 -m unittest discover -s tests -v
```
The inspector reports stream metadata plus whole-file SHA-256 for each file. Do not interpret differing file hashes alone as evidence of manipulated visual content.

## Working with your own cameras
1. Confirm ownership/authorization; document make, model, firmware version and ONVIF/RTSP capabilities **through the camera's own admin interface**.
2. Export a short recording via the manufacturer's supported export workflow. Store originals read-only; do not put private camera footage or credentials in this public repository.
3. Run the local inspector on copies; record codec, timestamps and cryptographic hashes.
4. If conducting a live pipeline study, set up an isolated VLAN with your devices and a **deliberately configured** MediaMTX lab server. Use authenticated, voluntary RTSP routing. Do not impersonate devices or redirect production surveillance traffic.
5. Use an independent recording or source-side signed reference to test provenance questions.

## Findings to pursue
- Can normal transcoding explain any observed hash differences? (Almost always for raw file hashes.)
- Does the NVR preserve device-provided timestamps, or rewrite on ingest?
- Are recorder and camera clocks independently anchored?
- Do multiple camera brands use the same disclosed OEM and firmware family?

## Limitations
No claim that any of these tools can access locked cameras, overcome authentication, edit archives remotely, or reproduce Toka's exploitation capability. Never make an inference about compromise solely from model/OEM similarity.
