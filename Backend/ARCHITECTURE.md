# 🏗️ Arquitectura del Proyecto - Testify

Este documento describe la arquitectura, patrones de diseño y decisiones técnicas del proyecto Testify.

## 📐 Arquitectura General

### Patrón de Capas

El backend sigue una **arquitectura en capas** (layered architecture) que separa responsabilidades:

```
┌─────────────────────────────────────┐
│         API Layer (Routers)         │  ← FastAPI Endpoints
├─────────────────────────────────────┤
│      Service Layer (Business)       │  ← Lógica de Negocio
├─────────────────────────────────────┤
│     Data Access Layer (Models)      │  ← SQLModel + PostgreSQL
├─────────────────────────────────────┤
│         Database (PostgreSQL)       │  ← Persistencia
└─────────────────────────────────────┘
```

### Flujo de una Request

```
Client Request
    ↓
FastAPI Router (app/api/router/)
    ↓
Service Layer (app/services/)
    ↓
Model/Database (app/models/)
    ↓
PostgreSQL
    ↓
Response ← Service ← Router ← Client
```

## 🗂️ Estructura de Módulos

### 1. **API Layer** (`app/api/`)

**Responsabilidad**: Manejar HTTP requests/responses, validación de entrada, autenticación.

```python
# Ejemplo: app/api/router/testimonials.py
from fastapi import APIRouter, Depends, status
from uuid import UUID, uuid4
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.db import get_session
from app.core.security import get_current_user
from app.schemas.testimonial import TestimonialCreate, TestimonialRead
from app.services.testimonial_service import TestimonialService
from app.models.user import User

router = APIRouter(prefix="/api/v1/testimonials", tags=["testimonials"])

@router.post("/", response_model=TestimonialRead, status_code=status.HTTP_201_CREATED)
async def create_testimonial(
    testimonial_data: TestimonialCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Create a new testimonial."""
    service = TestimonialService(session)
    return await service.create(testimonial_data, user_id=current_user.id)
```

**Principios**:

- ✅ Solo validación de entrada/salida
- ✅ Manejo de errores HTTP
- ✅ Documentación con docstrings
- ❌ NO lógica de negocio compleja
- ❌ NO acceso directo a base de datos

### 2. **Service Layer** (`app/services/`)

**Responsabilidad**: Lógica de negocio, orquestación de operaciones, validaciones complejas.

```python
# Ejemplo: app/services/testimonial_service.py
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from uuid import UUID

from app.models.testimonial import Testimonial
from app.schemas.testimonial import TestimonialCreate, TestimonialUpdate
from app.services.moderation_service import ModerationService

class TestimonialService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.moderation = ModerationService()

    async def create(
        self,
        data: TestimonialCreate,
        user_id: UUID
    ) -> Testimonial:
        """Create a new testimonial with automatic moderation."""
        # Validación de negocio
        if not data.content or len(data.content) < 10:
            raise ValueError("Content must be at least 10 characters")

        # Moderación automática
        is_approved = await self.moderation.check_content(data.content)

        # Crear testimonial
        testimonial = Testimonial(
            **data.model_dump(),
            author_id=user_id,
            status="approved" if is_approved else "pending"
        )

        self.session.add(testimonial)
        await self.session.commit()
        await self.session.refresh(testimonial)

        return testimonial

    async def list(
        self,
        category_id: UUID | None = None,
        status: str | None = None,
        limit: int = 10,
        offset: int = 0
    ) -> list[Testimonial]:
        """List testimonials with filters."""
        query = select(Testimonial)

        if category_id:
            query = query.where(Testimonial.category_id == category_id)
        if status:
            query = query.where(Testimonial.status == status)

        query = query.limit(limit).offset(offset)

        result = await self.session.exec(query)
        return result.all()
```

**Principios**:

- ✅ Lógica de negocio centralizada
- ✅ Validaciones complejas
- ✅ Coordinación entre múltiples modelos
- ✅ Transacciones de base de datos
- ❌ NO manejo de HTTP directamente
- ❌ NO conocimiento de FastAPI

### 3. **Models Layer** (`app/models/`)

**Responsabilidad**: Definición de esquemas de base de datos, relaciones, validaciones básicas.

