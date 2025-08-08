# app/utils/jwt.py

from datetime import datetime, timedelta
from jose import JWTError, jwt
from dotenv import load_dotenv
import os
from app.core.config import settings

# Load from .env
load_dotenv()

# JWT Config
SECRET_KEY = settings.SECRET_KEY #os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # 1 hour

def create_access_token(data: dict, expires_delta: timedelta = None) -> dict:
    to_encode = data.copy()

    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": token,
        "expire_date": expire.isoformat()
    }


def create_refresh_token(data: dict, expires_delta: timedelta = None) -> dict:
    expire = datetime.utcnow() + (expires_delta or timedelta(days=7))  # refresh token lasts 7 days
    to_encode = data.copy()
    to_encode.update({"exp": expire})

    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "refresh_token": token,
        "expire_date": expire.isoformat()
    }
