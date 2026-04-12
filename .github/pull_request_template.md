# Pull Request Template

## Description

**What is this PR about?** (Brief 1-2 sentence summary)

Closes #(issue number)

### Type of Change

- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 📝 Documentation update
- [ ] ♻️ Refactoring
- [ ] 🎨 Style improvement
- [ ] ⚙️ Configuration/DevOps

---

## Development Checklist

**Did you follow TDD (Red-Green-Refactor)?**

- [ ] Red: Created failing test(s) first
- [ ] Green: Implemented code to pass test(s)
- [ ] Refactor: Improved code quality while tests still pass
- [ ] All tests passing: `pytest --cov=src --cov-fail-under=80`

**Is this spec-driven?**

- [ ] If feature-related: Code matches @docs/specs/spec.md requirements
- [ ] `docs/specs/spec.md` validation passed (all requirements met)
- [ ] No scope creep (no features beyond spec)

**Code Quality**

- [ ] Type hints on all functions: `def func(param: Type) -> ReturnType:`
- [ ] No hardcoded secrets or credentials
- [ ] No `eval()`, `exec()`, or other security anti-patterns
- [ ] Complex logic has inline comments explaining "why", not "what"
- [ ] Docstrings follow project format (Sphinx for Python)

**Security & Performance**

- [ ] All user inputs validated/sanitized
- [ ] Database queries use parameterized statements (no SQL concatenation)
- [ ] No N+1 database queries (use select_related/prefetch_related)
- [ ] Performance tested (if applicable)

**Testing**

- [ ] Test coverage: >80%
- [ ] Edge cases covered
- [ ] Error scenarios tested
- [ ] Integration tests include mocking of external services

**Documentation**

- [ ] README updated (if new features/setup instructions)
- [ ] API documentation updated (if new endpoints)
- [ ] Docstrings complete
- [ ] Related ADRs referenced (if architectural decision)

**Commit Quality**

- [ ] Commits follow [Conventional Commits](https://www.conventionalcommits.org/)
  - `feat: add email validation`
  - `fix: handle null pointer in processor`
  - `docs: update installation guide`
- [ ] Commit messages are clear (doesn't just say "fix bug")
- [ ] No debug commits (remove console.log, print(), etc.)

---

## Pre-Merge Checklist (for reviewers)

**Functionality**

- [ ] Feature works as specified
- [ ] Tests are comprehensive and passing
- [ ] No regressions in existing functionality

**Code Review**

- [ ] Code is clear and maintainable
- [ ] Naming is self-documenting
- [ ] No code duplication (DRY principle)
- [ ] Functions are single-responsibility (<25 lines preferred)

**Architecture**

- [ ] Changes align with ADRs in `docs/adr/`
- [ ] No breaking changes without migration plan
- [ ] Dependencies are necessary and justified

**Performance**

- [ ] No obvious performance regressions
- [ ] Database queries are optimized
- [ ] No memory leaks (if long-running code)

---

## Testing Instructions

**How to test this PR locally:**

```bash
# 1. Checkout this branch
git checkout <branch-name>

# 2. Install dependencies (if changed)
pip install -r requirements.txt

# 3. Run tests
pytest

# 4. Run with coverage
pytest --cov=src --cov-report=html

# 5. Manual testing steps:
# (Add any manual testing specific to this feature)
```

**Test Results**

- [ ] All unit tests passing
- [ ] All integration tests passing (if applicable)
- [ ] Linter passing: `pylint src/` (if Python)
- [ ] Type checker passing: `pyright src/` (if Python)
- [ ] Coverage threshold met: >80%

---

## Notes for Reviewers

(Add any notes that might help reviewers understand the approach or ask for specific feedback on implementation details)

---

## Related Issues

- Closes #(issue number)
- Related to #(issue number)

---

## Screenshots/Demos (if applicable)

(Include screenshots for UI changes or GIF for demos)

---

## Deployment Considerations

- [ ] Database migrations needed? (Link migration here)
- [ ] Environment variables need updating? (Document here)
- [ ] Backwards compatibility maintained? (Or migration plan documented)
- [ ] Rollback plan documented? (If high-risk change)

---

## Questions for Reviewers

(Ask specific questions you want feedback on, e.g., "Is this approach better than...?" or "Should we handle XYZ like this?")

---

**Contributor:** @username

**Estimated Review Time:** (How long should this take to review?)
