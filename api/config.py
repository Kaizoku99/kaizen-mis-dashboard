"""Configuration settings for KAIZEN MIS Dashboard API."""
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API
    app_name: str = "KAIZEN MIS Dashboard API"
    app_version: str = "0.1.0"
    debug: bool = True
    cors_origins: list[str] = ["http://localhost:8501", "http://localhost:3000"]
    
    # Database (placeholder — connect real DBs later)
    database_url: str = "sqlite:///./mis_data.db"
    
    # Cache TTL in seconds
    cache_ttl: int = 300  # 5 minutes
    
    # Data refresh interval
    data_refresh_interval: int = 3600  # 1 hour

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
