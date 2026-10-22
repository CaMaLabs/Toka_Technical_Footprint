"""Offline merger of authorized Nmap XML, ONVIF JSON and ffprobe JSON."""
import argparse,ipaddress,json,sqlite3,xml.etree.ElementTree as ET
from pathlib import Path

def private_ip(value):
 try:
  ip=ipaddress.ip_address(value)
  return ip.is_private and not ip.is_loopback and not ip.is_link_local
 except ValueError:return False

def parse_nmap(path):
 records={}
 for host in ET.parse(path).getroot().findall("host"):
  ip=next((a.get("addr") for a in host.findall("address") if a.get("addrtype")=="ipv4"),None)
  if not ip or not private_ip(ip):continue
  ports=[]
  for p in host.findall("./ports/port"):
   state=p.find("state")
   if state is None or state.get("state")!="open":continue
   s=p.find("service")
   ports.append({"port":int(p.get("portid")),"protocol":p.get("protocol"),"service":s.get("name","") if s is not None else "","product":s.get("product","") if s is not None else ""})
  records[ip]={"ip":ip,"ports":ports,"onvif":{},"media":[]}
 return records

def merge(records,onvif_path=None,media_path=None):
 if onvif_path:
  for row in json.loads(Path(onvif_path).read_text()):
   ip=row.get("ip","")
   if ip in records:records[ip]["onvif"]={k:row[k] for k in ("manufacturer","model","firmware","hardware_id","serial") if k in row}
 if media_path:
  for row in json.loads(Path(media_path).read_text()):
   ip=row.get("ip","")
   if ip in records:
    for s in row.get("probe",{}).get("streams",[]):
     records[ip]["media"].append({k:s[k] for k in ("codec_name","codec_type","width","height","avg_frame_rate") if k in s})
 return records

def write_db(records,path):
 con=sqlite3.connect(path)
 try:
  with con:
   con.execute("CREATE TABLE IF NOT EXISTS devices (ip TEXT PRIMARY KEY,manufacturer TEXT,model TEXT,firmware TEXT,hardware_id TEXT,services_json TEXT,media_json TEXT)")
   for r in records.values():
    o=r["onvif"]
    con.execute("INSERT OR REPLACE INTO devices VALUES (?,?,?,?,?,?,?)",(r["ip"],o.get("manufacturer"),o.get("model"),o.get("firmware"),o.get("hardware_id"),json.dumps(r["ports"]),json.dumps(r["media"])))
 finally:con.close()

def main():
 p=argparse.ArgumentParser(description="Offline authorized-camera inventory (no network activity)")
 p.add_argument("--nmap",required=True);p.add_argument("--onvif");p.add_argument("--media")
 p.add_argument("--out",default="inventory.sqlite");p.add_argument("--dry-run",action="store_true")
 a=p.parse_args();rows=merge(parse_nmap(a.nmap),a.onvif,a.media)
 if not a.dry_run:write_db(rows,a.out)
 print(json.dumps({"devices":len(rows),"ips":sorted(rows),"written":not a.dry_run},indent=2))
if __name__=="__main__":main()
