---
name: dart_test_generation
description: Generate comprehensive tests for Dart code
arguments:
  - name: file_path
    description: Path to Dart file to generate tests for
    required: true
  - name: test_framework
    description: Test framework - flutter_test (default) or test
    required: false
    default: flutter_test
---

Generate comprehensive tests for Dart code in '{file_path}'.
Test framework: {test_framework}

Include:
- Unit tests for functions and methods
- Widget tests for Flutter widgets
- Integration tests if applicable
- Edge cases and error handling
- Mocking strategies

Follow Dart testing best practices:
- Use descriptive test names
- Arrange-Act-Assert pattern
- Test both success and failure cases
- Proper use of setUp and tearDown
