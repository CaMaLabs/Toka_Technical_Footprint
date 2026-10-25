"""Read-only inventory of RTSP/ONVIF access boundaries from user-supplied lab logs.

No network operations. No credential guessing. No exploit execution.
"""
import argparse
import json
from pathlib import Path

def summarize(events):
    if not isinstance(events,list):
        raise ValueError("events must be a list")
    results=[]
    for e in events:
        if not isinstance(e,dict):
            raise ValueError("event must be an object")
        operation=e.get("operation")
        status=e.get("status")
        if operation not in ("rtsp_options","rtsp_describe","rtsp_play","onvif_device_info",
                             "onvif_profiles","onvif_stream_uri"):
            raise ValueError("unrecognized operation")
        if status not in ("succeeded","auth_required","denied","unsupported","not_tested"):
            raise ValueError("unrecognized status")
        results.append({"operation":operation,"credential_context":e.get("credential_context","anonymous"),
                        "status":status})
    return {"tests":results,
        "interpretation":"These are operator-supplied outcomes; a returned stream URI does not prove stream playback access.",
        "limits":["A successful OPTIONS response does not prove media access.",
                  "One profile's result does not establish permissions for other profiles.",
                  "Do not publish access tokens or camera-specific RTSP URIs."]}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input",help="JSON array of manually observed results")
    p.add_argument("--output")
    a=p.parse_args()
    result=json.dumps(summarize(json.loads(Path(a.input).read_text())),indent=2)+"\n"
    if a.output:Path(a.output).write_text(result)
    print(result,end="")

if __name__=="__main__":main()
