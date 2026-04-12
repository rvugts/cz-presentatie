# ADR-002: Async I/O by Default

**Status:** Accepted

**Date:** 2026-04-07

**Deciders:** [Team Lead, Backend Architect]

**Technical Story:** [Link to issue/ticket if applicable]

---

## Context

**Problem Statement:**

The backend needs to handle I/O operations (database queries, external API calls, file I/O) efficiently. The choice is between:
- Synchronous (blocking) I/O - simple but wastes threads
- Asynchronous (non-blocking) I/O - complex but efficient
- Hybrid (async for I/O, sync for CPU-bound) - flexible

**Background:**

- Most endpoints are I/O bound (database, external services)
- Using FastAPI which has excellent async support via ASGI
- Team is comfortable with Python async/await syntax
- Performance is critical (must handle 1000+ concurrent users)

**Assumptions:**

- Async libraries are available for all I/O operations (databases, HTTP clients)
- Team has async/await experience
- Blocking operations are rare and can be explicitly managed

---

## Decision

**We will use async I/O by default for all I/O operations.**

Key components:
- All API endpoints are `async def`
- All database queries use async drivers (asyncpg, tortoise-orm, sqlalchemy async)
- All external HTTP calls use async clients (httpx, aiohttp)
- File I/O uses async libraries where applicable
- CPU-bound operations use sync (no async overhead needed)

---

## Rationale

**Why this approach:**

1. **Resource Efficiency:** Async allows single thread to handle 1000+ concurrent connections. Sync would require 1000+ threads (expensive).

2. **Scalability:** Single container can handle higher throughput without increasing resources (CPU, memory).

3. **Performance:** I/O operations don't block other requests. While one request waits for database, others execute concurrently.

4. **FastAPI Native:** FastAPI is built on top of Starlette (ASGI). Async is first-class, not a bolt-on.

5. **Team Skill:** Python async/await is well understood by modern developers and widely used.

**Alignment with Project Principles:**

- **Operational Rigor:** Async enables us to handle production scale with minimal infrastructure.
- **Performance:** Non-blocking I/O ensures consistent response times under load.
- **Deterministic Core:** Async behavior is predictable (single event loop); no race conditions from thread interleaving like sync threading.

---

## Consequences

### Positive Consequences

- ✅ **High concurrency:** Single process handles 1000+ concurrent requests
- ✅ **Efficient resource use:** No thread pool exhaust issues
- ✅ **Better response times:** I/O doesn't block unrelated requests
- ✅ **Simpler scaling:** One container = enough for MVP; no load balancer needed yet
- ✅ **Reduced infrastructure cost:** Fewer containers, simpler deployment
- ✅ **Native to FastAPI:** Full framework support, excellent tooling

### Negative Consequences / Trade-offs

- ⚠️ **Learning curve:** Async is harder than sync (callback hell, exception handling)
- ⚠️ **All or nothing:** Mixing sync and async requires careful management
- ⚠️ **CPU-bound code is slower:** Async has overhead; CPU operations are slower than sync
- ⚠️ **Debugging is harder:** Stack traces don't show full call chain; coroutine context is harder to follow

### Risks & Mitigation

| Risk | Likelihood | Impact | Mitigation Strategy |
|------|------------|--------|---------------------|
| **Accidentally blocking the event loop** | Medium | High | Code review enforces async patterns. Don't call blocking functions (time.sleep, requests.get) in async code. Use asyncio.sleep() instead. |
| **CPU-bound code runs slower** | Low | Medium | CPU operations must be intentional. If needed, use executor.run_in_executor() to offload to thread pool. Rare for web API work. |
| **Coroutine not awaited warning** | Low | Medium | IDE and linter catch these. Enable strict async checking (pylint, pyright). |
| **Context management complexity** | Low | Low | Use async context managers (async with) consistently. Patterns are well established. |

---

## Alternatives Considered

### Alternative 1: Sync I/O (Blocking)

**Description:** Traditional request-per-thread model. Each HTTP request gets its own thread.

**Pros:**
- Simpler to understand and debug
- No async/await complexity
- Existing sync libraries work directly (requests, psycopg2)

