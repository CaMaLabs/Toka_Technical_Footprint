# ONVIF live device identification

`src/onvif_collect.py` makes an opt-in, single-address ONVIF **GetDeviceInformation** request on an owned RFC1918 camera. Default is dry-run. It returns IP, manufacturer, model, firmware and hardware identifier; it intentionally omits serial numbers, credentials and stream URLs.

```bash
python3 -m src.onvif_collect --ip 192.168.1.50
# Enable network request, and save locally:
python3 -m src.onvif_collect --ip 192.168.1.50 --execute --out onvif_local.json
# Join with an Nmap export into the existing SQLite inventory:
python3 -m src.camera_inventory --nmap scan.xml --onvif onvif_local.json --out inventory.sqlite
```

For cameras requiring HTTP Digest authentication, set ONVIF_USER and ONVIF_PASSWORD in your local environment. Do **not** commit credentials, inventory databases or exports to this public repository. Some devices use WS-Security instead of Digest, a different service path, or HTTPS, and will not work with this initial implementation. The script does not guess passwords, bypass authentication, or discover targets. Only use it on your own or explicitly authorized cameras.

Local validation: five tests passed against synthetic SOAP responses and address checks. No real-camera end-to-end test has been performed.
