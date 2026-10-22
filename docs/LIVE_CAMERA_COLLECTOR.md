# Opt-in live camera inventory (small private networks)

This module adds **actual Nmap collection** for a specified camera IP or a small, RFC1918 private subnet (/28–/32). It does not perform cloud searches, credential guessing, exploitation, or stealth operations.

## Setup
```bash
sudo apt-get install nmap
python3 -m src.live_camera_collector --target 192.168.1.50
```
The default prints the exact command and does **not scan**.

To explicitly execute against **your own or authorized** device:
```bash
python3 -m src.live_camera_collector --target 192.168.1.50 --execute --out inventory.sqlite
sqlite3 inventory.sqlite 'SELECT ip,manufacturer,model FROM devices;'
```
Optional `--onvif device_details.json` and `--media media_details.json` import pre-exported metadata in the format in [CAMERA_INVENTORY.md](CAMERA_INVENTORY.md).

**Scope:** fixed common web/RTSP ports, bounded version detection, TCP only; no camera authentication. Private IPs are not proof of authorization. The operator must choose an owned or explicitly authorized target.

**Current limitation:** automatically collects Nmap metadata but **not** ONVIF device information or live FFprobe metadata. Those currently require authorized exports. The importer creates the SQLite inventory using the existing `src.camera_inventory` module.

## Validation
Six dry-run/address-validation tests passed locally in an isolated test harness with the dependency interface stubbed. This is **not** an end-to-end live network scan; test on your own LAN and review the command before executing. Do not commit live `inventory.sqlite` files to this public repository.
