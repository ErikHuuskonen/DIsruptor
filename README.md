# JTBD Disruptor

Enter a product → get its Jobs To Be Done → choose a disruptive strategy → get 5 very different, scored business ideas that make the original product obsolete.

## Structure

```
Disruptor/
├── index.html      # the whole app (UI + prompts)
├── server.py       # local server: serves the page, calls the Anthropic API
├── .env.example    # template for your settings
├── .env            # your API key (NOT committed)
└── README.md
```

## Run locally

Requires Python 3 (built into macOS). No packages to install.

```bash
cp .env.example .env        # then put your API key in .env
python3 server.py
```

Open http://localhost:8000

## Where to edit

| What | Where |
|---|---|
| Look and colors | `<style>` in `index.html` |
| JTBD analysis prompt | `analyzeJTBD()` in `index.html` |
| Business idea prompt | `generateDisruptors()` in `index.html` |
| Strategy buttons | `.strategy-chips` in `index.html` |
| Model / token limit | `.env` |

After editing `index.html`, just refresh the browser. After editing `server.py` or `.env`, restart the server (Ctrl+C, then `python3 server.py`).
