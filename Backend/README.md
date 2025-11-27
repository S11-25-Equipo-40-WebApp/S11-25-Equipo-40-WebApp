# 🔧 Testify Backend

Backend API REST para Testify - Sistema CMS de Testimonios y Casos de Éxito.

## 🚀 Inicio Rápido

Sigue estos pasos para levantar el backend localmente en pocos minutos.

### 📋 Requisitos rápidos

```bash
# 1. Verificar Python 3.13+
python --version  # o python3 --version

# 2. Instalar uv (si no lo tienes)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Verificar Docker
docker --version
docker-compose --version
```

### 🏃 Inicio en 5 pasos

#### 1) Clonar y entrar al backend

```bash
git clone https://github.com/sibas1/S11-25-Equipo-40-WebApp.git
cd S11-25-Equipo-40-WebApp/Backend
```

#### 2) Configurar variables de entorno

```bash
cp .env.example .env
# Edita .env si necesitas ajustar credenciales o secretos
```

#### 3) Instalar dependencias

```bash
# uv sincroniza dependencias (incluye pre-commit)
uv sync
```

#### 4) Instalar los pre-commit hooks (importante)

```bash
# Recomendado: script automático
./scripts/setup-hooks.sh

# Alternativa manual (desde Backend/):
uv run pre-commit install --hook-type commit-msg
uv run pre-commit install
```

> ⚠️ Importante: `uv sync` instala la herramienta `pre-commit` pero NO configura los hooks en tu repo; ejecuta `./scripts/setup-hooks.sh` o los comandos manuales para activarlos.

#### 5) Levantar servicios

```bash
docker-compose up -d

# Ver logs (opcional)
docker-compose logs -f app
```

6. Migraciones (si necesitas ejecutarlas manualmente)

```bash
# Normalmente el entrypoint aplica migraciones al arrancar el contenedor
# Si necesitas hacerlo manualmente desde el host:
uv run alembic upgrade head
```

### ✅ Verificar instalación

Abre en tu navegador:

- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Deberías ver la documentación interactiva y los endpoints listados.

### 🔧 Comandos útiles de desarrollo

```bash
# Formateo y linting
uv run ruff format .
uv run ruff check --fix .

# Opción Makefile
# Ejecuta el objetivo `lint` definido en `Backend/Makefile` (formatea y aplica fixes):
# Desde el directorio del backend:
make lint
# Desde la raíz del repositorio:
make -C Backend lint

# Tests
uv run pytest
uv run pytest --cov=app

# Dependencias
uv add paquete
uv add --dev paquete
```

### 🐛 Problemas comunes

- Puerto 8000 ocupado: `lsof -i :8000` o cambiar mapeo en `docker-compose.yaml`.
- uv no encontrado: instala con el script de arriba y recarga tu shell (`source ~/.zshrc`).
- Docker no está corriendo: arrancar Docker Desktop o el servicio del demonio.

---

## 📚 Documentación Completa

Ver documentación detallada en la raíz del proyecto:

- **[README.md](../README.md)** - Documentación principal del proyecto
- **[ARCHITECTURE.md](./docs/ARCHITECTURE.md)** - Arquitectura y patrones de diseño
- **[GIT_WORKFLOW.md](./docs/GIT_WORKFLOW.md)** - Convenciones de Git y commits

## 🏗️ Estructura del Backend

```
Backend/
├── alembic/               # Migraciones de base de datos
│   └── versions/          # Archivos de migración
├── app/                   # Código de la aplicación
│   ├── api/               # Endpoints REST
│   │   └── router/        # Routers de FastAPI
│   ├── core/              # Configuración y utilidades core
│   │   ├── config.py      # Settings y variables de entorno
│   │   ├── db.py          # Conexión a base de datos
│   │   └── security.py    # Autenticación y autorización
│   ├── models/            # Modelos SQLModel (ORM)
│   ├── schemas/           # Schemas Pydantic (DTOs)
│   ├── services/          # Lógica de negocio
│   └── utils/             # Utilidades helpers
├── tests/                 # Tests unitarios e integración
├── .env                   # Variables de entorno (no versionado)
├── .env.example           # Ejemplo de variables de entorno
├── alembic.ini            # Configuración de Alembic
├── docker-compose.yaml    # Orquestación de servicios
├── Dockerfile             # Imagen Docker
├── Makefile               # Comandos útiles
└── pyproject.toml         # Dependencias y configuración
```

## 🔧 Stack Tecnológico

- **FastAPI 0.121+** - Framework web moderno y rápido
- **Python 3.13+** - Lenguaje de programación
- **SQLModel 0.0.27+** - ORM con Pydantic integration
- **PostgreSQL** - Base de datos relacional
- **Alembic** - Migraciones de base de datos
- **uv** - Gestor de paquetes ultra-rápido
- **Ruff** - Linter y formateador de código
- **Pytest** - Framework de testing
- **Docker** - Contenerización

## 💻 Desarrollo

### Comandos Principales

