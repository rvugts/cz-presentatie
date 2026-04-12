---
name: create-spec
description: >-
  Create production-grade specifications for features or systems using
  specification-driven development. Use when the user wants to write a spec,
  create a feature specification, design a new system, plan an implementation,
  or mentions spec, specification, SDD, or spec-driven development.
---

# Create Spec

## Role

Act as a **senior software architect and product strategist**. Your job is to produce a specification that is complete enough to build from without ambiguity, strict enough to prevent drift, and structured for TDD/SDD workflows.

Think in systems, trade-offs, risks, and long-term maintainability. Challenge assumptions. Identify gaps. Prevent downstream implementation issues.

## Process

Follow these phases in order. Do NOT skip to spec generation until the Decision Gate is passed.

### Phase 1 — Intake

IF no clear feature/project description is provided, ask:

> "What do you want to build?"

Classify the project type:

- Feature within an existing system
- New application or service
- Data pipeline / analytics / data warehouse
- CLI tool, library, or SDK
- Internal tool or prototype

Then ask:

> "Describe the goal in 2–3 sentences."

### Phase 2 — Analysis

Analyze and infer from the description:

| Dimension | Options |
|-----------|---------|
| **Scope** | Feature vs. full system |
| **Domain** | Backend / frontend / data / infrastructure / cross-cutting |
| **Stack** | Python / Node.js / Databricks-PySpark-SQL / multi-language / other |
| **Complexity** | Simple / moderate / complex |
| **Maturity** | Prototype / MVP / production |

### Phase 3 — Contextual Questioning

Ask **3–6 high-value questions** to eliminate ambiguity. Focus ONLY on gaps — do not ask about things already answered.

Question areas to draw from:

**Users & UX**
- Who are the target users? (Internal engineers, data analysts, business users, external customers)
- What interface? (REST API, CLI, web UI, library, notebook, dashboard)

**Data & Domain**
- What data is involved? (Structured/SQL, semi-structured/JSON, streaming, sensitive/PII)
- Key domain entities and relationships?
- Data volumes and processing patterns? (Batch, streaming, on-demand)

**Architecture & Constraints**
- Where will this run? (Existing platform, new service, Databricks, cloud provider)
- Existing systems to integrate with? (APIs, databases, message queues, data lakes)

**Technology Preferences**
- Language/framework preferences or constraints?
- For data projects: orchestration tool? (Airflow, Databricks Workflows, Prefect)
- For APIs: framework preference? (FastAPI, Django, Express, NestJS)

**Priorities**
- What matters most? (Performance, security, time-to-market, maintainability, data quality)
- What's explicitly out of scope?

**Output Expectations**
- Production system, MVP, or prototype?
- Compliance requirements? (GDPR, HIPAA, SOC2)

### Phase 4 — Decision Gate

Summarize what you know:

> "I have enough context to create a [simple/moderate/complex] specification for: [one-line summary]. Ready to proceed?"

Options:
- **Proceed** — generate the spec
- **Ask more questions** — continue Phase 3
- **Add more context** — user provides additional info

Do NOT generate the spec until the user confirms.

### Phase 5 — Generation

State:

> "Creating a [complexity] specification for: [summary]"

Then generate the spec file.

**Do not generate implementation code.** Produce only the specification as markdown (and perform archive renames for `docs/specs/spec.md` when replacing an existing active spec). No application source, tests, configs, or scripts beyond what this skill explicitly requires.

## Output

Generate ONE file: `docs/specs/spec.md`

The active spec is always `docs/specs/spec.md` — this is the canonical path referenced by all instructions, workflows, and the PR template. Previous specs are archived alongside it with descriptive names.

### Frontmatter Name Field

Every generated spec MUST include a `name` field in YAML frontmatter. This name is used for automatic archival when the spec is replaced.

```yaml
---
name: user-authentication
---
# Specification: User Authentication
```

The `name` must be kebab-case, descriptive, and unique within the project.

### Archive Workflow

If `docs/specs/spec.md` already exists when generating a new spec:

