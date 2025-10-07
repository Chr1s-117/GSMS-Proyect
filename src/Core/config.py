# src/Core/settings.py
from pydantic_settings import BaseSettings
from pydantic import model_validator

"""
Application Settings Module

This module centralizes all configuration for the GSMS application.
- Uses Pydantic BaseSettings to validate and load environment variables.
- Supports local development and production (AWS EC2) environments.
- Settings are globally available via the 'settings' object.
"""

class Settings(BaseSettings):
    # --------------------------
    # Project Metadata
    # --------------------------
    PROJECT_NAME: str = "GSMS"          # Name of the project
    PROJECT_VERSION: str = "1.9.0"      # Current version

    # --------------------------
    # Application Runtime Parameters
    # --------------------------
    APP_ENV: str = "prod"               # Application environment ('dev', 'staging', 'prod')
    PORT: int = 8000                     # Uvicorn server port

    # --------------------------
    # Database Configuration
    # --------------------------
    # Mandatory: Must be provided via environment variable
    DATABASE_URL: str

    # --------------------------
    # UDP / Broadcasters
    # --------------------------
    # Pydantic interpreta "0/1/true/false/no/off" correctamente
    DISABLE_UDP: bool = False
    UDP_ENABLED: bool = True
    DDNS_ENABLED: bool = False
    BROADCASTER_ENABLE: bool = True

    @model_validator(mode="after")
    def _cohere_udp_flags(self):
        # Semántica deseada:
        # - Si DISABLE_UDP=true/1 => UDP_ENABLED=False
        # - Si DISABLE_UDP=false/0/ausente => UDP_ENABLED=True
        self.UDP_ENABLED = not bool(self.DISABLE_UDP)
        # Si UDP está apagado, apaga broadcasters siempre
        self.BROADCASTER_ENABLE = bool(self.BROADCASTER_ENABLE and self.UDP_ENABLED)
        return self

    # --------------------------
    # Pydantic Settings Behavior
    # --------------------------
    class Config:
        # Disable .env loading in production; only system environment variables are used
        env_file = None

        # Case-insensitive environment variables (DATABASE_URL, database_url, etc.)
        case_sensitive = False

# --------------------------
# Global settings instance
# --------------------------
# Reads environment variables at startup, validates types, and exposes globally
settings = Settings()  # type: ignore
