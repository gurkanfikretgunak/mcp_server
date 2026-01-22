---
name: python_test_generation
description: Generate comprehensive tests for Python code
arguments:
  - name: file_path
    description: Path to Python file to generate tests for
    required: true
  - name: test_framework
    description: Test framework - pytest (default), unittest, or nose2
    required: false
    default: pytest
---

Generate comprehensive tests for Python code in '{file_path}'.
Test framework: {test_framework}

Include:
- Unit tests for functions and methods
- Test fixtures and setup/teardown
- Edge cases and error handling
- Mocking strategies (using unittest.mock or pytest-mock)
- Parametrized tests for multiple scenarios
- Integration tests if applicable

Follow Python testing best practices:
- Use descriptive test names (test_function_name_scenario)
- Arrange-Act-Assert pattern
- Test both success and failure cases
- Use pytest fixtures for test setup
- Mock external dependencies
- Aim for high test coverage
