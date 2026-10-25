# US11212308B1 — Location identification through network-log correlation

**Evidence: PRIMARY patent disclosure; actual Toka implementation not verified.**

- Assignee: Cybertoka Ltd.
- Filed: 2020-12-31; granted: 2021-12-28.
- Inventors: Alon Kantor, Moty Zaltzman, Sofia Belikovetsky, Reut Roich.
- Primary source: https://patents.google.com/patent/US11212308B1/en

## Disclosed technique

The patented architecture receives logs from devices carrying **network identifiers** and **location information**, correlates target identifiers with network observations, and infers a location for a networked device. Identifiers discussed include local/public IP addresses, MAC addresses, network SSIDs and Bluetooth information; location signals may be associated with devices elsewhere on the network. Timestamps can restrict matches to particular intervals and support location-type classification.

This could help explain geographic indexing of devices behind NAT where IP geolocation alone is insufficient. It does **not** establish access to any particular data feed, universal camera geolocation, or exploitation of target devices.

## Relationship to prior patents

- US10523549B1 covers device discovery/classification.
- US11212308B1 covers location identification by network-log correlation.
- US10674118B1 discloses interception and stream substitution.
- These may conceptually describe complementary functions, but patent ownership alone does not prove they are implemented together.

## Falsifiable privacy-preserving offline research

Generate synthetic, clearly fictional device observations with intentionally unambiguous/non-identifying keys, associated location tokens, and timestamps. Evaluate false correlations when identifiers are reused behind NAT, randomized, stale, or shared among multiple devices. Test missing logs, false observations and location uncertainty. Never collect third-party wireless identifiers or geolocate unconsenting real devices.

**Research priority:** examine independent claims and data provenance. Distinguish location prediction from access control, which remains unresolved.
