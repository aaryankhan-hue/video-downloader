#!/bin/bash
# Video Downloader - one-time install (Linux / Mac)
cd "$(dirname "$0")"
set -e

command -v python3 >/dev/null || { echo "[X] Python3 nahi mila. Pehle Python install karo."; exit 1; }
echo "[OK] Python mil gaya."

[ -d .venv ] || python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip >/dev/null
echo "[...] Packages install ho rahe hain (Flask, yt-dlp)..."
pip install -r requirements.txt
echo "[OK] Packages install ho gaye."

command -v ffmpeg >/dev/null || echo "[!] ffmpeg nahi mila (HD/MP3 ke liye lazmi): Linux: sudo apt install ffmpeg | Mac: brew install ffmpeg"
command -v cloudflared >/dev/null || echo "[!] cloudflared nahi mila (public link ke liye): Cloudflare ki official site se apne system ke liye install karo, ya Mac par: brew install cloudflared"

echo ""
echo "Install complete! Ab chalao:  bash 2-start-linux-mac.sh"
