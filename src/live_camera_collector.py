"""Opt-in small private-LAN camera inventory collector. Never runs until --execute."""
import argparse, ipaddress, json, subprocess, tempfile
from pathlib import Path
from src.camera_inventory import parse_nmap, merge, write_db

PORTS = "80,443,554,8554,8000,8080"

def validate_target(value):
    try:
        net = ipaddress.ip_network(value, strict=False)
    except ValueError as e:
        raise ValueError("Enter an explicit RFC1918 IPv4 host or subnet") from e
    blocks = tuple(ipaddress.ip_network(s) for s in ("10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"))
    if net.version != 4 or net.prefixlen < 28 or not any(net.subnet_of(b) for b in blocks):
        raise ValueError("Target must fit entirely within RFC1918, with prefix /28 through /32")
    return str(net)

def collect(target, out, dry_run=True, onvif=None, media=None):
    target = validate_target(target)
    cmd = ["nmap", "-sT", "-sV", "--version-light", "-Pn",
           "--max-retries", "1", "--host-timeout", "45s",
           "-p", PORTS, "-oX", "-", target]
    if dry_run:
        return {"dry_run": True, "command": cmd, "database_written": False}
    result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=240)
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "scan.xml"
        path.write_text(result.stdout)
        records = merge(parse_nmap(path), onvif, media)
        write_db(records, out)
    return {"dry_run": False, "devices": len(records), "database_written": True, "output": str(out)}

def main():
    p = argparse.ArgumentParser(description="Authorized camera inventory collection on small private LAN ranges")
    p.add_argument("--target", required=True, help="Explicit RFC1918 IP or at most /28 network")
    p.add_argument("--out", default="inventory.sqlite")
    p.add_argument("--onvif", help="Pre-exported ONVIF details JSON; no login is attempted")
    p.add_argument("--media", help="Pre-exported FFprobe metadata JSON")
    p.add_argument("--execute", action="store_true", help="Opt in to executing Nmap")
    a = p.parse_args()
    print(json.dumps(collect(a.target, a.out, not a.execute, a.onvif, a.media), indent=2))

if __name__ == "__main__":
    main()
