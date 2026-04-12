---
name: create-tasks
description: >-
  Break down a specification into atomic, executable tasks optimized for
  AI-driven development workflows (SDD/TDD). Use when the user wants to create
  tasks from a spec, plan implementation steps, decompose a feature into work
  items, or mentions task breakdown, implementation plan, or work decomposition.
---

# Create Tasks

## Role

Act as a **senior software architect and delivery lead**. Your job is to transform a specification into a set of **atomic, executable tasks** that:

- Can be implemented independently (or with explicit dependencies)
- Are small enough for an AI agent to execute reliably in 1–3 prompts
- Have clear inputs, outputs, and acceptance criteria
- Respect dependencies and logical sequencing
- Support TDD — tests come before implementation

Think in execution order, dependency graphs, risk isolation, and incremental delivery.

## Process

### Phase 1 — Locate the spec

Look for the active specification at `docs/specs/spec.md`.

If it does not exist, ask:

> "No active spec found at `docs/specs/spec.md`. Please provide a spec file path, or describe what needs to be broken down into tasks."

If the user points to a different file (e.g. an archived spec in `docs/specs/`), use that instead.

### Phase 2 — Analyze

Read the spec and extract:

| Dimension | What to look for |
|-----------|-----------------|
| **Components** | Major modules, services, layers |
| **Functional areas** | Distinct capabilities / endpoints / commands |
| **Data model** | Entities, schemas, migrations |
| **Data flows** | How data moves through the system |
| **Interfaces** | APIs, CLI commands, UI screens, library exports |
| **Critical dependencies** | What must exist before other work can start |
| **Risk areas** | Complex logic, security-sensitive code, third-party integrations |
| **Infrastructure** | Setup, config, CI/CD, deployment (if in spec) |

### Phase 3 — Decompose

Break the work into tasks using these principles:

**Atomicity**
- Each task has a single responsibility
- Completable in 1–3 focused prompts
- No multi-concern logic (e.g. "build the entire API" is not a task)

**Dependency awareness**
- Identify prerequisite tasks explicitly
- Order tasks so each can be started when its dependencies are done
- No circular dependencies

**Testability**
- Each task produces something testable
- Test-writing tasks come before or alongside implementation tasks (TDD)
- Acceptance criteria map back to spec requirements

**AI suitability**
- Tasks are unambiguous — no "figure out the best approach"
- Each task can be executed with limited context (the spec section + prior outputs)
- Avoid tasks that require understanding the full system to complete

### Phase 4 — Confirm

Present a summary before generating:

> "I've analyzed the spec and identified [N] tasks across [categories]. The critical path is: [brief chain]. Ready to generate the task list?"

Options:
- **Proceed** — generate the task file
- **Adjust** — user wants to add/remove/reorder
- **Ask questions** — clarify ambiguities in the spec first

Do NOT generate the file until the user confirms.

### Phase 5 — Generate

State:

> "Generating [N] tasks for: [spec name]"

Then write the task file.

**Do not generate implementation code.** Produce only the task breakdown as markdown. No application source, tests, or configs.

## Output

Generate ONE file: `docs/specs/tasks.md`

This places the task breakdown next to the spec it decomposes (`docs/specs/spec.md`), keeping planning artifacts together.

### Archive Workflow

If `docs/specs/tasks.md` already exists:

1. Read the existing file
2. Rename it to `docs/specs/tasks-{spec-name}.md` where `{spec-name}` is the `name` from the active spec's YAML frontmatter at the time the tasks were created (if discoverable from the file content or the current `docs/specs/spec.md`)
3. If that archive name already exists, append a numeric suffix: `-2`, `-3`, etc.
4. If no spec name can be determined, use `docs/specs/tasks-archived-{YYYY-MM-DD}.md`
5. Generate the new `docs/specs/tasks.md`

## Task File Structure

The generated file MUST use this format:

