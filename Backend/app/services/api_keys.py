import hashlib
import hmac
import secrets
from uuid import UUID

from sqlmodel import select

from app.core.config import settings
from app.core.db import SessionDep
from app.models.api_key import APIKey


class APIKeyService:
    @staticmethod
    def get_tenant_owner_id_from_api_key(api_key: APIKey) -> UUID | None:
        """
        Extract tenant owner ID from a validated APIKey.
        APIKey.user_id always points to the tenant owner.
        """
        return api_key.user_id

    @staticmethod
    def generate_api_key_pair(length: int = 48) -> tuple[str, str, str]:
        token_body = secrets.token_urlsafe(length)
        raw = f"{settings.API_KEY_DISPLAY_PREFIX}{token_body}"
        prefix = raw[: len(settings.API_KEY_DISPLAY_PREFIX) + settings.API_KEY_PREFIX_BODY_CHARS]
        digest = hmac.new(
            settings.API_KEY_SECRET.encode(), raw.encode(), hashlib.sha256
        ).hexdigest()

        return raw, prefix, digest

    @staticmethod
    def create_api_key(
        db: SessionDep,
        tenant_owner_id: UUID,
        name: str | None = None,
    ) -> dict[str, str | None]:
        """Create and persist a new APIKey; returns dict with name and raw_key.
        The raw token must be shown to the user once and is not stored.
        """
        raw, prefix, digest = APIKeyService.generate_api_key_pair()
        model = APIKey(name=name, prefix=prefix, secret_digest=digest, user_id=tenant_owner_id)

        db.add(model)
        db.commit()
        db.refresh(model)
        return {"name": name, "raw_key": raw}

    @staticmethod
    def revoke_api_key(
        db: SessionDep,
        api_key_id: UUID,
        tenant_owner_id: UUID,
    ) -> bool:
        key = db.get(APIKey, api_key_id)
        if not key:
            return False

        if key.user_id != tenant_owner_id:
            return False

        key.revoked = True
        db.add(key)
        db.commit()
        return True

    @staticmethod
    def verify_api_key(db: SessionDep, raw_token: str) -> APIKey | None:
        """Verify a raw token: compute digest and return the active APIKey model if matches.

        Strategy: lookup by prefix, then compare digest with constant-time compare.
        """
        if not raw_token or len(raw_token) < len(settings.API_KEY_DISPLAY_PREFIX) + 1:
            return None

        prefix = raw_token[
            : len(settings.API_KEY_DISPLAY_PREFIX) + settings.API_KEY_PREFIX_BODY_CHARS
        ]

        result = db.exec(
            select(APIKey).where(
                APIKey.prefix == prefix,
                APIKey.revoked.is_(False),  # type: ignore
            )
        ).first()

        if not result:
            return None
        incoming = hmac.new(
            settings.API_KEY_SECRET.encode(), raw_token.encode(), hashlib.sha256
        ).hexdigest()
        if hmac.compare_digest(incoming, result.secret_digest):
            return result
        return None

    @staticmethod
    def list_api_keys(db: SessionDep, tenant_owner_id: UUID) -> list[APIKey]:
        """List all API keys by tenant owner."""
        return db.exec(
            select(APIKey)
            .where(
                APIKey.revoked.is_(False),  # type: ignore
                APIKey.user_id == tenant_owner_id,
            )
            .order_by(APIKey.created_at.desc())  # type: ignore
        ).all()
