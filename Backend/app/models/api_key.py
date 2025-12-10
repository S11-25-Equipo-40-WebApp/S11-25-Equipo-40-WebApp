from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from .abstract import AbstractActive

if TYPE_CHECKING:
    from .user import User


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

    # Foreign key
    user_id: UUID | None = Field(default=None, foreign_key="user.id", ondelete="SET NULL")

    # Relationship
    user: Optional["User"] = Relationship(back_populates="api_keys")
