from datetime import UTC, datetime
from uuid import UUID, uuid4

import sqlalchemy
from sqlmodel import Field, SQLModel


def get_utc_now():
    return datetime.now(UTC)


class Abstract(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
        # sa_column=Column(DateTime(timezone=True), server_default=func.now()),
    )
    updated_at: datetime = Field(
        default_factory=get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
    )


class AbstractActive(Abstract):
    is_active: bool = Field(default=True, nullable=False)
    deleted_at: datetime | None = None
