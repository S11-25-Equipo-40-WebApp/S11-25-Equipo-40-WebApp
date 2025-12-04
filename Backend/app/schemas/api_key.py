from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel


class APIKeyCreate(SQLModel):
    name: str | None = Field(default="Secret Key", max_length=50)


class APIKeyResponse(APIKeyCreate):
    raw_key: str


class APIKeyUpdate(APIKeyCreate):
    pass


class APIKeyListResponse(SQLModel):
    id: UUID
    name: str | None
    prefix: str
    revoked: bool
    created_at: datetime
