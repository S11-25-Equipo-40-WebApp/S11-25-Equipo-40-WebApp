from sqlmodel import Field, SQLModel


class TokenResponse(SQLModel):
    access_token: str = Field(description="Access token")
    refresh_token: str | None = Field(default=None, description="Refresh token")
    token_type: str = Field(default="bearer", description="Token type")
