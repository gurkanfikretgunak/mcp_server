---
name: typescript_test_generation
description: Generate comprehensive tests for TypeScript code
arguments:
  - name: file_path
    description: Path to TypeScript file to generate tests for
    required: true
  - name: test_framework
    description: Test framework - jest (default), vitest, or mocha
    required: false
    default: jest
---

Generate comprehensive tests for TypeScript code in '{file_path}'.
Test framework: {test_framework}

Include:
- Unit tests with proper typing
- Type testing (type assertions)
- Mocking with TypeScript types
- Edge cases and error handling
- Async/await testing

Follow TypeScript testing best practices:
- Use TypeScript in test files
- Proper type definitions for mocks
- Test type safety, not just runtime behavior
- Use type guards and assertions