**Cons:**
- Thread per request = high resource usage (memory, context switching)
- Can't handle 1000+ concurrent users without 1000+ threads
- Thread exhaustion under load = requests queue up
- Much higher infrastructure cost for same throughput

**Why rejected:**
Sync would require 100+ containers to handle production load. Async handles it in 1-2 containers. Cost and complexity of sync scale is prohibitive.

### Alternative 2: Hybrid (Mixed Async/Sync)

**Description:** Async for I/O, sync for CPU-bound, with careful boundaries between them.

**Pros:**
- Use sync libraries where they're simpler
- Avoid async overhead for CPU work
- Flexibility

**Cons:**
- Much harder to manage (when to switch between async/sync?)
- Risk of blocking event loop if boundaries aren't respected
- Debugging is harder (mixing paradigms)
- Still requires async knowledge

**Why not selected:**
Requiring developers to decide "should this be async or sync?" on every function is complexity. Decision to default to async is clearer and simpler.

---

## Implementation Notes

**Technical Requirements:**

- Python 3.10+ with full async support
- FastAPI for API framework
- Async database driver (asyncpg for PostgreSQL, or sqlalchemy async mode)
- Async HTTP client (httpx, aiohttp)
- All I/O operations must be awaited

**Dependencies:**

- Requires ADR-001 (Monolithic Architecture) for simplicity
- Requires type hints (to catch async mismatches)
- Requires strict linting (pylint, pyright in strict mode)

**Patterns to Follow:**

```python
# ✅ GOOD: Async endpoint, async I/O
@app.post("/users")
async def create_user(user: UserCreate) -> User:
    """Create new user - async endpoint with async database."""
    user_data = await db.users.insert({...})  # Awaited!
    return user_data

# ✅ GOOD: Async endpoint, async external API call
@app.get("/external-data")
async def get_external_data() -> dict:
    """Fetch from external API - async client."""
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/data")
    return response.json()

# ❌ BAD: Blocking I/O in async endpoint
@app.post("/users")
async def create_user(user: UserCreate) -> User:
    """DON'T DO THIS - BLOCKS EVENT LOOP!"""
    import time
    time.sleep(5)  # ❌ BLOCKS EVERYTHING
    return user

# ❌ BAD: Sync I/O in async endpoint
@app.get("/external-data")
async def get_external_data() -> dict:
    """DON'T DO THIS - BLOCKS EVENT LOOP!"""
    import requests
    response = requests.get("https://api.example.com/data")  # ❌ Sync, blocks
    return response.json()

# ✅ GOOD: If you must use sync, offload to executor
@app.get("/cpu-work")
async def cpu_work() -> dict:
    """CPU-bound work - run in executor to not block event loop."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, expensive_cpu_function)
    return {"result": result}
```

**Code Review Checklist:**

- [ ] All I/O operations are awaited
- [ ] No `import time` with `time.sleep()` in async code
- [ ] No sync requests library (use httpx with async)
- [ ] Database calls use async driver
- [ ] External API calls use async client
- [ ] Dependencies are async-compatible

**Verification:**

- ✓ All endpoint handlers are `async def`
- ✓ All database queries are awaited
- ✓ All HTTP calls use async client with `await`
- ✓ Linter reports no unawaited coroutines
- ✓ Load test verifies 1000+ concurrent connections

---

## References

- [Python asyncio Documentation](https://docs.python.org/3/library/asyncio.html)
- [FastAPI Async Support](https://fastapi.tiangolo.com/async/)
- [async/await Syntax](https://docs.python.org/3/library/asyncio-task.html)
- [Asyncpg - PostgreSQL Driver](https://magicstack.github.io/asyncpg/)
- [HTTPX - Async HTTP Client](https://www.python-httpx.org/)
- Related ADRs: [ADR-001: Monolithic Architecture](./ADR-001-monolithic-backend-architecture.md)

---

## Notes

**Review Date:** 2026-10-07 (6-month review recommended)

**Supersedes:** N/A

**Superseded By:** (If this decision is replaced in future)

---

**Document History:**

- 2026-04-07: Initial draft
- 2026-04-07: Accepted by team
