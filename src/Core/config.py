# src/Core/config.py

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
    PROJECT_VERSION: str = "2.0.1"      # Current version

    # --------------------------
    # Application Runtime Parameters
    # --------------------------
    APP_ENV: str = "prod"               # Application environment ('dev', 'staging', 'prod')
    PORT: int = 8000                     # Uvicorn server port

    # --------------------------
    # Database Configuration
    # --------------------------
    """
    Database URL is required and loaded from environment variables.
    In Pydantic 2.x, BaseSettings automatically reads from the .env file.
    Type checkers like Pylance/mypy may incorrectly warn that an argument is missing,
    even though at runtime the value is correctly loaded.
    """
    DATABASE_URL: str

    # --------------------------
    # UDP / Broadcasters
    # --------------------------
    """
    Service configuration flags
    Set to False to disable the corresponding service
    
    Pydantic interpreta "0/1/true/false/no/off" correctamente
    """
    DISABLE_UDP: bool = False
    UDP_ENABLED: bool = True
    DDNS_ENABLED: bool = False
    BROADCASTER_ENABLE: bool = True

    # [AWS-MIGRATION-P1] Compatibilidad DISABLE_UDP garantizada via model_validator
    @model_validator(mode="after")
    def _cohere_udp_flags(self):
        """
        Ensures coherence between UDP-related flags.
        
        Semantics:
        - If DISABLE_UDP=true/1 => UDP_ENABLED=False
        - If DISABLE_UDP=false/0/absent => UDP_ENABLED=True
        - If UDP is disabled, broadcasters are always disabled
        """
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
        """
        In production (AWS), disable .env loading; only system environment variables are used.
        In local development, specify env_file = ".env" to load from .env file.
        """
        env_file = None  # Specify the .env file location for local development
        # For production (AWS), use: env_file = None

        # Case-insensitive environment variables (DATABASE_URL, database_url, etc.)
        case_sensitive = False

# --------------------------
# Global settings instance
# --------------------------
"""
Instantiate the settings object.
The `# type: ignore` comment is used to suppress static type warnings from IDEs
regarding the DATABASE_URL argument, which is automatically populated at runtime
by Pydantic 2.x from the environment variable.

Reads environment variables at startup, validates types, and exposes globally.
"""
settings = Settings()  # type: ignore