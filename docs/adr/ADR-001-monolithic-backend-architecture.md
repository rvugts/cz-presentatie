# ADR-001: Monolithic Backend Architecture

**Status:** Accepted

**Date:** 2026-04-07

**Deciders:** [Team Lead, Architect]

**Technical Story:** [Link to issue/ticket if applicable]

---

## Context

**Problem Statement:**

This project requires a scalable, maintainable backend that serves a small team with diverse requirements. The options are deciding between:
- Monolithic architecture (single codebase, all services together)
- Microservices architecture (separate services per domain)
- Hybrid approach (modular monolith)

**Background:**

- Team size: 2-5 engineers
- Expected users: <100K initially
- Development speed is critical (MVP in 3 months)
- Operational complexity should be minimized (small DevOps team)
- Future scaling is uncertain

**Assumptions:**

- Most endpoints will be I/O bound (database queries, external APIs)
- Database is shared across all features initially
- Single cloud region is sufficient for v1
- CI/CD pipeline is mature (automated testing, deployment)

---

## Decision

**We will build a monolithic backend using FastAPI/Python with modular organization.**

Key components:
- Single FastAPI application serving all APIs
- Organized by feature within the application (app/routers/, app/services/)
- Shared database (PostgreSQL)
- Single deployment unit
- Modular structure within monolith for future extraction if needed

---

## Rationale

**Why this approach:**

1. **Development Speed:** Single codebase reduces context switching and onboarding time. Team can move quickly without inter-service coordination.

2. **Operational Simplicity:** One application, one database connection pool, one deployment. Easier to debug, monitor, and maintain with small team.

3. **Data Consistency:** Single database eliminates distributed transaction challenges and simplifies ACID compliance.

4. **Cost Efficiency:** Lower infrastructure costs (single container, single database). No service discovery, load balancing, or inter-service communication overhead.

5. **Modularity for Future:** Code is organized by feature/module. If microservices becomes necessary later, we can extract modules into separate services.

**Alignment with Project Principles:**

- **Deterministic Core:** Single deployment means consistent behavior. No coordination failures between services.
- **Operational Rigor:** Smaller operational surface area = fewer things to fail or mismanage.
- **Development Velocity:** Clear decision removes architectural debate. Team focuses on features, not infrastructure.

---

## Consequences

### Positive Consequences

- ✅ **Faster time-to-market:** Features can be shipped without waiting for service coordination
- ✅ **Easier debugging:** Single execution context, complete stack traces, no network latency issues to debug
- ✅ **Simple deployment:** One artifact deployed to production
- ✅ **Code reuse:** Shared services, utilities, models across features
- ✅ **Transactional integrity:** Atomic operations across features
- ✅ **Lower infrastructure cost:** Single container, single database

### Negative Consequences / Trade-offs

- ⚠️ **Scaling limits:** All features scaled together (can't scale just one feature)
- ⚠️ **Technology lock-in:** One tech stack (Python/FastAPI) for all features
- ⚠️ **Deployment risk:** Bug in one feature can impact entire system
- ⚠️ **Single point of failure:** One deployment unit means one place everything can break

### Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Monolith becomes too large** | Medium | High | Enforce modular organization. Maximum 1000 lines per module. Use feature flags for feature isolation. Plan extraction if service grows beyond 50K lines. |
| **Performance bottleneck** | Low | High | Async I/O by default (ADR-002). Database indexing and query optimization. Load testing before scale. |
| **One bug crashes entire system** | Medium | High | Test coverage >80%. Type hints (Python) catch bugs at development time. Staging environment mirrors production. Gradual rollout (canary deployment). |
| **Coordination delays if team grows** | Low | Medium | Plan modular extraction into microservices if team >5. Document APIs clearly. Code reviews enforce quality. |

---

## Alternatives Considered

### Alternative 1: Microservices Architecture

**Description:** Separate services per domain (users, posts, messaging, etc.) with service discovery, inter-service communication.

**Pros:**
- Independent scaling per service
- Technology diversity (different languages per service)
- Independent deployment and updates
- Fault isolation (one service down doesn't crash others)

**Cons:**
- Significantly higher operational complexity (Docker, Kubernetes, service mesh)
- Distributed tracing and debugging is harder
- Network latency between services
- Distributed transaction challenges (eventual consistency)
- Higher infrastructure cost
- Requires larger DevOps/platform team

**Why rejected:** 
Team is too small to manage microservices operationally. The operational burden outweighs the benefits. At our scale, a monolith is 10x simpler.

### Alternative 2: Hybrid Modular Monolith

**Description:** Single backend with explicitly modular structure and clear boundaries (inspired by domain-driven design). Services are logical, not physical.

**Pros:**
- All benefits of monolith (simple deployment, data consistency)
- Modularity for future extraction
- Clean boundaries between features
- Easier path to microservices if needed

**Cons:**
- Still limited by single process (can't scale one module independently)
- Module boundaries are not enforced by technology (requires discipline)
- No isolation if one module has a memory leak

**Why not selected as primary:** 
This is actually what we're doing (monolith with modular organization). Listed separately to clarify we considered it explicitly. The name "monolithic" can be misleading—we're building it modular from day one.

---

## Implementation Notes

**Technical Requirements:**

- Python 3.10+
- FastAPI web framework
- PostgreSQL database
- Async I/O by default (see ADR-002)
- Feature isolation using FastAPI routers (app/routers/)
- Service layer organization (app/services/)

**Dependencies:**

- Requires ADR-002 (Async by Default) for performance
- Requires Python type hints (enforced by pyright/mypy)
- Requires test coverage >80%

**Migration Path:**

N/A (this is the initial architecture decision for new project)

**If microservices becomes needed later:**

1. Identify service to extract (e.g., messaging service)
2. Define external API (REST, gRPC, or event-based)
3. Create separate repository and deployment
4. Implement client in monolith that calls extracted service
5. Gradually migrate logic from monolith to service
6. Repeat for next service

**Verification:**

- ✓ Single artifact deployed to production
- ✓ Database is shared (no per-service databases)
- ✓ Code organized by feature (app/routers/user.py, app/services/user.py)
- ✓ No hardcoded service endpoints (configurable via environment)

---

## References

- [Monolithic vs Microservices - Martin Fowler](https://martinfowler.com/articles/microservices.html)
- [Modular Monolith - Simon Brown](https://www.codingthearchitecture.com/2014/11/19/what_is_the_definition_of_a_monolith.html)
- [FastAPI Architecture - FastAPI Documentation](https://fastapi.tiangolo.com/)
- Related ADRs: [ADR-002: Async by Default](./ADR-002-async-io-by-default.md)

---

## Notes

**Review Date:** 2026-10-07 (6-month review recommended)

**Supersedes:** N/A

**Superseded By:** (If this decision is replaced in future)

---

**Document History:**

- 2026-04-07: Initial draft
- 2026-04-07: Accepted by team leads
