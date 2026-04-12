---
applyTo: "**/*.py"
---
# Test-Driven Development (TDD) Workflow

You are enforcing a strict Test-Driven Development (TDD) workflow. This is a workflow-based instruction that applies alongside language-specific instructions.

## TDD Workflow

Always follow this workflow when implementing features:

### 1. Red Phase
- Write a failing test **first** before any implementation.
- The test should define the expected behavior clearly.
- Run the test to confirm it fails.

### 2. Green Phase
- Write the **minimum code** needed to make the test pass.
- Focus on functionality, not optimization.
- Run the test to confirm it passes.

### 3. Refactor Phase
- Improve code quality while keeping tests passing.
- Refactor for clarity, efficiency, and maintainability.
- Run tests frequently to ensure nothing breaks.

## Test Structure

- **Naming:** Test functions should clearly describe what they test (e.g., `test_calculate_total_with_empty_cart_returns_zero`)
- **Arrange-Act-Assert:** Organize tests with clear AAA pattern:
  - **Arrange:** Set up test data and conditions
  - **Act:** Call the function being tested
  - **Assert:** Verify the results
- **One Assertion Per Test:** Each test should verify one behavior (use subtests for related assertions).
- **Isolation:** Each test should be independent and not rely on other tests.
- **Fixtures:** Use fixtures to share common setup across tests.

## Testing Tools

- **Framework:** Use `pytest` for Python testing.
- **Mocking:** Use `unittest.mock` or `pytest-mock` for mocking dependencies.
- **Assertions:** Use pytest's simple assertion syntax.
- **Parametrization:** Use `@pytest.mark.parametrize` for testing multiple scenarios.
- **Fixtures:** Use `conftest.py` for shared fixtures.

## Best Practices

- **No Test Skipping:** Avoid `@pytest.mark.skip` or `@unittest.skip` in production code.
- **No Test Duplication:** Use parameters and fixtures to reduce duplication.
- **Test Coverage:** Aim for high code coverage (>80%). Use `pytest-cov` to measure.
- **Integration Tests:** In addition to unit tests, write integration tests for critical paths.
- **Performance Tests:** Write performance tests for time-sensitive operations.

## Continuous Integration

- **Pre-commit Hooks:** Run tests before committing code.
- **CI Pipeline:** Integrate tests into CI/CD pipeline.
- **Coverage Reporting:** Report test coverage in CI pipeline.
- **Failure Prevention:** Ensure tests must pass before merging pull requests.