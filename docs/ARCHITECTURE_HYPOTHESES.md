# Architecture hypotheses and falsifiers

## Separate five stages
1. Geographic *selection* — a map, installation directory, or other coarse region-of-interest index.
2. Device *discovery* — exposed service listings or authorized inventory, not a proof of access.
3. Device *identification* — network/metadata fingerprints or OEM/firmware mapping.
4. *Access* — separate authentication, permission, or vulnerability question; method unknown.
5. Media *processing* — reading/reconstructing streams; archived data modification is an independent, unproven capability.

## Candidate access paths (HYPOTHESIS only)
- Central recorder or video-management server.
- Cloud-management credentials or services.
- Shared OEM software/firmware components.
- Weak deployment configuration or exposed interfaces.
- Individual device vulnerabilities.

No ranking is experimentally supported by this repository. A single central recorder can administer many cameras, but that does not establish that Toka actually uses it.

## What would falsify a universal-exploit theory?
Demonstrations of different device families requiring independent access methods, or geographic discovery without access. Distinguish a vendor's coverage claim from a controlled compatibility test.

## Defensive lab experiment
Use only owned/synthetic camera data, local NVR storage, independent timestamped capture and archive-hash verification. A mismatch after an authorized archive edit localizes which output changed; it does not attribute intrusion techniques to any named company.
