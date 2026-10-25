"""Private read-only viewer for authorized local camera recordings."""
import argparse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote, urlsplit

HTML = """<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Local camera recording review</title>
<style>body{font:16px system-ui;background:#101827;color:#f4f7ff;margin:2rem}
h1{font-size:1.5rem}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:14px}
article{background:#1b2840;padding:12px;border-radius:12px}video{width:100%;background:black}
small{color:#a9b8cb}</style><h1>Authorized recording review</h1><p>Offline file playback · no camera access</p>
<div class="grid"><article><h3>Main stream</h3><video controls preload="metadata" src="/main.mp4"></video></article>
<article><h3>Substream</h3><video controls preload="metadata" src="/sub.mp4"></video></article>
<article><h3>Transcoded</h3><video controls preload="metadata" src="/main_transcoded.mp4"></video></article>
<article><h3>Modified (red box)</h3><video controls preload="metadata" src="/main_modified.mp4"></video></article>
<article><h3>Remuxed</h3><video controls preload="metadata" src="/main_remux.mp4"></video></article></div>
<p><small>Press play on each panel to compare. Browser controls are independent; clips aren't time-synchronized.</small></p></html>"""

def serve(directory,port):
    root=Path(directory).resolve()
    if not root.is_dir():raise ValueError("directory does not exist")
    names={"main.mp4","sub.mp4","main_transcoded.mp4","main_modified.mp4","main_remux.mp4"}
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            name=unquote(urlsplit(self.path).path).removeprefix("/")
            if name=="":
                data=HTML.encode()
                self.send_response(200)
                self.send_header("Content-Type","text/html; charset=utf-8")
                self.send_header("Cache-Control","no-store")
                self.send_header("Content-Length",str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            if name not in names or not (root/name).is_file():
                self.send_error(404)
                return
            return super().do_GET()
        def translate_path(self,path):
            return str(root/unquote(urlsplit(path).path).removeprefix("/"))
        def end_headers(self):
            self.send_header("X-Content-Type-Options","nosniff")
            self.send_header("Cache-Control","no-store")
            super().end_headers()
        def log_message(self,fmt,*args):
            pass
    httpd=ThreadingHTTPServer(("127.0.0.1",port),Handler)
    print(f"Viewer: http://127.0.0.1:{port}",flush=True)
    try:httpd.serve_forever()
    except KeyboardInterrupt:pass
    finally:httpd.server_close()

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--directory",default="local_recordings/viewer")
    p.add_argument("--port",type=int,default=18766)
    args=p.parse_args();serve(args.directory,args.port)
if __name__=="__main__":main()
