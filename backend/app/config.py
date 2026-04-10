from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+asyncpg://localhost:5432/zenithspectra"

    # LLM
    llm_provider: str = "ollama"  # "ollama" or "groq"
    groq_api_key: str = ""
    ollama_base_url: str = "http://localhost:11434"
    llm_model: str = "llama3.1:8b"

    # CORS
    cors_origins: str = "http://localhost:3000"

    # Ingestion
    ingestion_interval_hours: int = 6

    # App
    app_name: str = "ZenithSpectra"
    debug: bool = False

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
