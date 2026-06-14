# ZenithSpectra

**See the full picture. Trust the source.**

AI-powered science intelligence platform that tracks live developments in space exploration and frontier physics, ranks source credibility, surfaces trending topics, and helps users understand complex discoveries through grounded summaries and source-backed question answering.

## Architecture

- **Frontend**: Next.js 16.2.3 (App Router, TypeScript, Tailwind CSS) — deployed on Fly.io
- **Backend**: FastAPI (Python) — deployed on Fly.io
- **Database**: PostgreSQL — managed Fly Postgres
- **AI**: Gemma 4 (E4B) via Ollama — runs as a separate Fly GPU app (private `.internal`)

## Project Structure

```
zenithspectra/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── docs/              # Documentation
├── scripts/           # Utility scripts, seed data
├── *.fly.toml         # Fly.io deploy configs (see DEPLOYMENT.md)
└── .env.example       # Environment variable template
```

## Getting Started

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env       # Edit with your values
uvicorn app.main:app --reload
```

## Categories

- **Space Exploration** — NASA, ESA, SpaceX, missions, exoplanets
- **Quantum Physics** — Entanglement, computing, error correction
- **Theoretical Physics** — Black holes, dark matter, string theory
- **Frontier Ideas** — Time travel, warp drives, simulation theory
