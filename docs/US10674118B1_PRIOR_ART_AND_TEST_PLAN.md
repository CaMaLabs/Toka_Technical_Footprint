# US10674118B1 — prior art and falsifiable investigation

Status: research plan, not proof of an operational Toka exploit.

Primary patent: https://patents.google.com/patent/US10674118B1/en
Existing claim summary: [PATENT_DISCREET_CAMERA_ACCESS_US10674118B1.md](PATENT_DISCREET_CAMERA_ACCESS_US10674118B1.md)

## Technical finding
The disclosed stream-redirection and replacement mechanism could operate upstream of a recorder. If a recorder archives its received stream, a substituted stream might be present in saved footage *without modifying a stored file afterward*. This is an architectural inference, not evidence of deployed Toka capabilities.

## Competing hypotheses
- H1 — Camera endpoint control: source output differs from an authenticated independent source capture.
- H2 — Intermediary control: source-side authenticated recording and downstream capture differ.
- H3 — Recorder/VMS control: independently authenticated source capture and recorder archive differ.
- H4 — Cloud/archive-only changes: trusted on-prem recordings agree while a downstream cloud copy diverges.

These distinctions require independently trusted observations. Without them, a valid-looking recording cannot identify where a modification occurred.

## Source and code comparison
Track relevant technical concepts in open-source media parsing, but **do not infer reuse**:
- FFmpeg libavformat: https://github.com/FFmpeg/FFmpeg/tree/master/libavformat
- OpenDHFS: https://github.com/OpenDHFS/OpenDHFS
- Untrunc: https://github.com/anthwlock/untrunc

These tools concern format interpretation and/or recovery; none establishes access to devices. Compare against numbered patent claims before reporting an algorithmic match.

## Prior-art review procedure
Review the patent's References Cited section directly and record publication dates, relevant claim language, and whether the cited art concerns interception, stream replacement, recording, timestamp integrity, or generic streaming. A patent citation is not evidence of copied code. Specific cited patents require individual verification before inclusion.

## Offline experiment
1. Generate deterministic synthetic camera-frame records containing payload, monotonic index, timestamp, and origin signature/hash manifest.
2. Construct authorized fixture variants: baseline, altered ingested copy, modified archive copy, and shifted timestamps.
3. Compare archive payload hashes with independently captured source manifests. Test that legitimate transcoding does not cause a misleading attribution.
4. Report true/false positives for each variant. Do not claim localization if the reference and archive share a compromised trust anchor.

No public scanning, unauthorized interception, covert media substitution, or vulnerability exploitation is part of this experiment.

## Progress criteria
- Claim-to-function mapping backed by numbered patent claims.
- Reproducible synthetic validation with control cases and command/output logs.
- OEM / firmware grouping only where public vendor documentation supports a relationship.
- Negative findings retained alongside positive findings.
