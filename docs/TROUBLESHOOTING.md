# Troubleshooting Guide

Common issues when working with this repository and how to resolve them.

## Copilot Issues

### Copilot Suggests Non-Async Code in Async Context

**Problem:** Copilot suggests sync patterns (e.g., `import time; time.sleep(5)`) in async functions.

**Root Cause:** ADR-002 states all I/O must be async, but Copilot may not know this context.

**Solution:**
1. Add comment: `# Must use async/await per ADR-002`
2. Reference the ADR: "See ADR-002: Async by Default"
3. Use explicit prompt: "Write this using async/await per ADR-002"

**Example - Before:**
```python
@app.post("/process")
async def process_data():
    import time
    time.sleep(5)  # ❌ Blocks event loop
```

**Example - After:**
```python
@app.post("/process")
async def process_data():
    # Must use async/await per ADR-002 (Async by Default)
    await asyncio.sleep(5)  # ✅ Non-blocking
```

---

### Copilot Writes Code Without Tests

**Problem:** Copilot generates implementation code without writing tests first.

**Root Cause:** TDD isn't enforced in the request.

**Solution:**
1. Always start with: "Write a failing test first (TDD Red phase)"
2. Reference: `.github/instructions/workflows/tdd.instructions.md`
3. Example test in `tests/test_example.py`

**Correct Request Format:**
```
Write a failing test first for user email validation (Red phase).
Then implement minimal code to pass (Green phase).
Finally refactor for quality (Refactor phase).
Follow TDD pattern in .github/instructions/workflows/tdd.instructions.md
```

---

### Copilot Ignores Project Specifications

**Problem:** Copilot implements features that don't match @docs/specs/spec.md.

**Root Cause:** Spec not referenced in the request.

**Solution:**
1. Always reference @docs/specs/spec.md: "Implement per @docs/specs/spec.md section 2.1"
2. Paste spec requirements if not obvious
3. Ask Copilot to validate: "Verify this implementation matches @docs/specs/spec.md requirements exactly"

**Correct Request Format:**
```
Create user authentication per @docs/specs/spec.md section 2.1.
Requirements:
1. Support email/password login
2. Return JWT token (not cookies)
3. Sessions expire in 24 hours
```

---

### Instructions Not Being Applied

**Problem:** Language-specific instructions (e.g., `python-general.instructions.md`) aren't showing in Copilot Chat.

**Root Cause:** File not detected by Copilot.

**Solution:**
1. Verify file exists: `.github/instructions/python/python-general.instructions.md`
2. Check `applyTo` pattern matches your file: `applyTo: "**/*.py"`
3. Reload VS Code: `Cmd+Shift+P` → "Developer: Reload Window"
4. Wait up to 1 minute for changes to propagate
5. Attach file to chat: Right-click file → "Attach to Chat"

---

## Testing Issues

### Tests Not Running / Import Errors

**Problem:** `pytest` fails with import errors.

**Solution:**
1. Verify `tests/conftest.py` exists (pytest looks for this)
2. Check `tests/` directory is in PYTHONPATH:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   pytest
   ```
3. Verify dependencies installed:
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov pytest-mock
   ```

---

### Test Coverage Below 80%

**Problem:** Coverage report shows <80% (builds fail due to this).

**Solution:**
1. Check coverage report:
   ```bash
   pytest --cov=src --cov-report=html
   open htmlcov/index.html
   ```
2. Add tests for uncovered lines (show in red)
3. Use fixtures from `tests/conftest.py` to reduce duplication

---

### Tests Failing After Refactoring

**Problem:** Tests break after refactoring code.

**Root Cause:** Tests are tightly coupled to implementation (not testing behavior).

**Solution:**
1. Verify tests test *behavior*, not *implementation*
2. Example - Bad test (too specific):
   ```python
   def test_user_service():
       service = UserService()
       assert service._data == {}  # Testing internals ❌
   ```
3. Example - Good test (behavior):
   ```python
   def test_user_create():
       service = UserService()
       user = service.create("user@example.com")
       assert user.email == "user@example.com"  # Testing behavior ✅
   ```

---

## Code Quality Issues

### Type Checker (Pyright) Complaining

**Problem:** `pyright` reports type errors.

**Solution:**
1. Add type hints:
   ```python
   # ❌ BEFORE
   def process(data):
       return data
   
   # ✅ AFTER
   from typing import List, Dict, Any
   
   def process(data: List[Dict[str, Any]]) -> bool:
       return len(data) > 0
   ```
2. Run type checker: `pyright src/`
3. Fix errors or add `# pyright: ignore` if false positive

---

### Linter (Pylint) Complaints

**Problem:** `pylint` reports style or logic issues.

**Solution:**
1. Run linter: `pylint src/`
2. Fix issues:
   - Unused imports: Remove them
   - Line too long: Break into multiple lines (max 100 chars)
   - Missing docstring: Add docstring (Sphinx format)
3. Ignore specific issues (if false positive):
   ```python
   x = 5  # pylint: disable=unused-variable
   ```

---

### Black Formatter Conflicts

**Problem:** Black (auto-formatter) reformats code unexpectedly.