```python
# Ejemplo: app/models/testimonial.py
# using builtin generics (list[], dict[], ...) in examples; List import removed
from datetime import datetime
from uuid import UUID, uuid4
from sqlmodel import Field, SQLModel, Relationship

class Testimonial(SQLModel, table=True):
    """Testimonial model representing user testimonials."""

    __tablename__ = "testimonials"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    title: str = Field(max_length=200, index=True)
    content: str = Field(max_length=5000)

    # Tipo de contenido
    media_type: str = Field(default="text")  # text, image, video
    media_url: str | None = Field(default=None, max_length=500)

    # Estado
    status: str = Field(default="pending")  # pending, approved, rejected

    # Relaciones
    author_id: UUID = Field(foreign_key="users.id")
    category_id: UUID | None = Field(default_factory=uuid4, foreign_key="categories.id")

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    author: "User" | None = Relationship(back_populates="testimonials")
    category: "Category" | None = Relationship(back_populates="testimonials")
    tags: list["Tag"] = Relationship(
        back_populates="testimonials",
        link_model="testimonial_tags"
    )
```

**Principios**:

- ✅ Definición clara de esquema
- ✅ Relaciones entre tablas
- ✅ Índices para optimización
- ✅ Validaciones de tipo y formato
- ❌ NO lógica de negocio
- ❌ NO queries complejos

### 4. **Schemas Layer** (`app/schemas/`)

**Responsabilidad**: DTOs (Data Transfer Objects) para validación de entrada/salida.

```python
# Ejemplo: app/schemas/testimonial.py
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl

# Schema para creación (Input)
class TestimonialCreate(BaseModel):
    title: str = Field(min_length=5, max_length=200)
    content: str = Field(min_length=10, max_length=5000)
    media_type: str = Field(default="text", pattern="^(text|image|video)$")
    media_url: HttpUrl | None = None
    category_id: UUID | None = None
    tag_ids: list[int] | None = None

# Schema para lectura (Output)
class TestimonialRead(BaseModel):
    id: UUID
    title: str
    content: str
    media_type: str
    media_url: str | None
    status: str
    author_id: UUID
    category_id: UUID | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# Schema para actualización (Input)
class TestimonialUpdate(BaseModel):
    title: str | None = Field(None, min_length=5, max_length=200)
    content: str | None = Field(None, min_length=10, max_length=5000)
    media_url: HttpUrl | None = None
    category_id: UUID | None = None
```

**Principios**:

- ✅ Separar schemas de entrada/salida
- ✅ Validaciones con Pydantic
- ✅ Documentación automática en OpenAPI
- ❌ NO lógica de negocio

### 5. **Core Layer** (`app/core/`)

**Responsabilidad**: Configuración, utilidades compartidas, conexiones.

```python
# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application
    PROJECT_NAME: str = "Testify"
    VERSION: str = "0.0.1"
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )

settings = Settings()
```

```python
# app/core/db.py
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession, AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

async_session_maker = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
```

## 🔐 Seguridad

### Autenticación JWT

```python
# app/core/security.py
from datetime import datetime, timedelta
from uuid import UUID
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> User:
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: UUID = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    user = await session.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user
```

### Autorización por Roles

```python
# app/core/permissions.py
from enum import Enum
from fastapi import Depends, HTTPException, status

class UserRole(str, Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"

def require_role(required_role: UserRole):
    async def role_checker(
        current_user: User = Depends(get_current_user)
    ):
        user_roles = [UserRole(r) for r in current_user.roles]

        if required_role not in user_roles and UserRole.ADMIN not in user_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return current_user

    return role_checker

# Uso en endpoints
@router.delete("/{id}")
async def delete_testimonial(
    id: UUID,
    current_user: User = Depends(require_role(UserRole.MODERATOR)),
    session: AsyncSession = Depends(get_session)
):
    # Solo moderadores y admins pueden eliminar
    pass
```

## 🔄 Manejo de Errores

### Exception Handlers Globales

```python
# app/main.py
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

app = FastAPI()

@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": "Database integrity error",
            "message": str(exc.orig)
        }
    )

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": str(exc)}
    )
```

### Excepciones Personalizadas

