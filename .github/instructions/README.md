# GitHub Copilot Custom Instructions

This directory contains language-specific and workflow-specific custom instructions for GitHub Copilot. These instructions guide Copilot's responses and code generation to follow your project's conventions and best practices.

## What Are Custom Instructions?

Custom instructions are files that provide Copilot with additional context and guidance on how to work with your codebase. They're similar to Cursor's `.mdc` rules but use GitHub's custom instructions format with glob patterns via YAML frontmatter.

**Copilot automatically applies relevant instructions based on the file you're working on.**

## Directory Structure

```
.github/instructions/
├── python/
│   ├── python-general.instructions.md       # General Python best practices
│   ├── python-fastapi.instructions.md       # FastAPI-specific guidelines
│   └── python-django.instructions.md        # Django-specific guidelines
├── javascript/
│   ├── react.instructions.md                # React/TypeScript best practices
│   └── nodejs.instructions.md               # Node.js backend best practices
├── terraform/
│   └── terraform.instructions.md            # Infrastructure as Code best practices
└── workflows/
    └── tdd.instructions.md                  # Test-Driven Development workflow
```

## How It Works

Each `.instructions.md` file contains:

1. **YAML Frontmatter:** Specifies which files the instructions apply to using glob patterns
   ```yaml
   ---
   applyTo: "**/*.py"
   excludeAgent: "code-review"  # Optional: exclude from specific agents
   ---
   ```

2. **Markdown Content:** Natural language guidelines and best practices

### Pattern Matching Examples

| Pattern | Matches |
|---------|---------|
| `**/*.py` | All Python files in all directories |
| `**/*.jsx,**/*.tsx` | JSX and TSX files |
| `**/fastapi/**/*.py` | Python files in FastAPI directories |
| `**/*.tf` | All Terraform files |

## Available Instructions

### Python Instructions

#### [python-general.instructions.md](python/python-general.instructions.md)
Applies to: All `.py` files

Covers:
- Test-Driven Development (TDD) with pytest
- Spec-Driven Development (SSD)
- Type hints and annotations
- Code structure and formatting
- Import organization
- Naming conventions
- Documentation standards
- Security best practices

#### [python-fastapi.instructions.md](python/python-fastapi.instructions.md)
Applies to: Python files in FastAPI projects

Covers:
- FastAPI architecture and best practices
- Async/await patterns
- Pydantic model validation
- Dependency injection
- API documentation and OpenAPI
- Performance optimization
- Security (CORS, authentication, rate limiting)

#### [python-django.instructions.md](python/python-django.instructions.md)
Applies to: Python files in Django projects

Covers:
- Django models, views, and templates
- Class-Based Views (CBVs)
- Authentication and authorization
- Database optimization (select_related, prefetch_related)
- Testing strategies
- Performance and caching
- Security practices

### JavaScript Instructions

#### [react.instructions.md](javascript/react.instructions.md)
Applies to: `.jsx` and `.tsx` files

Covers:
- React component structure
- TypeScript integration
- Import organization
- Naming conventions
- React hooks best practices
- Performance optimization
- Accessibility (a11y)
- Testing with React Testing Library

#### [nodejs.instructions.md](javascript/nodejs.instructions.md)
Applies to: `.js` and `.ts` files (Node.js backend)

Covers:
- Code structure and formatting
- Error handling
- Async/await patterns
- TypeScript usage
- API design (RESTful)
- Database practices
- Security best practices

### Infrastructure Instructions

#### [terraform.instructions.md](terraform/terraform.instructions.md)
Applies to: All `.tf` files

Covers:
- Terraform module organization
- Naming conventions
- Variables and outputs
- State management
- Security best practices
- Code quality
- Deployment strategies

### Workflow Instructions

#### [tdd.instructions.md](workflows/tdd.instructions.md)
Applies to: All `.py` files (workflow approach)

