from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str):
    password = pwd_context.hash(password)
    return password


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)
