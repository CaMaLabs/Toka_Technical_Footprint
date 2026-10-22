"""Opt-in ONVIF Device Management query for one RFC1918 owned camera."""
import argparse,ipaddress,json,os,urllib.request,xml.etree.ElementTree as ET
SOAP=b'''<?xml version="1.0"?><s:Envelope xmlns:s="http://www.w3.org/2003/05/soap-envelope" xmlns:d="http://www.onvif.org/ver10/device/wsdl"><s:Body><d:GetDeviceInformation/></s:Body></s:Envelope>'''
def target_ip(value):
 ip=ipaddress.ip_address(value)
 nets=[ipaddress.ip_network(s) for s in ("10.0.0.0/8","172.16.0.0/12","192.168.0.0/16")]
 if ip.version!=4 or not any(ip in n for n in nets):raise ValueError("Requires explicit RFC1918 IPv4 camera")
 return str(ip)
def parse_device_info(data):
 root=ET.fromstring(data)
 body=next((e for e in root.iter() if e.tag.split("}")[-1]=="Body"),None)
 response=next((e for e in body.iter() if e.tag.split("}")[-1]=="GetDeviceInformationResponse"),None) if body is not None else None
 if response is None:raise ValueError("No ONVIF DeviceInformation response")
 fields={e.tag.split("}")[-1]:(e.text or "").strip() for e in response.iter()}
 return {v:fields[k] for k,v in (("Manufacturer","manufacturer"),("Model","model"),("FirmwareVersion","firmware"),("HardwareId","hardware_id")) if k in fields}
def query(ip,port=80):
 ip=target_ip(ip)
 if port not in (80,8000,8080,8899):raise ValueError("Unsupported ONVIF port")
 url=f"http://{ip}:{port}/onvif/device_service"
 opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
 user,password=os.environ.get("ONVIF_USER"),os.environ.get("ONVIF_PASSWORD")
 if user and password:
  manager=urllib.request.HTTPPasswordMgrWithDefaultRealm()
  manager.add_password(None,url,user,password)
  opener.add_handler(urllib.request.HTTPDigestAuthHandler(manager))
 request=urllib.request.Request(url,SOAP,{"Content-Type":"application/soap+xml; charset=utf-8"},method="POST")
 with opener.open(request,timeout=5) as response: data=response.read(65536)
 return {"ip":ip,**parse_device_info(data)}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--ip",required=True);p.add_argument("--port",type=int,default=80)
 p.add_argument("--execute",action="store_true");p.add_argument("--out")
 a=p.parse_args();ip=target_ip(a.ip)
 if not a.execute:
  print(json.dumps({"dry_run":True,"ip":ip,"port":a.port,"query":"ONVIF GetDeviceInformation"}));return
 result=[query(ip,a.port)];output=json.dumps(result,indent=2)
 if a.out:
  from pathlib import Path
  Path(a.out).write_text(output+"\n")
 print(output)
if __name__=="__main__":main()
