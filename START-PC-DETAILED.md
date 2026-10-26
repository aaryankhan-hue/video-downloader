# PC + Cloudflare Setup — Poori Detailed Guide (Step by Step)

Ye guide bilkul zero se hai. Har step ke sath ye bhi likha hai ke screen par **kya nazar ana chahiye** — taake tumhe pata chale ke tum sahi ja rahe ho ya nahi. Total time pehli dafa: ~15–20 minute. Us ke baad roz sirf 1 click.

---

## STEP 0 — Files tayyar rakho

1. Jo ZIP tumhe bheji gayi hai (`video-downloader-tool.zip`) use **Downloads** se kisi asaan jagah le jao, masalan **Desktop**.
2. ZIP par **right-click → Extract All → Extract**. Ek folder ban jayega: `video-downloader-tool`.
3. Folder khol kar confirm karo andar ye sab hai:
   - `app.py`, `requirements.txt`, `static` (folder — andar `index.html`)
   - `1-INSTALL-Windows.bat`, `2-START-Windows.bat`
   - `START-PC.md`, `START-PC-DETAILED.md` (ye wali file)
4. ⚠️ Files ko ZIP ke andar se seedha NA chalao — pehle extract karna lazmi hai, warna kuch nahi chalega.

**Concept samjho (30 second):** Tumhara PC hi "server" banega. `app.py` = tool ka engine. Cloudflare Tunnel = ek mehfooz surang jo bahir ki duniya ko tumhare PC tak laati hai, bina router settings chhere. Isi liye koi card/hosting nahi chahiye.

---

## STEP 1 — Python install karo (sirf pehli dafa)

Python wo zuban hai jis me tool likha hai — PC ko wo samajhna ana chahiye.

**Tareeqa A (sab se asaan):**
1. **Microsoft Store** kholo (Windows search me "Store" likho).
2. Search: **Python 3.12** → **Get / Install**.
3. Install hone do (2–3 minute).

**Tareeqa B:** python.org se installer download karo. Install ke pehle screen par neeche **"Add python.exe to PATH"** wala checkbox lazmi **tick** karna — ye aksar log bhool jate hain aur phir `python` command nahi milta.

**Check (confirm karna seekho):**
1. **Command Prompt** kholo: keyboard par `Win + R` → `cmd` likh kar Enter. (Ya Start menu me "cmd" search karo.)
2. Likho: `python --version` → Enter.
3. ✅ Aana chahiye: `Python 3.12.x` (koi bhi 3.10+ number theek hai).
4. ❌ Agar Microsoft Store khul jaye ya "not recognized" aye → Python ya to install nahi hua, ya PATH wala tick miss hua. Tareeqa A se dobara install karo.

---

## STEP 2 — ffmpeg install karo (sirf pehli dafa)

ffmpeg video ko jorne (HD me video+awaz alag hoti hai, ye unhe milata hai) aur MP3 banane ke liye lazmi hai. Is ke baghair 360p chalega lekin HD/MP3 fail honge.

1. Command Prompt me likho:
   `winget install Gyan.FFmpeg`
2. Beech me `Y` likh kar Enter karna par sakta hai (source agreements).
3. Install ke baad Command Prompt **band karke dobara kholo** (naye program ka rasta tabhi milta hai).
4. Check: `ffmpeg -version` → pehli line me version aana chahiye. ✅

> ⚠️ `winget` hi na mile (purana Windows) to pehle Microsoft Store se **"App Installer"** update karo, phir dobara try karo.

---

## STEP 3 — One-time Install chalao

1. `video-downloader-tool` folder me jao.
2. **`1-INSTALL-Windows.bat`** par **double-click** karo.
3. Agar neeli screen aye **"Windows protected your PC"** → ghabrana nahi, ye har nayi .bat file par ata hai. **"More info"** → **"Run anyway"** dabao. (Ye file tumhari apni hai jo main ne banayi hai.)
4. Kaali window khulegi aur line by line ye hoga (3–7 minute lag sakte hain, internet ki speed par hai):
   - `[OK] Python mil gaya.`
   - `[...] Packages install ho rahe hain (Flask, yt-dlp)...` — yahan thora rukega, ye normal hai.
   - `[OK] Packages install ho gaye.`
   - ffmpeg aur cloudflared ki `[OK]` lines.
   - Aakhir me: **`Install complete!`**
5. Window band karne ke liye koi key dabao (neeche "Press any key" likha hoga).

