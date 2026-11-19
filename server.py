"""
JTBD Disruptor - local server.

Serves index.html and forwards AI requests to the Anthropic API.
The API key stays on your machine (in .env), never in the browser.

Run:  python3 server.py
Open: http://localhost:8000
"""
import json
import os
import urllib.error
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent


def load_env():
    """Read KEY=VALUE lines from .env into environment variables."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5-5")
MAX_TOKENS = int(os.environ.get("MAX_TOKENS", "4000"))
PORT = int(os.environ.get("PORT", "8000"))


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def send_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/claude":
            return self.send_json(404, {"error": "Not found"})
        if not API_KEY:
            return self.send_json(500, {"error": "ANTHROPIC_API_KEY missing. Add it to the .env file and restart."})

        length = int(self.headers.get("Content-Length", 0))
        prompt = json.loads(self.rfile.read(length) or b"{}").get("prompt", "")
        if not prompt:
            return self.send_json(400, {"error": "Empty prompt"})

        request = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=json.dumps({
                "model": MODEL,
                "max_tokens": MAX_TOKENS,
                "messages": [{"role": "user", "content": prompt}],
            }).encode(),
            headers={
                "Content-Type": "application/json",
                "x-api-key": API_KEY,
                "anthropic-version": "2023-06-01",
            },
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as resp:
                data = json.loads(resp.read())
            text = "".join(b.get("text", "") for b in data.get("content", []) if b.get("type") == "text")
            self.send_json(200, {"text": text})
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")
            try:
                detail = json.loads(detail)["error"]["message"]
            except Exception:
                pass
            self.send_json(e.code, {"error": f"Anthropic API: {detail}"})
        except Exception as e:
            self.send_json(502, {"error": f"Request failed: {e}"})


if __name__ == "__main__":
    print(f"JTBD Disruptor running at http://localhost:{PORT}  (model: {MODEL})")
    if not API_KEY:
        print("WARNING: ANTHROPIC_API_KEY is not set. Copy .env.example to .env and add your key.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
