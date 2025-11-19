from datetime import datetime, timedelta

import jwt

SECRET_KEY = "CAMBIA_ESTO"
ALGORITHM = "HS256"


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(hours=6)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
