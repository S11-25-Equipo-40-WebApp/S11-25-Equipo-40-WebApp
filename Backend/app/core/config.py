import secrets
from typing import Annotated, Any

from pydantic import AnyUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    API: str = "/api"
    PROJECT_NAME: str = "Testify Backend"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"

    # Environment
    ENVIRONMENT: str = "development"

    @property
    def ACCESS_TOKEN_EXPIRE_MINUTES(self) -> int:
        """
        Token expiration time based on environment:
        - development: 8 days (for easier testing)
        - production: 5 minutes (for security)
        """
        if self.ENVIRONMENT == "production":
            return 60  # 60 minutes in production
        return 60 * 24 * 8  # 8 days in development

    # postgres
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_URL: str

    @property
    def async_database_url(self):
        url = self.POSTGRES_URL
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return url

    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )

    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
