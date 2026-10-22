# Local camera inventory merger

Combines **existing, authorized** Nmap XML, manually collected ONVIF device information, and ffprobe results into an SQLite inventory. This code performs **no active scanning**, ONVIF authentication or stream requests; collection of ONVIF data and ffprobe annotations is still manual.

## Example
Run Nmap separately only against an explicitly approved private camera IP (illustrative example):
```bash
nmap -sT -sV -p 80,443,554,8554 -oX scan.xml 192.168.50.12
python3 -m src.camera_inventory --nmap scan.xml --dry-run
python3 -m src.camera_inventory --nmap scan.xml --onvif device_details.json --media media_details.json --out inventory.sqlite
sqlite3 inventory.sqlite 'SELECT ip,manufacturer,model,firmware FROM devices;'
```
Example `device_details.json`:
```json
[{"ip":"192.168.50.12","manufacturer":"Example Vendor","model":"Test Camera","firmware":"1.0","hardware_id":"board-A"}]
```
Example `media_details.json`:
```json
[{"ip":"192.168.50.12","probe":{"streams":[{"codec_type":"video","codec_name":"h264","width":1920,"height":1080}]}}]
```
**Do not commit** live network inventories, camera credentials, internal IPs, or actual footage to this public repository. The merger drops public-address results and never stores stream URL fields, but a private IP itself may still be sensitive.

## Current limitations
No automated ONVIF queries, MAC vendor lookup, chipset inference, CIDR scanning, or cloud-based internet-wide discovery. Hardware family correlation requires separate sourced OEM evidence, not guessed equivalence. Duplicate IP observations overwrite prior records.
