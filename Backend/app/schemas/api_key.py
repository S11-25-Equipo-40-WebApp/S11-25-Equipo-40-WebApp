from sqlmodel import Field, SQLModel


class APIKeyCreate(SQLModel):
    name: str | None = Field(default=None, max_length=50)


class APIKeyResponse(APIKeyCreate):
    raw_key: str


class APIKeyUpdate(APIKeyCreate):
    pass
