# Backend deployment (Render / Railway)

Use this guide to deploy the HRMS Lite backend to **Render** or **Railway**. Both platforms provide a free tier and managed PostgreSQL.

---

## Prerequisites

- Code in a **Git repository** (GitHub, GitLab, or Bitbucket).
- A **PostgreSQL** database (Render or Railway can create one for you).

---

## Option A: Deploy on Render

### 1. Create a PostgreSQL database (optional but recommended for production)

1. Go to [render.com](https://render.com) and sign in.
2. **New** → **PostgreSQL**.
3. Choose a name, region, and plan (free tier available).
4. Click **Create Database**. Wait until it is ready.
5. Open the database and copy the **Internal Database URL** (or **External** if your app will run outside Render). You will use this as `DATABASE_URL`.

### 2. Create a Web Service (backend)

1. **New** → **Web Service**.
2. Connect your repository and select the repo that contains this project.
3. Configure:
   - **Root Directory:** `backend` (if your repo root is the project root and backend is in `backend/`).
   - **Runtime:** Python 3.
   - **Build Command:**
     ```bash
     pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```
   - **Instance Type:** Free (or paid if you prefer).

4. **Environment variables** (Add in the Render dashboard):
   - `DATABASE_URL` — Paste the PostgreSQL connection URL from step 1. (If you skip PostgreSQL, leave this unset to use SQLite; not recommended for production.)
   - `CORS_ORIGINS` — Your frontend URL(s), comma-separated. Example:
     ```
     https://your-app.vercel.app,https://your-app.netlify.app
     ```
     If you deploy the frontend later, add this then. You can leave it empty or set a placeholder; default allows only localhost.

5. Click **Create Web Service**. Render will build and deploy. The first deploy may take a few minutes.

6. Your API will be at: `https://<your-service-name>.onrender.com`
   - Health check: `https://<your-service-name>.onrender.com/api/health`
   - API docs: `https://<your-service-name>.onrender.com/docs`

### 3. Root directory note

If your repo structure is:

```
your-repo/
  backend/    <-- app code here
  frontend/
  README.md
```

then in Render, set **Root Directory** to `backend`. If the repo root is the backend folder itself, leave Root Directory empty.

---

## Option B: Deploy on Railway

### 1. Create a project and PostgreSQL database

1. Go to [railway.app](https://railway.app) and sign in.
2. **New Project** → **Deploy from GitHub repo** (or add repo later).
3. In the project, click **+ New** → **Database** → **PostgreSQL**. Railway will provision a Postgres instance and set `DATABASE_URL` automatically when you add the backend service.

### 2. Add the backend service

1. In the same project, click **+ New** → **GitHub Repo** (or **Empty Service** and connect repo).
2. Select the repository. If the backend is in a `backend` subfolder, Railway may detect it; otherwise configure the **Root Directory** to `backend` in **Settings**.
3. **Settings** (or **Variables**):
   - **Build Command** (if not auto-detected): `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Variables:** Railway often injects `DATABASE_URL` from the linked PostgreSQL service. If not, add it manually. Add `CORS_ORIGINS` with your frontend URL(s), e.g. `https://your-app.vercel.app`.

4. Deploy. Railway will build and run the app. It will assign a public URL like `https://<your-app>.up.railway.app`.

5. API base: `https://<your-app>.up.railway.app`
   - Health: `https://<your-app>.up.railway.app/api/health`
   - Docs: `https://<your-app>.up.railway.app/docs`

---

## Environment variables summary

| Variable        | Required | Description |
|----------------|----------|-------------|
| `DATABASE_URL` | No (for production yes) | PostgreSQL URL. Render/Railway provide this when you add a Postgres service. If unset, app uses SQLite (not suitable for production on these platforms). |
| `CORS_ORIGINS` | No | Comma-separated frontend origins, e.g. `https://hrms-lite.vercel.app`. Default allows only `http://localhost:5173`. |
| `PORT`         | Set by platform | Render and Railway set this automatically; the start command uses `$PORT`. |

---

## After deployment

1. Open `https://<your-backend-url>/api/health` — you should see `{"status":"ok"}`.
2. Open `https://<your-backend-url>/docs` — Swagger UI should load.
3. When you deploy the frontend (Vercel/Netlify), set the frontend’s API base URL to `https://<your-backend-url>` and add that URL to `CORS_ORIGINS` (e.g. `https://your-app.vercel.app`).

---

## Troubleshooting

- **Build fails:** Ensure **Root Directory** is `backend` if your backend code lives in `backend/`. Ensure `requirements.txt` and `app/main.py` are in that root.
- **Database connection error:** Check that `DATABASE_URL` is set and is a valid PostgreSQL URL. On Render, use the **Internal** URL if the web service and database are in the same account.
- **CORS errors from frontend:** Add your frontend’s full origin (e.g. `https://your-app.vercel.app`) to `CORS_ORIGINS` (no trailing slash).
- **App sleeps (Render free tier):** Free web services spin down after inactivity. The first request after idle may take 30–60 seconds; subsequent requests are fast.
