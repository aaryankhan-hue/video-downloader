# All-in-One Video Downloader

A complete website tool to download videos from **YouTube, Facebook, Instagram, TikTok**, X/Twitter, Vimeo and 1000+ other sites (powered by yt-dlp).

Features:
- Paste link → see thumbnail, title, duration, uploader
- Download in Best HD / 720p / 480p / 360p, or **MP3 audio only**
- TikTok saved **without watermark** where the source allows it
- Mobile-friendly, SEO-ready page sections for each platform
- No database needed

---

## Option 1 — Run on your own PC (2 minutes)

Requirements: Python 3.10+ and ffmpeg installed.

Windows:
```
pip install -r requirements.txt
python app.py
```
Linux / Mac:
```
pip3 install -r requirements.txt
python3 app.py
```
Then open in your browser: **http://127.0.0.1:5000**

> ffmpeg is needed for HD merging and MP3. Windows: download from ffmpeg.org and add to PATH. Linux: `sudo apt install ffmpeg`. Mac: `brew install ffmpeg`.

---

## Option 2 — Put it live on the internet (free hosting)

The tool needs a real server backend — it **cannot** run on Blogger/Blogspot, because Blogger cannot run Python/yt-dlp.

### Render.com (easiest, free tier)
1. Put this folder in a GitHub repo (github.com → New repository → upload files).
2. Go to render.com → New → Web Service → connect your repo.
3. Build Command: `pip install -r requirements.txt`
   - Render's free image may not include ffmpeg. Use the Docker option below if HD merging fails.
4. Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 300`
5. Deploy — Render gives you a public URL like `https://your-tool.onrender.com`

### Docker (works on Render, Railway, VPS — includes ffmpeg)
This folder already has a `Dockerfile`. On Railway.app or Render choose **Docker** as the build type and deploy — ffmpeg is included automatically, so HD + MP3 will work fully.

### Railway.app
1. railway.app → New Project → Deploy from GitHub repo (same repo as above).
2. It detects the Dockerfile automatically. Deploy, then open the generated domain.

---

## How it works
- `POST /api/info` — yt-dlp reads the link and returns title/thumbnail/qualities.
- `GET /api/download?url=...&quality=best|1080|720|480|360|mp3` — the server downloads the file with yt-dlp into a temp folder, streams it to the visitor's browser, then deletes it.

## Important notes
- **Private / login-only videos** (e.g. private Instagram accounts, age-restricted YouTube) will fail — the server is not logged into your account.
- **YouTube can sometimes block server IPs** ("Sign in to confirm you're not a bot"). The tool already supports the standard fix: export your YouTube cookies from your browser (a "Get cookies.txt LOCALLY" type extension, while logged in), save the file as `cookies.txt` next to `app.py`, and it will be used automatically. Never share that file — it holds your login session. Running locally on your PC also works reliably without cookies.
- Free hosting tiers sleep when idle and have limited CPU/disk — fine for personal/small traffic, not for heavy public traffic.
- Only download content you own or have permission to save. Add your own disclaimer if you run it publicly.

## Files
- `app.py` — backend (Flask + yt-dlp)
- `static/index.html` — the full website UI (edit name/logo/colors here)
- `requirements.txt`, `Procfile`, `Dockerfile` — deployment
