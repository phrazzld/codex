# DEVELOPMENT PHILOSOPHY - APPENDIX FRONTEND

## Introduction

This document specifies the frontend-specific standards, architecture patterns, tooling requirements, and best practices required for our React/Next.js projects. It serves as a mandatory extension to the main **Development Philosophy (v3)** document. All frontend code written for our projects **MUST** adhere to the guidelines herein, in addition to the core philosophy.

**Reference:** Always refer back to the main [Development Philosophy](DEVELOPMENT_PHILOSOPHY.md) for overarching principles.

## Table of Contents

- [1. Component Architecture (Atomic Design)](#1-component-architecture-atomic-design)
- [2. Component Development Workflow (Storybook-First)](#2-component-development-workflow-storybook-first)
- [3. UI Library and Styling (shadcn/ui, Tailwind)](#3-ui-library-and-styling-shadcnui-tailwind)
- [4. Testing Strategy (Component, Integration, E2E)](#4-testing-strategy-component-integration-e2e)
- [5. State Management](#5-state-management)
- [6. Performance Optimization](#6-performance-optimization)
- [7. Accessibility (a11y)](#7-accessibility-a11y)
- [8. Responsive Design](#8-responsive-design)
- [9. Form Handling](#9-form-handling)
- [10. Error Handling and Feedback](#10-error-handling-and-feedback)
- [11. Data Fetching](#11-data-fetching)
- [12. Internationalization (i18n)](#12-internationalization-i18n)
- [13. Animation and Transitions](#13-animation-and-transitions)
- [14. Build and Deployment](#14-build-and-deployment)

---

## 1. Component Architecture (Atomic Design)

* **Atomic Design is Mandatory:** Structure components following the [Atomic Design](https://bradfrost.com/blog/post/atomic-web-design/) methodology to enable systematic UI composition and reuse.
* **Component Hierarchy:**
    * **Atoms:** Foundational UI primitives (buttons, inputs, typography, icons). **MUST** be:
        * Highly reusable
        * Stateless or with minimal self-contained state
        * Focused on a single responsibility
        * Styled according to the design system
    * **Molecules:** Combinations of atoms forming small, functional units (form groups, search bars, menu items). **MUST**:
        * Compose atoms without knowledge of the larger context
        * Handle simple interactions between constituent atoms
        * Maintain cohesive functionality
    * **Organisms:** Complex UI sections combining molecules and atoms (navigation, forms, content cards). **MUST**:
        * Represent distinct sections of the interface
        * Encapsulate related functionality
        * Form a meaningful unit within the application interface
    * **Templates:** Page-level layout components defining content structure without specific data.
    * **Pages:** Concrete implementations of templates that bring together organisms with actual data.
* **Folder Structure:** Organize components by atomic level and domain, not technical type.

## 2. Component Development Workflow (Storybook-First)

* **Storybook-First Development is Mandatory:** Components **MUST** be designed, developed, and documented in [Storybook](https://storybook.js.org/) before integration into the application. This approach:
    * Enforces component-driven development
    * Ensures components work in isolation
    * Provides a living component library and documentation
    * Enables visual testing and review
* **Story Requirements:** Each component **MUST** have the following Storybook stories:
    * Default state/variant
    * All variant combinations (e.g., sizes, colors, states)
    * Interactive examples demonstrating behavior
    * Edge cases (long text, error states, loading states)
* **Storybook Documentation:** Component documentation in Storybook **MUST** include:
    * Purpose and usage
    * Props API documentation with types and descriptions
    * Usage examples
    * Any performance or accessibility considerations
* **Development Order:** The preferred component development workflow is:
    1. Define component requirements, API, and design
    2. Implement component with tests
    3. Create Storybook stories with documentation
    4. Review in isolation (UI, functionality, accessibility)
    5. Integrate into the application
* **Storybook Integration:** Storybook **MUST** be part of the CI pipeline, with:
    * Chromatic or similar visual testing
    * Accessibility checks (via addon-a11y)
    * Automated testing of component interactions

## 3. UI Library and Styling (shadcn/ui, Tailwind)

* **shadcn/ui as Foundation:** [shadcn/ui](https://ui.shadcn.com/) is our preferred component library foundation. It:
    * Provides accessible, customizable, and unstyled components
    * Follows best practices for component implementation
    * Integrates well with our atomic design approach
* **Extending shadcn/ui:** When extending shadcn/ui components:
    * Preserve accessibility features and behaviors
    * Maintain consistent API patterns
    * Document any deviations from standard shadcn/ui components
* **Styling with Tailwind CSS:** [Tailwind CSS](https://tailwindcss.com/) is our preferred styling approach. It:
    * Promotes design system consistency
    * Reduces CSS complexity and bundle size
    * Enables responsive design directly in components
    * Pairs well with shadcn/ui
* **CSS-in-JS Usage:** Avoid CSS-in-JS solutions except for dynamic styles that cannot be achieved with Tailwind. If required, use a zero-runtime solution like [vanilla-extract](https://vanilla-extract.style/).
* **Design Tokens:** Leverage Tailwind's theme configuration to define and enforce design tokens (colors, spacing, typography, etc.).
* **Dark Mode:** All components **MUST** support both light and dark modes.

## 4. Testing Strategy (Component, Integration, E2E)

* **Multi-Level Testing Approach:**
    * **Component Tests:** Unit tests for individual components (atoms, molecules)
    * **Integration Tests:** Tests for composite components (organisms, templates)
    * **E2E Tests:** Critical user flows and application behaviors
* **Component Testing Requirements:**
    * Use [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/) for component tests
    * Test behavior, not implementation details
    * Cover all component variants and states
    * Ensure accessibility in tests (a11y testing)
* **Integration Testing:** Verify that component compositions work correctly and handle data properly.
* **E2E Testing is Mandatory:** [Cypress](https://www.cypress.io/) or [Playwright](https://playwright.dev/) **MUST** be used to test critical user flows:
    * **Minimum Coverage:** All happy paths of core user journeys **MUST** have E2E test coverage
    * **Critical Error Paths:** Test important error scenarios (form validation, API failures)
    * **Visual Testing:** Integrate visual testing to catch unintended UI changes
* **Test Coverage Thresholds:**
    * Component tests: 90%+ for atoms and molecules
    * Integration tests: 85%+ for organisms and templates
    * E2E tests: 100% of critical user flows
* **Test Organization:** Co-locate tests with components. For E2E tests, organize by user flow or feature.

## 5. State Management

* **Minimalist State Management:** Following core principles of simplicity, use the most appropriate and minimal state management for the need:
    * **Component State:** Use React's `useState` for local component state
    * **Shared State:** Use React's Context API for state shared between related components
    * **Server State:** Use [TanStack Query](https://tanstack.com/query) (React Query) for server state and data fetching
    * **Form State:** Use [React Hook Form](https://react-hook-form.com/) for form state management
* **Global State:** For complex applications requiring global state, prefer [Zustand](https://github.com/pmndrs/zustand) or Redux Toolkit for:
    * Predictable state updates
    * DevTools integration
    * Time-travel debugging
* **State Architecture:**
    * **Colocation:** Keep state as close as possible to where it's used
    * **Immutability:** All state updates **MUST** follow immutable patterns
    * **Normalized State:** Complex relational data should be normalized
    * **Atomic Updates:** State updates should be atomic and targeted

## 6. Performance Optimization

* **Core Metrics (Web Vitals):** Applications **MUST** consistently meet or exceed scores for:
    * Largest Contentful Paint (LCP): < 2.5 seconds
    * First Input Delay (FID): < 100 milliseconds
    * Cumulative Layout Shift (CLS): < 0.1
* **Required Optimizations:**
    * **Code Splitting:** Use dynamic imports for route-based and component-based code splitting
    * **Image Optimization:** Use Next.js Image component or equivalent with proper sizing and formats
    * **Font Optimization:** Use Web fonts with proper loading strategies (preconnect, font-display)
    * **Asset Optimization:** Minimize and compress all assets (images, fonts, JS, CSS)
* **Component Rendering Optimization:**
    * **Memoization:** Use `React.memo`, `useMemo`, and `useCallback` judiciously for expensive operations
    * **Virtualization:** Use virtualization for long lists (react-window, react-virtualized)
    * **Lazy Loading:** Implement lazy loading for off-screen content
* **Measurement and Monitoring:**
    * Implement real user monitoring (RUM)
    * Regularly audit and benchmark performance
    * Set performance budgets and enforce them in CI

## 7. Accessibility (a11y)

* **WCAG Compliance is Mandatory:** Applications **MUST** meet [WCAG 2.1 AA](https://www.w3.org/WAI/WCAG21/quickref/) standards at minimum.
* **Key Requirements:**
    * **Keyboard Navigation:** All interactive elements must be accessible via keyboard
    * **Screen Reader Support:** Content must be properly structured for screen readers
    * **Color Contrast:** Text must meet minimum contrast ratios
    * **Focus Management:** Visible focus indicators and proper focus order
    * **ARIA Attributes:** Correct use of ARIA roles, states, and properties
* **Testing and Validation:**
    * Use automated tools (axe-core, jest-axe, Storybook a11y addon)
    * Conduct manual testing with keyboard and screen readers
    * Include people with disabilities in user testing when possible
* **Implementation Guidelines:**
    * Use semantic HTML elements
    * Implement proper heading hierarchy
    * Provide text alternatives for non-text content
    * Ensure sufficient color contrast
    * Design for different input methods

## 8. Responsive Design

* **Mobile-First Approach is Mandatory:** All components and layouts **MUST** be designed and implemented with a mobile-first approach.
* **Breakpoint System:** Standardize on Tailwind's breakpoint system:
    * `sm`: 640px
    * `md`: 768px
    * `lg`: 1024px
    * `xl`: 1280px
    * `2xl`: 1536px
* **Implementation Requirements:**
    * Use relative units (rem, em) instead of pixels for typography and spacing
    * Components must adapt appropriately across all breakpoints
    * Avoid fixed widths that can cause overflow
    * Test on actual devices or accurate device emulators
* **Content Requirements:**
    * Implement appropriate content prioritization for smaller screens
    * Use appropriately sized tap targets (minimum 44x44px)
    * Consider reduced motion preferences

## 9. Form Handling

* **Form Implementation:**
    * Use [React Hook Form](https://react-hook-form.com/) for form state management and validation
    * Leverage [Zod](https://github.com/colinhacks/zod) for schema validation
    * Ensure forms are accessible, with proper labels, error messages, and ARIA attributes
* **Required Features:**
    * Client-side validation with clear error messages
    * Server-side validation (duplicate check, business rules)
    * Loading states and submission feedback
    * Error recovery and field preservation
* **Form UX Guidelines:**
    * Inline validation at appropriate times (blur, submit)
    * Clear error messages near the relevant fields
    * Logical tab order and keyboard support
    * Appropriate input types for different data

## 10. Error Handling and Feedback

* **User-Facing Error Handling:**
    * Implement graceful error boundaries to prevent full UI crashes
    * Present friendly error messages with actionable steps
    * Log detailed errors for debugging (but never expose sensitive info to users)
* **Loading States:**
    * Provide visual feedback for all asynchronous operations
    * Use skeleton screens for initial content loading
    * Implement optimistic UI updates where appropriate
* **Success Feedback:**
    * Confirm successful actions visually and with screen reader announcements
    * Use toast notifications for non-critical confirmations
    * Use modal confirmations for critical actions
* **Empty States:**
    * Design explicit empty states for lists and data-driven views
    * Provide clear guidance on how to proceed from empty states

## 11. Data Fetching

* **Client-Side Data Fetching:**
    * Use [TanStack Query](https://tanstack.com/query) (React Query) for managing server state
    * Implement proper loading, error, and success states
    * Configure appropriate caching and revalidation strategies
* **Server-Side Rendering (SSR) and Static Generation:**
    * Leverage Next.js data fetching methods (getServerSideProps, getStaticProps)
    * Use Incremental Static Regeneration (ISR) where appropriate
    * Consider streaming SSR for large pages
* **API Design:**
    * Structure API endpoints by resource/domain
    * Implement consistent error responses
    * Standardize on a global fetch wrapper with error handling

## 12. Internationalization (i18n)

* **i18n Implementation:**
    * Use [next-intl](https://next-intl-docs.vercel.app/) or [react-i18next](https://react.i18next.com/) for translations
    * Extract all user-facing strings to translation files
    * Support RTL languages where required
* **Content Requirements:**
    * Handle pluralization and formatting (dates, numbers, currencies)
    * Support dynamic string interpolation
    * Accommodate varying text lengths in UI design

## 13. Animation and Transitions

* **Animation Principles:**
    * Use animation purposefully to enhance UX, not for decoration
    * Respect user preferences (`prefers-reduced-motion`)
    * Keep animations subtle and brief (150-300ms)
* **Implementation:**
    * Use CSS transitions for simple state changes
    * Use [Framer Motion](https://www.framer.com/motion/) for complex animations
    * Maintain 60fps performance
* **Standard Transitions:**
    * Page transitions
    * List item additions/removals
    * Modal/dialog entrances and exits
    * Hover/focus states

## 14. Build and Deployment

* **Build Optimization:**
    * Enable tree-shaking and code splitting
    * Implement aggressive caching strategies
    * Configure proper bundle analysis and optimization
* **Next.js Configuration:**
    * Leverage Next.js Image and Font optimization
    * Configure appropriate Next.js build outputs (static, SSR, ISR)
    * Use middleware judiciously for cross-cutting concerns
* **Deployment:**
    * Implement preview deployments for PRs
    * Configure proper environment variable management
    * Set up monitoring and error tracking (Sentry, LogRocket)
* **Core Web Vitals Verification:**
    * Measure and verify Web Vitals in CI/CD pipeline
    * Implement Lighthouse CI
    * Set performance budgets and treat violations as build failures
