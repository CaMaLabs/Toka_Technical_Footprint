# Patent-to-code comparison: research plan

## US10523549B1: verified high-level mechanism
1. Obtain a network response that includes a content-length characteristic.
2. Classify the device into a preliminary category.
3. Issue a protocol-specific request and classify again using returned content.
4. Optional evidence sources described include packet observation and infrastructure logs.

### Comparison targets
- Nmap's service detection: https://nmap.org/book/vscan.html
- Wireshark dissectors: https://www.wireshark.org/docs/
These are **analogues**, not evidence of copied code or common authorship. No network scanning is implemented in this repository.

## US10511648B1: media reconstruction
Earlier research associated this patent with reconstruction of proprietary media streams, but its **numbered claims and precise method still need line-by-line verification**. The comparison remains provisional.

### Candidate reference implementations
- FFmpeg libavformat: https://github.com/FFmpeg/FFmpeg/tree/master/libavformat
- OpenDHFS: https://github.com/OpenDHFS/OpenDHFS
- Untrunc: https://github.com/anthwlock/untrunc

### Questions to test
- Does a format use recognizable boundaries/magic bytes?
- Are unknown headers stripped, or is the payload actually decoded?
- Can intact frame payloads be recovered with known framing?
- Which metadata is necessary to preserve ordering and timestamps?

These are distinct tasks: demultiplexing, decoding, recovering damaged containers, and altering archival evidence. **None implies the others automatically.**

## Comparison matrix
| Idea | Patent support | Candidate code | Attribution |
|---|---|---|---|
| Response-length classification | US10523549B1 description | Nmap-style device/service detection (conceptual only) | No evidence of reuse |
| Multi-stage protocol identification | US10523549B1 description | Network dissectors / identification logic | No evidence of reuse |
| Proprietary media reconstruction | US10511648B1 (precise claims pending) | FFmpeg / OpenDHFS | No evidence of reuse |
| Broken container recovery | Not confirmed as patent claim | Untrunc | No evidence of reuse |
| Unauthorized access / archive rewrite | Not demonstrated by either patent | None identified | Unknown |

**Experiment:** local synthetic byte stream in `src/framing_lab.py` shows the limited case of locating and extracting framed bytes. This does not reproduce the patent or operate on camera streams.
