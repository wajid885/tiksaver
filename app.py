#!/usr/bin/env python3
"""
TikSaver — Video Downloader (website + API for the Android app).

Routes:
  GET  /                -> the web page (paste a link, get the video)
  POST /api/resolve     -> JSON metadata for a link (used by web + app)
  GET  /download?url=&quality=hd|sd -> the video as an mp4 file
  GET  /mp3?url=        -> the audio of the video as an mp3 file
  GET  /about /privacy /dmca -> info pages
  GET  /api/stats       -> {"downloads": N} counter
  GET  /health          -> {"ok": true}

Supported: TikTok (full), Instagram and Facebook (best effort — those
platforms often block server requests or require login for some posts).
Videos are fetched fresh for every request with yt-dlp and streamed to
the visitor; nothing is stored except a simple download counter.
Config: PORT env var (default 8090).
"""
import os
import re
import subprocess
import sys
import tempfile
import threading

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

from webui import ABOUT_HTML, DMCA_HTML, INDEX_HTML, PRIVACY_HTML

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YTDLP = os.path.join(BASE_DIR, "venv", "bin", "yt-dlp")
if not os.path.exists(YTDLP):
    YTDLP = "yt-dlp"

app = Flask(__name__)

URL_RE = re.compile(r"https?://[^\s]+")
TIKTOK_DOMAINS = ("tiktok.com", "vm.tiktok.com", "vt.tiktok.com")
INSTAGRAM_DOMAINS = ("instagram.com",)
FACEBOOK_DOMAINS = ("facebook.com", "fb.watch", "fb.com")

# ---------------- download counter (simple file, survives restarts of
# the process but may reset when the host redeploys — free-tier limit).
COUNT_FILE = os.path.join(BASE_DIR, "counter.txt")
_count_lock = threading.Lock()


def get_count():
    try:
        with open(COUNT_FILE) as fh:
            return int(fh.read().strip() or 0)
    except Exception:
        return 0


def bump_count():
    with _count_lock:
        n = get_count() + 1
        try:
            with open(COUNT_FILE, "w") as fh:
                fh.write(str(n))
        except Exception:
            pass
        return n


# ---------------- helpers -------------------------------------------------
def extract_url(text):
    m = URL_RE.search(text or "")
    return m.group(0).strip() if m else None


def platform_of(url):
    if not url:
        return None
    if any(d in url for d in TIKTOK_DOMAINS):
        return "TikTok"
    if any(d in url for d in INSTAGRAM_DOMAINS):
        return "Instagram"
    if any(d in url for d in FACEBOOK_DOMAINS):
        return "Facebook"
    return None


