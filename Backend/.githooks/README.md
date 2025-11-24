# Git Hooks Scripts

Este directorio contiene los scripts de Git hooks que son **versionados** con el repositorio.

## 📁 ¿Por qué este directorio?

El directorio `.git/hooks/` **NO se clona** con el repositorio (es local). Para que todos los desarrolladores tengan los mismos hooks, necesitamos versionarlos fuera de `.git/`.

## 📝 Scripts Disponibles

### `check-gitmoji.sh`

Script que valida el formato Gitmoji en mensajes de commit.

**Uso:**

```bash
.githooks/check-gitmoji.sh /ruta/al/archivo-de-mensaje
```

**Formato válido:**

```
<emoji> <tipo>: <descripción>

Ejemplos:
✨ Feat: add new feature
🐛 Fix: resolve bug
📝 Docs: update README
```

**Emojis soportados:** 23 emojis (ver `GIT_WORKFLOW.md`)

## 🚀 Instalación Automática

Cuando ejecutas:

```bash
uv run pre-commit install --hook-type commit-msg
uv run pre-commit install
```

Pre-commit framework:

1. Lee la configuración de `.pre-commit-config.yaml`
2. Copia este script a `.git/hooks/`
3. Lo configura para ejecutarse automáticamente

## 🔧 Mantenimiento

Si modificas estos scripts, los cambios deben:

1. **Comitearse** al repositorio
2. **Reinstalarse** en cada máquina:
   ```bash
   uv run pre-commit install --hook-type commit-msg -f
   uv run pre-commit install -f
   ```

## 📚 Más Información

- Ver `.pre-commit-config.yaml` para la configuración
- Ver `GIT_WORKFLOW.md` para convenciones Gitmoji
- Ver `DEVELOPMENT_SETUP.md` para setup completo
