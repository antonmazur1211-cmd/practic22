from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Налаштування проекту"""
    
    # PostgreSQL
    POSTGRES_USER: str = "antonmazur"
    POSTGRES_PASSWORD: str = "password123"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "antonmazur_db"
    
    # FastAPI
    APP_NAME: str = "Antonmazur API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # JWT Authentication
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production-antonmazur-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Cookie settings
    COOKIE_NAME: str = "access_token"
    COOKIE_SECURE: bool = False  # True в production з HTTPS
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"
    
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    @property
    def SYNC_DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
