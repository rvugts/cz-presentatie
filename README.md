# Copilot Dev Starter

A comprehensive starter template for Copilot-powered development projects. Includes agent rules, skills, templates, and workflows supporting Specification-Driven Development (SDD) and Test-Driven Development (TDD).

This repository provides:
- GitHub Copilot agent rules and instructions in `.github/`
- Copilot skills and prompts for secure coding, prompt creation, refactoring, and testing
- Templates and docs supporting Specification-Driven Development (SDD) and Test-Driven Development (TDD)
- Architecture Decision Records in `docs/adr/`
- A claims data quality validator implementation in `src/claims_validation/`

## Claims Validator

The active specification in `docs/specs/spec.md` is implemented as a reusable validator package with:
- Row-level rules (amount/date checks)
- Dataset-level rules (duplicate claim IDs)
- A PySpark-compatible validation engine entrypoint
- Structured, deterministic validation error reporting

### Run validation locally (library mode)

```bash
source ./venv/bin/activate
PYTHONPATH=src python - <<'PY'
from datetime import date
from claims_validation.engine import validate_claims

claims = [
    {
        "claim_id": "C-100",
        "patient_id": "PAT-001",
        "provider_id": "PRV-001",
        "treatment_code": "TREAT-100",
        "amount": -5.0,
        "claim_date": date(2026, 4, 10),
        "submitted_date": date(2026, 4, 9),
        "status": "submitted",
    }
]

violations = validate_claims(
    claims=claims,
    patient_ids={"PAT-001"},
    provider_ids={"PRV-001"},
)
print(violations)
PY
```

Expected result: a list of violation records with codes like
`VALIDATION_NEGATIVE_AMOUNT` and `VALIDATION_INVALID_DATE_ORDER`.

### Run validation in Databricks (table mode)

The table runner reads hardcoded sources:
- `workspace.demo.claims`
- `workspace.demo.patients`
- `workspace.demo.providers`

and writes canonical JSON output to `/dbfs/tmp/validation_report.json`.

```bash
%sh
cd /Workspace/Repos/<your-org>/cz-presentatie
source ./venv/bin/activate
PYTHONPATH=src python scripts/run_claims_validation_from_tables.py
```

Then inspect output:

```bash
%sh cat /dbfs/tmp/validation_report.json
```

### JSON error contract and code categories

Runner output is a JSON array of records in this envelope format:

```json
{
  "error": {
    "code": "VALIDATION_NEGATIVE_AMOUNT",
    "message": "Claim amount must be non-negative.",
    "details": {
      "claim_id": "C-100",
      "field": "amount",
      "value": -5.0
    },
    "request_id": "validation-run-uuid"
  }
}
```

Code categories used by the implementation:
- `VALIDATION_*`
- `NOT_FOUND_*`
- `CONFLICT_*`
- `SERVER_*`

Source of truth: `src/claims_validation/types.py`.

### Add a new validation rule

1. Add or update tests in `tests/claims_validation/` (Red).
2. Implement the rule in `src/claims_validation/rules/`:
   - Row rule: function signature `rule(claim) -> list[Violation]`
   - Dataset rule: function signature `rule(claims) -> list[Violation]`
3. Register the rule in `src/claims_validation/rules/registry.py`:
   - `get_row_rules(...)` for row checks
   - `get_dataset_rules()` for dataset checks
4. Add any new stable code constant/message in `src/claims_validation/types.py`.
5. Re-run validator tests and quality gates.

### Run tests (validator)

```bash
source ./venv/bin/activate
PYTHONPATH=src pytest tests/claims_validation -v
```

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
