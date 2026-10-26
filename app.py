"""
All-in-One Video Downloader
Backend: Flask + yt-dlp
Supports: YouTube, Facebook, Instagram, TikTok, X/Twitter, Vimeo, Dailymotion
and 1000+ other sites supported by yt-dlp.

Run locally:
    pip install -r requirements.txt
    python app.py
Then open: http://127.0.0.1:5000
"""

import os
import re
import uuid
import shutil
import threading

from flask import Flask, request, jsonify, send_file, send_from_directory, abort

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Flask(__name__, static_folder="static", static_url_path="/static")

# ---------------------------------------------------------------- helpers

def clean_url(url: str) -> str:
    url = (url or "").strip()
    return url

def is_valid_url(url: str) -> bool:
    return bool(re.match(r"^https?://[^\s]+$", url or ""))

def detect_platform(url: str) -> str:
    u = url.lower()
    if "youtube.com" in u or "youtu.be" in u:
        return "YouTube"
    if "facebook.com" in u or "fb.watch" in u or "fb.com" in u:
        return "Facebook"
    if "instagram.com" in u:
        return "Instagram"
    if "tiktok.com" in u:
        return "TikTok"
    if "twitter.com" in u or "x.com" in u:
        return "X (Twitter)"
    if "vimeo.com" in u:
        return "Vimeo"
    if "dailymotion.com" in u or "dai.ly" in u:
        return "Dailymotion"
    return "Other"

def base_opts():
    """Shared yt-dlp options. If a cookies.txt file sits next to app.py,
    it is used automatically — this fixes YouTube's 'Sign in to confirm
    you're not a bot' error on server IPs. Export cookies from your
    browser with a 'Get cookies.txt LOCALLY' type extension while
    logged in to YouTube, and save the file as cookies.txt here.
    NEVER share that file publicly — it contains your login session."""
    opts = {}
    cookie_file = os.path.join(BASE_DIR, "cookies.txt")
    if os.path.exists(cookie_file):
        opts["cookiefile"] = cookie_file
    return opts

def fmt_duration(seconds):
    if not seconds:
        return None
    seconds = int(seconds)
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def fmt_size(n):
    if not n:
        return None
    for unit in ["B", "KB", "MB", "GB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"

# Quality -> yt-dlp format selector
QUALITY_FORMATS = {
    "2160": "bestvideo[height<=2160]+bestaudio/best[height<=2160]/best",
    "best": "bestvideo+bestaudio/best",
    "1080": "bestvideo[height<=1080]+bestaudio/best[height<=1080]/best",
    "720":  "bestvideo[height<=720]+bestaudio/best[height<=720]/best",
    "480":  "bestvideo[height<=480]+bestaudio/best[height<=480]/best",
    "360":  "bestvideo[height<=360]+bestaudio/best[height<=360]/best",
    "mp3":  "bestaudio/best",
}

# ---------------------------------------------------------------- routes

@app.route("/")
def home():
    return send_from_directory(os.path.join(BASE_DIR, "static"), "index.html")

@app.route("/api/health")
def health():
    return jsonify({
        "ok": True,
        "yt_dlp_installed": yt_dlp is not None,
        "yt_dlp_version": getattr(yt_dlp, "version", None).__version__ if yt_dlp else None,
    })

@app.route("/api/info", methods=["POST"])
def info():
    if yt_dlp is None:
        return jsonify({"error": "yt-dlp is not installed on the server. Run: pip install -r requirements.txt"}), 500

    data = request.get_json(silent=True) or {}
    url = clean_url(data.get("url", ""))
    if not is_valid_url(url):
        return jsonify({"error": "Please paste a valid video link (starting with https://)."}), 400

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 30,
        **base_opts(),
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
    except Exception as e:
        msg = str(e)
        # Shorten very long yt-dlp errors for the UI
        if len(msg) > 350:
            msg = msg[:350] + "..."
        return jsonify({"error": f"Could not fetch this video. Reason: {msg}"}), 422

    # Available heights (for showing quality options)
    heights = sorted(
        {f.get("height") for f in (info_dict.get("formats") or []) if f.get("height")},
        reverse=True,
    )

    return jsonify({
        "title": info_dict.get("title"),
        "thumbnail": info_dict.get("thumbnail"),
        "duration": info_dict.get("duration"),
        "duration_text": fmt_duration(info_dict.get("duration")),
        "uploader": info_dict.get("uploader") or info_dict.get("channel"),
        "platform": detect_platform(url),
        "webpage_url": info_dict.get("webpage_url") or url,
        "available_heights": heights,
        "view_count": info_dict.get("view_count"),
    })

@app.route("/api/download")
def download():
    """Download on the server with yt-dlp, then stream the file to the browser.
    Query params: url=<video link>&quality=2160|4k|best|1080|720|480|360|mp3
    """
    if yt_dlp is None:
        return jsonify({"error": "yt-dlp is not installed on the server."}), 500

    url = clean_url(request.args.get("url", ""))
    quality = (request.args.get("quality") or "best").lower()
    if quality == "4k":  # friendly alias for 2160p
        quality = "2160"
    if not is_valid_url(url):
        abort(400, "Invalid URL")
    if quality not in QUALITY_FORMATS:
        quality = "best"

    job_id = uuid.uuid4().hex[:12]
    job_dir = os.path.join(DOWNLOAD_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    is_mp3 = quality == "mp3"
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
        "socket_timeout": 60,
        "retries": 3,
        "format": QUALITY_FORMATS[quality],
        **base_opts(),
        "outtmpl": os.path.join(job_dir, "%(title).80s.%(ext)s"),
        "merge_output_format": "mp3" if is_mp3 else "mp4",
    }
    if is_mp3:
        ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        shutil.rmtree(job_dir, ignore_errors=True)
        msg = str(e)
        if len(msg) > 350:
            msg = msg[:350] + "..."
        return jsonify({"error": f"Download failed. Reason: {msg}"}), 422

    files = [os.path.join(job_dir, f) for f in os.listdir(job_dir) if os.path.isfile(os.path.join(job_dir, f))]
    if not files:
        shutil.rmtree(job_dir, ignore_errors=True)
        return jsonify({"error": "Download finished but no file was produced. Try another quality."}), 500

    file_path = max(files, key=os.path.getsize)
    filename = os.path.basename(file_path)

    # Clean up the temp folder shortly after the response is sent
    def cleanup():
        import time
        time.sleep(15)
        shutil.rmtree(job_dir, ignore_errors=True)
    threading.Thread(target=cleanup, daemon=True).start()

    return send_file(file_path, as_attachment=True, download_name=filename)

# ---------------------------------------------------------------- main

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
