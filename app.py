#!/usr/bin/env python3
"""
TikSaver — TikTok Video Downloader (website + API for the Android app).

Routes:
  GET  /                -> the web page (paste a TikTok link, get the video)
  POST /api/resolve     -> JSON metadata for a TikTok link (used by web + app)
  GET  /download?url=   -> downloads the video and returns it as an mp4 file

Only TikTok links are supported. Videos are fetched fresh for every
request with yt-dlp and streamed to the visitor; nothing is stored.
Config: PORT env var (default 8090).
"""
import os
import re
import subprocess
import sys
import tempfile

# --- Sandbox egress CA shim: on Muse's VM all traffic goes through an
# egress proxy whose CA must be added to certifi for yt-dlp. On normal
# hosting this file does not exist and the shim is a no-op.
_EGRESS_CA = "/run/hatch/egress-tls/ca-bundle.pem"
if os.path.exists(_EGRESS_CA):
    try:
        import certifi
        bundle = certifi.where()
        with open(_EGRESS_CA, "rb") as fh:
            extra = fh.read()
        with open(bundle, "rb") as fh:
            current = fh.read()
        if extra[:64] not in current:
            with open(bundle, "ab") as fh:
                fh.write(extra)
    except Exception:
        pass

from flask import Flask, Response, jsonify, request, send_file

from webui import INDEX_HTML

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YTDLP = os.path.join(BASE_DIR, "venv", "bin", "yt-dlp")
if not os.path.exists(YTDLP):
    YTDLP = "yt-dlp"

app = Flask(__name__)

URL_RE = re.compile(r"https?://[^\s]+")
TIKTOK_DOMAINS = ("tiktok.com", "vm.tiktok.com", "vt.tiktok.com")


def extract_url(text):
    m = URL_RE.search(text or "")
    return m.group(0).strip() if m else None


def is_tiktok(url):
    return bool(url) and any(d in url for d in TIKTOK_DOMAINS)


def ytdlp_json(url):
    """Return info dict for a TikTok URL via yt-dlp -J."""
    cmd = [YTDLP, "--no-playlist", "--no-warnings", "-J", url]
    out = subprocess.run(cmd, check=True, timeout=120,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    import json
    return json.loads(out.stdout.decode("utf-8", "ignore"))


def download_file(url, workdir):
    out = os.path.join(workdir, "video.%(ext)s")
    cmd = [YTDLP, "--no-playlist", "--no-warnings",
           "-f", "bv*[height<=720][ext=mp4]+ba[ext=m4a]/b[height<=720][ext=mp4]/b[ext=mp4]/b",
           "--merge-output-format", "mp4", "-o", out, url]
    subprocess.run(cmd, check=True, timeout=300,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for name in os.listdir(workdir):
        if name.startswith("video."):
            return os.path.join(workdir, name)
    raise RuntimeError("no file produced")


def safe_name(title):
    name = re.sub(r"[^\w\- ]+", "", (title or "tiktok-video")).strip()[:60]
    return (name or "tiktok-video") + ".mp4"


@app.route("/")
def home():
    return Response(INDEX_HTML, mimetype="text/html")


@app.route("/api/resolve", methods=["POST"])
def resolve():
    data = request.get_json(silent=True) or {}
    url = extract_url(data.get("url") or request.form.get("url") or "")
    if not is_tiktok(url):
        return jsonify({"ok": False,
                        "error": "Please paste a valid TikTok link."}), 400
    try:
        info = ytdlp_json(url)
    except subprocess.CalledProcessError:
        return jsonify({"ok": False,
                        "error": "Could not fetch this video. It may be private or the link is wrong."}), 422
    except Exception:
        return jsonify({"ok": False,
                        "error": "Something went wrong. Please try again."}), 500
    from urllib.parse import quote
    return jsonify({
        "ok": True,
        "title": info.get("title") or "TikTok video",
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader"),
        "download": f"/download?url={quote(url, safe='')}",
    })


@app.route("/download")
def download():
    url = extract_url(request.args.get("url") or "")
    if not is_tiktok(url):
        return "Invalid TikTok link.", 400
    tmp = tempfile.mkdtemp(prefix="tiksaver-")
    try:
        path = download_file(url, tmp)
        title = None
        try:
            title = ytdlp_json(url).get("title")
        except Exception:
            pass
        return send_file(path, as_attachment=True,
                         download_name=safe_name(title),
                         mimetype="video/mp4")
    except subprocess.CalledProcessError:
        return "Could not download this video. It may be private or the link is wrong.", 422
    except Exception:
        return "Something went wrong. Please try again.", 500


@app.route("/health")
def health():
    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8090")),
            threaded=True)
