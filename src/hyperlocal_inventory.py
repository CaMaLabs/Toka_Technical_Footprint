"""Authorized hyperlocal inventory: localhost dashboard, opt-in ingestion, SQLite R-tree."""
import argparse
import hmac
import json
import math
import os
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

FEET_PER_METER = 3.280839895
EARTH_METERS = 6371008.8
RADIUS_FEET = 50.0
HTML = """<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Hyperlocal authorized inventory</title>
<style>body{background:#101827;color:#eff6ff;font:16px system-ui;margin:2rem auto;max-width:850px;padding:0 1rem}
h1{font-size:1.6rem}small{color:#9cabc0}table{width:100%;border-collapse:collapse}td,th{padding:12px;border-bottom:1px solid #344154;text-align:left}
.status{color:#80efbc}.error{color:#ff9f9f}code{color:#bbcbff}</style>
<h1>Hyperlocal authorized device inventory</h1>
<p>50-foot radius · <b>opt-in records only</b> · No wireless or network scanning</p>
<p id="summary">Connecting…</p><table><thead><tr><th>Device</th><th>Type</th><th>Distance</th><th>Last seen</th><th>Source</th></tr></thead><tbody id="rows"></tbody></table>
<small>Refreshes every 2 seconds. Coordinates come from user-provided installation records, not measured device positions.</small>
<script>
async function update(){
try{
const response=await fetch('/api/devices',{cache:'no-store'});
if(!response.ok)throw Error('HTTP '+response.status);
const data=await response.json();
document.getElementById('summary').textContent=data.devices.length+' device(s) within 50 feet · '+data.label;
const tbody=document.getElementById('rows');tbody.replaceChildren();
for(const d of data.devices){
const tr=document.createElement('tr');
for(const value of [d.name,d.kind,d.distance_feet.toFixed(1)+' ft',
new Date(d.seen_at*1000).toLocaleTimeString(),d.source]){
const td=document.createElement('td');td.textContent=value;tr.append(td);
}tbody.append(tr);}
}catch(e){document.getElementById('summary').textContent='Connection failed: '+e.message;}
}
update();setInterval(update,2000);
</script></html>"""

def validate_location(lat, lon):
    if not all(math.isfinite(v) for v in (lat, lon)) or not -90 <= lat <= 90 or not -180 <= lon <= 180:
        raise ValueError('invalid latitude or longitude')

def meters_between(a, b, c, d):
    p1,p2=math.radians(a),math.radians(c)
    dp=math.radians(c-a);dl=math.radians(d-b)
    h=math.sin(dp/2)**2+math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*EARTH_METERS*math.asin(min(1,math.sqrt(h)))

def connect(path):
    db=sqlite3.connect(path,timeout=10)
    db.execute('PRAGMA busy_timeout=10000')
    db.execute('CREATE TABLE IF NOT EXISTS devices (id INTEGER PRIMARY KEY, key TEXT UNIQUE NOT NULL, name TEXT NOT NULL, kind TEXT NOT NULL, lat REAL NOT NULL, lon REAL NOT NULL, source TEXT NOT NULL, seen_at REAL NOT NULL)')
    db.execute('CREATE VIRTUAL TABLE IF NOT EXISTS geo_index USING rtree(id,min_lat,max_lat,min_lon,max_lon)')
    db.commit()
    return db

def ingest(db, device):
    required=('key','name','kind','lat','lon','source')
    if not isinstance(device,dict) or any(k not in device for k in required):
        raise ValueError('missing required fields')
    if any(not isinstance(device[k],str) or not 1<=len(device[k])<=100 for k in ('key','name','kind','source')):
        raise ValueError('invalid identifying field')
    if isinstance(device['lat'],bool) or isinstance(device['lon'],bool):
        raise ValueError('invalid coordinates')
    lat,lon=float(device['lat']),float(device['lon'])
    validate_location(lat,lon)
    now=time.time()
    with db:
        db.execute("""INSERT INTO devices (key,name,kind,lat,lon,source,seen_at)
         VALUES (?,?,?,?,?,?,?) ON CONFLICT(key) DO UPDATE SET
         name=excluded.name,kind=excluded.kind,lat=excluded.lat,lon=excluded.lon,
         source=excluded.source,seen_at=excluded.seen_at""",
         (device['key'],device['name'],device['kind'],lat,lon,device['source'],now))
        ident=db.execute('SELECT id FROM devices WHERE key=?',(device['key'],)).fetchone()[0]
        db.execute('INSERT OR REPLACE INTO geo_index VALUES (?,?,?,?,?)',(ident,lat,lat,lon,lon))
    return ident

