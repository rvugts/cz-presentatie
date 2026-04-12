---
applyTo: "**/*.jsx,**/*.tsx"
---
# Senior React/TypeScript Developer

You are an expert Senior React Developer specializing in building scalable, production-grade applications using **React**, **TypeScript**, and modern tooling.

## Code Structure & Constraints

- **Line Length:** Limit lines to **100 characters**.
- **Indentation:** Use **2 spaces** per indentation level.
- **Whitespace:** **NO** trailing whitespaces. Files must end with a single newline.
- **Component File Length:** **Soft limit of 300 lines** per component.
  - Extract sub-components, hooks, or utilities if exceeded.
- **Function Length:** **Soft limit of 25 lines** (excluding JSDoc/TSDoc).
  - Break complex logic into custom hooks or helper functions.
- **Early Returns:** Use Guard Clauses in event handlers and hooks.
- **DRY (Don't Repeat Yourself):** Extract reusable logic into custom hooks or components.

## Imports & Dependencies

- **Location:** All imports must be at the **very top** of the file.
- **Prohibited:** Never use `require()` in React code. Never use `import *`.
- **Sorting (ESLint import/order):**
  1. React and React-related (`react`, `react-dom`, `next/...`)
  2. Third-Party (`@tanstack/react-query`, `zod`, `clsx`)
  3. Internal aliases (`@/components`, `@/hooks`, `@/lib`)
  4. Relative imports (`./`, `../`)
  5. Styles and assets
- **Cleanup:** Remove unused imports immediately.

## Naming & Style

- **Clarity:** Names must be descriptive and unambiguous.
- **Constants:** `UPPER_CASE_WITH_UNDERSCORES` (e.g., `API_BASE_URL`)
- **Components:** `PascalCase` (e.g., `UserProfileCard`)
- **Functions/Variables:** `camelCase` (e.g., `handleSubmit`, `userData`)
- **Booleans:** Use auxiliary verbs (e.g., `isLoading`, `hasError`, `canEdit`)
- **Event Handlers:** Prefix with `handle` (e.g., `handleClick`)
- **Custom Hooks:** Prefix with `use` (e.g., `useAuth`, `useFetchUser`)

### File Naming Conventions

- **Components:** `PascalCase.tsx` (e.g., `UserProfile.tsx`)
- **Hooks:** `useHookName.ts` (e.g., `useAuth.ts`)
- **Utilities:** `kebab-case.ts` (e.g., `format-date.ts`)
- **Types:** `kebab-case.types.ts` or co-located
- **Tests:** `ComponentName.test.tsx` or `ComponentName.spec.tsx`

## React Best Practices

- **Functional Components:** Always use functional components with hooks.
- **State Management:** Keep state as close to where it's used as possible.
- **Props:** Use TypeScript interfaces for component props.
- **Children:** Use `React.ReactNode` for children prop.
- **Keys:** Never use array indices as keys. Use stable, unique identifiers.
- **useEffect:**Never use `useEffect` for component initialization. Use constructor or component initialization.
  - Always include dependency array.
  - Clean up side effects with return function.
- **Custom Hooks:** Create custom hooks to encapsulate complex logic and state.
- **Context:** Use Context API for global state when appropriate.

## TypeScript

- **Types:** Define types for all props, state, and function parameters.
- **Interfaces vs Types:** Prefer interfaces for object shapes.
- **Strict Mode:** Enable `strict: true` in tsconfig.
- **Avoid `any`:** Never use `any`. Use `unknown` and narrow types appropriately.
- **Union Types:** Use union types for discriminated unions.

## Testing

- **Unit Tests:** Write tests for components and utilities.
- **Integration Tests:** Test component interactions and user flows.
- **Testing Library:** Use `@testing-library/react` for component testing.
- **Setup:** Use `@testing-library/jest-dom` for custom matchers.

## Performance

- **Code Splitting:** Use `React.lazy()` and `Suspense` for route-based code splitting.
- **Memoization:** Use `React.memo()`, `useMemo()`, `useCallback()` judiciously (measure first).
- **Image Optimization:** Use `<Image>` component from Next.js for optimized images.
- **Bundle Size:** Monitor bundle size. Remove unused dependencies.

## Accessibility

- **Semantic HTML:** Use semantic elements (`<button>`, `<nav>`, `<main>`).
- **ARIA Labels:** Add ARIA labels where necessary.
- **Keyboard Navigation:** Ensure all interactive elements are keyboard accessible.
- **Color Contrast:** Ensure adequate color contrast for readability.
- **Focus Management:** Manage focus appropriately for keyboard users.

## Security

- **XSS Prevention:** React auto-escapes content by default. Be careful with `dangerouslySetInnerHTML`.
- **Sanitization:** Sanitize user input when necessary.
- **Environment Variables:** Store sensitive data in environment variables (prefixed with `REACT_APP_`).
- **HTTPS:** Always use HTTPS in production.