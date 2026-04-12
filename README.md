# Copilot Dev Starter

A comprehensive starter template for Copilot-powered development projects. Includes agent rules, skills, templates, and workflows supporting Specification-Driven Development (SDD) and Test-Driven Development (TDD).

This repository provides:
- GitHub Copilot agent rules and instructions in `.github/`
- Copilot skills and prompts for secure coding, prompt creation, refactoring, and testing
- Templates and docs supporting Specification-Driven Development (SDD) and Test-Driven Development (TDD)
- Architecture Decision Records in `docs/adr/`

## Key files

- `LICENSE.md` — project license
- `README.md` — project overview
- `CONTRIBUTING.md` — guidelines for extending the template
- `CODE_OF_CONDUCT.md` — community standards
- `requirements.txt` — Python dependencies for SDD/TDD development
- `pyproject.toml` — Python project configuration and tool settings
- `docs/DEVELOPMENT.md` — development workflow and standards
- `docs/specs/spec.md` — active feature specification (when present); archived specs live in `docs/specs/` too
- `docs/TROUBLESHOOTING.md` — common issues and fixes
- `docs/VIBE_CODING_GUIDE.md` — contributor guide and Copilot best practices
- `.github/copilot-instructions.md` — repository-wide Copilot guidance
- `.github/instructions/` — language-specific instruction files
- `.github/skills/` — reusable Copilot skills (create-spec, create-tasks, audit-security, refactor-python, create-prompt, run-prompt)
- `.github/hooks/pre-commit.template` — pre-commit hook template for Python projects (copy to `.git/hooks/pre-commit`)
- `.github/ci-templates/` — CI workflow templates (copy and customize)
- `.vscode/settings.json` — shared VS Code settings for the project
- `.vscode/extensions.json` — recommended VS Code extensions

## Getting started

### Install this template for a new project

For a new project, do not simply clone this repository and keep its `.git` history. That would link your project to the template repo and pollute your own commit history.

Use one of these approaches instead:

- **Create a new repo from this template on GitHub:** This repository is configured as a GitHub template, so use the **Use this template** button to create a fresh repo when your organization allows creating new repos on GitHub.
- **Download the repository archive:** Download the ZIP from GitHub, extract it into a new project folder, then initialize your own git repository.
- **Clone then reinitialize git:** If you need a local-only start, clone locally, delete the `.git` folder, and run `git init` inside the new project directory before making your first commit.

Example:

```bash
git clone https://github.com/<owner>/copilot-dev-starter.git my-new-project
cd my-new-project
rm -rf .git
git init
```

### Start using the template

1. **Read the Vibe Coding Guide:** Start with `docs/VIBE_CODING_GUIDE.md` for development philosophy and Copilot best practices
2. **For Python development:** Run `bash scripts/enable-python.sh`
3. **For Terraform:** Run `bash scripts/enable-terraform.sh`
4. Review `.github/copilot-instructions.md`
5. Read `docs/DEVELOPMENT.md` for workflow and quality standards
6. Create a spec for your feature using the `create-spec` skill (or manually from `docs/spec.template.md`)
7. Write tests first, then implement code
8. Use the Copilot skills in `.github/skills/` as needed

## Specification-Driven Development

This template supports SDD — every feature starts with a specification that serves as the contract between requirements and implementation.

**Quick start:**
1. Ask Copilot to use the `create-spec` skill, or invoke `/create-spec`
2. Answer the guided questions about your feature
3. The skill writes `docs/specs/spec.md` (archiving any previous active spec using its frontmatter `name`), aligned with `docs/spec.template.md`
4. Use the `create-tasks` skill (or invoke `/create-tasks`) to decompose the spec into an ordered, executable task list at `docs/specs/tasks.md`
5. Work through the tasks in order — write tests first (TDD), then implement
6. Use `/create-prompt` and `/run-prompt` to delegate individual tasks to Copilot agents

The `create-spec` and `create-tasks` skills support Python, Node.js/TypeScript, Databricks/PySpark/SQL, and other stacks. See `.github/skills/` for details.

## Contributing

This repository is intended as a starting point for Copilot-powered projects. If you want to extend the template:
- Add new `docs/` templates for your workflow
- Add new Copilot skills in `.github/skills/`
- Keep the root docs and license up to date
