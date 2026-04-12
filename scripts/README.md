# Scripts

This folder contains setup and automation scripts for initializing different language and infrastructure environments.

## Quick Start: Python + Terraform

To set up a project with both Python and Terraform (recommended for most projects):

```bash
bash scripts/enable-python.sh
bash scripts/enable-terraform.sh
```

Both scripts can be run in any order. The setup is idempotent, so you can run them multiple times safely.

## Python Setup

To enable Python development in your project:

```bash
bash scripts/enable-python.sh
```

This script will:
1. ✅ Create a Python virtual environment (`venv/`)
2. ✅ Install dependencies from `requirements.txt`
3. ✅ Enable GitHub Actions CI workflow (from `ci-python.template.yml`)
4. ✅ Merge Python pre-commit hook checks
5. ✅ Merge Python VS Code settings and extensions
6. ✅ Merge Python Makefile targets
7. ✅ Create `src/` and `tests/` directories

## Terraform Setup

To enable Terraform development in your project:

```bash
bash scripts/enable-terraform.sh
```

This script will:
1. ✅ Verify Terraform is installed
2. ✅ Enable GitHub Actions CI workflow (from `ci-terraform.template.yml`)
3. ✅ Merge Terraform pre-commit hook checks
4. ✅ Create Terraform directory structure (terraform/modules, terraform/envs, etc)
5. ✅ Merge Terraform VS Code settings and extensions
6. ✅ Merge Terraform Makefile targets
7. ✅ Create .terraform-version file

## How the Merge System Works

Instead of overwriting files when both Python and Terraform are enabled, the scripts use intelligent merge helpers:

- **`scripts/append-makefile.py`**: Merges language-specific Makefile targets without duplicates
- **`scripts/append-precommit.py`**: Merges language-specific pre-commit hook checks

This allows you to run both setup scripts and get a combined development environment with:
- ✅ Python Makefile targets (test, lint, format, type-check, etc)
- ✅ Terraform Makefile targets (init, validate, plan, etc)
- ✅ Python pre-commit checks (pytest, black, pylint, pyright)
- ✅ Terraform pre-commit checks (terraform fmt, terraform validate, tflint)
- ✅ Combined VS Code configuration with both language extensions

### After Python Setup

```bash
# Activate the virtual environment
source venv/bin/activate

# View all available commands
make help

# Run tests with coverage
make test

# Run tests in watch mode (auto-reload on file changes)
make test-watch

# Format code with Black
make format

# Run linters
make lint

# Run type checking
make type-check

# Run all checks (lint, format, type-check, test)
make all
```

### After Terraform Setup

```bash
# View all available commands
make help

# Initialize Terraform
make init

# Validate Terraform configuration
make validate

# Format Terraform code
make format

# Run TFLint linter
make lint

# Generate Terraform plan
make plan

# Run all checks (validate, format, lint)
make check
```

## What Gets Created/Modified

### Python Setup

| File | Purpose |
|------|---------|
| `venv/` | Python virtual environment |
| `Makefile` | Development commands (copied from `Makefile.python.template`) |
| `.github/workflows/ci.yml` | GitHub Actions CI (copied from `.github/ci-templates/ci-python.template.yml`) |
| `.git/hooks/pre-commit` | Pre-commit hook (copied from `.github/hooks/pre-commit.template`) |
| `.vscode/settings.json` | Updated with Python-specific settings |
| `.vscode/extensions.json` | Updated with Python-specific extensions |
| `src/__init__.py` | Python source directory marker |
| `tests/__init__.py` | Python tests directory marker |

### Terraform Setup

| File | Purpose |
|------|---------|
| `Makefile` | Development commands (copied from `Makefile.terraform.template`) |
| `.github/workflows/ci-terraform.yml` | GitHub Actions CI (copied from `.github/ci-templates/ci-terraform.template.yml`) |
| `terraform/envs/` | Terraform environments directory |
| `terraform/modules/` | Terraform modules directory |
| `terraform/common/` | Common Terraform code directory |
| `.terraform-version` | Terraform version lock file |
| `.vscode/settings.json` | Updated with Terraform-specific settings |
| `.vscode/extensions.json` | Updated with Terraform-specific extensions |

## VS Code Configuration Merge

Both setup scripts automatically:
1. Read language-specific settings and extensions (e.g., `settings.python.json`)
2. Merge them into the main `settings.json` and `extensions.json`
3. Set language-specific interpreter/formatter paths

This ensures that template users who don't use Python or Terraform are not polluted with their specific extensions and settings, but users who enable them get a fully configured VS Code experience.

See [.vscode/README.md](.vscode/README.md) for more details on the VS Code configuration system.

## Dependencies

### Python

The `requirements.txt` includes:
- **pytest** - Testing framework
- **pydantic** - Data validation
- **black** - Code formatter
- **flake8** - Linter
- **pylint** - Code analysis
- **pyright** - Type checker
- **python-dotenv** - Environment management

The `pyproject.toml` contains full project configuration including:
- Project metadata
- Dependency specifications
- Tool configurations (pytest, black, pylint, pyright)
- Coverage settings (minimum 80%)

### Terraform

Requires:
- **Terraform** - Infrastructure as Code tool (install separately)
- **TFLint** - Terraform linter (optional, but recommended)
  - Install: `brew install tflint` (macOS) or see https://github.com/terraform-linters/tflint


