# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str  # Your SQLAlchemy-compatible connection string
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENCRYPTION_KEY: str
    YOUTUBE_API_KEY: str

    APP_ADMIN: str
    APP_FROM_EMAIL: str
    APP_SMTP_HOST: str
    APP_SMTP_PORT: int = 587
    APP_SMTP_PWD: str
    COMPLETE_REGISTRATION_LINK: str
    APP_NAME: str


    class Config:
        env_file = ".env"

settings = Settings()