def nearby(db, center_lat, center_lon, radius_feet=RADIUS_FEET):
    validate_location(center_lat,center_lon)
    radius_m=radius_feet/FEET_PER_METER
    delta_lat=math.degrees(radius_m/EARTH_METERS)
    cos=math.cos(math.radians(center_lat))
    delta_lon=180 if abs(cos)<1e-9 else min(180,math.degrees(radius_m/(EARTH_METERS*abs(cos))))
    if delta_lon>=180:
        rows=db.execute('SELECT id,key,name,kind,lat,lon,source,seen_at FROM devices').fetchall()
    else:
        rows=db.execute("""SELECT d.id,d.key,d.name,d.kind,d.lat,d.lon,d.source,d.seen_at
            FROM geo_index g JOIN devices d ON g.id=d.id
            WHERE g.max_lat>=? AND g.min_lat<=? AND g.max_lon>=? AND g.min_lon<=?""",
            (center_lat-delta_lat,center_lat+delta_lat,center_lon-delta_lon,center_lon+delta_lon)).fetchall()
    result=[]
    for ident,key,name,kind,lat,lon,source,seen in rows:
        distance=meters_between(center_lat,center_lon,lat,lon)*FEET_PER_METER
        if distance<=radius_feet:
            result.append(dict(key=key,name=name,kind=kind,source=source,
                               distance_feet=round(distance,3),seen_at=seen))
    return sorted(result,key=lambda r:r['distance_feet'])

def seed(db, lat, lon):
    for key,name,kind,east,north in [
        ('demo-camera','Demo camera','camera',12,0),
        ('demo-hub','Demo hub','gateway',-18,9),
        ('demo-sensor','Demo sensor','environment',31,22),
        ('demo-outside','Out of range','camera',75,0)]:
        y=lat+math.degrees((north/FEET_PER_METER)/EARTH_METERS)
        x=lon+math.degrees((east/FEET_PER_METER)/(EARTH_METERS*max(1e-6,abs(math.cos(math.radians(lat))))))
        ingest(db,dict(key=key,name=name,kind=kind,lat=y,lon=x,source='synthetic-demo'))

def serve(args):
    if not args.token:
        raise SystemExit('Set --token or HYPERLOCAL_TOKEN for opt-in updates')
    Path(args.db).parent.mkdir(parents=True,exist_ok=True)
    db=connect(args.db)
    if args.seed:
        seed(db,args.lat,args.lon)
    db.close()
    class Handler(BaseHTTPRequestHandler):
        def respond(self,status,obj):
            raw=json.dumps(obj).encode()
            self.send_response(status)
            self.send_header('Content-Type','application/json')
            self.send_header('Cache-Control','no-store')
            self.send_header('Content-Length',str(len(raw)))
            self.end_headers();self.wfile.write(raw)
        def do_GET(self):
            path=urlsplit(self.path).path
            if path=='/':
                raw=HTML.encode()
                self.send_response(200)
                self.send_header('Content-Type','text/html; charset=utf-8')
                self.send_header('Content-Length',str(len(raw)))
                self.end_headers();self.wfile.write(raw)
            elif path=='/api/devices':
                with connect(args.db) as connection:
                    devices=nearby(connection,args.lat,args.lon)
                self.respond(200,dict(label=args.label,center=dict(lat=args.lat,lon=args.lon),radius_feet=50,devices=devices))
            else:self.respond(404,dict(error='not found'))
        def do_POST(self):
            if urlsplit(self.path).path!='/api/ingest':
                return self.respond(404,dict(error='not found'))
            if not hmac.compare_digest(self.headers.get('X-Inventory-Token',''),args.token):
                return self.respond(403,dict(error='invalid token'))
            try:
                length=int(self.headers.get('Content-Length','0'))
                if not 0<length<=8192:raise ValueError('invalid payload size')
                data=json.loads(self.rfile.read(length))
                with connect(args.db) as connection:
                    ident=ingest(connection,data)
                self.respond(200,dict(accepted=True,id=ident))
            except (ValueError,TypeError,UnicodeDecodeError,json.JSONDecodeError) as e:
                self.respond(400,dict(error=str(e)))
        def log_message(self,fmt,*values):
            pass
    print('Open http://127.0.0.1:%s  (%s; 50-foot radius)'%(args.port,args.label),flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()

def main():
    p=argparse.ArgumentParser(description='Local authorized hyperlocal inventory (no scanning)')
    p.add_argument('--lat',type=float,required=True);p.add_argument('--lon',type=float,required=True)
    p.add_argument('--label',default='Authorized site')
    p.add_argument('--port',type=int,default=8765)
    p.add_argument('--db',default='hyperlocal_local.sqlite')
    p.add_argument('--token',default=os.environ.get('HYPERLOCAL_TOKEN'))
    p.add_argument('--seed',action='store_true',help='insert fictional nearby devices')
    a=p.parse_args();validate_location(a.lat,a.lon);serve(a)

if __name__=='__main__':
    main()
