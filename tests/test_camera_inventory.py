import json,sqlite3,tempfile,unittest
from pathlib import Path
from src.camera_inventory import parse_nmap,merge,write_db
XML='<nmaprun><host><address addr="192.168.50.12" addrtype="ipv4"/><ports><port protocol="tcp" portid="554"><state state="open"/><service name="rtsp"/></port></ports></host><host><address addr="8.8.8.8" addrtype="ipv4"/></host></nmaprun>'
class CameraInventoryTest(unittest.TestCase):
 def test_offline_merge(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);(p/"nmap.xml").write_text(XML)
   (p/"onvif.json").write_text(json.dumps([{"ip":"192.168.50.12","manufacturer":"FixtureCo","model":"Synthetic","firmware":"1"}]))
   (p/"media.json").write_text(json.dumps([{"ip":"192.168.50.12","probe":{"streams":[{"codec_name":"h264"}]}}]))
   data=merge(parse_nmap(p/"nmap.xml"),p/"onvif.json",p/"media.json")
   self.assertEqual(list(data),["192.168.50.12"])
   self.assertEqual(data["192.168.50.12"]["onvif"]["model"],"Synthetic")
   self.assertEqual(data["192.168.50.12"]["media"][0]["codec_name"],"h264")
   write_db(data,p/"db.sqlite");con=sqlite3.connect(p/"db.sqlite")
   self.assertEqual(con.execute("SELECT COUNT(*) FROM devices").fetchone()[0],1)
   con.close()
