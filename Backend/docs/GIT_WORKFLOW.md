# 🔄 Git Workflow & Convenciones

Guía de trabajo colaborativo con Git para el proyecto Testify.

Esta guía rápida establece las reglas mínimas para trabajar en el monorepo Testify. Está pensada para ser práctica: ramas, formato de commits (Gitmoji), PRs y hooks.

## Branches (resumen)

- `main` — producción (estable). Merge sólo desde `develop` vía PR.
- `develop` — integración y preparación de releases.
- Ramas de trabajo: `feature/*`, `fix/*`, `hotfix/*`.

Buenas prácticas:

- Crear rama desde `develop`: `git checkout -b feature/mi-feature`
- Nombres claros y pequeños commits atómicos.

## Commits con Gitmoji (obligatorio)

Formato obligatorio:

```
<emoji> <type>(scope opt): <description>
```

Ejemplos cortos:

- `✨ feat(auth): add refresh token`
- `🐛 fix(api): prevent crash on missing field`
- `📝 docs: update README`

Si el commit no respeta el formato, el hook `commit-msg` lo rechazará.

## Pull Requests (rápido)

1. Mantén tu rama actualizada con `develop`.
2. Haz PR desde tu rama hacia `develop` con descripción clara.
3. Asegura que CI y tests pasen antes de merge.
4. Preferencia: **Squash and merge** para features.

## Pre-commit hooks (qué y cómo)

El repo usa `pre-commit` para:

- Ejecutar `ruff` (lint + auto-fix) y `ruff-format`.
- Validar mensajes con un hook local que exige Gitmoji.

Instalación (desde la raíz):

```bash
cd Backend
uv sync            # instala deps (incluye pre-commit)
./scripts/setup-hooks.sh
```

Comandos útiles:

- Ejecutar hooks localmente: `uv run pre-commit run --all-files`

## Ejemplos rápidos

Crear rama y commit:

```bash
git checkout -b feature/new
git add Backend/app/...
git commit -m "✨ feat(api): add endpoint"
```

Hacer PR:

```bash
git push origin feature/new
# Crear PR en GitHub: base=develop
```

## Errores comunes

- "Commit rejected: Gitmoji format" → arregla el mensaje: `📝 docs: ...`.
- Hooks no encontrados → ejecutar `./scripts/setup-hooks.sh` en `Backend`.

## Consejo final

Mantén `Backend/.githooks` como fuente de verdad para los hooks. Documenta en `Backend/README.md` cómo instalar los hooks (el script `./scripts/setup-hooks.sh`) para que los colaboradores del front no se confundan.

---

Este archivo ahora es un resumen práctico; si quieres puedo extraer algunos ejemplos adicionales o añadir una tabla corta de los Gitmojis más usados.

````

### "Your branch has diverged from origin"

```bash
# Solución: Rebase
git pull --rebase origin develop
````

### Commitear en rama incorrecta

```bash
# Solución: Mover commits a otra rama
git log  # Copiar hash del commit
git checkout rama-correcta
git cherry-pick <hash-del-commit>

# En rama incorrecta:
git reset --hard HEAD~1
```

### Eliminar rama remota por error

```bash
# Restaurar rama eliminada
git checkout -b nombre-rama <hash-ultimo-commit>
git push origin nombre-rama
```

## 📚 Recursos

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
- [Gitmoji](https://gitmoji.dev/)

---

**Recuerda**: Un buen historial de Git es documentación viviente del proyecto. 📖
