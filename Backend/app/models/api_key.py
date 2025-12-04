from uuid import UUID

from sqlmodel import Field

from .abstract import AbstractActive


class APIKey(AbstractActive, table=True):
    """API keys stored as digests. The raw key is shown once at creation.

    Fields:
    - id: uuid primary key
    - name: optional human name
    - prefix: first chars of raw token (for quick lookup)
    - secret_digest: HMAC/SHA digest of the raw token (stored, not reversible)
    """

    name: str | None = Field(default=None, max_length=50)
    prefix: str = Field(index=True, max_length=16)
    secret_digest: str = Field(max_length=128)
    revoked: bool = Field(default=False)

    # Foreing key
    user_id: UUID | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")
