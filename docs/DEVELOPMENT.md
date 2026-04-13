# Development Guide

Welcome to the project! This guide helps both humans and AI agents (like Copilot) understand our development practices and keep code quality high.

## Core Development Philosophy

We practice **Spec-Driven Development (SDD)** and **Test-Driven Development (TDD)** to keep AI agents on the rails and ensure features are correctly implemented from conception.

### Spec-Driven Development (SDD)

Before writing any code, features must have a specification:

1. **Create `docs/specs/spec.md`** using the `create-spec` skill or manually from `docs/spec.template.md`
2. Include: Context, Requirements, Edge Cases, Success Criteria
3. Get approval before starting implementation

**Why:** The spec is the contract. AI agents must reference `@docs/specs/spec.md` to validate their suggestions align with requirements. Previous specs are archived automatically in `docs/specs/` with descriptive names.

### Test-Driven Development (TDD)

All features use the **Red-Green-Refactor** workflow:

1. **Red:** Write a failing test that defines desired behavior
2. **Green:** Write minimal code to make the test pass
3. **Refactor:** Improve code quality while tests stay passing

**Why:** TDD ensures requirements are met and prevents "golden hammer" solutions by AI agents.

## Getting Started

### 1. Set Up Python Environment

For Python projects, use the automated setup script:

```bash
bash scripts/enable-python.sh
```

This will:
- Create a virtual environment (`venv/`)
- Install dependencies from `requirements.txt`
- Set up the pre-commit hook
- Enable GitHub Actions CI workflow
- Create `src/` and `tests/` directories

Then activate the environment:
```bash
source venv/bin/activate
```

### 2. Install Dependencies (Manual Setup)

If you don't want to use the script:

```bash
pip install -r requirements.txt      # Python dependencies
npm install                           # If applicable
```

### 3. Understand the Structure

```
project/
├── .github/
│   ├── copilot-instructions.md      # Repository-wide AI guidance
│   ├── instructions/                # Language-specific AI guidance
│   ├── skills/                      # Reusable Copilot skills
│   ├── prompts/                     # Reusable task prompts
│   ├── pull_request_template.md     # GitHub PR template
│   ├── hooks/                       # Git hook templates
│   └── ci-templates/                # CI/CD workflow templates
├── .vscode/
│   ├── settings.json                # Shared VS Code settings
│   └── extensions.json              # Recommended extensions
├── scripts/
│   ├── enable-python.sh             # Python environment setup script
│   └── README.md                    # Script documentation
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Python project configuration
├── docs/
│   ├── DEVELOPMENT.md               # This file
│   ├── TROUBLESHOOTING.md           # Common issues & solutions
│   ├── spec.template.md             # Template for feature specs
│   ├── specs/                       # Feature specifications
│   │   ├── spec.md                  # Current active spec
│   │   └── *.md                     # Archived previous specs
│   └── adr/                         # Architecture Decision Records
├── tests/
│   ├── test_example.py              # Reference TDD pattern
│   └── conftest.py                  # Shared pytest fixtures
└── src/                             # Implementation
```

### 4. Review Relevant Guidelines

**For all developers:**
- Read `.github/copilot-instructions.md` (repository-wide rules)
- Read `docs/adr/` (architectural decisions)
- Check `.vscode/settings.json` and `.vscode/extensions.json` (shared environment)

**For Python developers:**
- Read `.github/instructions/python/python-general.instructions.md`
- Consult `pyproject.toml` for tool configurations (pytest, black, pylint, pyright)
- Use `scripts/enable-python.sh` for initial setup

**For your specific language/role:**
- **Python:** Read `.github/instructions/python/python-general.instructions.md`
- **FastAPI:** Read `.github/instructions/python/python-fastapi.instructions.md`
- **Django:** Read `.github/instructions/python/python-django.instructions.md`
- **React/TypeScript:** Read `.github/instructions/javascript/react.instructions.md`
- **Node.js backend:** Read `.github/instructions/javascript/nodejs.instructions.md`
- **Terraform/IaC:** Read `.github/instructions/terraform/terraform.instructions.md`
- **Testing patterns:** Read `.github/instructions/workflows/tdd.instructions.md`

## Development Workflow

### Creating a New Feature

```bash
# 1. Create specification (use create-spec skill or copy template)
cp docs/spec.template.md docs/specs/spec.md
# Edit with requirements, edge cases, success criteria

# 2. Get approval (team review)
# [ ] Spec reviewed and approved

# 3. Create feature branch
git checkout -b feature/your-feature-name

# 4. Write test first (Red phase)
# See tests/test_example.py for pattern
pytest tests/test_your_feature.py -v

# 5. Implement to pass test (Green phase)
# Follow language-specific instructions in .github/instructions/

# 6. Refactor for quality (Refactor phase)
# Use /refactor-python skill in Copilot Chat if applicable
# See .github/skills/README.md for available skills

# 7. Verify spec alignment
# Run: python scripts/validate-spec.py (if exists)
# Manual check: Does code match docs/specs/spec.md exactly?

# 8. Commit with clear message
git add .
git commit -m "feat: description following conventional commits"

# 9. Push and create PR
git push origin feature/your-feature-name
# See .github/pull_request_template.md for PR checklist
```

