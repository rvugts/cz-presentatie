# Copilot Repository Instructions

This file provides repository-wide guidance for GitHub Copilot. These instructions apply to all Copilot interactions within this repository and complement the language/framework-specific instructions in `.github/instructions/`.

## Core Principles

All code should follow these fundamental principles:

### 1. Code Quality
- Write clean, maintainable code that's easy to understand and modify
- Use meaningful variable and function names that are self-documenting
- Keep functions and methods focused on a single responsibility
- Maintain consistent code style throughout the project
- Follow DRY (Don't Repeat Yourself) principle to avoid code duplication

### 2. Best Practices
- Follow language-specific and framework-specific best practices
- Leverage the path-specific instructions in `.github/instructions/` for detailed guidance
- Use established patterns and conventions within the industry and codebase
- Keep dependencies minimal and well-maintained
- Stay current with security and performance best practices

### 3. Security First
- Always consider security implications when writing code
- Validate and sanitize all user inputs
- Prevent common vulnerabilities: SQL injection, XSS, CSRF, etc.
- Use parameterized queries and prepared statements for databases
- Never hardcode secrets or sensitive credentials
- Implement proper authentication and authorization mechanisms
- Use HTTPS for all external communications
- Keep dependencies updated to patch security vulnerabilities

### 4. Performance Considerations
- Write efficient code that minimizes unnecessary computations
- Consider algorithmic complexity and optimize hot paths
- Implement caching where appropriate
- Optimize database queries (use indexes, avoid N+1 problems)
- Lazy-load resources when beneficial
- Profile code to identify bottlenecks before optimizing prematurely
- Consider memory usage and avoid resource leaks

### 5. Accessibility
- Ensure code supports accessibility when applicable (especially frontend code)
- Use semantic HTML and ARIA labels for web interfaces
- Provide keyboard navigation support
- Ensure sufficient color contrast for text
- Include alt text for images
- Test with screen readers when relevant
- Follow WCAG 2.1 AA standards for web applications

### 6. Specification-Driven Development (SDD)
- **Always reference @docs/specs/spec.md if it exists in the project**
- The `docs/specs/spec.md` file serves as the authoritative contract for implementation
- Before writing code, verify implementation against the specification
- If the approach contradicts the spec, follow the spec strictly
- See `docs/spec.template.md` for specification format
- Previous specs are archived in `docs/specs/` with descriptive names

### 7. Test-Driven Development (TDD)
- **Mandatory workflow:** Red → Green → Refactor
- Write test cases first, before writing implementation code
- Maintain high test coverage (aim for >80%)
- See `tests/test_example.py` for TDD patterns and fixtures
- See `.github/instructions/workflows/tdd.instructions.md` for detailed guidance

## General Guidelines

### Documentation
- Add comments for complex logic that isn't immediately obvious
- Write clear, descriptive commit messages
- Keep README.md and documentation up-to-date with code changes
- Document public APIs with appropriate docstrings/comments
- Include examples in complex module documentation

### Error Handling
- Include appropriate error handling for all operations that can fail
- Catch specific exceptions rather than broad catches
- Provide meaningful error messages to help debugging
- Log errors with sufficient context for troubleshooting
- Use proper error types/classes for different error scenarios

### Code Style
- Follow the project's existing code style and conventions
- Use consistent indentation and formatting
- Avoid overly complex nested structures
- Use language idioms and patterns (not direct translations from other languages)
- Limit line length to improve readability (typically 100 characters)

### Edge Cases & Error Scenarios
- Always consider edge cases in requirement analysis
- Handle null/undefined values appropriately
- Provide meaningful defaults when applicable
- Test boundary conditions
- Consider what happens during concurrent access
- Plan for graceful degradation when external services fail

### Specification Alignment
- When `docs/specs/spec.md` exists, it is the source of truth
- Do not implement features beyond the specification
- If implementation requires changes to the spec, document and discuss (don't just modify)
- Use `docs/specs/spec.md` to validate completeness of implementation

### Development Workflow
- Watch `docs/DEVELOPMENT.md` for complete development workflow
- See `docs/adr/` for architectural decisions
- Commit frequently with clear, descriptive messages following Conventional Commits
- Keep commits focused on single logical changes

## Language/Framework-Specific Rules

For detailed rules specific to your language or framework, see:
- `.github/instructions/python/` - Python projects
- `.github/instructions/javascript/` - JavaScript/TypeScript projects
- `.github/instructions/terraform/` - Infrastructure as Code
- `.github/instructions/workflows/` - Development workflow specifics

The specific instructions will automatically apply based on the file type you're working with.

## Specification File

When `docs/specs/spec.md` exists, it defines:
- Feature requirements and expected behavior
- Input/output specifications
- Edge cases that must be handled
- Performance requirements (if applicable)
- Security requirements for the feature

Previous specs are archived alongside it in `docs/specs/` with descriptive names.

**Always verify implementation against `docs/specs/spec.md` requirements.**

## Asking Copilot for Help

When requesting Copilot's assistance:
- Reference `docs/specs/spec.md` if your request involves feature implementation
- Mention the language/framework you're working with for optimal guidance
- Include context about the current code structure
- Specify if this is for tests or implementation
- Ask for TDD-style implementation when creating new features

## Examples

### Good Integration
```
Create a Python function to validate email addresses. 
Follow TDD - write tests first. Reference python-general.instructions.md 
and ensure the implementation aligns with @docs/specs/spec.md section 2.1.
```

### Specification Reference
```
@docs/specs/spec.md says the user authentication must support OAuth2. 
Create the implementation following this spec and python-django.instructions.md.
```

### Workflow
```
Write a failing test first for the payment processing feature (Red phase).
Then implement the minimal code to pass the test (Green phase).
Finally, refactor for better structure (Refactor phase).
```

## Questions or Clarifications

If implementation conflicts with this guidance:
1. Check the specific language instructions in `.github/instructions/`
2. Review `docs/specs/spec.md` if it exists
3. Verify against the core principles above
4. When in doubt, prioritize: **Spec > Security > Best Practices > Style**
