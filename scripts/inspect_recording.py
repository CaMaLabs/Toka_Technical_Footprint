"""Inspect local video files only; never opens network URLs or writes source footage."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def inspect(path: str):
    f = Path(path)
    if not f.is_file():
        raise ValueError("must be an existing local file")
    data = f.read_bytes()
    p = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries",
         "format=duration,format_name:stream=index,codec_name,codec_type,width,height,avg_frame_rate",
         "-of", "json", str(f)],
        check=True, capture_output=True, text=True, timeout=30
    )
    return {"path": str(f), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(),
            "probe": json.loads(p.stdout)}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 scripts/inspect_recording.py LOCAL_FILE [...]")
    print(json.dumps([inspect(s) for s in sys.argv[1:]], indent=2))