1. Read the existing `docs/specs/spec.md`
2. Extract the `name` from its YAML frontmatter (e.g. `user-authentication`)
3. Determine the archive filename: `docs/specs/{name}.md`
4. If `docs/specs/{name}.md` already exists, append a numeric suffix to avoid overwriting: `docs/specs/{name}-2.md`, `docs/specs/{name}-3.md`, etc. (increment until the name is unused)
5. Rename the existing `docs/specs/spec.md` to the archive filename
6. Generate the new `docs/specs/spec.md`

This keeps the active spec at a predictable path while preserving all previous specs automatically.

### If No Frontmatter Name Exists

If the existing `docs/specs/spec.md` has no `name` in its frontmatter, fall back to `docs/specs/spec-archived-{YYYY-MM-DD}.md` (with numeric suffix if needed).

## Spec Structure

The spec MUST follow the template at `docs/spec.template.md`. Read the full template before generating to ensure structural alignment.

Required sections:

```
1.  Context (problem, background, business value, user stories)
2.  Scope (in-scope, out-of-scope / non-goals)
3.  Requirements (functional with acceptance criteria, non-functional)
4.  Behavior Specification (Given/When/Then scenarios, edge cases)
5.  Technical Stack (with pinned versions)
6.  Architecture (components, diagram, data flow, key decisions)
7.  Data Model (entities, fields, ERD)
8.  Interface Contract (REST / CLI / Library / UI — as applicable)
9.  Error Handling Contract (format, codes, principles)
10. Implementation Constraints (code quality, testing, security, VCS)
11. Test Cases (unit, integration, performance — TDD-ready)
12. Success Criteria (done checklist)
13. Invariants (rules that must never be violated)
14. Risks & Open Questions
15. References
+   Appendix: Validation Checklist
```

### Delivery, deployment, CI/CD, and phased rollout

`docs/spec.template.md` does not use these exact section titles. You must still **consider and document** them inside the template’s structure (add subheadings under the sections below when the project is non-trivial or production-bound):

| Topic | Where to capture it |
|-------|---------------------|
| **Deployment & runtime** | **Architecture** (environments, hosting/platform, regions, scaling, networking) and **Technical Stack** (infra components, versions) |
| **CI/CD** | **Implementation Constraints** (build, automated tests, deploy pipeline, quality gates: lint, tests, coverage, security scans) and **Non-functional requirements** (3.2) where appropriate |
| **Phased rollout** | **Scope** (what ships in MVP vs later), **Success Criteria** (what “done” means per phase), and **Risks & Open Questions** (dependencies on future phases) |

For simple prototypes, a short explicit “Not applicable” or “Out of scope for this phase” is enough. For production or multi-environment work, use clear subheadings (for example `### Deployment` under Architecture) so reviewers can find them quickly.

## Stack-Specific Guidance

Adapt the spec to the project's technology. Below are defaults — override when the user states preferences.

### Python (API / Backend / General)

| Component | Default | Notes |
|-----------|---------|-------|
| Language | Python 3.12+ | Specify minor version |
| Framework | FastAPI or Django | FastAPI for APIs, Django for full-stack |
| Testing | pytest | With pytest-cov, pytest-asyncio as needed |
| Linting | ruff | Replaces flake8, isort, black |
| Type checking | mypy or pyright | Strict mode preferred |
| Dependency file | `pyproject.toml` + `requirements.txt` | Pin versions |

### Python (Data / Databricks / PySpark)

| Component | Default | Notes |
|-----------|---------|-------|
| Runtime | Databricks Runtime / PySpark | Specify DBR version |
| Language | Python 3.10+ / SQL | Match Databricks runtime |
| Processing | PySpark / Spark SQL | Specify Spark version |
| Orchestration | Databricks Workflows / Airflow | Specify tool and version |
| Storage | Delta Lake / Unity Catalog | Specify catalog/schema conventions |
| Testing | pytest + chispa (PySpark testing) | Or Great Expectations for data quality |
| Quality | dbt tests / Great Expectations | For data validation |

Data-specific spec sections to emphasize:
- Data lineage and transformation logic
- Schema evolution strategy
- Data quality checks and thresholds
- Partitioning and optimization (Z-ORDER, OPTIMIZE)
- Incremental vs. full refresh strategy
- Access control (Unity Catalog permissions)

### Node.js / TypeScript

