---
name: refactor-python
description: Refactor Python code applying sound engineering practices, DRY, and security without altering functionality. Use when refactoring Python files or when the user invokes /refactor-python.
---

# Refactor Python Guidelines

You are an expert Python Engineer focused on sound engineering practices, maintainability, and "vibe coding" aesthetics. Your goal is to refactor the provided code to meet professional standards without changing its external behavior.

## 1. Code Structure & Constraints
- **Line Length:** Limit lines to **100 characters** where possible to ensure readability on standard screens.
- **Whitespace:** Strict adherence to **no trailing whitespace** on any line.
- **Module Length:** Strict limit of **1000 lines**. If a module exceeds this, propose splitting it into logical sub-modules.
- **Function Length:** Strong suggestion (soft limit) of **25 lines** (excluding docstrings and comments).
    - Aim to break down complex functions into smaller, single-purpose helper functions.
    - **Exception:** Longer functions are permitted only if the logic is irreducible and splitting it would harm readability.
- **Early Exits:** Use "Guard Clauses" to return early from functions. Avoid deep nesting of `if/else` blocks.
- **DRY (Don't Repeat Yourself):** Aggressively remove duplicate logic.
    - Use **Decorators** for repetitive tasks (e.g., logging, timing, validation, error handling).
    - Extract shared logic into utility functions or base classes.

## 2. Imports & Dependencies
- **Organization:** All imports must be at the **very top** of the file. Never place imports inside functions or classes, unless needed to avoid cyclic dependencies—such imports must be documented (e.g. in a comment or docstring).
- **Cleanup:** Remove all unused imports immediately.
- **Sorting:** Group imports by standard library, third-party, and local application (following PEP 8/isort standards).
- **No Wildcards:** Never use `from module import *`. Explicitly import what is needed.

## 3. Naming & Style
- **Clarity:** Use descriptive, unambiguous names for all variables, functions, and classes.
- **Constants:** Use **UPPER_CASE_WITH_UNDERSCORES** for constants. Define them at module level, or at class level for class-specific constants.
- **Class Names:** PascalCase.
- **Function/Variable Names:** SnakeCase (`snake_case`).
- **Type Hints:** Add Python type hints to **all** function signatures (arguments and return types) to improve code comprehension and reduce bugs. Use `Optional`, `Union`, or generics when they simplify signatures.

## 4. Documentation (Docstrings)
- **Style:** Use **Sphinx/reStructuredText** format for all docstrings (e.g., `:param`, `:return:`). Omit `:rtype` and `:type` when type hints are present on the function signature.
- **Module Docstring:**
    - Must explain the purpose of the file.
    - **Requirement:** Must include a list of major dependencies used in the module. **Exception**: __init__.py files
- **Class/Function Docstrings:** Mandatory for every class and public function. Explain purpose, arguments, and return values clearly. Skip the type of arguments. For non-public methods explain the purpose.

## 5. Refactoring & Performance
- **Functional Style:** Prefer **List/Dict/Set Comprehensions** over `for` loops for transformations.
- **Built-ins:** Use `map()`, `filter()`, and `reduce()` where they offer cleaner, more efficient alternatives.
- **Performance:** Optimize for time and space complexity where obviously beneficial; avoid micro-optimization that harms readability.
- **Error handling:** Use specific exception types; avoid bare `except:`. Prefer context managers for resource cleanup. Document exceptions that callers should handle.
- **Safety & Security:**
    - **SQL Injection:** When interacting with databases, **ALWAYS** use parameterized queries. Never concatenate strings to build SQL commands.
    - **Code Injection:** Ensure no usage of `eval()`, `exec()`, or unsafe YAML loading. Sanitize inputs where applicable.

## 6. Verification
- **No Functionality Change (non-negotiable):** The refactor must be purely structural and stylistic. The logic must remain identical. Security rules are also non-negotiable; style limits (e.g. line length) are soft where stated.
- **Tests:** If tests exist (pytest/unittest), you **must** request to run them after refactoring to confirm nothing is broken. If no tests exist, suggest creating a basic test case for the refactored critical path.

## 7. Execution
- [ ] **Do not change behavior.** Preserve logic and external behavior throughout.
- [ ] Analyze the code for violations of the above rules.
- [ ] Refactor step-by-step.
- [ ] Verify adherence to the soft limit of 25 lines per function and strict 1000 lines per module.
- [ ] Output the final cleaned code.
- [ ] Run pylint and resolve linter errors. You may ignore "too many arguments" errors. If a specific check cannot be resolved, disable that check locally (e.g. with an inline comment), not the linter globally.

## 8. Subagent use
For large or multi-file refactors, consider dispatching a subagent with this skill and the target scope so refactoring runs in an isolated context. Pass the target files or modules and this skill's content as the subagent instructions.

## 9. Async code
When refactoring async code: use `async`/`await` consistently; name async functions and methods so that async nature is clear (e.g. `fetch_user_async` or conventional names); prefer `asyncio` primitives over raw callbacks where appropriate.