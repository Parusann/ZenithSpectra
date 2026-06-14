# Self-hostable Ollama service that boots the Gemma 4 E4B model.
# Deploy this as its own service (Railway/Fly/VPS) or via the root docker-compose.yml,
# then point the backend's OLLAMA_BASE_URL at it.
FROM ollama/ollama:latest

# Model the entrypoint ensures is pulled on first boot.
ENV OLLAMA_MODEL=gemma4:e4b

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 11434
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
