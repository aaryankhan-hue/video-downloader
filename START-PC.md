# PC + Cloudflare — Bina Card Ke Free Setup

Tumhara tool tumhare **apne PC** par chalega, aur **Cloudflare Tunnel** us ka ek public link bana dega jo tum khud bhi use kar sakte ho aur kisi ko bhej bhi sakte ho. Koi hosting nahi, koi card nahi, bilkul free.

**2 shartein:**
1. Link tab tak live rahe ga jab tak PC on hai aur dono windows khuli hain.
2. Quick tunnel ka link **har restart par badal jata hai** (naya random link banta hai). Apne use ke liye ye koi masla nahi — link hamesha PUBLIC-LINK wali window me nazar aye ga.

---

## Sirf pehli dafa — Install (Windows)

**Step 1 — Python** (agar pehle se hai to skip)
Microsoft Store kholo → "Python 3.12" search → Install. (Ya Command Prompt me: `winget install Python.Python.3.12`)

**Step 2 — ffmpeg** (HD merge aur MP3 ke liye lazmi)
Command Prompt me chalao: `winget install Gyan.FFmpeg`

**Step 3 — Project files**
- Nayi ZIP download karke extract karo (ya GitHub repo se **Code → Download ZIP**).
- Folder ke andar **`1-INSTALL-Windows.bat`** par double-click karo.
- Ye khud: virtual environment banayega, Flask + yt-dlp install karega, aur cloudflared install karega (public link ke liye).
- Khatam par "Install complete!" nazar aye ga.

## Har dafa use karne ke liye — Start

1. **`2-START-Windows.bat`** par double-click karo.
2. 2 windows khulengi:
   - **VideoDownloader-Server** — ye tumhara tool hai (ise band na karo).
   - **PUBLIC-LINK** — is me tumhara public link hoga, is tarah ka:
     `https://random-words-1234.trycloudflare.com`
3. Wahi link browser me kholo — ya mobile par / kisi ko bhej kar test karo. Tool live hai! 🎉
4. Sirf khud use karna hai to `http://localhost:5000` bhi chalega, bina tunnel ke.

**Band karna:** dono windows band kar do. Bas.

## Masla aye to

| Masla | Hal |
|---|---|
| "Python nahi mila" | Step 1 dobara karo; install ke waqt Command Prompt band karke dobara kholo. |
| Install bat me lal error | Internet on karke bat dobara chalao — adhoora install khud poora ho jayega. |
| Public link nahi bana | PUBLIC-LINK window ka error parho — aam wajah cloudflared ka install na hona hai; `1-INSTALL` dobara chalao ya `winget install Cloudflare.cloudflared` chalao. |
| Pehla download slow | Pehli dafa yt-dlp thora time leta hai, phir tez ho jata hai. |
| Link kaam karna band | PC so gaya hoga ya window band ho gayi — `2-START` dobara chalao, naya link mile ga. |
| Tunnel error de (bohat rare) | Internet ki koi proxy/VPN rok rahi ho sakti hai — VPN off karke dobara chalao. Phir bhi na ho to Plan B: **nZucchini** (nZucchini.com par free account — card nahi chahiye — authtoken set karke command: `nZucchini http 5000`). |

## Linux / Mac?

Wohi tareeqa hai: pehle `bash 1-install-linux-mac.sh`, phir har dafa `bash 2-start-linux-mac.sh`.

---

### Ek mashwara
Ye setup personal use, doston ke sath share karne aur testing ke liye perfect hai. Agar kal ko tool ko **hamesha-on public website** banana ho (PC band ho tab bhi chale, link bhi na badle), to us ke 2 hi rasta hain: Render par card verification, ya sasta sa VPS (~$4–6/month). Jab chaho, bata dena — usi project ko wahan shift kar dunga, files yehi rahengi.
