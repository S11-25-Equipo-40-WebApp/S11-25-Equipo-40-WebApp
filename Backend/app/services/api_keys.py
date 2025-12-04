import hashlib
import hmac
import secrets
from uuid import UUID

from sqlmodel import select

from app.core.config import settings
from app.core.db import SessionDep
from app.models.api_key import APIKey
from app.schemas import APIKeyResponse


def generate_api_key_pair(length: int = 48) -> tuple[str, str, str]:
    token_body = secrets.token_urlsafe(length)
    raw = f"{settings.API_KEY_DISPLAY_PREFIX}{token_body}"
    prefix = raw[: len(settings.API_KEY_DISPLAY_PREFIX) + settings.API_KEY_PREFIX_BODY_CHARS]
    digest = hmac.new(settings.API_KEY_SECRET.encode(), raw.encode(), hashlib.sha256).hexdigest()
    return raw, prefix, digest


def create_api_key(db: SessionDep, name: str | None = None) -> APIKeyResponse:
    """Create and persist a new APIKey; returns (APIKey model, raw_token).
    The raw token must be shown to the user once and is not stored.
    """
    raw, prefix, digest = generate_api_key_pair()
    model = APIKey(name=name, prefix=prefix, secret_digest=digest)
    db.add(model)
    db.commit()
    db.refresh(model)
    return APIKeyResponse(name=name, raw_key=raw)


def revoke_api_key(db: SessionDep, api_key_id: UUID) -> bool:
    key = db.get(APIKey, api_key_id)
    if not key:
        return False
    key.revoked = True
    db.add(key)
    db.commit()
    return True


def verify_api_key(db: SessionDep, raw_token: str) -> APIKey | None:
    """Verify a raw token: compute digest and return the active APIKey model if matches.

    Strategy: lookup by prefix, then compare digest with constant-time compare.
    """
    if not raw_token or len(raw_token) < len(settings.API_KEY_DISPLAY_PREFIX) + 1:
        return None

    prefix = raw_token[: len(settings.API_KEY_DISPLAY_PREFIX) + settings.API_KEY_PREFIX_BODY_CHARS]
    statement = select(APIKey).where(APIKey.prefix == prefix, APIKey.revoked.is_(False))  # type: ignore
    result = db.exec(statement).first()
    if not result:
        return None
    incoming = hmac.new(
        settings.API_KEY_SECRET.encode(), raw_token.encode(), hashlib.sha256
    ).hexdigest()
    if hmac.compare_digest(incoming, result.secret_digest):
        return result
    return None


def list_api_keys(db: SessionDep) -> list[APIKey]:
    """List all API keys in the database."""
    return db.exec(
        select(APIKey).where(APIKey.revoked.is_(False)).order_by(APIKey.created_at.desc())  # type: ignore
    ).all()
