"""Offline synthetic provenance robustness tests; no camera or networking operations."""
import hashlib, hmac, json
KEY=b"fixed-demo-only-key"

def sign(value, key=KEY):
    msg=json.dumps(value,sort_keys=True,separators=(",",":")).encode()
    return hmac.new(key,msg,hashlib.sha256).hexdigest()

def verify(value,signature,key=KEY):
    return hmac.compare_digest(sign(value,key),signature)

def run_cases():
    source=[{"seq":i,"tick_ms":i*40,"scene":f"scene-{i}","encoding":"raw"} for i in range(8)]
    signature=sign(source)
    transcoded=[{**f,"encoding":"h264"} for f in source]
    canonical=lambda frames:[{"seq":f["seq"],"tick_ms":f["tick_ms"],"scene":f["scene"]} for f in frames]
    canonical_sig=sign(canonical(source))
    transit_archive=[dict(x) for x in source]
    transit_archive[3]["scene"]="substituted"
    recorder_archive=[dict(x) for x in source]
    recorder_archive[3]["scene"]="substituted"
    shifted=[{**x,"tick_ms":x["tick_ms"]+3600000} for x in source]
    normalized=[{**x,"tick_ms":x["tick_ms"]-3600000} for x in shifted]
    altered=[dict(x) for x in source]
    altered[3]["scene"]="substituted"
    forged_signature=sign(altered,KEY)
    return {
      "legitimate_transcode":{"raw_signature_valid":verify(transcoded,signature),"canonical_signature_valid":verify(canonical(transcoded),canonical_sig)},
      "missing_intermediate":{"two_distinct_causes_identical_archive":transit_archive==recorder_archive,"location_identifiable_from_archive":False},
      "clock_offset":{"raw_signature_valid":verify(shifted,signature),"calibrated_signature_valid":verify(normalized,signature)},
      "compromised_key":{"forged_record_validates":verify(altered,forged_signature),"provenance_assured":False}
    }
if __name__=="__main__":print(json.dumps(run_cases(),indent=2,sort_keys=True))