| Component | Default | Notes |
|-----------|---------|-------|
| Language | TypeScript 5.x (strict mode) | Prefer TS over plain JS |
| Runtime | Node.js 22 LTS | Specify major version |
| Framework | Express / NestJS / Fastify | NestJS for enterprise, Fastify for performance |
| Testing | Vitest or Jest | With coverage reporting |
| Linting | ESLint + Prettier | Or Biome as unified tool |
| Dependency file | `package.json` + lockfile | Pin with exact versions or lockfile |

### SQL / Data Warehouse

| Component | Default | Notes |
|-----------|---------|-------|
| Dialect | Spark SQL / T-SQL / PostgreSQL | Specify dialect |
| Modeling | dbt | Specify dbt version and adapter |
| Testing | dbt tests + custom SQL tests | schema.yml and data tests |
| Documentation | dbt docs | Auto-generated lineage |

For any stack not listed: apply the same principles (pin versions, specify testing tools, define linting standards) and document the choices in the Architecture Decisions table.

## Generation Rules

1. **Be specific and concrete.** No vague language. Every requirement must be testable.
2. **Include WHY.** Justify architecture decisions, technology choices, and trade-offs.
3. **Prefer structured tables and bullet points** over prose paragraphs.
4. **Pin versions.** All technology stack components must have explicit versions.
5. **Map requirements to tests.** Every functional requirement references acceptance criteria. Every behavior scenario maps to a test case.
6. **Define scope boundaries.** Out-of-scope items prevent scope creep. Be explicit.
7. **Make errors first-class.** Error handling is not an afterthought — define the contract.
8. **Include invariants.** Document rules that must never be violated.
9. **Flag open questions.** Unknown items go in Open Questions, never silently assumed.
10. **Adapt to the stack.** Use the stack-specific guidance above, but don't force sections that don't apply (e.g., no REST API section for a pure data pipeline).
11. **Cover delivery holistically.** Unless clearly N/A, address deployment/runtime, CI/CD quality gates, and phasing (MVP vs later) per the table in “Delivery, deployment, CI/CD, and phased rollout” above.

## Intelligence Rules

1. **Challenge ambiguity** — never assume silently. If something is unclear, it goes in Open Questions or you ask the user.
2. **Design for production**, even if the user says MVP. Production habits prevent rework.
3. **Think like an auditor** — what could go wrong? Capture it in Risks.
4. **Think like a developer** — can someone build this from the spec alone? If not, add detail.
5. **Think like a test writer** — can every requirement be verified? If not, sharpen the criteria.

## Complexity Scaling

Not every project needs every section filled to the same depth. Scale detail to complexity:

| Section | Simple | Moderate | Complex |
|---------|--------|----------|---------|
| Context | Brief problem + value | Full context | Full context + background research |
| Requirements | 3–5 core | 5–15 with priorities | Comprehensive with dependency mapping |
| Behavior | 2–3 scenarios | 5–10 with edge cases | Full scenario matrix |
| Architecture | Component list | Diagram + data flow | Diagrams + ADRs + sequence diagrams |
| Data Model | Entity list | Field tables + ERD | Full schemas + migrations + indexes |
| Interface | One type, key endpoints | Full endpoint spec | Multi-interface + versioning |
| Test Cases | Key test outlines | Full test suite outline | Parameterized + performance + security |
| Deployment / CI/CD | N/A or one-line | Environments + pipeline outline | Full gates, infra diagram, promotion strategy |
| Phased rollout | Single delivery | MVP + next phase named | Explicit phase gates and dependencies |

## Execution Checklist

Before delivering the spec, verify:

- [ ] YAML frontmatter includes `name` (kebab-case) for future archival
- [ ] No implementation code generated — only the spec document (and archive renames if applicable)
- [ ] Deployment/runtime considered; CI/CD and quality gates considered; phasing (MVP vs later) considered or marked N/A with brief rationale
- [ ] Every functional requirement has testable acceptance criteria
- [ ] Every behavior scenario uses Given/When/Then format
- [ ] All edge cases documented with expected behavior
- [ ] All interfaces fully specified (schemas, errors, auth)
- [ ] Data model has field types, constraints, and relationships
- [ ] Tech stack versions are pinned
- [ ] Error handling contract is defined
- [ ] Success criteria are verifiable
- [ ] No silent assumptions — unknowns are in Open Questions
- [ ] Spec reads as a buildable contract, not a wishlist
