@echo off
title Video Downloader - One-time Install
cd /d %~dp0
echo ============================================
echo  Video Downloader - One-Time Install
echo ============================================
echo.

REM --- Check Python ---
where python >nul 2>nul
if %errorlevel% neq 0 (
  echo [X] Python nahi mila!
  echo     Pehle Python install karo: Microsoft Store me "Python 3.12" search karke install karo,
  echo     ya ye command chalao:  winget install Python.Python.3.12
  echo     Phir is file ko dobara chalao.
  pause
  exit /b 1
)
echo [OK] Python mil gaya.

REM --- Create virtual environment and install packages ---
if not exist ".venv" (
  echo [...] Virtual environment ban raha hai...
  python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul
echo [...] Packages install ho rahe hain (Flask, yt-dlp)... thora wait karo.
pip install -r requirements.txt
if %errorlevel% neq 0 (
  echo [X] Package install fail ho gaya. Internet check karke dobara chalao.
  pause
  exit /b 1
)
echo [OK] Packages install ho gaye.

REM --- Check ffmpeg (needed for HD merge + MP3) ---
where ffmpeg >nul 2>nul
if %errorlevel% neq 0 (
  echo [!] ffmpeg nahi mila - HD aur MP3 ke liye ye lazmi hai.
  echo     Install karne ke liye ye command chalao, phir is file ko dobara chalao:
  echo         winget install Gyan.FFmpeg
) else (
  echo [OK] ffmpeg mil gaya.
)

REM --- Check cloudflared (for the public link) ---
where cloudflared >nul 2>nul
if %errorlevel% equ 0 (
  echo [OK] cloudflared installed hai.
) else if exist "cloudflared.exe" (
  echo [OK] cloudflared.exe folder me mojood hai.
) else (
  echo [...] cloudflared install ho raha hai (winget se)...
  winget install --id Cloudflare.cloudflared --accept-package-agreements --accept-source-agreements
  echo     Agar winget fail ho to cloudflared ko Cloudflare ki official
  echo     website se download karke cloudflared.exe is folder me rakho.
)

echo.
echo ============================================
echo  Install complete! Ab "2-START-Windows.bat"
echo  chalao - tool aur public link start ho jayega.
echo ============================================
pause
