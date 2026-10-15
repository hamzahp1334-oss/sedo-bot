# 🥋 SEDO MARTIAL ART — Render Deployment Package

> **Production Deployment Files for Influencer SEDO MARTIAL ART (`@sedomartialart3`)**  
> Complete dual-bot suite featuring Customer Front-Desk Bot (`@officialsedo_bot`) and Admin Operations Bot (`@sedoadmin_bot`).

---

## 🚀 Exact Render.com Deployment Commands & Settings

### Step 1: Create Web Service on Render
1. Push this folder to a GitHub repository (or upload as a repo).
2. Go to **[dashboard.render.com](https://dashboard.render.com/)**.
3. Click **New +** ➔ **Web Service**.
4. Select your GitHub repository containing these files.

---

### Step 2: Render Service Configuration
Configure the fields exactly as follows:

| Setting | Value to Enter |
| :--- | :--- |
| **Name** | `sedo-martial-art-bot` *(or any name you prefer)* |
| **Region** | Frankfurt (EU Central) or Oregon (US West) |
| **Branch** | `main` |
| **Root Directory** | *(leave blank if repository root)* |
| **Runtime** | **Python** |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python -u main.py` |
| **Plan** | **Free** or **Starter** |

---

### Step 3: Advanced / Health Check Settings (Under "Advanced")
Render will automatically monitor your bot's health using its built-in HTTP server:

| Setting | Value |
| :--- | :--- |
| **Health Check Path** | `/health` |
| **Auto-Deploy** | **Yes** |

---

### Step 4: Environment Variables (Add under "Environment Variables")
Render injects `$PORT` automatically (defaulting to 10000 or 8080). Add the following variables:

```env
CUSTOMER_BOT_TOKEN=8684430105:AAFGXfNwKVTC_tteTIEnrFYL93CfsUZNSCY
ADMIN_BOT_TOKEN=8742362718:AAFS31WL2zFFJNTX_hrcrzou1JWrAs002Tw
ADMIN_IDS=8798202536,406274598
TIKTOK_URL=https://www.tiktok.com/@sedomartialart3
PORT=8080
PYTHONUNBUFFERED=1
```

---

### Step 5: Click "Create Web Service"
- Render will execute `pip install -r requirements.txt`.
- Render will start `python -u main.py`.
- Both `@officialsedo_bot` and `@sedoadmin_bot` will immediately start polling!
- Render will ping `http://localhost:8080/health` (or `$PORT/health`), receive `{"status": "healthy"}`, and mark the service as **Live (200 OK)**!

---

## 📁 Included Files in this Folder

- `main.py` — Dual bot runners + aiohttp web server on port 8080 / `$PORT`
- `config.py` — Config loader supporting Render `$PORT` and token management
- `states.py` — FSM states for advertising, partnerships, and direct messaging
- `i18n.py` — Strict Amharic and English translation catalog (zero mixing)
- `keyboards.py` — Keyboards with compact ASCII tokens (< 25 bytes)
- `database.py` — Async SQLite database operations (aiosqlite)
- `storage.py` — Media and document storage handler
- `notifications.py` — Instant admin alert dispatchers
- `handlers/` — Handlers for `/start`, ads, partnerships, my requests, contact, admin
- `requirements.txt` — Python dependencies
- `render.yaml` — Render Blueprint specification
- `Procfile` — `web: python -u main.py`
- `stackhost.yaml` & `stackhost.yml` — StackHost configurations with `runtime:` object
- `Dockerfile` & `.dockerignore` — Alternative container deployment
- `.env` & `.env.example` — Pre-filled production tokens
- `assets/sedo_logo.jpg` — Official SEDO MARTIAL ART brand logo
- `test_bot.py` — Test suite (6/6 tests passing)
