from datetime import datetime, timedelta

import jwt

from app.core.config import settings


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=6)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
