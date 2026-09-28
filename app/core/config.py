from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AIA LeadOps Automation"
    app_version: str = "1.0.0"
    database_url: str = "postgresql+psycopg://leadops:leadops@db:5432/leadops"

    ai_provider: str = "openai-compatible"
    ai_base_url: str = "https://api.groq.com/openai/v1"
    ai_model: str = "llama-3.1-8b-instant"
    ai_api_key: str | None = None
    ai_timeout_seconds: float = 15.0

    n8n_webhook_url: str | None = None
    n8n_webhook_secret: str | None = None
    automation_timeout_seconds: float = 5.0
    automation_max_attempts: int = 3
    automation_retry_backoff_seconds: float = 0.25

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
