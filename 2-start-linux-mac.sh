#!/bin/bash
# Video Downloader - start server + Cloudflare public link (Linux / Mac)
cd "$(dirname "$0")"

[ -d .venv ] || { echo "Pehle install chalao: bash 1-install-linux-mac.sh"; exit 1; }

echo "Server start ho raha hai http://localhost:5000 par..."
source .venv/bin/activate
python app.py &
SERVER_PID=$!
sleep 4

echo ""
echo "Public link neeche aye ga (https://....trycloudflare.com) -"
echo "band karne ke liye Ctrl+C dabao."
echo ""
cloudflared tunnel --url http://localhost:5000

kill $SERVER_PID 2>/dev/null
