from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "AIA LeadOps Automation"
    app_version: str = "0.1.0"
    database_url: str = "postgresql+psycopg://leadops:leadops@db:5432/leadops"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