### Using Copilot Effectively

**Copilot Skills Available:**

Invoke with `/` in Copilot Chat:
- `/create-spec` - Generate feature specifications (SDD)
- `/create-tasks` - Break down a spec into executable tasks
- `/audit-security` - Security audit of codebase
- `/generate-prompt` - Generate reusable prompts
- `/refactor-python` - Refactor Python code
- `/run-prompt` - Execute saved prompts

See `.github/skills/README.md` for details.

**Requesting Features from Copilot:**

```
✅ GOOD:
Create a Python function to validate email addresses.
Follow TDD - write tests first. Reference python-general.instructions.md
and ensure the implementation aligns with @docs/specs/spec.md section 2.1.

❌ BAD:
Write validation code for emails.
```

**Keeping Copilot on Rails:**

Always include:
1. Reference to @docs/specs/spec.md (if applicable)
2. Expected language/framework (Python, React, etc.)
3. TDD requirement (write tests first)
4. Acceptance criteria

## Code Quality Standards

### Type Hints
- **Required for all Python functions and methods**
- Use `typing` module for complex types
- Example: `def process_data(items: List[Dict[str, Any]]) -> bool:`

### Testing
- **Minimum coverage: 80%** (configured in `pyproject.toml`)
- **All tests must pass before commit** (enforced by pre-commit hook)
- Use `pytest` fixtures from `tests/conftest.py` (create if needed)
- Follow test pattern in `tests/test_example.py`
- Configure in `pyproject.toml` under `[tool.pytest.ini_options]`

### Line Length
- **Python:** Maximum 100 characters
- **JavaScript/TypeScript:** Maximum 100 characters

### Documentation
- **Docstrings required** for all modules, classes, and public functions
- Use **Sphinx format** for Python: `:param`, `:return:`, `:raises:`
- Include examples for complex functions

### Security
- **No hardcoded secrets** - use environment variables
- **Parameterized queries only** - never string concatenation for SQL
- **No eval() or exec()** - ever
- **Sanitize all user inputs**
- Validate API requests with models (Pydantic for FastAPI, marshmallow for Django)

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test
pytest tests/test_specific.py::test_function

# Watch mode (auto-rerun on file changes)
pytest-watch
```

## Pre-commit Hook Setup (Python Projects)

To enforce code quality standards automatically in Python projects, install the pre-commit hook:

```bash
# Copy the template to your local hooks directory
cp .github/hooks/pre-commit.template .git/hooks/pre-commit

# Make it executable
chmod +x .git/hooks/pre-commit
```

The hook will run before each commit and check:
- Tests pass with 80%+ coverage
- Type checking (if pyright available)
- Linting (if pylint available)
- Code formatting (if black available)
- No obvious hardcoded secrets
- Commit message format

**Note:** This hook is not active in the starter template itself to avoid issues during initial setup.

## Code Review Checklist

Before submitting a PR, ensure:
- [ ] Tests written first (Red phase complete)
- [ ] All tests passing (`pytest --cov=src --cov-fail-under=80`)
- [ ] Code follows language-specific instructions (`.github/instructions/`)
- [ ] `docs/specs/spec.md` alignment verified (if feature-related)
- [ ] Type hints on all functions
- [ ] No hardcoded secrets or credentials
- [ ] Complex logic has inline comments
- [ ] Docstrings follow Sphinx format
- [ ] Commits follow conventional commits format
- [ ] No `eval()`, `exec()`, or other security anti-patterns

For detailed PR checklist, see `.github/pull_request_template.md`

## Architecture Decisions

Major architecture decisions are recorded in `docs/adr/` using ADR format.

When making significant technical decisions:
1. Check existing ADRs to understand context
2. Create new ADR following the template in `docs/adr/adr.template.md`
3. Reference relevant ADRs in your implementation

Examples:
- **ADR-001:** Monolithic backend architecture
- **ADR-002:** Async by default for I/O operations

## Troubleshooting

Having issues with Copilot guidance? See `docs/TROUBLESHOOTING.md` for common problems and solutions.

## Additional Resources

- **GitHub Copilot Skills:** `.github/skills/README.md`
- **Custom Instructions:** `.github/instructions/README.md`
- **Architecture Decisions:** `docs/adr/`
- **Spec Template:** `docs/spec.template.md`
- **Active Spec:** `docs/specs/spec.md` (archived specs in the same folder)
- **Test Example:** `tests/test_example.py`

---

**Questions?** Check the relevant guide above or open an issue for clarification.