Covers:
- Red-Green-Refactor cycle
- Test structure (Arrange-Act-Assert)
- Testing tools (pytest)
- Test coverage
- Continuous Integration practices

## Using Custom Instructions

### Automatic Application

Copilot automatically applies matching instructions when you:
- Work in a file that matches the `applyTo` pattern
- Ask Copilot Chat questions with the file as context
- Use Copilot code suggestions in matching files

### In Copilot Chat

When using Copilot Chat, relevant instructions are automatically included in your requests. You'll see them referenced in the response (check the References section).

### Enabling/Disabling

Custom instructions are **enabled by default** for:
- Copilot code generation
- Copilot Chat
- Copilot code review

You can disable them in repository settings if needed:
1. Go to Settings > Copilot > Code review
2. Toggle "Use custom instructions when reviewing pull requests"

## Creating/Modifying Instructions

### Adding a New Instruction File

1. Create a new `.instructions.md` file in the appropriate subdirectory
2. Add YAML frontmatter with `applyTo` pattern:
   ```yaml
   ---
   applyTo: "**/*.ext"
   ---
   ```
3. Write your instructions in Markdown
4. Commit and push to your repository

### Best Practices for Instructions

- **Conciseness:** Keep instructions focused and actionable
- **Specificity:** Be specific about expectations and patterns
- **Language:** Use natural language; Copilot understands conversational guidance
- **Examples:** Include code examples when helpful
- **Prioritization:** Order guidelines by importance
- **Avoid Conflicts:** Try not to have conflicting instructions for the same file type

## Instruction Priorities

When multiple instruction files apply, they're all used together:
1. **Path-specific instructions** (most specific pattern)
2. **Repository-wide instructions** (if a `copilot-instructions.md` exists in `.github/`)
3. **Organization-wide instructions** (if configured)

## Examples in Action

### Example 1: Python File

When working on `src/services/user_service.py`, Copilot applies:
- ✅ `python/python-general.instructions.md` (matches `**/*.py`)
- ✅ `workflows/tdd.instructions.md` (matches `**/*.py`)

### Example 2: React Component

When working on `src/components/UserProfile.tsx`, Copilot applies:
- ✅ `javascript/react.instructions.md` (matches `**/*.tsx`)

### Example 3: FastAPI Route

When working on `app/routers/users.py`, Copilot applies:
- ✅ `python/python-general.instructions.md` (matches `**/*.py`)
- ✅ `python/python-fastapi.instructions.md` (matches `**/fastapi/**/*.py`)
- ✅ `workflows/tdd.instructions.md` (matches `**/*.py`)

## Troubleshooting

### Instructions Not Being Used

**Problem:** Custom instructions aren't showing in Copilot Chat references

**Solutions:**
1. Ensure the `.instructions.md` file exists in `.github/instructions/`
2. Check that the `applyTo` glob pattern matches your file
3. File must be in the context (attached to chat or open in editor)
4. Wait up to 1 minute for changes to propagate
5. Reload VS Code if changes don't appear

### Conflicting Instructions

**Problem:** Different instructions give conflicting guidance

**Solutions:**
1. Review both instruction files for conflicts
2. Specify more specific `applyTo` patterns
3. Consider merging related instructions
4. Use specific patterns to prevent overlap

## Further Resources

- [GitHub Docs: Custom Instructions](https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions)
- [Copilot Customization Library](https://github.com/github/copilot-docs/tree/main/docs/custom-instructions)
- [Agent Skills Specification](https://agentskills.io/specification)

## Migration from Cursor

If migrating from Cursor's `.mdc` rules:

| Cursor | Copilot |
|--------|---------|
| `.cursor/rules/` | `.github/instructions/` |
| `.mdc` files | `.instructions.md` files |
| `globs` frontmatter | `applyTo` frontmatter |
| File path pattern | Glob pattern in `applyTo` |

All instruction content remains largely the same; only the format and location change.