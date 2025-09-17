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
    PROJECT_VERSION: str = "0.0.2"      # Current version

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
    # Feature Flags / Service Configuration
    # --------------------------
    UDP_ENABLED: bool = True             # Enable UDP server
    DDNS_ENABLED: bool = False           # Enable DDNS service (AWS doesn't need it)
    BROADCASTER_ENABLE: bool = True      # Enable GPS broadcaster

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
