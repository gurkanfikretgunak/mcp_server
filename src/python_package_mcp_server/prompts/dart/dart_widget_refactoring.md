---
name: dart_widget_refactoring
description: Refactor Flutter widgets following best practices
arguments:
  - name: file_path
    description: Path to Dart file containing widgets
    required: true
  - name: refactoring_type
    description: Type - extract_widget, optimize_build, or state_management
    required: false
---

Refactor Flutter widgets in '{file_path}' following Dart/Flutter best practices.
{if refactoring_type}
Refactoring type: {refactoring_type}
{endif}

Focus on:
- Extracting reusable widgets
- Optimizing build methods (const, keys)
- Improving state management
- Following Effective Dart guidelines
- Widget composition and separation of concerns

Provide:
- Refactored code examples
- Explanation of improvements
- Performance benefits
- Testing considerations
