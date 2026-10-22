# Toka Technical Footprint

Open, evidence-first research into public technical disclosures associated with Cybertoka Ltd. / Toka and defensive verification of surveillance media integrity.

## Purpose
- Catalog primary-source patents and documented claims.
- Compare disclosed ideas with existing open-source implementations **without attributing code reuse without evidence**.
- Model *geographic discovery*, *device identification*, *access*, *media processing*, and *tamper detection* as distinct stages.
- Build **offline, synthetic-fixture experiments**, not scanning or intrusion tools.

## Start here
- [Evidence register](docs/EVIDENCE_REGISTER.md)
- [Patent comparison](docs/PATENT_COMPARISON.md)
- [Discreet camera access patent — US10674118B1](docs/PATENT_DISCREET_CAMERA_ACCESS_US10674118B1.md)
- [Researcher and open-source leads](docs/RESEARCH_LEADS.md)
- [Architecture hypotheses](docs/ARCHITECTURE_HYPOTHESES.md)
- [Offline stream-framing fixture](src/framing_lab.py), [tests](tests/test_framing_lab.py)

## Run
```bash
python3 -m unittest discover -s tests -v
python3 -m src.framing_lab
```
Standard-library-only; no network activity or device access.

## Evidence policy
Use `PRIMARY` for patent text or vendor-authored documents, `REPORTED` for attributable journalism or external studies, `DEMONSTRATED` only for reproducible results, and `HYPOTHESIS` for technical inference. Similarity of function does **not** imply source-code reuse or common ownership.

## Safety and scope
Only analyze public sources, authorized recordings, and locally generated fixtures. Do not collect location-specific live camera targets, credentials, exploits, or unauthorized streams. No claims of real-world compromises.
