# Backend image for the self-hosted / docker-compose stack.
# (Fly builds this via fly.backend.toml; also used by docker-compose & VPS.)
# Build context is the repo ROOT so both backend/ and the root scripts/ are available.
FROM python:3.12-slim

WORKDIR /app

# Install Python deps first for layer caching.
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the app and the seed/migration scripts, preserving the repo layout
# (seed_sources.py resolves ../backend relative to itself).
COPY backend/ /app/backend/
COPY scripts/ /app/scripts/

# config.py reads .env / env from the working dir, and `app.main` must be importable.
WORKDIR /app/backend

EXPOSE 8000
CMD ["gunicorn", "app.main:app", "-w", "2", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
