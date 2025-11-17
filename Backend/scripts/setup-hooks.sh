#!/bin/bash

# Post-installation script
# Este script se ejecuta después de instalar dependencias

echo "🔧 Configurando hooks de pre-commit..."

# Ir al directorio Backend (donde está .pre-commit-config.yaml)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$BACKEND_DIR" || exit 1

# Verificar que estamos en el directorio correcto
if [ ! -f ".pre-commit-config.yaml" ]; then
    echo "❌ Error: No se encontró .pre-commit-config.yaml en Backend/"
    echo "   Ejecuta este script desde Backend/"
    exit 1
fi

# Instalar hooks de pre-commit
echo "📦 Instalando hooks..."
uv run pre-commit install --hook-type commit-msg
uv run pre-commit install

if [ $? -eq 0 ]; then
    echo "✅ Hooks instalados correctamente!"
    echo ""
    echo "Pre-commit está configurado para validar:"
    echo "  - Código Python con Ruff"
    echo "  - Formato de commits con Gitmoji"
    echo ""
else
    echo "❌ Error al instalar hooks"
    exit 1
fi
