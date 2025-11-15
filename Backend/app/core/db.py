from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.config import settings

engine = create_async_engine(
    settings.async_database_url,
    # !imprime logs de querys
    echo=settings.ENVIRONMENT == "development",
    future=True,
)


async def init_db() -> None:
    async with engine.begin() as conn:
        # run_sync permite ejecutar operaciones sincrónicas como create_all dentro de una sesión asíncrona
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
