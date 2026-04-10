# ZenithSpectra

**See the full picture. Trust the source.**

AI-powered science intelligence platform that tracks live developments in space exploration and frontier physics, ranks source credibility, surfaces trending topics, and helps users understand complex discoveries through grounded summaries and source-backed question answering.

## Architecture

- **Frontend**: Next.js 14+ (App Router, TypeScript, Tailwind CSS) — deployed on Vercel
- **Backend**: FastAPI (Python) — deployed on Railway
- **Database**: PostgreSQL
- **AI**: LLM abstraction layer supporting Ollama (local dev) and Groq (production)

## Project Structure

```
zenithspectra/
├── frontend/          # Next.js app
├── backend/           # FastAPI app
├── docs/              # Documentation
├── scripts/           # Utility scripts, seed data
├── .github/           # CI/CD workflows
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