```python
# app/core/exceptions.py
from uuid import UUID
from fastapi import HTTPException, status

class TestimonialNotFoundError(HTTPException):
    def __init__(self, testimonial_id: UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Testimonial with id {testimonial_id} not found"
        )

class ModerationFailedError(HTTPException):
    def __init__(self, reason: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Content moderation failed: {reason}"
        )
```

## 📊 Base de Datos

### Migraciones con Alembic

```python
# Crear migración después de modificar modelos
uv run alembic revision --autogenerate -m "Add tags table"

# Estructura de migración
"""Add tags table

Revision ID: abc123
Revises: xyz789
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

def upgrade():
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_tags_name', 'tags', ['name'])

def downgrade():
    op.drop_index('ix_tags_name', table_name='tags')
    op.drop_table('tags')
```

### Relaciones Many-to-Many

```python
# app/models/testimonial_tags.py
from uuid import UUID
from sqlmodel import SQLModel, Field

class TestimonialTag(SQLModel, table=True):
    """Link table for many-to-many relationship."""
    __tablename__ = "testimonial_tags"

    testimonial_id: UUID = Field(foreign_key="testimonials.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)
```

## 🧪 Testing

### Estructura de Tests

```python
# tests/conftest.py
import pytest
from sqlmodel import create_engine, Session
from fastapi.testclient import TestClient

from app.main import app
from app.core.db import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
```

```python
# tests/test_api/test_testimonials.py
def test_create_testimonial(client: TestClient):
    response = client.post(
        "/api/v1/testimonials/",
        json={
            "title": "Great Experience",
            "content": "This product changed my life!",
            "media_type": "text"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Great Experience"
```

## 📈 Performance

### Optimizaciones de Queries

```python
# ✅ BIEN: Eager loading para evitar N+1
from sqlmodel import select
from sqlalchemy.orm import selectinload

query = select(Testimonial).options(
    selectinload(Testimonial.author),
    selectinload(Testimonial.category),
    selectinload(Testimonial.tags)
)

# ❌ MAL: N+1 queries
testimonials = await session.exec(select(Testimonial))
for testimonial in testimonials:
    author = testimonial.author  # Query separado por cada testimonial
```

### Paginación

```python
from typing import TypeVar, Generic
from pydantic import BaseModel

T = TypeVar("T")

class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int

async def paginate(
    query: Select,
    session: AsyncSession,
    page: int = 1,
    size: int = 10
) -> PaginatedResponse:
    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = await session.scalar(count_query)

    # Fetch items
    offset = (page - 1) * size
    result = await session.exec(query.limit(size).offset(offset))
    items = result.all()

    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size
    )
```

## 🔍 Logging

```python
# app/core/logger.py
import logging
from app.core.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger("testify")

# Uso en servicios
logger.info(f"Creating testimonial for user {user_id}")
logger.error(f"Failed to moderate content: {error}")
```

## 📝 Convenciones de Código

### Naming Conventions

- **Variables/Funciones**: `snake_case`
- **Clases**: `PascalCase`
- **Constantes**: `UPPER_SNAKE_CASE`
- **Archivos**: `snake_case.py`

### Type Hints

```python
# ✅ Siempre usar type hints
async def get_testimonial(
    testimonial_id: UUID,
    session: AsyncSession
) -> Testimonial | None:
    return await session.get(Testimonial, testimonial_id)

# ❌ Evitar código sin tipos
async def get_testimonial(testimonial_id, session):
    return await session.get(Testimonial, testimonial_id)
```

### Docstrings

```python
def create_testimonial(data: TestimonialCreate, user_id: UUID) -> Testimonial:
    """
    Create a new testimonial.

    Args:
        data: Testimonial data including title, content, and media.
        user_id: ID of the user creating the testimonial.

    Returns:
        Created testimonial instance with generated ID.

    Raises:
        ValueError: If content is too short or invalid.
        ModerationFailedError: If content fails moderation checks.
    """
    pass
```

---

Esta arquitectura garantiza:

- ✅ **Separation of Concerns**: Cada capa tiene responsabilidades claras
- ✅ **Testability**: Fácil de mockear y probar
- ✅ **Maintainability**: Código organizado y predecible
- ✅ **Scalability**: Fácil de extender con nuevas features
