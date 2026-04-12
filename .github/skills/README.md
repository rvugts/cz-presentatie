# GitHub Copilot Skills

This directory contains custom agent skills for GitHub Copilot. These skills enhance Copilot's capabilities for specialized tasks in software development, security auditing, and workflow management.

## Available Skills

### create-spec
**Description:** Creates production-grade specifications for features or systems using specification-driven development (SDD). Guides the user through requirements gathering, then writes `docs/specs/spec.md` aligned with the project's spec template, archiving the previous active spec automatically.

**When to use:** When you need to write a spec, plan a new feature, design a system, or start an implementation using spec-driven development.

**Key features:**
- Guided 5-phase process: intake, analysis, contextual questioning, decision gate, generation
- Produces specs aligned with `docs/spec.template.md`
- Stack-specific guidance for Python, Node.js/TypeScript, Databricks/PySpark/SQL, and more
- Complexity scaling — lightweight specs for simple features, comprehensive for complex systems
- Every requirement maps to testable acceptance criteria (SDD + TDD ready)

### create-tasks
**Description:** Breaks down a specification (`docs/specs/spec.md`) into atomic, executable tasks optimized for AI-driven development workflows. Writes `docs/specs/tasks.md`, archiving any prior task file automatically.

**When to use:** After creating a spec with `create-spec`, when you need to plan implementation steps, decompose a feature into work items, or create a task breakdown for AI agents.

**Key features:**
- Reads the active spec at `docs/specs/spec.md` and decomposes it into ordered tasks
- Each task has: category, spec reference, inputs, outputs, acceptance criteria, dependencies
- TDD-aware sequencing (test tasks paired with implementation tasks)
- Prompt hints for each task to support the `create-prompt` / `run-prompt` workflow
- Complexity scaling: 5–10 tasks for simple specs, up to 50 for complex ones
- Archives previous `tasks.md` automatically when regenerating

### audit-security
**Description:** Performs a comprehensive security audit of the current codebase, identifying vulnerabilities and providing remediation strategies based on OWASP Top 10 2025 standards.

**When to use:** When you need to audit code for security vulnerabilities, authentication issues, input validation problems, or dependency risks.

**Key features:**
- OWASP Top 10 2025 compliance
- Deep-dive analysis of authentication, sessions, and tokens
- Input validation and sanitization checks
- Dependency scanning and supply chain security
- Generates detailed SECURITY_AUDIT_REPORT.md

### create-prompt
**Description:** Creates a new prompt that another agent can execute, using structured XML formatting and best practices for effective task delegation.

**When to use:** When you need to generate high-quality, structured prompts for complex coding tasks, analysis, or research that will be executed by agents.

**Key features:**
- Adaptive requirements gathering with contextual questioning
- XML-structured prompt generation
- Support for single or sequential multi-prompt workflows
- Saves prompts to ./prompts/ directory with proper numbering

### refactor-python
**Description:** Refactor Python code applying sound engineering practices, DRY, and security without altering functionality.

**When to use:** When refactoring Python files to improve maintainability, readability, and adherence to best practices.

**Key features:**
- Code structure optimization (line length, function length limits)
- Import organization and cleanup
- Type hints and documentation (docstrings)
- DRY principle enforcement
- Security checks (SQL injection prevention, input sanitization)
- Performance optimizations where beneficial

### run-prompt
**Description:** Delegate one or more prompts to fresh sub-task contexts with parallel or sequential execution.

**When to use:** When executing saved prompts from the ./prompts/ directory as isolated sub-tasks.

**Key features:**
- Single or sequential prompt execution
- Automatic prompt resolution by number or name
- Fresh context for each execution
- Git integration (staging and committing changes)
- Consolidated results reporting

## Installation

### Project-Level Skills (Recommended)
Project-level skills are stored in the repository and available to all contributors.

1. **Place skills in the repository:**
   - `.github/skills/` (GitHub Copilot standard)
   - `.claude/skills/` (Claude compatibility)
   - `.agents/skills/` (General agent compatibility)

2. **Commit and push** the skills directory to your repository.

3. **Skills are automatically discovered** by Copilot when working in this repository.

### Personal Skills
Personal skills are available across all your projects.

1. **Create the skills directory:**
   ```bash
   mkdir -p ~/.copilot/skills/
   # or ~/.claude/skills/ or ~/.agents/skills/
   ```

2. **Copy skill folders** from this repository to your personal skills directory.

3. **Skills are available** in all repositories where you use Copilot.

## Skill Invocation

### Automatic Invocation
Skills are automatically loaded when Copilot determines the task matches the skill's description. For example:
- Asking to "create a spec" or "write a specification" will invoke `create-spec`
- Asking to "break down the spec into tasks" or "create implementation tasks" will invoke `create-tasks`
- Mentioning "security audit" will likely invoke `audit-security`
- Requesting Python refactoring will invoke `refactor-python`
- Asking to create prompts will invoke `create-prompt`

### Explicit Invocation
You can force skill invocation in several ways:

#### 1. Mention the Skill Name
In your Copilot Chat request, explicitly mention the skill:
```
Use the audit-security skill to perform a security audit on this codebase.
```

#### 2. Slash Commands
Use slash commands in Copilot Chat:
```
/create-spec
/create-tasks
/audit-security
/refactor-python
/create-prompt
/run-prompt
```

#### 3. Agent Mode
Skills are fully supported in Copilot's agent mode and coding agent contexts.

## Skill Structure

Each skill follows the Agent Skills specification:
- `SKILL.md`: Contains YAML frontmatter with metadata and detailed instructions
- Optional subdirectories: `scripts/`, `references/`, `assets/`

## Requirements

- GitHub Copilot Pro, Pro+, Business, or Enterprise plan
- VS Code with GitHub Copilot extension
- For CLI usage: GitHub Copilot CLI (policy must be enabled in organization settings)

## Contributing

To add new skills:
1. Create a new directory with the skill name (lowercase, hyphens)
2. Add a `SKILL.md` file with proper YAML frontmatter
3. Follow the Agent Skills specification
4. Test the skill thoroughly

## Troubleshooting

- **Skill not loading:** Ensure the directory name matches the `name` field in `SKILL.md`
- **Skill not invoked:** Try explicit invocation methods
- **Permission issues:** Check that skills are in the correct directory and committed to repo for project skills

For more information, see the [Agent Skills specification](https://agentskills.io/specification).