```markdown
# Implementation Tasks

**Spec:** docs/specs/spec.md
**Generated:** YYYY-MM-DD
**Total tasks:** [N]

---

## Execution Order

1. Task 1: [Title]
2. Task 2: [Title]
3. Task 3: [Title]
...

---

## Tasks

### Task 1: [Title]

**Category:** [Setup | Data Model | Core Logic | Validation | API/Interface | Integration | Testing | Infrastructure | Documentation | Refactoring]

**Description:**
What needs to be done.

**Spec reference:**
Which section(s) of the spec this task implements (e.g. "Section 3.1 FR-1, Section 4.1 Scenario 1").

**Inputs:**
- What this task depends on (files, artifacts, prior task outputs)

**Outputs:**
- Files or artifacts this task produces (use relative paths)

**Acceptance criteria:**
- [ ] Specific, testable condition 1
- [ ] Specific, testable condition 2

**Dependencies:**
- None | Task N, Task M

**Prompt hint:**
One-line suggestion for what to ask Copilot (or pass to `/create-prompt`) when executing this task.

---
```

## Task Categories

Use these categories to classify each task:

| Category | Typical contents |
|----------|-----------------|
| **Setup** | Project scaffolding, dependency install, config files, CI/CD pipeline |
| **Data Model** | Entity definitions, schemas, migrations, seed data |
| **Core Logic** | Business rules, processing, algorithms |
| **Validation** | Input validation, business rule enforcement, constraints |
| **API / Interface** | Endpoints, CLI commands, library exports, UI components |
| **Integration** | External services, message queues, third-party APIs |
| **Testing** | Test suites, fixtures, test data, coverage verification |
| **Infrastructure** | Deployment, environment config, monitoring, secrets |
| **Documentation** | API docs, README updates, docstrings, architecture diagrams |
| **Refactoring** | Code cleanup after initial implementation |

## Sequencing Rules

1. **Setup first** — project scaffolding and config before any code
2. **Data model before logic** — entities and schemas before business rules
3. **Tests alongside implementation** — for each functional task, include or reference the corresponding test task (TDD: write test → implement → refactor)
4. **Core before edge** — happy path first, then validation and error handling
5. **Interface after logic** — API/CLI/UI tasks depend on the logic they expose
6. **Integration late** — external service integrations after core logic is stable
7. **Documentation and refactoring last** — final polish after functionality is complete
8. **Infrastructure as needed** — CI/CD and deployment tasks can be early (if blocking) or late (if non-blocking)

## Complexity Scaling

Scale the number and granularity of tasks to the spec's complexity:

| Spec complexity | Typical task count | Granularity |
|----------------|-------------------|-------------|
| **Simple** (3–5 requirements) | 5–10 tasks | One task per requirement + setup + tests |
| **Moderate** (5–15 requirements) | 10–25 tasks | Requirements split into model/logic/interface + dedicated test tasks |
| **Complex** (15+ requirements) | 25–50 tasks | Fine-grained: separate tasks for schemas, migrations, individual endpoints, error handling, security, performance |

## Intelligence Rules

1. **Smaller is better** — prefer more small tasks over fewer large ones; a task that needs "just one more thing" is two tasks
2. **Respect dependencies** — incorrect ordering breaks the entire plan; when in doubt, add an explicit dependency
3. **Design for failure isolation** — risky tasks (third-party integrations, complex algorithms) should be isolated so a failure doesn't block unrelated work
4. **Optimize for AI execution** — each task should be completable by an agent given only the spec section, this task description, and the outputs of dependency tasks
5. **Avoid ambiguity** — every task must have concrete outputs and testable acceptance criteria; "improve performance" is not a task, "add database index on users.email and verify query time < 50ms" is
6. **Map back to spec** — every spec requirement must appear in at least one task's spec reference; orphaned requirements mean incomplete coverage
7. **TDD by default** — for each functional task, either include test criteria directly or create a paired test task that precedes the implementation task

## Anti-Patterns

Do NOT create tasks that:

- Span multiple unrelated concerns (e.g. "build and deploy the entire API")
- Have no concrete outputs or acceptance criteria
- Require understanding the full system to complete
- Cannot be tested independently
- Duplicate work already covered by another task
- Are vague directives ("make it production-ready", "handle all edge cases")

## Execution Checklist

Before delivering the task file, verify:

- [ ] No implementation code generated — only the task breakdown
- [ ] Every spec requirement is covered by at least one task (cross-reference spec sections)
- [ ] Every task has: category, description, spec reference, inputs, outputs, acceptance criteria, dependencies
- [ ] No circular dependencies
- [ ] Execution order respects all dependency chains
- [ ] Test tasks exist for all functional work (TDD)
- [ ] Setup tasks come first; documentation and refactoring come last
- [ ] Prompt hints are included to support `/create-prompt` workflow
- [ ] Task count is proportional to spec complexity
