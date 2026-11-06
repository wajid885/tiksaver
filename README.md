# TikSaver — TikTok Video Downloader (Website)

Paste a TikTok link → get the video as an MP4 without watermark.
Same backend also serves the TikSaver Android app (`/api/resolve`).

## Run locally
```
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
PORT=8090 ./venv/bin/python app.py
```
Open http://localhost:8090

## Deploy on Render (free)
1. Put this folder in a GitHub repo.
2. Render → New → Web Service → connect the repo. Render reads
   `render.yaml` (Docker, free plan) and deploys automatically.
3. Free services sleep when idle; the first visit after sleep takes
   ~1 minute to wake up.

## Notes
- Only TikTok links are supported (`tiktok.com`, `vm.tiktok.com`,
  `vt.tiktok.com`).
- Videos are fetched fresh per request with yt-dlp and streamed to
  the visitor; nothing is stored on the server.
- For personal use; respect the original creators' rights.