```bash
# Desarrollo con Docker
docker-compose up              # Levantar servicios
docker-compose down            # Detener servicios
docker-compose logs -f app     # Ver logs

# Formateo y linting
uv run ruff format .           # Formatear código
uv run ruff check .            # Verificar linting
uv run ruff check --fix .      # Arreglar automáticamente

# Base de datos
make migrate                   # Aplicar migraciones
uv run alembic revision --autogenerate -m "mensaje"  # Crear migración

# Testing
uv run pytest                  # Ejecutar tests
uv run pytest --cov=app        # Con coverage

# Dependencias
uv add paquete                 # Agregar dependencia
uv add --dev paquete           # Agregar dependencia de desarrollo
uv sync                        # Sincronizar dependencias
```

### Desarrollo Local (Sin Docker)

Si prefieres desarrollar sin Docker:

```bash
# 1. Tener PostgreSQL corriendo localmente
# brew install postgresql (macOS)
# brew services start postgresql

# 2. Actualizar DATABASE_URL en .env
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/testify_db

# 3. Ejecutar aplicación
uv run fastapi dev app/main.py

# 4. Aplicar migraciones
uv run alembic upgrade head
```

## 🧪 Testing

### Estructura de Tests

```
tests/
├── conftest.py             # Fixtures globales
├── test_api/               # Tests de endpoints
│   ├── test_auth.py
│   └── test_testimonials.py
├── test_services/          # Tests de lógica de negocio
└── test_models/            # Tests de modelos
```

### Ejecutar Tests

```bash
# Todos los tests
uv run pytest

# Tests específicos
uv run pytest tests/test_api/test_testimonials.py

# Con coverage report
uv run pytest --cov=app --cov-report=html
open htmlcov/index.html

# Modo verbose
uv run pytest -v

# Detener al primer fallo
uv run pytest -x
```

## 📝 API Endpoints

Una vez corriendo, accede a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Estructura Planificada

```
/api/v1
├── /auth
│   ├── POST /register        # Registrar usuario
│   ├── POST /login           # Login
│   └── POST /refresh         # Refresh token
│
├── /testimonials
│   ├── GET    /              # Listar testimonios
│   ├── POST   /              # Crear testimonial
│   ├── GET    /{id}          # Obtener testimonial
│   ├── PUT    /{id}          # Actualizar testimonial
│   ├── DELETE /{id}          # Eliminar testimonial
│   └── POST   /{id}/moderate # Moderar testimonial
│
├── /categories
│   ├── GET    /              # Listar categorías
│   └── POST   /              # Crear categoría
│
├── /tags
│   ├── GET    /              # Listar tags
│   └── POST   /              # Crear tag
│
└── /analytics
    └── GET /dashboard        # Métricas del dashboard
```

## 🗄️ Base de Datos

### Migraciones con Alembic

```bash
# Crear nueva migración automática
uv run alembic revision --autogenerate -m "add user roles"

# Aplicar todas las migraciones
uv run alembic upgrade head

# Aplicar migración específica
uv run alembic upgrade <revision_id>

# Revertir última migración
uv run alembic downgrade -1

# Ver historial
uv run alembic history

# Ver estado actual
uv run alembic current
```

### Acceso Directo a PostgreSQL

```bash
# Con Docker
docker-compose exec testify_db psql -U testify_user -d testify_db

# Comandos útiles en psql:
# \dt              - Listar tablas
# \d tabla         - Describir tabla
# \l               - Listar bases de datos
# \q               - Salir
```

## 🔐 Seguridad

### Variables de Entorno Sensibles

**NUNCA** commitear:

- `.env` - Variables de entorno locales
- Archivos con `SECRET_KEY` o credenciales
- Tokens de servicios externos

### Autenticación

El proyecto usa **JWT (JSON Web Tokens)** para autenticación:

1. Usuario hace login → recibe access token
2. Cliente incluye token en header: `Authorization: Bearer <token>`
3. Backend valida token en cada request

## 🐛 Debugging

### Ver Logs

```bash
# Logs de la aplicación
docker-compose logs -f app

# Logs de PostgreSQL
docker-compose logs -f testify_db

# Logs en tiempo real
docker-compose logs -f
```

### Conectarse al Contenedor

```bash
# Acceder a shell del contenedor
docker-compose exec app bash

# Ejecutar Python interactivo
docker-compose exec app uv run python

# Ver variables de entorno
docker-compose exec app env
```

## 🚀 Despliegue

### Consideraciones de Producción

- ✅ Configurar CORS apropiadamente
- ✅ Usar PostgreSQL externo (no Docker)
- ✅ Configurar reverse proxy (Nginx)
- ✅ Habilitar HTTPS
- ✅ Configurar monitoring y logging
- ✅ Backup automático de base de datos

## 🤝 Contribución

Ver [GIT_WORKFLOW.md](GIT_WORKFLOW.md) para convenciones de:

- Branches
- Commits
- Pull Requests
- Code Review

### Checklist antes de PR

- [ ] Pre-commit hooks instalados (`./scripts/setup-hooks.sh`)
- [ ] `uv run pre-commit run --all-files` pasa
- [ ] `uv run pytest` pasa
- [ ] Código tiene tests
- [ ] Commits siguen convención Gitmoji
- [ ] Documentación actualizada
- [ ] Migraciones incluidas (si aplica)

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/sibas1/S11-25-Equipo-40-WebApp/issues)
- **Documentación Principal**: Ver `README.md` en raíz del proyecto

---

**Stack**: FastAPI + SQLModel + PostgreSQL + Docker + uv + Ruff
