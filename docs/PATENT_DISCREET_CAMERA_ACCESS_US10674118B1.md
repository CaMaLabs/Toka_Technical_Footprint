# US10674118B1 — discreet access to security camera systems

**Evidence class: PRIMARY (patent disclosure), not independently demonstrated deployment.**

- Title: *Method and system for discreetly accessing security camera systems*
- Assignee: CYBERTOKA Ltd.
- Filed: 2019-05-01; granted/published: 2020-06-02
- Inventors: Micha Kalfon, Sofia Belikovetsky, Shimi Gersner, Roi Leibovich, Michael Volfman, Alon Kantor
- Full patent: https://patents.glgoo.top/patent/US10674118B1/en
- Additional patent index: https://patents.justia.com/inventor/roi-leibovich

## Main claims, summarized (not verbatim)

The patent has 17 numbered claims. Independent method claim **1** describes responding to a selectable trigger, identifying and intercepting a media stream headed to an original destination, redirecting that stream elsewhere, delivering replacement media to the original destination, and supplying a timestamp different from the original interception time.

Independent **system claim 11** describes processor-executed modules for a corresponding workflow. Another independent claim covers computer-readable storage containing the relevant instructions.

Dependent claims discuss audio/video content, an alternate source connection, simulated environmental appearance (including light/weather), real-time operation, and maintaining camera-to-monitoring-center connection continuity.

## Access discussion in the description

The patent's description explicitly contemplates obtaining access by physical camera access before/after installation **or** exploiting camera software/hardware vulnerabilities, and discusses positioning the control system with access to the camera, monitoring center, or communication path. It does **not** identify a specific zero-day, vulnerability identifier, exploit source code, or proof of use against real systems.

## Architectural implication

The claim is consistent with **in-path media substitution** that could deceive the recorder/monitoring destination without necessarily editing a saved file in place. Whether an archive contains substituted content depends on its recording path. This is meaningfully more specific than an assumption that cloud storage itself was compromised.

## Defensive research questions

- What checks can distinguish source-originated media from substituted downstream media?
- Can independent camera-side authentication and an independent recording channel expose mismatches?
- What timestamp and provenance discrepancies survive recorder-side ingestion?

Only use prerecorded, synthetic fixtures or explicitly owned local test systems. No third-party targeting, traffic interception, or manipulation.

## Interpretation limits

Patent rights/disclosure are not a product manual. Patent publication does not establish a functioning deployment, reliability, vendor compatibility, or unrestricted real-world access. Do not treat claimed interception and substitution as verified observation.
