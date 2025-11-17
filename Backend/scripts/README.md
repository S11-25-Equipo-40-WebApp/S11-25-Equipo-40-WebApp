# Scripts de Automatización

Este directorio contiene scripts útiles para configurar y mantener el proyecto.

## 📝 Scripts Disponibles

### `setup-hooks.sh`

Instala automáticamente los hooks de pre-commit después de clonar el repositorio.

**Uso:**

```bash
# Desde la raíz del proyecto
./scripts/setup-hooks.sh
```

**Qué hace:**

1. Verifica que estés en el directorio correcto
2. Instala hooks de pre-commit para validar código
3. Instala hooks de commit-msg para validar formato Gitmoji
4. Muestra mensaje de confirmación

**Cuándo ejecutar:**

- Después de clonar el repositorio
- Después de `uv sync`
- Cuando actualices `.pre-commit-config.yaml`

## 🔄 Por qué son necesarios estos scripts

### El Problema

```bash
uv sync  # ✅ Instala paquete pre-commit
         # ❌ NO instala hooks en .git/hooks/
```

El paquete `pre-commit` se instala, pero los hooks (scripts en `.git/hooks/`) **no se crean automáticamente**.

### La Solución

Este script automatiza el paso manual:

```bash
# Sin script (manual):
uv run pre-commit install --hook-type commit-msg
uv run pre-commit install

# Con script (automático):
./scripts/setup-hooks.sh
```

## 🚀 Workflow Completo

```bash
# 1. Clonar repo
git clone repo
cd proyecto/Backend

# 2. Instalar dependencias
uv sync

# 3. Configurar hooks (NECESARIO)
./scripts/setup-hooks.sh  # ← Este script

# 4. Desarrollar normalmente
# ... código ...
git commit -m "✨ feat: new feature"  # Hooks se ejecutan automáticamente
```

## 📚 Más Información

- Ver `.pre-commit-config.yaml` para configuración de hooks
- Ver `GIT_WORKFLOW.md` para convenciones de commits
- Ver `DEVELOPMENT_SETUP.md` para setup completo
