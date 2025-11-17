#!/bin/bash

# Check if commit message follows gitmoji format
# Format: <emoji> <type>: <description>
# Example: ✨ feat: add new feature

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Lista de emojis válidos según GIT_WORKFLOW.md
valid_emojis="✨|🐛|📝|💄|🎨|♻️|⚡|✅|🔧|📦|👷|🔥|🚑|🚀|🔒|🗃️|⬆️|⬇️|🚧|💚|🔀|⏪|🎉|🔖"

# Pattern: emoji + espacio + tipo + : + descripción
pattern="^($valid_emojis) .+:.+"

if echo "$commit_msg" | grep -qE "$pattern"; then
    echo "✅ Commit message format OK"
    exit 0
else
    echo ""
    echo "❌ Error: Commit message must follow Gitmoji format"
    echo ""
    echo "Format: <emoji> <type>: <description>"
    echo ""
    echo "Examples:"
    echo "  ✨ Feat: add new feature"
    echo "  🐛 Fix: resolve authentication bug"
    echo "  📝 Docs: update README"
    echo "  🎨 Style: format code with ruff"
    echo "  ♻️ Refactor: simplify service logic"
    echo ""
    echo "See GIT_WORKFLOW.md for all valid emojis"
    echo ""
    exit 1
fi
