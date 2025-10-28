# src/Core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    PROJECT_NAME: str = "GSMS"
    PROJECT_VERSION: str = "0.0.1"
    APP_ENV: str = "prod"  
    PORT: int = 8000        

    DATABASE_URL: str

    UDP_ENABLED: bool = True

    class Config:
        env_file = None         
        case_sensitive = False  

settings = Settings()  # type: ignore