**Solution:**
1. Black is opinionated and that's okay! Let it reformat.
2. Configure in `pyproject.toml` if needed:
   ```toml
   [tool.black]
   line-length = 100
   ```
3. Run before committing: `black src/`

---

## Async/Await Issues

### "Coroutine Was Never Awaited" Warning

**Problem:** Python warning: "coroutine 'function_name' was never awaited"

**Root Cause:** Forgot to `await` an async function call.

**Solution:**
1. Find the line mentioned in warning
2. Add `await`:
   ```python
   # ❌ BEFORE
   result = async_function()  # Returns coroutine, not value
   
   # ✅ AFTER
   result = await async_function()  # Actually runs async function
   ```

---

### "Event Loop is Closed" Error

**Problem:** `RuntimeError: Event loop is closed`

**Root Cause:** Mixing sync and async code incorrectly.

**Solution:**
1. Ensure `async def` endpoints in FastAPI:
   ```python
   # ✅ GOOD
   @app.get("/data")
   async def get_data():
       result = await db.query()
       return result
   ```
2. For testing, use `pytest-asyncio`:
   ```bash
   pip install pytest-asyncio
   ```
3. Mark async tests:
   ```python
   @pytest.mark.asyncio
   async def test_async_function():
       result = await my_async_function()
       assert result is not None
   ```

---

## Database Issues

### "Connection Pool Exhausted" Under Load

**Problem:** Database connections run out under concurrent requests.

**Root Cause:** Connections not released (missing `await`, blocking I/O).

**Solution:**
1. Ensure all database operations are awaited:
   ```python
   # ✅ GOOD
   user = await db.users.get(id=123)
   ```
2. Use connection pooling (FastAPI handles this if using async driver)
3. Check ADR-002: All I/O must be async

---

### SQL Injection Risk

**Problem:** Security concern: String interpolation in SQL.

**Root Cause:** Concatenating user input into SQL strings.

**Solution:**
1. Always use parameterized queries:
   ```python
   # ❌ BAD - SQL INJECTION RISK
   query = f"SELECT * FROM users WHERE email = '{email}'"
   
   # ✅ GOOD - Safe
   user = await db.query("SELECT * FROM users WHERE email = ?", (email,))
   
   # ✅ GOOD - ORM (safest)
   user = await db.users.filter(email=email).first()
   ```

---

## Git / Commit Issues

### Commit Rejected: Test Coverage Below 80%

**Problem:** Pre-commit hook fails: "Tests must pass with 80% coverage"

**Solution:**
1. Run tests with coverage:
   ```bash
   pytest --cov=src --cov-fail-under=80
   ```
2. If fails, add tests:
   ```bash
   pytest --cov=src --cov-report=html
   open htmlcov/index.html  # See what's uncovered
   ```
3. Try commit again after fixing

---

### Unclear Commit Messages

**Problem:** PR rejected due to poor commit messages.

**Root Cause:** Commit message doesn't follow Conventional Commits.

**Solution:**
Use format: `<type>: <description>`

**Valid types:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `refactor:` - Code refactoring (no behavior change)
- `test:` - Adding tests
- `perf:` - Performance improvement
- `chore:` - Build/deps/config

**Examples:**
```bash
git commit -m "feat: add email validation endpoint"
git commit -m "fix: handle null pointer in data processing"
git commit -m "docs: update API documentation"
git commit -m "refactor: extract email validation into utility"
git commit -m "test: add edge case tests for email validation"
```

---

## Architecture Decision Issues

### "Should I violate ADR-001/002?"

**Problem:** Want to make architectural decision that contradicts existing ADRs.

**Solution:**
1. Check if ADR-001 or ADR-002 applies (see `docs/adr/`)
2. If must violate:
   - **Create new ADR** explaining why (via `docs/adr/ADR-XXX.md`)
   - **Mark old ADR as superseded** (update header: `Superseded By: ADR-XXX`)
   - **Review with team** before implementing
3. Never silently violate architectural decisions

---

### "Can I use sync code?"

**Problem:** Async is hard, sync is easier.

**Root Cause:** ADR-002 (in `docs/adr/`) requires async by default.

**Solution:**
1. If I/O operation: **Must be async** (per ADR-002)
2. If CPU-bound: Okay to use sync, but consider:
   ```python
   # Use executor to not block event loop
   loop = asyncio.get_event_loop()
   result = await loop.run_in_executor(None, cpu_heavy_function)
   ```
3. If truly necessary sync: Document why (add comment with justification)

---

## Getting Help

**Still stuck?**

1. Check `docs/DEVELOPMENT.md` (development workflow)
2. Check `.github/instructions/` (language-specific guidance)
3. Check `docs/adr/` (architectural decisions)
4. Review `tests/test_example.py` (testing patterns)
5. Check `docs/spec.template.md` (specification format)
6. Search GitHub issues for similar problem
7. Ask team lead or open an issue with reproduction steps

---

## Contributing to This Guide

Found a new issue? Add it here!

1. Add section under appropriate heading
2. Follow format: Problem → Root Cause → Solution
3. Include code examples
4. Reference relevant documents (ADRs, instructions)
5. Submit PR

---

**Last Updated:** 2026-04-07

**Maintained By:** [Team Lead]
