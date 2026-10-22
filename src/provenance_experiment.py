"""Offline surveillance provenance experiment. Synthetic records only."""
import hashlib,hmac,json
KEY=b'lab-only-provenance-key'
def digest(s): return hashlib.sha256(s.encode()).hexdigest()
def seal(frames):
 msg=json.dumps(frames,sort_keys=True,separators=(',',':')).encode()
 return hmac.new(KEY,msg,hashlib.sha256).hexdigest()
def validate(frames,signature):return hmac.compare_digest(seal(frames),signature)
def simulate(kind):
 source=[{'seq':i,'tick':i*40,'content':digest(f'frame:{i}')} for i in range(8)]
 signed_origin=seal(source)
 wire=[dict(f) for f in source]; archive=[dict(f) for f in wire]; cloud=[dict(f) for f in archive]
 if kind=='transit':
  wire[3]['content']=digest('replacement');archive=[dict(f) for f in wire];cloud=[dict(f) for f in archive]
 elif kind=='recorder':
  archive[3]['content']=digest('replacement');cloud=[dict(f) for f in archive]
 elif kind=='cloud':cloud[3]['content']=digest('replacement')
 elif kind!='baseline':raise ValueError(kind)
 return dict(case=kind,origin_valid=validate(source,signed_origin),wire_matches_origin=validate(wire,signed_origin),archive_matches_origin=validate(archive,signed_origin),cloud_matches_origin=validate(cloud,signed_origin),wire_matches_archive=wire==archive,archive_matches_cloud=archive==cloud)
def infer(r):
 if not r['wire_matches_origin']:return 'before_or_at_wire_observation'
 if not r['archive_matches_origin']:return 'between_wire_and_archive'
 if not r['cloud_matches_origin']:return 'between_archive_and_cloud'
 return 'no_divergence_observed'
def main():
 rows=[]
 for case in ['baseline','transit','recorder','cloud']:
  r=simulate(case);r['inferred_boundary']=infer(r)
  r['archive_only_can_localize']=False if case!='baseline' else None
  rows.append(r)
 print(json.dumps(rows,indent=2))
if __name__=='__main__':main()
