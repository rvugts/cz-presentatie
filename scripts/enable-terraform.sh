#!/bin/bash

# Enable Terraform Development Environment
# This script sets up a Terraform project with:
# - Terraform workflow checks
# - GitHub Actions CI workflow
# - Terraform directory structure
# - Linting and formatting (tflint, terraform fmt)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$REPO_ROOT"

echo "🏗️  Enabling Terraform Development Environment..."
echo ""

# ============================================================================
# 1. Check if Terraform is Installed
# ============================================================================

if ! command -v terraform &> /dev/null; then
    echo "⚠️  Terraform is not installed"
    echo ""
    echo "Install Terraform from: https://www.terraform.io/downloads"
    echo "On macOS: brew install terraform"
    echo "On Linux: sudo apt-get install terraform"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Terraform $(terraform version -json | jq -r '.terraform_version') installed"
fi

echo ""

# ============================================================================
# 2. Install Terraform Tools
# ============================================================================

echo "📚 Installing Terraform tools..."

# TFLint for linting (optional)
if ! command -v tflint &> /dev/null; then
    echo "⚠️  TFLint not installed (optional)"
    echo "   Install: curl https://raw.githubusercontent.com/terraform-linters/tflint/master/install_linux.sh | bash"
    echo "   Or macOS: brew install tflint"
else
    echo "✅ TFLint installed"
fi

echo ""

# ============================================================================
# 3. Enable Terraform GitHub Actions CI Workflow
# ============================================================================

if [ ! -f ".github/workflows/ci-terraform.yml" ]; then
    echo "🚀 Enabling GitHub Actions CI workflow..."
    cp .github/ci-templates/ci-terraform.template.yml .github/workflows/ci-terraform.yml
    echo "✅ CI workflow enabled at .github/workflows/ci-terraform.yml"
else
    echo "✅ CI workflow already exists at .github/workflows/ci-terraform.yml"
fi

echo ""

# ============================================================================
# 4. Merge Terraform Pre-commit Hook Checks
# ============================================================================

echo "🔒 Setting up pre-commit hook..."
if [ -d ".git" ]; then
    python3 scripts/append-precommit.py terraform
else
    echo "⚠️  Not a git repository yet, skipping pre-commit hook"
fi

echo ""

# ============================================================================
# 5. Merge Terraform Makefile Targets
# ============================================================================

echo "📋 Setting up Makefile..."
python3 scripts/append-makefile.py terraform

echo ""

# ============================================================================
# 6. Create Terraform Directory Structure
# ============================================================================

echo "📁 Creating Terraform directory structure..."

directories=(
    "terraform/envs"
    "terraform/modules"
    "terraform/common"
)

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "  ✅ Created $dir/"
    fi
done

# Create a basic .terraform-version file if it doesn't exist
if [ ! -f ".terraform-version" ]; then
    terraform version -json 2>/dev/null | jq -r '.terraform_version' > .terraform-version 2>/dev/null || echo "1.14.8" > .terraform-version
    echo "  ✅ Created .terraform-version"
fi

echo ""

# ============================================================================
# 7. Merge Terraform VS Code Configuration (Optional)
# ============================================================================

if [ -f ".vscode/merge-configs.py" ]; then
    echo "🔧 Merging Terraform VS Code settings and extensions..."
    python3 .vscode/merge-configs.py terraform
    echo "✅ VS Code configuration updated"
    echo ""
fi

# ============================================================================
# ✨ Setup Complete
# ============================================================================

echo "✨ Terraform development environment is ready!"
echo ""
echo "Setup includes:"
echo "  ✅ Terraform verification"
echo "  ✅ GitHub Actions CI workflow (.github/workflows/ci-terraform.yml)"
echo "  ✅ Terraform directory structure (terraform/modules, terraform/envs, etc)"
echo "  ✅ Pre-commit hooks for Terraform validation"
echo "  ✅ Makefile with common commands (make help)"
echo "  ✅ VS Code configuration (optional)"
echo ""
echo "Next steps:"
echo "  1. View commands: make help"
echo "  2. Initialize: make init"
echo "  3. Create your Terraform code in terraform/ directory"
echo "  4. Validate: make validate"
echo "  5. Format: make format"
echo ""
echo "Happy infrastructure as code! 🚀"
