# src/Core/settings.py
from pydantic_settings import BaseSettings

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
    PROJECT_VERSION: str = "2.0.0"      # Current version

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

    # --- BEGIN: UDP / broadcasters on/off from env -----------------
    import os

    def _truthy(name: str, default: bool) -> bool:
        v = os.getenv(name, "")
        if v == "":   # sin variable => usa el default que definas
            return default
        return str(v).strip().lower() not in ("0", "false", "no", "off")

    # Si pones DISABLE_UDP=1 -> UDP_ENABLED=False
    UDP_ENABLED = _truthy("DISABLE_UDP", True) and not _truthy("DISABLE_UDP", False)

    # Si además quieres apagar los broadcasters al desactivar UDP:
    BROADCASTER_ENABLE = _truthy("BROADCASTER_ENABLE", True) and UDP_ENABLED
    # --- END -------------------------------------------------------

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