def ytdlp_json(url):
    """Return info dict for a URL via yt-dlp -J."""
    cmd = [YTDLP, "--no-playlist", "--no-warnings", "-J", url]
    out = subprocess.run(cmd, check=True, timeout=120,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    import json
    return json.loads(out.stdout.decode("utf-8", "ignore"))


FMT = {
    # Width caps, not height: TikTok videos are portrait, so the width is
    # the meaningful "quality" side (720x1280 is the good no-watermark
    # file). Combined mp4 first; split video+audio merge as fallback.
    "hd": "b[width<=720][ext=mp4]/bv*[width<=720][ext=mp4]+ba[ext=m4a]/b[ext=mp4]/b",
    "sd": "b[width<=480][ext=mp4]/bv*[width<=480][ext=mp4]+ba[ext=m4a]/b[width<=640][ext=mp4]/b[ext=mp4]/b",
}


def download_file(url, workdir, quality="hd"):
    out = os.path.join(workdir, "video.%(ext)s")
    cmd = [YTDLP, "--no-playlist", "--no-warnings",
           "-f", FMT.get(quality, FMT["hd"]),
           "--merge-output-format", "mp4", "-o", out, url]
    subprocess.run(cmd, check=True, timeout=300,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    for name in os.listdir(workdir):
        if name.startswith("video."):
            return os.path.join(workdir, name)
    raise RuntimeError("no file produced")


def safe_name(title, ext="mp4"):
    name = re.sub(r"[^\w\- ]+", "", (title or "video")).strip()[:60]
    return (name or "video") + "." + ext


FETCH_ERR = ("Could not fetch this video. It may be private, or the "
             "platform blocked the request. Please try another link.")


# ---------------- routes --------------------------------------------------
@app.route("/")
def home():
    html = INDEX_HTML.replace("%%COUNT%%", f"{get_count():,}")
    return Response(html, mimetype="text/html")


@app.route("/about")
def about():
    return Response(ABOUT_HTML, mimetype="text/html")


@app.route("/privacy")
def privacy():
    return Response(PRIVACY_HTML, mimetype="text/html")


@app.route("/dmca")
def dmca():
    return Response(DMCA_HTML, mimetype="text/html")


@app.route("/api/stats")
def stats():
    return jsonify({"downloads": get_count()})


@app.route("/api/resolve", methods=["POST"])
def resolve():
    data = request.get_json(silent=True) or {}
    url = extract_url(data.get("url") or request.form.get("url") or "")
    platform = platform_of(url)
    if not platform:
        return jsonify({"ok": False,
                        "error": "Please paste a valid TikTok, Instagram or Facebook link."}), 400
    try:
        info = ytdlp_json(url)
    except subprocess.CalledProcessError:
        return jsonify({"ok": False, "error": FETCH_ERR}), 422
    except Exception:
        return jsonify({"ok": False,
                        "error": "Something went wrong. Please try again."}), 500
    from urllib.parse import quote
    q = quote(url, safe="")
    return jsonify({
        "ok": True,
        "platform": platform,
        "title": info.get("title") or f"{platform} video",
        "duration": info.get("duration"),
        "thumbnail": info.get("thumbnail"),
        "uploader": info.get("uploader"),
        "download": f"/download?url={q}",
        "download_hd": f"/download?url={q}&quality=hd",
        "download_sd": f"/download?url={q}&quality=sd",
        "mp3": f"/mp3?url={q}",
    })


@app.route("/download")
def download():
    url = extract_url(request.args.get("url") or "")
    if not platform_of(url):
        return "Invalid link. Please paste a TikTok, Instagram or Facebook link.", 400
    quality = (request.args.get("quality") or "hd").lower()
    if quality not in FMT:
        quality = "hd"
    tmp = tempfile.mkdtemp(prefix="tiksaver-")
    try:
        path = download_file(url, tmp, quality)
        title = None
        try:
            title = ytdlp_json(url).get("title")
        except Exception:
            pass
        bump_count()
        return send_file(path, as_attachment=True,
                         download_name=safe_name(title),
                         mimetype="video/mp4")
    except subprocess.CalledProcessError:
        return FETCH_ERR, 422
    except Exception:
        return "Something went wrong. Please try again.", 500


@app.route("/mp3")
def mp3():
    url = extract_url(request.args.get("url") or "")
    if not platform_of(url):
        return "Invalid link. Please paste a TikTok, Instagram or Facebook link.", 400
    tmp = tempfile.mkdtemp(prefix="tiksaver-mp3-")
    try:
        video = download_file(url, tmp, "sd")
        audio = os.path.join(tmp, "audio.mp3")
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", "-i", video,
             "-vn", "-codec:a", "libmp3lame", "-b:a", "128k", audio],
            check=True, timeout=300)
        title = None
        try:
            title = ytdlp_json(url).get("title")
        except Exception:
            pass
        bump_count()
        return send_file(audio, as_attachment=True,
                         download_name=safe_name(title, "mp3"),
                         mimetype="audio/mpeg")
    except subprocess.CalledProcessError:
        return FETCH_ERR, 422
    except Exception:
        return "Something went wrong. Please try again.", 500


@app.route("/health")
def health():
    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8090")),
            threaded=True)
