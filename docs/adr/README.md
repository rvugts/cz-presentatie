# Architecture Decision Records (ADRs)

This directory contains Architecture Decision Records for the project. An ADR is a short document describing an important architectural decision and its context, consequences, and alternatives.

## What is an ADR?

An ADR captures a single significant technical decision that affects the codebase. It includes:
- **Context**: The problem or question that led to the decision
- **Decision**: What we decided to do
- **Rationale**: Why we made this decision
- **Consequences**: The implications of this decision (positive and negative)
- **Alternatives**: Other options we considered and why we rejected them

ADRs are permanent records that help team members (and AI agents like Copilot) understand the reasoning behind technical choices.

## Files in This Directory

### Core Architecture

- **[ADR-001: Monolithic Backend Architecture](./ADR-001-monolithic-backend-architecture.md)**
  - Decision to build a single FastAPI monolith rather than microservices
  - Status: Accepted | Date: 2026-04-07

- **[ADR-002: Async I/O by Default](./ADR-002-async-io-by-default.md)**
  - Decision to use async/await for all I/O operations
  - Status: Accepted | Date: 2026-04-07

## Creating a New ADR

### When to Create an ADR

Create an ADR when:
- Making a significant architectural decision that affects multiple team members
- Choosing between competing approaches (monolith vs microservices, sync vs async, etc.)
- Establishing patterns that will be used repeatedly (testing strategy, API design, etc.)
- Documenting important constraints or limitations

**Don't** create an ADR for:
- Minor implementation decisions (library choices, function names)
- Tactical changes that don't affect architecture
- Bug fixes or performance tweaks

### How to Create an ADR

1. **Copy the template:**
   ```bash
   cp docs/adr/adr.template.md ADR-XXX-short-title.md
   ```

2. **Find the next ADR number:**
   - Look at existing ADRs (ADR-001, ADR-002, etc.)
   - Use next sequential number (e.g., ADR-003)

3. **Follow the format:**
   - MUST include: Context, Decision, Consequences, Alternatives
   - SHOULD include: Rationale, Implementation Notes, References
   - Use the template at `docs/adr/adr.template.md`

4. **Submit for review:**
   - Create PR with ADR file
   - Request feedback from team leads/architects
   - Update status from "Proposed" to "Accepted" after approval

5. **Update this README:**
   - Add entry to the "Files in This Directory" section
   - Link to the new ADR file

## ADR Status Transitions

```
Proposed  →  Accepted  →  Deprecated
             (Default)     (if replaced)
                           ↓
                      Superseded by ADR-X
```

- **Proposed**: Under discussion, not yet approved
- **Accepted**: Team decision is final; follow this approach
- **Deprecated**: No longer recommended; use alternative
- **Superseded**: Replaced by newer ADR; see `Superseded By`

## Using ADRs as an AI Agent

When working with Copilot:
- Reference ADRs in your requests: "Per ADR-002, use async I/O"
- Check ADRs before violating architectural decisions
- If an ADR seems wrong, propose a new ADR (don't silently violate)
- Link ADRs in code comments for complex decisions

**Example in code:**
```python
# ADR-002: Async I/O by Default
# Use async/await for database operations
async def get_user(user_id: int) -> User:
    return await db.users.get(id=user_id)
```

## Querying ADRs

Find decisions related to a topic:

**Backend architecture:**
- ADR-001: Should I build a monolith or microservices? → Monolith

**Performance & Concurrency:**
- ADR-002: Should I use async or sync I/O? → Async

**When adding new decisions:**
- Search existing ADRs first (don't duplicate)
- Update related ADRs (add cross-references)
- If new ADR contradicts old one, mark old as "Superseded"

## References

- [Michael Nygard's ADR Template](https://github.com/joelparkerhenderson/architecture-decision-record)
- [ADRs in Practice - thoughtworks.com](https://www.thoughtworks.com/radar/techniques/lightweight-architecture-decision-records)
- [ADR GitHub Repository](https://github.com/adr/adr)

## Questions?

- Missing or unclear ADR? Open an issue
- Want to propose new architecture decision? Create a PR with new ADR (Proposed status)
- Disagree with existing ADR? Discuss in team meeting and propose superseding ADR if needed

---

**Maintained By:** [Team Lead]

**Last Updated:** 2026-04-07
