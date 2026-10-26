# Deploy Guide — All-in-One Video Downloader

Pehle **Step 0 (GitHub)** dono options ke liye common hai. Us ke baad **Render (free)** ya **Railway (paid, hamesha on)** me se ek choose karo.

**Recommendation:** Pehle Render try karo — permanent free tier hai. Farq sirf ye hai ke free service 15 minute khali rehne par so jati hai, aur agla visitor aane par ~1 minute me jaagti hai. Railway soota nahi, lekin free nahi hai (30 din ka $5 trial credit, phir Hobby plan $5/month).

---

## Step 0 — Code ko GitHub par upload karo (common)

1. ZIP ko apne PC par extract karo — ek folder `video-downloader-tool` banega.
2. github.com par login karo → upar right `+` → **New repository**.
3. Repository name: `video-downloader` → **Public** select karo → **Create repository**.
4. Naye repo me **uploading an existing file** wale link par click karo.
5. Extract kiye hue folder ki **saari files** drag & drop karo:
   `app.py`, `requirements.txt`, `Dockerfile`, `render.yaml`, `railway.json`, `Procfile`, `README.md`, `DEPLOY.md` aur poora `static` folder.
   ⚠️ `cookies.txt` kabhi upload NA karo (ye tumhara login session hota hai — `.gitignore` me pehle se block hai, lekin web upload me khud dhyan rakho).
6. **Commit changes** dabao.

> GitHub Desktop ya git command use karna ata hai to wo bhi theek hai — nateeja ek hi hai: code repo me hona chahiye.

---

## Option A — Render (FREE) ⭐ recommended

Is project me `render.yaml` pehle se mojood hai, to Render taqreeban sab kuch khud set kar dega. Docker runtime select karna sab se zaroori hai — isi se ffmpeg milega, jo HD merge aur MP3 ke liye lazmi hai.

1. render.com par **GitHub se sign up / login** karo.
2. Dashboard → **New +** → **Web Service**.
3. **Build and deploy from a Git repository** → **Next** → apna `video-downloader` repo select karo (pehli dafa GitHub connect karne ki permission deni hogi).
4. Settings is tarah rakho:
   - **Name:** `video-downloader` (jo marzi — URL isi se bane ga)
   - **Runtime:** **Docker** ⭐ (Python select NA karo, warna ffmpeg nahi mile ga aur HD/MP3 fail hoga)
   - **Instance Type:** **Free**
   - Baqi sab default — Dockerfile aur health check (`/api/health`) auto-detect ho jaye ge.
5. **Create Web Service** dabao. Pehla build 3–6 minute lega.
6. Build khatam hote hi upar tumhara live URL mile ga, jaisay:
   `https://video-downloader-xxxx.onrender.com`
7. URL kholo → link paste karke test karo (neeche wali checklist dekho).

**Free tier ki haqeeqat:**
- 750 free instance-hours / month (ek service ke liye kaafi)
- 15 minute koi visitor na aye to service so jati hai; agla visitor aane par ~1 minute ki loading ke baad jaagti hai — ye normal hai, error nahi
- Agar baad me hamesha-on chahiye to yahi service $7/month wale Starter plan par upgrade ho jati hai, kuch change kiye baghair

---

## Option B — Railway (hamesha on, paid)

1. railway.app par **GitHub se login** karo.
2. **New Project** → **Deploy from GitHub repo** → `video-downloader` repo select karo.
3. Railway `Dockerfile` khud detect kar lega (is project me `railway.json` bhi mojood hai jo Docker build confirm karta hai) — koi setting change karne ki zaroorat nahi.
4. Deploy complete hone par service par click karo → **Settings → Networking → Generate Domain**. Tumhe `https://video-downloader-production-xxxx.up.railway.app` jaisa URL mile ga.
5. URL kholo aur test karo.

**Railway ki cost ki haqeeqat:**
- Permanent free tier **nahi** hai — naye account ko ek dafa $5 trial credit (30 din) milta hai
- Us ke baad **Hobby plan $5/month** (us me $5 usage shamil; chhoti si site aam tor par isi me chal jati hai)
- Faida: service soti nahi, deploy bhi tez hota hai

---

## Deploy ke baad — Test checklist ✅

1. Live URL kholo — downloader page nazar ana chahiye.
2. Ek **YouTube** link paste karo → **Fetch Video** → title/thumbnail ana chahiye.
3. **360p** se chhoti video download karke dekho (tez test hoga).
4. **MP3** button test karo (ffmpeg check — agar ye chala to sab chalega).
5. Ek **TikTok** aur ek **Facebook Reel** ka link bhi try karo.

## Masla aye to (Troubleshooting)

| Masla | Wajah / Hal |
|---|---|
| Page khulta hai lekin HD ya MP3 fail | ffmpeg missing — matlab Docker runtime ki jagah Python select ho gaya. Render me service ka runtime Docker karo (ya nayi Docker service banao). |
| YouTube: "Sign in to confirm you're not a bot" | YouTube ne server IP ko check lagaya. Hal: apne browser se YouTube cookies export karke (ek "Get cookies.txt LOCALLY" extension se) file ka naam `cookies.txt` rakh kar server par rakho. Render free par file kal persist mushkil hai, to behtareen hal: cookies ko secret file ke tor par add karo ya PC local version use karo. Note: GitHub par cookies kabhi upload na karo. |
| Pehla page load bohat slow | Render free ki neend (sleep) hai — ~1 minute wait karo, phir fast ho jayega. Railway/VPS par ye masla nahi. |
| "Could not fetch this video" | Video private / login-only hai, ya link ghalat hai. Public link try karo. |
| Build fail | Logs me error dekho — aam wajah: repo me `Dockerfile` ya `static/index.html` miss hona. Saari files upload hui thin check karo. |

## Custom domain (baad me, optional)

Render: Service → **Settings → Custom Domains → Add** → apna domain add karo aur wahan diye hue DNS (CNAME) record apne domain registrar (masalan Porkbun) me lagao — free tier par bhi custom domain + HTTPS milta hai.
Railway: Service → **Settings → Networking → Custom Domain** — same DNS tareeqa.
