@echo off
title Video Downloader - Running
cd /d %~dp0

if not exist ".venv" (
  echo Pehle "1-INSTALL-Windows.bat" chalao - install abhi nahi hua.
  pause
  exit /b 1
)

echo ============================================
echo  Video Downloader start ho raha hai...
echo ============================================
echo.
echo  1) Server ek nayi window me start hoga.
echo  2) Public link dosri window (PUBLIC LINK) me milega -
echo     https://..........trycloudflare.com
echo.
echo  BAND karne ke liye: dono windows band kar do.
echo ============================================
echo.

REM --- Start the downloader server in its own window ---
start "VideoDownloader-Server" cmd /k ".venv\Scripts\python app.py"

REM --- Wait for the server to come up ---
timeout /t 5 /nobreak >nul

REM --- Start the Cloudflare quick tunnel in its own window ---
if exist "cloudflared.exe" (
  start "PUBLIC-LINK" cmd /k "cloudflared.exe tunnel --url http://localhost:5000"
) else (
  start "PUBLIC-LINK" cmd /k "cloudflared tunnel --url http://localhost:5000"
)

echo Server aur tunnel alag windows me khul gaye hain.
echo PUBLIC-LINK wali window me apna public link dekho.
echo Ye window band kar sakte ho.
pause
