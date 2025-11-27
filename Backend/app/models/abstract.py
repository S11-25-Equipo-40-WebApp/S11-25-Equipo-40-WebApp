from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Abstract(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class AbstractActive(Abstract):
    is_active: bool = Field(default=True, nullable=False)
    deleted_at: datetime | None = None
