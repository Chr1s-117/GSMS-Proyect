# src/core/config.py
"""
Application Settings Module

This module centralizes all configuration for the GSMS application.
- Uses Pydantic BaseSettings to validate and load environment variables.
- Supports local development (.env) and production (AWS EC2 via env vars).
- Settings are globally available via the 'settings' object.

Environment Variables Required:
    DATABASE_URL: PostgreSQL connection string (format: postgresql://user:pass@host:port/db)

Optional Environment Variables:
    PORT: Uvicorn server port (default: 8000)
    ROOT_PATH: FastAPI root_path for reverse proxy (default: "")
    APP_ENV: Environment name (dev/staging/prod, default: prod)
    DISABLE_UDP: Disable UDP services (default: false)
    UDP_ENABLED: Enable UDP services (default: true)
    BROADCASTER_ENABLE: Enable broadcaster service (default: true)
    DDNS_ENABLED: Enable DDNS service (default: false)
    ALLOWED_ORIGINS_HTTP: CORS origins for HTTP (comma-separated)
    ALLOWED_ORIGINS_WS: CORS origins for WebSocket (comma-separated)

AWS Production Setup:
    - System environment variables are loaded from /etc/gsms/env and /etc/gsms/dev/<name>.env
    - No .env file is used in production
    - Variables are injected via SSM Parameter Store
"""

from pydantic_settings import BaseSettings
from pydantic import model_validator, Field
from typing import List

class Settings(BaseSettings):
    # --------------------------
    # Project Metadata
    # --------------------------
    PROJECT_NAME: str = "GSMS"
    PROJECT_VERSION: str = "2.0.1"

    # --------------------------
    # Application Runtime Parameters
    # --------------------------
    APP_ENV: str = Field(default="prod", description="Application environment (dev/staging/prod)")
    PORT: int = Field(default=8000, description="Uvicorn server port")
    ROOT_PATH: str = Field(default="", description="FastAPI root_path for reverse proxy (e.g., /dev/chris)")

    # --------------------------
    # Database Configuration
    # --------------------------
    # Mandatory: Must be provided via environment variable
    # Format: postgresql://user:password@host:port/database
    DATABASE_URL: str = Field(..., description="PostgreSQL connection string")

    # --------------------------
    # CORS Configuration
    # --------------------------
    ALLOWED_ORIGINS_HTTP: str = Field(
        default="*",
        description="Comma-separated list of allowed HTTP origins for CORS"
    )
    ALLOWED_ORIGINS_WS: str = Field(
        default="*",
        description="Comma-separated list of allowed WebSocket origins"
    )

    # --------------------------
    # UDP / Broadcasters Configuration
    # --------------------------
    # Pydantic interprets "0/1/true/false/yes/no/on/off" correctly as bool
    DISABLE_UDP: bool = Field(default=False, description="Disable UDP services")
    UDP_ENABLED: bool = Field(default=True, description="Enable UDP services")
    BROADCASTER_ENABLE: bool = Field(default=True, description="Enable broadcaster service")

    @model_validator(mode="after")
    def _cohere_udp_flags(self):
        """
        Coherence validator for UDP-related flags.
        
        Logic:
        - If DISABLE_UDP=true => UDP_ENABLED=False
        - If DISABLE_UDP=false => UDP_ENABLED=True (unless explicitly set)
        - If UDP is disabled, all broadcasters are also disabled
        """
        # DISABLE_UDP takes precedence
        if self.DISABLE_UDP:
            self.UDP_ENABLED = False
        
        # If UDP is disabled, force broadcaster off
        if not self.UDP_ENABLED:
            self.BROADCASTER_ENABLE = False
        
        return self

    # --------------------------
    # Helper Methods
    # --------------------------
    def get_allowed_origins_http(self) -> List[str]:
        """Parse ALLOWED_ORIGINS_HTTP into a list"""
        if self.ALLOWED_ORIGINS_HTTP == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_HTTP.split(",") if origin.strip()]

    def get_allowed_origins_ws(self) -> List[str]:
        """Parse ALLOWED_ORIGINS_WS into a list"""
        if self.ALLOWED_ORIGINS_WS == "*":
            return ["*"]
        return [origin.strip() for origin in self.ALLOWED_ORIGINS_WS.split(",") if origin.strip()]

    # --------------------------
    # Pydantic Settings Behavior
    # --------------------------
    class Config:
        # CRITICAL for production: Disable .env file loading
        # Only system environment variables are used in AWS EC2
        # This prevents accidentally loading local .env files in production
        env_file = None
        
        # Allow loading from .env in local development (optional, override with env_file=".env")
        # env_file = ".env"  # Uncomment for local development only
        
        # Case-insensitive environment variables
        case_sensitive = False
        
        # Allow extra fields (forward compatibility)
        extra = "allow"

# --------------------------
# Global settings instance
# --------------------------
# Reads environment variables at startup, validates types, and exposes globally
# The `# type: ignore` suppresses static type checker warnings about DATABASE_URL
# being "required", even though Pydantic loads it from the environment at runtime.
settings = Settings()  # type: ignore