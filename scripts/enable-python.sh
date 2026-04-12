#!/bin/bash

# Enable Python Development Environment
# This script sets up a Python project with:
# - Virtual environment (venv)
# - GitHub Actions CI workflow
# - Python dependencies for SDD/TDD
# - VS Code Python extensions and settings
# - Pre-commit hooks

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "🐍 Enabling Python Development Environment..."
echo ""

# ============================================================================
# 1. Create Virtual Environment
# ============================================================================

if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

echo ""

# ============================================================================
# 2. Activate Virtual Environment and Install Dependencies
# ============================================================================

echo "📚 Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
echo "✅ Dependencies installed"

echo ""

# ============================================================================
# 3. Enable Python GitHub Actions CI Workflow
# ============================================================================

if [ ! -f ".github/workflows/ci.yml" ]; then
    echo "🚀 Enabling GitHub Actions CI workflow..."
    mkdir -p .github/workflows
    cp .github/ci-templates/ci-python.template.yml .github/workflows/ci.yml
    echo "✅ CI workflow enabled at .github/workflows/ci.yml"
else
    echo "✅ CI workflow already exists at .github/workflows/ci.yml"
fi

echo ""

# ============================================================================
# 4. Merge Python Pre-commit Hook Checks
# ============================================================================

echo "🔒 Setting up pre-commit hook..."
if [ -d ".git" ]; then
    python3 scripts/append-precommit.py python
else
    echo "⚠️  Not a git repository yet, skipping pre-commit hook"
fi

echo ""

# ============================================================================
# 5. Merge Python VS Code Configuration
# ============================================================================

echo "🔧 Merging Python VS Code settings and extensions..."
python3 .vscode/merge-configs.py python
echo "✅ VS Code configuration updated"

echo ""

# ============================================================================
# 6. Merge Python Makefile Targets
# ============================================================================

echo "📋 Setting up Makefile..."
python3 scripts/append-makefile.py python

echo ""

# ============================================================================
# 7. Create src and tests directories if they don't exist
# ============================================================================

if [ ! -d "src" ]; then
    echo "📁 Creating src directory..."
    mkdir -p src
    touch src/__init__.py
    echo "✅ src/ directory created"
fi

if [ ! -d "tests" ]; then
    echo "📁 Creating tests directory..."
    mkdir -p tests
    touch tests/__init__.py
    echo "✅ tests/ directory created"
fi

echo ""

# ============================================================================
# ✨ Setup Complete
# ============================================================================

echo "✨ Python environment is ready!"
echo ""
echo "Setup includes:"
echo "  ✅ Virtual environment (venv/)"
echo "  ✅ Dependencies (pytest, pydantic, black, pylint, pyright, etc)"
echo "  ✅ GitHub Actions CI workflow (.github/workflows/ci.yml)"
echo "  ✅ Pre-commit hooks (.git/hooks/pre-commit)"
echo "  ✅ VS Code configuration (settings.json, extensions.json merged)"
echo "  ✅ Makefile with common commands (test, lint, format, etc)"
echo ""
echo "Next steps:"
echo "  1. Activate: source venv/bin/activate"
echo "  2. View commands: make help"
echo "  3. Write tests first: pytest tests/"
echo "  4. Check coverage: make test"
echo ""
echo "Happy coding! 🚀"
