# Anonymous RTSP and ONVIF packet-delivery milestone — 2026-10-24

**Classification: DEMONSTRATED by operator-supplied Ubuntu lab output.**

Owned lab camera `192.168.1.2`; no `ONVIF_USER` or `ONVIF_PASSWORD` set, and a subsequent script explicitly supplied empty ONVIF credentials. ONVIF `GetProfiles` and `GetStreamUri` succeeded. FFprobe `-rtsp_transport tcp -read_intervals %+3 -show_entries packet=codec_type,pts_time,dts_time,duration_time,size,flags` received media packets from both stream URLs.

| Metric | MainProfile | SubProfile |
|---|---|---|
| Video packets returned | 45 | 47 |
| Audio packets returned | 47 | 48 |
| Video | H.264 1920×1080 | H.264 640×360 |
| Audio | AAC | AAC |
| Reported first video packet duration | 0.066667 s | 0.066667 s |
| Reported first audio packet duration | 0.064000 s | 0.064000 s |
| First video flags | K__ | K__ |
| First audio PTS | -0.051000 | 0.069000 |

This establishes *observed anonymous reception of demuxed video and audio packets* from this particular authorized camera under tested conditions. It does not establish a generalized exploit, a security boundary bypass, or any Toka deployment capability.

**Unresolved:** Earlier recording metadata reported 25 FPS while the new packet duration suggests ~15 FPS; confirm using packet delta statistics and decoded-frame count, not only reported durations. First video PTS absent in output; no absolute wall-clock synchronization demonstrated. RTP header sequence numbers, RTP timestamps, RTCP sender reports, loss, and jitter were not captured. Do not commit full RTSP URIs, stream tokens or audiovisual footage.

**Next experiment:** Read-only per-stream packet timing summary and controlled isolated relay comparison, with independent recording and provenance.
