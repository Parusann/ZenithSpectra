# ZenithSpectra — Deployment

The platform is **Ollama-only** for LLM inference: Gemma 4 (E4B) is the single model
everywhere (`LLM_MODEL=gemma4:e4b`). There is no third-party LLM API — so any deploy
that uses LLM enrichment needs a reachable **Ollama host**.

```
Vercel (Next.js)  ──HTTP──▶  Backend (FastAPI)  ──┬──▶  Postgres
                                                  └──▶  Ollama (gemma4:e4b)
```

`ENABLE_LLM_ENRICHMENT=false` ⇒ the backend never calls Ollama (rule-based credibility +
trends still populate the feed). Enrichment (AI summaries / multi-level explanations / Q&A)
requires `ENABLE_LLM_ENRICHMENT=true` **and** a reachable `OLLAMA_BASE_URL`.

---

## Option A — Full self-hosted stack (docker-compose)

Brings up Postgres + a self-hosting Ollama service (auto-pulls `gemma4:e4b`) + the backend.
Best for a VPS/workstation; the Ollama container needs ~10 GB disk for the model and is
**much** faster with an NVIDIA GPU (uncomment the `deploy.resources` block in the compose file).

```bash
docker compose up -d --build
docker compose exec backend alembic upgrade head                 # run once
docker compose exec backend python ../scripts/seed_sources.py    # run once (NOT idempotent)
curl -X POST http://localhost:8000/api/v1/ingest
# Backend → http://localhost:8000   Ollama → http://localhost:11434
```

Enable enrichment by setting `ENABLE_LLM_ENRICHMENT=true` (env or a `.env` beside the compose
file) and re-creating the backend: `docker compose up -d backend`.

---

## Option B — Managed (Railway + Vercel) + a hosted Ollama

### 1. Ollama host
Deploy `ollama/Dockerfile` as its own always-on service. It runs `ollama serve` and pulls
`gemma4:e4b` on first boot. Options:
- **Railway**: new service → "Deploy from Dockerfile" → path `ollama/Dockerfile`. Attach a
  volume at `/root/.ollama` so the model persists across restarts. ⚠️ Railway is CPU-only;
  `gemma4:e4b` will run but be slow.
- **Fly.io / RunPod / a GPU VPS**: recommended for usable latency. Expose port `11434`
  (keep it private to your backend network if possible — it is unauthenticated).

### 2. Backend → Railway
- Root dir `backend/` (NIXPACKS uses `backend/requirements.txt` + `railway.toml`).
- Env vars:
  - `DATABASE_URL` = Railway Postgres URL **rewritten to `postgresql+asyncpg://…`**.
  - `OLLAMA_BASE_URL` = your Ollama host's internal URL (e.g. `http://ollama.railway.internal:11434`).
  - `LLM_MODEL=gemma4:e4b`
  - `ENABLE_LLM_ENRICHMENT` = `false` for a bare deploy, `true` once the Ollama host is wired.
  - `CORS_ORIGINS` = your Vercel domain.
- One-off after first deploy:
  `railway run alembic upgrade head` → `railway run python scripts/seed_sources.py` →
  `curl -X POST <railway-url>/api/v1/ingest`.

### 3. Frontend → Vercel
- Root dir `frontend/` (`vercel.json` present).
- Env: `NEXT_PUBLIC_API_URL = https://<railway-backend-url>`.
- After deploy, set the backend's `CORS_ORIGINS` to the Vercel domain and redeploy.

---

## Notes & footguns
- **asyncpg URL**: the app needs `postgresql+asyncpg://`; Alembic auto-converts to psycopg2
  for migrations. Railway's default `DATABASE_URL` will **not** include `+asyncpg` — add it.
- **`seed_sources.py` is not idempotent** — run it exactly once per database.
- **Model size**: `gemma4:e4b` ≈ 9.6 GB. The Ollama volume must have room; first boot pulls it.
- **Security**: the Ollama API is unauthenticated. Keep `OLLAMA_BASE_URL` on a private network;
  do not expose `:11434` publicly.
