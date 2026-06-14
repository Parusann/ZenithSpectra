# ZenithSpectra — Deployment

LLM inference is **Ollama-only**: Gemma 4 (E4B) is the single model everywhere
(`LLM_MODEL=gemma4:e4b`). There is no third-party LLM API, so any deploy that uses
LLM enrichment needs a reachable **Ollama host**.

```
Fly: frontend (Next.js)  ──HTTPS──▶  Fly: backend (FastAPI)  ──┬──▶  Fly Postgres
                                                               └──▶  Fly: ollama (GPU, .internal)
```

`ENABLE_LLM_ENRICHMENT=false` ⇒ the backend never calls Ollama (rule-based credibility +
trends still populate the feed). Enrichment (AI summaries / multi-level explanations / Q&A)
needs `ENABLE_LLM_ENRICHMENT=true` **and** a reachable `OLLAMA_BASE_URL`.

---

## Option A — Local / self-hosted stack (docker-compose)

Postgres + a self-hosting Ollama (auto-pulls `gemma4:e4b`) + the backend. Best for a
workstation/VPS; the Ollama container needs ~10 GB disk and is **much** faster with an
NVIDIA GPU (uncomment the `deploy.resources` block in `docker-compose.yml`).

```bash
docker compose up -d --build
docker compose exec backend alembic upgrade head                 # run once
docker compose exec backend python ../scripts/seed_sources.py    # run once (NOT idempotent)
curl -X POST http://localhost:8000/api/v1/ingest
# Backend → http://localhost:8000 · Ollama → http://localhost:11434
```

---

## Option B — Fly.io (production)

Four Fly apps in one org (so private `.internal` DNS resolves between them). Configs live
in this repo and are pre-validated (`fly config validate`).

### 1. Postgres (managed)
```bash
fly postgres create --name zenithspectra-db --region iad
```
Attach happens in step 3.

### 2. Ollama host (GPU) — `ollama/fly.toml`
```bash
cd ollama
fly launch --no-deploy --copy-config --name zenithspectra-ollama
fly volumes create ollama_models --region ord --size 15   # ~9.6 GB model + headroom
fly deploy
```
- GPU requires GPU access on your org; adjust `gpu_kind`/region in `ollama/fly.toml`
  to what's available (`fly platform vm-sizes`). Railway-style CPU-only also "works" but
  is slow — a GPU is strongly recommended.
- The entrypoint pulls `gemma4:e4b` on first boot. **Not exposed publicly** (the API is
  unauthenticated); the backend reaches it at `http://zenithspectra-ollama.internal:11434`.

### 3. Backend — `fly.backend.toml` (deploy from the REPO ROOT)
```bash
fly launch --no-deploy --copy-config -c fly.backend.toml --name zenithspectra-backend
fly postgres attach zenithspectra-db -a zenithspectra-backend   # injects DATABASE_URL (postgres://)

# Rewrite DATABASE_URL to the async driver, and point at the Ollama app:
fly secrets set -a zenithspectra-backend \
  DATABASE_URL="postgresql+asyncpg://<from-attach>" \
  OLLAMA_BASE_URL="http://zenithspectra-ollama.internal:11434" \
  CORS_ORIGINS="https://zenithspectra-frontend.fly.dev"

fly deploy -c fly.backend.toml          # release_command runs `alembic upgrade head`
fly ssh console -a zenithspectra-backend -C "python ../scripts/seed_sources.py"  # once
curl -X POST https://zenithspectra-backend.fly.dev/api/v1/ingest
```
To turn on enrichment later: `fly secrets set -a zenithspectra-backend ENABLE_LLM_ENRICHMENT=true`.

### 4. Frontend — `frontend/fly.toml`
```bash
cd frontend
fly launch --no-deploy --copy-config --name zenithspectra-frontend
fly deploy --build-arg NEXT_PUBLIC_API_URL=https://zenithspectra-backend.fly.dev
```
`NEXT_PUBLIC_API_URL` is baked at build time, so it must be passed as a `--build-arg`.
After the frontend URL exists, make sure the backend's `CORS_ORIGINS` matches it (step 3).

---

## Notes & footguns
- **asyncpg URL**: the app needs `postgresql+asyncpg://`; Alembic auto-converts to psycopg2
  for migrations. `fly postgres attach` injects `postgres://` — you **must** rewrite it.
- **`seed_sources.py` is not idempotent** — run it exactly once per database.
- **Model size**: `gemma4:e4b` ≈ 9.6 GB. Size the Ollama volume accordingly; first boot pulls it.
- **Security**: the Ollama API is unauthenticated. Keep it private (`.internal`); never publish `:11434`.
- **Migrations**: handled automatically by the backend's `release_command` on each deploy.
