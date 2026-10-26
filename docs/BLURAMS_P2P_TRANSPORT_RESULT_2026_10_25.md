# Blurams owned-camera P2P UDP framing: observed milestone (2026-10-25)

## Scope and provenance
Authorized local lab: user-owned Blurams camera on Ubuntu NetworkManager Wi-Fi hotspot `wlo1` (10.42.0.1/24), camera 10.42.0.73, and user's cellular phone (public IP confirmed by user as 172.58.117.136). Passive capture analyzed locally at `~/research/Toka_Technical_Footprint/local_recordings/network/blurams_live.pcap`. **The PCAP and raw media are not committed.** Capture snap length was 128 bytes; most UDP payloads were truncated.

## Observed connection
- 10.42.0.73:57601 ↔ 172.58.117.136:34968, UDP, 570 packets, ~326 kB total (approximately 306 kB camera-originating and 20 kB phone-originating), over 24.1 s.
- Additional TLS-bearing TCP to 44.240.235.243:50920 and STUN/classic STUN traffic were observed. Direct UDP media transport is strongly supported; not all individual datagrams are proven video.

## UDP header (large camera-to-phone packets)
- First 4 bytes: `00000000` in all 221 large payload prefixes examined.
- Big-endian bytes 4–7 act as candidate cumulative byte offset; most successive offsets increase 1,284 for a UDP datagram length of 1,316 (minus 8-byte UDP header and 24-byte application header).
- Bytes 16–19 act as a millisecond-rate clock: median absolute error vs capture elapsed time 1.509 ms; median absolute difference of successive timestamp intervals 0.63 ms. 31 of 221 had absolute error >20 ms (maximum 116.923 ms), in clusters. Clock's precise semantics remain unproven.
- Two repeated offsets (42413 and 182369) had identical first 62 application-body bytes but only bytes 18–19 of the UDP application header differed; consistent with retransmission, not proof of full-packet identity because of truncation.

## Inner framing hypothesis and checks
Within the captured data after the candidate 24-byte header, marker `2a3a3f6d` occurs. Candidate record structure:
`[4-byte marker][4-byte field][2-byte big-endian record length][record body of that length]`.
- In 55 candidate records, 28 advertised length 32 and 15 advertised length 160; several longer lengths were seen.
- Eleven captured within-stream marker boundaries fit `10 + 32 = 42` bytes precisely.
- Coverage-aware check: **11 MATCH, 0 MISMATCH, 44 UNOBSERVED**. Only observed comparisons tested; other length classes not confirmed.
- **Eleven** complete 32-byte record bodies recovered. Each begins `0000001c` (28-byte message length), then protobuf-wire-compatible bytes `08 04 2a 18 ...`. A local decoder recovered a nested message: nested field 1 (type) = 1 or 2; field 4 = 33; field 5 varies; field 6 increases but does not track packet arrival time one-to-one.
- Eight type-1 instances: field 5 = 160 in all eight; differences in field 6 between successive type-1 instances divisible by 20 (GCD 20).
- Three type-2 instances: field 5 values 304, 280, 375; two successive field-6 differences 1733 and 5333 (GCD 1). Frame-type and field-6 clock meanings remain hypotheses.
- Following-record validation of the complete 32-byte metadata bodies: **7 FOUND and all 7 following record lengths match the metadata field 5, 0 mismatches, 4 unobservable**. Five type-1 → length 160; two type-2 → lengths 304 and 280. Thus field 5 is strongly supported as the following record body's length.

## Media observations and limits
- HEVC/H.265 Annex B-like NAL signatures found within *individual* captured fragments, including VPS (`000000014001`), SPS (`000000014201`), slice type 1 (`0201`), and SEI type 39 (`4e01`). Recurrent contexts support HEVC-bearing content, but the complete codec configuration is unproven.
- 219 unique offset fragments, 2 repeated offsets (identical captured data prefixes), total 13,578 recovered application bytes over a 278,651-byte offset span (4.87% captured). The remaining 265,073 bytes were **not** captured.
- FFprobe recognized HEVC syntax on partial extracted data but did not recover valid width/height/profile; reported bogus dimensions are parser failures, not actual device specs. **No full media frame or playable recording reconstructed.**
- The original 128-byte-snaplen capture cannot be used to recover missing video data; a new complete capture would be necessary for reliable decode.

## Next offline tests
1. Cross-check the complete 32-byte record fields and nested lengths with a strict wire-format parser; report all field numbers and types without semantic over-interpretation.
2. Validate predicted following record length for all *observable* boundaries and quantify confidence by type.
3. Compare HEVC signatures against stream offsets and records, avoiding concatenation across uncaptured gaps.
4. For decoding actual footage, obtain a separate explicitly authorized, full-snaplen capture in the controlled lab; do not infer missing bytes.

All conclusions are limited to this single owned-device session. No evidence here establishes access to third-party cameras or implementation of any Toka/Cybertoka technique.
