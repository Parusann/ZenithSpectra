#!/usr/bin/env bash
set -euo pipefail

MODEL="${OLLAMA_MODEL:-gemma4:e4b}"

# Start the Ollama server in the background.
ollama serve &
server_pid=$!

# Wait for the server to accept requests.
echo "[ollama] waiting for server to come up..."
until ollama list >/dev/null 2>&1; do
  sleep 1
done

# Ensure the configured model is present (idempotent — a no-op if already pulled).
echo "[ollama] ensuring model '${MODEL}' is available..."
ollama pull "${MODEL}"
echo "[ollama] ready — serving '${MODEL}'."

# Hand the foreground back to the server process.
wait "${server_pid}"
