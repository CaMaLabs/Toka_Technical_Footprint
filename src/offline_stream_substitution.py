"""Offline controlled simulation of camera footage substitution.

Consumes a user-owned local source recording; NEVER connects to a camera/network.
The middle interval is visibly labeled as laboratory replacement in the manifest.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

def sha(path):
    d=hashlib.sha256()
    with open(path,"rb") as stream:
        for block in iter(lambda:stream.read(1024*1024),b""):
            d.update(block)
    return d.hexdigest()

def simulate(source, output, mode="replay", seconds=2):
    source,output=Path(source),Path(output)
    if not source.is_file():raise ValueError("source must be an existing local video")
    if source.resolve()==output.resolve():raise ValueError("never overwrite source")
    if mode not in ("replay","blank","marked_overlay"):
        raise ValueError("invalid mode")
    if not 1<=seconds<=10:raise ValueError("seconds must be 1..10")
    details=json.loads(subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
        "-show_entries","stream=width,height,r_frame_rate:format=duration",
        "-of","json",str(source)],check=True,capture_output=True,text=True).stdout)
    if not details.get("streams"):raise ValueError("source contains no video")
    duration=float(details.get("format",{}).get("duration",0))
    if duration<seconds*3:raise ValueError("source must contain at least three intervals")
    # Three independent segments; the middle is the controlled replacement.
    a=f"[0:v]trim=start=0:end={seconds},setpts=PTS-STARTPTS,format=yuv420p[a]"
    c=f"[0:v]trim=start={seconds*2}:end={seconds*3},setpts=PTS-STARTPTS,format=yuv420p[c]"
    if mode=="blank":
        w,h=details["streams"][0]["width"],details["streams"][0]["height"]
        middle=f"color=c=black:size={w}x{h}:rate=25:d={seconds},format=yuv420p[b]"
    elif mode=="replay":
        middle=f"[0:v]trim=start=0:end={seconds},setpts=PTS-STARTPTS,format=yuv420p[b]"
    else:
        middle=(f"[0:v]trim=start={seconds}:end={seconds*2},setpts=PTS-STARTPTS,"
                "format=yuv420p,drawbox=x=20:y=20:w=240:h=80:color=red:t=fill[b]")
    graph=";".join([a,middle,c,"[a][b][c]concat=n=3:v=1:a=0[v]"])
    output.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-nostdin","-hide_banner","-v","error","-y","-i",str(source),
        "-filter_complex",graph,"-map","[v]","-an","-c:v","libx264","-preset","veryfast",
        "-crf","23",str(output)],check=True,timeout=180)
    report={"simulation_only":True,"mode":mode,
        "segment_seconds":seconds,
        "segments":[{"start":0,"end":seconds,"content":"original"},
          {"start":seconds,"end":seconds*2,"content":mode},
          {"start":seconds*2,"end":seconds*3,"content":"original"}],
        "source_sha256":sha(source),"output_sha256":sha(output),
        "conclusion":"Offline substituted-file simulation. No stream interception or third-party access."}
    report_path=output.with_suffix(".manifest.json")
    report_path.write_text(json.dumps(report,indent=2)+"\n")
    return report

def main():
    p=argparse.ArgumentParser()
    p.add_argument("source");p.add_argument("output")
    p.add_argument("--mode",choices=["blank","replay","marked_overlay"],default="replay")
    p.add_argument("--seconds",type=int,default=2)
    a=p.parse_args()
    print(json.dumps(simulate(a.source,a.output,a.mode,a.seconds),indent=2))

if __name__=="__main__":main()