**Agar beech me lal (red) error aye:** internet check karke wahi .bat **dobara** chalao — jahan se ruka tha wahan se aage barh jayega, dobara shuru se nahi hoga.

**Is step ne asal me kya kiya:** folder ke andar `.venv` naam ka ek private box banaya aur tool ki libraries us me dal dein (tumhare PC ke baqi system ko kuch nahi hua), aur `cloudflared` — Cloudflare ka chhota sa program — install kar diya.

---

## STEP 4 — Tool Start karo (ab yehi roz ka tareeqa hai)

1. **`2-START-Windows.bat`** par double-click karo.
2. Kul **2 nayi windows** khulengi:
   - **Window 1 — "VideoDownloader-Server":** is me Flask ki lines ayengi, jin me `Running on http://127.0.0.1:5000` jaisi line hogi. Is ka matlab: **tool tumhare PC par chal raha hai.** ✅ Is window ko band NA karo.
   - **Window 2 — "PUBLIC-LINK":** is me Cloudflare ki lines ayengi. Thoray seconds me ek **box** bane ga jis ke andar bara sa link hoga:
     `https://kuch-bhi-random-words.trycloudflare.com`
     **Yehi tumhara public link hai.** 🎉
3. Link ko mouse se select karke copy kar lo.

> Dono windows ka khula rehna lazmi hai jab tak tool live rakhna hai. Ek band = tool band.

---

## STEP 5 — Test karo (2 tareeqon se)

**Test 1 — khud PC par:**
Browser me `http://localhost:5000` kholo → downloader ka page aana chahiye.

**Test 2 — asal test, mobile se:**
1. Apne **phone ki WiFi band** karke mobile data on karo (taake pakka pata chale ke link bahir se bhi khulta hai, sirf ghar ke network se nahi).
2. PUBLIC-LINK wala link phone ke browser me kholo → page khulna chahiye. ✅

**Test 3 — download test:**
1. YouTube ki koi chhoti video ka link copy karo.
2. Tool me paste → **Fetch Video** → title aur thumbnail aana chahiye.
3. **360p** wala button dabao → server thora soche ga, phir browser download shuru kar dega.
4. Phir **MP3** bhi try karo — ye chal gaya to samjho poora system (ffmpeg samet) 100% set hai. ✅✅

---

## STEP 6 — Band karna aur dobara chalana

- **Band karna:** dono windows (Server + PUBLIC-LINK) band kar do. Bas, tool off, link khatam.
- **Dobara chalana:** sirf `2-START-Windows.bat` — Install wala dobara NAHI chalana (wo sirf pehli dafa tha).
- **Link badalna:** har start par **naya** trycloudflare link bane ga. Purana link kisi ko bheja tha to wo ab kaam nahi kare ga — naya link PUBLIC-LINK window se le kar bhejna. (Yahi is free tareeqe ki ek khami hai, pehle se bata raha hun taake surprise na ho.)

---

## Errors — poori list

| Jo nazar aye | Matlab | Hal |
|---|---|---|
| `'python' is not recognized...` | Python PATH me nahi | Microsoft Store se dobara install (Step 1-A), phir Command Prompt band karke kholo |
| SmartScreen neeli screen | Windows ki aam hifazat | "More info" → "Run anyway" |
| `winget` nahi mila | Purana Windows/App Installer | Store se "App Installer" update karo |
| Install beech me ruk gaya | Internet drop | Internet on karke `1-INSTALL` dobara chalao |
| Page khulta hai, HD/MP3 fail | ffmpeg missing | Step 2 ka check chalao: `ffmpeg -version` |
| PUBLIC-LINK window me link hi nahi bana | cloudflared nahi chala | Error ki line parho; `winget install Cloudflare.cloudflared` chalao, phir `2-START` dobara |
| Link phone par nahi khulta, PC par khulta hai | PC so gaya / window band | PC ki sleep settings: tool chalate waqt PC ko sone na do; windows khuli rakho |
| YouTube: "Sign in to confirm you're not a bot" | YouTube ka IP check | README.md me cookies.txt wala hal likha hai; ya koi aur video dobara try karo — aksar khud theek ho jata hai |
| 5000 port busy error | Tool pehle se chal raha hai | Purani Server window pehle band karo, phir start karo |

---

## Mehfooz mashwara

PUBLIC-LINK wala link jise bhi bhejoge, wo tumhare tool ko use kar sakega jab tak tumhara PC on hai. Apna link public jagah (Facebook page waghera) post NA karo jab tak tum khud online ho aur chahte ho — kyun ke videos tumhare PC aur tumhare internet se download hongi.
